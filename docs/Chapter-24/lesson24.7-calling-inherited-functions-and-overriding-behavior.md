24.7 — 调用继承函数与重写行为  
===========================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2017年6月27日 PDT下午4:28  
2024年6月9日更新  

默认情况下，派生类（derived class）会继承基类（base class）中定义的所有行为。本节我们将深入探讨成员函数的选择机制，以及如何通过派生类修改基类行为。  

当在派生类对象上调用成员函数时，编译器首先检查派生类中是否存在同名函数。如果存在，所有该名称的重载函数（overloaded functions）都会被考虑，并通过函数重载解析（function overload resolution）确定最佳匹配。若不存在，编译器将沿继承链向上查找，依次检查每个父类。  

简而言之，编译器会从具有至少一个同名函数的最深层派生类中选择最佳匹配函数。  

调用基类函数  
----------------  

首先考察派生类无匹配函数而基类存在的情况：  

```cpp
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
```  

输出：  
```
Base::identify()
Base::identify()
```  

调用`base.identify()`时，编译器查找`Base`类中定义的`identify()`函数并匹配成功。  

调用`derived.identify()`时，由于`Derived`类未定义该函数，编译器转向基类`Base`查找，发现匹配函数后调用。这意味着当基类行为满足需求时，可直接使用其功能。  

重定义行为  
----------------  

若在派生类中定义`Derived::identify()`，将覆盖基类行为：  

```cpp
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const { std::cout << "Derived::identify()\n"; }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
```  

输出：  
```
Base::identify()
Derived::identify()
```  

注意：  
- 派生类函数不会继承基类同名函数的访问限定符（access specifier）  
- 基类私有函数可在派生类中重定义为公有，反之亦然  

```cpp
#include <iostream>

class Base
{
private:
	void print() const 
	{
		std::cout << "Base";
	}
};
 
class Derived : public Base
{
public:
	void print() const 
	{
		std::cout << "Derived ";
	}
};
 
 
int main()
{
	Derived derived {};
	derived.print(); // 调用派生类公有print()
	return 0;
}
```  

扩展现有功能  
----------------  

若需在派生类函数中调用基类函数并扩展功能，可使用基类作用域限定符（scope qualifier）：  

```cpp
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const
    {
        std::cout << "Derived::identify()\n";
        Base::identify(); // 显式调用基类函数
    }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
```  

输出：  
```
Base::identify()
Derived::identify()
Base::identify()
```  

若省略作用域限定符会导致无限递归：  

```cpp
void identify() const
{
    std::cout << "Derived::identify()\n";
    identify(); // 错误：无限递归调用自身
}
```  

友元函数处理  
----------------  

调用基类友元函数（friend function）时需使用静态转换（static_cast）：  

```cpp
#include <iostream>

class Base
{
public:
    Base() { }

	friend std::ostream& operator<< (std::ostream& out, const Base&)
	{
		out << "In Base\n";
		return out;
	}
};

class Derived: public Base
{
public:
    Derived() { }

 	friend std::ostream& operator<< (std::ostream& out, const Derived& d)
	{
		out << "In Derived\n";
		out << static_cast<const Base&>(d); // 转换为基类引用
		return out;
    }
};

int main()
{
    Derived derived {};
    std::cout << derived << '\n'; // 输出两行
    return 0;
}
```  

输出：  
```
In Derived
In Base
```  

派生类中的重载解析  
----------------  

当派生类存在同名函数时，基类重载函数将被隐藏：  

```cpp
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
    void print(double) { std::cout << "Derived::print(double)"; }
};

int main()
{
    Derived d{};
    d.print(5); // 调用Derived::print(double)
    return 0;
}
```  

若要保留基类重载，可使用using声明（using-declaration）：  

```cpp
class Derived: public Base
{
public:
    using Base::print; // 暴露基类所有print重载
    void print(double) { std::cout << "Derived::print(double)"; }
};
```  

此时`d.print(5)`将调用`Base::print(int)`，因其参数匹配更优。  

[下一课 24.8 隐藏继承功能](Chapter-24/lesson24.8-hiding-inherited-functionality.md)  
[返回主页](/)  
[上一课 24.6 为派生类添加新功能](Chapter-24/lesson24.6-adding-new-functionality-to-a-derived-class.md)