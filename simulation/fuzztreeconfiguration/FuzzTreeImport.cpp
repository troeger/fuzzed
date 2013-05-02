#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <algorithm>
#include <iostream>
#include <boost/range/counting_range.hpp>
#if IS_WINDOWS 
#pragma warning(pop)
#endif


#include "FuzzTreeImport.h"
#include "FaultTreeIncludes.h"
#include "Constants.h"
#include "util.h"

using namespace fuzzTree;

FaultTreeNode* FuzzTreeImport::loadFaultTree(const string& fileName)
{
	FuzzTreeImport import(fileName);
	FTResults* results = new FTResults();

	try
	{
		if (!import.validateAndLoad())
			return nullptr;

		import.loadTree(results);
	}
	catch (exception& e)
	{
		cout << "Error during import " << e.what() << endl;
		return nullptr;
	}

	FaultTreeNode* res = nullptr;
	results->try_dequeue(res);
	delete results;
	return res;
}	

std::pair<FuzzTreeImport*,FTResults*> FuzzTreeImport::loadFaultTreeAsync(const string& fileName)
{
	FuzzTreeImport* import = new FuzzTreeImport(fileName);
	FTResults* results = new FTResults();

	try
	{
		if (!import->validateAndLoad())
			return make_pair(import, results);

		import->loadTree(results);
	}
	catch (std::exception& e)
	{
		cout << "Error during import " << e.what() << endl;
		return make_pair(import, results);
	}

	return make_pair(import, results);
}

FuzzTreeImport::FuzzTreeImport(const string& fileName)
	: XMLImport(fileName), m_busy(false)
{}

bool FuzzTreeImport::loadRootNode()
{
	m_rootNode = m_document.child(FUZZ_TREE);
	if (!m_rootNode)
	{
		cout << "Missing FuzzTree Node" << endl;
		return false;
	}
	return true;
}

void FuzzTreeImport::loadTree(FTResults* queue)
{
	m_busy = true;
	m_running.emplace_back( std::thread([this, queue]() -> void
	{
		assert(m_rootNode);
		try
		{
			const xml_node topEvent = m_rootNode.child("topEvent");
			if (!topEvent)
				throw runtime_error("Missing TopEvent");

			auto tree = new TopLevelEvent(topEvent.attribute("id").as_int());

			loadNode(topEvent, tree, queue);
			queue->enqueue(tree);
		}
		catch (std::exception& e)
		{
			cout << "Error during asynchronous import" << e.what() << endl;
		}
		catch (...)
		{
			cout << "Unknown error during asynchronous import" << endl;
		}

		m_busy = false;
	}));
}

void FuzzTreeImport::loadNode(const xml_node& node, FaultTreeNode* tree, FTResults* results)
{
	assert(tree != nullptr);

	for (xml_node& child : node.children("children"))
	{
		const string typeDescriptor = child.attribute("xsi:type").as_string();

		const int id		= child.attribute("id").as_int(-1);
		const char* name	= child.attribute("name").as_string();
		const bool opt		= child.attribute(OPTIONAL_ATTRIBUTE).as_bool(false);

		if (id < 0)
			throw runtime_error("Invalid ID");

		/************************************************************************/
		/* Basic Events/ Leaf Nodes                                             */
		/************************************************************************/
		if (typeDescriptor == BASIC_EVENT)
		{
			tree->addChild(new BasicEvent(id, parseFailureRate(child), name));
			continue;
		}
		else if (typeDescriptor == UNDEVELOPED_EVENT)
		{
			tree->addChild(new UndevelopedEvent(id, parseFailureRate(child), name));
			continue;
		}

		/************************************************************************/
		/* Configuration Points                                                 */
		/************************************************************************/
		else if (typeDescriptor == FEATURE_VP)
		{
			handleFeatureVP(child, id, name, tree, results);
			continue;
		}
		else if (typeDescriptor == REDUNDANCY_VP)
		{
			handleRedundancyVP(child, id, name, tree, results);
			continue;
		}
		else if (typeDescriptor == BASIC_EVENT_SET)
		{
			handleBasicEventSet(child, id, name, tree, results);
			continue;
		}
		else if (typeDescriptor == TRANSFER_GATE)
		{
			// TODO
			continue;
		}

		/************************************************************************/
		/* Gates                                                                */
		/************************************************************************/
		FaultTreeNode* gate = nullptr;
		if (typeDescriptor == AND_GATE)
		{
			gate = new ANDGate(id, name);
		}
		else if (typeDescriptor == OR_GATE)
		{
			gate = new ORGate(id, name);
		}
		else if (typeDescriptor == VOTING_OR_GATE)
		{
			const int k = child.attribute(VOTING_OR_K).as_int(-1);
			if (k < 0)
				throw runtime_error("Invalid k for VotingORGate");

			gate = new VotingORGate(id, k, name);
		}
		else if (typeDescriptor == COLD_SPARE_GATE)
		{
			const string spareIds = child.attribute(SPARE_ID_ATTRIBUTE).as_string("");
			vector<int> spareIndices;
			util::tokenizeIntegerString(spareIds, spareIndices);

			gate = new SpareGate(id, set<int>(spareIndices.begin(), spareIndices.end()), name);
		}
		else if (typeDescriptor == PAND_GATE)
		{
			const string prioIds = child.attribute(PRIO_ID_ATTRIBUTE).as_string("");
			vector<int> prioIndices;
			util::tokenizeIntegerString(prioIds, prioIndices);

			gate = new PANDGate(id, set<int>(prioIndices.begin(), prioIndices.end()), name);
		}
		else
		{
			cout << "Unrecognized type descriptor: " << typeDescriptor
				<< "...ignoring this node.";
			continue;

		}
		if (gate != nullptr)
			tree->addChild(gate);

		// Recurse
		loadNode(child, gate, results);
	}
}

double FuzzTreeImport::parseFailureRate(const xml_node &child)
{
	for (const auto& probabilityNode : child.children("probability"))
	{
		if (!probabilityNode)
			throw runtime_error("Could not find Probability Node for Basic event");

		// TODO find an adequate crisp number in this case
		if (string(probabilityNode.attribute(NODE_TYPE).as_string()) != CRISP_NUM)
			throw runtime_error("Fuzzy Probabilites are not supported yet");

		return probabilityNode.attribute("value").as_double(-1.0);
	}
	throw runtime_error("Unable to parse failure rate");
	return -1.0;
}

void FuzzTreeImport::handleBasicEventSet(
	xml_node &child, 
	const int id, 
	const char* name, 
	FaultTreeNode* tree,
	FTResults* results)
{
	const int numEvents = child.attribute(BASIC_EVENT_SET_QUANTITY).as_int(1);
	if (numEvents <= 0)
	{
		throw runtime_error("Invalid quantity in Basic Event Set!");
	}

	unsigned int count = 0;
	while (count < numEvents)
	{
		// TODO unique ids
		tree->addChild(new BasicEvent(id*100+(++count), parseFailureRate(child), name));
	}
}

void FuzzTreeImport::handleFeatureVP(
	xml_node &node, 
	const int id,
	const char* name, 
	FaultTreeNode* tree,
	FTResults* results)
{
	// find the top level node and clone it
	const FaultTreeNode* const top = tree->getRoot();
	const int parentID = tree->getId();

	for (xml_node& child : node.children("children"))
	{
		FaultTreeNode* newTree = top->clone();
		assert(newTree != nullptr);
		loadNode(child, newTree->getChildById(parentID), results);
		results->enqueue(newTree);
	}
}

void FuzzTreeImport::handleRedundancyVP(
	xml_node &child, 
	const int id, 
	const char* name, 
	FaultTreeNode* tree,
	FTResults* results)
{
	const int from = child.attribute("start").as_int(-1);
	const int to = child.attribute("end").as_int(-1);
	if (from < 0 || to < 0 || from > to)
		throw runtime_error("Invalid boundaries for RedundancyGate");

	const char* const formula = child.attribute("formula").as_string();
	const int parentID = tree->getId();

	// find the top level node and clone it
	const FaultTreeNode* const top = tree->getRoot();
	for (int i : boost::counting_range(from, to+1))
	{
		FaultTreeNode* newTree = top->clone();
		assert(newTree != nullptr);

		RedundancyGate* gate = new RedundancyGate(id, from, to, i, formula, name);
		if (!gate->isValidConfiguration())
			continue;

		newTree->addChildBelow(parentID, gate);
		loadNode(child, newTree->getChildById(id), results);

		if (!gate->isValid()) // e.g. if the gate turned out to have less children than numVotes
			continue;

		results->enqueue(newTree);
	}
}

FuzzTreeImport::~FuzzTreeImport()
{
	for (auto& thread : m_running)
		thread.join();
}
