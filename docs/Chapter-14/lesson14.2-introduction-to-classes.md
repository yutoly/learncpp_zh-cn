14.2 — 类简介  
================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日 下午12:14（PDT）  
2024年6月26日更新  

前章回顾  
----------------  
在上一章中，我们学习了结构体（structs）（[13.7 — 结构体、成员与成员选择简介](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)），讨论了它们如何有效地将多个成员变量打包成单个对象，便于初始化和整体传递。换句话说，结构体为存储和传输相关数据提供了便捷的封装方式。  

考虑以下结构体示例：  
```cpp
#include <iostream>

struct Date
{
    int day{};
    int month{};
    int year{};
};

void printDate(const Date& date)
{
    std::cout << date.day << '/' << date.month << '/' << date.year; // 这里假设使用日/月/年格式
}

int main()
{
    Date date{ 4, 10, 21 }; // 使用聚合初始化
    printDate(date);         // 可将整个结构体传递给函数

    return 0;
}
```  
上述程序输出：  
```
4/10/21
```  

> **重要提醒**  
> 本系列教程中所有结构体均为聚合类型（aggregates）。聚合类型的详细讨论见课程[13.8 — 结构体的聚合初始化](Chapter-13/lesson13.8-struct-aggregate-initialization.md)。  

结构体的局限性  
----------------  
尽管结构体非常实用，但在构建大型复杂程序（尤其是多人协作项目）时，结构体存在若干缺陷。  

**类不变量问题（Class invariant problem）**  
结构体的最大缺陷在于无法有效记录和强制类不变量（class invariants）。在课程[9.6 — assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md)中，我们将不变量定义为"某个组件执行期间必须保持为真的条件"。  

对于类类型（包括结构体、类和联合体），**类不变量**是指对象生命周期内必须始终满足的条件，以保持对象的有效状态。违反类不变量的对象处于**无效状态**，继续使用可能导致意外行为或未定义行为。  

> **关键洞察**  
> 使用违反类不变量的对象可能导致意外行为或未定义行为。  

**示例分析**  
考虑以下结构体：  
```cpp
struct Pair
{
    int first {};
    int second {};
};
```  
`first`和`second`成员可独立设置任意值，因此Pair结构体没有不变量。  

再观察以下类似结构体：  
```cpp
struct Fraction
{
    int numerator { 0 };
    int denominator { 1 };
};
```  
数学上分母为`0`的分数是未定义的（因为分数值等于分子除以分母，而除以0是数学未定义操作）。因此我们需要确保Fraction对象的`denominator`成员永远不为`0`。若违反，该Fraction对象即处于无效状态，继续使用可能导致未定义行为。  

示例程序：  
```cpp
#include <iostream>

struct Fraction
{
    int numerator { 0 };
    int denominator { 1 }; // 类不变量：永远不能为0
};

void printFractionValue(const Fraction& f)
{
     std::cout << f.numerator / f.denominator << '\n';
}

int main()
{
    Fraction f { 5, 0 };   // 创建分母为0的Fraction对象
    printFractionValue(f); // 导致除零错误

    return 0;
}
```  
虽然我们通过注释记录了Fraction的不变量，并通过默认成员初始化确保用户不显式初始化时`denominator`为`1`，但显式违反此不变量（如初始化分母为`0`）仍被允许。当调用`printFractionValue(f)`时，程序因除零错误终止。  

> **补充说明**  
> 改进方法是在`printFractionValue`函数顶部添加`assert(f.denominator != 0);`。这虽增加代码文档性，但未从根本上解决问题。我们更希望在问题源头（成员初始化或赋值时）捕获错误，而非在下游使用错误值时发现。  

**复杂类不变量案例**  
当结构体成员间需要保持复杂关联时，类不变量的维护更具挑战性。  
```cpp
#include <string>

struct Employee
{
    std::string name { };
    char firstInitial { }; // 应始终保存name的首字符（或0）
};
```  
该结构体中，`firstInitial`成员值应与`name`的首字符一致。初始化或修改`name`时，用户需手动维护这种关联关系。这种关联对使用Employee对象的开发者可能不够明显，即使知晓也容易遗忘。  

即使编写辅助函数来创建和更新Employee对象（确保`firstInitial`始终取自`name`首字符），仍需依赖用户主动使用这些函数。简而言之，依赖对象使用者维护类不变量容易引发问题。  

> **关键洞察**  
> 依赖对象使用者维护类不变量极易导致问题。  

类的引入  
----------------  
开发C++时，Bjarne Stroustrup希望引入能创建更直观的程序自定义类型的能力，并寻求解决大型复杂程序常见问题（如类不变量问题）的优雅方案。受Simula（首个面向对象编程语言）启发，他创造了**类（class）**类型。  

与结构体类似，**类**是程序定义的复合类型，可包含多个不同类型的成员变量。  

> **技术说明**  
> 从技术角度看，结构体与类几乎完全相同——任何能用结构体实现的示例都可用类实现，反之亦然。但从实践角度，二者用法不同。结构体与类的异同详见课程[14.5 — 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)。  

类的定义  
----------------  
类作为程序定义类型，需先定义后使用。类定义方式与结构体相似，但使用`class`关键字。例如：  
```cpp
class Employee
{
    int m_id {};
    int m_age {};
    double m_wage {};
};
```  

> **相关说明**  
> 类成员变量常以"m_"前缀命名，详见课程[14.5 — 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)。  

为展示类与结构体的相似性，以下程序将开篇示例中的`Date`改为类实现：  
```cpp
#include <iostream>

class Date       // 将struct改为class
{
public:          // 添加访问说明符
    int m_day{}; // 成员变量添加"m_"前缀
    int m_month{};
    int m_year{};
};

void printDate(const Date& date)
{
    std::cout << date.m_day << '/' << date.m_month << '/' << date.m_year;
}

int main()
{
    Date date{ 4, 10, 21 };
    printDate(date);

    return 0;
}
```  
输出结果仍为：  
```
4/10/21
```  

> **相关说明**  
> 访问说明符的作用详见课程[14.5 — 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)。  

标准库中的类  
----------------  
您可能已在不知情的情况下使用过类对象。`std::string`和`std::string_view`均定义为类。实际上，标准库中大多数非别名类型都是类！  

类是C++的核心——其重要性体现在C++最初被命名为"带类的C"。熟悉类后，您将在C++开发中大量编写、测试和使用类。  

测验时间  
----------------  
**问题1**  
给定一组值（年龄、地址编号等），我们可能需要知道其中的最小值和最大值。由于这两个值相关，可用结构体组织：  
```cpp
struct minMax
{
    int min; // 当前最小值
    int max; // 当前最大值
};
```  
该结构体存在未明示的类不变量。请问不变量是什么？  
  
<details><summary>答案</summary>不变量是`min <= max`。若`min`大于`max`，使用该结构体的代码可能出错。</details>  

[下一课14.3 成员函数](Chapter-14/lesson14.3-member-functions.md)  
[返回主页](/)  
[上一课14.1 面向对象编程简介](Chapter-14/lesson14.1-introduction-to-object-oriented-programming.md)