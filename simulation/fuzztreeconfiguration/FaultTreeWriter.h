#pragma once

#include <pugixml.hpp>

class FaultTreeWriter : public pugi::xml_writer
{
public:
	FaultTreeWriter(ReaderWriterQueue* results, FuzzTreeImport* importer);
	virtual ~FaultTreeWriter();


protected:

};