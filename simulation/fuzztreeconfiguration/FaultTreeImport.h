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

class FaultTreeNode;

class FaultTreeImport : public XMLImport
{
public:
	static FaultTreeNode* loadFaultTree(const std::string& fileName);
	virtual ~FaultTreeImport();

protected:
	static void loadNode(const pugi::xml_node& node, FaultTreeNode* ft);

	static double	parseFailureRate(const pugi::xml_node& child);
	static int		parseId(const pugi::xml_node& child);

private:
	FaultTreeImport(const std::string& fileName);
	FaultTreeNode* loadTree();

	virtual bool loadRootNode() override;
};