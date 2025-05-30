25.1 — 基类指针与派生类对象的引用  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月25日（首次发布于2008年1月29日）

在上一章中，您学习了如何使用继承从现有类派生新类。本章我们将重点讨论继承最重要且强大的特性之一 —— 虚函数（virtual functions）。

在深入探讨虚函数之前，让我们先了解其必要性。

在[派生类构造](113-order-of-construction-of-derived-classes/)章节中，您了解到派生类由多个部分组成：每个继承基类的部分和自身的特有部分。例如：

```cpp
#include <string_view>

class Base // 基类（base class）
{
protected:
    int m_value {};

public:
    Base(int value)
        : m_value{ value }
    {
    }

    std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};

class Derived: public Base // 派生类（derived class）
{
public:
    Derived(int value)
        : Base{ value }
    {
    }

    std::string_view getName() const { return "Derived"; }
    int getValueDoubled() const { return m_value * 2; }
};
```

当创建派生类对象时，包含基类部分（首先构造）和派生类部分（其次构造）。继承意味着派生类与基类存在"is-a"关系，因此派生类包含基类部分是合理的。

 
**指针、引用与派生类**  
很直观的是，我们可以为派生类对象设置派生类指针和引用：

```cpp
int main()
{
    Derived derived{ 5 };
    Derived& rDerived{ derived }; // 派生类引用（derived class reference）
    Derived* pDerived{ &derived }; // 派生类指针（derived class pointer）
}
```

但更值得探讨的是：C++是否允许基类指针或引用指向派生类对象？答案是肯定的：

```cpp
int main()
{
    Derived derived{ 5 };
    Base& rBase{ derived }; // 基类引用（base class reference）
    Base* pBase{ &derived }; // 基类指针（base class pointer）
}
```

由于rBase和pBase是基类引用/指针，它们只能访问基类成员。即使派生类中的getName()隐藏（shadow）了基类版本，基类指针/引用仍然调用基类版本的getName()。

以下更复杂的示例说明了这个问题：

```cpp
class Animal // 动物基类（base class）
{
protected:
    std::string m_name;

    Animal(std::string_view name) : m_name{ name } {}
    
public:
    std::string_view getName() const { return m_name; }
    std::string_view speak() const { return "???"; }
};

class Cat: public Animal // 猫派生类（derived class）
{
public:
    Cat(std::string_view name) : Animal{ name } {}
    std::string_view speak() const { return "Meow"; }
};

class Dog: public Animal // 狗派生类（derived class）
{
public:
    Dog(std::string_view name) : Animal{ name } {}
    std::string_view speak() const { return "Woof"; }
};

int main()
{
    const Cat cat{ "Fred" };
    const Dog dog{ "Garbo" };
    const Animal* pAnimal{ &cat };
    pAnimal = &dog;
}
```

由于pAnimal是动物指针，`pAnimal->speak()`始终调用Animal::speak()而非派生类版本。

**基类指针/引用的应用场景**  
1. **通用函数编写**：避免为每个派生类编写重复函数
2. **异构对象存储**：使用基类指针数组存储不同派生类对象

例如存储多类型动物的数组：

```cpp
const auto animals{ std::to_array<const Animal*>({&cat, &dog}) };
for (auto animal : animals) {
    std::cout << animal->speak(); // 输出"???"而非实际动物叫声
}
```

当前方案的局限在于基类指针只能调用基类方法。这正是虚函数要解决的问题。

**测验答案**  
1. 通过基类添加m_speak成员的解决方案虽然可行，但存在以下问题：
   - 基类会随差异化需求膨胀
   - 初始化时确定的成员无法支持运行时动态行为
   - 无法实现派生类特有逻辑

[下一课 25.2 虚函数与多态](Chapter-25/lesson25.2-virtual-functions.md)  
[返回主页](/)  
[上一课 24.x 第24章总结与测验](Chapter-24/lesson24.x-chapter-24-summary-and-quiz.md)