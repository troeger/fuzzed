#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <pugixml.hpp>
#include <boost/filesystem/path.hpp>
#include <thread>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif

#include "FaultTreeNode.h"
#include "XMLImport.h"
#include "ReaderWriterQueue.h"
#include "platform.h"

using namespace std;
using namespace pugi;

typedef moodycamel::ReaderWriterQueue<FaultTreeNode*> FTResults;

class FuzzTreeImport : public XMLImport
{
public:
	DEPRECATED static FaultTreeNode* loadFaultTree(const string& fileName);

	// returns a vector of futures on the fault tree configurations
	// the caller should tidy up the FuzzTreeImport pointer
	DEPRECATED static pair<FuzzTreeImport*,FTResults*> loadFaultTreeAsync(const string& fileName);

	virtual ~FuzzTreeImport();

	bool isBusy() const { return m_busy; };

protected:

	static void loadNode(const xml_node& node, FaultTreeNode* ft, FTResults* queue);

	static void handleBasicEventSet(xml_node &child, const string& id, const char* name, FaultTreeNode* tree, FTResults* queue);
	static void handleFeatureVP(xml_node &child, const string& id, const char* name, FaultTreeNode* tree, FTResults* queue);
	static void handleRedundancyVP(xml_node &child, const string& id, const char* name, FaultTreeNode* tree, FTResults* queue);

	static double parseFailureRate(const xml_node &child);

private:
	FuzzTreeImport(const string& fileName);

	virtual bool loadRootNode() override;

	void loadTree(FTResults* queue);

	FaultTreeNode* m_tree;
	std::vector<std::thread> m_running;

	bool m_busy;
};