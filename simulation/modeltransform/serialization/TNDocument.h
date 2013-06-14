#pragma once
#include "PNDocument.h"
#include "Types.h"

#include <map>
#include <fstream>

class TNDocument : public PNDocument
{
public:
	TNDocument();
	virtual ~TNDocument();

	virtual int addTimedTransition(long double rate, const std::string& label = "") override;
	virtual int addImmediateTransition(unsigned int priority = 1, const std::string& label = "") override;
	virtual int addTopLevelPlace(const std::string& label) override;
	virtual int addPlace(int initialMarking, int capacity = 1,  const std::string& label = "", PlaceSemantics semantics = DEFAULT_PLACE) override;
	
	virtual bool save(const std::string& fileName) override;

protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const std::string& inscription = "x") override;

	void writeHeader();

	std::map<std::string, std::string> m_transitions;
	std::map<std::string, std::string> m_places;
	std::vector<std::string> m_measures; // TODO
};