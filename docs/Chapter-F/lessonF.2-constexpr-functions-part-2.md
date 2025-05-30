F.2 — Constexpr函数（第二部分）  
===================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看Alex的所有文章")  
2024年11月26日，太平洋标准时间下午4:16  
2024年12月10日  

非必需常量表达式中的constexpr函数调用  
----------------  

您可能认为constexpr函数在任何可能的情况下都会在编译时求值，但事实并非如此。  

在课程[5.5 — 常量表达式](Chapter-5/lesson5.5-constant-expressions.md)中我们提到：在不*要求*常量表达式的上下文中，编译器可选择在编译时或运行时求值常量表达式。因此，任何作为非必需常量表达式组成部分的constexpr函数调用都可能在编译时或运行时求值。  

例如：  

```
#include <iostream>

constexpr int getValue(int x)
{
    return x;
}

int main()
{
    int x { getValue(5) }; // 可能在运行时或编译时求值
    return 0;
}
```  

上例中，由于`getValue()`是constexpr函数，调用`getValue(5)`是常量表达式。但因变量`x`非constexpr，其初始化器不要求常量表达式。即使我们提供了常量表达式初始化器，编译器仍可自由选择在运行时或编译时求值`getValue(5)`。  

> **关键洞察**  
> 仅当上下文要求常量表达式时，才保证constexpr函数的编译时求值。  

必需常量表达式中constexpr函数的诊断  
----------------  

编译器*不要求*必须在实际编译时求值前确定constexpr函数是否可在编译时求值。编写constexpr函数时，很容易出现成功编译运行时调用，但在编译时求值失败的情况。  

请看以下典型示例：  

```
#include <iostream>

int getValue(int x)
{
    return x;
}

// 此函数可在运行时求值
// 但在编译时求值会产生编译错误
// 因为getValue(x)调用无法在编译时解析
constexpr int foo(int x)
{
    if (x < 0) return 0; // C++23采用P2448R1前需此行（见下文说明）
    return getValue(x);   // 此处调用非constexpr函数
}

int main()
{
    int x { foo(5) };           // 正确：将在运行时求值
    constexpr int y { foo(5) }; // 编译错误：foo(5)无法在编译时求值
    return 0;
}
```  

上例中，当`foo(5)`用于非constexpr变量`x`的初始化器时，将在运行时求值，正常返回值`5`。  

但当`foo(5)`用于constexpr变量`y`的初始化器时，必须在编译时求值。此时编译器将判定`foo(5)`无法在编译时求值，因为`getValue()`不是constexpr函数。  

因此，编写constexpr函数时，务必显式测试其在编译时求值是否通过编译（通过在必需常量表达式的上下文中调用，如constexpr变量初始化）。  

> **最佳实践**  
> 所有constexpr函数都应能在编译时求值，因为在要求常量表达式的上下文中必须如此。  
>  
> 始终在要求常量表达式的上下文中测试constexpr函数，因为该函数可能在运行时求值正常，但在编译时求值失败。  

> **进阶阅读**  
> C++23之前，若不存在任何参数值能使constexpr函数在编译时求值，则程序非良构（不要求诊断）。若省略`if (x < 0) return 0`行，则上例不存在允许函数在编译时求值的参数集，导致程序非良构。由于不要求诊断，编译器可能不会强制执行此规则。  
>  
> C++23中此要求已被撤销（[P2448R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2448r1.html)）。  

Constexpr/consteval函数参数非constexpr  
----------------  

constexpr函数的参数既非隐式constexpr，也不能声明为`constexpr`。  

> **关键洞察**  
> constexpr函数参数将意味着函数只能接受constexpr实参。但事实并非如此——当函数在运行时求值时，constexpr函数可接受非constexpr实参。  

由于此类参数非constexpr，它们不能在函数内的常量表达式中使用。  

```
consteval int goo(int c)    // c非constexpr，不能用于常量表达式
{
    return c;
}

constexpr int foo(int b)    // b非constexpr，不能用于常量表达式
{
    constexpr int b2 { b }; // 编译错误：constexpr变量要求常量表达式初始化器
    return goo(b);          // 编译错误：consteval函数调用要求常量表达式实参
}

int main()
{
    constexpr int a { 5 };
    std::cout << foo(a);    // 正确：常量表达式a可作为constexpr函数foo()的实参
    return 0;
}
```  

上例中，函数参数`b`非constexpr（即使实参`a`是常量表达式）。这意味着`b`不能用于任何要求常量表达式的场景，例如constexpr变量的初始化器（如`b2`）或调用consteval函数（`goo(b)`）。  

constexpr函数的参数可声明为`const`，此时它们被视为运行时常量。  

> **相关内容**  
> 若需要常量表达式参数，请参见课程[11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)。  

Constexpr函数隐式内联  
----------------  

当constexpr函数在编译时求值时，编译器必须能在函数调用前看到其完整定义（以便执行求值）。仅前置声明不够，即使实际函数定义出现在同一编译单元中。  

这意味着在多个文件中调用的constexpr函数需将其定义包含到每个翻译单元——这通常违反单一定义规则。为避免此问题，constexpr函数隐式内联，使其不受单一定义规则约束。  

因此，constexpr函数通常定义在头文件中，以便通过#include包含到任何需要完整定义的.cpp文件。  

> **规则**  
> 编译器必须能看见constexpr（或consteval）函数的完整定义，而非仅前置声明。  

> **最佳实践**  
> 在单个源文件(.cpp)中使用的constexpr/consteval函数应在源文件中使用位置之前定义。  
>  
> 在多个源文件中使用的constexpr/consteval函数应在头文件中定义，以便包含到各源文件。  

> **进阶阅读**  
> 对于仅在运行时求值的constexpr函数调用，前置声明足以满足编译器要求。这意味着可通过前置声明调用另一翻译单元定义的constexpr函数，但仅能在不要求编译时求值的上下文中调用。  

> **进阶阅读**  
> 根据[CWG2166](https://www.open-std.org/jtc1/sc22/wg21/docs/cwg_active.html#2166)，编译时求值的constexpr函数前置声明的实际要求是“constexpr函数必须在最终导致调用的最外层求值前定义”。因此以下代码合法：  

```
#include <iostream>

constexpr int foo(int);

constexpr int goo(int c)
{
    return foo(c);   // 注意foo尚未定义
}

constexpr int foo(int b) // 正确：在调用goo前foo已定义
{
    return b;
}

int main()
{
    constexpr int a{ goo(5) }; // 此为最外层调用
    return 0;
}
```  

此设计旨在支持相互递归的constexpr函数（两个constexpr函数相互调用），否则无法实现。  

要点总结  
----------------  

将函数标记为`constexpr`表示其可用于常量表达式，但*不*表示“将在编译时求值”。  

常量表达式（可能包含constexpr函数调用）仅在要求常量表达式的上下文中才必须在编译时求值。  

在不要求常量表达式的上下文中，编译器可选择在编译时或运行时求值常量表达式（可能包含constexpr函数调用）。  

运行时（非常量）表达式（可能包含constexpr或非constexpr函数调用）将在运行时求值。  

另一个示例  
----------------  

通过以下示例进一步探究constexpr函数的求值要求与可能性：  

```
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    constexpr int g { greater(5, 6) };              // 情况1：始终在编译时求值
    std::cout << g << " is greater!\n";

    std::cout << greater(5, 6) << " is greater!\n"; // 情况2：可能在运行时或编译时求值

    int x{ 5 }; // 非constexpr但值在编译时已知
    std::cout << greater(x, 6) << " is greater!\n"; // 情况3：通常在运行时求值

    std::cin >> x;
    std::cout << greater(x, 6) << " is greater!\n"; // 情况4：始终在运行时求值

    return 0;
}
```  

情况1中，我们在要求常量表达式的上下文中调用`greater()`，因此必须在编译时求值。  

情况2中，`greater()`在不要求常量表达式的上下文中调用（输出语句必须在运行时执行）。但由于实参是常量表达式，函数可能被编译时求值，因此编译器可自由选择求值时机。  

情况3中，我们使用一个非常量表达式实参调用`greater()`，通常会在运行时执行。  

但此实参值在编译时已知。根据as-if规则，编译器可能将`x`的求值视为常量表达式，并在编译时求值`greater()`。不过更可能在运行时求值。  

> **相关内容**  
> as-if规则详见课程[5.5 — 常量表达式](Chapter-5/lesson5.5-constant-expressions.md)。  
>  
> 注意：根据as-if规则，非constexpr函数也可能在编译时求值！  

情况4中，实参`x`的值在编译时不可知，因此`greater()`调用始终在运行时求值。  

> **关键洞察**  
> 换句话说，函数实际在编译时求值的可能性可分类如下：  
>  
> **必然（标准要求）**：  
> * 在要求常量表达式的上下文中调用constexpr函数  
> * 从正在编译时求值的其他函数调用constexpr函数  
>  
> **很可能（无理由不执行）**：  
> * 在不要求常量表达式的上下文中调用constexpr函数，且所有实参为常量表达式  
>  
> **可能（根据as-if规则优化）**：  
> * 在不要求常量表达式的上下文中调用constexpr函数，部分实参非常量表达式但其值编译时已知  
> * 可在编译时求值的非constexpr函数，且所有实参为常量表达式  
>  
> **永不（不可能）**：  
> * 在不要求常量表达式的上下文中调用constexpr函数，且部分实参值编译时不可知  

注意：编译器的优化级别设置可能影响其在编译时或运行时求值函数的选择。这意味着调试版和发布版中编译器可能做出不同选择（调试版通常关闭优化）。  

例如：除非启用代码优化（如使用`-O2`编译器选项），否则gcc和Clang不会对不要求常量表达式上下文中的constexpr函数进行编译时求值。  

> **进阶阅读**  
> 编译器还可能选择内联函数调用，甚至完全优化掉函数调用。这两种情况都会影响函数调用内容求值的时机（或是否求值）。  

[下一课 F.3 — Constexpr函数（第三部分）与consteval](Chapter-F/lessonF.3-constexpr-functions-part-3-and-consteval.md)  
[返回主页](/)  
[  
[上一课 F.1 — Constexpr函数](Chapter-F/lessonF.1-constexpr-functions.md)