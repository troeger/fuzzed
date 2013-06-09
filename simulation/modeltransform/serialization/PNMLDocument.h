#pragma once
#include "PNDocument.h"

class PNMLDocument : public PNDocument
{
public:
	PNMLDocument();
	PNMLDocument(const std::string& fileName);

	virtual ~PNMLDocument();

	virtual int addTimedTransition(long double rate, const std::string& label = "") override;
	virtual int addImmediateTransition(long double weight = 1.0, const std::string& label = "") override;

	virtual int addPlace(int initialMarking, int capacity = 1,  const std::string& label = "", PlaceSemantics semantics = DEFAULT_PLACE) override;
	virtual int addTopLevelPlace(const std::string& label) override;
	
	virtual void addSequenceConstraint(const std::vector<int>& sequence, SequenceType type) override;

protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const std::string& inscription = "x") override;
	int addTransition(long double rate, bool isTimed, const std::string& label = "");
	
	// helpers
	static void setName(pugi::xml_node node, const std::string& label);
	// adds a child node: <value>val</value>
	static void setNodeValue(pugi::xml_node name, const std::string& val);

	virtual void initXML() override;
};
