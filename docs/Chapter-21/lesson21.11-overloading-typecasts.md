21.11 — 重载类型转换运算符
==============================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年3月14日（首次发布于2007年10月30日）

在课程[10.6 — 显式类型转换与static_cast](Chapter-10/lesson10.6-explicit-type-conversion-casting-and-static-cast.md)中，我们学习了C++允许数据类型之间的转换。以下示例展示了int到double的转换：

```cpp
int n{ 5 };
auto d{ static_cast<double>(n) }; // 将int转换为double
```

C++已经内置了基础数据类型之间的转换规则。但对于自定义类类型，编译器默认无法进行转换。

在课程[14.16 — 转换构造函数与explicit关键字](Chapter-14/lesson14.16-converting-constructors-and-the-explicit-keyword.md)中，我们演示了如何使用转换构造函数（converting constructor）从其他类型创建类对象。但这种方法仅适用于目标类型是可修改的类类型。如果目标类型不可修改怎么办？

请看以下Cents类：

```cpp
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};
```

这个类保存美分数值，并提供了构造器将int转换为Cents。现在我们需要实现从Cents到int的逆转换。

作者注：
一首小诗：

将int转为Cents  
构造器欣然应允  
但反向转换的意图  
编译器却报错阻止

为此我们需要授予  
类型转换的许可证书  
定义转换的详细方式  
谜底即将为你揭示


重载类型转换运算符
----------------

我们可以通过重载类型转换运算符（overloaded typecast operator）实现类类型到其他类型的转换。以下为Cents添加int转换支持：

```cpp
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    // 重载int类型转换
    operator int() const { return m_cents; }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};
```

关键点说明：
- 重载类型转换必须是类的非静态成员函数，通常标记为const
- 没有显式参数，通过隐式this指针操作对象
- 返回类型由运算符名称决定，无需显式声明

现在我们可以直接将Cents对象传递给需要int参数的函数：

```cpp
#include <iostream>

void printInt(int value)
{
    std::cout << value;
}

int main()
{
    Cents cents{ 7 };
    printInt(cents); // 隐式调用operator int()

    std::cout << '\n';
    return 0;
}
```

显式调用方式：
```cpp
std::cout << static_cast<int>(cents);
```

类类型互转示例
------------

定义Dollars类并重载到Cents的转换：

```cpp
class Dollars
{
private:
    int m_dollars{};
public:
    Dollars(int dollars=0)
        : m_dollars{ dollars }
    {
    }

    // 允许Dollars到Cents的转换
    operator Cents() const { return Cents{ m_dollars * 100 }; }
};
```

使用示例：
```cpp
void printCents(Cents cents)
{
    std::cout << cents; // 隐式调用Cents::operator int()
}

int main()
{
    Dollars dollars{ 9 };
    printCents(dollars); // 先转Cents再转int
    std::cout << '\n';
    return 0;
}
// 输出：900
```

显式类型转换
----------

与构造函数类似，类型转换运算符也可以标记为explicit：

```cpp
explicit operator int() const { return m_cents; } // 显式转换
```

此时必须使用static_cast显式转换：
```cpp
std::cout << static_cast<int>(cents);
```

最佳实践建议：
- 类型转换运算符通常应标记为explicit
- 例外情况：当转换目标类型与源类型本质相同时

转换构造函数 vs 重载类型转换
-----------------------

选择原则：
1. 优先使用转换构造函数（让目标类管理自己的构造）
2. 以下情况使用重载类型转换：
   - 转换为基础类型（如bool）
   - 返回引用类型
   - 目标类型不可修改（如std::vector）
   - 避免循环依赖

示例说明：
std::string到std::string_view的转换使用重载类型转换，避免头文件循环包含。

注意事项：
- 不要同时为同一转换定义构造函数和类型转换运算符，可能导致歧义
- 转换路径选择策略：
   - 优先让目标类提供构造函数
   - 次选源类提供类型转换
   - 最后使用非成员函数

[下一课 21.12 重载赋值运算符](Chapter-21/lesson21.12-overloading-the-assignment-operator.md)  
[返回主页](/)  
[上一课 21.10 重载括号运算符](Chapter-21/lesson21.10-overloading-the-parenthesis-operator.md)