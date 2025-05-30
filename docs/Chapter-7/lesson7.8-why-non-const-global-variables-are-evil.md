7.8 — 为何（非常量）全局变量是万恶之源  
=================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月29日（首次发布于2015年3月23日）  

若向资深程序员请教优秀编程实践的建议，经过深思熟虑后最可能的答案会是："避免使用全局变量！"。这一忠告背后有充分理由：全局变量是C++历史上最常被滥用的概念之一。虽然在小型教学程序中看似无害，但在大型项目中往往问题重重。  

新手程序员常倾向于大量使用全局变量，因其易于操作，尤其在涉及多函数调用时（通过函数参数传递数据非常麻烦）。然而这通常是个糟糕的选择。许多开发者认为应完全避免使用非常量（non-const）全局变量！  

在深入探讨原因前，需先明确概念。当开发者称全局变量有害时，通常特指非常量全局变量。  

非常量全局变量的危害根源  
----------------  

非常量全局变量最危险之处在于：任何被调用的函数都能修改其值，而程序员难以察觉这种变化。参考以下程序：  

```cpp
#include <iostream>

int g_mode; // 声明全局变量（默认零初始化）

void doSomething()
{
    g_mode = 2; // 将全局变量g_mode设为2
}

int main()
{
    g_mode = 1; // 注意：此处设置的是全局变量g_mode，而非声明局部变量！

    doSomething();

    // 程序员仍预期g_mode为1
    // 但doSomething已将其改为2！

    if (g_mode == 1)
    {
        std::cout << "未检测到威胁。\n";
    }
    else
    {
        std::cout << "启动核导弹...\n";
    }

    return 0;
}
```  

注意程序员将`g_mode`设为*1*后调用了`doSomething()`。除非明确知晓`doSomething()`会修改`g_mode`，否则程序员不会预料到该变化！因此，`main()`函数的后续逻辑将偏离预期（导致世界毁灭）。  

简言之，全局变量使程序状态不可预测。每个函数调用都潜藏危险，而程序员无从判断哪些调用存在风险！局部变量则安全得多，因为其他函数无法直接影响它们。  

其他拒绝使用非常量全局变量的理由  
----------------  

使用全局变量时，常会遇到如下代码：  

```cpp
void someFunction()
{
    // 有效代码

    if (g_mode == 4)
    {
        // 执行正确操作
    }
}
```  

调试后发现程序异常源于`g_mode`值为`3`而非*4*。如何修复？需要找出所有可能设置`g_mode`为`3`的位置，并追溯初始赋值过程。这些代码可能分布在完全无关的模块中！  

局部变量的核心优势在于：就近声明可最小化代码审查范围。全局变量则相反——因其可被任意位置访问，可能需要审查整个程序才能理解其用途。在小型程序中尚可接受，大型项目中将成噩梦。  

例如，程序中可能442处引用了`g_mode`。除非有完善文档，否则需审查所有使用场景才能理解其功能、有效值和整体作用。  

全局变量还削弱程序的模块化与灵活性。仅使用参数且无副作用的函数具备完美模块性。模块化既助于理解程序功能，也提升代码复用率。全局变量严重破坏模块化。  

特别要避免将全局变量用于关键"决策点"（如条件语句中的变量，前例中的`g_mode`）。信息型全局变量（如用户名）的变动不易引发问题，但影响程序运行逻辑的全局变量修改极易导致崩溃。  

> **最佳实践**  
> 尽可能使用局部变量替代全局变量。  

全局变量的初始化顺序问题  
----------------  

静态变量（含全局变量）的初始化在程序启动时、`main`函数执行前完成，分为两个阶段：  

**第一阶段：静态初始化（static initialization）**  
- 具有常量表达式（constexpr）初始化的全局变量执行常量初始化（constant initialization）  
- 无初始化器的全局变量执行零初始化（zero-initialization）  

**第二阶段：动态初始化（dynamic initialization）**  
处理具有非常量表达式初始化的全局变量。  

示例非常量表达式初始化：  
```cpp
int init()
{
    return 5;
}

int g_something{ init() }; // 非常量表达式初始化
```  

单文件内，各阶段的全局变量通常按定义顺序初始化（动态初始化阶段有少数例外）。因此需注意避免变量依赖尚未初始化的其他变量。例如：  

```cpp
#include <iostream>

int initX();  // 前置声明
int initY();  // 前置声明

int g_x{ initX() }; // g_x先初始化
int g_y{ initY() };

int initX()
{
    return g_y; // 调用时g_y尚未初始化
}

int initY()
{
    return 5;
}

int main()
{
    std::cout << g_x << ' ' << g_y << '\n';
}
```  

输出：  
```
0 5
```  

更严重的是，不同翻译单元中静态对象的初始化顺序具有不确定性。对于*a.cpp*和*b.cpp*两个文件，其全局变量可能以任意顺序初始化。若*a.cpp*中的静态变量使用*b.cpp*中的静态变量初始化，有50%概率后者尚未初始化。  

> **术语说明**  
> 不同翻译单元中静态存储期对象的初始化顺序不确定性被称为[静态初始化顺序问题（static initialization order fiasco）](https://en.cppreference.com/w/cpp/language/siof)。  

> **警告**  
> 避免使用其他翻译单元的静态存储期对象来初始化本单元对象。全局变量的动态初始化也受顺序问题影响，应尽量避免。  

合理使用非常量全局变量的场景  
----------------  

适用场景极少。多数情况下，使用局部变量并通过参数传递是更优方案。但在某些特殊场景中，谨慎使用非常量全局变量可降低程序复杂度。  

典型案例是日志文件，用于记录错误或调试信息。定义为全局变量是合理的，因为程序通常只需一个日志且各处使用。另一案例是随机数生成器（参见课程[8.15 — 全局随机数（Random.h）](Chapter-8/lesson8.15-global-random-numbers-random-h.md)）。  

值得一提的是，`std::cout`和`std::cin`对象即以全局变量形式实现（位于*std*命名空间）。  

> **经验法则**  
> 使用全局变量应至少满足：  
> 1. 变量代表的事物在程序中具有唯一性  
> 2. 变量在程序中普遍使用  

新手常误以为"当前只需一个实例"就可使用全局变量。例如单机游戏中的玩家角色。但当需要添加多人模式（对战或热座）时，这种设计将引发问题。  

全局变量的防护措施  
----------------  

若必须使用非常量全局变量，以下建议可降低风险（适用于所有全局变量）：  

**1. 命名规范**  
- 为所有非命名空间的全局变量添加"g"或"g_"前缀  
- 更优方案是置于命名空间中（参见课程[7.2 — 用户定义命名空间与作用域解析运算符](Chapter-7/lesson7.2-user-defined-namespaces-and-the-scope-resolution-operator.md)）  

示例改进：  
```cpp
#include <iostream>

namespace constants
{
    constexpr double gravity { 9.8 }; // 避免与其他全局变量命名冲突
}

int main()
{
    std::cout << constants::gravity << '\n'; // 明确全局变量身份

    return 0;
}
```  

**2. 封装访问**  
- 限制变量仅能在声明文件中访问（如设为static或const）  
- 提供外部全局访问函数进行管控（可添加输入验证、范围检查等）  
- 便于后续实现变更时集中修改  

示例改进：  
constants.cpp:  
```cpp
namespace constants
{
    constexpr double gravity { 9.8 }; // 内部链接，仅本文件可访问
}

double getGravity() // 外部链接，其他文件可访问
{
    // 可后续添加逻辑或透明修改实现
    return constants::gravity;
} 
```  

main.cpp:  
```cpp
#include <iostream>

double getGravity(); // 前置声明

int main()
{
    std::cout << getGravity() << '\n';

    return 0;
}
```  

> **提醒**  
> 全局`const`变量默认具有内部链接，`gravity`无需声明为`static`。  

**3. 函数参数化**  
编写独立函数时，应将全局变量作为参数传递而非直接使用，以保持模块性。  

改进示例：  
```cpp
#include <iostream>

namespace constants
{
    constexpr double gravity { 9.8 };
}

// 此函数可计算任意重力值的瞬时速度（更通用）
double instantVelocity(int time, double gravity)
{
    return gravity * time;
}

int main()
{
    std::cout << instantVelocity(5, constants::gravity) << '\n'; // 将常量作为参数传递

    return 0;
}
```  

C++笑话  
----------------  

问：全局变量的最佳命名前缀是什么？  
答：// （注释符号）  

这个笑话值得所有评论。  

[下一课 7.9 内联函数与变量](Chapter-7/lesson7.9-inline-functions-and-variables.md)  
[返回主页](/)  
[上一课 7.7 外部链接与变量前置声明](Chapter-7/lesson7.7-external-linkage-and-variable-forward-declarations.md)