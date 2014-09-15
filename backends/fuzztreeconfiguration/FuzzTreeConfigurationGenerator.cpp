#include "FuzzTreeConfigurationGenerator.h"
#include "FuzzTreeConfiguration.h"
#include "FatalException.h"
#include "ExpressionParser.h"

#include "RedundancyVariationPoint.h"
#include "FeatureVariationPoint.h"
#include "BasicEventSet.h"

#include "xmlutil.h"

#include <boost/range/counting_range.hpp>

#include <functional>
#include <unordered_set>
#include "util.h"

using namespace std;


bool isGate(const std::string& typeName)
{
	return
		typeName == "andGate"||
		typeName == "orGate" ||
		typeName == "xorGate" ||
		typeName == "votingOrGate";
}

bool isLeaf(const std::string& typeName)
{
	return
		typeName == "basicEvent"||
		typeName == "houseEvent" ||
		typeName == "UndevelopedEvent" ||
		typeName == "basicEventSet";
}


bool isVariationPoint(const std::string& typeName)
{
	return
		typeName == "featureVariationPoint" ||
		typeName == "redundancyVariationPoint";
}

bool isEventSet(const std::string& typeName)
{
	return
		typeName == "basicEventSet" ||
		typeName == "IntermediateEventSet";
}

FuzzTreeTransform::FuzzTreeTransform(
	const string& fuzzTreeXML, 
	std::set<Issue>& errors) :
	m_count(0),
	m_bValid(true),
	m_issues(errors)
{
	// TODO: parse GraphML
}


FuzzTreeTransform::FuzzTreeTransform(
	std::istream& fuzzTreeXML,
	std::set<Issue>& errors) :
	m_count(0),
	m_bValid(true),
	m_issues(errors)
{
	// TODO: parse GraphML
}

FuzzTreeTransform::FuzzTreeTransform(
	std::auto_ptr<Fuzztree> ft,
	std::set<Issue>& errors) :
	m_fuzzTree(ft),
	m_count(0),
	m_bValid(true),
	m_issues(errors)
{
	assert(m_fuzzTree.get());
}

FuzzTreeTransform::~FuzzTreeTransform()
{}

/************************************************************************/
/* Generating all possible configurations initially                     */
/************************************************************************/

void FuzzTreeTransform::generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations)
{
	unsigned int configCount = 0;
	configurations.emplace_back(FuzzTreeConfiguration(++configCount)); // default
	generateConfigurationsRecursive(m_fuzzTree->getTopEvent(), configurations, configCount); // TODO handle errors here
}

ErrorType FuzzTreeTransform::generateConfigurationsRecursive(
	const AbstractNode* node, 
	std::vector<FuzzTreeConfiguration>& configurations,
	unsigned int& configCount)
{
	for (const auto& child : node->children())
	{
		const string id = child->getId();
		const auto childType = child->getTypeDescriptor();
		
		if (child->isOptional())
		{ // inclusion variation point. Generate n + n configurations.
			vector<FuzzTreeConfiguration> additional;
			for (FuzzTreeConfiguration& config : configurations)
			{
				if (!config.isIncluded(id) || !config.isIncluded(node->getId())) 
					continue;

				FuzzTreeConfiguration copied = config;
				copied.setId(++configCount);
				// one configuration with this node
				copied.setOptionalEnabled(id, true);
				if (childType == "basicEvent" || childType == "intermediateEvent")
					copied.setCost(copied.getCost() + child->getCost());

				// one configuration without this node
				config.setOptionalEnabled(id, false);
				config.setNotIncludedRecursive(*child);

				additional.emplace_back(copied);
			}
			configurations.insert(configurations.begin(), additional.begin(), additional.end());
		}

		if (childType == "redundancyVariationPoint")
		{ // any VotingOR with k in [from, to] and k=n-2. Generate n * #validVotingOrs configurations.
			const RedundancyVariationPoint* redundancyNode = static_cast<const RedundancyVariationPoint*>(child);
			const int from = redundancyNode->start();
			const int to = redundancyNode->end();
			if (from < 0 || to < 0 || from > to)
			{
				m_issues.insert(Issue(
					std::string("Invalid Redundancy VP attributes, to: ") + 
					util::toString(to) + 
					", from: " + 
					util::toString(from), 0, id));
				
				return INVALID_ATTRIBUTE;
			}
			
			const std::string formulaString = redundancyNode->formula();
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
					for (int N = from; N <= to; ++N)
					{
						const int k = formula(N);
						if (k <= 0)
						{
							m_issues.insert(Issue(
								std::string("Ignoring invalid redundancy configuration with k=") + 
								util::toString(k) + 
								std::string(" N=") + 
								util::toString(N),
								0, id));
							continue;
						}
						FuzzTreeConfiguration copied = config;
						copied.setId(++configCount);
						copied.setRedundancyNumber(id, k, N);
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
			if (childType == "featureVariationPoint")
			{ // exactly one subtree. Generate N * #Features configurations.
				const FeatureVariationPoint* featureNode = static_cast<const FeatureVariationPoint*>(child);
				if (featureNode->children().size() == 0)
				{
					throw FatalException(std::string("FeatureVP without children found: ") + id, 0, id);
				}

				vector<FuzzTreeConfiguration> newConfigs;
				for (FuzzTreeConfiguration& config : configurations)
				{
					if (config.isIncluded(id))
					{
						for (const auto& featuredChild : featureNode->children())
						{
							FuzzTreeConfiguration copied = config;
							copied.setId(++configCount);
							copied.setFeatureNumber(id, featuredChild->getId());
							for (const auto& other : featureNode->children())
							{
								if (other->getId() != featuredChild->getId()) 
									copied.setNotIncludedRecursive(*other);
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
			else if (
				childType == "basicEvent" || 
				childType == "basicEventSet")
			{ // handle costs, TODO intermediateEvents!
				int costs = child->getCost();

				// multiply costs...
				if (childType == "basicEventSet")
				{
					const auto bes = static_cast<const BasicEventSet*>(child);
					costs *= bes->getQuantity();
				}

				for (FuzzTreeConfiguration& config : configurations)
				{
					if (config.isIncluded(id))
						config.setCost(costs + config.getCost());
				}
			}

			if (isLeaf(childType)) continue; // end recursion
		}
		generateConfigurationsRecursive(child, configurations, configCount);
	}

	return OK;
}

/************************************************************************/
/* Generating fault trees from configurations                           */
/************************************************************************/

Fuzztree FuzzTreeTransform::generateVariationFreeFuzzTree(const FuzzTreeConfiguration& configuration)
{
	const auto topEvent = m_fuzzTree->getTopEvent();

	// Create a new empty top event to fill up with the configuration
	TopEvent newTopEvent(topEvent->getId());
	
	// TODO
	//newTopEvent.missionTime(topEvent.missionTime());
	//newTopEvent.decompositionNumber(topEvent.decompositionNumber());
	newTopEvent.name(topEvent->name());

	if (generateVariationFreeFuzzTreeRecursive(&topEvent, &newTopEvent, configuration) == OK)
		return Fuzztree(m_fuzzTree->getId(), newTopEvent);
	else
		return Fuzztree("", newTopEvent); // TODO handle properly
}

ErrorType FuzzTreeTransform::generateVariationFreeFuzzTreeRecursive(
	const AbstractNode* templateNode,
	AbstractNode* node,
	const FuzzTreeConfiguration& configuration)
{
	for (const auto& currentChild : templateNode->children())
	{
		const string id = currentChild->getId();
		const auto typeName = currentChild->getTypeDescriptor();
		
		const bool opt = isOptional(currentChild);

		if (!configuration.isIncluded(id) || (opt && !configuration.isOptionalEnabled(id)))
			continue; // do not add this node

		bool bChanged = true;
		
		if (typeName == "redundancyVariationPoint")
		{ // TODO: probably this always ends up with a leaf node
			int numChildren = currentChild.children().size();
			if (numChildren != 1)
			{
				throw FatalException(
					std::string("Redundancy VP with invalid number of children found: ") + util::toString(numChildren),
					0, id);
			}
			const auto& firstChild = currentChild.children().front();
			const auto& childTypeName = firstChild->getTypeDescriptor();
			const auto kOutOfN = configuration.getRedundancyCount(id);

			VotingOrGate votingOrGate(id, get<0>(kOutOfN));
			if (childTypeName == "basicEventSet")
			{
				const BasicEventSet* bes = 
					static_cast<const BasicEventSet*>(firstChild);

				expandBasicEventSet(&bes, &votingOrGate, get<1>(kOutOfN));
			}
			else if (childTypeName == "intermediateEventSet")
			{
				const IntermediateEventSet* ies = 
					static_cast<const ntermediateEventSet*>(firstChild);

				expandIntermediateEventSet(&ies, &votingOrGate, configuration, get<1>(kOutOfN));
			}
			else
			{
				m_issues.insert(Issue(std::string("Unrecognized Child Type: ") + typeName.name(), 0, id));
				return WRONG_CHILD_TYPE;
			}
			node->children().push_back(votingOrGate);

			continue; // stop recursion
		}
		else if (typeName == "featureVariationPoint")
		{
			if (handleFeatureVP(
				&currentChild, 
				node,
				configuration, 
				configuration.getFeaturedChild(id))) continue;

			bChanged = false;
		}
		else if (typeName == "basicEventSet")
		{
			auto ret = expandBasicEventSet(&currentChild, node, 0);
			if (ret != OK) return ret;
			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == "intermediateEventSet")
		{
			auto ret = expandIntermediateEventSet(&currentChild, node, configuration, 0);
			if (ret != OK)
				return ret;
			continue;
		}
		else if (typeName == "transferIn")
		{
			throw FatalException(std::string("TransferIn Gate not yet implemented."), 0, id);

			// m_issues.insert("TransferIn Gate not yet implemented.", 0, id);
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
	const AbstractNode* templateNode,
	AbstractNode* parentNode, 
	const int& defaultQuantity /*= 0*/)
{
	assert(parentNode && templateNode);

	const BasicEventSet* eventSet = static_cast<const BasicEventSet*>(templateNode);
	assert(eventSet);

	const int numChildren = eventSet->getQuantity();
	if (numChildren <= 0)
	{
		m_issues.insert(Issue("Invalid number of Children in BasicEventSet", 0 , eventSet->getId()));
		return INVALID_ATTRIBUTE;
	}
	const auto& prob = eventSet->probability();

	const int cost = eventSet->getCost();
	unsigned int i = 0;
	const auto eventSetId = eventSet->id();
	while (i < numChildren)
	{
		BasicEvent be(eventSetId + "." + util::toString(i), prob);
		be.costs(costs);
		parentNode->children().push_back(be);
		i++;
	}

	return OK;
}

ErrorType FuzzTreeTransform::expandIntermediateEventSet(
	const AbstractNode* templateNode,
	AbstractNode* parentNode, 
	const FuzzTreeConfiguration& configuration,
	const int& defaultQuantity /*= 0*/)
{
	assert(parentNode && templateNode);

	const IntermediateEventSet* eventSet = static_cast<const IntermediateEventSet*>(templateNode);
	assert(eventSet);
	const auto eventSetId = eventSet->getId();
	if (eventSet->children().size() == 0)
	{
		m_issues.insert(Issue::fatalIssue("Intermediate Event Set has no children.", 0, eventSetId));
		return WRONG_CHILD_NUM;
	}
	// barharhar
	const int numChildren = 
		defaultQuantity == 0 ? 
		eventSet->quantity().present() ? 
			eventSet->quantity().get() : 
			defaultQuantity : 
		defaultQuantity;

	if (numChildren <= 0)
	{
		m_issues.insert(Issue("Invalid number of Children in IntermediateEventSet", 0 , eventSetId));
		return INVALID_ATTRIBUTE;
	}

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
	const AbstractNode* templateNode,
	AbstractNode* node,
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
	const auto featuredType = featuredTemplate->getTypeDescriptor();
	
	if (isOptional(featuredTemplate) && !configuration.isIncluded(configuredChildId))
	{
		return true;
	}
	else if (featuredType == "basicEventSet")
	{
		expandBasicEventSet(&featuredTemplate, node, 0);
		return true;
	}
	else if (featuredType == "andGate")
		node->addChild(new AndGate(configuredChildId));
	else if (featuredType == "orGate")
		node->addChild(new Or(configuredChildId));
	else if (featuredType == "votingOrGate")
		node->addChild(new VotingOrGate(configuredChildId, (static_cast<const VotingOrGate*>(featuredTemplate)).k())));
	else if (featuredType == "xorGate")
		node->addChild(new XorGate(configuredChildId));
	else if (isLeaf(featuredType))
		node->addChild(new BasicEvent(static_cast<const BasicEvent*>(featuredTemplate)));
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
			m_issues.insert(Issue("Invalid FuzzTree."));
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
		m_issues.insert(Issue::fatalIssue(e.what()));
	}
	catch (std::exception& e)
	{
		m_issues.insert(Issue::fatalIssue(e.what()));
	}
	catch (...)
	{
		m_issues.insert(Issue::fatalIssue("Unknown Error during FuzzTree Transformation"));
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
	if (typeName == *AND)					
		node->children().push_back(fuzztree::And(id));
	else if (typeName == *OR)				
		node->children().push_back(fuzztree::Or(id));
	else if (typeName == *VOTINGOR)			
		node->children().push_back(fuzztree::VotingOr(id, (static_cast<const fuzztree::VotingOr&>(currentChild)).k()));
	else if (typeName == *XOR)				
		node->children().push_back(fuzztree::Xor(id));
	else if (typeName == *INTERMEDIATEEVENT)
		node->children().push_back(fuzztree::IntermediateEvent(id));
	else if (typeName == *BASICEVENT)		
		node->children().push_back(fuzztree::BasicEvent(static_cast<const fuzztree::BasicEvent&>(currentChild)));
	else if (typeName == *UNDEVELOPEDEVENT)	
		node->children().push_back(fuzztree::UndevelopedEvent(id));
	else
	{
		throw FatalException(std::string("Unexpected Node Type encountered: ") + typeName.name(), 0, id);
	}
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
