#include "TestUtil.h"
#include "pugixml.hpp"
#include "ResultStruct.h"
#include "Constants.h"

SimulationResult readResultFile(const std::string& fn)
{
	using namespace simulation;

	SimulationResult res;
	pugi::xml_document resultDoc;
	if (!resultDoc.load_file(fn.c_str()))
		return res;
	pugi::xml_node topNode = resultDoc.child(SIMULATION_RESULT);
	if (topNode.empty()) return res;

	res.reliability			= topNode.attribute(RELIABILITY).as_double(-1.0);
	res.meanAvailability	= topNode.attribute(AVAILABILTIY).as_double(-1.0);
	res.mttf				= topNode.attribute(MTTF).as_double(-1.0);
	res.nRounds				= topNode.attribute(NROUNDS).as_uint(0);
	res.nFailures			= topNode.attribute(NFAILURES).as_uint(0);

	return res;
}


