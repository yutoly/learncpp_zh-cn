15.2 — 类（class）与头文件（header file）
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月3日（首次发布于2007年9月11日）  

目前我们编写的所有类都足够简单，可以直接在类定义内部实现成员函数（member function）。例如这个简单的`Date`类，所有成员函数都在类定义中实现：  
```
#include <iostream>

class Date
{
private:
    int m_year{};
    int m_month{};
    int m_day{};
 
public:
    Date(int year, int month, int day)
        : m_year { year }
        , m_month { month }
        , m_day { day}
    {
    }

    void print() const { std::cout << "Date(" << m_year << ", " << m_month << ", " << m_day << ")\n"; }

    int getYear() const { return m_year; }
    int getMonth() const { return m_month; }
    int getDay() const { return m_day; }
};

int main()
{
    Date d { 2015, 10, 14 };
    d.print();

    return 0;
}
```  
但随着类的复杂度增加，将所有成员函数定义放在类内部会导致代码难以维护。使用现成类只需理解其公共接口（public interface），无需了解内部实现细节。成员函数实现细节会干扰公共接口的清晰度。  

为解决这个问题，C++允许通过在类定义外定义成员函数，将类的"声明（declaration）"与"实现（implementation）"分离。以下是改造后的`Date`类，构造函数和`print()`成员函数定义移至类外。注意这些成员函数的原型仍保留在类定义中（需作为类类型声明的一部分），但实际实现已外移：  
```
#include <iostream>

class Date
{
private:
    int m_year{};
    int m_month{};
    int m_day{};

public:
    Date(int year, int month, int day); // 构造函数声明

    void print() const; // print函数声明

    int getYear() const { return m_year; }
    int getMonth() const { return m_month; }
    int getDay() const  { return m_day; }
};

Date::Date(int year, int month, int day) // 构造函数定义
    : m_year{ year }
    , m_month{ month }
    , m_day{ day }
{
}

void Date::print() const // print函数定义
{
    std::cout << "Date(" << m_year << ", " << m_month << ", " << m_day << ")\n";
};

int main()
{
    const Date d{ 2015, 10, 14 };
    d.print();

    return 0;
}
```  
成员函数可像非成员函数那样定义在类外，区别在于需在成员函数名前添加类名限定符（本例为`Date::`），让编译器明确这是类成员而非普通函数。  

注意访问函数（access function）仍保留在类定义内。由于访问函数通常仅一行，放在类定义中不会增加过多冗余，而外移会导致代码行数增加。因此访问函数（及其他简单单行函数）通常保留在类定义内。  

将类定义置于头文件中  
--------------------  
若在源文件（.cpp）中定义类，该类仅能在该源文件内使用。大型项目中，常需在多个源文件中复用自定义类。  

在课程[2.11 — 头文件](Chapter-2/lesson2.11-header-files.md)中已学过函数声明可放入头文件，并通过`#include`在多个代码文件中使用。类同理，其定义可置于头文件中，通过`#include`供其他文件使用。  

与函数不同，使用类时编译器需看到完整定义（而非前向声明（forward declaration））。因为编译器需要：  
1. 校验成员的正确使用  
2. 计算类对象大小以实例化  

因此头文件通常包含类的完整定义。  

类文件命名规范  
--------------  
通常将类定义置于与类同名的头文件（.h），外联成员函数定义置于同名源文件（.cpp）。以下是`Date`类的拆分示例：  

Date.h：  
```
#ifndef DATE_H
#define DATE_H

class Date
{
private:
    int m_year{};
    int m_month{};
    int m_day{};
 
public:
    Date(int year, int month, int day);

    void print() const;

    int getYear() const { return m_year; }
    int getMonth() const { return m_month; }
    int getDay() const { return m_day; }
};

#endif
```  
Date.cpp：  
```
#include "Date.h"

Date::Date(int year, int month, int day) // 构造函数定义
    : m_year{ year }
    , m_month{ month }
    , m_day{ day }
{
}

void Date::print() const // print函数定义
{
    std::cout << "Date(" << m_year << ", " << m_month << ", " << m_day << ")\n";
};
```  
其他文件只需`#include "Date.h"`即可使用`Date`类。注意项目需编译Date.cpp以使链接器（linker）正确关联成员函数定义。  

最佳实践  
--------  
* 将类定义置于同名头文件  
* 简单成员函数（如访问函数、空构造函数等）保留在类定义内  
* 非简单成员函数定义在同名源文件中  

关于头文件多次包含的疑问  
----------------------  
多次包含含类定义的头文件是否违反单一定义规则（ODR）？  
类型不受ODR"每个程序仅能有一个定义"的限制，因此多翻译单元（translation unit）包含类定义不会引发问题。单翻译单元内多次包含仍违反ODR，但头文件保护符（header guard）或`#pragma once`可防止这种情况。  

内联成员函数  
------------  
定义在头文件中的成员函数可能引发ODR问题，解决方案如下：  
* 类内定义的成员函数隐式内联（inline），不受ODR限制  
* 类外定义的成员函数需显式标记`inline`才能置于头文件  

修改后的Date.h示例：  
```
#ifndef DATE_H
#define DATE_H

#include <iostream>

class Date
{
private:
    int m_year{};
    int m_month{};
    int m_day{};
 
public:
    Date(int year, int month, int day);

    void print() const;

    int getYear() const { return m_year; }
    int getMonth() const { return m_month; }
    int getDay() const { return m_day; }
};

inline Date::Date(int year, int month, int day) // 显式内联
    : m_year{ year }
    , m_month{ month }
    , m_day{ day }
{
}

inline void Date::print() const // 显式内联
{
    std::cout << "Date(" << m_year << ", " << m_month << ", " << m_day << ")\n";
};

#endif
```  
关键点  
------  
* 类内定义的函数隐式内联，允许多次包含  
* 类外定义函数需`inline`关键字标记才能内联  

内联展开条件  
------------  
编译器需看到完整函数定义才能进行内联展开。通常简单函数（如访问函数）定义在类内。若需在类外定义但希望内联，可在头文件中类定义下方以`inline`定义。  

为何不全放在头文件？  
--------------------  
虽然可行但存在弊端：  
1. 类定义冗余  
2. 头文件修改触发全量重编译  
3. 源文件修改仅需重编译自身  

例外情况  
--------  
1. 小型类仅用于单一源文件  
2. 少量非简单函数不值得单独源文件  
3. 现代C++的"纯头文件"库  
4. 模板类成员函数需定义在头文件  

作者说明  
--------  
后续课程为简洁起见，类多在单一源文件中实现。实际项目建议遵循头文件与源文件分离原则。  

成员函数的默认参数  
------------------  
根据课程[11.5 — 默认参数](Chapter-11/lesson11.5-default-arguments.md)，成员函数默认参数应置于类定义中。  

最佳实践  
--------  
成员函数的默认参数必须放在类定义内。  

库文件  
------  
标准库类（如`std::string`）只需包含头文件（如`#include <string>`），其实现位于预编译库文件中。第三方库可能提供头文件与预编译库，原因包括：  
1. 链接更快  
2. 共享库减少体积  
3. 知识产权保护  

创建自定义库需分离声明与实现，相关方法详见附录。  

测验  
----  
**问题1**  
成员函数外联定义的目的？  
a) 简化类定义  
b) 分离接口与实现  
c) 减少实现变更引发的重编译  
d) 以上全部  
<details><summary>答案</summary>d) 以上全部</details>  

**问题2**  
如何外联定义成员函数？  
a) 普通函数无类名前缀  
b) 类名+作用域解析运算符（::）  
c) 类内声明+`friend`外联定义  
d) 以上均否  
<details><summary>答案</summary>b) 类名+作用域解析运算符</details>  

**问题3**  
何时在类内定义简单成员函数？  
a) 总是（提升性能）  
b) 单行函数  
c) 高频调用函数  
d) 不建议类内定义  
<details><summary>答案</summary>b) 单行函数</details>  

**问题4**  
类定义存放位置？  
a) 同名.cpp文件  
b) 同名.h文件  
c) 包含头文件的.cpp  
d) 任意位置  
<details><summary>答案</summary>b) 同名.h文件</details>  

**问题5**  
关于ODR的正确描述？  
a) 禁止头文件定义类  
b) 允许单文件多次包含类定义  
c) 类内定义函数豁免ODR  
d) 非简单函数应放头文件  
<details><summary>答案</summary>c) 类内定义函数隐式内联，豁免ODR</details>  

[下一课 15.3 — 嵌套类型（成员类型）](Chapter-15/lesson15.3-nested-types-member-types.md)  
[返回主页](/)  
[上一课 15.1 — 隐藏的"this"指针与成员函数链式调用](Chapter-15/lesson15.1-the-hidden-this-pointer-and-member-function-chaining.md)