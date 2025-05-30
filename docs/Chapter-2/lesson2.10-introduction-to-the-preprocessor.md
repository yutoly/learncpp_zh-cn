2.10 — 预处理器简介  
========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年3月5日（首次发布于2007年6月3日）  

项目编译时，您可能认为编译器会逐字处理每个代码文件。实际并非如此。在编译之前，每个代码（.cpp）文件会经历**预处理（preprocessing）**阶段。此阶段中，名为**预处理器（preprocessor）**的程序对代码文本进行各种修改。预处理器不会直接修改原始代码文件——所有改动仅在内存或临时文件中进行。  

> **历史沿革**  
> 早期预处理器是独立于编译器的程序，但现代编译器中预处理器通常内置其中。  

预处理器主要执行常规操作，例如删除注释、确保文件以换行符结尾等。但其核心功能是处理`#include`指令（稍后详述）。预处理完成的代码文件称为**翻译单元（translation unit）**，该单元将被编译器实际编译。  

> **相关概念**  
> 预处理、编译与链接的完整过程统称为**翻译（translation）**。  
> 详细翻译阶段可参考[翻译阶段列表](https://en.cppreference.com/w/cpp/language/translation_phases)。当前标准中，预处理包含第1至4阶段，编译涵盖第5至7阶段。  

预处理器指令  
----------------  

预处理器逐行扫描代码文件，寻找以*#*开头、换行符结尾的**预处理器指令（preprocessor directives）**（注意不以分号结尾）。这些指令指示预处理器执行特定文本操作。需注意预处理器不解析C++语法，其指令有独立语法体系。  

> **核心原则**  
> 预处理器的最终输出不含任何指令本身，仅包含处理后的结果。  

> **术语澄清**  
> `using`指令（见课程[2.9 — 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)）并非预处理器指令，故不由预处理器处理。  

#include指令  
----------------  

`#include`指令（通常用于包含头文件如`<iostream>`）的作用是：预处理器将指令替换为指定文件内容。包含内容会递归预处理。  

示例程序：  
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello, world!\n";
    return 0;
}
```  
预处理器将`#include <iostream>`替换为iostream文件内容。后续课程讨论头文件时将深入解析此指令。  

> **核心概念**  
> 每个翻译单元通常由一个.cpp文件及其递归包含的所有头文件组成。  

宏定义  
----------------  

`#define`指令用于创建**宏（macro）**。C++中的宏是定义输入文本如何转换为输出文本的规则，分为两类：  
* **函数式宏（function-like macros）**：类似函数但存在安全隐患，建议改用普通函数  
* **对象式宏（object-like macros）**：分为两种形式：  
```cpp
#define 标识符
#define 标识符 替换文本
```  

宏标识符遵循常规命名规则（字母/数字/下划线，不以数字开头），约定使用全大写+下划线组合。  

> **最佳实践**  
> 优先使用其他替代方案，避免使用带替换文本的宏。  

带替换文本的对象式宏  
----------------  

预处理器将程序中所有宏标识符替换为指定文本。示例：  
```cpp
#define MY_NAME "Alex"
```  
预处理后`MY_NAME`被替换为"Alex"。此类宏曾用于C语言常量命名，现代C++建议使用更安全的方式（见[7.10 — 使用inline变量共享全局常量](Chapter-7/lesson7.10-sharing-global-constants-across-multiple-files-using-inline-variables.md)）。  

无替换文本的对象式宏  
----------------  

此类宏仅定义标识符，不做文本替换。常见用途是条件编译：  
```cpp
#define USE_YEN
```  

条件编译  
----------------  

条件编译指令允许根据条件决定编译内容，常用指令包括：  
* `#ifdef`：检查标识符是否已定义  
* `#ifndef`：检查标识符是否未定义  
* `#endif`：结束条件块  

示例：  
```cpp
#ifdef PRINT_JOE
    // 若PRINT_JOE已定义则编译此代码
#endif
```  
等价形式`#if defined(标识符)`和`#if !defined(标识符)`更具C++风格。  

> **实用技巧**  
> 使用`#if 0`可批量注释代码块（支持嵌套含多行注释的代码）：  
> ```cpp
> #if 0  // 从此处开始不编译
>     /* 多行注释 */
> #endif
> ```  

宏的作用域  
----------------  

预处理器按文件顺序处理指令，不受C++作用域影响。例如函数内定义的宏仍全局有效：  
```cpp
void foo()
{
#define MY_NAME "Alex"  // 宏在函数外仍有效
}
```  
但建议在函数外定义宏以避免混淆。  

通过`#include`引入的宏仅在该文件内有效。示例：  
头文件Alex.h：  
```cpp
#define MY_NAME "Alex"
```  
main.cpp包含该头文件后可使用该宏，但其他文件不受影响。  

[下一课 2.11 — 头文件](Chapter-2/lesson2.11-header-files.md)  
[返回主页](/)  
[上一课 2.9 — 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)