#pragma once

#include <assert.h>
#include <iostream>

#include "pugixml.hpp"
#include "FuzzTreeConfiguration.h"
#include "Issue.h"

static const char* INDENT = "    ";

class ResultsXML
{
    pugi::xml_node createResultsNode(pugi::xml_document& document) const
    {
        pugi::xml_node results = document.append_child();
        results.set_name("ftr:backendResults");
        results.append_attribute("xmlns:ftc") = "http://www.fuzztrees.net/commonTypes";
        results.append_attribute("xmlns:ftr") = "http://www.fuzztrees.net/backendResults";
        results.append_attribute("xmlns:xsi") = "http://www.w3.org/2001/XMLSchema-instance";

        return results;
    }
	pugi::xml_node createIssueNode(pugi::xml_node& results, const Issue& issue) const
	{
		pugi::xml_node issueNode = results.append_child("issue");

		issueNode.append_attribute("issueId").set_value(issue.getIssueId());
		issueNode.append_attribute("elementId").set_value(issue.getElementId().c_str());
		issueNode.append_attribute("message").set_value(issue.getMessage().c_str());
		issueNode.append_attribute("isFatal").set_value(issue.isFatal());
		return issueNode;
	}

    pugi::xml_node createConfigurationNode(pugi::xml_node& results, const FuzzTreeConfiguration& configuration) const
    {
        pugi::xml_node configurationNode = results.append_child("configuration");
        configurationNode.append_attribute("id")    = configuration.getId().c_str();
        configurationNode.append_attribute("costs") = configuration.getCost();

		for (const auto& inclusionChoice : configuration.getOptionalNodes())
		{
			pugi::xml_node choiceNode = configurationNode.append_child("choice");
			choiceNode.append_attribute("key").set_value(inclusionChoice.first.c_str());
			choiceNode.append_child("value").append_attribute("included").set_value(inclusionChoice.second);
		}

		for (const auto& redundancyChoice : configuration.getRedundancyNodes())
		{
			pugi::xml_node choiceNode = configurationNode.append_child("choice");
			choiceNode.append_attribute("key").set_value(redundancyChoice.first.c_str());
			choiceNode.append_child("value").append_attribute("n").set_value(std::get<1>(redundancyChoice.second));
		}

		for (const auto& featureChoice : configuration.getFeaturedNodes())
		{
			pugi::xml_node choiceNode = configurationNode.append_child("choice");
			choiceNode.append_attribute("key").set_value(featureChoice.first.c_str());
			choiceNode.append_child("value").append_attribute("featureId").set_value(featureChoice.second.c_str());
		}

		return configurationNode;
    }

    template <typename ResultType>
    pugi::xml_node createResultNode(pugi::xml_node& results, const ResultType& result) const
    {
        pugi::xml_node resultNode = results.append_child();
        resultNode.set_name("result");
        resultNode.append_attribute("valid")     = result.isValid();
        resultNode.append_attribute("modelId")   = result.getModelId().c_str();
        resultNode.append_attribute("configId")  = result.getId().c_str();
        resultNode.append_attribute("timestamp") = result.getTimestamp().c_str();
        resultNode.append_attribute("xsi:type")  = result.getType().c_str();

        //this->createSpecificOutcome(resultNode, result);

		result.createXML(resultNode);

		return resultNode;
    }

	template <typename ResultType>
	pugi::xml_node createSpecificOutcome(pugi::xml_node& result, const ResultType& outcome) const
    {
        pugi::xml_node probability = result.append_child();
        probability.set_name("probability");
        probability.append_attribute("xsi:type") = "ftc:DecomposedFuzzyProbability";

        for (const auto& alphaCut : outcome.getAlphaCuts())
        {
            pugi::xml_node alphaCut_node = probability.append_child();
			alphaCut_node.set_name("alphaCuts");
			alphaCut_node.append_attribute("key") = alphaCut.first;

            const NumericInterval& bounds = alphaCut.second;
			pugi::xml_node value = alphaCut_node.append_child();
            value.set_name("value");
            value.append_attribute("lowerBounds") = bounds.lowerBound;
            value.append_attribute("upperBounds") = bounds.upperBound;
        }

		return probability;
    }

public:
    /* "FaultTree" template without configurations */
    template <typename ResultType>
    void generate(
		const std::vector<ResultType>& results,
		const std::set<Issue>& issues,
		std::ostream& output) const
    {
        pugi::xml_document document;
        pugi::xml_node resultsNode = this->createResultsNode(document);

        for (const auto& result : results)
        {
            this->createResultNode(resultsNode, result);
        }

		for (const Issue& issue : issues)
		{
			this->createIssueNode(resultsNode, issue);
		}
        document.save(output, INDENT);
    }

    /* "FuzzTree" template that accepts configurations */
    template <typename ResultType>
	void generate(
		const std::vector<FuzzTreeConfiguration>& configurations,
		const std::vector<ResultType>& results,
		const std::set<Issue>& issues,
		std::ostream& output) const
    {
        pugi::xml_document document;
        pugi::xml_node resultsNode = this->createResultsNode(document);

        assert(configurations.size() == results.size() /* there are not enough configurations for results or vice versa */);

        for (size_t i = 0; i < configurations.size(); ++i)
        {
            const auto& configuration = configurations[i];
            const auto& result        = results[i];

            this->createConfigurationNode(resultsNode, configuration);
            this->createResultNode(resultsNode, result);
        }

		for (const auto& issue : issues)
		{
			this->createIssueNode(resultsNode, issue);
		}
        document.save(output, INDENT);
    }

	/* "FuzzTree" template that only outputs configurations */
	void generate(
		const std::vector<FuzzTreeConfiguration>& configurations,
		const std::set<Issue>& issues,
		std::ostream& output) const
	{
		pugi::xml_document document;
		pugi::xml_node resultsNode = this->createResultsNode(document);

		for (size_t i = 0; i < configurations.size(); ++i)
		{
			const auto& configuration = configurations[i];
			this->createConfigurationNode(resultsNode, configuration);
		}

		for (const Issue& issue : issues)
		{
			this->createIssueNode(resultsNode, issue);
		}

		document.save(output, INDENT);
	}
};
