#include "FuzzTreeTransform.h"
#include "FuzzTreeConfiguration.h"
#include "ExpressionParser.h"
#include "TreeHelpers.h"
#include "FuzzTreeTypes.h"
#include "FaultTreeTypes.h"

#include "xmlutil.h"
#include "configurationResult.h"

#include <xsd/cxx/tree/elements.hxx>
#include <xsd/cxx/xml/dom/serialization-header.hxx>
#include <boost/range/counting_range.hpp>

#include <functional>
#include "util.h"

using xercesc::DOMNode;
using xercesc::DOMDocument;
using namespace std;

FuzzTreeTransform::FuzzTreeTransform(const string& fuzzTreeXML, std::ofstream& logFile /* = DEFAULT_LOG_FILE*/) :
	m_count(0),
	m_bValid(true),
	m_logFile(logFile)
{
	try
	{
		m_fuzzTree = fuzztree::fuzzTree(fuzzTreeXML.c_str(), xml_schema::Flags::dont_validate);
		assert(m_fuzzTree.get());
	}
	catch (const xml_schema::Exception& e)
	{
		m_logFile << "Exception while reading: " << fuzzTreeXML << e << std::endl;
		m_bValid = false;
	}
}


FuzzTreeTransform::FuzzTreeTransform(std::istream& fuzzTreeXML, std::ofstream& logFile/* = DEFAULT_LOG_FILE*/) :
	m_count(0),
	m_bValid(true),
	m_logFile(logFile)
{
	try
	{
		m_fuzzTree = fuzztree::fuzzTree(fuzzTreeXML, xml_schema::Flags::dont_validate);
		assert(m_fuzzTree.get());
	}
	catch (const xml_schema::Exception& e)
	{
		m_logFile << "Exception while reading: " << fuzzTreeXML << e << std::endl;
		m_bValid = false;
	}
}

FuzzTreeTransform::FuzzTreeTransform(std::auto_ptr<fuzztree::FuzzTree> ft, std::ofstream& logFile/* = DEFAULT_LOG_FILE*/) :
	m_fuzzTree(ft),
	m_count(0),
	m_bValid(true),
	m_logFile(logFile)
{
	assert(m_fuzzTree.get());
}

FuzzTreeTransform::~FuzzTreeTransform()
{
	m_logFile.close();
}

bool FuzzTreeTransform::isOptional(const fuzztree::Node& node)
{
	const type_info& typeName = typeid(node);
	
	if (typeName != *fuzztreeType::INTERMEDIATEEVENT && !fuzztreeType::isLeaf(typeName)) 
		return false;
	
	const fuzztree::InclusionVariationPoint* inclusionNode =
		static_cast<const fuzztree::InclusionVariationPoint*>(&node);
	return inclusionNode->optional();
}


std::string FuzzTreeTransform::generateUniqueId(const std::string& oldId)
{
	return oldId + "." + treeHelpers::toString(++m_count);
}

/************************************************************************/
/* Generating all possible configurations initially                     */
/************************************************************************/

void FuzzTreeTransform::generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations)
{
	configurations.emplace_back(FuzzTreeConfiguration()); // default
	generateConfigurationsRecursive(&m_fuzzTree->topEvent(), configurations); // TODO handle errors here
}

ErrorType FuzzTreeTransform::generateConfigurationsRecursive(
	const fuzztree::Node* node, 
	std::vector<FuzzTreeConfiguration>& configurations)
{
	using namespace fuzztree;
	using namespace fuzztreeType;

	for (const auto& child : node->children())
	{
		const string id = child.id();
		const type_info& childType = typeid(child);
		
		if (isOptional(child))
		{ // inclusion variation point. Generate n + n configurations.
			vector<FuzzTreeConfiguration> additional;
			for (FuzzTreeConfiguration& config : configurations)
			{
				if (!config.isIncluded(id) || !config.isIncluded(node->id())) 
					continue;

				FuzzTreeConfiguration copied = config;
				// one configuration with this node
				copied.setOptionalEnabled(id, true);
				if (childType == *BASICEVENT || childType == *INTERMEDIATEEVENT)
					copied.setCost(copied.getCost() + parseCost(static_cast<const InclusionVariationPoint&>(child)));

				// one configuration without this node
				config.setOptionalEnabled(id, false);
				config.setNotIncluded(id);

				additional.emplace_back(copied);
			}
			configurations.insert(configurations.begin(), additional.begin(), additional.end());
		}

		if (childType == *REDUNDANCYVP)
		{ // any VotingOR with k in [from, to] and k=n-2. Generate n * #validVotingOrs configurations.
			const RedundancyVariationPoint* redundancyNode = static_cast<const RedundancyVariationPoint*>(&child);
			const int from = redundancyNode->start();
			const int to = redundancyNode->end();
			if (from < 0 || to < 0 || from > to)
			{
				m_logFile << 
					"Invalid Redundancy VP attributes, to: " << 
					util::toString(to) << ", from: " << util::toString(from)
					<< std::endl;
				return INVALID_ATTRIBUTE;
			}
			if (from == to) continue;

			const std::string formulaString = redundancyNode->formula();
			ExpressionParser<int> parser;
			const std::function<int(int)> formula = [&](int n) -> int
			{
				std::string fomulaStringTmp = formulaString;
				treeHelpers::replaceStringInPlace(fomulaStringTmp, "N", treeHelpers::toString(n));
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
		else
		{
			if (childType == *FEATUREVP)
			{ // exactly one subtree. Generate N * #Features configurations.
				const FeatureVariationPoint* featureNode = static_cast<const FeatureVariationPoint*>(&child);
				vector<FuzzTreeConfiguration::id_type> childIds;
				for (const auto& featuredChild : featureNode->children())
					childIds.emplace_back(featuredChild.id());

				if (childIds.empty())
				{
					m_logFile << "FeatureVP without children found: " << id << std::endl;
					return WRONG_CHILD_NUM;
				}

				vector<FuzzTreeConfiguration> newConfigs;
				for (FuzzTreeConfiguration& config : configurations)
				{
					if (config.isIncluded(id))
					{
						for (const auto& i : childIds)
						{
							FuzzTreeConfiguration copied = config;
							copied.setFeatureNumber(id, i);
							for (const auto& other : childIds)
								if (other != i) 
									copied.setNotIncluded(other);
							
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
			else if (isLeaf(childType))
			{
				continue; // end recursion
			}
		}
		generateConfigurationsRecursive(&child, configurations);
	}

	return OK;
}

/************************************************************************/
/* Generating fault trees from configurations                           */
/************************************************************************/

fuzztree::FuzzTree FuzzTreeTransform::generateVariationFreeFuzzTree(const FuzzTreeConfiguration& configuration)
{
	const fuzztree::TopEvent topEvent = m_fuzzTree->topEvent();

	// Create a new empty top event to fill up with the configuration
	fuzztree::TopEvent newTopEvent(topEvent.id());
	newTopEvent.missionTime(topEvent.missionTime());
	newTopEvent.decompositionNumber(topEvent.decompositionNumber());
	newTopEvent.name(topEvent.name());

	if (generateVariationFreeFuzzTreeRecursive(&topEvent, &newTopEvent, configuration) == OK)
		return fuzztree::FuzzTree(generateUniqueId(topEvent.id()), newTopEvent);
	else
	{
		m_logFile << "Error during FaultTree generation: " << endl;
		return fuzztree::FuzzTree("", newTopEvent); // TODO handle properly
	}
}

ErrorType FuzzTreeTransform::generateVariationFreeFuzzTreeRecursive(
	const fuzztree::Node* templateNode,
	fuzztree::Node* node,
	const FuzzTreeConfiguration& configuration)
{
	using namespace fuzztreeType;
	
	for (const auto& currentChild : templateNode->children())
	{
		const string id = currentChild.id();
		const type_info& typeName = typeid(currentChild);
		
		const bool opt = isOptional(currentChild);

		if (!configuration.isIncluded(id) || (opt && !configuration.isOptionalEnabled(id)))
			continue; // do not add this node

		bool bChanged = true;
		
		if (typeName == *REDUNDANCYVP)
		{ // TODO: probably this always ends up with a leaf node
			if (currentChild.children().size() > 1)
			{
				m_logFile << "Redundancy VP with multiple children found: " << id << std::endl;
				return WRONG_CHILD_NUM;
			}
			const auto& firstChild = currentChild.children().front();
			const type_info& childTypeName = typeid(firstChild);
			const auto kOutOfN = configuration.getRedundancyCount(id);

			fuzztree::VotingOr votingOrGate(id, get<0>(kOutOfN));
			if (childTypeName == *BASICEVENTSET)
			{
				const fuzztree::BasicEventSet& bes = 
					static_cast<const fuzztree::BasicEventSet&>(firstChild);

				expandBasicEventSet(&bes, &votingOrGate, get<1>(kOutOfN));
			}
			else if (childTypeName == *INTERMEDIATEEVENTSET)
			{
				const fuzztree::IntermediateEventSet& ies = 
					static_cast<const fuzztree::IntermediateEventSet&>(firstChild);

				expandIntermediateEventSet(&ies, &votingOrGate, configuration, get<1>(kOutOfN));
			}
			else
			{
				m_logFile << "Unrecognized Child Type: " << typeName.name() << std::endl;
				return WRONG_CHILD_TYPE;
			}
			node->children().push_back(votingOrGate);

			continue; // stop recursion
		}
		else if (typeName == *FEATUREVP)
		{
			if (handleFeatureVP(
				&currentChild, 
				node,
				configuration, 
				configuration.getFeaturedChild(id))) continue;

			bChanged = false;
		}
		else if (typeName == *BASICEVENTSET)
		{
			auto ret = expandBasicEventSet(&currentChild, node, 0);
			if (ret != OK) return ret;
			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == *INTERMEDIATEEVENTSET)
		{
			auto ret = expandIntermediateEventSet(&currentChild, node, configuration, 0);
			if (ret != OK)
				return ret;
			continue;
		}
		// remaining types
		else copyNode(typeName, node, id, currentChild);
		
		// break recursion
		// BasicEvents can have FDEP children...
		// continue;

		generateVariationFreeFuzzTreeRecursive(&currentChild, bChanged ? &node->children().back() : node, configuration);
	}

	return OK;
}

ErrorType FuzzTreeTransform::expandBasicEventSet(
	const fuzztree::Node* templateNode,
	fuzztree::Node* parentNode, 
	const int& defaultQuantity /*= 0*/)
{
	assert(parentNode && templateNode);

	const fuzztree::BasicEventSet* eventSet = static_cast<const fuzztree::BasicEventSet*>(templateNode);
	assert(eventSet);

	int numChildren = defaultQuantity;
	if (numChildren == 0 && eventSet->quantity().present())
		numChildren = eventSet->quantity().get();

	if (numChildren <= 0) return INVALID_ATTRIBUTE;

	const auto& prob = eventSet->probability();
	
	int i = 0;
	const auto eventSetId = eventSet->id();
	while (i < numChildren)
	{
		fuzztree::BasicEvent be(eventSetId + "." + treeHelpers::toString(i), prob);
		parentNode->children().push_back(be);
		i++;
	}

	return OK;
}

ErrorType FuzzTreeTransform::expandIntermediateEventSet(
	const fuzztree::Node* templateNode,
	fuzztree::Node* parentNode, 
	const FuzzTreeConfiguration& configuration,
	const int& defaultQuantity /*= 0*/)
{
	assert(parentNode && templateNode);

	const fuzztree::IntermediateEventSet* eventSet = static_cast<const fuzztree::IntermediateEventSet*>(templateNode);
	assert(eventSet);
	const auto eventSetId = eventSet->id();

	// barharhar
	const int numChildren = 
		defaultQuantity == 0 ? eventSet->quantity().present() ? eventSet->quantity().get() : defaultQuantity : defaultQuantity;

	if (numChildren <= 0) return INVALID_ATTRIBUTE;

	const auto& nextNode = eventSet->children().front();

	int i = 0;
	while (i < numChildren)
	{
		copyNode(typeid(nextNode), parentNode, eventSetId, nextNode);
		generateVariationFreeFuzzTreeRecursive(&nextNode, &parentNode->children().back(), configuration);
		i++;
	}

	return OK;
}

bool FuzzTreeTransform::handleFeatureVP(
	const fuzztree::ChildNode* templateNode,
	fuzztree::Node* node,
	const FuzzTreeConfiguration& configuration,
	const FuzzTreeConfiguration::id_type& configuredChildId)
{
	assert(node && templateNode);
	// find the configured child
	auto it = templateNode->children().begin();
	while (it != templateNode->children().end())
	{
		if (it->id() == configuredChildId)
			break;
		++it;
	}
	
	const auto featuredTemplate = *it;
	const type_info& featuredType = typeid(featuredTemplate);
	
	using namespace fuzztreeType;
	if (isOptional(featuredTemplate) && !configuration.isIncluded(configuredChildId))
	{
		return true;
	}
	else if (featuredType == *BASICEVENTSET)
	{
		expandBasicEventSet(&featuredTemplate, node, 0);
		return true;
	}
	else if (featuredType == *AND)		node->children().push_back(fuzztree::And(configuredChildId));
	else if (featuredType == *OR)		node->children().push_back(fuzztree::Or(configuredChildId));
	else if (featuredType == *VOTINGOR)
		node->children().push_back(fuzztree::VotingOr(configuredChildId, (static_cast<const fuzztree::VotingOr&>(featuredTemplate)).k()));
	else if (featuredType == *XOR)		node->children().push_back(fuzztree::Xor(configuredChildId));
	else if (isLeaf(featuredType))		node->children().push_back(fuzztree::BasicEvent(static_cast<const fuzztree::BasicEvent&>(featuredTemplate)));
	else if (isVariationPoint(featuredType))
	{
		return false;
	}
	return false;
}

std::vector<std::pair<FuzzTreeConfiguration, fuzztree::FuzzTree>>
	FuzzTreeTransform::transform()
{
	vector<std::pair<FuzzTreeConfiguration, fuzztree::FuzzTree>> results;
	try
	{
		if (!m_fuzzTree.get())
		{
			m_logFile << "Invalid FuzzTree." << endl;
			return results;
		}

		vector<FuzzTreeConfiguration> configs;
		generateConfigurations(configs);

		for (const auto& instanceConfiguration : configs)
		{
			results.emplace_back(
				std::make_pair(
				instanceConfiguration,
				generateVariationFreeFuzzTree(instanceConfiguration)));
		}
	}
	catch (xsd::cxx::exception& e)
	{
		m_logFile << "Parse Error: " << e.what() << endl;
	}
	catch (std::exception& e)
	{
		m_logFile << "Error during FuzzTree Transformation: " << e.what() << endl;
	}
	catch (...)
	{
		m_logFile << "Unknown Error during FuzzTree Transformation" << endl;
	}

	return results;
}

void FuzzTreeTransform::copyNode(
	const type_info& typeName, 
	fuzztree::Node* node, 
	const string id, 
	const fuzztree::ChildNode& currentChild)
{
	using namespace fuzztreeType;
	if (typeName == *AND)					node->children().push_back(fuzztree::And(id));
	else if (typeName == *OR)				node->children().push_back(fuzztree::Or(id));
	else if (typeName == *VOTINGOR)			node->children().push_back(fuzztree::VotingOr(id, (static_cast<const fuzztree::VotingOr&>(currentChild)).k()));
	else if (typeName == *XOR)				node->children().push_back(fuzztree::Xor(id));
	else if (typeName == *INTERMEDIATEEVENT) node->children().push_back(fuzztree::IntermediateEvent(id));
	else if (typeName == *BASICEVENT)		node->children().push_back(fuzztree::BasicEvent(static_cast<const fuzztree::BasicEvent&>(currentChild)));
	else assert(false);
}

void FuzzTreeTransform::generateConfigurationsFile(const std::string& outputXML)
{
	vector<FuzzTreeConfiguration> results;
	generateConfigurations(results);

	configurationResults::ConfigurationResults configResults;
	for (const FuzzTreeConfiguration& c : results)
	{
		configurationResults::Result r;
		r.configuration(serializedConfiguration(c));
		configResults.result().push_back(r);
	}

	std::ofstream output(outputXML);
	configurationResults::configurationResults(output, configResults);
}

xml_schema::Properties FuzzTreeTransform::validationProperties()
{
	static const string fuzztreeSchema = "FUZZTREEXSD"; // Path to schema from CMakeLists.txt
	assert(!fuzztreeSchema.empty());

	xml_schema::Properties props;
	props.schema_location("ft", fuzztreeSchema);
	props.no_namespace_schema_location(fuzztreeSchema);

	return props;
}

int FuzzTreeTransform::parseCost(const fuzztree::InclusionVariationPoint& node)
{
	auto c = node.costs();
	if (c.present())
		return c.get();
	return 0;
}
