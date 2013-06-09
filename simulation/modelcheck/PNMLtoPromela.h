#pragma once

#include <boost/filesystem/path.hpp>

class PetriNet;

class PNMLtoPromela
{
public:
	static void convertFile(const boost::filesystem::path& pnmlPath, const boost::filesystem::path& outPath);

	bool checkPetriNet();
	void convertToPromela();

private:
	PNMLtoPromela(const boost::filesystem::path& pnmlPath, const boost::filesystem::path& outPath);
	~PNMLtoPromela();

	PetriNet* m_net;

	const boost::filesystem::path m_outPath;
};