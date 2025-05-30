14.5 — 公有成员与私有成员及访问说明符  
========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年9月4日下午2:17（首次发布）  
2024年7月3日（最后更新）  

成员访问  
----------------  

类类型的每个成员都有一个称为**访问级别（access level）**的属性，用于确定谁可以访问该成员。  

C++有三种不同的访问级别：*public（公有）*、*private（私有）* 和 *protected（受保护）*。本章重点介绍常用的两种访问级别：公有和私有。  

> **相关内容**  
> 受保护访问级别将在继承章节讨论（课程[24.5 — 继承与访问说明符](Chapter-24/lesson24.5-inheritance-and-access-specifiers.md)）。  

当访问成员时，编译器会检查该成员的访问级别是否允许访问。若不允许，编译器将生成编译错误。这种访问级别系统有时非正式地称为**访问控制（access controls）**。  

结构体（struct）的成员默认是公有的  
----------------  

具有*public*访问级别的成员称为*公有成员（public members）*。**公有成员**是指没有任何访问限制的类类型成员。正如开篇类比中的公园，公有成员可以被任何人访问（只要在作用域内）。  

公有成员可以被同一类的其他成员访问。特别需要注意的是，公有成员也可以被**公共代码（the public）**访问，这里的公共代码指存在于给定类类型成员*之外*的代码。公共代码包括非成员函数以及其他类类型的成员。  

> **关键洞察**  
> 结构体的成员默认是公有的。公有成员可以被类类型的其他成员以及公共代码访问。  
>  
> 术语"公共代码"用于指代存在于给定类类型成员之外的代码，包括非成员函数和其他类类型的成员。  

默认情况下，结构体的所有成员都是公有成员。考虑以下结构体示例：  
```cpp
#include <iostream>

struct Date
{
    // struct成员默认公有，可被任何人访问
    int year {};       // 默认公有
    int month {};      // 默认公有
    int day {};        // 默认公有

    void print() const // 默认公有
    {
        // 成员函数中可访问公有成员
        std::cout << year << '/' << month << '/' << day;
    }
};

// 非成员函数main属于"公共代码"
int main()
{
    Date today { 2020, 10, 14 }; // 聚合初始化结构体

    // 公共代码可访问公有成员
    today.day = 16; // 合法：day成员是公有的
    today.print();  // 合法：print()成员函数是公有的

    return 0;
}
```  

类（class）的成员默认是私有的  
----------------  

具有*private*访问级别的成员称为*私有成员（private members）*。**私有成员**是指只能被同一类的其他成员访问的类类型成员。  

考虑以下与上例几乎相同的示例：  
```cpp
#include <iostream>

class Date // 改为class而非struct
{
    // class成员默认私有，只能被其他成员访问
    int m_year {};     // 默认私有
    int m_month {};    // 默认私有
    int m_day {};      // 默认私有

    void print() const // 默认私有
    {
        // 成员函数中可访问私有成员
        std::cout << m_year << '/' << m_month << '/' << m_day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // 编译错误：无法再使用聚合初始化

    // 公共代码不能访问私有成员
    today.m_day = 16; // 编译错误：m_day成员是私有的
    today.print();    // 编译错误：print()成员函数是私有的

    return 0;
}
```  

> **关键洞察**  
> 类的成员默认是私有的。私有成员可以被类的其他成员访问，但不能被公共代码访问。  
>  
> 含有私有成员的类不再是聚合类型（aggregate），因此无法再使用聚合初始化。  

通过访问说明符设置访问级别  
----------------  

虽然结构体和类有默认访问级别，但我们可以使用**访问说明符（access specifier）**显式设置成员的访问级别。访问说明符会设置其后所有成员的访问级别。C++提供三种访问说明符：`public:`、`private:` 和 `protected:`。  

在以下示例中，我们使用`public:`说明符确保`print()`成员函数可被公共代码访问，使用`private:`说明符使数据成员保持私有：  
```cpp
class Date
{
// 此处定义的成员默认私有

public: // 公有访问说明符
    void print() const // 因public说明符成为公有成员
    {
        // 成员函数可访问其他私有成员
        std::cout << m_year << '/' << m_month << '/' << m_day;
    }

private: // 私有访问说明符
    int m_year { 2020 };  // 因private说明符成为私有成员
    int m_month { 14 };   // 私有成员
    int m_day { 10 };     // 私有成员
};

int main()
{
    Date d{};
    d.print();  // 合法：main()允许访问公有成员

    return 0;
}
```  

访问级别最佳实践  
----------------  

**结构体**应完全避免使用访问说明符，保持所有成员默认公有。我们希望结构体保持聚合类型（aggregate），而聚合类型只能包含公有成员。  

**类**通常应该：  
* 将成员变量设为私有（或受保护）  
* 将成员函数设为公有  

> **最佳实践**  
> 类通常应使成员变量私有（或受保护），成员函数公有。  
> 结构体通常应避免使用访问说明符（所有成员默认公有）。  

访问级别按类生效  
----------------  

C++访问级别的一个微妙特性是：成员访问权限是按类（per-class）而非按对象（per-object）定义的。成员函数不仅可以访问隐式对象（implicit object）的私有成员，还可以访问同类型其他对象的私有成员。  

结构体与类的技术差异  
----------------  

结构体与类在技术上的唯一区别是：  
* 类默认成员为私有  
* 结构体默认成员为公有  

> **作者注**  
> 严格来说还有一个小差异——结构体默认公有继承，类默认私有继承。但在实践中这无关紧要，因为不应依赖继承的默认设置。  

测验时间  
----------------  

**问题1**  
a) 什么是公有成员？  
<details><summary>答案</summary>公有成员是类中可被任何人访问的成员，包括类其他成员和公共代码。</details>  

b) 什么是私有成员？  
<details><summary>答案</summary>私有成员是只能被类其他成员访问的成员。</details>  

c) 什么是访问说明符？  
<details><summary>答案</summary>决定后续成员访问权限的说明符。</details>  

d) 有多少种访问说明符？分别是什么？  
<details><summary>答案</summary>三种：public、private、protected。</details>  

**问题2**  
a) 编写包含私有成员和公有成员函数的Point3d类  
<details><summary>查看解答</summary>  
```cpp
#include <iostream>

class Point3d
{
private:
    int m_x {};
    int m_y {};
    int m_z {};

public:
    void setValues(int x, int y, int z)
    {
        m_x = x;
        m_y = y;
        m_z = z;
    }

    void print() const
    {
        std::cout << '<' << m_x << ", " << m_y << ", " << m_z << '>';
    }
};
```  
</details>  

b) 添加isEqual成员函数  
<details><summary>查看解答</summary>  
```cpp
bool isEqual(const Point3d& p) const
{
    return (m_x == p.m_x) && (m_y == p.m_y) && (m_z == p.m_z);
}
```  
</details>  

[下一课 14.6 访问函数](Chapter-14/lesson14.6-access-functions.md)  
[返回主页](/)  
[上一课 14.4 常量类对象与常量成员函数](Chapter-14/lesson14.4-const-class-objects-and-const-member-functions.md)