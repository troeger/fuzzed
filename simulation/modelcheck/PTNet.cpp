#include <pugixml.hpp>
#include <boost/filesystem/operations.hpp>

#include "PTNet.h"
#include "Constants.h"
#include "util.h"

using namespace PNML;
using namespace pugi;
using namespace std;
namespace fs = boost::filesystem;

PTNet::PTNet()
{}

const PTNet* PTNet::loadNet(const boost::filesystem::path& path)
{
	if (!fs::exists(path) || !fs::is_regular_file(path)) return nullptr;

	xml_document doc;
	if (!doc.load_file(path.generic_string().c_str())) return nullptr;
	
	xml_node root = doc.child(PNML_TAG);
	if (!root) return nullptr;
	
	root = root.child(ROOT_TAG);
	if (!root) return nullptr;

	PTNet* net = new PTNet();
	
	// Places
	for (const xml_node& child : root.children(PLACE_TAG))
	{
		const int initialMarking = util::parseIntegerValue(child, INITIALMARKING_TAG, 0);
		const string ID = child.attribute(ID_ATTRIBUTE).as_string();
		const int capacity = util::parseIntegerValue(child, CAPACITY_TAG, 0);

		net->m_places.emplace_back(ID, initialMarking, capacity);
	}

	// Transitions
	for (const xml_node& child : root.children(TRANSITION_TAG))
	{
		const string ID = child.attribute(ID_ATTRIBUTE).as_string();
		const int priority = util::parseIntegerValue(child, PRIORITY_TAG, 0);

		net->m_transitions.emplace_back(ID, priority);
	}

	// Arcs
	for (const xml_node& child : root.children(ARC_TAG))
	{
		const string src = child.attribute(SOURCE_TAG).as_string();
		const string dst = child.attribute(TARGET_TAG).as_string();

		int weight = 1;
		const xml_node valNode = child.child(INSCRIPTION_TAG);
		if (!valNode.empty())
		{ // in the inscription node, the number of tokens is written comma-separated from the token type
			xml_node c = valNode.child(VALUE_TAG);
			if (!valNode)
				throw runtime_error("Value node not found");

			vector<int> results;
			util::tokenizeIntegerString(c.text().as_string(""), results);
			weight = results.back();
		}

		net->m_arcs.emplace_back(src, dst, weight);
	}

	return net;
}

