#include "FuzzTreeTransform.h"
#include "Constants.h"

#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <boost/filesystem/operations.hpp>
#include <boost/range/counting_range.hpp>
#include <exception>
#include <iostream>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif
#include "util.h"
#include <omp.h>

using namespace pugi;
using namespace std;
using namespace fuzzTree;
using namespace boost;

void FuzzTreeTransform::transformFuzzTree(const string& fileName, const string& targetDir)
{
	try
	{
		FuzzTreeTransform tranform(fileName, targetDir);
		if (!tranform.validateAndLoad())
		{
			cout << "Could not load FuzzTree" << endl;
			return;
		}
		tranform.loadTree();
	}
	catch (std::exception& e)
	{
		cout << "Error during FuzzTree Transformation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Error during FuzzTree Transformation" << endl;
	}
}

void FuzzTreeTransform::loadNode(const xml_node& node, xml_node& previous, xml_document* doc, std::set<int> includedIds)
{
	const int previousId = previous.attribute("id").as_int(-1);
	assert(previousId >= 0);
	
	for (auto child : node.children("children"))
	{
		const string typeDescriptor = child.attribute("xsi:type").as_string();

		const int id		= child.attribute("id").as_int(-1);
		const char* name	= child.attribute("name").as_string();
		const bool opt		= child.attribute(OPTIONAL_ATTRIBUTE).as_bool(false);

		if (id < 0)
			continue;
		
		if (opt)
		{ // branch and create a new tree - WITH the optional node	
			auto itID = includedIds.find(id);
			if (itID == includedIds.end())
			{
				xml_document* copiedDoc = new xml_document();
				copiedDoc->reset(*doc);
				copiedDoc->print(cout);
								
				xml_node node = copiedDoc->child(TOP_EVENT);
				assert(!node.empty());

				xml_node copiedPrevious;
				for (xml_node c : node.children("children"))
				{
					if (c.attribute("id").as_int(-1) == previousId)
					{
						copiedPrevious = c;
						break;
					}
				}
				assert(!copiedPrevious.empty());

				xml_node optionalNode = copiedPrevious.append_copy(child);
				optionalNode.print(cout);
				optionalNode.remove_attribute("optional");

				std::set<int> newOptIds(includedIds);
				newOptIds.emplace(id);

				// restart at the same level
				boost::function<void()> branchedTask = boost::bind(
					&FuzzTreeTransform::loadNodeInBranch, this, node, copiedPrevious, copiedDoc, newOptIds);

				m_threadPool.schedule(branchedTask);
				continue;
			}
			else
			{
				includedIds.erase(itID);
				continue;
			}
		}
		
		/************************************************************************/
		/* Basic Events/ Leaf Nodes                                             */
		/************************************************************************/
		if (typeDescriptor == BASIC_EVENT)
		{
			previous.append_copy(child);
			continue;
		}
		else if (typeDescriptor == UNDEVELOPED_EVENT)
		{
			previous.append_copy(child);
			continue;
		}

		/************************************************************************/
		/* Configuration Points                                                 */
		/************************************************************************/
		else if (typeDescriptor == FEATURE_VP)
		{
			handleFeatureVP(child, previous, doc);
			continue;
		}
		else if (typeDescriptor == REDUNDANCY_VP)
		{
			handleRedundancyVP(child, previous, doc);
			continue;
		}
		else if (typeDescriptor == BASIC_EVENT_SET)
		{
			handleBasicEventSet(child, previous, doc);
			continue;
		}
		else if (typeDescriptor == TRANSFER_GATE)
		{
			continue;
		}

		/************************************************************************/
		/* Gates                                                                */
		/************************************************************************/

		else if (isFaultTreeGate(typeDescriptor))
		{ // basic gates can just be copied
			xml_node lastNode = previous.append_child("children");
			shallowCopy(child, lastNode);

			// recurse!
			loadNode(child, lastNode, doc, includedIds);
		}
		else
		{
			assert(false);
		}
	}
}

void FuzzTreeTransform::handleBasicEventSet(
	const xml_node& child, 
	xml_node& previouslyAdded,
	xml_document* doc)
{
	const int numEvents = child.attribute("quantity").as_int(1);
	if (numEvents <= 0)
	{
		throw runtime_error("Invalid quantity in Basic Event Set!");
	}

	for (auto i : boost::counting_range(0, numEvents))
	{
		xml_node basicEvent = previouslyAdded.append_child("children");
		shallowCopy(child, basicEvent);
		basicEvent.remove_attribute(NODE_TYPE);
		basicEvent.append_attribute(NODE_TYPE).set_value(BASIC_EVENT);
		
		// TODO event probability
	}
}

void FuzzTreeTransform::handleFeatureVP(const xml_node &child, xml_node& previous, xml_document* doc)
{
	// TODO
}

void FuzzTreeTransform::handleRedundancyVP(const xml_node &child, xml_node& previous, xml_document* doc)
{
	// TODO
}

FuzzTreeTransform::FuzzTreeTransform(const string& fileName, const string& targetDir)
	: XMLImport(fileName), 
	m_targetDir(targetDir), 
	m_count(0)
{
	if (!filesystem::is_directory(targetDir))
	{
		m_targetDir = filesystem::path(fileName);
		m_targetDir.remove_filename();

		cout << "Directory " << targetDir << " not found, defaulting to " << m_targetDir.generic_string() << endl;

		if (!filesystem::is_directory(m_targetDir))
			throw runtime_error("Could not find target directory");
	}
	
	if (!filesystem::is_regular_file(fileName))
	{
		throw runtime_error("File not found " + fileName);
	}

	m_threadPool = threadpool::fifo_pool(omp_get_max_threads()-1);
}

FuzzTreeTransform::~FuzzTreeTransform()
{
	m_threadPool.wait();
	m_threadPool.clear();
}

bool FuzzTreeTransform::loadRootNode()
{
	m_rootNode = m_document.child(FUZZ_TREE);
	if (!m_rootNode)
	{
		throw runtime_error("Missing FuzzTree Root Node");
	}
	return true;
}

void FuzzTreeTransform::loadTree()
{
	xml_document* newDoc = new xml_document();
	xml_node newTop = newDoc->append_child(TOP_EVENT);
	shallowCopy(m_rootNode.child(TOP_EVENT), newTop);

	loadNode(m_rootNode.child(TOP_EVENT), newTop, newDoc, std::set<int>());
	
	const string fileName = 
		m_targetDir.generic_string() + "\\" +
		m_file.filename().generic_string() + 
		util::toString(m_count++) + ".fuzztree_";

	newDoc->save_file(fileName.c_str());
	delete newDoc;
}

void FuzzTreeTransform::shallowCopy(const xml_node& proto, xml_node& copiedNode)
{
	copiedNode.set_name(proto.name());
	copiedNode.set_value(proto.value());

	for (auto attr = proto.attributes_begin(); attr != proto.attributes_end(); ++attr)
	{
		copiedNode.append_attribute(attr->name()).set_value(attr->value());
	}
}

bool FuzzTreeTransform::isFaultTreeGate(const string& typeDescriptor)
{
	return
		typeDescriptor == AND_GATE ||
		typeDescriptor == OR_GATE ||
		typeDescriptor == VOTING_OR_GATE;// TODO dynamic gates
}

void FuzzTreeTransform::loadNodeInBranch(const xml_node& node, xml_node& previous, xml_document* newDoc, std::set<int> optIds)
{
	loadNode(node, previous, newDoc, optIds);

	const string fileName = 
		m_targetDir.generic_string() + "\\" +
		m_file.filename().generic_string() + 
		util::toString(m_count++) + ".fuzztree_";

	newDoc->save_file(fileName.c_str());
	delete newDoc;
}