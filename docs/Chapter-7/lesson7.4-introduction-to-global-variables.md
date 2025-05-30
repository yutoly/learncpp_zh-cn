7.4 — 全局变量简介  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月19日上午8:22（太平洋夏令时）  
2024年6月9日  

 

在课程[7.3 — 局部变量](Chapter-7/lesson7.3-local-variables.md)中，我们学习了局部变量（local variables）是定义在函数体内的变量。局部变量具有块作用域（仅在声明它们的块内可见）和自动存储期（在定义点创建，块退出时销毁）。

在C++中，变量也可以声明在函数*外部*。这类变量称为**全局变量（global variables）**。

声明全局变量  
----------------  

按照惯例，全局变量通常声明在文件顶部（包含指令之后）的全局命名空间（global namespace）中。以下是全局变量定义的示例：

```cpp
#include <iostream>

// 在函数外部声明的变量是全局变量（global variables）
int g_x {}; // 全局变量 g_x

void doSomething()
{
    // 全局变量在文件各处可见可用
    g_x = 3;
    std::cout << g_x << '\n';
}

int main()
{
    doSomething();
    std::cout << g_x << '\n';

    // 全局变量在文件各处可见可用
    g_x = 5;
    std::cout << g_x << '\n';

    return 0;
}
// g_x 在此处离开作用域
```

上述示例输出：

```
3
3
5
```

全局变量的作用域  
----------------  

在全局命名空间（global namespace）中声明的标识符具有**全局命名空间作用域**（通常称为**全局作用域**，有时非正式称为**文件作用域**），这意味着它们从声明点开始到文件结束都可见。

一旦声明后，全局变量可以在文件后续的任何位置使用！在上例中，全局变量`g_x`在函数`doSomething()`和`main()`中都被使用。

全局变量也可以定义在用户自定义的命名空间（namespace）中。以下是相同示例，但`g_x`被移入用户自定义命名空间`Foo`：

```cpp
#include <iostream>

namespace Foo // Foo 定义在全局作用域
{
    int g_x {}; // g_x 现在位于 Foo 命名空间，但仍是全局变量
}

void doSomething()
{
    // 全局变量在文件各处可见可用
    Foo::g_x = 3;
    std::cout << Foo::g_x << '\n';
}

int main()
{
    doSomething();
    std::cout << Foo::g_x << '\n';

    // 全局变量在文件各处可见可用
    Foo::g_x = 5;
    std::cout << Foo::g_x << '\n';

    return 0;
}
```

尽管`g_x`标识符现在被限制在`namespace Foo`的作用域内，该名称仍可通过`Foo::g_x`全局访问，`g_x`依然是全局变量。

> **关键洞察**  
> 声明在命名空间内的变量仍然是全局变量。

最佳实践  
----------------  

优先将全局变量定义在命名空间而非全局命名空间中。

全局变量的存储期  
----------------  

全局变量在程序启动时（`main()`执行前）创建，在程序终止时销毁。这称为**静态存储期（static duration）**。具有静态存储期的变量有时称为**静态变量（static variables）**。

全局变量的命名  
----------------  

按照惯例，开发者常在全局变量标识符前添加"g"或"g_"前缀以表明其全局性。这种前缀有以下作用：

* 避免与全局命名空间中的其他标识符命名冲突
* 防止意外名称遮蔽（详见课程[7.5 — 变量遮蔽（名称隐藏）](Chapter-7/lesson7.5-variable-shadowing-name-hiding.md)）
* 表明带前缀的变量在函数作用域外持续存在，对其的修改也将持续

定义在用户自定义命名空间中的全局变量通常省略前缀（因为前两点在此情况下不再适用，且通过命名空间前缀可推断变量为全局）。但保留前缀作为更显眼的提醒仍无妨。

最佳实践  
----------------  

命名全局变量（尤其是定义在全局命名空间中的）时考虑使用"g"或"g_"前缀，以便与局部变量和函数参数区分。

> **作者说明**  
> 有时读者会质疑"g_"等前缀是否合适，因其被视作[匈牙利命名法](https://en.wikipedia.org/wiki/Hungarian_notation)而认为"匈牙利命名法不好"。  
>  
> 对匈牙利命名法的主要反对意见源自使用类型前缀（如`nAge`的`n`表示整型），这在现代C++中作用有限。  
>  
> 但使用前缀（如`g`/`g_`、`s`/`s_`、`m`/`m_`）表示变量的作用域或存储期确实有价值，如本节所述原因。

全局变量的初始化  
----------------  

与默认不初始化的局部变量不同，具有静态存储期的变量默认进行零初始化（zero-initialized）。

非常量（non-constant）全局变量可选择初始化：

```cpp
int g_x;       // 无显式初始化（默认零初始化）
int g_y {};    // 值初始化（结果为零初始化）
int g_z { 1 }; // 列表初始化指定值
```

常量全局变量  
----------------  

与局部变量类似，全局变量可以是常量。所有常量（constant）全局变量必须初始化：

```cpp
#include <iostream>

const int g_x;     // 错误：常量变量必须初始化
constexpr int g_w; // 错误：constexpr变量必须初始化

const int g_y { 1 };     // const全局变量 g_y，带值初始化
constexpr int g_z { 2 }; // constexpr全局变量 g_z，带值初始化

void doSomething()
{
    // 全局变量在文件各处可见可用
    std::cout << g_y << '\n';
    std::cout << g_z << '\n';
}

int main()
{
    doSomething();

    // 全局变量在文件各处可见可用
    std::cout << g_y << '\n';
    std::cout << g_z << '\n';

    return 0;
}
// g_y 和 g_z 在此处离开作用域
```

相关阅读  
----------------  

我们将在课程[7.10 — 跨文件共享全局常量（使用内联变量）](Chapter-7/lesson7.10-sharing-global-constants-across-multiple-files-using-inline-variables.md)详细讨论全局常量。

关于（非常量）全局变量的警告  
----------------  

新手常倾向于大量使用全局变量，因为它们无需显式传递给每个需要的函数。然而，通常应完全避免使用非常量（non-const）全局变量！我们将在后续课程[7.8 — 为何（非常量）全局变量有害](Chapter-7/lesson7.8-why-non-const-global-variables-are-evil.md)讨论原因。

快速总结  
----------------  

```cpp
// 非常量全局变量
int g_x;                 // 定义未初始化的全局变量（默认零初始化）
int g_x {};              // 定义显式值初始化的全局变量
int g_x { 1 };           // 定义显式初始化的全局变量

// 常量全局变量
const int g_y;           // 错误：常量变量必须初始化
const int g_y { 2 };     // 定义初始化的全局常量

// constexpr全局变量
constexpr int g_y;       // 错误：constexpr变量必须初始化
constexpr int g_y { 3 }; // 定义初始化的全局constexpr
```

[下一课 7.5 变量遮蔽（名称隐藏）](Chapter-7/lesson7.5-variable-shadowing-name-hiding.md)  
[返回主页](/)  
[上一课 7.3 局部变量](Chapter-7/lesson7.3-local-variables.md)