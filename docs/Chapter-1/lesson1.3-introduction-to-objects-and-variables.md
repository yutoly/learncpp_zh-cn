1.3 — 对象与变量简介  
============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年3月18日（首次发布于2007年5月30日）

数据与值（Data and values）  
----------------  

在课程[1.1 — 语句与程序结构](Chapter-1/lesson1.1-statements-and-the-structure-of-a-program.md)中，我们了解到程序中的多数指令是语句，而函数是按顺序执行的语句集合。函数中的语句通过操作数据（读取、修改和写入）来产生预期结果。

> **核心洞察**  
> 程序是通过操作数据来产生预期结果的指令集合。

计算机程序（包括源代码和编译后的二进制）在技术层面上也属于数据，但通常将程序本身称为"代码"，而程序处理的信息称为"数据"。

程序可通过多种方式获取数据：文件、数据库、网络、用户输入或直接在源代码中嵌入数据。例如"Hello world"程序中的文本"Hello world!"就是直接嵌入代码中的数据。

在编程中，单个数据单位称为**值（value）**（或称数据值）。常见值类型包括：  
* 数字（如`5`或`-6.7`）  
* 单引号包裹的字符（如`'H'`或`'$'`）  
* 双引号包裹的文本（如`"Hello"`或`"H"`）

> **关键规则**  
> 单引号包裹的值被编译器识别为字符值  
> 双引号包裹的值被识别为文本值  
> 数字值不使用引号  

直接嵌入源代码的值称为**字面量（literal）**。打印值的示例程序：  
```cpp
#include <iostream> // 用于std::cout

int main()
{
    std::cout << 5;       // 打印数字字面量5
    std::cout << -6.7;    // 打印数字字面量-6.7
    std::cout << 'H';     // 打印字符字面量H
    std::cout << "Hello"; // 打印文本字面量Hello

    return 0;
}
```

随机存取存储器（Random Access Memory）  
----------------  

计算机主存称为**随机存取存储器（Random Access Memory，RAM）**。程序运行时：  
1. 操作系统将程序加载至RAM  
2. 程序硬编码数据（如"Hello world!"）同时载入  
3. 操作系统为程序保留额外RAM空间  

RAM可视为编号存储单元的集合，用于存储运行时数据。传统编程语言允许直接访问特定地址（如7532号单元），但C++不鼓励直接内存访问。

对象与变量（Objects and variables）  
----------------  

在C++中，通过**对象（object）**间接访问内存。对象代表可存储值的存储区域（通常位于RAM或CPU寄存器）。编译器负责管理对象的内存分配细节。

> **核心概念**  
> 对象是存储值的存储区域。**变量（variable）**是具名对象。

变量定义（Variable definition）  
----------------  

使用**定义语句（definition statement）**声明变量：  
```cpp
int x; // 定义名为x的变量（类型为int）
```
编译器在编译时记录变量名和类型，运行时为变量分配实际存储空间（如内存地址140）。变量在定义语句处被创建。

完整示例：  
```cpp
int main()
{
    int x; // 变量x的定义
    
    return 0;
}
```

数据类型（Data types）  
----------------  

**数据类型（data type）**决定对象存储值的种类。例如`int`类型变量存储整数（如`4`, `-12`）。C++要求类型在编译时确定且不可更改。

定义其他类型变量：  
```cpp
double width; // 定义double类型变量width
```

多变量定义（Defining multiple variables）  
----------------  

同类型变量可在单语句中定义：  
```cpp
int a, b; // 正确但非最佳实践
```
常见错误：  
1. 重复指定类型：`int a, int b;`（错误）  
2. 混合类型定义：`int a, double b;`（错误）  

> **最佳实践**  
> 每个变量单独定义，并添加行内注释说明用途。

总结（Summary）  
----------------  

C++通过对象访问内存，变量是具名对象。每个变量包含：  
* 标识符（identifier）  
* 类型（type）  
* 值（value）  

变量在运行时创建。下节课将学习变量赋值与使用。

测验（Quiz time）  
----------------  

**问题1**  
什么是数据？  
  
<details><summary>答案</summary>计算机可移动、处理或存储的任何信息。</details>

**问题2**  
什么是值？  
  
<details><summary>答案</summary>可表示为数据的字母、数字、文本或其他概念实例。</details>

**问题3**  
什么是对象？  
  
<details><summary>答案</summary>存储值的存储区域（通常为内存）。</details>

**问题4**  
什么是变量？  
  
<details><summary>答案</summary>具名对象。</details>

**问题5**  
什么是标识符？  
  
<details><summary>答案</summary>变量被访问时使用的名称。</details>

**问题6**  
数据类型的用途？  
  
<details><summary>答案</summary>决定对象存储值的种类（如数字、字符等）。</details>

**问题7**  
什么是整数？  
  
<details><summary>答案</summary>无小数部分的数字。</details>

[下一课 1.4 — 变量赋值与初始化](Chapter-1/lesson1.4-variable-assignment-and-initialization.md)  
[返回主页](/)  
[上一课 1.2 — 注释](Chapter-1/lesson1.2-comments.md)