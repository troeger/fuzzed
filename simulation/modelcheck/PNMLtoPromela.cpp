#include "PNMLtoPromela.h"
#include "petrinet/PNMLImport.h"
#include "petrinet/PetriNet.h"

#include <boost/format.hpp>

using std::string;


/************************************************************************/
/* http://www.ieice.org/proceedings/ITC-CSCC2008/pdf/p285_F1-3.pdf      */
/************************************************************************/

const string promelaTemplate = ""
	"#define nPlaces %1% \n"
	"#define nTransitions %2% \n"
	"#define inp1(x1) (x1>0) -> x1-- \n"
	"#define out1(x1) x1++ \n"
	"int M[nPlaces]; \n"
	"int T[nTransitions]; \n"
	"proctype net() {\n"
	"	do\n"
	"		%4%" // connect arcs and transitions
	"	od\n"
	"}\n"
	"init {\n"
	"	%3% \n" // initialize marking
	"	run net();"
	"}\n";

const string arcTemplate1to1 = ":: d_step{ inp1(M[%1%]) -> T[%2%]++; out1(M[%3%]); skip; } \n";
const string markingTemplate = "M[%1%] = %2% \n";

PNMLtoPromela::PNMLtoPromela(const boost::filesystem::path& pnmlPath, const boost::filesystem::path& outPath)
	: m_net(PNMLImport::loadPNML(pnmlPath.generic_string())),
	m_outPath(outPath)
{}

void PNMLtoPromela::convertFile(const boost::filesystem::path& pnmlPath, const boost::filesystem::path& outPath)
{
	PNMLtoPromela converter(pnmlPath, outPath);
	converter.checkPetriNet();
	converter.convertToPromela();
}

void PNMLtoPromela::convertToPromela()
{
	boost::format(promelaTemplate);
}

bool PNMLtoPromela::checkPetriNet()
{
	return m_net && m_net->valid();
}
