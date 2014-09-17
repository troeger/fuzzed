#include "FuzzTreeToFaultTree.h"
#include "FatalException.h"

std::vector<FuzzTreeConfiguration> FuzzTreeToFaultTree::generateConfigurations() const
{
	std::vector<FuzzTreeConfiguration> results;

	/**
	 * Traverse tree recursively to obtain configurations.
	 */
	unsigned int configCount = 0;

	FuzzTreeConfiguration f = FuzzTreeConfiguration();
	results.push_back(f);
	generateConfigurationsRecursive(m_model->getTopEvent(), results, configCount);

	return results;
}

Model FuzzTreeToFaultTree::faultTreeFromConfiguration(const FuzzTreeConfiguration& config) const
{
	Node* topEvent = nullptr;

	{

	}

	return Model::createFaulttree(m_model->getId(), m_model->getName(), topEvent);
}

bool FuzzTreeToFaultTree::generateConfigurationsRecursive(
	const Node* node, 
	std::vector<FuzzTreeConfiguration>& configurations,
	unsigned int& configCount) const
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
			/*// const RedundancyVariationPoint* redundancyNode = static_cast<const RedundancyVariationPoint*>(child);
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
			}*/
		}
		else
		{
			if (childType == nodetype::FEATUREVP)
			{ // exactly one subtree. Generate N * #Features configurations.
				if (node->getChildren().size() == 0)
					throw FatalException(std::string("FeatureVP without children found: ") + id, 0, id);
				
				std::cout << "FEATUREVP";
				std::vector<FuzzTreeConfiguration> newConfigs;
				for (const FuzzTreeConfiguration& config : configurations)
				{
					if (config.isIncluded(id))
					{
						for (const auto& featuredChild : node->getChildren())
						{
							FuzzTreeConfiguration copied = config;
							copied.setId(++configCount);
							copied.setFeatureNumber(id, featuredChild.getId());
							for (const auto& other : node->getChildren())
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
		std::cout << "....";
		generateConfigurationsRecursive(&child, configurations, configCount);
	}
	return true;
}