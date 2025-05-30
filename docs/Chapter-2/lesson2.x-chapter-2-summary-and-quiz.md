2.x — 第2章总结与测验
=================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2019年2月1日 上午10:56（首次发布于2024年4月26日）

本章回顾  
----------------  

**函数（function）**是为特定任务设计的可重用语句序列。用户自定义的函数称为**用户定义函数（user-defined）**。  

**函数调用（function call）**是通知CPU执行函数的表达式。发起调用的函数称为**调用者（caller）**，被调用的函数称为**被调用函数（callee/called function）**。注意函数调用必须包含括号。  

函数定义中的花括号和语句称为**函数体（function body）**。  

返回值的函数称为**值返回函数（value-returning function）**。函数的**返回类型（return type）**指明返回值的数据类型。**return语句**决定返回给调用者的具体**返回值（return value）**。返回值从函数复制回调用者的过程称为**按值返回（return by value）**。非void函数若未返回值将导致未定义行为。  

main函数的返回值称为**状态码（status code）**，用于告知操作系统（及其他调用程序）程序执行是否成功。约定俗成：返回0表示成功，非零值表示失败。  

遵循**DRY（Don’t Repeat Yourself）编程原则**，利用变量和函数消除冗余代码。  

返回类型为**void**的函数不向调用者返回值，称为**void函数（void function）**或**非值返回函数（non-value returning function）**。void函数不能在需要值的上下文中调用。  

函数中非最后执行的return语句称为**提前返回（early return）**，将立即返回调用者。  

**函数参数（function parameter）**是函数中由调用者提供值的变量。**实参（argument）**是调用者传递给参数的具体值。实参复制到参数的过程称为**按值传递（pass by value）**。  

函数参数和函数体内定义的变量称为**局部变量（local variable）**。变量的存在时间称为**生命周期（lifetime）**。变量在**运行时（runtime）**创建和销毁。变量的**作用域（scope）**决定其可见与可用范围。变量可见时称为**在作用域内（in scope）**，不可见时称为**超出作用域（out of scope）**。作用域是**编译期（compile-time）**属性，在编译时生效。  

**空白符（whitespace）**指用于格式化的字符，C++中包括空格、制表符和换行符。  

**前向声明（forward declaration）**允许在定义标识符前告知编译器其存在。函数前向声明使用**函数原型（function prototype）**，包含返回类型、名称和参数（无函数体），后接分号。  

**定义（definition）**实现函数/类型或实例化变量。**声明（declaration）**告知编译器标识符的存在。C++中所有定义同时是声明。**纯声明（pure declaration）**指非定义的声明（如函数原型）。  

多数复杂程序包含多个文件。  

当两个标识符以编译器/链接器无法区分的方式引入程序时，将产生**命名冲突（naming collision）**错误。**命名空间（namespace）**确保其内所有标识符唯一性，std命名空间即为典型示例。  

**预处理器（preprocessor）**在编译前处理代码。**预处理指令（directive）**是以#开头、换行符结尾的特殊指令。**宏（macro）**定义输入文本如何转换为输出文本的规则。  

**头文件（header file）**用于向代码文件传播声明。使用#include指令时，该指令被包含文件内容替换。包含系统头文件（如C++标准库）时使用尖括号，用户自定义头文件使用双引号。包含系统头文件时优先选择无.h扩展名的版本。  

**头文件保护（header guard）**防止头文件内容被多次包含到同一代码文件，但不阻止包含到不同文件。  

测验时间  
----------------  

确保使用编辑器自动格式化功能保持代码风格一致，增强可读性。  

**问题1**  
编写单文件程序（main.cpp），实现以下功能：  
* 从用户读取两个整数  
* 相加后输出结果  
要求使用三个函数：  
- readNumber：获取并返回用户输入的整数  
- writeAnswer：输出结果（带参数，无返回值）  
- main：整合上述函数  

[查看提示](javascript:void(0))  
<details><summary>提示1</summary>无需单独加法函数（直接使用+运算符）</details>  
[查看提示](javascript:void(0))  
<details><summary>提示2</summary>需调用两次readNumber()</details>  
  
main.cpp:
```cpp
#include <iostream>

int readNumber()
{
    std::cout << "Enter a number to add: ";
    int x {};
    std::cin >> x;
    return x;
}

void writeAnswer(int x)
{
    std::cout << "The answer is " << x << '\n';
}

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x + y); // 使用+运算符传递x+y的和给writeAnswer()
    return 0;
}
```

**问题2**  
修改问题1的程序，将readNumber()和writeAnswer()移至io.cpp文件。使用前向声明在main()中访问。  

  
io.cpp:
```cpp
#include <iostream>

int readNumber()
{
    std::cout << "Enter a number to add: ";
    int x {};
    std::cin >> x;
    return x;
}

void writeAnswer(int x)
{
    std::cout << "The answer is " << x << '\n';
}
```
main.cpp:
```cpp
// 无需#include <iostream>（main.cpp未使用I/O功能）

// io.cpp函数的前向声明
int readNumber();
void writeAnswer(int x);

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x+y);
    return 0;
}
```

**问题3**  
修改问题2的程序，改用头文件io.h（含头文件保护）访问函数。  

  
io.h:
```cpp
#ifndef IO_H
#define IO_H

int readNumber();
void writeAnswer(int x);

#endif
```
io.cpp:
```cpp
#include "io.h"
#include <iostream>

int readNumber()
{
    std::cout << "Enter a number to add: ";
    int x {};
    std::cin >> x;
    return x;
}

void writeAnswer(int x)
{
    std::cout << "The answer is " << x << '\n';
}
```
main.cpp:
```cpp
#include "io.h"

int main()
{
    int x { readNumber() };
    int y { readNumber() };
    writeAnswer(x+y);
    return 0;
}
```
注意：虽然io.cpp无需包含io.h，但最佳实践要求代码文件包含对应的头文件（详见课程[2.11 — 头文件](header-files/#corresponding_include)）。  

若出现以下错误：  
```
未解析的外部符号 "int __cdecl readNumber(void)"
readNumber()未定义引用
```
可能未将io.cpp加入项目，导致函数定义未编译。  

[下一课 3.1 — 语法与语义错误](Chapter-3/lesson3.1-syntax-and-semantic-errors.md)  
[返回主页](/)  
[上一课 2.13 — 如何设计首个程序](Chapter-2/lesson2.13-how-to-design-your-first-programs.md)