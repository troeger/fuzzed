#include "XMLImport.h"

#include <boost/filesystem/operations.hpp>
#include <iostream>

namespace fs = boost::filesystem;

bool XMLImport::validateAndLoad()
{
	cout << "loading " << m_file.generic_string() << endl;
	bool valid = false;
	try
	{
		if (fs::exists(m_file) && fs::is_regular_file(m_file))
		{
			valid = m_document.load_file(m_file.generic_string().c_str());

#ifdef DEBUG
			cout << "Loaded XML: " << endl;
			m_document.print(std::cout);
#endif
			m_bLoaded = loadRootNode();
			return m_bLoaded;
		}
	}
	catch (exception& e)
	{
		cout << e.what();
		return false;
	}
}

XMLImport::XMLImport(const string& fileName)
	: m_file(fileName)
{}