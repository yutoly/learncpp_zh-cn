15.5 — 带有成员函数的类模板  
=============================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月6日（首次发布于2023年9月11日）  

在课程[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)中，我们学习了函数模板：  

```cpp
template <typename T> // 模板参数声明
T max(T x, T y) // max<T>的函数模板定义
{
    return (x < y) ? y : x;
}
```  

通过函数模板，我们可以定义类型模板参数（如`typename T`），并将其用作函数参数的类型（`T x, T y`）。  

在课程[13.13 — 类模板](Chapter-13/lesson13.13-class-templates.md)中，我们介绍了类模板，它允许将类型模板参数用于类类型（结构体、类、联合体）的数据成员类型：  

```cpp
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// Pair的推导指引（C++17及之前版本需要）
template <typename T>
Pair(T, T) -> Pair<T>;

int main()
{
    Pair<int> p1{ 5, 6 };        // 实例化Pair<int>并创建对象p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // 实例化Pair<double>并创建对象p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // 使用已有的Pair<double>定义创建对象p3
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
```  

**相关内容**  
推导指引的详细讨论见课程[13.14 — 类模板参数推导（CTAD）与推导指引](class-template-argument-deduction-ctad-and-deduction-guides/#DeductionGuide)。  

本章将结合函数模板和类模板的元素，深入探讨带有成员函数的类模板。  

成员函数中的类型模板参数  
----------------  

类模板参数声明中定义的类型模板参数既可用作数据成员类型，也可用作成员函数参数类型。  

以下示例将上述`Pair`类模板从结构体改为类：  

```cpp
#include <ios>       // 用于std::boolalpha
#include <iostream>

template <typename T>
class Pair
{
private:
    T m_first{};
    T m_second{};

public:
    // 在类定义内部定义成员函数时
    // 自动应用类的模板参数声明
    Pair(const T& first, const T& second)
        : m_first{ first }
        , m_second{ second }
    {
    }

    bool isEqual(const Pair<T>& pair);
};

// 在类定义外部定义成员函数时
// 需要重新提供模板参数声明
template <typename T>
bool Pair<T>::isEqual(const Pair<T>& pair)
{
    return m_first == pair.m_first && m_second == pair.m_second;
}

int main()
{
    Pair p1{ 5, 6 }; // 使用CTAD推导为Pair<int>
    std::cout << std::boolalpha << "isEqual(5, 6): " << p1.isEqual( Pair{5, 6} ) << '\n';
    std::cout << std::boolalpha << "isEqual(5, 7): " << p1.isEqual( Pair{5, 7} ) << '\n';

    return 0;
}
```  

需注意以下几点：  

1. 由于类包含私有成员，不再是聚合类型，因此不能使用聚合初始化。必须通过构造函数初始化对象。  
2. 构造函数的参数类型设为`const T&`以避免拷贝开销。  
3. 在类模板内部定义成员函数时，隐式使用类模板参数声明。  
4. 非聚合类通过匹配的构造函数即可实现CTAD，无需推导指引。  
5. 在类外部定义成员函数时，需重新提供模板参数声明，并使用完全限定的模板类名（如`Pair<T>::isEqual`）。  

**注入类名（injected class name）**  
在类作用域内，未限定的类名称为注入类名。对于类模板`Pair<T>`，在其作用域内使用`Pair`等价于`Pair<T>`。因此构造函数命名为`Pair`仍有效，编译器会视为`Pair<T>`。  

这意味着成员函数定义可简化为：  

```cpp
template <typename T>
bool Pair<T>::isEqual(const Pair& pair) // 参数类型使用Pair而非Pair<T>
{
    return m_first == pair.m_first && m_second == pair.m_second;
}
```  

**关键洞察**  
在课程[13.14](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)中提到，CTAD不适用于函数参数。但使用注入类名作为参数类型时，实际是模板全名的简写，与CTAD无关。  

类模板成员函数的定义位置  
----------------  

编译器需要同时看到类定义和成员函数模板定义才能实例化模板：  
- 成员函数定义在类内部时，模板定义随类定义可见  
- 定义在外部时，应紧接类定义下方（通常在头文件中）  

**最佳实践**  
类模板的成员函数若定义在外部，应紧接类定义之后（同一文件内）。  

测验时间  
----------------  

**问题1**  
编写名为Triad的类模板，包含3个独立类型模板参数的私有数据成员。要求包含构造函数、访问函数及外部定义的`print()`成员函数。  

测试程序应输出：  
```
[1, 2, 3]
1
[1, 2.3, Hello]
```  

  
<details><summary>解答</summary>  

```cpp
#include <iostream>
#include <string>

template <typename T, typename U, typename V>
class Triad
{
private:
    T m_first{};
    U m_second{};
    V m_third{};

public:
    Triad(const T& first, const U& second, const V& third)
        : m_first{ first }
        , m_second{ second }
        , m_third{ third }
    {
    }

    const T& first() const { return m_first; }
    const U& second() const { return m_second; }
    const V& third() const { return m_third; }

    void print() const;
};

template <typename T, typename U, typename V>
void Triad<T, U, V>::print() const
{
    std::cout << '[' << m_first << ", " << m_second << ", " << m_third << ']' ;
}

int main()
{
    Triad<int, int, int> t1{ 1, 2, 3 };
    t1.print();
    std::cout << '\n';
    std::cout << t1.first() << '\n';

    using namespace std::literals::string_literals;
    const Triad t2{ 1, 2.3, "Hello"s };
    t2.print();
    std::cout << '\n';

    return 0;
}
```  
</details>  

**问题2**  
若移除`print()`函数的`const`限定，程序为何无法编译？  
  
<details><summary>解答</summary>  
`t2`是常量对象，只能调用常量成员函数。非const的`print()`可能修改对象，违反常量性约束。</details>  

[下一课 15.6 静态成员变量](Chapter-15/lesson15.6-static-member-variables.md)  
[返回主页](/)  
[上一课 15.4 析构函数简介](Chapter-15/lesson15.4-introduction-to-destructors.md)