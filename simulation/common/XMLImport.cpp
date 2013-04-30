#include "XMLImport.h"

#include <boost/filesystem/operations.hpp>
#include <iostream>

namespace fs = boost::filesystem;

bool XMLImport::validateAndLoad()
{
	cout << "loading " << m_file.generic_string() << endl;
	try
	{
		if (fs::exists(m_file) && fs::is_regular_file(m_file))
		{
			if (!m_document.load_file(m_file.generic_string().c_str()))
				return false;

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
	return false;
}

XMLImport::XMLImport(const string& fileName)
	: m_file(fileName),
	m_bLoaded(false)
{}