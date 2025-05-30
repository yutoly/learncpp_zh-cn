10.1 — 隐式类型转换  
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年3月3日（首次发布于2007年6月19日）  

我们在课程[4.12 — 类型转换与static_cast简介](Chapter-4/lesson4.12-introduction-to-type-conversion-and-static_cast.md)中介绍了类型转换。以下是该课程的核心要点回顾：  
* 将数据从一种类型转换为另一种类型的过程称为"类型转换（type conversion）"  
* **隐式类型转换（implicit type conversion）**由编译器在需要某数据类型但提供不同数据类型时自动执行  
* **显式类型转换（explicit type conversion）**通过类型转换运算符（如`static_cast`）主动请求  
* 转换不会改变被转换的数据本身，而是将原始数据作为输入生成转换结果  
* 将值转换为其他类型时，转换过程会产生临时对象来保存目标类型的转换结果  

本章前半部分将深入探讨类型转换机制。本节重点讲解隐式转换，显式转换（类型强制转换）将在后续课程[10.6 — 显式类型转换（casting）与static_cast](Chapter-10/lesson10.6-explicit-type-conversion-casting-and-static-cast.md)中讨论。由于类型转换在代码中广泛应用，理解其底层机制非常重要。这些知识对理解函数重载（与其他函数同名的函数）的工作方式也至关重要。  
> **作者注**  
> 本章重点讲解值到值的转换。其他类型转换将在引入必要前置知识（如指针、引用、继承等）后讨论。  

为何需要转换  
----------------  

对象的值以二进制位序列存储，数据类型决定了编译器如何将这些位解释为有意义的值。不同数据类型可能以不同方式表示"相同"的值。例如：整数值`3`可能存储为二进制`0000 0000 0000 0000 0000 0000 0000 0011`，而浮点值`3.0`可能存储为`0100 0000 0100 0000 0000 0000 0000 0000`。  

当我们执行如下操作时会发生什么？  
```cpp
float f{ 3 }; // 使用整数值3初始化浮点变量
```  
此时编译器不能直接将整数值`3`的二进制位复制给浮点变量`f`的内存空间。如果直接复制，当`f`（浮点类型）被访问时，这些位会被解释为浮点数而非整数，最终得到的浮点值将无法预测！  
> **扩展阅读**  
> 以下程序尝试将整数值`3`作为浮点数输出：  
> ```cpp
> #include <iostream>
> #include <cstring>
> 
> int main()
> {
>     int n { 3 };                        // 整数值3
>     float f {};                         // 浮点变量
>     std::memcpy(&f, &n, sizeof(float)); // 将n的二进制位复制到f
>     std::cout << f << '\n';             // 输出f（包含n的二进制位）
>     return 0;
> }
> ```  
> 输出结果为：  
> ```
> 4.2039e-45
> ```  

正确做法是将整数值`3`转换为等效的浮点值`3.0`，再存入`f`的内存空间（使用浮点值`3.0`的位表示）。  

隐式类型转换发生的时机  
----------------  

**隐式类型转换**（亦称**自动类型转换**或**强制转换**）在表达式类型与上下文预期类型不符时由编译器自动执行。C++中绝大多数类型转换属于隐式转换，例如以下情形：  
* 用不同类型值初始化或赋值变量：  
  ```cpp
  double d{ 3 }; // 整数值3隐式转换为double类型
  d = 6;         // 整数值6隐式转换为double类型
  ```  
* 返回值类型与函数声明类型不符：  
  ```cpp
  float doSomething()
  {
      return 3.0; // double值3.0隐式转换为float类型
  }
  ```  
* 二元运算符的操作数类型不同：  
  ```cpp
  double division{ 4.0 / 3 }; // 整数值3隐式转换为double类型
  ```  
* 在if语句中使用非布尔值：  
  ```cpp
  if (5) // 整数值5隐式转换为bool类型
  {
  }
  ```  
* 函数实参与形参类型不符：  
  ```cpp
  void doSomething(long l)
  {
  }
  
  doSomething(3); // 整数值3隐式转换为long类型
  ```  

编译器如何确定类型转换方式？答案在于标准转换规则。  

标准转换  
----------------  

C++核心语言定义了一系列转换规则，称为"标准转换（standard conversions）"。**标准转换**规定了基础类型（及部分复合类型，包括数组、引用、指针、枚举）如何相互转换。截至C++23，共有14种标准转换，可归纳为5大类：  

| 类别          | 含义                                                                 | 链接                                                                 |
|---------------|----------------------------------------------------------------------|----------------------------------------------------------------------|
| 数值提升      | 小整数类型转`int`或`unsigned int`，`float`转`double`                | [10.2 — 浮点与整数提升](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md) |
| 数值转换      | 非提升的整数/浮点转换                                                | [10.3 — 数值转换](Chapter-10/lesson10.3-numeric-conversions.md) |
| 限定符转换    | 添加或移除`const`/`volatile`                                         |                                                                      |
| 值类别转换    | 改变表达式的值类别                                                   | [12.2 — 值类别（左值与右值）](Chapter-12/lesson12.2-value-categories-lvalues-and-rvalues.md) |
| 指针转换      | `std::nullptr`转指针，指针类型互转                                   |                                                                      |  

例如，将`int`转为`float`属于数值转换类别，编译器只需应用`int`到`float`的数值转换规则即可。数值转换和数值提升是最重要的类别，后续课程将详细讲解。  

> **进阶阅读**  
> 完整标准转换列表：  
> | 类别             | 标准转换                | 描述                                                                 | 参考链接                                                                 |
> |------------------|-------------------------|----------------------------------------------------------------------|--------------------------------------------------------------------------|
> | 值类别转换       | 左值到右值              | 左值表达式转右值表达式                                               | [12.2 — 值类别](Chapter-12/lesson12.2-value-categories-lvalues-and-rvalues.md) |
> | 值类别转换       | 数组到指针              | C风格数组转为指向首元素的指针（数组退化）                             | [17.8 — C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md) |
> | 值类别转换       | 函数到指针              | 函数转为函数指针                                                     | [20.1 — 函数指针](Chapter-20/lesson20.1-function-pointers.md) |
> | 限定符转换       | 限定符转换              | 添加或移除`const`/`volatile`                                         |                                                                          |
> | 数值提升         | 整数提升                | 小整数类型转`int`或`unsigned int`                                    | [10.2 — 数值提升](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md) |
> | 数值提升         | 浮点提升                | `float`转`double`                                                   | [10.2 — 数值提升](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md) |
> | 数值转换         | 整数转换                | 非提升的整数转换                                                     | [10.3 — 数值转换](Chapter-10/lesson10.3-numeric-conversions.md) |
> | 数值转换         | 浮点转换                | 非提升的浮点转换                                                     | [10.3 — 数值转换](Chapter-10/lesson10.3-numeric-conversions.md) |
> | 数值转换         | 整浮转换                | 整数与浮点类型互转                                                   | [10.3 — 数值转换](Chapter-10/lesson10.3-numeric-conversions.md) |
> | 数值转换         | 布尔转换                | 整数、枚举、指针等转bool                                             | [4.10 — if语句简介](Chapter-4/lesson4.10-introduction-to-if-statements.md) |
> | 指针转换         | 指针转换                | `std::nullptr`转指针，指针转void指针或基类指针                       |                                                                          |  

类型转换可能失败  
----------------  

当尝试类型转换（隐式或显式）时，编译器会判断能否完成转换。若找到有效转换方式，则生成目标类型的值。若无法找到合适转换，编译将失败并报错。转换失败的原因可能包括：  
* 编译器不知如何转换类型  
  示例：  
  ```cpp
  int main()
  {
      int x { "14" }; // 无标准转换将字符串字面量"14"转为int
      return 0;
  }
  ```  
  GCC报错：`prog.cc:3:13: error: invalid conversion from 'const char*' to 'int' [-fpermissive]`  
* 特定功能禁止某些转换  
  示例：  
  ```cpp
  int x { 3.5 }; // 大括号初始化禁止导致数据丢失的转换
  ```  
  尽管编译器知道如何将`double`转为`int`，但大括号初始化禁止窄化转换  
* 编译器无法确定最佳转换方式（详见课程[11.3 — 函数重载解析与歧义匹配](Chapter-11/lesson11.3-function-overload-resolution-and-ambiguous-matches.md)）  

类型转换的完整规则较为复杂，但多数情况下转换能"正常工作"。后续课程将讲解标准转换的重要知识点，如需了解罕见情况的细节，可参考[隐式转换技术文档](https://en.cppreference.com/w/cpp/language/implicit_conversion)。  

[下一课 10.2 浮点与整数提升](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md)  
[返回主页](/)  
[上一课 9.x 第9章总结与测验](Chapter-9/lesson9.x-chapter-9-summary-and-quiz.md)