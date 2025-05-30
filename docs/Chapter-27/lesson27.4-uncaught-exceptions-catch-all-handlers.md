27.4 — 未捕获异常（uncaught exceptions）与全捕获处理程序（catch-all handlers）  
===================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月12日（首次发布于2008年10月25日）  

至此，您应该对异常（exceptions）机制有了基本理解。本章节我们将探讨更多有趣的异常案例。

未捕获异常  
----------------  

当函数抛出未自行处理的异常时，它默认调用栈（call stack）中的某个函数会处理该异常。以下示例中，mySqrt()假设有人会处理其抛出的异常——但如果实际无人处理会发生什么？

这是我们的平方根程序（移除了main()中的try块）：

```cpp
#include <iostream>
#include <cmath> // 包含sqrt函数

// 模块化平方根函数
double mySqrt(double x)
{
    // 用户输入负数时触发错误条件
    if (x < 0.0)
        throw "无法计算负数平方根"; // 抛出const char*类型异常

    return std::sqrt(x);
}

int main()
{
    std::cout << "输入数字：";
    double x;
    std::cin >> x;

    // 注意：无异常处理器！
    std::cout << x << "的平方根是" << mySqrt(x) << '\n';

    return 0;
}
```

假设用户输入-4，mySqrt(-4)将抛出异常。函数mySqrt()未处理该异常，程序将检查调用栈中的其他函数是否处理。main()同样没有对应异常处理器，最终无法找到处理程序。

当未找到异常处理器时，将调用std::terminate()终止程序。此时，调用栈可能不会展开（unwound）！若栈未展开，局部变量不会被销毁，预期的清理操作也不会执行！

> **警告**  
> 未处理异常可能导致调用栈不展开。  
> 若栈未展开，局部变量不会销毁（尤其当这些变量具有非平凡析构函数时可能引发问题）。

题外话...  
虽然不展开栈看似奇怪，但有其合理原因。未处理异常是应极力避免的情况。若展开栈，关于异常抛出位置的调用栈调试信息将丢失！保留未展开的栈可完整保存这些信息，便于诊断未处理异常的根源。

当异常未处理时，操作系统通常会通知未处理异常错误。具体形式因系统而异，可能包括：打印错误信息、弹出错误对话框或直接崩溃。某些系统处理方式不够优雅，这种情况应尽量避免！

全捕获处理程序  
----------------  

现在我们面临一个难题：
* 函数可能抛出任意数据类型异常（包括用户自定义类型），意味着需捕获的异常类型无限多
* 若异常未被捕获，程序将立即终止（且调用栈可能未展开，导致清理不彻底）
* 为所有可能类型编写显式catch处理器过于繁琐（尤其非常规路径的异常）

C++提供了捕获所有类型异常的机制——**全捕获处理程序（catch-all handler）**。该处理程序使用省略号运算符（...）作为捕获类型，故亦称"省略号捕获处理器"。

回忆[20.5 — 省略号及其避免原因](Chapter-20/lesson20.5-ellipsis-and-why-to-avoid-them.md)，省略号曾用于传递任意类型参数。在此上下文中，它表示捕获任意数据类型的异常。示例如下：

```cpp
#include <iostream>

int main()
{
    try
    {
        throw 5; // 抛出int类型异常
    }
    catch (double x)
    {
        std::cout << "捕获double类型异常：" << x << '\n';
    }
    catch (...) // 全捕获处理器
    {
        std::cout << "捕获未知类型异常\n";
    }
}
```

由于没有int类型的显式处理器，全捕获处理器将捕获此异常。输出结果：

```
捕获未知类型异常
```

全捕获处理器必须置于catch链末尾，以确保特定类型的异常优先被专用处理器捕获。

通常全捕获处理器块留空：

```cpp
catch(...) {} // 忽略未预期的异常
```

这将捕获所有未预期异常，确保栈展开至该点并阻止程序终止，但不进行具体错误处理。

用全捕获处理器包装main()  
----------------  

全捕获处理器的典型应用是包装main()函数内容：

```cpp
#include <iostream>

struct GameSession
{
    // 游戏会话数据
};

void runGame(GameSession&)
{
    throw 1;
}

void saveGame(GameSession&)
{
    // 保存用户游戏进度
}

int main()
{
    GameSession session{};

    try
    {
        runGame(session);
    }
    catch(...)
    {
        std::cerr << "异常终止\n";
    }

    saveGame(session); // 保存游戏（即使触发全捕获处理器）

    return 0;
}
```

此例中，若runGame()或其调用函数抛出未处理异常，将被全捕获处理器捕获。调用栈将有序展开（确保局部变量销毁），避免立即终止程序，让我们有机会打印自定义错误并保存用户状态后再退出。

> **技巧**  
> 若程序使用异常，建议在main()中使用全捕获处理器，确保未捕获异常时的有序处理。  
> 捕获异常后应假定程序处于不确定状态，立即清理并终止。

调试未处理异常  
----------------  

未处理异常表明发生意外情况，通常需要诊断其根源。许多调试器可配置为在未处理异常时中断，允许查看异常抛出点的调用栈。但若使用全捕获处理器，所有异常都被处理（且调用栈展开），将丢失重要诊断信息。

因此在调试版本中，禁用全捕获处理器很有用。可通过条件编译指令实现：

```cpp
#include <iostream>

struct GameSession
{
    // 游戏会话数据
};

void runGame(GameSession&)
{
    throw 1;
}

void saveGame(GameSession&)
{
    // 保存用户游戏进度
}

class DummyException // 不可实例化的虚拟类
{
    DummyException() = delete;
}; 

int main()
{
    GameSession session {}; 

    try
    {
        runGame(session);
    }
#ifndef NDEBUG // 发布版本
    catch(...) // 编译全捕获处理器
    {
        std::cerr << "异常终止\n";
    }
#else // 调试版本
    catch(DummyException) // 语法占位（永不触发）
    {
    }
#endif

    saveGame(session); // 保存游戏（即使触发处理器）

    return 0;
}
```

语法上，try块必须关联至少一个catch块。若全捕获处理器被条件编译排除，需要条件编译排除整个try块或编译其他catch块。后者更简洁。

为此创建无法实例化的DummyException类（删除默认构造函数）。当定义NDEBUG时，编译捕获DummyException的处理器。由于无法创建该类型异常，此处理器永不触发，任何到达此处的异常都将未处理。

[下一课 27.5 异常、类与继承](Chapter-27/lesson27.5-exceptions-classes-and-inheritance.md)  
[返回主页](/)  
[上一课 27.3 异常、函数与栈展开](Chapter-27/lesson27.3-exceptions-functions-and-stack-unwinding.md)