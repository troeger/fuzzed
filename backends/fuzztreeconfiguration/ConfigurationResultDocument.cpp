#include "ConfigurationResultDocument.h"

ConfigurationResultDocument::ConfigurationResultDocument()
	: AbstractResultDocument("Configuration")
{}

void ConfigurationResultDocument::addConfigurations(const std::vector<FuzzTreeConfiguration>& configs)
{
	// for each configuration, write only the Choice information
	for (const auto& config : configs)
		addConfigurationNode(config, m_root);
}

void ConfigurationResultDocument::addTreeSpecification(std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree)
{
// 	std::ostringstream sstream;
// 	const fuzztree::FuzzTree& foo = m_fuzzTree.get();
// 	fuzztree::fuzzTree(sstream, foo);
// 	m_root.append_child(pugi::node_pcdata).set_value(sstream.str().c_str());
}
