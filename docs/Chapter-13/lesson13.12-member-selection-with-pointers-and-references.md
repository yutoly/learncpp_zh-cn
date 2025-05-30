13.12 -- 指针和引用的成员选择  
======================================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2007年7月17日 上午11:40 PDT  
2024年7月2日  

结构体与结构体引用的成员选择  
----------------  

在课程[13.7 -- 结构体、成员与成员选择](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)中，我们展示了可通过成员选择运算符(.)从结构体对象中选择成员：  

```cpp
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 34, 65000.0 };

    // 使用成员选择运算符(.)从结构体对象选择成员
    ++joe.age; // Joe过了生日
    joe.wage = 68000.0; // Joe升职了
    
    return 0;
}
```  

由于对象的引用行为与对象本身一致，我们同样可用成员选择运算符(.)从结构体引用中选择成员：  

```cpp
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

void printEmployee(const Employee& e)
{
    // 使用成员选择运算符(.)从结构体引用选择成员
    std::cout << "Id: " << e.id << '\n';
    std::cout << "Age: " << e.age << '\n';
    std::cout << "Wage: " << e.wage << '\n';
}

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    printEmployee(joe);

    return 0;
}
```  

指向结构体的指针成员选择  
----------------  

但成员选择运算符(.)不能直接用于指向结构体的指针：  

```cpp
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << ptr.id << '\n'; // 编译错误：不能对指针使用运算符.

    return 0;
}
```  

使用普通变量或引用时可直接访问对象。但指针存储的是地址，需先解引用指针获取对象才能操作。因此访问结构体指针成员的一种方式如下：  

```cpp
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << (*ptr).id << '\n'; // 可行但不优雅：先解引用ptr，再用成员选择

    return 0;
}
```  

此语法较繁琐，尤其需用括号确保解引用操作优先于成员选择操作。  

为简化语法，C++提供了**指针成员选择运算符(->)**（亦称**箭头运算符(arrow operator)**），用于从对象指针选择成员：  

```cpp
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << ptr->id << '\n'; // 更佳：使用->从对象指针选择成员

    return 0;
}
```  

此指针成员选择运算符(->)与成员选择运算符(.)功能相同，但会隐式解引用指针对象再选择成员。因此`ptr->id`等价于`(*ptr).id`。  

箭头运算符不仅输入更简便，且不易出错——解引用由编译器隐式完成，无需考虑优先级问题。故通过指针访问成员时，始终应使用->而非.运算符。  

> **最佳实践**  
> 通过指针访问成员时，始终使用指针成员选择运算符(->)而非成员选择运算符(.)。  

链式调用`operator->`  
----------------  

若通过`operator->`访问的成员本身是指向类类型的指针，可在同表达式再次应用`operator->`访问该类的成员。  

下例演示此用法（由读者Luna提供）：  

```cpp
#include <iostream>

struct Point
{
    double x {};
    double y {};
};

struct Triangle
{
    Point* a {};
    Point* b {};
    Point* c {};
};

int main()
{
    Point a {1,2};
    Point b {3,7};
    Point c {10,2};

    Triangle tr { &a, &b, &c };
    Triangle* ptr {&tr};

    // ptr是指向Triangle的指针，其成员又是指向Point的指针
    // 访问ptr所指Triangle中c点的y成员，以下方式等价：

    // 通过运算符.访问
    std::cout << (*(*ptr).c).y << '\n'; // 繁琐！

    // 通过运算符->访问
    std::cout << ptr -> c -> y << '\n'; // 更清晰
}
```  

连续使用多个`operator->`时（如`ptr->c->y`），表达式可能难读。在成员与`operator->`间添加空格（如`ptr -> c -> y`）可提升可读性。  

混合指针与非指针成员访问  
----------------  

成员选择运算符始终作用于当前选定变量。若混合指针与普通成员变量，可见到.和->连用的成员选择：  

```cpp
#include <iostream>
#include <string>

struct Paw
{
    int claws{};
};
 
struct Animal
{
    std::string name{};
    Paw paw{};
};
 
int main()
{
    Animal puma{ "Puma", { 5 } };
 
    Animal* ptr{ &puma };
 
    // ptr是指针，使用->
    // paw非指针，使用.

    std::cout << (ptr->paw).claws << '\n';
 
    return 0;
}
```  

注意`(ptr->paw).claws`中括号非必需（因`operator->`和`operator.`均从左向右求值），但能略微提升可读性。  

[下一课 13.13 类模板](Chapter-13/lesson13.13-class-templates.md)  
[返回主页](/)  
[上一课 13.11 结构体杂项](Chapter-13/lesson13.11-struct-miscellany.md)