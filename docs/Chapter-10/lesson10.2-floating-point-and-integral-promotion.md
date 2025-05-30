10.2 — 浮点提升（Floating-point promotion）与整数提升（Integral promotion）  
==============================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年7月31日（首次发布于2021年6月17日）  

在课程[4.3 — 对象大小与sizeof运算符](Chapter-4/lesson4.3-object-sizes-and-the-sizeof-operator.md)中，我们提到C++为每个基础类型设定了最小尺寸保证。然而这些类型的实际尺寸可能因编译器和架构而异。  

这种可变性允许`int`和`double`数据类型根据特定架构设置最佳性能尺寸。例如，32位计算机通常能一次性处理32位数据。此时`int`的宽度很可能设为32位，这是CPU操作的"自然"数据尺寸（也可能是最高效的）。  

> **术语回顾**  
> 数据类型使用的比特数称为其**宽度（width）**。**较宽（wider）**数据类型使用更多比特，**较窄（narrower）**数据类型使用更少比特。  

当32位CPU需要修改8位值（如`char`）或16位值时会发生什么？某些32位处理器（如32位x86 CPU）可直接操作8位或16位值，但效率通常低于操作32位值。而其他32位CPU（如32位PowerPC CPU）只能操作32位值，需要额外技巧来处理较窄值。  

数值提升（Numeric promotion）  
----------------  

由于C++需要兼顾广泛架构的可移植性和性能，语言设计者无法假设所有CPU都能高效操作小于自然数据尺寸的值。  

为解决此挑战，C++定义了一类称为**数值提升（numeric promotions）**的类型转换。**数值提升**将特定较窄数值类型（如`char`）转换为更宽类型（通常是`int`或`double`）以提升处理效率。  

所有数值提升都是**值保留转换（value-preserving conversion）**（亦称**安全转换（safe conversion）**），即每个源值都能转换为目标类型的等效值。  

由于提升是安全的，编译器将自由使用数值提升且不发出警告。  

数值提升减少冗余  
----------------  

数值提升还解决了另一个问题。假设需要编写打印`int`类型的函数：  
```cpp
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}
```  
若没有类型转换，我们将需要为`short`和`char`分别编写不同版本，还需处理`unsigned char`、`signed char`等类型，这将导致代码爆炸。  

数值提升机制让我们只需编写接收`int`或`double`参数的函数（如上述`printInt()`），即可通过数值提升兼容多种参数类型。  

数值提升分类  
----------------  

数值提升规则分为两个子类：**整数提升（integral promotions）**和**浮点提升（floating point promotions）**。只有这些类别中的转换才被视为数值提升。  

浮点提升（Floating point promotions）  
----------------  

使用**浮点提升**规则，`float`类型值可转换为`double`类型。这意味着我们可以编写接收`double`参数的函数，并用`double`或`float`值调用它：  
```cpp
#include <iostream>

void printDouble(double d)
{
    std::cout << d << '\n';
}

int main()
{
    printDouble(5.0); // 无需转换
    printDouble(4.0f); // float数值提升为double

    return 0;
}
```  
在第二个`printDouble()`调用中，`float`字面量`4.0f`被提升为`double`以匹配函数参数类型。  

整数提升（Integral promotions）  
----------------  

**整数提升**规则更为复杂：  
* 有符号字符（signed char）或短整型（short）可转换为`int`  
* 无符号字符（unsigned char）、`char8_t`和无符号短整型（unsigned short）可转换为`int`（若`int`能容纳其全部范围），否则转换为`unsigned int`  
* 默认有符号的字符（char）遵循有符号字符转换规则，默认无符号则遵循无符号字符规则  
* 布尔（bool）可转换为`int`，`false`转为0，`true`转为1  

假设8位字节和4字节及以上`int`（现代常见配置），上述规则意味着`bool`、`char`、`signed char`、`unsigned char`、`signed short`和`unsigned short`都会提升为`int`。  

其他整数提升规则可参考[cppreference](https://en.cppreference.com/w/cpp/language/implicit_conversion#Integral_promotion)。  

示例：  
```cpp
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(2);

    short s{ 3 }; // 无短整型字面量后缀，使用变量
    printInt(s); // short整数提升为int

    printInt('a'); // char整数提升为int
    printInt(true); // bool整数提升为int

    return 0;
}
```  

需注意两点：  
1. 在某些架构（如2字节`int`）中，部分无符号整型可能提升为`unsigned int`而非`int`  
2. 部分无符号类型（如`unsigned char`）可能提升为更大的有符号类型（如`int`）。因此整数提升保留值但不一定保留符号属性  

并非所有扩宽转换都是数值提升  
----------------  

某些扩宽转换（如`char`转`short`，`int`转`long`）不被视为数值提升，而属于**数值转换（numeric conversions）**（将在[10.3 — 数值转换](Chapter-10/lesson10.3-numeric-conversions.md)中讲解）。因为这些转换不符合将小类型转为高效处理的大类型的目标。  

此区别主要在理论层面，但编译器在函数重载解析时会优先选择数值提升而非数值转换（详见[11.3 — 函数重载解析与歧义匹配](Chapter-11/lesson11.3-function-overload-resolution-and-ambiguous-matches.md)）。  

[下一课 10.3 数值转换](Chapter-10/lesson10.3-numeric-conversions.md)  
[返回主页](/)  
[上一课 10.1 隐式类型转换](Chapter-10/lesson10.1-implicit-type-conversion.md)