14.17 — constexpr 聚合体与类  
=========================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月29日（首次发布于2024年5月22日）  

在课程[F.1 — constexpr 函数](Chapter-F/lessonF.1-constexpr-functions.md)中，我们介绍了可在编译期或运行时求值的 constexpr 函数。例如：  

```cpp
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    std::cout << greater(5, 6) << '\n'; // greater(5, 6)可能在编译期或运行时求值

    constexpr int g { greater(5, 6) };  // greater(5, 6)必须在编译期求值
    std::cout << g << '\n';             // 输出6

    return 0;
}
```  

在此示例中，`greater()`是 constexpr 函数，`greater(5, 6)`是常量表达式（constant expression）。由于`std::cout << greater(5, 6)`在非 constexpr 上下文中调用，编译器可自由选择求值时机。当用`greater(5, 6)`初始化 constexpr 变量`g`时，则必须在编译期求值。  

现在考虑以下类似示例：  

```cpp
#include <iostream>

struct Pair
{
    int m_x {};
    int m_y {};

    int greater() const
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};

int main()
{
    Pair p { 5, 6 };                  // 输入是constexpr值
    std::cout << p.greater() << '\n'; // p.greater()在运行时求值

    constexpr int g { p.greater() };  // 编译错误：greater() 非 constexpr
    std::cout << g << '\n';

    return 0;
}
```  

此版本中，`greater()`是成员函数但未标记为 constexpr。当尝试用`p.greater()`初始化 constexpr 变量`g`时，由于无法在编译期求值导致错误。  

**constexpr 成员函数**  
通过`constexpr`关键字可将成员函数声明为 constexpr：  

```cpp
struct Pair
{
    int m_x {};
    int m_y {};

    constexpr int greater() const // 可在编译期或运行时求值
    {
        return (m_x > m_y  ? m_x : m_y);
    }
};
```  

当`p.greater()`用于初始化 constexpr 变量时，仍会报错，因为`p`本身并非 constexpr。  

**constexpr 聚合体**  
将`p`声明为 constexpr 即可解决：  

```cpp
constexpr Pair p { 5, 6 };        // 现在为constexpr
constexpr int g { p.greater() };  // 正确：p.greater()在编译期求值
```  

由于`Pair`是聚合体（aggregate），隐式支持 constexpr，因此该方案有效。  

**非聚合类与 constexpr 构造函数**  
当`Pair`变为非聚合类时：  

```cpp
class Pair // 不再是聚合体
{
private:
    int m_x {};
    int m_y {};

public:
    Pair(int x, int y): m_x { x }, m_y { y } {}
    // ...
};
```  

此时声明`constexpr Pair p`会导致编译错误，提示`Pair`非字面类型（literal type）。字面类型需满足特定条件，如拥有 constexpr 构造函数。解决方案是将构造函数标记为 constexpr：  

```cpp
class Pair
{
public:
    constexpr Pair(int x, int y): m_x { x }, m_y { y } {}
    // ...
};
```  

**最佳实践**  
若希望类能在编译期求值：  
* 将成员函数和构造函数标记为 constexpr  
* 隐式定义的构造函数若符合条件会自动成为 constexpr  
* 显式默认化的构造函数需手动标记 constexpr  

**C++14 中的变化**  
在 C++14 中，constexpr 成员函数不再隐式具有 const 限定。需显式标记：  

```cpp
constexpr int greater() const // C++14需显式const
{
    return (m_x > m_y ? m_x : m_y);
}
```  

**非 const 的 constexpr 成员函数**  
非 const 的 constexpr 成员函数可修改成员变量（当对象非 const 时）：  

```cpp
constexpr void reset() // constexpr但非const
{
    m_x = m_y = 0; // 可修改非const对象的成员
}
```  

在编译期求值的上下文中，仍可调用此类函数：  

```cpp
constexpr Pair zero()
{
    Pair p { 1, 2 }; // p是非const
    p.reset();       // 合法：在非const对象上调用非const成员函数
    return p;
}
```  

**返回 const 引用/指针**  
返回 const 引用的 constexpr 成员函数示例：  

```cpp
constexpr const int& getX() const { return m_x; }
```  

该函数同时满足：  
* `constexpr`：可在编译期求值  
* `const int&`：返回常量引用  
* 末尾`const`：可在 const 对象上调用  

[下一课 14.x — 第14章总结与测验](Chapter-14/lesson14.x-chapter-14-summary-and-quiz.md)  
[返回主页](/)  
[上一课 14.16 — 转换构造函数与explicit关键字](Chapter-14/lesson14.16-converting-constructors-and-the-explicit-keyword.md)