#include "FuzzTreeTransform.h"
#include "Constants.h"
#include "FuzzTreeConfiguration.h"

#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <boost/filesystem/operations.hpp>
#include <boost/range/counting_range.hpp>
#include <exception>
#include <iostream>
#include "ExpressionParser.h"
#if IS_WINDOWS
#pragma warning(pop) 
#endif
#include "util.h"

#include <omp.h>

using namespace pugi;
using namespace std;
using namespace fuzzTree;
using namespace faultTree;
using namespace boost;

const char* const DUMMY = "dummy";

void FuzzTreeTransform::transformFuzzTree(const string& fileName, const string& targetDir) noexcept
{
	try
	{
		FuzzTreeTransform transform(fileName, targetDir);
		if (!transform.validateAndLoad())
		{
			cout << "Could not load FuzzTree" << endl;
			return;
		}
		
		vector<FuzzTreeConfiguration> configs;
		transform.generateConfigurations(configs);
		
		for (const auto& instanceConfiguration : configs)
		{
			boost::function<void()> generationTask = boost::bind(
				&FuzzTreeTransform::generateFaultTree, &transform, instanceConfiguration);
			
			transform.scheduleFTGeneration(generationTask);
		}
	}
	catch (std::exception& e)
	{
		cout << "Error during FuzzTree Transformation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Error during FuzzTree Transformation" << endl;
	}
}

FuzzTreeTransform::FuzzTreeTransform(const string& fileName, const string& targetDir)
	: XMLImport(fileName), 
	m_targetDir(targetDir), 
	m_count(0)
{
	if (!filesystem::is_directory(targetDir))
		EXIT_ERROR(string("Directory ") + targetDir + " not found.");
	
	else if (!filesystem::is_regular_file(fileName))
		EXIT_ERROR(string("File ") + fileName + " not found.");

	m_threadPool = threadpool::fifo_pool(omp_get_max_threads()-1); // TODO
}

FuzzTreeTransform::~FuzzTreeTransform()
{
	m_threadPool.wait();
	m_threadPool.clear();
}

bool FuzzTreeTransform::loadRootNode()
{
	m_rootNode = m_document.child(FUZZ_TREE);
	if (!m_rootNode)
		EXIT_ERROR("Missing Fuzztree Root Node");
	return true;
}

void FuzzTreeTransform::shallowCopy(const xml_node& proto, xml_node& copiedNode)
{
	copiedNode.set_name(proto.name());
	copiedNode.set_value(proto.value());

	for (auto attr = proto.attributes_begin(); attr != proto.attributes_end(); ++attr)
	{
		copiedNode.append_attribute(attr->name()).set_value(attr->value());
	}
}

bool FuzzTreeTransform::isGate(const string& typeDescriptor)
{ // all gates which do not lead to additional configuration branching
	return
		typeDescriptor == AND_GATE ||
		typeDescriptor == OR_GATE ||
		typeDescriptor == XOR_GATE ||
		typeDescriptor == VOTING_OR_GATE ||
		typeDescriptor == PAND_GATE ||
		typeDescriptor == COLD_SPARE_GATE;
}

void FuzzTreeTransform::generateConfigurations(vector<FuzzTreeConfiguration>& configs) const
{
	xml_node topEventNode = m_rootNode.child(TOP_EVENT);
	assert(!topEventNode.empty());

	configs.emplace_back(FuzzTreeConfiguration()); // default
	generateConfigurationsRecursive(topEventNode, configs);
}

// TODO refactor?
void FuzzTreeTransform::generateConfigurationsRecursive(
	const xml_node& fuzzTreeNode, 
	vector<FuzzTreeConfiguration>& configurations) const
{
	for (const auto& child : fuzzTreeNode.children(CHILDREN))
	{
		const int id		= parseID(child);
		const bool opt		= child.attribute(OPTIONAL_ATTRIBUTE).as_bool(false);

		if (id < 0)
			continue;

		const string typeDescriptor = child.attribute(NODE_TYPE).as_string();

		if (opt)
		{ // inclusion variation point. Generate n + n configurations.
			vector<FuzzTreeConfiguration> additional;
			for (FuzzTreeConfiguration& config : configurations)
			{
				if (!config.isIncluded(id) || !config.isIncluded(parseID(fuzzTreeNode)))
					continue;

				FuzzTreeConfiguration copied = config;
				copied.setNodeOptional(id, true);
				config.setNodeOptional(id, false);
				config.setNotIncluded(id);

				additional.emplace_back(copied);
			}
			configurations.insert(configurations.begin(), additional.begin(), additional.end());
		}

		if (typeDescriptor == REDUNDANCY_VP)
		{ // any VotingOR with k in [from, to] and k=n-2. Generate n * #validVotingOrs configurations.
			const int from = child.attribute("start").as_int(-1);
			const int to = child.attribute("end").as_int(-1);
			if (from < 0 || to < 0 || from > to)
				throw runtime_error("Invalid boundaries for RedundancyGate");

			if (from == to) continue;

			const std::string formulaString = child.attribute(REDUNDANCY_FORMULA).as_string();
			ExpressionParser<int> parser;
			const std::function<int(int)> formula = [&](int n) -> int
			{
				std::string fomulaStringTmp = formulaString;
				util::replaceStringInPlace(fomulaStringTmp, "N", util::toString(n));
				return parser.eval(fomulaStringTmp);
			};

			vector<FuzzTreeConfiguration> newConfigs;
			for (FuzzTreeConfiguration& config : configurations)
			{
				if (config.isIncluded(id))
				{
					for (int i : boost::counting_range(from, to+1))
					{
						FuzzTreeConfiguration copied = config;
						const int numVotes = formula(i);
						if (numVotes <= 0)
							continue;
						copied.setRedundancyNumber(id, numVotes, i);
						newConfigs.emplace_back(copied);
					}
				}
				else
					newConfigs.emplace_back(config); // keep config as it is
			}
			
			if (!newConfigs.empty())
			{
				assert(newConfigs.size() >= configurations.size());
				configurations.assign(newConfigs.begin(), newConfigs.end());
			}
		}
		else if (typeDescriptor == FEATURE_VP)
		{ // exactly one subtree. Generate N * #Features configurations.
			vector<int> childIds;
			for (const auto& featuredChild : child.children(CHILDREN))
				childIds.emplace_back(featuredChild.attribute(ID_ATTRIBUTE).as_int(-1));
			
			if (childIds.empty())
			{
				throw runtime_error("Feature Variation Points need child nodes");
				continue;
			}

			vector<FuzzTreeConfiguration> newConfigs;
			for (FuzzTreeConfiguration& config : configurations)
			{
				if (config.isIncluded(id))
				{
					for (const int& i : childIds)
					{
						FuzzTreeConfiguration copied = config;
						copied.setFeatureNumber(id, i);
						for (const int& other : childIds)
						{
							if (other != i)
								copied.setNotIncluded(other);
						}
						newConfigs.emplace_back(copied);
					}
				}
				else
					newConfigs.emplace_back(config); // keep config as it is
			}
			
			if (!newConfigs.empty())
			{
				assert(newConfigs.size() >= configurations.size());
				configurations.assign(newConfigs.begin(), newConfigs.end());
			}
		}
		else if (isLeaf(typeDescriptor))
		{
			// end recursion
			continue;
		}
		generateConfigurationsRecursive(child, configurations);
	}
}

void FuzzTreeTransform::generateFaultTree(const FuzzTreeConfiguration& configuration)
{
	const xml_node topEvent = m_rootNode.child(TOP_EVENT);
	const char* name = m_rootNode.attribute(NAME_ATTRIBUTE).as_string();
	const char* id = m_rootNode.attribute(ID_ATTRIBUTE).as_string();
	
	assert(!topEvent.empty());

	xml_document* const newDoc = new xml_document();
	xml_node faultTree = newDoc->append_child(FAULT_TREE);
	faultTree.append_attribute(NAME_ATTRIBUTE).set_value(name);
	faultTree.append_attribute(ID_ATTRIBUTE).set_value(generateUniqueId(id).c_str());

	// TODO attributes
	xml_node newTopEvent = faultTree.append_child(TOP_EVENT);
	shallowCopy(topEvent, newTopEvent);
	
	generateFaultTreeRecursive(topEvent, newTopEvent, configuration);
	removeEmptyNodes(newTopEvent);

	newDoc->save_file(uniqueFileName().c_str());
}

void FuzzTreeTransform::scheduleFTGeneration(boost::function<void()>& task)
{ // does this even make sense??
	//m_threadPool.schedule(task);
	task();
}

void FuzzTreeTransform::generateFaultTreeRecursive(
	const xml_node& templateNode,
	xml_node& faultTreeNode,
	const FuzzTreeConfiguration& configuration) const
{
	for (const auto& currentChild : templateNode.children(CHILDREN))
	{
		const int		id	= parseID(currentChild);
		const bool		opt	= currentChild.attribute(OPTIONAL_ATTRIBUTE).as_bool(false);
		
		if (id < 0 || !configuration.isIncluded(id) || (opt && !configuration.isOptionalEnabled(id)))
		{
			continue; // do not add this node
		}

		const string	typeDescriptor = currentChild.attribute(NODE_TYPE).as_string();		
		const bool		bLeaf = isLeaf(typeDescriptor);

		xml_node newNode;
		if (typeDescriptor == REDUNDANCY_VP)
		{
			const tuple<int,int> configuredN = configuration.getRedundancyCount(id);
			auto result = handleRedundancyVP(currentChild, faultTreeNode, configuredN, id); // returns a VotingOR Gate
			newNode = result.first;

			if (result.second)
				continue; // stop recursion
		}
		else if (typeDescriptor == FEATURE_VP)
		{
			const int configuredChildID = configuration.getFeaturedChild(id);
			auto result = handleFeatureVP(currentChild, faultTreeNode, configuration, configuredChildID);
			newNode = result.first;
			
			if (result.second)
				continue; // stop recursion
		}
		else if (typeDescriptor == BASIC_EVENT_SET)
		{ // TODO forbid quantity parameter in basic event sets below Redundancy VP
			expandBasicEventSet(currentChild, faultTreeNode, id, 0);
			continue;
		}
		else
		{
			if (isGate(typeDescriptor))
			{ // don't copy children yet
				newNode = faultTreeNode.append_child(CHILDREN);
				shallowCopy(currentChild, newNode);
			}
			else if (bLeaf)
			{ // copy everything including probability child node
				newNode = faultTreeNode.append_copy(currentChild);
			}
			SET_OPTIONAL_FALSE(newNode);
		}

		// break recursion
		if (bLeaf)	continue;

		else if (!HAS_CHILDREN(currentChild))
			faultTreeNode.remove_child(newNode);
		
		generateFaultTreeRecursive(currentChild, newNode, configuration);
	}
}

bool FuzzTreeTransform::isLeaf(const string& typeDescriptor)
{
	return 
		typeDescriptor == BASIC_EVENT || 
		typeDescriptor == UNDEVELOPED_EVENT;
}

const std::string FuzzTreeTransform::uniqueFileName() const
{
	boost::filesystem::path slash("/");
	const string sSlash = slash.make_preferred().string();
	
	string fn = 
		m_targetDir.generic_string() + sSlash +
		m_file.filename().generic_string();
	
	util::replaceFileExtensionInPlace(fn, "");
	return fn + util::toString(m_count) + FAULT_TREE_EXT;
}

// the second return value is true if the recursion should terminate below the gate
// (i.e. there was a basic event set)

pair<xml_node,bool> FuzzTreeTransform::handleRedundancyVP(
	const xml_node& templateNode, 
	xml_node& node,
	const tuple<int,int> kOutOfN, const int& id) const
{
	if (string(node.name()) == DUMMY)
		node.set_name(CHILDREN);

	xml_node votingOR = node.append_child(CHILDREN);
	votingOR.append_attribute(NODE_TYPE).set_value(VOTING_OR_GATE);
	
	const xml_node child = templateNode.child(CHILDREN); // TODO: allow only one child below RedundancyVP	
	if (child.empty())
	{
		assert(false);
		return make_pair(votingOR, true);
	}

	const string typeDescriptor = child.attribute(NODE_TYPE).as_string();

	if (typeDescriptor == BASIC_EVENT_SET)
	{
		votingOR.append_attribute(ID_ATTRIBUTE).set_value(id);
		votingOR.append_attribute(VOTING_OR_K).set_value(get<0>(kOutOfN));
		expandBasicEventSet(child, votingOR, id, get<1>(kOutOfN));
		return make_pair(votingOR, true);
	}
	else
	{
		throw runtime_error("Child of Redundancy VP must be an event set");
	}

	return make_pair(votingOR, false);
}

void FuzzTreeTransform::expandBasicEventSet(
	const xml_node& templateNode, 
	xml_node& parent,
	const int& id,
	const int& defaultQuantity) const
{
	const int numChildren = defaultQuantity == 0 ? 
		templateNode.attribute(BASIC_EVENT_SET_QUANTITY).as_int(defaultQuantity) : defaultQuantity;

	if (numChildren <= 0)
	{
		throw runtime_error("Invalid Quantity in Basic Event Set");
	}
	xml_node probabilityNode = templateNode.child("probability");
	if (probabilityNode.empty())
	{
		assert(false);
		return;
	}

	int i = 0;
	while (i < numChildren)
	{
		xml_node basicEvent = parent.append_child("children");
		basicEvent.append_attribute(NODE_TYPE).set_value(BASIC_EVENT);
		basicEvent.append_attribute(ID_ATTRIBUTE).set_value(util::nestedIDString(2, id, i).c_str());
		basicEvent.append_copy(probabilityNode);
		i++;
	}
}

pair<xml_node, bool /*isLeaf*/> FuzzTreeTransform::handleFeatureVP(
	const xml_node& templateNode, 
	xml_node& node,
	const FuzzTreeConfiguration& configuration,
	const int configuredChildId) const
{
	// find the configured child
	xml_node featuredTemplate;
	for (auto& child : templateNode.children("children"))
	{
		if (parseID(child) == configuredChildId)
		{
			featuredTemplate = child;
			break;
		}
	}
	assert(!featuredTemplate.empty());

	xml_node newFeatured = node.append_child(DUMMY);
	const string configuredChildType = featuredTemplate.attribute(NODE_TYPE).as_string();
	const bool opt = featuredTemplate.attribute(OPTIONAL_ATTRIBUTE).as_bool();
	if (opt && !configuration.isIncluded(configuredChildId))
	{
		return make_pair(newFeatured, true);
	}
	if (configuredChildType == BASIC_EVENT_SET)
	{ 
		expandBasicEventSet(featuredTemplate, node, configuredChildId, 0);
		return make_pair(node, true);
	}
	else if (configuredChildType == BASIC_EVENT)
	{
		newFeatured = node.append_copy(featuredTemplate);
		SET_OPTIONAL_FALSE(newFeatured);
		return make_pair(newFeatured, true);
	}
	else if (isGate(configuredChildType))
	{
		newFeatured = node.append_child("children");
		shallowCopy(featuredTemplate, newFeatured);
		return make_pair(newFeatured, false);
	}
	else if (configuredChildType == FEATURE_VP)
	{
		return make_pair(node, false);
	}
	else
	{
		//???
	}
	return make_pair(newFeatured, false);
}

int FuzzTreeTransform::parseID(const xml_node& node)
{
	return node.attribute(ID_ATTRIBUTE).as_int(-1);
}

void FuzzTreeTransform::removeEmptyNodes(xml_node& node)
{
	for (auto& child : node.children())
	{
		if (string(child.name()) == DUMMY)
		{
			assert(child.children().begin() == child.children().end());
			node.remove_child(child);
		}
		removeEmptyNodes(child);
	}
}

std::string FuzzTreeTransform::generateUniqueId(const char* oldId)
{
	return string(oldId) + "." + util::toString(++m_count);
}
