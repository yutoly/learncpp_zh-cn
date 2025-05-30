14.3 — 成员函数（Member functions）
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年8月30日（首次发布于2007年8月30日）  
2025年2月10日更新  

在课程[13.7 — 结构体、成员与成员选择简介](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)中，我们介绍了包含成员变量的结构体（struct）类型。以下是用于保存日期的结构体示例：
```
struct Date
{
    int year {};
    int month {};
    int day {};
};
```
若希望将日期打印到屏幕（这可能是常用操作），编写专门函数实现该功能是合理的。完整示例如下：
```
#include <iostream>

struct Date
{
    // 成员变量
    int year {};
    int month {};
    int day {};
};

void print(const Date& date)
{
    // 通过成员选择运算符（.）访问成员变量
    std::cout << date.year << '/' << date.month << '/' << date.day;
}

int main()
{
    Date today { 2020, 10, 14 }; // 聚合初始化结构体

    today.day = 16; // 使用成员选择运算符（.）访问成员变量
    print(today);   // 使用常规调用方式访问非成员函数

    return 0;
}
```
该程序输出：
```
2020/10/16

```
属性与行为的分离  
观察周围环境——所有事物都是对象：书籍、建筑、食物，甚至你自己。真实对象包含两大要素：  
1. 可观察属性（如重量、颜色、尺寸、硬度、形状等）  
2. 基于属性的可执行行为或被施加行为（如被打开、损坏其他物体等）  

在编程中，我们用变量表示属性，用函数表示行为。  

在上例中，`Date`的属性（成员变量）与相关行为（`print()`函数）是分离的。我们只能通过`print()`的`const Date&`参数推断其与`Date`的关联。虽然可将`Date`和`print()`放入命名空间（以明确两者关联），但这会增加程序命名数量和命名空间前缀，使代码更冗长。  

成员函数（Member functions）  
类类型（包括struct、class和union）除了成员变量外，还可以拥有自己的函数！属于类类型的函数称为**成员函数**。  

> **术语说明**  
> 其他面向对象语言（如Java和C#）中称为**方法（methods）**。虽然C++不使用该术语，但来自这些语言的开发者可能仍沿用该称呼。  

非成员函数称为**非成员函数（non-member functions）**或**自由函数（free functions）**。上例中的`print()`即为非成员函数。  

> **作者提示**  
> 本节使用struct演示成员函数，但所有内容同样适用于class。后续课程[14.5 — 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)将展示class的成员函数示例。  

成员函数必须在类类型定义内声明，可在类内或类外定义。目前我们仅在类内定义成员函数以保持简单。  

> **相关内容**  
> 类外定义成员函数详见课程[15.2 — 类与头文件](Chapter-15/lesson15.2-classes-and-header-files.md)。  

成员函数示例  
将`print()`从非成员函数转换为成员函数的重写示例：
```
// 成员函数版本
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() // 定义名为print的成员函数
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // 聚合初始化结构体

    today.day = 16; // 使用成员选择运算符访问成员变量
    today.print();  // 使用成员选择运算符调用成员函数

    return 0;
}
```
该程序输出结果与之前相同：
```
2020/10/16

```
主要差异体现在三方面：  
1. `print()`函数的声明与定义位置  
2. `print()`的调用方式  
3. `print()`内部访问成员的方式  

成员函数的声明位置  
在非成员示例中，`print()`函数定义于全局命名空间。默认具有外部链接，可被其他源文件调用。  

在成员示例中，`print()`声明（并定义）于`Date`结构体内。类内定义的成员函数隐式内联，不会违反单一定义规则。  

> **相关内容**  
> 成员函数可在类内声明并在类外定义，详见课程[15.2 — 类与头文件](Chapter-15/lesson15.2-classes-and-header-files.md)。  

调用成员函数与隐式对象（implicit object）  
非成员版本调用形式为`print(today)`，显式传递参数。成员版本调用形式为`today.print()`，通过成员选择运算符调用，与访问成员变量的语法一致。  

所有（非静态）成员函数必须通过类类型对象调用。此时`today`即为**隐式对象**，被隐式传递给`print()`函数。  

成员访问机制  
非成员函数版本中，通过引用参数`date`访问成员：
```
// 非成员版本print
void print(const Date& date)
{
    std::cout << date.year << '/' << date.month << '/' << date.day;
}
```
成员函数版本中，直接访问成员变量：
```
void print()
{
    std::cout << year << '/' << month << '/' << day;
}
```
成员函数内未加前缀的成员标识符均关联隐式对象。当调用`today.print()`时，`year`等价于`today.year`。  

> **关键洞察**  
> 非成员函数需显式传递对象并通过该对象访问成员，成员函数则隐式传递对象并隐式访问成员。  

进阶成员函数示例  
以下示例展示更复杂的成员函数：
```
#include <iostream>
#include <string>

struct Person
{
    std::string name{};
    int age{};

    void kisses(const Person& person)
    {
        std::cout << name << " kisses " << person.name << '\n';
    }
};

int main()
{
    Person joe{ "Joe", 29 };
    Person kate{ "Kate", 27 };

    joe.kisses(kate);

    return 0;
}
```
输出：
```
Joe kisses Kate

```
调用`joe.kisses(kate)`时，`joe`为隐式对象，`name`解析为`joe.name`，`person.name`解析为`kate.name`。  

> **关键洞察**  
> 非成员函数调用形式为`kisses(joe, kate)`，成员函数形式为`joe.kisses(kate)`，后者更清晰表明动作发起者。  

成员变量与函数的声明顺序  
类定义内可任意顺序声明成员变量和函数，编译器通过以下机制实现：  
1. 遇到类内定义的成员函数时隐式前向声明  
2. 将函数定义移至类定义之后  

例如：
```
struct Foo
{
    int z() { return m_data; } // 可访问尚未声明的数据成员
    int x() { return y(); }    // 可访问尚未声明的成员函数
    int m_data{ y() };         // 默认成员初始化器中亦可访问（见警告）
    int y() { return 5; }
};
```
等效编译为：
```
struct Foo
{
    int z();
    int x();
    int y();
    int m_data{};
};

int Foo::z() { return m_data; }
int Foo::x() { return y(); }
int Foo::y() { return 5; }
```

> **警告**  
> 数据成员按声明顺序初始化。若初始化时访问后续声明的成员，将导致未定义行为：
```
struct Bad
{
    int m_bad1 { m_data }; // 未定义行为：m_bad1在m_data前初始化
    int m_bad2 { fcn() };  // 未定义行为：m_bad2在m_data前初始化

    int m_data { 5 };
    int fcn() { return m_data; }
};
```
建议避免在默认成员初始化器中使用其他成员。  

成员函数重载  
与普通函数类似，成员函数可重载，只要各版本可区分。  

`Date`结构体重载`print()`示例：
```
#include <iostream>
#include <string_view>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print()
    {
        std::cout << year << '/' << month << '/' << day;
    }

    void print(std::string_view prefix)
    {
        std::cout << prefix << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 };

    today.print();            // 调用Date::print()
    std::cout << '\n';

    today.print("日期：");    // 调用Date::print(std::string_view)
    std::cout << '\n';

    return 0;
}
```
输出：
```
2020/10/14
日期：2020/10/14

```
结构体与成员函数  
C语言中结构体仅有数据成员。C++设计时决定让struct拥有与class统一的能力，但约定struct应保持聚合类型特性。  

> **最佳实践**  
> struct和class均可使用成员函数，但struct应避免定义构造函数（会失去聚合类型特性）。  

无数据成员的类类型  
可创建仅有成员函数的类类型：
```
#include <iostream>

struct Foo
{
    void printHi() { std::cout << "Hi!\n"; }
};

int main()
{
    Foo f{};
    f.printHi(); // 需要对象调用

    return 0;
}
```
但若无数据成员，建议改用命名空间：
```
#include <iostream>

namespace Foo
{
    void printHi() { std::cout << "Hi!\n"; }
};

int main()
{
    Foo::printHi(); // 无需对象

    return 0;
}
```
> **最佳实践**  
> 无数据成员的类类型建议改用命名空间。  

测验时间  
**问题1**  
创建包含两个整数的`IntPair`结构体，添加打印函数：
```
#include <iostream>

struct IntPair
{
    int first{};
    int second{};

    void print()
    {
        std::cout << "Pair(" << first << ", " << second << ")\n";
    }
};

int main()
{
    IntPair p1 {1, 2};
    IntPair p2 {3, 4};

    p1.print();
    p2.print();

    return 0;
}
```

**问题2**  
为`IntPair`添加判断相等的成员函数：
```
#include <iostream>

struct IntPair
{
    int first{};
    int second{};

    void print() { /* 同上 */ }

    bool isEqual(IntPair a)
    {
        return first == a.first && second == a.second;
    }
};

int main()
{
    IntPair p1 {1, 2};
    IntPair p2 {3, 4};

    std::cout << std::boolalpha;
    p1.isEqual(p1); // true
    p1.isEqual(p2); // false

    return 0;
}
```

[下一课 14.4 — const类对象与const成员函数](Chapter-14/lesson14.4-const-class-objects-and-const-member-functions.md)  
[返回主页](/)  
[上一课 14.2 — 类简介](Chapter-14/lesson14.2-introduction-to-classes.md)