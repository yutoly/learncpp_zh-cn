13.11 — 结构体杂项  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月25日（首次发布于2023年7月21日）  

包含程序定义成员的结构体  
----------------  

在C++中，结构体（struct）和类（class）可以包含其他程序定义类型的成员。实现方式有两种：  

第一种方式是在全局作用域定义程序定义类型，然后将其作为另一个结构体的成员：  

```cpp
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

struct Company
{
    int numberOfEmployees {};
    Employee CEO {}; // Employee是Company结构体的成员
};

int main()
{
    Company myCompany{ 7, { 1, 32, 55000.0 } }; // 嵌套初始化列表初始化Employee
    std::cout << myCompany.CEO.wage << '\n'; // 输出CEO的薪资

    return 0;
}
```  

本例中，我们定义`Employee`结构体，然后将其作为`Company`结构体的成员。初始化`Company`时，可以通过嵌套初始化列表来初始化`Employee`。访问CEO薪资时，只需使用两次成员选择运算符：`myCompany.CEO.wage`。  

第二种方式是将类型嵌套在其他类型内部。若`Employee`仅作为`Company`的组成部分，可将其嵌套在`Company`结构体中：  

```cpp
#include <iostream>

struct Company
{
    struct Employee // 通过Company::Employee访问
    {
        int id{};
        int age{};
        double wage{};
    };

    int numberOfEmployees{};
    Employee CEO{}; // Employee是Company结构体内部的嵌套结构体
};

int main()
{
    Company myCompany{ 7, { 1, 32, 55000.0 } }; // 嵌套初始化列表初始化Employee
    std::cout << myCompany.CEO.wage << '\n'; // 输出CEO的薪资

    return 0;
}
```  

这种嵌套方式更常用于类，我们将在后续课程[15.3 — 嵌套类型（成员类型）](Chapter-15/lesson15.3-nested-types-member-types.md)详细讨论。  

作为所有者的结构体应包含所有者类型成员  
----------------  

在课程[5.9 — std::string_view（第二部分）](Chapter-5/lesson5.9-stdstring_view-part-2.md)中，我们介绍了所有者（owner）与观察者（viewer）的概念。所有者管理自己的数据，控制其销毁时机；观察者查看他人数据，不控制其修改或销毁。  

多数情况下，我们希望结构体（和类）成为其数据的所有者。这带来以下优势：  
* 数据成员在结构体（或类）存在期间保持有效  
* 数据成员的值不会意外改变  

使结构体（或类）成为所有者的最简单方式是确保每个数据成员都是所有者类型（即非观察者、指针或引用）。若结构体或类的所有数据成员均为所有者类型，则其本身自动成为所有者。  

若结构体（或类）包含观察者类型成员，被观察对象可能在观察成员之前销毁。此时结构体将持有悬垂成员，访问该成员会导致未定义行为。  

> **最佳实践**  
> 多数情况下应确保结构体（和类）为所有者。最简单方式是确保每个数据成员均为所有者类型（即非观察者、指针或引用）。  

> **作者提示**  
> 构建安全结构体，避免成员悬垂。  

这正是字符串成员通常使用`std::string`（所有者）而非`std::string_view`（观察者）的原因。以下示例演示此区别：  

```cpp
#include <iostream>
#include <string>
#include <string_view>

struct Owner
{
    std::string name{}; // std::string是所有者
};

struct Viewer
{
    std::string_view name {}; // std::string_view是观察者
};

// getName()返回用户输入的临时std::string
// 该临时对象将在包含函数调用的完整表达式结束时销毁
std::string getName()
{
    std::cout << "Enter a name: ";
    std::string name{};
    std::cin >> name;
    return name;
}

int main()
{
    Owner o { getName() };  // getName()的返回值在初始化后立即销毁
    std::cout << "所有者的姓名是：" << o.name << '\n';  // 正确

    Viewer v { getName() }; // getName()的返回值在初始化后立即销毁
    std::cout << "观察者的姓名是：" << v.name << '\n'; // 未定义行为

    return 0;
}
```  

`getName()`函数返回用户输入的临时`std::string`，该临时返回值在函数调用的完整表达式结束时销毁。  

对于`o`对象，该临时`std::string`用于初始化`o.name`。由于`o.name`是`std::string`类型，会复制临时对象。临时对象销毁后，`o.name`不受影响。后续输出`o.name`时表现正常。  

对于`v`对象，临时`std::string`用于初始化`v.name`。由于`v.name`是`std::string_view`类型，仅观察临时对象而不复制。临时对象销毁后，`v.name`成为悬垂引用。后续输出`v.name`将导致未定义行为。  

结构体大小与数据结构对齐  
----------------  

通常，结构体大小等于各成员大小之和，但并非总是如此！  

考虑以下程序：  

```cpp
#include <iostream>

struct Foo
{
    short a {};
    int b {};
    double c {};
};

int main()
{
    std::cout << "short的大小：" << sizeof(short) << "字节\n";
    std::cout << "int的大小：" << sizeof(int) << "字节\n";
    std::cout << "double的大小：" << sizeof(double) << "字节\n";

    std::cout << "Foo的大小：" << sizeof(Foo) << "字节\n";

    return 0;
}
```  

在作者机器上输出：  

```
short的大小：2字节
int的大小：4字节
double的大小：8字节
Foo的大小：16字节
```  

注意`short`+`int`+`double`总大小为14字节，但`Foo`大小为16字节！  

实际上，结构体大小*至少*等于其成员大小之和，但可能更大。出于性能考虑，编译器有时会在结构体中插入间隙（称为填充（padding））。  

上述`Foo`结构体中，编译器在成员`a`后隐式添加2字节填充，使结构体大小变为16字节而非14字节。  

> **进阶阅读**  
> 编译器添加填充的原因超出本教程范围，有兴趣的读者可参阅维基百科[数据结构对齐](https://en.wikipedia.org/wiki/Data_structure_alignment)。此为选读内容，不影响对结构体或C++的理解。  

填充可能显著影响结构体大小，如下例所示：  

```cpp
#include <iostream>

struct Foo1
{
    short a{}; // a后有2字节填充
    int b{};
    short c{}; // c后有2字节填充
};

struct Foo2
{
    int b{};
    short a{};
    short c{};
};

int main()
{
    std::cout << sizeof(Foo1) << '\n'; // 输出12
    std::cout << sizeof(Foo2) << '\n'; // 输出8

    return 0;
}
```  

程序输出：  

```
12
8
```  

注意`Foo1`和`Foo2`成员相同，仅声明顺序不同。但由于填充差异，`Foo1`比`Foo2`大50%。  

> **技巧**  
> 按成员大小降序排列可最小化填充。  
> C++编译器不能重排成员，需手动调整顺序。  

[下一课 13.12 — 通过指针和引用进行成员选择](Chapter-13/lesson13.12-member-selection-with-pointers-and-references.md)  
[返回主页](/)  
[上一课 13.10 — 结构体的传递与返回](Chapter-13/lesson13.10-passing-and-returning-structs.md)