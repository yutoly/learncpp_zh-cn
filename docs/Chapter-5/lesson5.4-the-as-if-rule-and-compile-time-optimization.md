5.4 — as\-if规则与编译期优化  
=====================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月22日 下午12:48（首次发布于2025年1月1日）  

优化概述  
----------------  

在编程中，**优化（optimization）**指通过修改软件使其更高效运行（例如提升速度或减少资源占用）的过程。优化对应用程序的整体性能有重大影响。  

部分优化需手动完成。使用**性能分析器（profiler）**可监测程序中各部分的执行时间及其对整体性能的影响。程序员可据此进行针对性优化。由于手动优化耗时，通常聚焦于能产生显著效果的高层改进（如选择更优算法、优化数据存储与访问、减少资源消耗、任务并行化等）。  

其他类型的优化可自动完成。执行优化的程序称为**优化器（optimizer）**。优化器通常在底层工作，通过重写、重排或删除语句/表达式来提升性能。例如编写`i = i * 2;`时，优化器可能将其改写为`i *= 2;`、`i += i;`或`i <<= 1;`。对于整型值，这些写法结果相同，但不同架构下性能表现可能不同。程序员难以预判最佳选择（答案可能因架构而异），但特定系统的优化器可以。单个底层优化的提升可能有限，但累积效果显著。  

现代C\+\+编译器属于**优化编译器（optimizing compiler）**，可在编译过程中自动优化程序。与预处理器类似，这些优化不修改源代码文件——它们作为编译过程的一部分透明应用。  

> **关键洞察**  
> 优化编译器让程序员专注于编写可读、可维护的代码，同时不牺牲性能。  

由于优化涉及权衡取舍（本课末将讨论），编译器通常支持多级优化设置，决定是否优化、优化强度及优先类型（如速度与体积）。多数编译器默认不启用优化，因此命令行用户需手动启用。IDE用户通常自动配置：发布版本启用优化，调试版本禁用优化。  

对于gcc和Clang用户  
----------------  
关于启用优化的方法，请参考课程[0.9 — 编译器配置：构建配置](Chapter-0/lesson0.9-configuring-your-compiler-build-configurations.md)。  

as\-if规则  
----------------  

C\+\+编译器在优化程序时拥有较大自由度。**as\-if规则（as-if rule）**规定：只要不改变程序的"可观察行为"，编译器可用任意方式修改代码以生成更优的版本。  

> **进阶阅读**  
> as\-if规则有一例外：即使复制（或移动）构造函数具有可观察行为，冗余调用也可被省略。详见课程[14.15 — 类初始化与复制省略](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)。  

现代编译器采用多种优化技术，具体应用取决于程序特性及编译器质量。  

> **相关内容**  
> [维基百科](https://en.wikipedia.org/wiki/Optimizing_compiler#Specific_techniques)列举了编译器使用的具体优化技术。  

优化案例  
----------------  
考虑以下程序：  
```cpp
#include <iostream>

int main()
{
	int x { 3 + 4 };
	std::cout << x << '\n';

	return 0;
}
```  
输出显然为：  
```
7
```  
但存在隐藏优化机会。  

若严格按代码编译（无优化），编译器将生成在运行时计算`3 + 4`的可执行文件。若程序执行百万次，该计算将重复百万次。由于`3 + 4`结果恒定，这种重复计算是低效的。  

编译期求值  
----------------  
现代C\+\+编译器能对部分表达式进行**编译期求值（compile-time evaluation）**（在编译阶段而非运行时计算）。  

> **关键洞察**  
> 编译期求值将工作从运行时转移至编译期，生成的可执行文件更小更快（代价是稍长的编译时间）。  

为便于说明，本节将介绍利用编译期求值的简单优化技术，后续课程继续讨论该主题。  

常量折叠  
----------------  
最早的编译期求值形式称为**常量折叠（constant folding）**。该技术将含字面量的表达式替换为计算结果。对`3 + 4`应用常量折叠后，编译器会将其替换为`7`，等效于：  
```cpp
#include <iostream>

int main()
{
	int x { 7 };
	std::cout << x << '\n';

	return 0;
}
```  
生成相同输出，但运行时无需计算`3 + 4`！  

常量折叠也适用于子表达式：  
```cpp
#include <iostream>

int main()
{
	std::cout << 3 + 4 << '\n';

	return 0;
}
```  
编译器将优化为`std::cout << 7 << '\n';`。  

常量传播  
----------------  
以下程序存在优化机会：  
```cpp
#include <iostream>

int main()
{
	int x { 7 };
	std::cout << x << '\n';

	return 0;
}
```  
初始化`x`需内存写入，打印时需内存读取。**常量传播（constant propagation）**将已知常量值的变量替换为值本身，优化后等效：  
```cpp
#include <iostream>

int main()
{
	int x { 7 };
	std::cout << 7 << '\n';

	return 0;
}
```  
消除内存读取操作。  

常量传播可与常量折叠结合：  
```cpp
#include <iostream>

int main()
{
	int x { 7 };
	int y { 3 };
	std::cout << x + y << '\n';

	return 0;
}
```  
`x + y`先传播为`7 + 3`，再折叠为`10`。  

死代码消除  
----------------  
**死代码消除（dead code elimination）**移除不影响程序行为的冗余代码。优化以下程序：  
```cpp
#include <iostream>

int main()
{
	int x { 7 };
	std::cout << 7 << '\n';

	return 0;
}
```  
变量`x`被定义但未使用，将被消除，等效于：  
```cpp
#include <iostream>

int main()
{
	std::cout << 7 << '\n';

	return 0;
}
```  
此时变量`x`被**优化移除（optimized out）**。相较原始版本，优化后无需运行时计算和内存操作，程序更小更快。  

常量变量更易优化  
----------------  
使用常量变量可辅助编译器优化。考虑以下非const示例：  
```cpp
#include <iostream>

int main()
{
	int x { 7 };
	std::cout << x << '\n';

	return 0;
}
```  
编译器需自行推断`x`值不变。若将`x`声明为const：  
```cpp
#include <iostream>

int main()
{
	const int x { 7 }; // x现为常量
	std::cout << x << '\n';

	return 0;
}
```  
编译器明确`x`不可变，更易应用常量传播并优化移除变量。  

> **关键洞察**  
> 使用const变量可提升编译器优化效果。  

优化对调试的影响  
----------------  
优化使程序更快，为何不默认启用？  

优化可能重排、修改、替换或删除代码元素，导致调试困难。例如：  
* 调试优化后的代码时，可能无法观察已被移除的变量  
* 单步跳过来被优化的函数  
* 编译期难以追踪被替换的表达式  

因此调试版本通常禁用优化，使编译代码更贴近源码。  

> **作者提示**  
> 编译期调试仍是待发展领域。C\+\+23正在讨论相关提案（如[P2758](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2758r1.html)），未来可能增强该方面能力。  

术语：编译期常量与运行时常量  
----------------  
C\+\+常量有时分为两类：  
* **编译期常量（compile-time constant）**：值在编译期已知（如字面量、用编译期常量初始化的const对象）  
* **运行时常量（runtime constant）**：值在运行时确定（如const函数参数、用非常量初始化的const对象）  

示例：  
```cpp
#include <iostream>

int five() { return 5; }

int pass(const int x) // x是运行时常量
{
    return x;
}

int main()
{
    // 非常量：
    [[maybe_unused]] int a { 5 };

    // 编译期常量：
    [[maybe_unused]] const int b { 5 };
    [[maybe_unused]] const double c { 1.2 };
    [[maybe_unused]] const int d { b }; // b是编译期常量

    // 运行时常量：
    [[maybe_unused]] const int e { a };       // a非常量
    [[maybe_unused]] const int f { e };       // e是运行时常量
    [[maybe_unused]] const int g { five() };  // 返回值运行时确定
    [[maybe_unused]] const int h { pass(5) }; // 返回值运行时确定

    return 0;
}
```  

注意：  
* 部分运行时常量可能被编译器按as-if规则优化为编译期求值  
* 部分编译期常量（如`const double d {1.2};`）无法用于标准定义的编译期特性  

建议避免使用这些术语，下节课将介绍更准确的术语体系。  

> **作者提示**  
> 未来文章将逐步淘汰这些术语。  

[下一课 5.5 — 常量表达式](Chapter-5/lesson5.5-constant-expressions.md)  
[返回主页](/)  
[上一课 5.3 — 数字系统（十进制、二进制、十六进制与八进制）](Chapter-5/lesson5.3-numeral-systems-decimal-binary-hexadecimal-and-octal.md)