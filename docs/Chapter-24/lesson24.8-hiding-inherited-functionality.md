24.8 — 隐藏继承功能
======================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2017年6月27日  
2024年7月17日更新  

**改变继承成员的访问级别**  
C\+\+允许在派生类中修改继承成员的访问说明符（access specifier）。具体方法是通过*using声明（using declaration）*在派生类的新访问说明符下标识（作用域限定的）基类成员。

例如以下基类：
```
#include <iostream>

class Base
{
private:
    int m_value {};

public:
    Base(int value)
        : m_value { value }
    {
    }

protected:
    void printValue() const { std::cout << m_value; }
};
```
由于Base::printValue()声明为protected（受保护），只能被Base或其派生类调用，外部无法访问。

定义派生类将printValue()的访问级别改为public（公共）：
```
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }

    // Base::printValue继承时为protected，外部无法访问
    // 通过using声明改为public
    using Base::printValue; // 注意：此处不带括号
};
```
现在以下代码可以正常运行：
```
int main()
{
    Derived derived { 7 };

    // printValue在Derived中是public，可以调用
    derived.printValue(); // 输出7
    return 0;
}
```
只能修改派生类原本有访问权限的基类成员的访问说明符。因此永远无法将基类私有（private）成员的访问说明符改为protected或public，因为派生类无法访问基类的private成员。

**功能隐藏**  
在C\+\+中，除了修改源代码外，无法直接移除或限制基类功能。但可以通过派生类隐藏基类功能，使其无法通过派生类访问。这可以通过修改相关访问说明符实现。

例如将public成员改为private：
```
#include <iostream>

class Base
{
public:
	int m_value{};
};

class Derived : public Base
{
private:
	using Base::m_value;

public:
	Derived(int value) : Base { value }
	{
	}
};

int main()
{
	Derived derived{ 7 };
	std::cout << derived.m_value; // 错误：m_value在Derived中是private

	Base& base{ derived };
	std::cout << base.m_value; // 正常：m_value在Base中是public

	return 0;
}
```
这种方式允许我们对设计不佳的基类进行数据封装。另一种做法是将基类私有继承（private inheritance），这样基类所有成员在派生类中默认私有。

但需注意，虽然m_value在Derived中是private，在Base中仍然是public。因此通过转换为Base\&仍可绕过Derived的封装。

**高级内容**  
同理，若基类有public虚函数（virtual function），派生类将其访问说明符改为private后，仍可通过将Derived对象转换为Base\&来调用该虚函数。编译器允许此操作是因为函数在基类中是public。但由于对象实际是Derived类型，虚函数解析会调用（private的）派生类版本。访问控制在运行时不会生效。
```
#include <iostream>

class A
{
public:
    virtual void fun()
    {
        std::cout << "public A::fun()\n";
    }
};

class B : public A
{
private:
    virtual void fun()
    {
         std::cout << "private B::fun()\n";
   }
};

int main()
{
    B b {};
    b.fun();                  // 编译错误：B::fun()是private
    static_cast<A&>(b).fun(); // 正常：A::fun()是public，运行时解析到private的B::fun()

    return 0;
}
```

**重载函数的访问说明符修改**  
对于基类中的重载函数（overloaded function）集合，无法单独修改某个重载版本的访问说明符，必须全部修改：
```
#include <iostream>

class Base
{
public:
    int m_value{};

    int getValue() const { return m_value; }
    int getValue(int) const { return m_value; }
};

class Derived : public Base
{
private:
	using Base::getValue; // 将所有getValue函数设为private

public:
	Derived(int value) : Base { value }
	{
	}
};

int main()
{
	Derived derived{ 7 };
	std::cout << derived.getValue();  // 错误：getValue()在Derived中是private
	std::cout << derived.getValue(5); // 错误：getValue(int)在Derived中是private

	return 0;
}
```

**删除派生类中的函数**  
可以将派生类的成员函数标记为已删除（deleted），确保无法通过派生对象调用：
```
#include <iostream>
class Base
{
private:
	int m_value {};

public:
	Base(int value)
		: m_value { value }
	{
	}

	int getValue() const { return m_value; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base { value }
	{
	}


	int getValue() const = delete; // 标记此函数为不可访问
};

int main()
{
	Derived derived { 7 };

	// 下列调用失败，因为getValue()已被删除
	std::cout << derived.getValue();

	return 0;
}
```
注意基类版本的getValue()仍然可访问。有两种调用方式：
```
int main()
{
	Derived derived { 7 };

	// 直接调用Base::getValue()
	std::cout << derived.Base::getValue();

	// 将Derived向上转型为Base引用后调用
	std::cout << static_cast<Base&>(derived).getValue();

	return 0;
}
```
使用转型方法时，应转换为Base\&而非Base，以避免复制派生对象的基类部分。

[下一课 24.9 多重继承](Chapter-24/lesson24.9-multiple-inheritance.md)  
[返回主页](/)  
[上一课 24.7 调用继承函数与重写行为](Chapter-24/lesson24.7-calling-inherited-functions-and-overriding-behavior.md)