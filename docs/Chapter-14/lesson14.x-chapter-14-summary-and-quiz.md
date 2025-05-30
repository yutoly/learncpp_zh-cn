14.x — 第14章总结与测验  
===================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月17日（首次发布于2016年3月25日）  

本章我们深入探讨了C++的核心精髓——类（class）！这是本教程系列中最关键的章节，为后续内容奠定了重要基础。  

本章回顾  
----------------  

在**过程式编程（procedural programming）**中，核心是创建实现程序逻辑的"过程"（在C++中称为函数）。我们将数据对象传递给这些函数，函数对数据执行操作后可能返回结果给调用者。  

通过**面向对象编程（object-oriented programming，OOP）**，核心在于创建程序定义的数据类型，这些类型既包含属性又包含一组明确定义的行为。  

**类不变量（class invariant）**是指对象生命周期中必须始终满足的条件，以确保对象处于有效状态。违反类不变量的对象处于**无效状态（invalid state）**，继续使用可能导致意外或未定义行为。  

**类（class）**是程序定义的复合类型，将数据与操作这些数据的函数捆绑在一起。  

属于类类型的函数称为**成员函数（member function）**。调用成员函数所针对的对象常被称为**隐式对象（implicit object）**。非成员函数则称为**非成员函数（non-member function）**以作区分。若类类型没有数据成员，建议改用命名空间。  

**const成员函数（const member function）**是保证不修改对象、也不调用任何非const成员函数的成员函数（因后者可能修改对象）。不改变对象状态的成员函数应声明为const，以便在非const和const对象上都能调用。  

每个类类型成员都有**访问级别（access level）**属性，决定谁能访问该成员。访问级别系统有时非正式地称为**访问控制（access controls）**。访问级别以类为单位定义，而非对象。  

**公有成员（public members）**是没有访问限制的类成员。公有成员可被任何人访问（只要在作用域内），包括同类其他成员。**公共代码（the public）**（即存在于类类型成员之外的代码）也能访问公有成员，例如非成员函数和其他类类型的成员。  

默认情况下，结构体（struct）的所有成员都是公有的。  

**私有成员（private members）**是只能被同类其他成员访问的类成员。  

默认情况下，类的成员是私有的。含有私有成员的类不再是聚合类型（aggregate），因此不能使用聚合初始化。建议私有成员名称以"m_"前缀开头，以便与局部变量、函数参数和成员函数区分。  

可通过**访问说明符（access specifier）**显式设置成员访问级别。结构体通常应避免使用访问说明符，让所有成员默认保持公有。  

**访问函数（access function）**是简单的公有成员函数，用于获取或修改私有成员变量值。访问函数分为两种：getter和setter。**Getter**（访问器）是返回私有成员变量值的公有成员函数。**Setter**（修改器）是设置私有成员变量值的公有成员函数。  

类类型的**接口（interface）**定义了用户与类类型对象的交互方式。由于只有公有成员能从类外部访问，类的公有成员构成其接口。因此，由公有成员组成的接口有时称为**公共接口（public interface）**。  

类类型的**实现（implementation）**包含使类按预期运行的代码，包括存储数据的成员变量，以及包含程序逻辑和操作成员变量的成员函数体。  

在编程中，**数据隐藏（data hiding）**（亦称**信息隐藏（information hiding）**或**数据抽象（data abstraction）**）是通过隐藏程序定义数据类型的实现细节，强制分离接口与实现的技术。  

**封装（encapsulation）**有时也指数据隐藏，但该术语也用于指代数据与函数的捆绑（不考虑访问控制），因此含义可能模糊。  

定义类时，建议先声明公有成员后声明私有成员，以突出公共接口并弱化实现细节。  

**构造函数（constructor）**是用于初始化类类型对象的特殊成员函数。创建非聚合类类型对象时，必须找到匹配的构造函数。  

**成员初始化列表（member initializer list）**允许在构造函数中初始化成员变量。列表中的成员变量应按类定义顺序排列。相比在构造函数体内赋值，优先使用成员初始化列表。  

不接收参数（或所有参数都有默认值）的构造函数称为**默认构造函数（default constructor）**。用户未提供初始化值时使用默认构造函数。若非聚合类类型对象没有用户声明的构造函数，编译器将生成**隐式默认构造函数（implicit default constructor）**以便进行值初始化或默认初始化。  

构造函数可将初始化委托给同类其他构造函数，此过程称为**构造函数链（constructor chaining）**，这类构造函数称为**委托构造函数（delegating constructor）**。构造函数只能委托或初始化，不可同时进行。  

**临时对象（temporary object）**（亦称**匿名对象（anonymous object）**或**无名对象（unnamed object）**）是没有名称且仅存在于单个表达式期间的对象。  

**拷贝构造函数（copy constructor）**是用同类型现有对象初始化新对象的构造函数。若未为类提供拷贝构造函数，C++将创建执行成员级初始化的公有**隐式拷贝构造函数（implicit copy constructor）**。  

**as-if规则（as-if rule）**允许编译器以任何方式修改程序以优化代码，只要不改变程序"可观察行为"。该规则的例外是拷贝省略（copy elision）。**拷贝省略**是编译器移除不必要对象拷贝的优化技术。当编译器优化掉拷贝构造函数调用时，称该构造函数被**省略（elided）**。  

用于在程序定义类型与值之间转换的函数称为**用户定义转换（user-defined conversion）**。可用于隐式转换的构造函数称为**转换构造函数（converting constructor）**。默认所有构造函数都是转换构造函数。  

使用**explicit**关键字可禁止构造函数作为转换构造函数。该构造函数不能用于拷贝初始化或拷贝列表初始化，也不能用于隐式转换。  

默认将接收单个参数的构造函数声明为explicit。若类型间的隐式转换语义等价且高效（如`std::string`到`std::string_view`的转换），可考虑不声明为explicit。不要将拷贝或移动构造函数声明为explicit，因其不执行转换。  

成员函数（含构造函数）可为constexpr。从C++14起，constexpr成员函数不再隐式const。  

测验时间  
----------------  

**作者注**  
原属本课的二十一点测验题已移至[17.x — 第17章总结与测验](Chapter-17/lesson17.x-chapter-17-summary-and-quiz.md)。  

**问题1**  
a) 编写名为`Point2d`的类，包含两个`double`类型成员变量：`m_x`和`m_y`，默认值均为`0.0`。提供构造函数和`print()`函数。  

以下程序应能运行：  

```cpp
#include <iostream>

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    // Point2d third{ 4.0 }; // 取消注释应报错 

    first.print();
    second.print();

    return 0;
}
```  

应输出：  

```
Point2d(0, 0)
Point2d(3, 4)
```  

[显示解答](javascript:void(0))  
<details><summary>解答</summary>  

```cpp
#include <iostream>

class Point2d
{
private:
	double m_x{ 0.0 };
	double m_y{ 0.0 };

public:
	Point2d() = default;

	Point2d(double x, double y)
		: m_x{ x }, m_y{ y }
	{
	}

	void print() const
	{
		std::cout << "Point2d(" << m_x << ", " << m_y << ")\n";
	}
};

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    // Point2d third{ 4.0 }; // 取消注释应报错 

    first.print();
    second.print();

    return 0;
}
```  
</details>  

b) 添加名为`distanceTo()`的成员函数，接收另一`Point2d`参数并计算间距。给定两点(x1,y1)和(x2,y2)，间距计算公式为`std::sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))`。`std::sqrt`函数位于`cmath`头文件。  

以下程序应能运行：  

```cpp
#include <cmath>
#include <iostream>

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    first.print();
    second.print();

    std::cout << "间距: " << first.distanceTo(second) << '\n';

    return 0;
}
```  

应输出：  

```
Point2d(0, 0)
Point2d(3, 4)
间距: 5
```  

[显示解答](javascript:void(0))  
<details><summary>解答</summary>  

```cpp
#include <cmath>
#include <iostream>

class Point2d
{
private:
	double m_x{ 0.0 };
	double m_y{ 0.0 };

public:
	Point2d() = default;

	Point2d(double x, double y)
		: m_x{ x }, m_y{ y }
	{
	}

	void print() const
	{
		std::cout << "Point2d(" << m_x << ", " << m_y << ")\n";
	}

	double distanceTo(const Point2d& other) const
	{
		return std::sqrt(
            (m_x - other.m_x)*(m_x - other.m_x) +
            (m_y - other.m_y)*(m_y - other.m_y)
            );
	}
};

int main()
{
    Point2d first{};
    Point2d second{ 3.0, 4.0 };

    first.print();
    second.print();

    std::cout << "间距: " << first.distanceTo(second) << '\n';

    return 0;
}
```  
</details>  

**问题2**  
在课程[13.10 — 结构体的传递与返回](Chapter-13/lesson13.10-passing-and-returning-structs.md)中，我们用`Fraction`结构体编写了程序。参考方案如下：  

```cpp
#include <iostream>

struct Fraction
{
    int numerator{ 0 };
    int denominator{ 1 };
};

// ...（函数实现略）
```  

将`Fraction`从结构体转换为类，所有函数改为（非静态）成员函数。  

**作者注**  
注意：本题未遵循何时使用非成员或成员函数的最佳实践，目的是测试将非成员函数转为成员函数的能力。  

[显示解答](javascript:void(0))  
<details><summary>解答</summary>  

```cpp
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    explicit Fraction(int numerator=0, int denominator=1)
        : m_numerator { numerator }, m_denominator { denominator}
    {
    }

    void getFraction()
    {
        std::cout << "分子值：";
        std::cin >> m_numerator; // 成员函数可直接访问成员
        std::cout << "分母值：";
        std::cin >> m_denominator;
        std::cout << '\n';
    }

    Fraction multiply(const Fraction& f) const
    {
        return Fraction{ m_numerator * f.m_numerator, m_denominator * f.m_denominator };
    }

    void printFraction() const
    {
        std::cout << m_numerator << '/' << m_denominator << '\n';
    }
};

int main()
{
    Fraction f1{};
    f1.getFraction();
    
    Fraction f2{};
    f2.getFraction();

    std::cout << "分数乘积：";

    f1.multiply(f2).printFraction();

    return 0;
}
```  
</details>  

**问题3**  
上题解答中为何将`Fraction`构造函数设为`explicit`？  

[显示解答](javascript:void(0))  
<details><summary>解答</summary>  
声明explicit构造函数可防止通过单值隐式转换创建`Fraction`，避免类似`f1.multiply(true)`的无效操作。该调用需要将`true`隐式转换为`Fraction`，但explicit构造函数无法用于隐式转换，编译器将报错。  
</details>  

**问题4**  
上题中为何`getFraction()`和`print()`更适合作为非成员函数？  

[显示解答](javascript:void(0))  
<details><summary>解答</summary>  
非成员版本`getFraction()`可一步完成分数对象的定义与初始化，而成员版本需要先创建对象再调用函数。同时将`print()`改为非成员函数（通过访问函数访问成员）可简化类接口，降低类实现变更对打印功能的影响。  
</details>  

[下一课 15.1 隐式"this"指针与成员函数链式调用](Chapter-15/lesson15.1-the-hidden-this-pointer-and-member-function-chaining.md)
[返回主页](/)  
[上一课 14.17 constexpr聚合与类](Chapter-14/lesson14.17-constexpr-aggregates-and-classes.md)