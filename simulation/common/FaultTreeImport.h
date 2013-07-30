#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <pugixml.hpp>
#include <boost/filesystem/path.hpp>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif

#include "XMLImport.h"
#include "platform.h"

class FaultTreeNode;

class FaultTreeImport : public XMLImport
{
public:
	static std::shared_ptr<FaultTreeNode> loadFaultTree(const std::string& fileName) noexcept;
	virtual ~FaultTreeImport();

protected:
	static void loadNode(const pugi::xml_node& node, std::shared_ptr<FaultTreeNode> ft);

	static double parseFailureRate(const pugi::xml_node& child);

private:
	FaultTreeImport(const std::string& fileName);
	std::shared_ptr<FaultTreeNode> loadTree();

	virtual bool loadRootNode() override;
};
