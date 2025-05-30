25.10 — 动态转换（dynamic_cast）  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月29日（首次发布于2016年11月22日）  

 

在课程[10.6 — 显式类型转换（强制转换）与static_cast](Chapter-10/lesson10.6-explicit-type-conversion-casting-and-static-cast.md)中，我们探讨了强制转换的概念以及使用static_cast进行类型转换的方法。本章将介绍另一种类型转换运算符：动态转换（dynamic_cast）。

**动态转换的必要性**  
处理多态时，常会遇到需要访问派生类特有成员的情况。考虑以下示例程序：

```cpp
#include <iostream>
#include <string>
#include <string_view>

class Base
{
protected:
    int m_value{};

public:
    Base(int value) : m_value{value} {}
    virtual ~Base() = default;
};

class Derived : public Base
{
protected:
    std::string m_name{};

public:
    Derived(int value, std::string_view name)
        : Base{value}, m_name{name} {}
    
    const std::string& getName() const { return m_name; }
};

Base* getObject(bool returnDerived)
{
    return returnDerived ? new Derived{1, "Apple"} : new Base{2};
}

int main()
{
    Base* b{ getObject(true) };
    // 如何通过Base指针访问Derived::getName()？
    delete b;
    return 0;
}
```

当Base指针实际指向派生类对象时，如何调用Derived::getName()？

**动态转换（dynamic_cast）**  
C++提供的**动态转换（dynamic_cast）**运算符可用于将基类指针转换为派生类指针，这一过程称为**向下转型（downcasting）**。示例：

```cpp
int main()
{
    Base* b{ getObject(true) };
    Derived* d{ dynamic_cast<Derived*>(b) }; // 将Base指针转换为Derived指针
    std::cout << "派生类名称：" << d->getName() << '\n';
    delete b;
    return 0;
}
```

**转换失败处理**  
若转换失败（如基类指针未指向派生类对象），dynamic_cast将返回空指针：

```cpp
int main()
{
    Base* b{ getObject(false) }; // 返回Base对象
    Derived* d{ dynamic_cast<Derived*>(b) };
    if (d) // 检查空指针
        std::cout << d->getName() << '\n';
    delete b;
    return 0;
}
```


规则  
----------------  
必须通过检查空指针结果确保动态转换成功。


**使用static_cast进行向下转型**  
static_cast也可用于向下转型，但不会进行运行时检查：

```cpp
Derived* d{ static_cast<Derived*>(b) }; // 危险：若b未指向Derived对象将导致未定义行为
```

**动态转换与引用**  
动态转换也可用于引用类型，失败时抛出std::bad_cast异常：

```cpp
Derived apple{1, "Apple"};
Base& b{ apple };
try {
    Derived& d{ dynamic_cast<Derived&>(b) };
    std::cout << d.getName() << '\n';
} catch (const std::bad_cast& e) {
    // 处理异常
}
```

**动态转换与静态转换的选择**  
- 优先使用虚函数实现多态
- 在以下情况考虑向下转型：
    1. 无法修改基类添加虚函数（如标准库类）
    2. 需要访问派生类特有成员
    3. 基类不适合实现虚函数

**运行时类型信息（RTTI）警告**  
动态转换依赖运行时类型信息，某些编译器允许关闭RTTI优化（此时dynamic_cast不可用）。


[下一课 25.11 — 使用operator<<打印继承类](Chapter-25/lesson25.11-printing-inherited-classes-using-operator.md)  
[返回主页](/)  
[上一课 25.9 — 对象切片](Chapter-25/lesson25.9-object-slicing.md)