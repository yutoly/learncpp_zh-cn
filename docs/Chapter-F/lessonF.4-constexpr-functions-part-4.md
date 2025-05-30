F.4 — Constexpr函数（第四部分）
===================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月26日（更新于2025年3月17日）  

Constexpr/consteval函数可以使用非常量局部变量
----------------

在constexpr或consteval函数中，我们可以使用非常量表达式（non-constexpr）的局部变量，并且可以修改这些变量的值。  

以下示例说明：  

```cpp
#include <iostream>

consteval int doSomething(int x, int y) // 函数标记为consteval
{
    x = x + 2;       // 可修改非常量函数参数的值

    int z { x + y }; // 可实例化非常量局部变量
    if (x > y)
        z = z - 1;   // 并可修改其值

    return z;
}

int main()
{
    constexpr int g { doSomething(5, 6) };
    std::cout << g << '\n';

    return 0;
}
```  

当这类函数在编译期求值时，编译器将"执行"该函数并返回计算结果。  

Constexpr/consteval函数可将函数参数和局部变量作为实参传递给constexpr函数调用
----------------  

前文提到："当constexpr（或consteval）函数在编译期求值时，其调用的其他函数也必须在编译期求值。"  

值得注意的是，constexpr或consteval函数可以使用其函数参数（非常量表达式）甚至局部变量（可能完全非常量）作为constexpr函数调用的实参。当这些函数在编译期求值时，编译器必须知晓所有函数参数和局部变量的值（否则无法在编译期求值）。因此在此特定上下文中，C++允许将这些值作为实参传递给constexpr函数调用，且该调用仍可在编译期求值。  

```cpp
#include <iostream>

constexpr int goo(int c) // goo()现在是constexpr
{
    return c;
}

constexpr int foo(int b) // b在foo()内部不是常量表达式
{
    return goo(b);       // 若foo()在编译期解析，则`goo(b)`也可在编译期解析
}

int main()
{
    std::cout << foo(5);
    
    return 0;
}
```  

此例中，`foo(5)`可能在编译期或运行期求值。若在编译期求值，编译器将`b`视为`5`。尽管`b`不是常量表达式，编译器仍可将`goo(b)`视为`goo(5)`并在编译期求值。若`foo(5)`在运行期解析，则`goo(b)`也将在运行期解析。  

constexpr函数能否调用非constexpr函数？
----------------  

答案是肯定的，但仅限于constexpr函数在非常量上下文中求值时。当constexpr函数在常量上下文中求值时，不可调用非constexpr函数（否则无法生成编译期常量值），否则将引发编译错误。  

允许调用非constexpr函数的情况通常用于实现如下功能：  

```cpp
#include <type_traits> // 用于std::is_constant_evaluated

constexpr int someFunction()
{
    if (std::is_constant_evaluated()) // 若在常量上下文中求值
        return someConstexprFcn();
    else
        return someNonConstexprFcn();
}
```  

考虑此变体：  

```cpp
constexpr int someFunction(bool b)
{
    if (b)
        return someConstexprFcn();
    else
        return someNonConstexprFcn();
}
```  

只要`someFunction(false)`未在常量表达式中调用，该代码即为合法。  

> **附注**  
> C++23之前的标准要求constexpr函数必须对至少一组参数返回constexpr值，否则技术上视为格式错误。无条件调用非constexpr函数的constexpr函数将被视为格式错误。但编译器无需为此类情况生成错误或警告——除非尝试在常量上下文中调用该函数。C++23已取消此要求。  

最佳实践建议：  

1. 尽量避免在constexpr函数中调用非constexpr函数  
2. 若需区分常量与非常量上下文行为，使用`if (std::is_constant_evaluated())`（C++20）或`if consteval`（C++23及以后）进行条件分支  
3. 始终在常量上下文中测试constexpr函数，因其可能在非常量上下文工作但在常量上下文失败  

何时应声明函数为constexpr？
----------------  

通常规则：若函数可作为必需常量表达式的一部分求值，则应设为`constexpr`。  

**纯函数（pure function）**需满足以下条件：  

* 给定相同参数时函数总返回相同结果  
* 函数无副作用（如不改变静态局部/全局变量值、不进行输入输出等）  

纯函数通常应设为constexpr。  

> **附注**  
> constexpr函数不一定是纯函数。C++23起，constexpr函数可使用并修改静态局部变量。由于静态局部变量的值在函数调用间保持，修改静态局部变量被视为副作用。  

若程序规模较小或为临时用途，未声明constexpr不会导致严重问题。  

最佳实践
----------------  

除非有特定理由，否则可参与常量表达式求值的函数应设为`constexpr`（即使当前未被如此使用）。  
无法作为必需常量表达式求值的函数不应标记为`constexpr`。  

为何不将所有函数设为constexpr？
----------------  

几个原因：  

1. `constexpr`表明函数可用于常量表达式。若函数无法如此求值，则不应标记  
2. `constexpr`是函数接口的一部分。设为constexpr后，其他constexpr函数可调用它或在需常量表达式的上下文中使用。移除`constexpr`将破坏相关代码  
3. 调试constexpr函数更困难，因其无法设置断点或逐步调试  

为何为仅在运行期求值的函数声明constexpr？
----------------  

新手常问："当函数仅在运行期求值（如函数参数非常量）时，为何要声明constexpr？"  

原因包括：  

1. 使用constexpr几乎没有缺点，且可能帮助编译器优化程序体积和速度  
2. 当前未在编译期求值不代表未来修改或扩展时不会如此使用。若未预先声明，可能在需要时遗漏constexpr声明，错失性能优势，或在需常量表达式的上下文中被迫添加  
3. 重复实践有助于巩固最佳方案  

在重要项目中，应以函数可能被复用（或扩展）为前提进行实现。修改现有函数存在破坏风险，需重新测试。通常值得花时间"首次正确实现"，避免后续重做和复测。  

[下一课 F.X章 F总结与测验](Chapter-F/lessonF.X-chapter-f-summary-and-quiz.md)  
[返回主页](/)    
[上一课 F.3Constexpr函数（第三部分）与consteval](Chapter-F/lessonF.3-constexpr-functions-part-3-and-consteval.md)