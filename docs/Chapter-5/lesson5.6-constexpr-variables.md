5.6 — constexpr变量  
==========================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月5日（首次发布于2023年10月23日）  

在前一课程[5.5 — 常量表达式](constant-expressions/#whywecare)中，我们定义了常量表达式（constant expression）的概念，讨论了为何需要常量表达式，并分析了常量表达式在何时进行编译期求值。  

本课程将深入探讨如何在现代C++中创建可用于常量表达式（constant expression）的变量。我们还将探索首个确保代码在编译期执行的方法。  

编译期`const`的局限性  
----------------  

前课提到，创建可用于常量表达式（constant expression）的变量方法之一是使用`const`关键字。具有整型（integral type）和常量表达式（constant expression）初始化器的`const`变量可用于常量表达式（constant expression），其他`const`变量则不可。  

然而，使用`const`创建可用于常量表达式（constant expression）的变量存在若干问题：  

首先，`const`无法直观表明变量是否可用于常量表达式（constant expression）。某些情况下较易判断：  
```
int a { 5 };       // 非常量
const int b { a }; // 明显非法（初始化器非常量）
const int c { 5 }; // 明显合法（初始化器是常量表达式）
```  

但在其他情况则较难判断：  
```
const int d { someVar };    // 无法直观判断d是否可用于常量表达式
const int e { getValue() }; // 无法直观判断e是否可用于常量表达式
```  

上述示例中，变量`d`和`e`是否可用于常量表达式（constant expression）取决于`someVar`和`getValue()`的定义。这意味着需要检查初始化器的定义才能推断具体情况。若`someVar`本身是`const`并通过变量或函数调用初始化，还需进一步追溯其初始化器的定义！  

其次，`const`无法告知编译器我们需要一个可用于常量表达式（constant expression）的变量（当不符合条件时应终止编译）。编译器只会默默生成一个仅能在运行期表达式（runtime expression）中使用的变量。  

第三，使用`const`创建编译期常量（compile-time constant）的方法不适用于非整型（non-integral）变量。而实际开发中常需要非整型（non-integral）的编译期常量（compile-time constant）。  

`constexpr`关键字  
----------------  

通过使用`constexpr`关键字（"constant expression"的缩写）替代`const`，我们可以借助编译器确保获得编译期常量（compile-time constant）变量。**constexpr变量（constexpr variable）**必定是编译期常量（compile-time constant）。因此，constexpr变量必须用常量表达式（constant expression）初始化，否则将引发编译错误。  

示例：  
```
#include <iostream>

// 非constexpr函数的返回值不是constexpr
int five()
{
    return 5;
}

int main()
{
    constexpr double gravity { 9.8 }; // 合法：9.8是常量表达式
    constexpr int sum { 4 + 5 };      // 合法：4+5是常量表达式
    constexpr int something { sum };  // 合法：sum是常量表达式

    std::cout << "请输入年龄：";
    int age{};
    std::cin >> age;

    constexpr int myAge { age };      // 编译错误：age不是常量表达式
    constexpr int f { five() };       // 编译错误：five()返回值不是constexpr

    return 0;
}
```  

由于函数通常在运行期执行，其返回值不是constexpr（即使返回的是常量表达式）。这就是`five()`不能作为`constexpr int f`合法初始化器的原因。  

相关课程  
我们将在[F.1 — constexpr函数](Chapter-F/lessonF.1-constexpr-functions.md)中讨论返回值可用于常量表达式（constant expression）的函数。  

此外，`constexpr`也适用于非整型（non-integral）变量：  
```
constexpr double d { 1.2 }; // d可用于常量表达式！
```  

变量中const与constexpr的语义差异  
----------------  

对于变量：  
* `const`表示对象值在初始化后不可修改。初始化器值可能在编译期或运行期确定。const对象可能在运行期求值  
* `constexpr`表示对象可用于常量表达式（constant expression）。初始化器值必须在编译期确定。constexpr对象可能在编译期或运行期求值  

constexpr变量隐式具有const属性。const变量不隐式具有constexpr属性（使用常量表达式初始化的const整型变量除外）。虽然变量可同时定义为`constexpr`和`const`，但多数情况下冗余，只需选择其一使用。  

与`const`不同，`constexpr`不是对象类型的组成部分。因此定义为`constexpr int`的变量实际类型为`const int`（因constexpr对对象隐式添加了const属性）。  

最佳实践  
----------------  

* 所有使用常量表达式（constant expression）初始化的常量变量应声明为`constexpr`  
* 所有使用非常量表达式（non-constant expression）初始化的运行时常量（runtime constant）应声明为`const`  

注意事项：后续课程将讨论不完全兼容`constexpr`的类型（如`std::string`、`std::vector`等使用动态内存分配的类型）。这些类型的常量对象应使用`const`替代`constexpr`，或选择兼容constexpr的类型（如`std::string_view`或`std::array`）。  

术语说明  
----------------  

术语`constexpr`是"constant expression"的合成词。该名称源于constexpr对象（和函数）可用于常量表达式（constant expression）。  

正式语境中，`constexpr`关键字仅适用于对象和函数。约定俗成下，`constexpr`也用作常量表达式（如`1+2`）的简称。  

作者注  
----------------  

本站部分示例在"使用constexpr"最佳实践确立前编写，因此某些示例未遵循上述准则。我们正在逐步更新不符合规范的示例。  

进阶阅读  
----------------  

在C/C++中，声明数组对象（可存储多个值的对象）要求数组长度（可存储值的数量）在编译期已知（以便编译器分配正确内存）。  

由于字面量（literal）在编译期已知，可用作数组长度：  
```
int arr[5]; // 5个int的数组，长度5在编译期已知
```  

许多情况下，使用符号常量（symbolic constant）作为数组长度更佳（例如避免魔术数字，便于多处使用时修改长度）。在C中，可通过预处理器宏（preprocessor macro）或枚举项（enumerator）实现，但无法使用const变量（可变长度数组VLA除外，但存在其他缺陷）。C++为改进此情况，希望允许使用const变量替代宏。但变量值通常被认为在运行期确定，因此无法用作数组长度。  

为解决此问题，C++标准新增豁免条款：使用常量表达式（constant expression）初始化的const整型（const integral type）将被视为编译期已知值，因而可用作数组长度：  
```
const int arrLen = 5;
int arr[arrLen]; // 合法：5个int的数组
```  

当C++11引入常量表达式（constant expression）时，使用常量表达式（constant expression）初始化的const int被纳入该定义。委员会讨论过是否包含其他类型，但最终决定保持现状。  

const与constexpr函数参数  
----------------  

普通函数调用在运行期求值，实参（argument）用于初始化函数形参（parameter）。由于形参初始化发生在运行期，导致两个后果：  
1. `const`形参被视为运行时常量（runtime constant）（即使实参是编译期常量）  
2. 形参不能声明为`constexpr`，因其初始化值直到运行期才能确定  

相关课程  
我们将在下方讨论可在编译期求值（因而可用于常量表达式）的函数。C++还支持向函数传递编译期常量的方法，详见[11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)。  

术语回顾  
----------------  

| 术语 | 定义 |  
| --- | --- |  
| 编译期常量（compile-time constant） | 值或不可修改对象，其值必须在编译期已知（如字面量和constexpr变量） |  
| constexpr | 声明对象为编译期常量（以及可在编译期求值的函数）的关键字。非正式语境下作为"常量表达式"简称 |  
| 常量表达式（constant expression） | 仅包含编译期常量（compile-time constant）和支持编译期求值的运算符/函数的表达式 |  
| 运行期表达式（runtime expression） | 非常量表达式 |  
| 运行时常量（runtime constant） | 非编译期常量的值或不可修改对象 |  

constexpr函数简介  
----------------  

**constexpr函数（constexpr function）**是可在常量表达式（constant expression）中调用的函数。当constexpr函数作为必须编译期求值的常量表达式（如constexpr变量初始化器）的组成部分时，必须在编译期求值。其他情况下，constexpr函数可能在编译期或运行期求值。要符合编译期执行条件，所有实参（argument）必须是常量表达式（constant expression）。  

创建constexpr函数时，需在函数声明返回类型前添加`constexpr`关键字：  
```
#include <iostream>

int max(int x, int y) // 非constexpr函数
{
    return (x > y) ? x : y;
}

constexpr int cmax(int x, int y) // constexpr函数
{
    return (x > y) ? x : y;
}

int main()
{
    int m1 { max(5, 6) };            // 合法
    const int m2 { max(5, 6) };      // 合法
    constexpr int m3 { max(5, 6) };  // 编译错误：max(5,6)不是常量表达式

    int m4 { cmax(5, 6) };           // 合法：可能编译期或运行期求值
    const int m5 { cmax(5, 6) };     // 合法：可能编译期或运行期求值
    constexpr int m6 { cmax(5, 6) }; // 合法：必须编译期求值

    return 0;
}
```  

作者注  
----------------  

我们曾计划在本章详细讨论constexpr函数，但读者反馈该主题过早出现且过于复杂。因此完整讨论移至[F.1 — constexpr函数](Chapter-F/lessonF.1-constexpr-functions.md)。  

关键要点是：constexpr函数可在常量表达式（constant expression）中调用。后续示例中会适当使用constexpr函数，但在正式讲解前不要求深入理解或自行编写。  

[下一课 5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)
[返回主页](/)  
[上一课 5.5 — 常量表达式](Chapter-5/lesson5.5-constant-expressions.md)