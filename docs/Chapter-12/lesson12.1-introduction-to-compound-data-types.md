12.1 — 复合数据类型简介  
===========================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年1月18日，太平洋标准时间上午10:01  
2024年11月23日  

在课程[4.1 — 基础数据类型简介](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)中，我们介绍了**基础数据类型（fundamental data types）**，它们是C++核心语言提供的基本数据类型。迄今为止，我们在程序中大量使用了这些基础类型，尤其是`int`数据类型。虽然这些基础类型在简单场景中非常有用，但在处理更复杂任务时无法满足全部需求。  

例如，假设您正在编写计算两个分数相乘的数学程序。如何在程序中表示分数？您可能使用一对整数（一个表示分子，一个表示分母），如下所示：  
```
#include <iostream>

int main()
{
    // 第一个分数
    int num1 {};
    int den1 {};

    // 第二个分数
    int num2 {};
    int den2 {};

    // 用于吸收（移除）分子与分母间的斜杠
    char ignore {};

    std::cout << "输入分数: ";
    std::cin >> num1 >> ignore >> den1;

    std::cout << "输入分数: ";
    std::cin >> num2 >> ignore >> den2;

    std::cout << "两分数相乘结果: "
        << num1 * num2 << '/' << den1 * den2 << '\n';

    return 0;
}
```  
程序运行示例：  
```
输入分数: 1/2
输入分数: 3/4
两分数相乘结果: 3/8
```  
虽然该程序能运行，但存在几个待改进的问题。首先，每对整数仅松散关联——除代码注释和使用上下文外，缺乏明确标识表明分子分母的关联性。其次，遵循**不要自我重复（DRY）**原则，应创建函数处理分数输入（含错误处理）。但函数只能返回单个值，如何将分子分母同时返回给调用方？  

再假设编写需要记录员工ID列表的程序。您可能尝试：  
```
int main()
{
    int id1 { 42 };
    int id2 { 57 };
    int id3 { 162 };
    // 依此类推
}
```  
但若有100名员工呢？首先需输入100个变量名。若需全部打印或传递给函数？这将导致大量重复劳动。这种方式显然不具备扩展性。  

显然，基础数据类型的能力存在局限。  

复合数据类型  
所幸C++支持第二类数据类型：**复合数据类型（compound data types）**（有时也称**组合数据类型（composite data types）**）是通过其他现有数据类型定义的类型。复合数据类型具有额外属性和行为，可有效解决特定类型问题。  

> **关键洞察**  
> 每个数据类型要么是基础类型，要么是复合类型。C++语言标准明确定义了各类别的归属。  

通过本章及后续章节的讲解，我们将展示如何利用复合数据类型优雅解决上述所有问题。  
C++支持以下复合类型：  
* 函数（Functions）  
* C风格数组（C-style Arrays）  
* 指针类型（Pointer types）:  
    + 对象指针（Pointer to object）  
    + 函数指针（Pointer to function）  
* 成员指针类型（Pointer to member types）:  
    + 数据成员指针（Pointer to data member）  
    + 成员函数指针（Pointer to member function）  
* 引用类型（Reference types）:  
    + 左值引用（L-value references）  
    + 右值引用（R-value references）  
* 枚举类型（Enumerated types）:  
    + 非限定作用域枚举（Unscoped enumerations）  
    + 限定作用域枚举（Scoped enumerations）  
* 类类型（Class types）:  
    + 结构体（Structs）  
    + 类（Classes）  
    + 联合体（Unions）  

您已频繁使用过一种复合类型：函数。例如：  
```
void doSomething(int x, double y)
{
}
```  
此函数的类型为`void(int, double)`。注意该类型由基础类型构成，故属于复合类型。当然，函数还有其特殊行为（如可调用性）。  

因内容较多，我们将分多章讲解。本章涵盖部分较简单的复合类型，包括`左值引用（l-value references）`和`指针（pointers）`。下一章介绍`非限定作用域枚举（unscoped enumerations）`、`限定作用域枚举（scoped enumerations）`及首个类类型：`结构体（structs）`。后续章节将引入类（classes）并深入探讨更实用的`数组（array）`类型，包括`std::string`（在课程[5.7 — std::string简介](Chapter-5/lesson5.7-introduction-to-stdstring.md)中介绍）——它实际属于类类型！  

> **术语说明**  
> **类类型（class type）**指结构体、类或联合体类型。后续课程将频繁使用此术语。  

准备就绪了吗？让我们开始吧！

[下一课 12.2 值类别（左值与右值）](Chapter-12/lesson12.2-value-categories-lvalues-and-rvalues.md)  
[返回主页](/)  
[上一课 F.X章 F总结与测验](Chapter-F/lessonF.X-chapter-f-summary-and-quiz.md)