#include "FuzzTreeTransform.h"
#include "FuzzTreeConfiguration.h"
#include "Constants.h"
#include "ExpressionParser.h"
#include "util.h"

#include <xsd/cxx/tree/elements.hxx>
#include <boost/range/counting_range.hpp>

using namespace fuzzTree;
using namespace faultTree;

using xercesc::DOMNode;
using xercesc::DOMDocument;

std::vector<faulttree::FaultTree> FuzzTreeTransform::transformFuzzTree(const std::string& fuzzTreeXML)
{
	std::vector<faulttree::FaultTree> results;
	
	try
	{
		FuzzTreeTransform transform(fuzzTreeXML);
		
		vector<FuzzTreeConfiguration> configs;
		transform.generateConfigurations(configs);

		for (const auto& instanceConfiguration : configs)
		{
			transform.generateFaultTree(instanceConfiguration);
		}
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

	return results;
}

FuzzTreeTransform::FuzzTreeTransform(const std::string& fuzzTreeXML) :
	m_count(0)
{
	m_fuzzTree = fuzztree::fuzzTree(fuzzTreeXML.c_str(), xsd::cxx::tree::flags::dont_validate);
	assert(m_fuzzTree.get());
}

FuzzTreeTransform::~FuzzTreeTransform()
{}

/************************************************************************/
/* Utility methods                                                      */
/************************************************************************/

bool FuzzTreeTransform::isGate(const fuzztree::Node& node)
{
	return
		false; // TODO
}

bool FuzzTreeTransform::isLeaf(const fuzztree::Node& node)
{
	return 
		false; // TODO
}

std::string FuzzTreeTransform::generateUniqueId(const char* oldId)
{
	return std::string(oldId) + "." + util::toString(++m_count);
}

/************************************************************************/
/* Generating all possible configurations initially                     */
/************************************************************************/

void FuzzTreeTransform::generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const
{
	configurations.emplace_back(FuzzTreeConfiguration()); // default
	generateConfigurationsRecursive(&m_fuzzTree->topEvent(), configurations);
}

void FuzzTreeTransform::generateConfigurationsRecursive(
	const fuzztree::Node* node, std::vector<FuzzTreeConfiguration>& configurations) const
{
	using namespace fuzztree;
	for (const auto& child : node->children())
	{
		const int id = child.id();
		if (id < 0) continue;

		const InclusionVariationPoint* inclusionNode = dynamic_cast<const InclusionVariationPoint*>(&child);
		const bool opt		= (inclusionNode != nullptr) && inclusionNode->optional();

		if (opt)
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

		const RedundancyVariationPoint* redundancyNode = dynamic_cast<const RedundancyVariationPoint*>(&child);
		if (redundancyNode)
		{ // any VotingOR with k in [from, to] and k=n-2. Generate n * #validVotingOrs configurations.
			const int from = redundancyNode->start();
			const int to = redundancyNode->end();
			if (from < 0 || to < 0 || from > to)
				throw runtime_error("Invalid boundaries for RedundancyGate");

			if (from == to) continue;

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
			const FeatureVariationPoint* featureNode = dynamic_cast<const FeatureVariationPoint*>(&child);

			if (featureNode)
			{
				// exactly one subtree. Generate N * #Features configurations.
				vector<int> childIds;
				for (const auto& featuredChild : featureNode->children())
					childIds.emplace_back(featuredChild.id());

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
			else if (isLeaf(child))
			{
				continue; // end recursion
			}
		}
		generateConfigurationsRecursive(&child, configurations);
	}
}

/************************************************************************/
/* Generating fault trees from configurations                           */
/************************************************************************/

void FuzzTreeTransform::generateFaultTree(const FuzzTreeConfiguration& configuration)
{

}

void FuzzTreeTransform::generateFaultTreeRecursive(
	const fuzztree::Node* templateNode, /*Xerces*/ 
	faulttree::Node* node, /*generated internal fault tree model*/ 
	const FuzzTreeConfiguration& configuration) const
{

}

void FuzzTreeTransform::expandBasicEventSet(
	const fuzztree::Node* templateNode,
	faulttree::Node* parentNode, 
	const int& id, const int& defaultQuantity /*= 0*/) const
{

}

std::pair<faulttree::Node, bool /*isLeaf*/> FuzzTreeTransform::handleFeatureVP(
	const fuzztree::Node* templateNode,
	faulttree::Node* node,
	const FuzzTreeConfiguration& configuration, const int configuredChildId) const
{
	assert(false && "implement");
	return make_pair(faulttree::Node(0), false);
}