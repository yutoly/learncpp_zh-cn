13.7 — 结构体（struct）、成员（member）与成员选择（member selection）入门  
==============================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月4日（首次发布于2007年6月20日）

编程中常需多个变量共同表示某个实体。正如前章介绍（[12.1 — 复合数据类型（compound data types）入门](Chapter-12/lesson12.1-introduction-to-compound-data-types.md)）所述，分数由分子和分母共同构成数学对象。

考虑编写公司员工信息管理程序时，可能需要跟踪员工姓名（name）、职位（title）、年龄（age）、员工ID（id）、上级ID（managerId）、工资（wage）、生日年份（birthdayYear）、生日月份（birthdayMonth）、生日日期（birthdayDay）、入职年份（hireYear）、入职月份（hireMonth）、入职日期（hireDay）等属性。

若使用独立变量跟踪这些信息：

```
std::string name;
std::string title;
int age;
int id;
int managerId;
double wage;
int birthdayYear;
int birthdayMonth;
int birthdayDay;
int hireYear;
int hireMonth;
int hireDay;
```

此方法存在明显问题：  
1. 变量间关系不直观（需通过注释或上下文推断）  
2. 需管理12个变量。传递员工信息给函数需12个参数（顺序须正确），导致函数原型和调用混乱  
3. 函数只能返回单个值，无法返回完整员工信息  
4. 新增员工需定义12个新变量（每个需唯一名称），扩展性极差

C++提供两种复合类型解决此类问题：**结构体（struct）**（本章重点）和**类（class）**（后续讲解）。结构体（structure的缩写）是程序定义的数据类型（[13.1 — 程序定义类型（program-defined types）入门](Chapter-13/lesson13.1-introduction-to-program-defined-user-defined-types.md)），可将多个变量捆绑为单一类型。

> **重要提示**  
> 结构体（struct）属于类类型（class type），类（class）和联合体（union）同理。类类型的规则均适用于结构体。

定义结构体  
----------------

结构体作为程序定义类型，需先告知编译器其结构：

```
struct Employee
{
    int id {};
    int age {};
    double wage {};
};
```

- `struct`关键字声明结构体类型  
- `Employee`为类型名称（程序定义类型通常首字母大写）  
- 花括号内定义每个Employee对象包含的变量：  
  - `int id`  
  - `int age`  
  - `double wage`  
这些变量称为**数据成员（data members）**或**成员变量（member variables）**。

> **术语解析**  
> 成员（member）指属于结构体（或类）的变量、函数或类型，必须在结构体（或类）定义内声明。

成员变量后的空花括号确保创建Employee时进行值初始化（[1.4 — 变量赋值与初始化（variable assignment and initialization）](Chapter-1/lesson1.4-variable-assignment-and-initialization.md)）。类型定义以分号结束。

定义结构体对象  
----------------

定义Employee类型变量：

```
Employee joe {}; // Employee是类型，joe是变量名
```

代码执行时实例化包含3个数据成员的Employee对象。空花括号确保对象值初始化。可定义多个同类型变量：

```
Employee joe {};  // 创建Joe的Employee结构体
Employee frank {}; // 创建Frank的Employee结构体
```

访问成员  
----------------

通过**成员选择运算符（member selection operator）**（`.`）访问成员变量：

```
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};
    joe.age = 32;  // 使用.运算符选择joe的age成员
    std::cout << joe.age << '\n'; // 输出32
    return 0;
}
```

结构体优势在于每个结构体变量只需一个新名称（成员名称在类型定义中固定）。下例演示两个Employee对象（joe和frank）的操作：

```
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};
    joe.id = 14;
    joe.age = 32;
    joe.wage = 60000.0;

    Employee frank {};
    frank.id = 15;
    frank.age = 28;
    frank.wage = 45000.0;

    int totalAge { joe.age + frank.age };
    std::cout << "Joe和Frank总年龄：" << totalAge << "岁\n";

    if (joe.wage > frank.wage)
        std::cout << "Joe薪资高于Frank\n";
    else if (joe.wage < frank.wage)
        std::cout << "Joe薪资低于Frank\n";
    else
        std::cout << "Joe与Frank薪资相同\n";

    // Frank晋升加薪
    frank.wage += 5000.0;

    // Joe生日年龄+1
    ++joe.age;

    return 0;
}
```

此例清晰区分各成员变量归属，相比独立变量更易组织。同结构类型的多个变量使用相同成员名称，保证操作一致性。

[下一课 13.8 结构体聚合初始化（struct aggregate initialization）](Chapter-13/lesson13.8-struct-aggregate-initialization.md)  
[返回主页](/)    
[上一课 13.6 作用域枚举（enum classes）](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)