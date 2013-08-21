#include "FuzzTreeTransform.h"
#include "FuzzTreeConfiguration.h"
#include "ExpressionParser.h"
#include "TreeHelpers.h"
#include "FuzzTreeTypes.h"
#include "FaultTreeTypes.h"

#include <xsd/cxx/tree/elements.hxx>
#include <xsd/cxx/xml/dom/serialization-header.hxx>

#include <functional>

using xercesc::DOMNode;
using xercesc::DOMDocument;
using namespace std;

FuzzTreeTransform::FuzzTreeTransform(const string& fuzzTreeXML) :
	m_count(0)
{
	static const string fuzztreeSchema = FUZZTREEXSD; // Path to schema from CMakeLists.txt
	assert(!fuzztreeSchema.empty());

	xml_schema::Properties props;
	props.schema_location("ft", fuzztreeSchema);
	props.no_namespace_schema_location(fuzztreeSchema);

	try
	{
		m_fuzzTree = fuzztree::fuzzTree(fuzzTreeXML.c_str(), xml_schema::Flags::dont_validate);//fuzztree::fuzzTree(fuzzTreeXML.c_str(), 0, props);
		assert(m_fuzzTree.get());
	}
	catch (const xml_schema::Exception& e)
	{
		std::cout << e.what() << std::endl;
	}
}


FuzzTreeTransform::FuzzTreeTransform(std::istream& fuzzTreeXML)
{
	static const string fuzztreeSchema = FUZZTREEXSD; // Path to schema from CMakeLists.txt
	assert(!fuzztreeSchema.empty());

	xml_schema::Properties props;
	props.schema_location("ft", fuzztreeSchema);
	props.no_namespace_schema_location(fuzztreeSchema);

	try
	{
		m_fuzzTree = fuzztree::fuzzTree(fuzzTreeXML, xml_schema::Flags::dont_validate);
		assert(m_fuzzTree.get());
	}
	catch (const xml_schema::Exception& e)
	{
		std::cout << e.what() << std::endl;
	}
}

FuzzTreeTransform::~FuzzTreeTransform()
{}

/************************************************************************/
/* Utility methods                                                      */
/************************************************************************/

bool FuzzTreeTransform::isGate(const string& typeName)
{
	using namespace fuzztreeType;
	return
		typeName == AND ||
		typeName == OR ||
		typeName == XOR ||
		typeName == VOTINGOR;
}

bool FuzzTreeTransform::isLeaf(const string& typeName)
{
	using namespace fuzztreeType;
	return
		typeName == BASICEVENT ||
		typeName == HOUSEEVENT ||
		typeName == UNDEVELOPEDEVENT ||
		typeName == BASICEVENTSET;
}


bool FuzzTreeTransform::isVariationPoint(const string& typeName)
{
	using namespace fuzztreeType;
	return
		typeName == FEATUREVP ||
		typeName == REDUNDANCYVP;
}



bool FuzzTreeTransform::isEventSet(const std::string& typeName)
{
	using namespace fuzztreeType;
	return
		typeName == BASICEVENTSET ||
		typeName == INTERMEDIATEEVENTSET;
}


bool FuzzTreeTransform::isOptional(const fuzztree::Node& node)
{
	const string typeName = typeid(node).name();
	if (typeName != fuzztreeType::INTERMEDIATEEVENT && !isLeaf(typeName)) 
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

void FuzzTreeTransform::generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const
{
	configurations.emplace_back(FuzzTreeConfiguration()); // default
	generateConfigurationsRecursive(&m_fuzzTree->topEvent(), configurations); // TODO handle errors here
}

ErrorType FuzzTreeTransform::generateConfigurationsRecursive(
	const fuzztree::Node* node, std::vector<FuzzTreeConfiguration>& configurations) const
{
	using namespace fuzztree;
	using namespace fuzztreeType;

	const string parentType = typeid(node).name();

	for (const auto child : node->children())
	{
		const string id = child.id();
		const string childType = typeid(child).name();
		
		if (isOptional(child))
		{ // inclusion variation point. Generate n + n configurations.
			vector<FuzzTreeConfiguration> additional;
			for (FuzzTreeConfiguration& config : configurations)
			{
				if (!config.isIncluded(id) || !config.isIncluded(node->id())) 
					continue;

				FuzzTreeConfiguration copied = config;
				copied.setNodeOptional(id, true);
				config.setNodeOptional(id, false);
				config.setNotIncluded(id);

				additional.emplace_back(copied);
			}
			configurations.insert(configurations.begin(), additional.begin(), additional.end());
		}

		if (childType == REDUNDANCYVP)
		{ // any VotingOR with k in [from, to] and k=n-2. Generate n * #validVotingOrs configurations.
			const RedundancyVariationPoint* redundancyNode = static_cast<const RedundancyVariationPoint*>(&child);
			const int from = redundancyNode->start();
			const int to = redundancyNode->end();
			if (from < 0 || to < 0 || from > to)
				return INVALID_ATTRIBUTE;

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
					for (int i = from; i < to+1; ++i)
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
			if (childType == FEATUREVP)
			{ // exactly one subtree. Generate N * #Features configurations.
				const FeatureVariationPoint* featureNode = static_cast<const FeatureVariationPoint*>(&child);
				vector<FuzzTreeConfiguration::id_type> childIds;
				for (const auto& featuredChild : featureNode->children())
					childIds.emplace_back(featuredChild.id());

				if (childIds.empty()) return WRONG_CHILD_NUM;

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

faulttree::FaultTree FuzzTreeTransform::generateFaultTree(const FuzzTreeConfiguration& configuration)
{
	const fuzztree::TopEvent topEvent = m_fuzzTree->topEvent();
	auto newTopEvent = treeHelpers::copyTopEvent(topEvent);

	if (generateFaultTreeRecursive(&topEvent, &newTopEvent, configuration) == OK)
		return faulttree::FaultTree(generateUniqueId(topEvent.id()), newTopEvent);
	else
	{
		cout << "Error during FaultTree generation: " << endl;
		return faulttree::FaultTree("", newTopEvent); // TODO handle properly
	}
}

ErrorType FuzzTreeTransform::generateFaultTreeRecursive(
	const fuzztree::Node* templateNode,
	faulttree::Node* node,
	const FuzzTreeConfiguration& configuration) const
{
	using namespace fuzztreeType;
	
	for (const auto& currentChild : templateNode->children())
	{
		const string id = currentChild.id();
		const string typeName = typeid(currentChild).name();
		
		const bool opt = isOptional(currentChild);

		if (!configuration.isIncluded(id) || (opt && !configuration.isOptionalEnabled(id)))
			continue; // do not add this node

		const bool bLeaf = isLeaf(typeName);
		bool bChanged = true;
		
		if (typeName == REDUNDANCYVP)
		{ // TODO: probably this always ends up with a leaf node
			if (currentChild.children().size() > 1)
				return WRONG_CHILD_NUM;

			const auto& firstChild = currentChild.children().front();
			const string childTypeName = typeid(firstChild).name();
			const auto kOutOfN = configuration.getRedundancyCount(id);

			faulttree::VotingOr votingOrGate(id, get<0>(kOutOfN));
			if (childTypeName == BASICEVENTSET)
			{
				const fuzztree::BasicEventSet& bes = 
					static_cast<const fuzztree::BasicEventSet&>(firstChild);

				expandBasicEventSet(&bes, &votingOrGate, id, get<1>(kOutOfN));
			}
			else if (childTypeName == INTERMEDIATEEVENTSET)
			{
				const fuzztree::IntermediateEventSet& ies = 
					static_cast<const fuzztree::IntermediateEventSet&>(firstChild);

				expandIntermediateEventSet(&ies, &votingOrGate, id, configuration, get<1>(kOutOfN));
			}
			else return WRONG_CHILD_TYPE;
			
			node->children().push_back(votingOrGate);

			continue; // stop recursion
		}
		else if (typeName == FEATUREVP)
		{
			if (handleFeatureVP(
				&currentChild, 
				node,
				configuration, 
				configuration.getFeaturedChild(id))) continue;

			bChanged = false;
		}
		else if (typeName == BASICEVENTSET)
		{
			auto ret = expandBasicEventSet(&currentChild, node, id, 0);
			if (ret != OK) return ret;
			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == INTERMEDIATEEVENTSET)
		{
			auto ret = expandIntermediateEventSet(&currentChild, node, id, configuration, 0);
			if (ret != OK) return ret;
			continue;
		}
		// remaining types
		else copyNode(typeName, node, id, currentChild);
		
		// break recursion
		// BasicEvents can have FDEP children...
		// continue;

		generateFaultTreeRecursive(&currentChild, bChanged ? &node->children().back() : node, configuration);
	}

	return OK;
}

ErrorType FuzzTreeTransform::expandBasicEventSet(
	const fuzztree::Node* templateNode,
	faulttree::Node* parentNode, 
	const FuzzTreeConfiguration::id_type& id,
	const int& defaultQuantity /*= 0*/) const
{
	assert(parentNode && templateNode);

	const fuzztree::BasicEventSet* eventSet = static_cast<const fuzztree::BasicEventSet*>(templateNode);
	assert(eventSet);

	// barharhar
	const int numChildren = 
		defaultQuantity == 0 ? eventSet->quantity().present() ? eventSet->quantity().get() : defaultQuantity : defaultQuantity;

	if (numChildren <= 0) return INVALID_ATTRIBUTE;

	const auto& prob = eventSet->probability();
	const auto& probType = typeid(prob).name();

	faulttree::Probability copiedProb;
	if (probType == fuzztreeType::CRISPPROB)
		copiedProb = faulttree::CrispProbability(static_cast<const fuzztree::CrispProbability&>(prob).value());
	else if (probType == fuzztreeType::FAILURERATE)
		copiedProb = faulttree::FailureRate(static_cast<const fuzztree::FailureRate&>(prob).value());
	else
		copiedProb = faulttree::FailureRate(0.0); 

	int i = 0;
	const auto eventSetId = eventSet->id();
	while (i < numChildren)
	{
		faulttree::BasicEvent be(eventSetId + "." + treeHelpers::toString(i), copiedProb);
		parentNode->children().push_back(be);
		i++;
	}

	return OK;
}

ErrorType FuzzTreeTransform::expandIntermediateEventSet(
	const fuzztree::Node* templateNode,
	faulttree::Node* parentNode, 
	const FuzzTreeConfiguration::id_type& id,
	const FuzzTreeConfiguration& configuration,
	const int& defaultQuantity /*= 0*/) const
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
		copyNode(typeid(nextNode).name(), parentNode, eventSetId, nextNode);
		generateFaultTreeRecursive(&nextNode, &parentNode->children().back(), configuration);
		i++;
	}

	return OK;
}

bool FuzzTreeTransform::handleFeatureVP(
	const fuzztree::ChildNode* templateNode,
	faulttree::Node* node,
	const FuzzTreeConfiguration& configuration,
	const FuzzTreeConfiguration::id_type& configuredChildId) const
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
	
	const fuzztree::ChildNode featuredTemplate = *it;
	const string featuredTypeName = typeid(featuredTemplate).name();
	
	using namespace fuzztreeType;
	if (isOptional(featuredTemplate) && !configuration.isIncluded(configuredChildId))
	{
		return true;
	}
	else if (featuredTypeName == BASICEVENTSET)
	{
		expandBasicEventSet(&featuredTemplate, node, configuredChildId, 0);
		return true;
	}
	else if (featuredTypeName == AND)		node->children().push_back(faulttree::And(configuredChildId));
	else if (featuredTypeName == OR)		node->children().push_back(faulttree::Or(configuredChildId));
	else if (featuredTypeName == VOTINGOR)	node->children().push_back(faulttree::VotingOr(configuredChildId, (static_cast<const fuzztree::VotingOr&>(featuredTemplate)).k()));
	else if (featuredTypeName == XOR)		node->children().push_back(faulttree::Xor(configuredChildId));
	else if (isLeaf(featuredTypeName))		node->children().push_back(treeHelpers::copyBasicEvent(static_cast<const fuzztree::BasicEvent&>(featuredTemplate)));
	else if (isVariationPoint(featuredTypeName))
	{
		return false;
	}
	return false;
}

bool FuzzTreeTransform::handleRedundancyVP(
	const fuzztree::ChildNode* templateNode,
	faulttree::Node* node,
	const tuple<int,int> kOutOfN,
	const FuzzTreeConfiguration::id_type& id) const
{
	assert(node && templateNode);

	
	return true;
}

std::vector<faulttree::FaultTree> FuzzTreeTransform::transform()
{
	try
	{
		vector<faulttree::FaultTree> results;
		if (!m_fuzzTree.get())
		{
			cout << "Invalid Fuzztree." << endl;
			return results;
		}

		vector<FuzzTreeConfiguration> configs;
		generateConfigurations(configs);

		int indent = 0;
		treeHelpers::printTree(m_fuzzTree->topEvent(), indent);
		cout << endl << " ...... configurations: ...... " << endl;

		for (const auto& instanceConfiguration : configs)
		{
			auto ft = generateFaultTree(instanceConfiguration);
			indent = 0;
			treeHelpers::printTree(ft.topEvent(), indent);
			cout << endl;

			results.emplace_back(ft);
		}

		return results;
	}
	catch (xsd::cxx::exception& e)
	{
		cout << "Parse Error: " << e.what() << endl;
	}
	catch (std::exception& e)
	{
		cout << "Error during FuzzTree Transformation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Error during FuzzTree Transformation" << endl;
	}

	return vector<faulttree::FaultTree>();
}

void FuzzTreeTransform::copyNode(
	const string typeName, 
	faulttree::Node* node, 
	const string id, 
	const fuzztree::ChildNode& currentChild)
{
	using namespace fuzztreeType;
	if (typeName == AND)					node->children().push_back(faulttree::And(id));
	else if (typeName == OR)				node->children().push_back(faulttree::Or(id));
	else if (typeName == VOTINGOR)			node->children().push_back(faulttree::VotingOr(id, (static_cast<const fuzztree::VotingOr&>(currentChild)).k()));
	else if (typeName == XOR)				node->children().push_back(faulttree::Xor(id));
	else if (typeName == INTERMEDIATEEVENT) node->children().push_back(faulttree::IntermediateEvent(id));
	else if (typeName == BASICEVENT)		node->children().push_back(treeHelpers::copyBasicEvent(static_cast<const fuzztree::BasicEvent&>(currentChild)));
	else assert(false);
}
