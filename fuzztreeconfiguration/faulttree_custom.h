#pragma once
#include <utility>
#include <iostream>
#include <typeinfo>
#include "Visitor.h"

namespace faulttree
{
	template <typename BaseType>
	class Visitable : public BaseType
	{
	public:
		template <typename... Args>
		Visitable(Args&&... arg) : BaseType(std::forward<Args>(arg)...) {}

		virtual Visitable<BaseType>*
			_clone (xml_schema::Flags f = 0, xml_schema::Container* c = 0) const
		{
			return new Visitable<BaseType>(*this, f, c);
		}

		virtual void accept(Visitor& visitor)
		{
			visitor.visit(this);
		}
	};
}