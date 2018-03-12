#include "PNDocument.h"
#include "Constants.h"

#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <iostream>
#include <cassert>
#if IS_WINDOWS 
	#pragma warning(pop) 
#endif

using namespace std;
using namespace pugi;

PNDocument::PNDocument(int id /*= 0*/)
	: xml_document(),
	m_transitionCount(0), 
	m_placeCount(0), 
	m_arcCount(0),
	m_bSaved(false),
	m_id(id)
{}

PNDocument::~PNDocument()
{
	if (!m_bSaved)
		cout << "PNML Document was not saved!" << endl;
}

bool PNDocument::save(const string& fileName)
{
	m_bSaved = xml_document::save_file(fileName.c_str());
	return m_bSaved;
}

void PNDocument::placeToTransition(int placeID, int transitionID, int tokenCount, const string& inscription /*= "x"*/)
{
	addArc(placeID, transitionID, tokenCount, PLACE_TO_TRANSITION, inscription);
}

void PNDocument::transitionToPlace(int transitionID, int placeID, int tokenCount, const string& inscription /*= "x"*/)
{
	addArc(placeID, transitionID, tokenCount, TRANSITION_TO_PLACE, inscription);
}

void PNDocument::addUserDescription(const string& description)
{
	assert(m_root && "cannot add description without document root");
	m_root.append_child(USER_DESCRIPTION_LABEL).append_child(node_pcdata).set_value(description.c_str());
}
