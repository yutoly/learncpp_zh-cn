5.5 — 常量表达式  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月18日（首次发布于2022年6月16日）  

在课程[1.10 — 表达式简介](Chapter-1/lesson1.10-introduction-to-expressions.md)中，我们介绍了表达式。默认情况下，表达式在运行时求值。某些情况下必须如此：
```
std::cin >> x;
std::cout << 5 << '\n';
```
由于输入输出无法在编译时执行，上述表达式必须在运行时求值。在先前课程[5.4 — as-if规则与编译时优化](Chapter-5/lesson5.4-the-as-if-rule-and-compile-time-optimization.md)中，我们讨论了as-if规则，以及编译器如何通过将工作从运行时转移到编译时来优化程序。根据as-if规则，编译器可以选择在运行时或编译时求值：
```
const double x { 1.2 };
const double y { 3.4 };
const double z { x + y }; // x + y 可能在运行时或编译时求值
```
表达式`x + y`通常会在运行时求值，但由于`x`和`y`的值在编译时已知，编译器可能选择在编译时求值，并用编译时计算的值`4.6`初始化`z`。某些情况下，C++语言要求表达式必须在编译时求值。例如constexpr变量需要可在编译时求值的初始化器：
```
int main()
{
    constexpr int x { expr }; // 由于x是constexpr，expr必须可在编译时求值
}
```
当需要常量表达式但未提供时，编译器将报错并停止编译。我们将在下节课（[5.6 — constexpr变量](Chapter-5/lesson5.6-constexpr-variables.md)）讨论constexpr变量时详细讲解。  

**进阶阅读**  
需要编译时可求值表达式的常见情况：  
* constexpr变量的初始化器（[5.6 — constexpr变量](Chapter-5/lesson5.6-constexpr-variables.md)）  
* 非类型模板参数（[11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)）  
* `std::array`（[17.1 — std::array简介](Chapter-17/lesson17.1-introduction-to-stdarray.md)）或C风格数组（[17.7 — C风格数组简介](Chapter-17/lesson17.7-introduction-to-c-style-arrays.md)）的指定长度  

编译时编程的优势  
虽然as-if规则能提升性能，但我们仍需依赖编译器的智能程度来决定哪些代码可以在编译时求值。这意味着我们期望在编译时执行的代码可能执行也可能不执行。同一代码在不同平台、编译器、编译选项或轻微修改下可能产生不同结果。由于as-if规则对我们不可见，我们无法获知编译器决定哪些代码在编译时求值。我们期望编译时求值的代码可能因拼写错误或理解偏差而不符合条件，而我们可能永远无法察觉。  

为改善这种情况，C++提供了显式指定代码在编译时执行的方式。利用语言特性实现编译时求值的技术称为**编译时编程**。这些特性在以下方面提升软件质量：  
* **性能**：编译时求值使程序更小更快  
* **通用性**：可在需要编译时值的场景使用此类代码  
* **可预测性**：若代码无法编译时执行，编译器将停止编译  
* **质量**：可靠检测编程错误，阻止未定义行为  

**关键洞察**  
编译时求值让我们编写更高性能和质量的程序！  

C++中编译时编程的核心特性：  
* constexpr变量（[5.6 — constexpr变量](Chapter-5/lesson5.6-constexpr-variables.md)）  
* constexpr函数（[F.1 — constexpr函数](Chapter-F/lessonF.1-constexpr-functions.md)）  
* 模板（[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)）  
* static_assert（[9.6 — assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md)）  

这些特性的共同点是都使用**常量表达式**。  

常量表达式  
C++标准将**常量表达式（constant expression）**定义为必须在编译时可求值的表达式。在课程[1.10 — 表达式简介](Chapter-1/lesson1.10-introduction-to-expressions.md)中，表达式定义为"由字面量、变量、运算符和函数调用组成的非空序列"。常量表达式则由字面量、常量变量、运算符和函数调用组成，且所有元素都必须在编译时可求值。  

**关键差异**  
常量表达式中的每个部分都必须在编译时可求值。  

非常量表达式常被称为**运行时表达式（runtime expression）**。  

**可选阅读**  
C++20标准规定"常量表达式可在翻译阶段求值"。在编译型程序中，翻译阶段包括预处理、编译和链接，因此常量表达式在编译时求值。  

常量表达式可包含：  
* 字面量（如`5`、`1.2`）  
* 具有常量表达式操作数的运算符（如`3+4`）  
* 具有常量表达式初始化器的const整型变量（如`const int x{5};`）  
* constexpr变量  
* 具有常量表达式参数的constexpr函数调用  

不可包含：  
* 非const变量  
* 具有常量表达式初始化器的const非整型变量（如`const double d{1.2};`）  
* 非constexpr函数的返回值  
* 函数参数  
* 非常量表达式操作数的运算符  

**术语说明**  
* "X可用于常量表达式"强调X本身可用  
* "X是常量表达式"强调整个表达式X是常量表达式  

示例分析  
以下程序演示常量表达式与运行时表达式的区别：
```
#include <iostream>

int getNumber()
{
    std::cout << "输入数字: ";
    int y{};
    std::cin >> y; // 只能在运行时执行
    return y;      // 返回表达式是运行时表达式
}

int five() { return 5; } // 返回表达式是常量表达式，但函数非constexpr

int main()
{
    5;                           // 常量表达式            
    1.2;                         // 常量表达式
    "Hello world!";              // 常量表达式
    5 + 6;                       // 常量表达式
    getNumber();                 // 运行时表达式
    five();                      // 运行时表达式
    std::cout << 5;              // 运行时表达式
    return 0;
}
```
变量分析：
```
const int a {5};     // 可用于常量表达式
int d {5};           // 不可用于常量表达式
const double f{1.2}; // 不可用于常量表达式（非整型）
```
编译时求值时机  
编译器仅在**需要常量表达式**的上下文中必须进行编译时求值。其他情况下可选择求值时机：
```
const int x {3+4}; // 必须编译时求值
int y {3+4};       // 可能运行时求值
```
**关键洞察**  
编译器仅在需要常量表达式的上下文中必须进行编译时求值。  

调试提示  
* **从不**：编译器无法确定值的非常量表达式  
* **可能**：编译器可确定值的非常量表达式（as-if规则优化）  
* **很可能**：非必需上下文的常量表达式  
* **总是**：必需上下文的常量表达式  

常量表达式必须恒定的原因  
考虑以下程序：
```
int x {5};          // 编译时已知
std::cin >> x;      // 用户输入改变x
```
由于`x`后续值未知，使用`x`的表达式无法保证编译时求值。const变量因不可变，可确保值始终已知。  

测验答案  
a) 常量表达式初始器；变量非常量表达式  
b) 常量表达式初始器；变量是常量表达式  
c) 常量表达式初始器；变量非常量表达式（非整型）  
d) 非常量表达式初始器；变量非常量表达式  
e) 非常量表达式初始器；变量非常量表达式  
f) 常量表达式初始器；变量是常量表达式  
g) 非常量表达式初始器；变量非常量表达式  
h) 值初始化（隐式0）；变量是常量表达式  

[下一课 5.6 — constexpr变量](Chapter-5/lesson5.6-constexpr-variables.md)  
[返回主页](/)  
[上一课 5.4 — as-if规则与编译时优化](Chapter-5/lesson5.4-the-as-if-rule-and-compile-time-optimization.md)