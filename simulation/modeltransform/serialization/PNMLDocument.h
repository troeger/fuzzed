#pragma once
#include "PNDocument.h"

class PNMLDocument : public PNDocument
{
public:
	PNMLDocument();
	
	virtual ~PNMLDocument();

	virtual int addTimedTransition(long double rate, const std::string& label = "") override;
	virtual int addImmediateTransition(unsigned int priority = 1, const std::string& label = "") override;

	virtual int addPlace(
		int initialMarking,
		int capacity = 1, 
		const std::string& label = "",
		PlaceSemantics semantics = DEFAULT_PLACE) override;

	virtual int addTopLevelPlace(const std::string& label) override;

	virtual void addInhibitorArc(
		int inhibitingPlace,
		int inhbitedTransitions,
		int tokenCount = 0) override;
	
protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const std::string& inscription = "x") override;
	
	// helpers
	static void setName(pugi::xml_node node, const std::string& label);
	// adds a child node: <value>val</value>
	static void setNodeValue(pugi::xml_node name, const std::string& val);

	virtual void initXML() override;
};
