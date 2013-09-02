#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <algorithm>
#include <iostream>
#include <boost/range/counting_range.hpp>
#if IS_WINDOWS 
#pragma warning(pop)
#endif

#include "FaultTreeImport.h"
#include "FaultTreeIncludes.h"
#include "Constants.h"
#include "util.h"

using namespace faultTree;
using namespace std;
using namespace pugi;

FaultTreeNode::Ptr FaultTreeImport::loadFaultTree(const string& fileName) noexcept
{
	try
	{
		FaultTreeImport import(fileName);
		if (!import.validateAndLoad())
			return nullptr;

		return import.loadTree();
	}
	catch (exception& e)
	{
		cout << "Error during import " << e.what() << endl;
		return nullptr;
	}
	catch (...)
	{
		cout << "Unknown error during import " << endl;
		return nullptr;
	}
}	


FaultTreeImport::FaultTreeImport(const string& fileName)
	: XMLImport(fileName)
{}

bool FaultTreeImport::loadRootNode()
{
	m_rootNode = m_document.child(FAULT_TREE);
	if (!m_rootNode)
	{
		cout << "Missing FuzzTree Node" << endl;
		return false;
	}
	return true;
}

FaultTreeNode::Ptr FaultTreeImport::loadTree()
{
	assert(m_rootNode);
	const xml_node topEvent = m_rootNode.child(TOP_EVENT);
	if (!topEvent)
		EXIT_ERROR("Missing Top Event");

	FaultTreeNode::Ptr tree = make_shared<TopLevelEvent>(topEvent.attribute("id").as_string());
	loadNode(topEvent, tree);
	return tree;
}

void FaultTreeImport::loadNode(const xml_node& node, FaultTreeNode::Ptr tree)
{
	assert(tree != nullptr);

	for (xml_node& child : node.children("children"))
	{
		const string id = child.attribute("id").as_string();
		if (id.empty()) throw runtime_error("Invalid ID");

		const char* name	= child.attribute(NAME_ATTRIBUTE).as_string();
		const string typeDescriptor = child.attribute(NODE_TYPE).as_string();

		/************************************************************************/
		/* Basic Events/ Leaf Nodes                                             */
		/************************************************************************/
		if (typeDescriptor == BASIC_EVENT)
		{
			tree->addChild(make_shared<BasicEvent>(id, parseFailureRate(child), name));
			continue; // end recursion
		}
		else if (typeDescriptor == UNDEVELOPED_EVENT)
		{
			tree->addChild(make_shared<UndevelopedEvent>(id, parseFailureRate(child), name));
			continue; // end recursion
		}

		/************************************************************************/
		/* Gates                                                                */
		/************************************************************************/
		FaultTreeNode::Ptr gate = nullptr;
		if (typeDescriptor == AND_GATE)
		{
			gate = make_shared<ANDGate>(id, name);
		}
		else if (typeDescriptor == OR_GATE)
		{
			gate = make_shared<ORGate>(id, name);
		}
		else if (typeDescriptor == XOR_GATE)
		{
			gate = make_shared<XORGate>(id, name);
		}
		else if (typeDescriptor == VOTING_OR_GATE)
		{
			const int k = child.attribute(VOTING_OR_K).as_int(-1);
			if (k < 0)
				throw runtime_error("Invalid k for VotingORGate");

			gate = make_shared<VotingORGate>(id, k, name);
		}
		else if (typeDescriptor == COLD_SPARE_GATE)
		{
			const string primaryId = child.attribute(SPARE_ID_ATTRIBUTE).as_string("");
			gate = make_shared<SpareGate>(id, primaryId, 1.0, name);
		}
		else if (typeDescriptor == PAND_GATE)
		{
			const string prioIds = child.attribute(PRIO_ID_ATTRIBUTE).as_string("");
			vector<string> prioIndices;
			util::tokenizeString(prioIds, prioIndices);

			gate = make_shared<PANDGate>(id, prioIndices, name);
		}
		else if (typeDescriptor == SEQ_GATE)
		{
			const string sequence = child.attribute(SEQUENCE_ATTRIBUTE).as_string("");
			vector<string> idSequence;
			util::tokenizeString(sequence, idSequence);

			gate = make_shared<SEQGate>(id, idSequence, name);
		}
		else
		{
			// TODO: throw, exit or ignore?
			throw runtime_error("Unrecognized node type: " + typeDescriptor);
		}

		assert(gate);
		tree->addChild(gate);

		// Recurse
		loadNode(child, gate);
	}
}

double FaultTreeImport::parseFailureRate(const xml_node &child)
{
	// TODO support failure rate directly
	for (const auto& probabilityNode : child.children("probability"))
	{
		if (string(probabilityNode.attribute(NODE_TYPE).as_string()) != CRISP_NUM)
			throw runtime_error("Fuzzy Probabilites are not supported yet");

		return probabilityNode.attribute("value").as_double(-1.0);
	}
	return -1.0;
}

FaultTreeImport::~FaultTreeImport()
{}