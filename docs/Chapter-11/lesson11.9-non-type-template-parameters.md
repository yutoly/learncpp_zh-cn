11.9 — 非类型模板参数  
=====================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年4月21日，下午4:12（太平洋夏令时）  
2024年10月20日  

在前几课中，我们讨论了如何创建使用类型模板参数（type template parameters）的函数模板。类型模板参数作为实际类型的占位符，通过模板实参传递。  

虽然类型模板参数是目前最常用的模板参数类型，但还有另一种值得了解的模板参数：非类型模板参数（non-type template parameters）。  

非类型模板参数  
----------------  

**非类型模板参数（non-type template parameter）**是具有固定类型的模板参数，作为通过模板实参传递的常量表达式（constexpr）值的占位符。  

非类型模板参数可以是以下任意类型：  
* 整型（integral type）  
* 枚举类型（enumeration type）  
* `std::nullptr_t`  
* 浮点类型（floating point type）（C++20起）  
* 对象指针或引用  
* 函数指针或引用  
* 成员函数指针  
* 字面类类型（literal class type）（C++20起）  

在课程[O.1 — 通过std::bitset处理位标志和位操作](Chapter-O/lessonO.1-bit-flags-and-bit-manipulation-via-stdbitset.md)讨论`std::bitset`时，我们首次见到非类型模板参数的示例：  

```cpp
#include <bitset>

int main()
{
    std::bitset<8> bits{ 0b0000'0101 }; // <8>是非类型模板参数
    return 0;
}
```  

在`std::bitset`中，非类型模板参数用于指定存储的位数。  

定义自定义非类型模板参数  
----------------  

以下是一个使用整型非类型模板参数的简单函数示例：  

```cpp
#include <iostream>

template <int N> // 声明名为N的整型非类型模板参数
void print()
{
    std::cout << N << '\n'; // 此处使用N的值
}

int main()
{
    print<5>(); // 5作为非类型模板实参
    return 0;
}
```  

该示例输出：  

```
5
```  

第3行是模板参数声明。尖括号内定义名为`N`的非类型模板参数，作为整型值的占位符。在`print()`函数内部使用`N`的值。  

第11行调用`print()`函数时，使用整数值`5`作为非类型模板实参。编译器实例化的函数类似：  

```cpp
template <>
void print<5>()
{
    std::cout << 5 << '\n';
}
```  

运行时从`main()`调用此函数输出`5`。  

类似于`T`通常作为首个类型模板参数的名称，`N`约定俗成地用作整型非类型模板参数的名称。  

> **最佳实践**  
> 使用`N`作为整型非类型模板参数的名称。  

非类型模板参数的用途  
----------------  

截至C++20，函数参数不能是常量表达式（constexpr）。这适用于普通函数、constexpr函数（必须在运行时执行）以及令人意外的consteval函数。  

假设我们有如下函数：  

```cpp
#include <cassert>
#include <cmath> // 引入std::sqrt
#include <iostream>

double getSqrt(double d)
{
    assert(d >= 0.0 && "getSqrt(): d必须为非负数");
    if (d >= 0) // 非调试版本中assert可能被编译器移除
        return std::sqrt(d);
    return 0.0;
}

int main()
{
    std::cout << getSqrt(5.0) << '\n';
    std::cout << getSqrt(-5.0) << '\n'; // 运行时触发断言
    return 0;
}
```  

调用`getSqrt(-5.0)`会在运行时触发断言。虽然这优于无错误处理，但`-5.0`是字面量（隐式constexpr），若能使用static_assert在编译时捕获此类错误会更佳。然而static_assert需要常量表达式，而函数参数不能是constexpr...  

若将函数参数改为非类型模板参数，则可实现预期效果：  

```cpp
#include <cmath>
#include <iostream>

template <double D> // C++20支持浮点非类型参数
double getSqrt()
{
    static_assert(D >= 0.0, "getSqrt(): D必须为非负数");
    if constexpr (D >= 0) // 此示例中忽略constexpr
        return std::sqrt(D); // 注意：std::sqrt在C++26前非constexpr函数
    return 0.0;
}

int main()
{
    std::cout << getSqrt<5.0>() << '\n';
    std::cout << getSqrt<-5.0>() << '\n'; // 编译时触发static_assert
    return 0;
}
```  

此版本编译失败。当编译器处理`getSqrt<-5.0>()`时，实例化的函数类似：  

```cpp
template <>
double getSqrt<-5.0>()
{
    static_assert(-5.0 >= 0.0, "getSqrt(): D必须为非负数"); // 断言失败
    if constexpr (-5.0 >= 0) 
        return std::sqrt(-5.0);
    return 0.0;
}
```  

static_assert条件为假，触发编译错误。  

> **关键洞察**  
> 非类型模板参数主要用于需要向函数（或类类型）传递constexpr值的场景，以便在需要常量表达式的上下文中使用。  
>  
> 类类型`std::bitset`使用非类型模板参数定义存储位数，因为位数必须是constexpr值。  

> **作者注**  
> 使用非类型模板参数规避函数参数不能为constexpr的限制并非理想方案。目前有多个提案正在评估以改进此类情况，预计未来C++标准会提供更优解决方案。  

非类型模板实参的隐式转换（可选）  
----------------  

某些非类型模板实参可隐式转换以匹配不同类型的非类型模板参数。例如：  

```cpp
#include <iostream>

template <int N> // 整型非类型模板参数
void print()
{
    std::cout << N << '\n';
}

int main()
{
    print<5>();   // 无需转换
    print<'c'>(); // 'c'转换为整型，输出99
    return 0;
}
```  

输出：  

```
5
99
```  

此例中，`'c'`被转换为`int`以匹配函数模板`print()`的非类型模板参数，随后作为整型值输出。  

此上下文中，仅允许特定类型的constexpr转换。常见允许的转换包括：  
* 整型提升（如`char`转`int`）  
* 整型转换（如`char`转`long`或`int`转`char`）  
* 用户定义转换（如自定义类转`int`）  
* 左值到右值转换（如变量`x`转其值）  

注意，此列表比列表初始化（list initialization）允许的隐式转换更严格。例如，可用constexpr整型列表初始化`double`变量，但constexpr整型非类型模板实参不会转换为`double`非类型模板参数。  

完整允许的转换列表见[常量表达式](https://en.cppreference.com/w/cpp/language/constant_expression)中的"转换后的常量表达式"小节。  

与普通函数不同，将函数模板调用匹配到定义的算法不复杂，且不根据所需转换类型（或无转换）优先匹配。这意味着若函数模板针对不同类型的非类型模板参数重载，极易导致歧义匹配：  

```cpp
#include <iostream>

template <int N> // 整型非类型模板参数
void print()
{
    std::cout << N << '\n';
}

template <char N> // 字符型非类型模板参数
void print()
{
    std::cout << N << '\n';
}

int main()
{
    print<5>();   // 歧义匹配：int N=5 和 char N=5
    print<'c'>(); // 歧义匹配：int N=99 和 char N='c'
    return 0;
}
```  

可能令人意外的是，这两个`print()`调用均导致歧义匹配。  

使用auto推导非类型模板参数（C++17）  
----------------  

自C++17起，非类型模板参数可使用`auto`让编译器从模板实参推导类型：  

```cpp
#include <iostream>

template <auto N> // 从模板实参推导非类型模板参数
void print()
{
    std::cout << N << '\n';
}

int main()
{
    print<5>();   // N推导为整型5
    print<'c'>(); // N推导为字符型'c'
    return 0;
}
```  

编译并输出预期结果：  

```
5
c
```  

> **进阶阅读**  
> 此示例未产生歧义匹配，因为编译器先检查歧义匹配，无歧义时才实例化函数模板。本例仅有一个函数模板，故无歧义可能。  

测验题  
----------------  

**问题1**  
编写带非类型模板参数的constexpr函数模板，返回模板参数的阶乘。以下程序执行`factorial<-3>()`时应编译失败。  

```cpp
// 在此定义factorial()函数模板

int main()
{
    static_assert(factorial<0>() == 1);
    static_assert(factorial<3>() == 6);
    static_assert(factorial<5>() == 120);
    factorial<-3>(); // 应编译失败
    return 0;
}
```  

  
<details><summary>答案</summary>  

```cpp
template <int N>
constexpr int factorial()
{
    static_assert(N >= 0);
    int product { 1 };
    for (int i { 2 }; i <= N; ++i)
        product *= i;
    return product;
}

int main()
{
    static_assert(factorial<0>() == 1);
    static_assert(factorial<3>() == 6);
    static_assert(factorial<5>() == 120);
    factorial<-3>(); // 编译失败
    return 0;
}
```  
</details>  

[下一课 11.10 — 在多文件中使用函数模板](Chapter-11/lesson11.10-using-function-templates-in-multiple-files.md)  
[返回主页](/)  
[上一课 11.8 — 含多模板类型的函数模板](Chapter-11/lesson11.8-function-templates-with-multiple-template-types.md)