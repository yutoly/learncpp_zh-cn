7.6 — 内部链接  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月30日（首次发布于2020年1月3日）  

在课程[7.3 — 局部变量](Chapter-7/lesson7.3-local-variables.md)中我们提到："标识符的链接属性（linkage）决定了其他同名声明是否指向同一实体"，并讨论了局部变量具有`无链接（no linkage）`的特性。

全局变量和函数标识符可具有`内部链接（internal linkage）`或`外部链接（external linkage）`。本节讨论内部链接情形，外部链接将在课程[7.7 — 外部链接与变量前向声明](Chapter-7/lesson7.7-external-linkage-and-variable-forward-declarations.md)中讲解。

具有**内部链接**的标识符在单个翻译单元（translation unit）内可见且可用，但无法被其他翻译单元访问。这意味着若两个源文件存在同名内部链接标识符，这些标识符将被视为独立实体（不会因重复定义引发ODR违规）。

> **关键洞察**  
> 具有内部链接的标识符可能对链接器完全不可见。或者虽然可见，但被标记为仅限特定翻译单元使用。

> **相关内容**  
> 翻译单元概念详见课程[2.10 — 预处理器简介](Chapter-2/lesson2.10-introduction-to-the-preprocessor.md)。

具有内部链接的全局变量  
----------------

具有内部链接的全局变量有时称为**内部变量**。

要将非常量全局变量设为内部链接，需使用`static`关键字：

```cpp
#include <iostream>

static int g_x{}; // 非常量全局变量默认具有外部链接，可通过static关键字赋予内部链接

const int g_y{ 1 }; // const全局变量默认具有内部链接
constexpr int g_z{ 2 }; // constexpr全局变量默认具有内部链接

int main()
{
    std::cout << g_x << ' ' << g_y << ' ' << g_z << '\n';
    return 0;
}
```

const和constexpr全局变量默认具有内部链接（因此无需`static`关键字——若使用将被忽略）。

以下示例演示多文件使用内部变量：

a.cpp：

```cpp
[[maybe_unused]] constexpr int g_x { 2 }; // 该内部g_x仅在a.cpp中可访问
```

main.cpp：

```cpp
#include <iostream>

static int g_x { 3 }; // 该独立内部g_x仅在main.cpp中可访问

int main()
{
    std::cout << g_x << '\n'; // 使用main.cpp的g_x，输出3
    return 0;
}
```

程序输出：

```
3
```

由于每个文件的`g_x`均为内部变量，`main.cpp`不会感知`a.cpp`的同名变量（反之亦然）。

> **进阶阅读**  
> 上文使用的`static`关键字属于**存储类说明符（storage class specifier）**，同时设置名称的链接属性和存储期。常用存储类说明符包括`static`、`extern`和`mutable`。该术语主要用于技术文档。

> **进阶阅读**  
> C++11标准（附录C）解释了const变量默认内部链接的设计考量："由于C++中const对象可用作编译期值，此特性促使程序员为每个const变量提供显式初始值，并允许将const对象置于被多个编译单元包含的头文件中。"  
>  
> C++设计者的意图是：  
> 1. const对象应可用于常量表达式。为此编译器必须见到定义（而非声明）以便在编译期求值  
> 2. const对象应能通过头文件传播  
>  
> 具有外部链接的对象只能在单个翻译单元定义而不违反ODR（单一定义规则），其他翻译单元必须通过前向声明访问。若const对象默认外部链接，则只能在定义它们的翻译单元中用于常量表达式，且无法通过头文件有效传播（多次包含会引发ODR违规）。  
>  
> 具有内部链接的对象可在需要它们的每个翻译单元定义而不违反ODR。这使得const对象可置于头文件中并被任意数量翻译单元包含。由于每个翻译单元都有定义而非声明，这保证了这些常量可用于本单元的常量表达式。  
>  
> 直到C++17才引入内联变量（具有外部链接而不引发ODR违规）。

具有内部链接的函数  
----------------

如前所述，函数标识符也具有链接属性。函数默认具有外部链接（下节讨论），但可通过`static`关键字设为内部链接：

add.cpp：

```cpp
// 该函数声明为static，仅限本文件使用
// 通过函数前向声明从其他文件访问将失败
[[maybe_unused]] static int add(int x, int y)
{
    return x + y;
}
```

main.cpp：

```cpp
#include <iostream>

int add(int x, int y); // 函数add的前向声明

int main()
{
    std::cout << add(3, 4) << '\n';
    return 0;
}
```

该程序无法链接，因`add`函数在`add.cpp`外不可访问。

单一定义规则与内部链接  
----------------

在课程[2.7 — 前向声明与定义](Chapter-2/lesson2.7-forward-declarations.md)中我们提到，单一定义规则（ODR）规定对象或函数在文件或程序中不可有多个定义。

需注意，不同文件中定义的内部对象（及函数）被视为独立实体（即使名称类型相同），因此不违反ODR。每个内部对象仅有一个定义。

static与未命名命名空间  
----------------

现代C++中，使用`static`关键字赋予标识符内部链接的做法逐渐式微。未命名命名空间（unnamed namespaces）能为更多类型标识符（如类型标识符）赋予内部链接，更适用于需要内部链接的多个标识符。

未命名命名空间详见课程[7.14 — 未命名与内联命名空间](Chapter-7/lesson7.14-unnamed-and-inline-namespaces.md)。

为何赋予标识符内部链接？  
----------------

通常有两个原因：  
1. 需要确保某标识符不被其他文件访问（如不想被修改的全局变量，或禁止调用的辅助函数）  
2. 严谨避免命名冲突。因内部链接标识符不暴露给链接器，仅可能在同一翻译单元内冲突

许多现代开发指南建议为不供外部使用的所有变量和函数赋予内部链接。若有足够规范意识，这是良好实践。

目前我们建议采用更轻量级方案：仅对明确禁止外部访问的标识符赋予内部链接。

> **最佳实践**  
> 当需要明确禁止其他文件访问时，赋予标识符内部链接。  
> 考虑为所有不应被外部访问的标识符赋予内部链接（使用未命名命名空间实现）。

快速总结  
----------------

```cpp
// 内部全局变量定义：
static int g_x;          // 定义未初始化的内部全局变量（默认零初始化）
static int g_x{ 1 };     // 定义已初始化的内部全局变量

const int g_y { 2 };     // 定义已初始化的内部const全局变量
constexpr int g_y { 3 }; // 定义已初始化的内部constexpr全局变量

// 内部函数定义：
static int foo() {};     // 定义内部函数
```

完整总结详见课程[7.12 — 作用域、存储期与链接属性总结](Chapter-7/lesson7.12-scope-duration-and-linkage-summary.md)。

[下一课 7.7 — 外部链接与变量前向声明](Chapter-7/lesson7.7-external-linkage-and-variable-forward-declarations.md)  
[返回主页](/)  
[上一课 7.5 — 变量遮蔽（名称隐藏）](Chapter-7/lesson7.5-variable-shadowing-name-hiding.md)