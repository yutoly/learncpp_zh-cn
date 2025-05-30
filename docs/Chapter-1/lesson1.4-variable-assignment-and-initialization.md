1.4 — 变量赋值与初始化  
=============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年3月6日（首次发布于2019年2月1日）  

前文课程（[1.3 — 对象与变量简介](Chapter-1/lesson1.3-introduction-to-objects-and-variables.md)）讲解了如何定义存储值的变量。本章将探讨如何为变量赋值。  

以下程序示例先定义名为`x`的整型变量，随后定义两个整型变量`y`和`z`：
```
int main()
{
    int x;    // 定义整型变量x（推荐写法）
    int y, z; // 定义两个整型变量y和z

    return 0;
}
```
推荐每行定义单个变量。多变量定义的情况将在本章后续讨论。  

变量赋值（Variable assignment）  
----------------  

变量定义后，可使用`=`运算符为其赋值。此操作称为**赋值（assignment）**，`=`称为**赋值运算符（assignment operator）**。  
```
int width; // 定义整型变量width
width = 5; // 将值5赋给变量width

// 此时width的值为5
```
默认情况下，赋值操作将右侧值复制到左侧变量，这称为**拷贝赋值（copy-assignment）**。  

变量赋值后可通过`std::cout`与`<<`运算符输出其值。赋值操作可随时修改变量值，如下例演示两次赋值：
```
#include <iostream>

int main()
{
	int width; // 定义变量width
	width = 5; // 将值5拷贝赋值给width

	std::cout << width; // 输出5

	width = 7; // 修改width值为7

	std::cout << width; // 输出7

	return 0;
}
```
输出结果：
```
57
```
程序运行时，从`main`函数顶部开始顺序执行。首先为`width`分配内存，随后赋值`5`。首次输出显示`5`，再次赋值`7`后覆盖原值，第二次输出显示`7`。普通变量同一时刻只能存储一个值。  

> **警告**  
> 新手常见错误是混淆赋值运算符（`=`）与相等运算符（`==`）。赋值用于给变量赋值，相等用于比较两值是否相同。

变量初始化（Variable initialization）  
----------------  

单独定义后赋值的做法需要两条语句：定义语句与赋值语句。  

这两个步骤可合并。定义对象时可选择提供初始值，此过程称为**初始化（initialization）**，语法称为**初始化器（initializer）**。例如以下语句同时定义并初始化变量`width`：
```
#include <iostream>

int main()
{
    int width { 5 };    // 定义变量width并用初始值5初始化
    std::cout << width; // 输出5

    return 0;
}
```
此处`{ 5 }`是初始化器，`5`是初始值。  

> **关键点**  
> 初始化为变量提供初始值，记住"初始-化"的关联。

初始化形式（Different forms of initialization）  
----------------  

C++初始化方式复杂，此处介绍5种常见形式：
```
int a;         // 默认初始化（无初始化器）

// 传统初始化形式：
int b = 5;     // 拷贝初始化（等号后接初始值）
int c ( 6 );   // 直接初始化（括号内初始值）

// 现代初始化形式（推荐）：
int d { 7 };   // 直接列表初始化（大括号初始值）
int e {};      // 值初始化（空大括号）
```
格式间距可变（如`int b=5;`或`int d{7};`），空格使用依个人习惯。C++17起，拷贝初始化、直接初始化与直接列表初始化在多数情况下行为一致。  

> **相关内容**  
> 拷贝初始化、直接初始化与列表初始化的差异详见课程[14.15 — 类初始化与拷贝省略](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)。

> **高级阅读**  
> 其他初始化形式包括：  
> * 聚合初始化（见[13.8 — 结构体聚合初始化](Chapter-13/lesson13.8-struct-aggregate-initialization.md)）  
> * 拷贝列表初始化（下文讨论）  
> * 引用初始化（见[12.3 — 左值引用](Chapter-12/lesson12.3-lvalue-references.md)）  
> * 静态初始化、常量初始化与动态初始化（见[7.8 — 为何（非const）全局变量有害](Chapter-7/lesson7.8-why-non-const-global-variables-are-evil.md)）  
> * 零初始化（下文讨论）

默认初始化（Default-initialization）  
----------------  

无初始化器时（如变量`a`）称为**默认初始化（default-initialization）**。多数情况下，默认初始化不执行任何操作，变量获得不确定值（不可预测的"垃圾值"）。详见课程[1.6 — 未初始化变量与未定义行为](Chapter-1/lesson1.6-uninitialized-variables-and-undefined-behavior.md)。  

拷贝初始化（Copy-initialization）  
----------------  

等号后接初始值的形式称为**拷贝初始化（copy-initialization）**，继承自C语言：
```
int width = 5; // 将值5拷贝初始化给width
```
类似拷贝赋值，将右侧值复制到左侧新变量。此例中`width`初始化为`5`。  

由于对复杂类型效率较低，拷贝初始化在现代C++中曾不受欢迎。但C++17解决了大部分问题，拷贝初始化重新获得青睐，常见于旧代码或开发者偏好自然阅读的场景。  

> **高级阅读**  
> 当值被隐式拷贝时（如传值参数、返回值或异常捕获），也会使用拷贝初始化。

直接初始化（Direct-initialization）  
----------------  

括号内提供初始值的形式称为**直接初始化（direct-initialization）**：
```
int width ( 5 ); // 将值5直接初始化给width
```
最初用于高效初始化类类型对象。虽曾被列表初始化取代，但因列表初始化存在特性，直接初始化在特定场景复现用途。  

> **高级阅读**  
> 显式类型转换（如`static_cast`）时也使用直接初始化。

列表初始化（List-initialization）  
----------------  

现代C++使用大括号初始化对象，称为**列表初始化（list-initialization）**或**统一初始化（uniform initialization）**/**大括号初始化（brace initialization）**。有两种形式：
```
int width { 5 };    // 直接列表初始化（推荐）
int height = { 6 }; // 拷贝列表初始化（极少使用）
```
C++11前，不同初始化场景需分别使用拷贝或直接初始化。列表初始化提供统一语法，通过大括号明确初始化意图。  

> **关键点**  
> 看见大括号即表示列表初始化。

列表初始化还支持用值列表初始化对象，示例见课程[16.2 — std::vector与列表构造器简介](Chapter-16/lesson16.2-introduction-to-stdvector-and-list-constructors.md)。  

禁止窄化转换（List-initialization disallows narrowing conversions）  
----------------  

列表初始化禁止**窄化转换（narrowing conversion）**，即用不安全值初始化变量时编译器必须报错。例如：
```
int main()
{
    int w1 { 4.5 }; // 编译错误：列表初始化禁止将4.5窄化为4
    int w2 = 4.5;   // 编译通过：w2拷贝初始化为4
    int w3 (4.5);   // 编译通过：w3直接初始化为4

    return 0;
}
```
第7行试图用含小数部分的值初始化整型变量，触发编译错误。拷贝初始化（第9行）与直接初始化（第10行）则静默截断小数部分。  

注意此限制仅适用于初始化阶段，后续赋值不受限：
```
int main()
{
    int w1 { 4.5 }; // 错误：初始化时禁止窄化
    w1 = 4.5;       // 合法：赋值允许窄化

    return 0;
}
```
值初始化与零初始化（Value-initialization and zero-initialization）  
----------------  

使用空大括号初始化时，进行**值初始化（value-initialization）**，通常隐式初始化为零，称为**零初始化（zero-initialization）**：
```
int width {}; // 值初始化/零初始化为0
```
> **高级阅读**  
> 类类型可能初始化为预定义默认值（可能非零）。

现代C++推荐列表初始化（Prefer list-initialization）  
----------------  

列表初始化（含值初始化）因以下优势成为首选：  
* 适用于多数场景  
* 禁止窄化转换  
* 支持值列表初始化  

> **最佳实践**  
> 优先使用直接列表初始化或值初始化。

> **作者注**  
> Bjarne Stroustrup（C++之父）与Herb Sutter（C++专家）[推荐使用列表初始化](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-list)。现代C++中偶有例外情况，详见[16.2 — std::vector与列表构造器简介](Chapter-16/lesson16.2-introduction-to-stdvector-and-list-constructors.md)。  

何时使用{0}与{}？（Q: When should I initialize with { 0 } vs {}?）  
----------------  

明确使用初始值时用直接列表初始化：
```
int x { 0 };    // 直接列表初始化
std::cout << x; // 使用该0值
```
值临时且将被替换时用值初始化：
```
int x {};      // 值初始化
std::cin >> x; // 立即替换该值，显式0无意义
```

初始化变量（Initialize your variables）  
----------------  

创建变量时立即初始化。特殊场景（如性能关键代码）可例外，但需谨慎决策。  

> **相关内容**  
> Bjarne Stroustrup与Herb Sutter[推荐始终初始化对象](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md#es20-always-initialize-an-object)。  

未定义值变量的影响详见[1.6 — 未初始化变量与未定义行为](Chapter-1/lesson1.6-uninitialized-variables-and-undefined-behavior.md)。  

> **最佳实践**  
> 变量创建时立即初始化。

实例化（Instantiation）  
----------------  

**实例化（instantiation）**指变量已创建（分配内存）并初始化（含默认初始化）。实例化对象常指类类型对象，偶尔也用于其他类型。  

多变量初始化（Initializing multiple variables）  
----------------  

同类型多变量可在单行定义（不推荐但需了解）：
```
int a, b; // 创建a和b但不初始化
```
可初始化同行定义的多个变量：
```
int a = 5, b = 6;          // 拷贝初始化
int c (7), d (8);          // 直接初始化
int e {9}, f {10};         // 直接列表初始化
int i {}, j {};            // 值初始化
```
常见错误是误用单初始化语句：
```
int a, b = 5;     // 错误：a未初始化为5！
int a = 5, b = 5; // 正确：a和b均初始化为5
```
每个变量必须有自己的初始化器：
```
int a = 4, b = 5; // 正确：均有初始化器
int a, b = 5;     // 错误：a无初始化器
```
未使用初始化变量的警告（Unused initialized variables warnings）  
----------------  

现代编译器会对已初始化但未使用的变量发出警告（若开启"视警告为错误"则导致编译失败）。例如：
```
int main()
{
    int x {5}; // 定义但未使用x
    return 0;
}
```
GCC报错：
```
prog.cc:3:9: 错误：未使用变量'x'
```
解决方法：  
1. 删除未用变量定义  
2. 添加使用代码：
```
std::cout << x;
```
3. 使用`[[maybe_unused]]`属性（C++17）：
```
[[maybe_unused]] double pi {3.14159}; // 允许未使用
```
该属性应选择性用于有合理未使用原因的变量，编译器可能优化掉这些变量。  

> **作者注**  
> 后续课程示例可能使用`[[maybe_unused]]`避免编译警告。

测验  
----------------  

**问题1**  
初始化与赋值的区别？  
<details><summary>答案</summary>初始化在创建时赋予初始值，赋值在创建后赋予值。</details>  

**问题2**  
应优先使用哪种初始化形式指定初始值？  
<details><summary>答案</summary>直接列表初始化（直接大括号初始化）。</details>  

**问题3**  
默认初始化与值初始化的行为及推荐选择？  
<details><summary>答案</summary>默认初始化通常导致不确定值，值初始化通常零初始化。推荐值初始化。</details>  

[下一课 1.5 — iostream简介：cout、cin与endl](Chapter-1/lesson1.5-introduction-to-iostream-cout-cin-and-endl.md)  
[返回主页](/)  
[上一课 1.3 — 对象与变量简介](Chapter-1/lesson1.3-introduction-to-objects-and-variables.md)