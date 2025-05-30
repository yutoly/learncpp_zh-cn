25.3 — override与final说明符，及协变返回类型  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月29日（首次发布于2016年11月6日）  

为应对继承机制中的常见挑战，C\+\+提供了两个与继承相关的标识符：`override`和`final`。需注意这些标识符并非关键字——它们是仅在特定上下文中具有特殊含义的普通单词。C\+\+标准称其为"具有特殊含义的标识符"，但通常被称作"说明符（specifiers）"。尽管final使用频率不高，但override是应频繁使用的优秀特性。本章将详解两者用法，并探讨虚函数覆盖中返回类型匹配规则的例外情况。  

override说明符  
----------------  

如前章所述，派生类的虚函数仅在签名与返回类型完全匹配时才会被视为覆盖。这可能导致无意中产生错误，即本应覆盖的函数实际未实现覆盖。  

考虑以下示例：  
```cpp
#include <iostream>
#include <string_view>

class A
{
public:
	virtual std::string_view getName1(int x) { return "A"; }
	virtual std::string_view getName2(int x) { return "A"; }
};

class B : public A
{
public:
	virtual std::string_view getName1(short x) { return "B"; } // 注意：参数为short类型
	virtual std::string_view getName2(int x) const { return "B"; } // 注意：函数为const限定
};

int main()
{
	B b{};
	A& rBase{ b };
	std::cout << rBase.getName1(1) << '\n';
	std::cout << rBase.getName2(2) << '\n';

	return 0;
}
```  

由于rBase是B对象的A类引用，此处意图是通过虚函数调用B::getName1()和B::getName2()。但由于B::getName1()参数类型不同（short而非int），不被视为对A::getName1()的覆盖。更隐蔽的是，B::getName2()为const限定而A::getName2()未限定，故B::getName2()也不被视为覆盖。  

程序输出结果为：  
```
A
A
```  

在此特定案例中，因A、B类仅打印名称，较易发现覆盖错误。但在复杂程序中，若函数行为或返回值未被显式输出，此类问题将难以调试。  

为解决意图覆盖但实际未覆盖的问题，`override`说明符可应用于任何虚函数，指示编译器强制检查该函数是否为有效覆盖。`override`说明符置于成员函数声明末尾（与函数级`const`位置相同）。若成员函数同时为`const`和`override`，`const`必须置于`override`之前。  

若标记为`override`的函数未覆盖基类函数（或应用于非虚函数），编译器将报错：  
```cpp
#include <string_view>

class A
{
public:
	virtual std::string_view getName1(int x) { return "A"; }
	virtual std::string_view getName2(int x) { return "A"; }
	virtual std::string_view getName3(int x) { return "A"; }
};

class B : public A
{
public:
	std::string_view getName1(short int x) override { return "B"; } // 编译错误：非覆盖函数
	std::string_view getName2(int x) const override { return "B"; } // 编译错误：非覆盖函数
	std::string_view getName3(int x) override { return "B"; } // 正确：覆盖A::getName3(int)
};

int main()
{
	return 0;
}
```  

上述程序产生两个编译错误：B::getName1()与B::getName2()均未覆盖基类函数。B::getName3()正确覆盖A::getName3()，故无错误。  

由于使用override说明符无性能损耗且能确保覆盖正确性，所有虚覆盖函数均应使用该说明符。此外，因override说明符隐含virtual特性，无需在override函数中重复使用virtual关键字。  

> **最佳实践**  
> 基类虚函数使用virtual关键字  
> 派生类覆盖函数使用override说明符（不含virtual关键字），包括虚析构函数  

> **规则**  
> 若成员函数同时为`const`和`override`，必须按`const override`顺序声明，`override const`为错误形式。  

final说明符  
----------------  

当需要禁止他人覆盖虚函数或继承类时，可使用`final`说明符强制实施限制。若用户尝试覆盖标记为final的函数或继承final类，编译器将报错。  

禁止函数覆盖时，final说明符用法与override相同：  
```cpp
#include <string_view>

class A
{
public:
	virtual std::string_view getName() const { return "A"; }
};

class B : public A
{
public:
	// 下行的final说明符使此函数无法在派生类中被覆盖
	std::string_view getName() const override final { return "B"; } // 正确：覆盖A::getName()
};

class C : public B
{
public:
	std::string_view getName() const override { return "C"; } // 编译错误：尝试覆盖B::getName()（已标记为final）
};
```  

上述代码中，B::getName()正确覆盖A::getName()。但B::getName()含final说明符，意味着任何进一步覆盖均视为错误。C::getName()尝试覆盖B::getName()将导致编译错误。  

禁止类继承时，final说明符置于类名之后：  
```cpp
#include <string_view>

class A
{
public:
	virtual std::string_view getName() const { return "A"; }
};

class B final : public A // 注意此处的final说明符
{
public:
	std::string_view getName() const override { return "B"; }
};

class C : public B // 编译错误：无法继承final类
{
public:
	std::string_view getName() const override { return "C"; }
};
```  

上述示例中，类B声明为final。当C尝试继承B时，编译器报错。  

协变返回类型（covariant return types）  
----------------  

在特定情况下，派生类虚函数覆盖可拥有与基类不同的返回类型仍被视为有效覆盖。当虚函数返回类型为某类的指针或引用时，覆盖函数可返回派生类的指针或引用，此称为**协变返回类型**。示例如下：  
```cpp
#include <iostream>
#include <string_view>

class Base
{
public:
	// 此版本getThis()返回Base类指针
	virtual Base* getThis() { std::cout << "调用Base::getThis()\n"; return this; }
	void printType() { std::cout << "返回Base类型\n"; }
};

class Derived : public Base
{
public:
	// 通常覆盖函数要求返回类型相同
	// 因Derived继承自Base，返回Derived*替代Base*是允许的
	Derived* getThis() override { std::cout << "调用Derived::getThis()\n";  return this; }
	void printType() { std::cout << "返回Derived类型\n"; }
};

int main()
{
	Derived d{};
	Base* b{ &d };
	d.getThis()->printType(); // 调用Derived::getThis()，返回Derived*，调用Derived::printType
	b->getThis()->printType(); // 调用Derived::getThis()，返回Base*，调用Base::printType

	return 0;
}
```  

输出结果：  
```
调用Derived::getThis()
返回Derived类型
调用Derived::getThis()
返回Base类型
```  

关于协变返回类型的重要说明：C\+\+无法动态选择类型，因此返回类型始终与所调用函数的实际版本匹配。  

首例调用d.getThis()时，d为Derived类型，故调用Derived::getThis()，返回`Derived*`，进而调用非虚函数Derived::printType()。  

第二例调用b->getThis()时，b为指向Derived对象的Base指针。Base::getThis()是虚函数，故调用Derived::getThis()。虽然Derived::getThis()返回`Derived*`，但基类版本返回`Base*`，故返回的Derived\*被向上转型为`Base*`。由于Base::printType()非虚，故调用Base版本。  

若printType()为虚函数，则b->getThis()返回的`Base*`将触发虚函数解析，调用Derived::printType()。  

协变返回类型常见于虚成员函数返回包含该成员的类指针或引用的情况（如Base::getThis()返回`Base*`，Derived::getThis()返回`Derived*`）。但协变返回类型适用于任何覆盖成员函数返回类型继承自基类虚成员函数返回类型的情况。  

测验时间  
----------------  

**问题1**  
以下程序输出结果是什么？  
```cpp
#include <iostream>

class A
{
public:
    void print() { std::cout << "A"; }
    virtual void vprint() { std::cout << "A"; }
};
class B : public A
{
public:
    void print() { std::cout << "B"; }
    void vprint() override { std::cout << "B"; }
};

class C
{
private:
    A m_a{};
public:
    virtual A& get() { return m_a; }
};

class D : public C
{
private:
    B m_b{};
public:
    B& get() override { return m_b; } // 协变返回类型
};

int main()
{
    // 案例1
    D d{};
    d.get().print();
    d.get().vprint();
    std::cout << '\n';
 
    // 案例2
    C c{};
    c.get().print();
    c.get().vprint();
    std::cout << '\n';

    // 案例3
    C& ref{ d };
    ref.get().print();
    ref.get().vprint();
    std::cout << '\n';

    return 0;
}
```  
<details><summary>答案</summary>  
```
BB
AA
AB
```  
解析：  
- 案例1：调用D::get()返回B&，调用B版本函数  
- 案例2：调用C::get()返回A&，调用A版本函数  
- 案例3：虚解析调用D::get()返回A&（实际引用B对象），非虚调用A::print()，虚调用B::vprint()  
</details>  

**问题2**  
函数重载（overloading）与覆盖（overriding）的应用场景有何区别？  
<details><summary>答案</summary>  
- 函数重载：需根据参数类型改变函数行为  
- 函数覆盖：需根据隐式对象类型（派生类）改变成员函数行为  
</details>  

[下一课 25.4 — 虚析构函数、虚赋值与覆盖虚拟化](Chapter-25/lesson25.4-virtual-destructors-virtual-assignment-and-overriding-virtualization.md)  
[返回主页](/)  
[上一课 25.2 — 虚函数与多态](Chapter-25/lesson25.2-virtual-functions.md)