13.1 — 程序定义类型（program-defined types）简介  
==============================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月24日（首次发布于2022年1月18日）  

基础类型（fundamental types）作为C++核心语言的一部分，可直接使用。例如定义`int`或`double`类型变量时：  
```cpp
int x;   // 定义基础类型'int'变量
double d;// 定义基础类型'double'变量
```  
对基础类型的简单扩展（包括函数、指针（pointer）、引用（reference）和数组）同样适用：  
```cpp
void fcn(int) {}; // 定义void(int)类型函数
int* ptr;         // 定义复合类型'int指针'
int& ref { x };   // 定义复合类型'int引用'（用x初始化）
int arr[5];       // 定义int[5]类型数组（后续章节详述）
```  
由于C++已预知这些类型的名称和符号含义，因此无需额外定义即可使用。  

但考虑类型别名（type alias，见课程[10.7 — 类型别名与typedef](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)）的情况：  
```cpp
#include <iostream>

using Length = int; // 定义类型别名'Length'

int main()
{
    Length x { 5 }; // 使用先前定义的'Length'
    std::cout << x << '\n';
    return 0;
}
```  
若未定义`Length`，编译器将无法识别该类型。类型别名定义本身不创建对象，仅告知编译器其含义。  

程序定义类型的概念  
----------------  
回顾[12.1 — 复合数据类型简介](Chapter-12/lesson12.1-introduction-to-compound-data-types.md)中存储分数的需求：若C++内置分数类型即可完美解决。但实际应用中存在无数潜在类型需求，C++通过允许创建全新**用户定义类型（user-defined types）**解决。不过我们更倾向于使用**程序定义类型（program-defined types）**指代自定义类型。  

C++通过两类复合类型创建程序定义类型：  
* 枚举类型（包括非限定域和限定域枚举）  
* 类类型（包括结构体（struct）、类（class）和联合体（union））  

定义程序定义类型  
----------------  
程序定义类型需预先定义名称和结构。以下示例展示自定义分数类型的定义与实例化：  
```cpp
// 定义程序定义类型Fraction
struct Fraction
{
    int numerator {};
    int denominator {};
};

int main()
{
    Fraction f { 3, 4 }; // 实例化Fraction对象f
    return 0;
}
```  
此处使用`struct`关键字在全局作用域定义`Fraction`类型。此定义不分配内存，仅告知编译器类型结构。  

程序定义类型定义必须以分号结尾，遗漏分号将导致编译错误。  

命名规范  
----------------  
程序定义类型应首字母大写且不带后缀（如`Fraction`而非`fraction_t`）。  

变量定义示例如下：  
```cpp
Fraction fraction {}; // 实例化Fraction类型变量fraction
```  
由于C++区分大小写，类型名与变量名不会冲突。  

多文件程序中的使用  
----------------  
使用程序定义类型的每个文件需在调用前包含完整类型定义。通常将类型定义置于同名头文件中（如`Fraction.h`），并通过`#include`引入。  

最佳实践：  
* 仅在单个文件使用的类型：定义于该文件顶部  
* 多文件共用的类型：定义于同名头文件  

示例头文件Fraction.h：  
```cpp
#ifndef FRACTION_H
#define FRACTION_H

struct Fraction
{
    int numerator {};
    int denominator {};
};

#endif
```  
使用文件Fraction.cpp：  
```cpp
#include "Fraction.h" 

int main()
{
    Fraction f{ 3, 4 };
    return 0;
}
```  

类型定义与单一定义规则（ODR）  
----------------  
类型定义部分豁免单一定义规则：允许在不同文件中多次定义相同类型，但所有定义必须完全一致。例如多个文件包含`<iostream>`时，输入输出类型定义将被多次引入。  

术语辨析  
----------------  
* **用户定义类型（user-defined types）**：C++标准中指所有类类型和枚举类型（含标准库定义的类型，如`std::string`）  
* **程序定义类型（program-defined types）**：特指自定义或第三方库定义的类/枚举类型  

| 类型 | 含义 | 示例 |  
| --- | --- | --- |  
| 基础类型 | C++核心内置类型 | int, std::nullptr_t |  
| 复合类型 | 基于其他类型定义 | int&, double*, std::string, Fraction |  
| 用户定义类型 | 类/枚举类型（含标准库定义） | std::string, Fraction |  
| 程序定义类型 | 自定义类/枚举类型 | Fraction |  

[下一课 13.2 — 非限定域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)  
[返回主页](/)  
[上一课 12.x — 第12章总结与测验](Chapter-12/lesson12.x-chapter-12-summary-and-quiz.md)  