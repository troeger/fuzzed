#pragma once

#include <assert.h>
#include <iostream>

#include "pugixml.hpp"

static const char* INDENT = "    ";

class ResultsXML
{
    pugi::xml_node createResultsNode(pugi::xml_document& document)
    {
        pugi::xml_node results = document.append_child();
        results.set_name("ftr:backendResults");
        results.append_attribute("xmlns:ftc") = "http://www.fuzztrees.net/commonTypes";
        results.append_attribute("xmlns:ftr") = "http://www.fuzztrees.net/backendResults";
        results.append_attribute("xmlns:xsi") = "http://www.w3.org/2001/XMLSchema-instance";

        return results;
    }

    pugi::xml_node createConfigurationNode(pugi::xml_node& results, const FuzzTreeConfiguration& configuration) const
    {
        pugi::xml_node configurationNode = results.append_child();
        configurationNode.set_name("configuration");
        configurationNode.append_attribute("id")    = configuration.getId();
        configurationNode.append_attribute("costs") = configuration.getCosts();

        return configuration;
    }

    template <typename ResultType>
    pugi::xml_node createResultNode(pugi::xml_node& results, const ResultType& result) const
    {
        pugi::xml_node resultNode = results.append_child;
        resultNode.set_name("result");
        resultNode.append_attribute("valid")     = result.isValid();
        resultNode.append_attribute("modelId")   = result.getModelId();
        resultNode.append_attribute("configId")  = result.getId();
        resultNode.append_attribute("timestamp") = result.getTimestamp();
        resultNode.append_attribute("xsi:type")  = "ftr:AnalysisResult";

        this->createSpecificOutome(resultNode, result);
    }

    pugi::xml_node createSpecificOutcome(pugi::xml_node& result, const FuzzTreeAnalysisResults& outcome) const
    {
        pugi::xml_node probability = result.append_child();
        probability.set_name("probability");
        probability.append_attribute("xsi:type") = "ftc:DecomposedFuzzyProbability";

        for (const auto& alphaCut : outcome.getAlphaCuts())
        {
            pugi::xml_node alphaCut = probability.append_child();
            alphaCut.set_name("alphaCuts");
            alphaCut.append_attribute("key") = alphaCut->first;

            const auto& bounds = alphaCut->second;
            pugi::xml_node value = alphaCut.append_child();
            value.set_name("value");
            value.append_attribute("lowerBounds") = bounds.first;
            value.append_attribute("upperBounds") = bounds.second;
        }
    }

public:
    /* "FaultTree" template without configurations */
    template <typename ResultType>
    void generate(std::vector<ResultType>& results, std::ostream& output) const
    {
        pugi::xml_document document;
        pugi::xml_node resultsNode = this->createResultsNode(document);

        for (const auto& result : results)
        {
            this->createResultNode(resultsNode, result);
        }
        document.save(output, INDENT);
    }

    /* "FuzzTree" template that accepts configurations */
    template <typename ResultType>
    void generate(std::vector<FuzzTreeConfiguration>& configurations, std::vector<ResultType>& results, std::ostream& output) const
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
        document.save(output, INDENT);
    }
};
