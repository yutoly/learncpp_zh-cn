12.12 — 返回引用与返回地址  
==================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年2月25日 下午9:04（PST） / 2025年1月3日  

在前文中我们讨论过，当按值（by value）传递参数时，会将参数的副本传入函数。对于基础类型（复制成本低）这没有问题，但类类型（如`std::string`）的复制通常成本较高。我们可以通过传递（常量）引用或地址来避免昂贵复制。  

返回值时也存在类似情况：返回值的副本会被传递回调用方。如果函数返回类型是类类型，这种操作可能代价高昂：  

```
std::string returnByValue(); // 返回std::string的副本（昂贵）
```  

**返回引用（Return by reference）**  
当需要向调用方返回类类型时，我们可以选择返回引用。**返回引用**会返回一个绑定到被返回对象的引用，避免复制返回值。要返回引用，只需将函数返回类型定义为引用类型：  

```
std::string&       returnByReference(); // 返回现有std::string的引用（廉价）
const std::string& returnByReferenceToConst(); // 返回现有std::string的常量引用（廉价）
```  

以下示例演示返回引用的机制：  

```
#include <iostream>
#include <string>

const std::string& getProgramName() // 返回常量引用
{
    static const std::string s_programName { "Calculator" }; // 具有静态存储期，程序结束时销毁
    return s_programName;
}

int main()
{
    std::cout << "This program is named " << getProgramName();
    return 0;
}
```  

该程序输出：  

```
This program is named Calculator
```  

由于`getProgramName()`返回常量引用，执行`return s_programName`时会返回`s_programName`的常量引用（避免复制）。调用方通过该引用访问`s_programName`的值进行打印。  

**返回引用的对象必须在函数返回后存在**  
使用返回引用有个重要限制：程序员必须确保被引用对象的生命周期长于返回引用的函数。否则返回的引用将成为悬垂引用（dangling reference，指向已销毁对象），使用该引用会导致未定义行为。  

修改上例演示悬垂引用情况：  

```
#include <iostream>
#include <string>

const std::string& getProgramName()
{
    const std::string programName { "Calculator" }; // 现在是非静态局部变量，函数结束时销毁
    return programName;
}

int main()
{
    std::cout << "This program is named " << getProgramName(); // 未定义行为
    return 0;
}
```  

此程序结果未定义。当`getProgramName()`返回时，返回的是绑定到局部变量`programName`的引用。由于`programName`是自动存储期的局部变量，函数结束时被销毁，导致返回的引用悬垂。  

> **警告**  
> 返回引用的对象必须比返回引用的函数存在更久，否则会产生悬垂引用。切勿返回（非静态）局部变量或临时对象的引用。  

**生命周期延长不跨越函数边界**  
观察返回临时对象引用的示例：  

```
#include <iostream>

const int& returnByConstReference()
{
    return 5; // 返回临时对象的常量引用
}

int main()
{
    const int& ref { returnByConstReference() };
    std::cout << ref; // 未定义行为
    return 0;
}
```  

在此示例中，函数返回整数字面量，但返回类型是`const int&`，这会创建并返回绑定到临时对象（保存值5）的临时引用。该引用被复制到调用方作用域的临时引用中，临时对象随后销毁，导致调用方的临时引用悬垂。  

**不要通过引用返回非const静态局部变量**  
原始示例中返回const静态局部变量引用是为了简单演示机制。但返回非const静态局部变量引用不符合惯用法，通常应避免：  

```
#include <iostream>
#include <string>

const int& getNextId()
{
    static int s_x{ 0 }; // 注意：变量为非const
    ++s_x; // 生成下一个ID
    return s_x; // 返回其引用
}

int main()
{
    const int& id1 { getNextId() }; // id1是引用
    const int& id2 { getNextId() }; // id2是引用
    std::cout << id1 << id2 << '\n'; // 输出22
    return 0;
}
```  

此程序输出`22`，因为`id1`和`id2`引用同一对象（静态变量`s_x`）。修改该值时，所有引用都访问修改后的值。  

> **最佳实践**  
> 避免返回非const局部静态变量的引用。  

**用返回引用初始化/赋值普通变量会创建副本**  
如果函数返回引用，且该引用用于初始化或赋值给非引用变量，将创建返回值的副本（如同按值返回）：  

```
#include <iostream>
#include <string>

const int& getNextId()
{
    static int s_x{ 0 };
    ++s_x;
    return s_x;
}

int main()
{
    const int id1 { getNextId() }; // id1是普通变量，获得副本
    const int id2 { getNextId() }; // id2同理
    std::cout << id1 << id2 << '\n'; // 输出12
    return 0;
}
```  

**返回引用参数是安全的**  
若参数通过引用传入函数，安全返回该参数引用是可行的。因为参数必须存在于调用方作用域中，函数返回时对象仍存在。  

**通过const引用传递的右值可安全返回**  
当const引用参数接收右值时，仍可安全返回该const引用。因为右值在完整表达式结束时才销毁。  

**调用方可通过引用修改值**  
当函数返回非const引用时，调用方可通过该引用修改被返回的值：  

```
#include <iostream>

int& max(int& x, int& y)
{
    return (x > y) ? x : y;
}

int main()
{
    int a{ 5 };
    int b{ 6 };
    max(a, b) = 7; // 将较大的数设为7
    std::cout << a << b << '\n'; // 输出57
    return 0;
}
```  

**返回地址（Return by address）**  
**返回地址**与返回引用几乎相同，区别在于返回的是对象指针而非引用。主要缺点与返回引用相同——返回地址的对象必须比函数存在更久，否则调用方获得悬垂指针。  

主要优势是可通过返回`nullptr`表示无有效对象。主要危险是调用方必须检查空指针，否则解引用会导致未定义行为。  

> **最佳实践**  
> 除非需要返回"无对象"（使用`nullptr`），否则优先选择返回引用而非地址。  

[下一课 12.13 — 输入与输出参数](Chapter-12/lesson12.13-in-and-out-parameters.md)  
[返回主页](/)  
[上一课 12.11 — 按地址传递（下）](Chapter-12/lesson12.11-pass-by-address-part-2.md)