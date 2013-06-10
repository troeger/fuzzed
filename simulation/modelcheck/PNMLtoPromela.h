#pragma once

#include <boost/filesystem/path.hpp>

class PTNet;

class PNMLtoPromela
{
public:
	static void convertFile(const boost::filesystem::path& pnmlPath, const boost::filesystem::path& outPath);

	void convertToPromela();

private:
	PNMLtoPromela(const boost::filesystem::path& pnmlPath, const boost::filesystem::path& outPath);
	~PNMLtoPromela();

	const PTNet* m_net;

	const boost::filesystem::path m_outPath;
};