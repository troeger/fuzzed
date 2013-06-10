#pragma once

#include <boost/filesystem/path.hpp>
#include <tuple>

typedef std::tuple<std::string, std::string, int> ArcSpec;

struct Place
{
	Place(const std::string& ID, const unsigned int& initialMarking, const unsigned int& capacity) :
		_id(ID), _initialMarking(initialMarking), _capacity(capacity) {}

	std::string _id;
	unsigned int _initialMarking;
	unsigned int _capacity;
};

struct Transition
{
	Transition(const std::string& ID, const unsigned int& prio) :
		_id(ID), _priority(prio) {}
	
	std::string _id;
	unsigned int _priority;
};

struct Arc
{
	Arc(const std::string& from, const std::string& to, const unsigned int& count) :
		_from(from), _to(to), _count(count) {}
	
	std::string _from;
	std::string _to;
	unsigned int _count;
};

class PTNet
{
public:
	static const PTNet* loadNet(const boost::filesystem::path& path);

	PTNet();

	std::vector<Transition>	m_transitions;
	std::vector<Place>		m_places;
	std::vector<Arc>		m_arcs;
};