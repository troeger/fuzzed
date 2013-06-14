#pragma once
#include "PNDocument.h"

class TNDocument : public PNDocument
{
public:
	TNDocument();
	TNDocument(const std::string& fileName);

	virtual int addTimedTransition(long double rate, const std::string& label = "") override;
	virtual int addImmediateTransition(const unsigned int priority = 1, const std::string& label = "") override;
	virtual int addTopLevelPlace(const std::string& label) override;
	virtual int addPlace(int initialMarking, int capacity = 1,  const std::string& label = "", PlaceSemantics semantics = DEFAULT_PLACE) override;
	
protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const std::string& inscription = "x") override;

	void writeHeader();
};