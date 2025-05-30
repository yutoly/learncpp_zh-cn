F.3 — constexpr函数（第三部分）与consteval  
=================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月26日（更新于2025年3月5日）  

强制constexpr函数在编译时求值  
----------------  

目前无法直接要求编译器优先在编译时求值constexpr函数（例如当constexpr函数的返回值用于非常量表达式时）。  

但我们可以通过确保constexpr函数的返回值被用于需要常量表达式的场景，强制要求其进行编译时求值。这种方式需要针对每个调用单独处理。  

最常用的方法是用返回值初始化constexpr变量（这也是之前示例中使用变量'g'的原因）。这种方法的缺点是必须引入新变量，既影响代码美观又降低可读性。  

> **进阶阅读**  
> 开发者尝试了多种方法解决强制编译时求值需引入新变量的问题，详见[此处](https://quuxplusone.github.io/blog/2018/08/07/force-constexpr/)和[此处](https://artificial-mind.net/blog/2020/11/14/cpp17-consteval)。  
>  
> C++20提供了更好的解决方案，我们稍后将介绍。  

consteval（C++20）  
----------------  

C++20引入**consteval**关键字，用于声明必须在编译时求值的函数（否则引发编译错误）。这类函数称为**立即函数（immediate functions）**。  

```cpp
#include <iostream>

consteval int greater(int x, int y) // 函数现在声明为consteval
{
    return (x > y ? x : y);
}

int main()
{
    constexpr int g { greater(5, 6) };              // 正确：将在编译时求值
    std::cout << g << '\n';

    std::cout << greater(5, 6) << " 是更大的数!\n"; // 正确：将在编译时求值

    int x{ 5 }; // 非常量表达式
    std::cout << greater(x, 6) << " 是更大的数!\n"; // 错误：consteval函数必须在编译时求值

    return 0;
}
```  

上述示例中，前两次调用`greater()`将在编译时求值。而`greater(x, 6)`无法在编译时求值，因此触发编译错误。  

> **最佳实践**  
> 若某函数必须进行编译时求值（例如执行只能在编译时完成的操作），应使用`consteval`。  

值得注意的是，consteval函数的参数并非constexpr（尽管这些函数只能在编译时求值）。此设计是为了保持语言一致性。  

判断constexpr函数调用是编译时还是运行时求值  
----------------  

C++目前未提供可靠机制实现此判断。  

> **关于`std::is_constant_evaluated`和`if consteval`的进阶讨论**  
>  
> 这两种方法均无法判断函数调用是编译时还是运行时求值。  
>  
> `std::is_constant_evaluated()`（定义于\<type_traits\>头文件）返回布尔值，指示当前是否处于**常量求值上下文（constant-evaluated context）**（即需要常量表达式的场景，如constexpr变量初始化）。当编译器必须在编译时求值常量表达式时，该函数返回`true`。  
>  
> 其典型用法如下：  
>  
> ```cpp
> #include <type_traits> // 包含std::is_constant_evaluated()
> 
> constexpr int someFunction()
> {
>     if (std::is_constant_evaluated()) // 若处于常量上下文
>         doSomething();
>     else
>         doSomethingElse();
> }
> ```  
>  
> 但编译器可能在不需要常量表达式的场景下选择编译时求值constexpr函数，此时`std::is_constant_evaluated()`仍返回`false`。因此该函数实际表示"编译器被强制要求编译时求值"，而非"正在编译时求值"。  
>  
> **关键洞察**  
> 此设计源于：  
> 1. 标准未严格区分"编译时"与"运行时"  
> 2. 优化不应改变程序可观察行为（除非标准明确允许）  
>  
> C++23引入的`if consteval`语法改进了`if (std::is_constant_evaluated())`，但求值逻辑相同。  

使用consteval强制constexpr在编译时求值（C++20）  
----------------  

consteval函数的局限性在于无法在运行时求值，灵活性不如constexpr函数。因此仍需便捷方法强制constexpr函数在可能时进行编译时求值。  

示例：  
```cpp
#include <iostream>

#define CONSTEVAL(...) [] consteval { return __VA_ARGS__; }()               // C++20版本（Jan Scultke）
#define CONSTEVAL11(...) [] { constexpr auto _ = __VA_ARGS__; return _; }() // C++11版本（Justin）

// 该函数在常量上下文中返回较大值，否则返回较小值
constexpr int compare(int x, int y) // constexpr函数
{
    if (std::is_constant_evaluated())
        return (x > y ? x : y);
    else
        return (x < y ? x : y);
}

int main()
{
    int x { 5 };
    std::cout << compare(x, 6) << '\n';                  // 运行时求值，返回5

    std::cout << compare(5, 6) << '\n';                  // 可能编译时求值，但总返回5
    std::cout << CONSTEVAL(compare(5, 6)) << '\n';       // 始终编译时求值，返回6
    
    return 0;
}
```  

> **进阶阅读**  
> 上述代码使用可变参数预处理器宏定义立即调用的consteval lambda。  
> 关于可变参数宏详见<https://en.cppreference.com/w/cpp/preprocessor/replace>  
> lambda详见课程[20.6 — lambda表达式（匿名函数）](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)  

更简洁的实现（不使用宏）：  
```cpp
#include <iostream>

// 使用C++20缩写函数模板和auto返回类型
consteval auto CONSTEVAL(auto value)
{
    return value;
}

constexpr int compare(int x, int y)
{
    if (std::is_constant_evaluated())
        return (x > y ? x : y);
    else
        return (x < y ? x : y);
}

int main()
{
    std::cout << CONSTEVAL(compare(5, 6)) << '\n';       // 编译时求值

    return 0;
}
```  

> **GCC用户注意**  
> GCC 14及以上版本存在优化启用时返回错误结果的bug。  
>  
> **进阶内容**  
> auto返回类型详见课程[10.9 — 函数返回类型推导](Chapter-10/lesson10.9-type-deduction-for-functions.md)  
> 缩写函数模板详见课程[11.8 — 多模板类型的函数模板](Chapter-11/lesson11.8-function-templates-with-multiple-template-types.md)  

[下一课 F.4 — constexpr函数（第四部分）](Chapter-F/lessonF.4-constexpr-functions-part-4.md)  
[返回主页](/)  
[上一课 F.2 — constexpr函数（第二部分）](Chapter-F/lessonF.2-constexpr-functions-part-2.md)