25.x — 第25章总结与测验  
===================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2016年11月23日，下午2:59（PST）  
2025年2月19日  

我们关于C++继承（inheritance）与虚函数（virtual functions）的探索之旅就此告一段落。但无需伤感，亲爱的读者，C++仍有诸多领域等待我们发掘。  

**本章要点**  

C++允许将基类指针（base class pointer）和引用指向派生类对象（derived object）。这在需要编写能处理所有基类派生对象的函数或数组时非常有用。  

若未使用虚函数，指向派生类的基类指针/引用只能访问基类成员变量和基础版本函数。  

虚函数（virtual function）是一种特殊函数，能解析到基类与派生类之间最派生版本（称为覆盖override）。要成为有效覆盖，派生类函数必须与虚基类函数具有相同签名和返回类型。唯一例外是协变返回类型（covariant return type），允许覆盖函数返回派生类指针/引用（当基类函数返回基类指针/引用时）。  

建议为覆盖函数添加override说明符（override specifier）以确保其确实是有效覆盖。  

final说明符（final specifier）可用于防止函数被覆盖或类被继承。  

若使用继承，应将析构函数设为虚函数（virtual destructor），确保通过基类指针删除对象时正确调用析构函数。  

可通过作用域解析运算符（scope resolution operator）直接指定要调用的函数版本，例如`base.Base::getName()`。  

早绑定（early binding）发生在编译器遇到直接函数调用时，编译器/链接器可直接解析这些调用。晚绑定（late binding）发生在通过函数指针调用时，具体调用函数需到运行时才能确定。虚函数使用晚绑定和虚表（virtual table）确定调用版本。  

使用虚函数存在开销：调用耗时更长，且虚表使每个含虚函数的对象增加一个指针大小。  

可通过在虚函数原型末尾添加"= 0"来定义纯虚函数（pure virtual function）/抽象函数（abstract function）。含纯虚函数的类称为抽象类（abstract class），不可实例化。继承纯虚函数的类必须具体定义这些函数，否则仍被视为抽象类。纯虚函数可拥有函数体，但类仍被视为抽象类。  

接口类（interface class）是无成员变量且所有函数都是纯虚函数的类，通常以大写I开头命名。  

虚基类（virtual base class）是被对象多次继承时仅包含一次的基类。  

当派生类赋值给基类对象时，基类仅复制派生类中的基类部分，这称为对象切片（object slicing）。  

动态转型（dynamic casting）可将基类对象指针转换为派生类对象指针，这称为向下转型（downcasting）。转换失败时返回空指针。  

为继承类重载operator<<的最简方法是为基础类编写重载版本，并调用虚成员函数完成输出。  

**测验题目**  

1. 以下程序均存在缺陷，请通过视觉检查（不编译）指出问题。每个程序的预期输出应为"Derived"。  

1a)  
```cpp
#include <iostream>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{ value }
	{
	}

	const char* getName() const { return "Base"; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base{ value }
	{
	}

	const char* getName() const { return "Derived"; }
};
// ...（其余代码省略）
```  
  
<details><summary>答案</summary>Base::getName()未声明为虚函数，b.getName()无法解析到Derived::getName()。</details>  

1b)  
```cpp
// ...（代码结构类似，差异在函数const属性）
```  
<details><summary>答案</summary>Base::getName()非const而Derived::getName()是const，不构成覆盖。</details>  

1c)  
<details><summary>答案</summary>通过值赋值导致对象切片。</details>  

1d)  
<details><summary>答案</summary>Base被声明为final，阻止Derived继承。</details>  

1e)  
<details><summary>答案</summary>Derived::getName()是纯虚函数，导致类无法实例化。</details>  

1f)  
<details><summary>答案</summary>未使用虚析构函数导致内存泄漏。</details>  

2a) 创建名为Shape的抽象类  
```cpp
class Shape
{
public:
	virtual std::ostream& print(std::ostream& out) const = 0;
	friend std::ostream& operator<<(std::ostream& out, const Shape& p)
	{
		return p.print(out);
	}
	virtual ~Shape() = default;
};
```  

2b) 派生Circle和Triangle类  
```cpp
// ...（完整实现代码）
```  

2c) 完成给定程序  
```cpp
// ...（包含动态转型和半径获取的实现）
```  

2d) 附加题：使用std::unique_ptr  
```cpp
// ...（智能指针版本实现）
```  

[下一课 26.1 模板类](Chapter-26/lesson26.1-template-classes.md)  
[返回主页](/)  
[上一课 25.11 使用operator<<打印继承类](Chapter-25/lesson25.11-printing-inherited-classes-using-operator.md)