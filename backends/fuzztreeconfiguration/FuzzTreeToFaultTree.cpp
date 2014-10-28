#include "FuzzTreeToFaultTree.h"
#include "FatalException.h"
#include "ExpressionParser.h"
#include "util.h"

#include <functional>
#include <algorithm>

std::vector<FuzzTreeConfiguration> FuzzTreeToFaultTree::generateConfigurations()
{
	std::vector<FuzzTreeConfiguration> results;

	/**
	 * Traverse tree recursively to obtain configurations.
	 */
	unsigned int configCount = 0;
	results.emplace_back(FuzzTreeConfiguration(++configCount));
	generateConfigurationsRecursive(m_model->getTopEvent(), results, configCount);

	return results;
}

Model FuzzTreeToFaultTree::faultTreeFromConfiguration(const FuzzTreeConfiguration& config)
{
	Node* topEvent = new Node(*m_model->getTopEvent());
	topEvent->m_children.clear(); // These need to be re-filled according to the configuration
	{
		faultTreeFromConfigurationRecursive(m_model->getTopEvent(), topEvent, config);
	}

	return Model::createFaulttree(m_model->getId(), m_model->getName(), topEvent);
}

bool FuzzTreeToFaultTree::generateConfigurationsRecursive(
	const Node* node, 
	std::vector<FuzzTreeConfiguration>& configurations,
	unsigned int& configCount)
{
	for (const auto& child : node->getChildren())
	{
		const std::string id = child.getId();
		const std::string childType = child.getType();
		
		if (child.isOptional())
		{ // inclusion variation point. Generate n + n configurations.
			std::cout << "optional";

			std::vector<FuzzTreeConfiguration> additional;
			for (FuzzTreeConfiguration& config : configurations)
			{
				if (!config.isIncluded(id) || !config.isIncluded(node->getId())) 
					continue;

				FuzzTreeConfiguration copied = config;
				copied.setId(++configCount);
				// one configuration with this node
				copied.setOptionalEnabled(id, true);
				if (childType == "basicEvent" || childType == "intermediateEvent")
					copied.setCost(copied.getCost() + child.getCost());

				// one configuration without this node
				config.setOptionalEnabled(id, false);
				config.setNotIncludedRecursive(child);

				additional.emplace_back(copied);
			}
			configurations.insert(configurations.begin(), additional.begin(), additional.end());
		}

		if (childType == nodetype::REDUNDANCYVP)
		{ // any VotingOR with k in [from, to] and k=n-2. Generate n * #validVotingOrs configurations.
			const int from	= child.getFrom();
			const int to	= child.getTo();
			if (from < 0 || to < 0 || from > to)
			{
				m_issues.insert(Issue(
					std::string("Invalid Redundancy VP attributes, to: ") + 
					util::toString(to) + 
					", from: " + 
					util::toString(from), 0, id));
				
				return false;
			}
			
			const std::string formulaString = child.getRedundancyFormula();
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
			if (childType == nodetype::FEATUREVP)
			{ // exactly one subtree. Generate N * #Features configurations.
				if (child.getChildren().size() == 0)
					throw FatalException(std::string("FeatureVP without children found: ") + id, 0, id);
				
				std::cout << "FEATUREVP";
				std::vector<FuzzTreeConfiguration> newConfigs;
				for (const FuzzTreeConfiguration& config : configurations)
				{
					if (config.isIncluded(id))
					{
						for (const auto& featuredChild : child.getChildren())
						{
							FuzzTreeConfiguration copied = config;
							copied.setId(++configCount);
							copied.setFeatureNumber(id, featuredChild.getId());
							for (const auto& other : child.getChildren())
							{
								if (other.getId() != featuredChild.getId()) 
									copied.setNotIncludedRecursive(other);
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
				childType == nodetype::BASICEVENT || 
				childType == nodetype::BASICEVENTSET)
			{ // handle costs, TODO intermediateEvents!
				int costs = child.getCost();

				// multiply costs...
				if (childType == nodetype::BASICEVENTSET)
					costs *= child.getQuantity();

				for (FuzzTreeConfiguration& config : configurations)
				{
					if (config.isIncluded(id))
						config.setCost(costs + config.getCost());
				}
			}

			if (node->isLeaf()) continue; // end recursion
		}
		generateConfigurationsRecursive(&child, configurations, configCount);
	}
	return true;
}

bool FuzzTreeToFaultTree::faultTreeFromConfigurationRecursive(
	const Node* templateNode,
	Node* node,
	const FuzzTreeConfiguration& configuration)
{
	for (const auto& currentChild : templateNode->getChildren())
	{
		const std::string& id = currentChild.getId();
		const std::string& typeName = currentChild.getType();

		const bool opt = currentChild.isOptional();

		if (!configuration.isIncluded(id) || (opt && !configuration.isOptionalEnabled(id)))
			continue; // do not add this node

		bool bChanged = true;

		if (typeName == nodetype::REDUNDANCYVP)
		{ // TODO: probably this always ends up with a leaf node
			size_t numChildren = currentChild.getChildren().size();
			if (numChildren != 1)
			{
				throw FatalException(
					std::string("Redundancy VP with invalid number of children found: ") + util::toString((int)numChildren),
					0, id);
			}
			const auto& firstChild = currentChild.getChildren().front();
			const auto& childTypeName = firstChild.getType();
			const auto kOutOfN = configuration.getRedundancyCount(id);

			Node votingOrGate = Node(nodetype::VOTINGOR, id, false, currentChild.getName());
			votingOrGate.setKOutOfN(get<0>(kOutOfN));
			if (childTypeName == nodetype::BASICEVENTSET)
			{
				expandBasicEventSet(&firstChild, &votingOrGate, get<1>(kOutOfN));
			}
			else if (childTypeName == nodetype::INTERMEDIATEEVENTSET)
			{
				expandIntermediateEventSet(&firstChild, &votingOrGate, configuration, get<1>(kOutOfN));
			}
			else
			{
				m_issues.insert(Issue(std::string("Unrecognized Child Type: ") + typeName, 0, id));
				return false;
			}
			node->addChild(votingOrGate);

			continue; // stop recursion
		}
		else if (typeName == nodetype::FEATUREVP)
		{
			if (handleFeatureVP(
				&currentChild,
				node,
				configuration,
				configuration.getFeaturedChild(id))) continue;

			bChanged = false;
		}
		else if (typeName == nodetype::BASICEVENTSET)
		{
			auto ret = expandBasicEventSet(&currentChild, node, 0);
			if (!ret) return ret;
			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == nodetype::INTERMEDIATEEVENTSET)
		{
			auto ret = expandIntermediateEventSet(&currentChild, node, configuration, 0);
			if (!ret) return ret;
			continue;
		}
		else if (typeName == "transferIn")
		{
			throw FatalException(std::string("TransferIn Gate not yet implemented."), 0, id);
			continue;
		}

		// remaining types
		//TODO else copyNode(typeName, node, id, currentChild);

		// break recursion
		// BasicEvents can have FDEP children...
		// continue;

		faultTreeFromConfigurationRecursive(&currentChild, bChanged ? &node->getChildren().back() : node, configuration);
	}

	return true;
}


bool FuzzTreeToFaultTree::handleFeatureVP(
	const Node* templateNode,
	Node* node,
	const FuzzTreeConfiguration& configuration,
	const FuzzTreeConfiguration::id_type& configuredChildId)
{
	assert(node && templateNode);
	// find the configured child
	auto it = templateNode->getChildren().begin();
	while (it != templateNode->getChildren().end())
	{
		if (it->getId() == configuredChildId)
			break;
		++it;
	}

	const Node& featuredTemplate = *it;
	const std::string& featuredType = featuredTemplate.getType();

	if (featuredTemplate.isOptional() && !configuration.isIncluded(configuredChildId))
	{
		return true;
	}
	else if (featuredType == nodetype::BASICEVENTSET)
	{
		expandBasicEventSet(&featuredTemplate, node, 0);
		return true;
	}
	else if (featuredTemplate.isVariationPoint())
	{
		return false;
	}
	else 
		node->addChild(featuredTemplate);
	
	return false;
}

bool FuzzTreeToFaultTree::expandIntermediateEventSet(const Node* child, Node* parent, const FuzzTreeConfiguration& configuration /*this is needed for further recursive descent*/, const int& defaultQuantity /*= 0*/)
{
	return false;
}

bool FuzzTreeToFaultTree::expandBasicEventSet(const Node* child, Node* parent, const int& defaultQuantity/*=0*/)
{
	assert(child && parent && child->getType() == nodetype::BASICEVENTSET);

	const unsigned int numChildren = std::max(defaultQuantity, (int)child->getQuantity());
	if (numChildren <= 0)
	{
		m_issues.insert(Issue("Invalid number of Children in BasicEventSet", 0, child->getId()));
		return false;
	}
	const auto& prob		= child->getProbability();
	const int& cost			= child->getCost();
	const auto& eventSetId	= child->getId();
	unsigned int i = 0;

	while (i < numChildren)
	{
		Node be(nodetype::BASICEVENT, eventSetId + "." + util::toString((int)i), false, child->getName());
		be.setProbability(prob);
		be.m_cost = cost;
		parent->addChild(be);
		i++;
	}

	return true;
}

const std::set<Issue>& FuzzTreeToFaultTree::getIssues() const
{
	return m_issues;
}
