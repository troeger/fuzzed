#pragma once
#include <utility>
#include <typeinfo>

using namespace std;

template <typename BaseType>
class Visitable : public BaseType
{
public:
	template <typename... Args>
	Visitable(Args&&... arg) : BaseType(std::forward<Args>(arg)...) {}

	virtual void accept(int i)
	{
		std::cout << typeid(BaseType).name() << " " << i << std::endl;
	}
};