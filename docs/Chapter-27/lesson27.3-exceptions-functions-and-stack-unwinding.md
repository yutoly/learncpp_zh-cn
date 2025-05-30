27.3 — 异常处理、函数与栈展开  
==================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月29日（首次发布于2008年10月5日）  

在课程[27.2 — 基础异常处理](Chapter-27/lesson27.2-basic-exception-handling.md)中，我们讲解了throw、try和catch如何协同实现异常处理。本节将探讨异常处理与函数间的交互。  

**被调用函数抛出异常**  
前文提到"try块会检测其中语句抛出的所有异常"。在之前的示例中，throw语句直接位于try块内，并由同函数的catch块捕获。但同一函数内抛出和捕获异常的实际应用有限。  

更有意义的情况是：当try块中的函数调用引发异常时，该异常是否会被检测到？答案显然是肯定的！  

异常处理最实用的特性之一是throw语句无需直接位于try块内。异常可以从函数任意位置抛出，并被调用者的try块（或其更上层调用者）捕获。此时，执行流将从异常抛出点跳转至处理该异常的catch块。  

关键洞察  
try块不仅能捕获其内部语句抛出的异常，还能捕获被调用函数中抛出的异常。  

这使我们能以更模块化的方式使用异常处理。以下通过重构前课的平方根程序来演示：  
```
#include <cmath> // 提供sqrt()函数
#include <iostream>

// 模块化平方根函数
double mySqrt(double x)
{
    if (x < 0.0)
        throw "负数无法开平方"; // 抛出const char*类型异常

    return std::sqrt(x);
}

int main()
{
    std::cout << "输入数字: ";
    double x{};
    std::cin >> x;

    try // 检测try块内的异常并路由到catch块
    {
        double d = mySqrt(x);
        std::cout << x << "的平方根是" << d << '\n';
    }
    catch (const char* exception) // 捕获const char*类型异常
    {
        std::cerr << "错误: " << exception << std::endl;
    }

    return 0;
}
```  
程序中，我们将异常检查和平方根计算封装到模块化函数mySqrt()中，并在try块内调用。验证其功能：  
```
输入数字: -4
错误: 负数无法开平方
```  
当mySqrt()抛出异常时，其内部没有处理程序。但由于在main()的try块中调用，异常被main()的catch块捕获。执行流从mySqrt()的throw跳转至main()的catch块。  

关键点在于mySqrt()抛出异常但不自行处理，将异常处理责任委托给调用者。不同应用场景可能需要不同的错误处理方式：控制台程序打印错误信息，GUI程序弹出对话框等。通过异常传递，各应用能以最适合自身的方式处理错误，保持mySqrt()的模块化。  

**异常处理与栈展开**  
本部分将解析多函数调用时的异常处理机制。  

预备知识  
建议复习课程[20.2 — 栈与堆](Chapter-20/lesson20.2-the-stack-and-the-heap.md)中关于调用栈和栈展开的内容。  

异常抛出时，程序首先检查当前函数能否处理（即异常是否在函数内的try块抛出，且存在匹配的catch块）。若不能处理，则检查调用栈中的上层函数：  

1. 检查调用者函数是否在try块中调用当前函数，且具有匹配的catch块  
2. 若未找到匹配，继续检查更上层调用者  
3. 该过程持续至找到处理程序或遍历完调用栈  

找到匹配的异常处理程序后，执行流从抛出点跳转至catch块顶部。这需要展开调用栈（移除当前函数），直至异常处理函数成为栈顶。  

关键洞察  
栈展开会销毁被展开函数中的局部变量（确保其析构函数执行）。  

**栈展开示例**  
通过多函数调用示例演示该机制：main()调用A()，A()调用B()，B()调用C()，C()调用D()，D()抛出异常。  
```
#include <iostream>

void D() // 由C()调用
{
    std::cout << "进入D\n";
    std::cout << "D抛出int型异常\n";
    throw -1;
    std::cout << "离开D\n"; // 跳过
}

void C() // 由B()调用
{
    std::cout << "进入C\n";
    D();
    std::cout << "离开C\n"; // 跳过
}

void B() // 由A()调用
{
    std::cout << "进入B\n";
    try { C(); }
    catch (double) { std::cerr << "B捕获double异常\n"; } // 类型不匹配，不捕获

    try { /* 空try块 */ }
    catch (int) { std::cerr << "B捕获int异常\n"; } // 未在try块内抛出，不捕获

    std::cout << "离开B\n"; // 跳过
}

void A() // 由main()调用
{
    std::cout << "进入A\n";
    try { B(); }
    catch (int) { std::cerr << "A捕获int异常\n"; } // 捕获并处理
    catch (double) { std::cerr << "A捕获double异常\n"; } // 不执行

    std::cout << "离开A\n"; // 异常处理后继续执行
}

int main()
{
    std::cout << "进入main\n";
    try { A(); }
    catch (int) { std::cerr << "main捕获int异常\n"; } // 异常已处理，不执行
    std::cout << "离开main\n";
    return 0;
}
```  
程序输出：  
```
进入main
进入A
进入B
进入C
进入D
D抛出int型异常
A捕获int异常
离开A
离开main
```  
执行流程解析：  
1. D()抛出int型异常，未自行处理  
2. 检查调用栈：C()无处理程序 → B()  
3. B()的第一个try块catch double不匹配，第二个try块未调用C()  
4. 继续检查A()，其try块内调用B()，catch int匹配异常  
5. A()处理异常后正常执行后续代码  
6. 控制流返回main()时异常已处理，main()继续执行  

该示例说明：  
- 异常的直接调用者可不处理异常（如C()委托给上层）  
- try块若无匹配catch，栈展开照常进行（如B()的情况）  
- 匹配catch块执行后，控制流从catch块后继续  
- 栈展开机制允许在调用链最合适的位置处理错误  

[下一课 27.4 — 未捕获异常与全能捕获](Chapter-27/lesson27.4-uncaught-exceptions-catch-all-handlers.md)  
[返回主页](/)  
[上一课 27.2 — 基础异常处理](Chapter-27/lesson27.2-basic-exception-handling.md)