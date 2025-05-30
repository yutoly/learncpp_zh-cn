10.x — 第10章总结与测验
===================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月3日（首次发布于2021年6月17日）  

恭喜您坚持到本章结束！标准类型转换规则相当复杂——若您未能理解所有细节也不必担心。  

本章回顾  
----------------  

**类型转换（type conversion）**是指将值从一种数据类型转换为另一种数据类型的过程。  

**隐式类型转换（implicit type conversion）**（又称自动类型转换或强制转换）在需要某种数据类型却提供其他类型时自动执行。若编译器能确定两种类型间的转换方式，则完成转换；否则将产生编译错误。  

C++语言为其基础类型（及部分高级类型）定义了多种内置转换方式，称为**标准转换（standard conversions）**。这些转换包括数值提升（numeric promotions）、数值转换（numeric conversions）和算术转换（arithmetic conversions）。  

**数值提升（numeric promotion）**是将较小数值类型转换为较大数值类型（通常为`int`或`double`）的过程，以便CPU能处理与处理器原生数据大小匹配的数据。数值提升包含整型提升（integral promotions）和浮点提升（floating-point promotions）。数值提升是**值保留（value-preserving）**的，即不会丢失数值或精度。但并非所有扩大转换（widening conversions）都是提升。  

**数值转换（numeric conversion）**是基础类型间非提升的转换操作。**窄化转换（narrowing conversion）**是可能导致数值或精度损失的数值转换。  

在C++中，某些二元运算符要求操作数类型一致。若提供不同类型操作数，将根据**常用算术转换（usual arithmetic conversions）**规则对操作数进行隐式类型转换。  

**显式类型转换（explicit type conversion）**通过程序员使用强制转换（cast）操作实现。**强制转换（cast）**是程序员对显式类型转换的明确请求。C++支持5种强制转换：`C风格强制转换`、`static_cast`、`const_cast`、`dynamic_cast`和`reinterpret_cast`。通常应避免使用`C风格强制转换`、`const_cast`和`reinterpret_cast`。`static_cast`用于将值从一种类型转换为另一种类型，是C++中最常用的强制转换方式。  

**typedef**和**类型别名（type alias）**允许程序员为数据类型创建别名。这些别名并非新类型，其行为与原始类型完全一致。typedef和类型别名不提供任何类型安全性，使用时需注意不要假定别名与其基础类型存在差异。  

**auto**关键字有多种用途。首先，auto可用于**类型推导（type deduction）**（又称类型推断），根据初始化表达式推断变量类型。类型推导会丢弃const和引用限定符，若需保留需显式添加。  

auto也可作为函数返回类型，让编译器根据return语句推断返回类型（但常规函数应避免此用法）。auto还用于**尾置返回类型（trailing return syntax）**。  

测验时间  
----------------  

**问题1**  
以下每种情况发生何种类型转换？有效答案为：无需转换（No conversion needed）、数值提升（numeric promotion）、数值转换（numeric conversion）、因窄化转换失败（won’t compile due to narrowing conversion）。假设`int`和`long`均为4字节。  

```cpp
int main()
{
    int a { 5 }; // 1a
    int b { 'a' }; // 1b
    int c { 5.4 }; // 1c
    int d { true }; // 1d
    int e { static_cast<int>(5.4) }; // 1e

    double f { 5.0f }; // 1f
    double g { 5 }; // 1g

    // 附加题部分
    long h { 5 }; // 1h

    float i { f }; // 1i（使用之前定义的变量f）
    float j { 5.0 }; // 1j
}
```  

1a) [显示答案](javascript:void(0))  
<details><summary>答案</summary>无需转换</details>  

1b) [显示答案](javascript:void(0))  
<details><summary>答案</summary>字符‘a’到int的数值提升（numeric promotion）</details>  

1c) [显示答案](javascript:void(0))  
<details><summary>答案</summary>因double到int的窄化转换导致编译失败</details>  

1d) [显示答案](javascript:void(0))  
<details><summary>答案</summary>布尔值true到int的数值提升</details>  

1e) [显示答案](javascript:void(0))  
<details><summary>答案</summary>double到int的数值转换</details>  

1f) [显示答案](javascript:void(0))  
<details><summary>答案</summary>float到double的数值提升</details>  

1g) [显示答案](javascript:void(0))  
<details><summary>答案</summary>int到double的数值转换</details>  

1h) [显示答案](javascript:void(0))  
<details><summary>答案</summary>int到long的数值转换（虽然简单但仍是转换）</details>  

1i) [显示答案](javascript:void(0))  
<details><summary>答案</summary>因double到float的窄化转换导致编译失败</details>  

1j) [显示答案](javascript:void(0))  
<details><summary>答案</summary>double到float的数值转换（允许转换因5.0是constexpr且在float范围内）</details>  

**问题2**  
2a) 更新以下程序，为角度值和弧度值使用类型别名：  

```cpp
#include <iostream>

namespace constants
{
    constexpr double pi { 3.14159 };
}

double convertToRadians(double degrees)
{
    return degrees * constants::pi / 180;
}

int main()
{
    std::cout << "Enter a number of degrees: ";
    double degrees{};
    std::cin >> degrees;

    double radians { convertToRadians(degrees) };
    std::cout << degrees << " degrees is " << radians << " radians.\n";

    return 0;
}
```  

[显示答案](javascript:void(0))  
```cpp
#include <iostream>

namespace constants
{
    constexpr double pi{ 3.14159 };
}

using Degrees = double;
using Radians = double;

Radians convertToRadians(Degrees degrees)
{
    return degrees * constants::pi / 180;
}

int main()
{
    std::cout << "Enter a number of degrees: ";
    Degrees degrees{};
    std::cin >> degrees;

    Radians radians{ convertToRadians(degrees) };
    std::cout << degrees << " degrees is " << radians << " radians.\n";

    return 0;
}
```  

2b) 根据上题的`Degrees`和`Radians`定义，解释以下语句能否编译：  
```cpp
radians = degrees;
```  

[显示答案](javascript:void(0))  
<details><summary>答案</summary>可以编译。`radians`的类型是`Radians`（即double的别名），`degrees`的类型是`Degrees`（同为double的别名），本质是将double值赋给double变量。</details>  

[下一课 11.1 函数重载简介](Chapter-11/lesson11.1-introduction-to-function-overloading.md)  
[返回主页](/)  
[上一课 10.9 函数类型推导](Chapter-10/lesson10.9-type-deduction-for-functions.md)