14.10 — 构造函数成员初始化列表  
=============================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年11月13日 上午10:03 PST  
2025年2月5日更新  

本课程延续[14.9 — 构造函数简介](Chapter-14/lesson14.9-introduction-to-constructors.md)的内容。  

通过成员初始化列表进行成员初始化  
----------------  

要让构造函数初始化成员变量，我们需要使用**成员初始化列表（member initializer list）**。请勿将此概念与名称相似的"初始化列表（initializer list）"混淆，后者用于通过值列表初始化聚合类型。  

通过示例学习成员初始化列表最为有效。以下示例中，`Foo(int, int)`构造函数已更新为使用成员初始化列表来初始化`m_x`和`m_y`：  
```cpp
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo(int x, int y)
        : m_x { x }, m_y { y } // 成员初始化列表
    {
        std::cout << "Foo(" << x << ", " << y << ") 已构造\n";
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo{ 6, 7 };
    foo.print();

    return 0;
}
```  

成员初始化列表定义在构造函数参数之后，以冒号（:）开头，列出每个成员及其初始化值（用逗号分隔）。此处必须使用直接初始化形式（推荐使用大括号，圆括号也可）——拷贝初始化（使用等号）在此处无效。注意成员初始化列表不以分号结尾。  

程序输出：  
```
Foo(6, 7) 已构造
Foo(6, 7)
```  

当`foo`实例化时，初始化列表中的成员会使用指定值初始化。本例中`m_x`被初始化为`x`的值（6），`m_y`被初始化为`y`的值（7）。随后执行构造函数体。  

调用`print()`成员函数时，可见`m_x`仍为6，`m_y`仍为7。  

成员初始化列表格式  
----------------  

C++允许灵活格式化成员初始化列表，以下样式均有效：  
```cpp
    Foo(int x, int y) : m_x { x }, m_y { y }
    {
    }
```

```cpp
    Foo(int x, int y) :
        m_x { x },
        m_y { y }
    {
    }
```

```cpp
    Foo(int x, int y)
        : m_x { x }
        , m_y { y }
    {
    }
```  

推荐使用第三种样式：  
* 冒号放在构造函数名之后的新行，清晰分隔成员初始化列表与函数原型  
* 缩进成员初始化列表，便于查看函数名称  

若初始化列表简短，可单行书写：  
```cpp
    Foo(int x, int y)
        : m_x { x }, m_y { y }
    {
    }
```  

否则每个成员单独成行（用逗号对齐）：  
```cpp
    Foo(int x, int y)
        : m_x { x }
        , m_y { y }
    {
    }
```  

成员初始化顺序  
----------------  

根据C++标准，成员初始化列表中的成员始终按照类定义中的声明顺序初始化（而非初始化列表中的顺序）。上例中，由于`m_x`在类定义中先于`m_y`声明，`m_x`会优先初始化（即使初始化列表中顺序不同）。  

由于直觉期望变量从左到右初始化，这可能导致潜在错误。例如：  
```cpp
#include <algorithm> // std::max
#include <iostream>

class Foo
{
private:
    int m_x{};
    int m_y{};

public:
    Foo(int x, int y)
        : m_y { std::max(x, y) }, m_x { m_y } // 问题在此行
    {
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo { 6, 7 };
    foo.print();

    return 0;
}
```  

作者机器输出：  
```
Foo(-858993460, 7)
```  

原因：虽然`m_y`在初始化列表中最先列出，但`m_x`因类定义顺序优先初始化。`m_x`初始化时使用了未初始化的`m_y`值。  

最佳实践  
----------------  

成员初始化列表中的变量应按类定义顺序排列。某些编译器会在成员初始化顺序错误时发出警告。  

建议避免使用其他成员的值来初始化成员。这样即使初始化顺序错误，也不会因依赖关系导致问题。  

成员初始化列表 vs 默认成员初始化器  
----------------  

成员可通过以下方式初始化：  
* 若成员在初始化列表中，使用列表中的值  
* 否则，使用默认成员初始化器  
* 否则，默认初始化  

若成员同时具有默认初始化器和初始化列表项，初始化列表项优先。示例如下：  
```cpp
#include <iostream>

class Foo
{
private:
    int m_x {};    // 默认成员初始化器（将被忽略）
    int m_y { 2 }; // 默认成员初始化器（将被使用）
    int m_z;       // 无初始化器

public:
    Foo(int x)
        : m_x { x } // 成员初始化列表
    {
        std::cout << "Foo 已构造\n";
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ", " << m_z << ")\n";
    }
};

int main()
{
    Foo foo { 6 };
    foo.print();

    return 0;
}
```  

作者机器输出：  
```
Foo 已构造
Foo(6, 2, -858993460)
```  

解释：`m_x`由列表初始化为6，`m_y`使用默认值2，`m_z`未初始化导致未定义行为。  

构造函数函数体  
----------------  

构造函数体通常保持为空，因为初始化工作通过成员初始化列表完成。但构造函数体在初始化列表之后执行，可用于其他设置任务（如打开文件、分配内存等）。  

新手有时会在构造函数体中赋值成员：  
```cpp
#include <iostream>

class Foo
{
private:
    int m_x { 0 };
    int m_y { 1 };

public:
    Foo(int x, int y)
    {
        m_x = x; // 错误：此为赋值而非初始化
        m_y = y; // 错误：此为赋值而非初始化
    }
};
```  

虽然简单案例可能有效，但对于const成员或引用类型，赋值不可行。  

关键洞察  
----------------  

成员初始化列表执行完毕后，对象即视为已初始化。函数体执行完毕后，对象视为已构造。  

最佳实践  
----------------  

优先使用成员初始化列表而非构造函数体内赋值。  

检测和处理构造函数无效参数  
----------------  

考虑Fraction类：  
```cpp
class Fraction
{
private:
    int m_numerator {};
    int m_denominator {};

public:
    Fraction(int numerator, int denominator):
        m_numerator { numerator }, m_denominator { denominator }
    {
    }
};
```  

分母不能为零。但如何检测用户传入零分母？  

在成员初始化列表中检测错误的手段有限。虽然可用条件运算符检测，但处理方式受限：  
```cpp
    Fraction(int numerator, int denominator):
        m_numerator { numerator }, m_denominator { denominator != 0.0 ? denominator : ??? }
    {
    }
```  

更好的做法是在构造函数体中使用断言或静态断言，但这无法处理生产环境的运行时错误。  

构造函数失败（预备知识）  
----------------  

构造函数失败时，最佳处理方式是抛出异常（详见[27.5 — 异常、类与继承](Chapter-27/lesson27.5-exceptions-classes-and-inheritance.md)和[27.7 — 函数try块](Chapter-27/lesson27.7-function-try-blocks.md)）。  

高级建议  
----------------  

若不能使用异常，可通过工厂函数返回`std::optional<Fraction>`（详见[12.15 — std::optional](Chapter-12/lesson12.15-stdoptional.md)和[15.8 — 友元非成员函数](Chapter-15/lesson15.8-friend-non-member-functions.md)）。  

测验  
----------------  

**问题1**  
编写Ball类，包含颜色（字符串）和半径（双精度）私有成员，实现打印函数。  
  
<details><summary>答案</summary>  
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Ball
{
private:
	std::string m_color { "none" };
	double m_radius { 0.0 };

public:
	Ball(std::string_view color, double radius)
		: m_color { color }, m_radius { radius }
	{
	}

	const std::string& getColor() const { return m_color; }
	double getRadius() const { return m_radius; }
};

void print(const Ball& ball)
{
    std::cout << "Ball(" << ball.getColor() << ", " << ball.getRadius() << ")\n";
}
```  
</details>  

**问题2**  
为何将`print()`设为非成员函数？  
  
<details><summary>答案</summary>遵循数据封装原则，详见[14.8 — 数据隐藏的优势](the-benefits-of-data-hiding-encapsulation/#prefer-non-member-functions)</details>  

**问题3**  
为何使用`std::string`而非`std::string_view`存储颜色？  
  
<details><summary>答案</summary>避免临时字符串导致悬垂指针，详见[13.11 — 结构体杂项](Chapter-13/lesson13.11-struct-miscellany.md)</details>  

[下一课 14.11 — 默认构造函数与默认参数](Chapter-14/lesson14.11-default-constructors-and-default-arguments.md)  
[返回主页](/)    
[上一课 14.9 — 构造函数简介](Chapter-14/lesson14.9-introduction-to-constructors.md)