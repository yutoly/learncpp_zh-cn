5.1 — 常量变量（constant variables，具名常量）
===========================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月17日（首次发布于2015年2月23日）  

常量简介  
----------------  

编程中，**常量（constant）**指程序执行期间不可改变的值。  

C++支持两类常量：  
* **具名常量（named constants）**：与标识符关联的常量值，亦称**符号常量（symbolic constants）**  
* **字面常量（literal constants）**：未关联标识符的常量值  

本章重点讨论具名常量，字面常量将在后续课程[5.2 — 字面量](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)中详述。  

具名常量类型  
----------------  

C++定义具名常量的三种方式：  
* 常量变量（本章内容）  
* 带替换文本的对象式宏（object-like macros，见课程[2.10 — 预处理器简介](Chapter-2/lesson2.10-introduction-to-the-preprocessor.md)）  
* 枚举常量（见课程[13.2 — 非限定作用域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)）  

常量变量是最常用的具名常量类型。  

常量变量  
----------------  

此前所见的变量均为**非常量（non-constant）**变量，即值可随时修改（通常通过赋值）：  
```cpp
int main()
{
    int x { 4 }; // x 是非常量变量
    x = 5;       // 通过赋值运算符修改x的值
    return 0;
}
```  

但许多场景需要定义不可变值的变量。例如地球表面重力加速度9.8米/秒²，该值短期内不会改变。将其定义为常量可防止意外修改，同时具备其他优势（后续课程详述）。  

初始化后不可改变的变量称为**常量变量（constant variable）**，虽然术语存在矛盾，但系约定俗成的名称。  

声明常量变量  
----------------  

声明常量变量时，将`const`关键字（称为"const限定符"）置于类型旁：  
```cpp
const double gravity { 9.8 };   // 推荐：const置于类型前
int const sidesInSquare { 4 };  // "east const"风格，可用但不推荐
```  

C++允许`const`置于类型前后，但惯例推荐类型前修饰，符合自然语言修饰语前置习惯（如"绿色球"而非"球绿色"）。  

> **扩展阅读**  
> 复杂声明解析时，部分开发者偏好"east const"风格（const后置）。虽有理据，但未成主流。  

最佳实践  
----------------  
* 将`const`置于类型前（更符合惯例）  

关键见解  
----------------  
对象类型包含const限定符。例如`const double gravity { 9.8 };`中，`gravity`的类型是`const double`。  

常量变量必须初始化  
----------------  
常量变量**必须**在定义时初始化，且后续不可通过赋值修改：  
```cpp
int main()
{
    const double gravity; // 错误：常量变量必须初始化
    gravity = 9.9;        // 错误：常量变量不可修改
    return 0;
}
```  

常量变量可使用其他变量（含非常量）初始化：  
```cpp
#include <iostream>

int main()
{ 
    std::cout << "输入年龄：";
    int age{};
    std::cin >> age;

    const int constAge { age }; // 用非常量值初始化常量变量

    age = 5;      // 正确：age是非常量
    constAge = 6; // 错误：constAge是常量

    return 0;
}
```  

此例中，`constAge`用非常量`age`初始化。`age`仍可修改，但`constAge`初始化后不可变。  

关键见解  
----------------  
常量变量的初始化器可以是非常量值。  

常量变量命名规范  
----------------  
C转来的程序员常使用全大写加下划线（如`EARTH_GRAVITY`）。C++更常见的是带'k'前缀的驼峰式（如`kEarthGravity`）。  

但常量变量行为与普通变量相似（除不可赋值外），无需特殊命名规范。因此推荐使用与非常量变量相同的命名方式（如`earthGravity`）。  

常量函数参数  
----------------  
函数参数可通过`const`设为常量：  
```cpp
#include <iostream>

void printInt(const int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(5); // 5将作为x的初始化器
    printInt(6); // 6将作为x的初始化器
    return 0;
}
```  

注意未显式初始化常量参数`x`——函数调用时的实参值将作为初始化器。  

将参数设为常量可借助编译器确保参数值在函数内不变。但在现代C++中，通常不将值参数设为`const`，因为：  
1. 参数只是副本，函数结束即销毁  
2. `const`会增加函数原型冗余  

最佳实践  
----------------  
* 值参数不使用`const`  

后续课程将讨论引用传递和地址传递，此时`const`的正确使用至关重要。  

常量返回值  
----------------  
函数返回值也可设为常量：  
```cpp
#include <iostream>

const int getValue()
{
    return 5;
}

int main()
{
    std::cout << getValue() << '\n';
    return 0;
}
```  

对于基本类型，返回类型的`const`限定符会被忽略（编译器可能警告）。其他类型返回常量值通常无意义，因为返回值是临时副本。返回常量值还可能阻碍编译器优化（如移动语义），影响性能。  

最佳实践  
----------------  
* 按值返回时不使用`const`  

为何使用常量变量  
----------------  
变量若可设为常量，则应设为常量，原因包括：  
1. 减少错误几率：防止意外修改  
2. 优化机会：编译器可基于常量假设优化程序，提升性能  
3. 降低复杂度：调试时无需跟踪常量变量的变化  

关键见解  
----------------  
系统中的每个活动部件都会增加复杂性和缺陷风险。非常量变量是活动部件，而常量变量不是。  

最佳实践  
----------------  
* 尽可能使用常量变量  
* 例外：函数的值参数和返回值通常不作为常量  

带替换文本的对象式宏  
----------------  
课程[2.10 — 预处理器简介](Chapter-2/lesson2.10-introduction-to-the-preprocessor.md)中讨论过带替换文本的对象式宏：  
```cpp
#include <iostream>

#define MY_NAME "Alex"

int main()
{
    std::cout << "我的名字是：" << MY_NAME << '\n';
    return 0;
}
```  

预处理器处理该文件时，将`MY_NAME`（第7行）替换为`"Alex"`。`MY_NAME`是名称，替换文本是常量值，故此类宏也是具名常量。  

优先使用常量变量而非预处理器宏  
----------------  
为何不用宏定义具名常量？至少存在三大问题：  
1. **作用域问题**：宏不遵循C++作用域规则。宏定义后，文件中所有同名出现都会被替换，可能导致意外替换：  
```cpp
#include <iostream>

void someFcn()
{
#define gravity 9.8 // 即使定义在函数内，后续所有gravity都会被替换
}

void printGravity(double gravity) // 此处导致编译错误
{
    std::cout << "重力：" << gravity << '\n';
}

int main()
{
    printGravity(3.71);
    return 0;
}
```  
GCC报错示例：  
```
prog.cc:7:17: 错误: 期待','或'...'在数字常量前
    5 | #define gravity 9.8
      |                 ^~~
prog.cc:10:26: 附注: 宏扩展处
```  

2. **调试困难**：调试器无法查看宏值，仅见替换后代码  
3. **行为差异**：宏替换机制异于C++其他特性，易引发错误  

常量变量无上述问题：遵循作用域规则，编译器可见，行为一致。  

最佳实践  
----------------  
* 优先使用常量变量而非带替换文本的对象式宏  

多文件程序中使用常量变量  
----------------  
许多应用中，具名常量需全局使用（如数学常数π或应用参数）。应在中央位置声明，避免重复定义。C++提供多种实现方式，详见课程[7.10 — 使用内联变量共享全局常量](Chapter-7/lesson7.10-sharing-global-constants-across-multiple-files-using-inline-variables.md)。  

术语：类型限定符  
----------------  
**类型限定符（type qualifier）**是修饰类型行为的关键字。声明常量变量的`const`称为**const类型限定符**。  

截至C++23，C++仅有两个类型限定符：`const`和`volatile`。  

> **扩展阅读**  
> `volatile`限定符告知编译器对象值可能随时改变（极少使用），禁用某些优化。  
> 技术文档中，`const`和`volatile`常统称为**cv限定符**。相关术语：  
> * **cv非限定类型**：无类型限定符的类型（如`int`）  
> * **cv限定类型**：应用了一个或多个限定符的类型（如`const int`）  
> * **可能cv限定类型**：可能是cv非限定或cv限定的类型  

这些术语主要用于技术文档，此处列出供参考。  

（附程序员笑话）  
* 问：如何判断C++开发者是否合格？  
* 答：看他们的CV（简历/cv限定符双关）。  

[下一课 5.2 字面量](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)  
[返回主页](/)  
[上一课 4.x 第4章总结与测验](Chapter-4/lesson4.x-chapter-4-summary-and-quiz.md)