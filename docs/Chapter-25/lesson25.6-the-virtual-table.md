25.6 — 虚表  
=========================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年2月8日 下午3:29（PST）  
2024年12月7日更新  

考虑以下程序：  
```cpp
#include <iostream>
#include <string_view>

class Base
{
public:
    std::string_view getName() const { return "Base"; }                // 非虚函数
    virtual std::string_view getNameVirtual() const { return "Base"; } // 虚函数
};

class Derived: public Base
{
public:
    std::string_view getName() const { return "Derived"; }
    virtual std::string_view getNameVirtual() const override { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& base { derived };

    std::cout << "base的静态类型是 " << base.getName() << '\n';
    std::cout << "base的动态类型是 " << base.getNameVirtual() << '\n';

    return 0;
}
```  

首先看`base.getName()`的调用。由于这是非虚函数，编译器可以使用`base`的实际类型（`Base`）在编译时确定应解析为`Base::getName()`。  

虽然看起来几乎相同，但`base.getNameVirtual()`的调用解析方式不同。由于这是虚函数调用，编译器必须使用`base`的动态类型来解析调用，而动态类型直到运行时才能确定。因此，只有运行时才能确定`base.getNameVirtual()`解析为`Derived::getNameVirtual()`而非`Base::getNameVirtual()`。  

虚函数如何实际运作？  

虚表（Virtual Table）  
----------------  

C++标准未规定虚函数的具体实现方式（此细节由实现决定）。但C++实现通常使用称为虚表（virtual table）的后期绑定形式实现虚函数。  

**虚表（virtual table）**是用于动态/后期绑定方式解析函数调用的查找表。虚表有时也被称作"vtable"、"虚函数表（virtual function table）"、"虚方法表（virtual method table）"或"派发表（dispatch table）"。在C++中，虚函数解析有时被称为**动态派发（dynamic dispatch）**。  

术语对照：  
- 早期绑定/静态派发（early binding/static dispatch）= 直接函数调用重载解析  
- 后期绑定（late binding）= 间接函数调用解析  
- 动态派发（dynamic dispatch）= 虚函数覆盖解析  

由于理解虚表工作原理并非使用虚函数的必要条件，本节可作为选读内容。  

虚表实际上相当简单，但用文字描述稍显复杂。首先，每个使用虚函数的类（或继承自使用虚函数的类）都有对应的虚表。该表是编译器在编译时建立的静态数组，虚表为类对象可调用的每个虚函数包含一个条目。每个条目是函数指针，指向该类可访问的最派生函数。  

其次，编译器还添加一个隐藏指针作为基类的成员，我们称其为`*__vptr`。当类对象创建时，`*__vptr`自动指向该类的虚表。与作为编译器用于解析自引用的函数参数`this`指针不同，`*__vptr`是真实的指针成员。这使得每个类对象的内存占用增加一个指针大小，同时也意味着`*__vptr`会被派生类继承（这点很重要）。  

现在通过简单示例理解这些机制：  
```cpp
class Base
{
public:
    virtual void function1() {};
    virtual void function2() {};
};

class D1: public Base
{
public:
    void function1() override {};
};

class D2: public Base
{
public:
    void function2() override {};
};
```  

由于有3个类，编译器将建立3个虚表：Base、D1和D2各一个。编译器还会向最顶层使用虚函数的基类添加隐藏指针成员。虽然这是自动完成的，我们在下例中显式展示其位置：  
```cpp
class Base
{
public:
    VirtualTable* __vptr;
    virtual void function1() {};
    virtual void function2() {};
};

class D1: public Base
{
public:
    void function1() override {};
};

class D2: public Base
{
public:
    void function2() override {};
};
```  

当类对象创建时，`*__vptr`被设置为指向该类的虚表。例如：  
- Base类型对象创建时，`*__vptr`指向Base的虚表  
- D1或D2对象创建时，`*__vptr`分别指向D1或D2的虚表  

现在讨论虚表填充规则。由于示例中有两个虚函数，每个虚表将包含两个条目（分别对应function1()和function2()）。记住当虚表被填充时，每个条目都指向该类对象可调用的最派生函数。  

- Base对象的虚表：条目指向Base::function1()和Base::function2()  
- D1的虚表：function1条目指向D1::function1()（覆盖基类），function2条目指向Base::function2()  
- D2的虚表：function1条目指向Base::function1()，function2条目指向D2::function2()  

图示如下：  
![](https://www.learncpp.com/images/CppTutorial/Section12/VTable.gif)  

每个类的`*__vptr`指向该类的虚表，虚表条目指向该类对象允许调用的最派生版本函数。  

考虑创建D1对象时：  
```cpp
int main()
{
    D1 d1 {};
}
```  
d1的`*__vptr`指向D1的虚表。  

当基类指针指向D1时：  
```cpp
int main()
{
    D1 d1 {};
    Base* dPtr = &d1;
    return 0;
}
```  
尽管dPtr是基类指针，但通过`*__vptr`（位于基类部分）仍可访问D1的虚表。  

调用`dPtr->function1()`时：  
1. 识别function1()是虚函数  
2. 通过`dPtr->__vptr`访问D1的虚表  
3. 查表确定调用D1::function1()  

若指针指向Base对象：  
```cpp
int main()
{
    Base b {};
    Base* bPtr = &b;
    bPtr->function1();
    return 0;
}
```  
此时`*__vptr`指向Base的虚表，条目指向Base::function1()。  

调用虚函数比非虚函数慢的原因：  
1. 需要通过`*__vptr`访问虚表  
2. 需索引虚表查找正确函数  
3. 才能调用函数  

现代计算机中这种开销通常微不足道。此外，使用虚函数的类每个对象都会增加一个指针大小的内存占用。  

[下一课 25.7 — 纯虚函数、抽象基类与接口类](Chapter-25/lesson25.7-pure-virtual-functions-abstract-base-classes-and-interface-classes.md)  
[返回主页](/)    
[上一课 25.5 — 早期绑定与后期绑定](Chapter-25/lesson25.5-early-binding-and-late-binding.md)