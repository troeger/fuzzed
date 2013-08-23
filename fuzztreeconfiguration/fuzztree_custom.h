#pragma once
#include <utility>
#include "xsd\cxx\tree\elements.hxx"
#include "xsd\cxx\xml\dom\parsing-source.hxx"

class Visitor;

namespace fuzztree
{
	template <class C>
	class Visitable : public xsd::cxx::tree::container
	{
	protected:
		C contained;
		virtual void parse(::xsd::cxx::xml::dom::parser< char >& p, ::xml_schema::Flags f) { contained.parse(p, f); };

	public:
		template <typename... Args> 
		Visitable(Args&&... a) : contained(std::forward<Args>(a)...) {};

		virtual C* operator->() { return &contained; };
	};
}
