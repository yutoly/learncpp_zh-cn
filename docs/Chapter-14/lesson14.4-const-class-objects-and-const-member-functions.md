14.4 — 常量类对象与常量成员函数  
======================================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月12日（首次发布于2007年9月11日）  

在课程[5.1 — 常量变量（命名常量）](Chapter-5/lesson5.1-constant-variables-named-constants.md)中，我们学习了基础数据类型（`int`、`double`、`char`等）的对象可以通过`const`关键字设为常量。所有常量变量必须在创建时初始化。  
```
const int x;      // 编译错误：未初始化
const int y{};    // 正确：值初始化
const int z{ 5 }; // 正确：列表初始化
```  
类似地，类类型对象（结构体、类、联合体）也可通过`const`关键字设为常量。此类对象同样必须在创建时初始化。  
```
struct Date
{
    int year {};
    int month {};
    int day {};
};

int main()
{
    const Date today { 2020, 10, 14 }; // 常量类类型对象

    return 0;
}
```  
与普通变量类似，当需要确保类类型对象在创建后不被修改时，通常应将其设为常量（或常量表达式）。  

**禁止修改常量对象的数据成员**  
一旦常量类类型对象完成初始化，任何修改对象数据成员的尝试都将被禁止，因为这违反对象的常量性。这包括直接修改公有成员变量，或调用设置成员变量值的成员函数。  
```
struct Date
{
    int year {};
    int month {};
    int day {};

    void incrementDay()
    {
        ++day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // 常量

    today.day += 1;        // 编译错误：不能修改常量对象的成员
    today.incrementDay();  // 编译错误：不能调用会修改常量对象成员的成员函数

    return 0;
}
```  

**常量对象不能调用非常量成员函数**  
以下代码同样会导致编译错误：  
```
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print()
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // 常量

    today.print();  // 编译错误：不能调用非常量成员函数

    return 0;
}
```  
尽管`print()`并未尝试修改成员变量，但调用`today.print()`仍违反常量性规则。这是因为`print()`成员函数本身未声明为常量。编译器不允许在常量对象上调用非常量成员函数。  

**常量成员函数（const member functions）**  
为解决上述问题，我们需要将`print()`设为常量成员函数。**常量成员函数**是保证不修改对象且不调用任何非常量成员函数（可能修改对象）的成员函数。  

将`print()`设为常量成员函数很简单——只需在函数原型参数列表后、函数体前添加`const`关键字：  
```
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // 现为常量成员函数
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // 常量

    today.print();  // 正确：常量对象可调用常量成员函数

    return 0;
}
```  
在上例中，`print()`已成为常量成员函数，这意味着我们可以在常量对象（如`today`）上调用它。  

**进阶阅读**  
对于在类定义外定义的成员函数，`const`关键字需同时用于类定义中的函数声明和类外函数定义。示例见课程[15.2 — 类与头文件](Chapter-15/lesson15.2-classes-and-header-files.md)。  

构造函数不能设为常量，因其需要初始化对象成员（需修改成员）。构造函数详见课程[14.9 — 构造函数简介](Chapter-14/lesson14.9-introduction-to-constructors.md)。  

**尝试修改数据成员的常量成员函数会导致编译错误**  
例如：  
```
struct Date
{
    int year {};
    int month {};
    int day {};

    void incrementDay() const // 设为常量
    {
        ++day; // 编译错误：常量函数不能修改成员
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // 常量

    today.incrementDay();

    return 0;
}
```  
本例中，`incrementDay()`被标记为常量成员函数，但试图修改`day`，将导致编译错误。  

**常量成员函数可以修改非成员对象**  
常量成员函数可正常修改非成员对象（如局部变量和函数参数）并调用非成员函数。`const`仅作用于类成员。  

**关键洞察**  
常量成员函数不可以：  
* 修改隐式对象  
* 调用非常量成员函数  

常量成员函数可以：  
* 修改非隐式对象  
* 调用常量成员函数  
* 调用非成员函数  

**常量成员函数可在非const对象上调用**  
常量成员函数也可在非const对象上调用：  
```
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // 常量
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // 非const

    today.print();  // 正确：可在非const对象上调用常量成员函数

    return 0;
}
```  
由于常量成员函数可在const和非const对象上调用，若成员函数不修改对象状态，应设为常量。  

**最佳实践**  
不修改（且永远不会修改）对象状态的成员函数应设为常量，以便在const和非const对象上均可调用。  

注意`const`的应用对象。一旦成员函数设为常量，该函数即可在const对象上调用。后续移除成员函数的`const`限定将破坏在const对象上调用该函数的所有代码。  

**通过常量引用传递的const对象**  
虽然实例化const局部变量是创建const对象的一种方式，但更常见的方式是通过常量引用（pass by const reference）将对象传递给函数。  

在课程[12.5 — 左值引用传递](Chapter-12/lesson12.5-pass-by-lvalue-reference.md)中，我们讨论了通过const引用而非值传递类类型参数的优势。简言之，按值传递类类型参数会创建副本（效率低）——多数情况下我们不需要副本，对原参数的引用即可正常工作且避免复制。通常将引用设为const以允许函数接受const左值参数和右值参数（如字面量和临时对象）。  

**以下代码有何问题？**  
```
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() // 非常量
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

void doSomething(const Date& date)
{
    date.print();
}

int main()
{
    Date today { 2020, 10, 14 }; // 非const
    today.print();

    doSomething(today);

    return 0;
}
```  
答案：在`doSomething()`函数内部，`date`被视为const对象（因其通过const引用传递）。对于这个const `date`，我们调用了非常量成员函数`print()`。由于不能在const对象上调用非常量成员函数，将导致编译错误。  

修复方法很简单：将`print()`设为const：  
```
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // 现为const
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

void doSomething(const Date& date)
{
    date.print();
}

int main()
{
    Date today { 2020, 10, 14 }; // 非const
    today.print();

    doSomething(today);

    return 0;
}
```  
现在在函数`doSomething()`中，const `date`将能成功调用const成员函数`print()`。  

**成员函数的常量与非常量重载**  
最后，虽然不常见，但可以重载成员函数以提供同一函数的const和非常量版本。这是因为const限定符被视为函数签名的一部分，因此仅在const性上不同的两个函数被视为不同函数。  
```
#include <iostream>

struct Something
{
    void print()
    {
        std::cout << "非常量\n";
    }

    void print() const
    {
        std::cout << "常量\n";
    }
};

int main()
{
    Something s1{};
    s1.print(); // 调用print()

    const Something s2{};
    s2.print(); // 调用print() const
    
    return 0;
}
```  
输出：  
```
非常量
常量
```  
为函数重载const和非常量版本通常在返回值需要不同常量性时使用，这种情况较为罕见。  

[下一课14.5 — 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)  
[返回主页](/)  
[
[上一课14.3 — 成员函数](Chapter-14/lesson14.3-member-functions.md)