13.8 — 结构体的聚合初始化  
=======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年1月18日上午10:24（PST）  
2025年1月6日  

在上一课（[13.7 — 结构体、成员与成员选择简介](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)）中，我们讨论了如何定义结构体、实例化结构体对象及访问其成员。本课将探讨结构体的初始化方式。  

数据成员的默认初始化问题  
----------------  

与普通变量类似，数据成员默认不进行初始化。考虑以下结构体：  
```cpp
#include <iostream>

struct Employee
{
    int id;  // 注意：此处无初始化器
    int age;
    double wage;
};

int main()
{
    Employee joe;  // 注意：此处也无初始化器
    std::cout << joe.id << '\n';

    return 0;
}
```  
由于未提供初始化器，当`joe`实例化时，`joe.id`、`joe.age`和`joe.wage`均处于未初始化状态。尝试打印`joe.id`时将产生未定义行为。  

在讲解结构体初始化方法前，我们先做概念澄清。  

何为聚合？  
----------------  

在编程领域，**聚合数据类型（aggregate data type）**（亦称**聚合体（aggregate）**）指可包含多个数据成员的类型。某些聚合体允许成员类型不同（如结构体），另一些要求成员类型统一（如数组）。  

在C++中，聚合的定义更为严格且复杂。  

> **作者说明**  
> 本系列教程中使用的"聚合"（或"非聚合"）术语均指C++标准定义。  

> **进阶阅读**  
> 简而言之，C++中的聚合体指：  
> * C风格数组（[17.7 — C风格数组简介](Chapter-17/lesson17.7-introduction-to-c-style-arrays.md)）  
> * 满足以下条件的类类型（结构体、类或联合体）：  
>   - 无用户声明构造函数（[14.9 — 构造函数简介](Chapter-14/lesson14.9-introduction-to-constructors.md)）  
>   - 无非静态私有或受保护数据成员（[14.5 — 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)）  
>   - 无虚函数（[25.2 — 虚函数与多态](Chapter-25/lesson25.2-virtual-functions.md)）  
>  
> 常用类型`std::array`（[17.1 — std::array简介](Chapter-17/lesson17.1-introduction-to-stdarray.md)）也属聚合体。  
>  
> 完整C++聚合定义参见[此处](https://en.cppreference.com/w/cpp/language/aggregate_initialization)。  

当前阶段需理解：仅含数据成员的结构体属于聚合体。  

结构体的聚合初始化  
----------------  

普通变量只能保存单个值，因此只需单个初始化器：  
```cpp
int x { 5 };
```  
而结构体可包含多个成员：  
```cpp
struct Employee
{
    int id {};
    int age {};
    double wage {};
};
```  
定义结构体类型对象时，需要初始化多个成员：  
```cpp
Employee joe; // 如何初始化joe.id、joe.age和joe.wage？
```  
聚合体使用**聚合初始化**方式，允许直接初始化成员。通过**初始化列表**（花括号包裹的逗号分隔值列表）实现。  

聚合初始化主要有两种形式：  
```cpp
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee frank = { 1, 32, 60000.0 }; // 使用花括号列表进行拷贝列表初始化
    Employee joe { 2, 28, 45000.0 };     // 使用花括号列表进行列表初始化（推荐）

    return 0;
}
```  
这两种形式均执行**成员逐一初始化**，即按声明顺序初始化结构体成员。例如`Employee joe { 2, 28, 45000.0 };`首先将`joe.id`初始化为`2`，接着`joe.age`为`28`，最后`joe.wage`为`45000.0`。  

> **最佳实践**  
> 初始化聚合体时优先使用（非拷贝）花括号列表形式。  

在C++20中，也可使用圆括号列表初始化聚合体：  
```cpp
    Employee robert ( 3, 45, 62500.0 );  // 使用圆括号列表直接初始化（C++20）
```  
建议尽量避免此形式，因其目前不支持使用大括号省略的聚合体（如`std::array`）。  

初始化列表中的缺失值  
----------------  

若初始化值数量少于成员数量，未显式初始化的成员按以下规则处理：  
* 有默认成员初始化器则使用该值  
* 否则从空初始化器列表进行拷贝初始化（通常执行值初始化，类类型调用默认构造函数）  

```cpp
struct Employee
{
    int id {};
    int age {};
    double wage { 76000.0 };
    double whatever;
};

int main()
{
    Employee joe { 2, 28 }; // joe.whatever将被值初始化为0.0
    return 0;
}
```  
本例中，`joe.id`初始化为`2`，`joe.age`为`28`。`joe.wage`因有默认成员初始化器，初始化为`76000.0`。`joe.whatever`未显式初始化，值初始化为`0.0`。  

> **提示**  
> 可使用空初始化列表对所有成员进行值初始化：  
> ```cpp
> Employee joe {}; // 值初始化所有成员
> ```  

重载operator<<输出结构体  
----------------  

在课程[13.5 — I/O运算符重载简介](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md)中，我们展示了如何重载`operator<<`输出枚举类型。同样可为结构体重载该运算符：  
```cpp
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

std::ostream& operator<<(std::ostream& out, const Employee& e)
{
    out << e.id << ' ' << e.age << ' ' << e.wage;
    return out;
}

int main()
{
    Employee joe { 2, 28 }; // joe.wage将值初始化为0.0
    std::cout << joe << '\n';
    return 0;
}
```  
输出：  
```
2 28 0
```  
可见`joe.wage`确实被值初始化为`0.0`。  

与枚举不同，结构体可包含多个值。输出格式完全自定义。例如增强输出可读性：  
```cpp
std::ostream& operator<<(std::ostream& out, const Employee& e)
{
    out << "id: " << e.id << " age: " << e.age << " wage: " << e.wage;
    return out;
}
```  
输出：  
```
id: 2 age: 28 wage: 0
```  

常量结构体  
----------------  

结构体类型变量可为const或constexpr，与所有const变量相同，必须初始化：  
```cpp
struct Rectangle
{
    double length {};
    double width {};
};

int main()
{
    const Rectangle unit { 1.0, 1.0 };
    const Rectangle zero { }; // 值初始化所有成员
    return 0;
}
```  

指定初始化器（C++20）  
----------------  

使用值列表初始化结构体时，初始化器按成员声明顺序应用：  
```cpp
struct Foo
{
    int a {};
    int c {};
};

int main()
{
    Foo f { 1, 3 }; // f.a = 1, f.c = 3
    return 0;
}
```  
若在结构体定义中间新增成员：  
```cpp
struct Foo
{
    int a {};
    int b {}; // 新增成员
    int c {};
};

int main()
{
    Foo f { 1, 3 }; // 现为f.a = 1, f.b = 3, f.c = 0
    return 0;
}
```  
初始化值顺序发生偏移，且编译器可能不报错。  

C++20引入**指定初始化器**，显式定义初始化值与成员的映射关系。支持列表或拷贝初始化，必须按声明顺序初始化成员，否则产生警告或错误。未指定成员执行值初始化。  
```cpp
struct Foo
{
    int a{ };
    int b{ };
    int c{ };
};

int main()
{
    Foo f1{ .a{ 1 }, .c{ 3 } }; // 正确：f1.a = 1, f1.b = 0, f1.c = 3
    Foo f2{ .a = 1, .c = 3 };   // 正确：f2.a = 1, f2.b = 0, f2.c = 3
    Foo f3{ .b{ 2 }, .a{ 1 } }; // 错误：初始化顺序与声明顺序不符
    return 0;
}
```  
Clang用户注意：使用大括号进行单值指定初始化时，可能误报"braces around scalar initializer"警告。  

指定初始化器虽增强自文档性，但会使初始化列表冗长，暂不作为最佳实践推荐。同时为避免初始化顺序问题，新增成员应置于定义列表末尾。  

> **最佳实践**  
> 向聚合体添加新成员时，应置于定义列表底部以防止初始化值偏移。  

使用初始化列表赋值  
----------------  

可通过成员逐一赋值更新结构体：  
```cpp
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 32, 60000.0 };
    joe.age  = 33;      // Joe生日
    joe.wage = 66000.0; // 加薪
    return 0;
}
```  
此方式适用于单成员修改，但批量更新时更推荐初始化列表成员逐一赋值：  
```cpp
joe = { joe.id, 33, 66000.0 }; // 使用当前id作为占位符
```  
需注意保留不想修改的成员当前值作为占位符。  

使用指定初始化器赋值（C++20）  
----------------  
```cpp
joe = { .id = joe.id, .age = 33, .wage = 66000.0 };
```  
未指定的成员将进行值初始化。若未指定`joe.id`，其将被赋值为0。  

使用同类型结构体初始化  
----------------  
```cpp
#include <iostream>

struct Foo
{
    int a{};
    int b{};
    int c{};
};

std::ostream& operator<<(std::ostream& out, const Foo& f)
{
    out << f.a << ' ' << f.b << ' ' << f.c;
    return out;
}

int main()
{
    Foo foo { 1, 2, 3 };

    Foo x = foo; // 拷贝初始化
    Foo y(foo);  // 直接初始化
    Foo z {foo}; // 直接列表初始化

    std::cout << x << '\n' << y << '\n' << z << '\n';
    return 0;
}
```  
输出均为`1 2 3`。此方式使用标准初始化形式（拷贝/直接/直接列表初始化），而非聚合初始化。常见于用函数返回的同类型结构体初始化对象，详见[13.10 — 结构体的传递与返回](Chapter-13/lesson13.10-passing-and-returning-structs.md)。  

[下一课 13.9 默认成员初始化](Chapter-13/lesson13.9-default-member-initialization.md)  
[返回主页](/)  
[
[上一课 13.7 结构体、成员与成员选择简介](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)