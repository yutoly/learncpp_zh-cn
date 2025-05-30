21.6 — 重载一元运算符 \+, \-, 和 !
=================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年11月25日（首次发布于2007年10月8日）

**重载一元运算符（unary operators）**

与之前介绍的运算符不同，正号（\+）、负号（\-）和逻辑非（!）运算符都是一元运算符（unary operators），这意味着它们仅作用于单个操作数。由于这些运算符仅操作应用它们的对象，因此一元运算符重载通常作为成员函数（member function）实现。这三个运算符的实现方式完全相同。

让我们通过之前示例中的Cents类来看看如何实现operator-：

```cpp
#include <iostream>

class Cents
{
private:
    int m_cents{};
 
public:
    Cents(int cents): m_cents{cents} {}
 
    // 以成员函数形式重载负号运算符（operator-）
    Cents operator-() const;

    int getCents() const { return m_cents; }
};
 
// 注意：此函数是成员函数！
Cents Cents::operator-() const
{
    return -m_cents; // 由于返回类型是Cents，这里使用Cents(int)构造函数进行隐式转换
}

int main()
{
    const Cents nickle{5};
    std::cout << "五美分债务的价值是 " << (-nickle).getCents() << " 分\n";

    return 0;
}
```

这个实现应该很直观。重载的负号运算符（operator-）是作为成员函数实现的，因此没有参数（操作对象是\*this）。它返回一个Cents对象，其值是原始值的取反。由于operator-不会修改Cents对象，我们可以（也应该）将其设为const函数（以便能在const Cents对象上调用）。

注意负号运算符（-）和减号运算符（-）之间不会混淆，因为它们的参数数量不同。

再看另一个示例。!运算符是逻辑非运算符（logical negation operator）——如果表达式为"true"，operator!将返回false，反之亦然。我们常见于布尔变量的判断：

```cpp
if (!isHappy)
    std::cout << "我不开心！\n";
else
    std::cout << "我很快乐！\n";
```

对于整数，0被视为false，其他值为true，因此应用于整数的operator!将在值为0时返回true，否则返回false。

扩展这个概念，我们可以说当对象处于"false"、"零"或默认初始化状态时，operator!应该返回true。

以下示例展示了对Point类同时重载operator-和operator!：

```cpp
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0):
        m_x{x}, m_y{y}, m_z{z}
    {
    }
 
    // 将Point转换为对应的负值
    Point operator- () const;

    // 当点在原点时返回true
    bool operator! () const;
 
    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }
};

// 将Point转换为对应的负值
Point Point::operator-() const
{
    return { -m_x, -m_y, -m_z };
}

// 当点在原点时返回true，否则返回false
bool Point::operator!() const
{
    return (m_x == 0.0 && m_y == 0.0 && m_z == 0.0);
}

int main()
{
    Point point{}; // 使用默认构造函数设置为(0.0, 0.0, 0.0)

    if (!point)
        std::cout << "点位于原点。\n";
    else
        std::cout << "点不在原点。\n";

    return 0;
}
```

该类的重载operator!在Point处于默认坐标(0.0, 0.0, 0.0)时返回布尔值"true"。因此上述代码输出：

```
点位于原点。

```

**测验时间**

1. 为Point类实现重载一元`operator+`。一元`operator+`只需返回其操作数（不会将负值转为正值）。

  
<details><summary>答案</summary>
直接解决方案：

```cpp
Point Point::operator+() const
{
    return { m_x, m_y, m_z };
}
```

由于返回的Point与操作对象完全相同，以下方式同样有效：

```cpp
Point Point::operator+() const
{
    return *this;
}
```

注意这里通过值返回拷贝而非const引用，因为使用者可能期望返回的对象是可修改的。
</details>

[下一课 21.7 重载比较运算符](Chapter-21/lesson21.7-overloading-the-comparison-operators.md)  
[返回主页](/)  
[上一课 21.5 使用成员函数重载运算符](Chapter-21/lesson21.5-overloading-operators-using-member-functions.md)