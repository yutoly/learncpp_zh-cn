A.4 — C++ 常见问题解答  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年3月28日（PDT时间 下午9:15） / 2025年2月11日  

本文收集了C++学习者反复提出的常见问题并进行解答。


Q1：为何不应使用"using namespace std"？  
----------------  

`using namespace std;`是**using指令（using-directive）**。该指令允许在当前作用域内访问指定命名空间（namespace）中的所有标识符（identifier）。  

您可能见过如下写法：  

```cpp
#include <iostream>

using namespace std;

int main()
{
    cout << "Hello world!";
    return 0;
}
```  

这使我们可以直接使用`std`命名空间中的名称而无需重复输入`std::`前缀。上例中，我们可以直接写`cout`代替`std::cout`。这听起来很方便，对吗？  

但当编译器遇到`using namespace std`时，会将`std`命名空间中的所有标识符暴露在全局作用域（global scope）中。这会引发三个关键问题：  

* 命名冲突风险显著增加：用户定义的标识符与`std`命名空间中已有名称发生碰撞的可能性大幅提升  
* 版本兼容性问题：未来标准库更新可能破坏现有程序。新版本可能引入导致命名冲突的名称，最坏情况下可能导致程序行为发生静默且意外的改变  
* 可读性下降：缺少`std::`前缀会降低代码可读性，使读者难以区分标准库名称和用户自定义名称  

因此，我们建议完全避免使用`using namespace std`（或其他任何using指令）。节省的少量打字成本不值得承担后续风险和麻烦。  

> **相关内容**  
> 详见课程[7.13 — Using声明与using指令](Chapter-7/lesson7.13-using-declarations-and-using-directives.md)  

Q2：为何某些函数/类型无需包含声明它们的头文件（header）即可使用？  
----------------  

例如许多读者发现，使用`std::string_view`时即使不包含`<string_view>`头文件程序仍能正常运行。  

头文件可能包含其他头文件。当您包含某个头文件时，也会获得其包含的所有其他头文件（及其递归包含的内容）。这些未显式包含的额外头文件称为**传递性包含（transitive includes）**。  

假设在*main.cpp*中包含了`<iostream>`。如果您的编译器实现中，`<iostream>`头文件自身包含了`<string_view>`（供其内部使用），那么当包含`<iostream>`时，您将间接获得`<string_view>`的内容。这意味着*main.cpp*可以在不显式包含`<string_view>`的情况下使用`std::string_view`类型。  

尽管这在当前编译器上可能通过编译，但您不应依赖此行为。当前能编译的代码可能在另一编译器或未来版本中失效。  

无法通过警告机制预防这种情况。最佳实践是显式包含所有使用功能的对应头文件。在不同编译器上测试程序有助于识别传递性包含的情况。  

> **相关内容**  
> 详见课程[2.11 — 头文件](Chapter-2/lesson2.11-header-files.md)  

Q3：产生未定义行为（undefined behavior）的代码看似运行正常，这可以接受吗？  
----------------  

即："我做了你警告不要做的事，但结果正确。这有什么问题？"  

未定义行为指执行了C++语言规范未定义行为的操作。这类代码可能表现出以下任意症状：  

* 程序每次运行产生不同结果  
* 行为不一致（有时正确有时错误）  
* 持续产生相同错误结果  
* 初始运行正常但后续产生错误  
* 立即或延迟性崩溃  
* 仅在部分编译器/平台有效  
* 修改无关代码后失效  
* 看似正常产生预期结果  

未定义行为最危险之处在于程序行为可能随时因任何原因改变。因此即使当前看似正常，也无法保证未来运行结果。  

> **相关内容**  
> 未定义行为详见课程[1.6 — 未初始化变量与未定义行为](Chapter-1/lesson1.6-uninitialized-variables-and-undefined-behavior.md)  

Q4：为何产生未定义行为的代码会生成特定结果？  
----------------  

读者常询问特定系统下产生特定结果的原因。多数情况下难以确定，因为结果可能取决于：  

* 当前程序状态  
* 编译器设置  
* 编译器实现方式  
* 计算机架构  
* 操作系统  

例如打印未初始化变量值时，可能得到随机值或特定值。这取决于变量类型、编译器内存布局以及内存原有内容（可能受操作系统或程序先前状态影响）。  

此类机制分析可能有趣但通常无实用价值（且任何变化都可能改变结果）。最佳答案不是物理层面的解释，而是"不要这样做"。  

Q5：为何尝试编译理应正确的示例时出现编译错误？  
----------------  

最常见原因是项目使用了错误的语言标准（language standard）。  

C++每个新标准都引入新特性。如果示例使用了C++17特性，而项目使用C++14标准编译，将因不支持该特性导致编译失败。  

尝试将语言标准设为编译器支持的最新版本。可通过运行课程[0.13 — 编译器使用的语言标准](Chapter-0/lesson0.13-what-language-standard-is-my-compiler-using.md)中的程序验证配置。  

> **相关内容**  
> 详见课程[0.12 — 配置编译器：选择语言标准](Chapter-0/lesson0.12-configuring-your-compiler-choosing-a-language-standard.md)  

也可能是编译器尚未支持某特性或存在缺陷。此时请更新至最新版本。  

CPPReference网站按语言标准跟踪编译器支持情况。支持表格链接位于其[主页](https://en.cppreference.com/w/cpp)右上角"Compiler Support"下。例如查看C++23支持情况可访问[此处](https://en.cppreference.com/w/cpp/compiler_support/23)。  

Q6：为何应在foo.cpp中包含"foo.h"？  
----------------  

最佳实践要求源文件（如foo.cpp）包含其配对头文件（如foo.h）。多数情况下，foo.h包含foo.cpp编译所需的定义。  

即使不包含头文件也能编译，包含配对头文件可让编译器检测两者间的潜在不一致（如函数返回类型与前置声明不匹配）。缺少包含可能导致未定义行为。  

包含头文件的代价可忽略不计，因此利大于弊。  

> **相关内容**  
> 详见课程[2.11 — 头文件](header-files/#corresponding_include)  

Q7：为何仅在main.cpp中包含"foo.cpp"时项目才能编译？  
----------------  

这通常源于忘记将foo.cpp加入项目/编译命令。更新项目/命令以包含所有源文件（.cpp）。编译时应看到每个源文件被编译。  

多文件项目中，编译器独立编译每个源文件，随后链接器（linker）将其链接为最终输出文件（如可执行文件）。若将代码拆分到多个文件（如main.cpp和foo.cpp）却仅编译main.cpp，将导致编译/链接错误。  

新手有时发现通过`#include "foo.cpp"`代替添加文件到项目可解决问题。此时预处理器（preprocessor）会将foo.cpp和main.cpp合并编译。在小项目中可能有效，但存在以下问题：  

1. 可能导致文件间的命名冲突  
2. 难以避免单一定义规则（ODR）违规  
3. 任何.cpp文件修改都将导致全项目重新编译，耗时增加  

> **相关内容**  
> 详见课程[2.11 — 头文件](header-files/#includecpp)  

Q8：为何必须在main()末尾return 0？  
----------------  

并非必须。`main()`函数特殊，若未提供返回语句将隐式返回0。  

但其他返回值函数（value-returning function）若未遇到返回语句将导致未定义行为。  

为保持一致性，建议显式返回0。若为简洁省略main()中的return亦可，但需注意其他函数不适用此规则。  

> **相关内容**  
> 详见课程[2.2 — 函数返回值](Chapter-2/lesson2.2-function-return-values-value-returning-functions.md)  

Q9：编译网站示例时出现"argument list for class template XXX is missing"错误，原因？  
----------------  

很可能示例使用了类模板参数推导（CTAD）——C++17特性。多数编译器默认使用C++14标准（不支持该特性）。  

若以下程序无法编译即为此原因：  

```cpp
#include <utility> // for std::pair

int main()
{
    std::pair p2{ 1, 2 }; // 使用CTAD从初始化式推导std::pair<int, int> (C++17)
    return 0;
}
```  

> **相关内容**  
> 使用课程[0.13](Chapter-0/lesson0.13-what-language-standard-is-my-compiler-using.md)程序检查语言标准  
> CTAD详见课程[13.14 — 类模板参数推导与推导指引](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)  

Q10：为何不将按值传递（pass-by-value）的函数参数或返回值设为const？  
----------------  

通常不将按值参数设为const的原因：  

* 对调用方无实际价值，但增加接口冗余  
* 通常不关心函数是否修改参数副本  

不将按值返回值设为const的原因：  

* 非类类型（如基础类型）的const返回值会被忽略  
* 类类型的const返回值可能阻碍优化（如移动语义）  

注意：按地址/引用传递时const相关  

> **相关内容**  
> 详见课程[5.1 — 常量变量](Chapter-5/lesson5.1-constant-variables-named-constants.md)  

Q11：为何使用constexpr？  
----------------  

constexpr等编译时编程技术有以下优势：  

* 更小更快的代码  
* 编译器可检测特定错误并停止编译  
* 编译时不允许未定义行为  
* 在需要常量表达式（constant expression）的场合使用变量/函数  

最后一点最为关键，因某些C++特性要求编译时可知的值。  

> **相关内容**  
> 详见课程[5.5 — 常量表达式](Chapter-5/lesson5.5-constant-expressions.md)  

Q12：为何要constexpr可能在运行时调用的函数？  
----------------  

原因包括：  

1. 使用constexpr几乎无成本，且可帮助编译器优化  
2. 当前未在编译时上下文中调用不代表未来不会  
3. 重复实践有助于巩固最佳习惯  

非小型项目中，建议以可复用性（reusability）为目标设计函数。初次正确实现可避免后续修改和重新测试的成本。  

> **相关内容**  
> 详见课程[F.1 — constexpr函数](constexpr-functions/#constexprruntimeeval)  

Q13：为何不应在表达式中多次调用同一输入函数？  
----------------  

C++标准通常不规定操作数（含函数参数）的求值顺序。运算符优先级和结合性仅决定操作数与运算符的分组方式及值计算顺序。  

例如`std::cout << subtract(getUserInput(), getUserInput())`中，`subtract()`的左右参数求值顺序不确定。用户输入5和2时，可能得到5-2=3或2-5=-3。  

通过将每个`getUserInput()`调用作为独立语句（顺序确定）并将返回值存入变量可消除歧义。  

> **相关内容**  
> 详见课程[6.1 — 运算符优先级与结合性](operator-precedence-and-associativity/#unspecified)  

Q14：练习题不足！哪里可获得更多练习？  
----------------  

推荐[Codewars](https://www.codewars.com/)，提供大量小型练习提升问题解决和C++实现能力。您可对比他人解法学习不同思路。  

但此类练习的答案具有临时性，无法体现高质量代码实践。最佳提升方式是创建个人项目：  

从简单项目开始（如小游戏或模拟程序），逐步增加功能。随着复杂度提升，代码缺陷将显现，帮助识别需要改进的领域。  

[下一课 B.1 — C++11简介](Appendix-B/lessonB.1-introduction-to-c11.md)  
[返回主页](/)  
[上一课 A.3 — 在Code::Blocks中使用库](Appendix-A/lessonA.3-a3-using-libraries-with-codeblocks.md)