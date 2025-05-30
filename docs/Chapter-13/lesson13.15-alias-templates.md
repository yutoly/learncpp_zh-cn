13.15 — 别名模板（alias templates）  
========================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月27日，上午10:20（首次发布于2024年6月11日）  

在课程[10.7 — 类型定义与类型别名](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)中，我们讨论了类型别名如何为现有类型创建别名。


当所有模板参数都明确指定时，为类模板创建类型别名的工作方式与普通类型别名相同：

```cpp
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
void print(const Pair<T>& p)
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    using Point = Pair<int>; // 创建普通类型别名
    Point p { 1, 2 };        // 编译器将其替换为 Pair<int>

    print(p);

    return 0;
}
```

此类别名可在局部（如函数内部）或全局作用域中定义。


别名模板（alias templates）  
----------------

在其他情况下，我们可能需要为模板类定义一个类型别名，其中并非所有模板参数都在别名中指定（而由类型别名使用者提供）。为此，我们可以定义**别名模板（alias template）**——即用于实例化类型别名的模板。如同类型别名不定义新类型，别名模板也不定义新类型。


以下示例演示其工作原理：

```cpp
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// 定义别名模板
// 别名模板必须在全局作用域中定义
template <typename T>
using Coord = Pair<T>; // Coord 是 Pair<T> 的别名

// 函数模板需要知道 Coord 的模板参数 T 是类型模板参数
template <typename T>
void print(const Coord<T>& c)
{
    std::cout << c.first << ' ' << c.second << '\n';
}

int main()
{
    Coord<int> p1 { 1, 2 }; // C++20之前：必须显式指定类型模板参数
    Coord p2 { 1, 2 };      // C++20起，当CTAD可用时可使用别名模板推导模板参数

    std::cout << p1.first << ' ' << p1.second << '\n';
    print(p2);

    return 0;
}
```

本例中，我们将别名模板`Coord`定义为`Pair<T>`的别名，其中类型模板参数`T`由`Coord`的使用者指定。`Coord`是别名模板，`Coord<T>`是`Pair<T>`的实例化类型别名。定义后，我们可以在原使用`Pair`的地方使用`Coord`，在原使用`Pair<T>`的地方使用`Coord<T>`。


此示例有几个注意要点：


首先，与普通类型别名（可在代码块内定义）不同，别名模板（alias template）必须在全局作用域中定义（所有模板均需如此）。


其次，C++20之前，使用别名模板实例化对象时必须显式指定模板参数。C++20起，可使用**别名模板推导（alias template deduction）**，当别名类型适用CTAD时从初始化器推导模板参数类型。


第三，由于CTAD不适用于函数参数，当使用别名模板作为函数参数时，必须显式指定别名模板使用的模板参数。即必须写作：

```cpp
template <typename T>
void print(const Coord<T>& c)
{
    std::cout << c.first << ' ' << c.second << '\n';
}
```

而非：

```cpp
void print(const Coord& c) // 错误：缺少模板参数
{
    std::cout << c.first << ' ' << c.second << '\n';
}
```

这与直接使用`Pair`或`Pair<T>`而非`Coord`或`Coord<T>`时的要求一致。


[下一课 13.x — 第13章总结与测验](Chapter-13/lesson13.x-chapter-13-summary-and-quiz.md)  
[返回主页](/)  
[上一课 13.14 — 类模板参数推导（CTAD）与推导指南](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)