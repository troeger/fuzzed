#pragma once

#include <boost/filesystem/path.hpp>
#include <tuple>

typedef std::tuple<std::string, std::string, int> ArcSpec;

struct Place
{
	std::string id;
	unsigned int initialMarking;
	unsigned int capacity;
};

struct Transition
{
	std::string id;
	unsigned int priority;
};

struct Arc
{
	std::string to;
	std::string from;
	unsigned int count;
};

class PTNet
{
public:
	const PTNet* loadNet(const boost::filesystem::path& path);

private:
	PTNet();

	std::vector<Transition>	m_transitions;
	std::vector<Place>		m_places;
	std::vector<Arc>		m_arcs;
};