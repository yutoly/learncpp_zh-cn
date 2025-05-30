25.2 — 虚函数与多态  
==========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年1月30日 15:46（PST）  
2024年12月11日修订  

在上一课[指向派生类对象的基类指针与引用](121-pointers-and-references-to-the-base-class-of-derived-objects/)中，我们考察了多个使用基类指针或引用简化代码的案例。然而所有案例都存在一个问题：基类指针或引用只能调用基类版本的函数，无法调用派生类版本。以下是一个简单示例：  
```cpp
#include <iostream>
#include <string_view>

class Base
{
public:
    std::string_view getName() const { return "Base"; }
};

class Derived: public Base
{
public:
    std::string_view getName() const { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& rBase{ derived };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
```
输出结果：  
```
rBase is a Base
```  
由于rBase是Base引用，即使实际指向Derived对象，仍调用Base::getName()。本课将介绍如何使用虚函数（virtual functions）解决此问题。  

虚函数（Virtual functions）  
----------------  

**虚函数（virtual function）**是一种特殊成员函数，当被调用时会根据实际对象的类型解析到继承链中最派生的函数版本。派生函数若与基类函数具有相同签名（函数名、参数类型、const属性）和返回类型，则视为匹配的**覆盖（override）**。  

通过在函数声明前添加`virtual`关键字可定义虚函数。修改后的示例：  
```cpp
#include <iostream>
#include <string_view>

class Base
{
public:
    virtual std::string_view getName() const { return "Base"; } // 注意添加了virtual关键字
};

class Derived: public Base
{
public:
    virtual std::string_view getName() const { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& rBase{ derived };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
```
输出结果：  
```
rBase is a Derived
```  
> **提示**  
> 部分现代编译器可能提示"具有虚函数但无虚析构函数"的错误。若出现此提示，请在基类添加虚析构函数：  
> ```cpp
>    virtual ~Base() = default;
> ```  
> 虚析构函数将在[25.4 — 虚析构函数、虚赋值与覆盖虚化](Chapter-25/lesson25.4-virtual-destructors-virtual-assignment-and-overriding-virtualization.md)讨论。  

由于rBase引用的是Derived对象中的Base部分，当调用`rBase.getName()`时，虽然表面调用Base::getName()，但虚函数机制会查找Derived对象中最派生的版本，最终解析到Derived::getName()。  

考察更复杂的示例：  
```cpp
#include <iostream>
#include <string_view>

class A
{
public:
    virtual std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    virtual std::string_view getName() const { return "B"; }
};

class C: public B
{
public:
    virtual std::string_view getName() const { return "C"; }
};

class D: public C
{
public:
    virtual std::string_view getName() const { return "D"; }
};

int main()
{
    C c {};
    A& rBase{ c };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
```  
输出结果为：  
```
rBase is a C
```  
虚函数解析机制仅在通过指针或引用调用时生效。直接通过对象调用虚函数将始终调用该对象类型的版本：  
```cpp
C c{};
std::cout << c.getName(); // 始终调用C::getName

A a { c }; // 将c的A部分拷贝到a（不建议这样做）
std::cout << a.getName(); // 始终调用A::getName
```  
> **关键洞察**  
> 虚函数解析仅在使用指针或引用调用成员函数时生效。  

多态（Polymorphism）  
----------------  

**多态（polymorphism）**指实体具有多种形态的能力。例如：  
```cpp
int add(int, int);
double add(double, double);
```  
`add`标识符有两种形态：整型和双精度浮点型版本。  

* **编译时多态（Compile-time polymorphism）**：由编译器解析的多态形式，包括函数重载和模板解析。  
* **运行时多态（Runtime polymorphism）**：在运行时解析的多态形式，即虚函数解析。  

复杂示例：动物类层次结构  
----------------  
修改后的Animal示例（speak()声明为虚函数）：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    Animal(std::string_view name) : m_name{ name } {} // 受保护构造函数

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; } // 虚函数
};

class Cat: public Animal
{
public:
    Cat(std::string_view name) : Animal{ name } {}
    virtual std::string_view speak() const { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name) : Animal{ name } {}
    virtual std::string_view speak() const { return "Woof"; }
};

void report(const Animal& animal)
{
    std::cout << animal.getName() << " says " << animal.speak() << '\n';
}

int main()
{
    Cat cat{ "Fred" };
    Dog dog{ "Garbo" };

    report(cat);
    report(dog);

    return 0;
}
```  
输出：  
```
Fred says Meow  
Garbo says Woof  
```  
当`animal.speak()`被调用时，虚函数机制会根据实际对象类型解析到Cat::speak()或Dog::speak()。  

数组示例同样适用：  
```cpp
Cat fred{ "Fred" };
Dog garbo{ "Garbo" };
/*...其他对象...*/

Animal* animals[]{ &fred, &garbo, /*...*/ };

for (const auto* animal : animals)
    std::cout << animal->getName() << " says " << animal->speak() << '\n';
```  
输出各对象对应的叫声。虚函数的最大优势在于：新派生类无需修改现有代码即可兼容。  

注意事项：  
1. 派生类函数签名必须与基类虚函数**完全一致**，否则无法正确覆盖  
2. 基类虚函数的所有派生覆盖默认具有虚属性，无需显式声明`virtual`  
3. 虚函数返回类型通常必须匹配（协变返回类型除外）  

> **最佳实践**  
> 不要在构造函数或析构函数中调用虚函数。因为：  
> - 构造派生类时先构造基类部分，此时派生部分尚未初始化  
> - 析构时派生部分已销毁，虚函数解析回退到基类版本  

虚函数的代价  
----------------  
虚函数的缺点包括：  
1. 调用虚函数比普通函数稍慢（需通过虚函数表查找）  
2. 每个含虚函数的类对象需额外存储虚表指针，增加内存开销  

测验解析  
----------------  
**问题1a**  
```cpp
class C: public B { /* 无getName() */ };
class D: public C { /* 实现getName() */ };

C c {};
A& rBase{ c };
rBase.getName(); // 解析B::getName()
```  
答案：B（继承链中最近的覆盖版本是B）  

**问题1b**  
```cpp
C c;
B& rBase{ c };
rBase.getName(); // 解析C::getName()
```  
答案：C  

**问题1c**  
基类函数非虚时，始终调用基类版本  
答案：A  

**问题1d**  
虚属性在继承链中隐式传递  
答案：C  

**问题1e**  
常量性不匹配导致未正确覆盖  
答案：A  

**问题1f**  
构造函数中调用虚函数解析到基类版本  
答案：A  

[下一课 25.3 — override与final说明符，协变返回类型](Chapter-25/lesson25.3-the-override-and-final-specifiers-and-covariant-return-types.md)  
[返回主页](/)  
[上一课 25.1 — 指向派生类对象的基类指针与引用](Chapter-25/lesson25.1-pointers-and-references-to-the-base-class-of-derived-objects.md)