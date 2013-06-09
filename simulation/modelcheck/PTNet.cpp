#include <pugixml.hpp>
#include "PTNet.h"
#include "Constants.h"

using namespace PNML;
using namespace pugi;
using namespace std;

PTNet::PTNet()
{}

const PTNet* PTNet::loadNet(const boost::filesystem::path& path)
{
	PTNet* net = new PTNet();
	return net;
}

