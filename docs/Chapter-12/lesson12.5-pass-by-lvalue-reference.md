12.5 — 按左值引用传递  
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年7月24日 PDT时间下午6:06  
2024年12月6日更新  

在前几课中，我们介绍了左值引用（lvalue references）（[12.3 — 左值引用](Chapter-12/lesson12.3-lvalue-references.md)）和const左值引用（[12.4 — const左值引用](Chapter-12/lesson12.4-lvalue-references-to-const.md)）。单独来看，这些概念似乎并不实用——当可以直接使用变量本身时，为什么要创建别名？  

本课将揭示引用的实用价值。从本章后续内容开始，您将频繁看到引用的应用场景。  

首先回顾背景知识。在课程[2.4 — 函数参数与实参简介](Chapter-2/lesson2.4-introduction-to-function-parameters-and-arguments.md)中，我们讨论了**按值传递（pass by value）**——传递给函数的实参会被复制到函数形参中：  
```
#include <iostream>

void printValue(int y)
{
    std::cout << y << '\n';
} // y在此处被销毁

int main()
{
    int x { 2 };

    printValue(x); // x按值传递（复制）给形参y（低开销）

    return 0;
}
```  
上述程序中，当调用`printValue(x)`时，x的值（2）被*复制*到形参y中。函数结束时，对象y被销毁。  

这意味着每次调用函数时，我们都会创建实参值的副本，而该副本仅被短暂使用后即被销毁！幸运的是，基础类型的复制成本低廉，这不会造成问题。  

**昂贵复制的对象**  
标准库提供的大多数类型（如`std::string`）都是类类型。类类型通常复制成本较高。我们应尽可能避免对高成本复制对象进行不必要的复制，尤其是当这些副本几乎立即被销毁时。  

以下程序演示了这一点：  
```
#include <iostream>
#include <string>

void printValue(std::string y)
{
    std::cout << y << '\n';
} // y在此处被销毁

int main()
{
    std::string x { "Hello, world!" }; // x是std::string类型

    printValue(x); // x按值传递（复制）给形参y（高开销）

    return 0;
}
```  
输出：  
```
Hello, world!
```  
虽然程序运行正常，但效率低下。与前例类似，当`printValue()`被调用时，实参x被复制到形参y。但本例中实参是`std::string`而非`int`，而`std::string`是高复制成本的类类型。每次调用`printValue()`都会产生这种昂贵复制！  

我们可以优化这个流程。  

**按引用传递**  
避免函数调用时复制高成本实参的方法之一是使用**按引用传递（pass by reference）**代替按值传递。使用按引用传递时，我们将函数形参声明为引用类型（或const引用类型）而非普通类型。函数被调用时，每个引用形参会绑定到对应实参。由于引用作为实参的别名，因此不会创建副本。  

以下是改用按引用传递的相同示例：  
```
#include <iostream>
#include <string>

void printValue(std::string& y) // 类型改为std::string&
{
    std::cout << y << '\n';
} // y在此处被销毁

int main()
{
    std::string x { "Hello, world!" };

    printValue(x); // x现在通过引用传递给形参y（低开销）

    return 0;
}
```  
该程序与前例完全相同，只是形参y的类型从`std::string`改为`std::string&`（左值引用）。现在调用`printValue(x)`时，左值引用形参y绑定到实参x。绑定引用始终是低成本操作，且无需创建x的副本。由于引用作为被引用对象的别名，当`printValue()`使用引用y时，实际访问的是原始实参x（而非x的副本）。  

**关键洞察**  
按引用传递允许我们在不复制参数的情况下将其传入函数。  

以下程序演示值参数是与实参分离的独立对象，而引用参数被视为实参本身：  
```
#include <iostream>

void printAddresses(int val, int& ref)
{
    std::cout << "值参数的地址是：" << &val << '\n';
    std::cout << "引用参数的地址是：" << &ref << '\n';   
}

int main()
{
    int x { 5 };
    std::cout << "x的地址是：" << &x << '\n';
    printAddresses(x, x);

    return 0;
}
```  
运行示例输出：  
```
x的地址是：0x7ffd16574de0
值参数的地址是：0x7ffd16574de4
引用参数的地址是：0x7ffd16574de0
```  
可见实参与值参数具有不同地址，说明值参数是独立对象。由于它们拥有独立内存地址，为了保持值参数与实参值相同，必须将实参值复制到值参数的内存中。  

而引用参数的地址与实参完全相同，说明引用参数被视为与实参是同一对象。  

**按引用传递允许修改实参值**  
当对象按值传递时，函数形参接收实参的副本。这意味着对形参值的修改仅作用于实参副本，而非原始实参：  
```
#include <iostream>

void addOne(int y) // y是x的副本
{
    ++y; // 修改x的副本，不影响原始x
}

int main()
{
    int x { 5 };

    std::cout << "值 = " << x << '\n';

    addOne(x);

    std::cout << "值 = " << x << '\n'; // x未被修改

    return 0;
}
```  
输出：  
```
值 = 5
值 = 5
```  
然而由于引用与原始对象行为一致，使用按引用传递时对引用参数的修改*会*影响实参：  
```
#include <iostream>

void addOne(int& y) // y绑定到实际对象x
{
    ++y; // 修改实际对象x
}

int main()
{
    int x { 5 };

    std::cout << "值 = " << x << '\n';

    addOne(x);

    std::cout << "值 = " << x << '\n'; // x已被修改

    return 0;
}
```  
输出：  
```
值 = 5
值 = 6
```  
本例中，x初始值为5。当调用`addOne(x)`时，引用形参y绑定到实参x。`addOne()`函数递增引用y时，实际将实参x从5增加到6（而非修改副本）。此值变化在`addOne()`执行结束后仍然保持。  

**关键洞察**  
通过非const引用传递值允许我们编写能修改实参值的函数。  

函数修改实参值的能力非常实用。例如，假设编写判断怪物是否成功攻击玩家的函数。若攻击成功，怪物应对玩家生命值造成伤害。若通过引用传递玩家对象，函数可直接修改实际传入的玩家对象的生命值。若按值传递，只能修改玩家对象副本的生命值，这显然不够实用。  

**按引用传递仅接受可修改左值实参**  
由于非const值的引用只能绑定到可修改左值（本质上是非const变量），这意味着按引用传递仅适用于可修改左值实参。这实际上严重限制了非const引用传递的实用性，因为无法传递const变量或字面量。例如：  
```
#include <iostream>

void printValue(int& y) // y仅接受可修改左值
{
    std::cout << y << '\n';
}

int main()
{
    int x { 5 };
    printValue(x); // 正确：x是可修改左值

    const int z { 5 };
    printValue(z); // 错误：z是不可修改左值

    printValue(5); // 错误：5是右值

    return 0;
}
```  
幸运的是，下一课将讨论解决此问题的方法。我们还将探讨何时使用按值传递与按引用传递。  

[下一课 12.6 按const左值引用传递](Chapter-12/lesson12.6-pass-by-const-lvalue-reference.md)  
[返回主页](/)  
[上一课 12.4 const左值引用](Chapter-12/lesson12.4-lvalue-references-to-const.md)