2.1 — 函数入门  
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月28日（首次发布于2007年5月31日）  

前章回顾  
----------------  

前一章我们将**函数（function）**定义为顺序执行的语句集合。虽然正确，但该定义未能充分阐释函数的实用价值。现更新定义：**函数**是为完成特定任务而设计的可复用语句序列。  

已知每个可执行程序必须包含名为`main()`的函数（程序运行时从此处开始执行）。但随着程序规模增长，将所有代码置于`main()`函数中会变得难以管理。函数使我们能将程序拆分为小型模块化单元，更易于组织、测试和使用。  

大多数程序使用众多函数。C++标准库（standard library）提供大量预置函数，但自定义函数同样常见。用户自行编写的函数称为**用户定义函数（user-defined function）**。  

现实场景类比：阅读书籍时需拨打电话，您会在书中放置书签，通话结束后返回标记位置继续阅读。C++程序运作方式类似（并借用了相同术语）。程序在函数内顺序执行语句时若遇到**函数调用（function call）**，CPU将中断当前函数转去执行另一函数。CPU会在当前执行点"放置书签"，执行完被调函数后**返回（return）**书签位置继续执行。  

术语说明  
----------------  
* 发起调用的函数称为**调用者（caller）**  
* 被调用的函数称为**被调函数（callee）**  
* 函数调用有时称为**调用（invocation）**，即调用者**调用（invoke）**被调函数  

用户定义函数示例  
----------------  
首先展示用户定义函数的基本语法结构，后续课程中所有用户定义函数将采用以下形式：  
```cpp
返回类型 函数名() // 函数头（向编译器声明函数存在）
{
    // 函数体（定义函数功能）
}
```  

* 首行称为**函数头（function header）**，告知编译器函数存在性、名称等信息（返回类型等细节后续课程讲解）  
* 本课程中，`main()`使用`int`返回类型，其他函数使用`void`。关于返回类型与返回值的深入讨论详见[2.2 — 函数返回值（值返回函数）](Chapter-2/lesson2.2-function-return-values-value-returning-functions.md)  
* 函数名遵循变量命名规则，称为**标识符（identifier）**  
* 函数名后的圆括号表明这是函数定义  

花括号及其内部语句构成**函数体（function body）**，定义函数具体功能。  

调用函数时使用函数名加圆括号（如`函数名()`）。约定俗成，圆括号紧接函数名（无空格）。  

当前要求函数必须先定义后调用，解决方法详见[2.7 — 前向声明与定义](Chapter-2/lesson2.7-forward-declarations.md)。  

以下示例程序演示用户定义函数的定义与调用：  
```cpp
#include <iostream> // 用于std::cout

// 用户定义函数doPrint()定义
// 本例中被调函数为doPrint()
void doPrint()
{
    std::cout << "In doPrint()\n";
}

// 用户定义函数main()定义
int main()
{
    std::cout << "Starting main()\n";
    doPrint();                        // 中断main()调用doPrint()，main()为调用者
    std::cout << "Ending main()\n";   // 该语句在doPrint()结束后执行

    return 0;
}
```  
程序输出：  
```
Starting main()
In doPrint()
Ending main()
```  

程序执行流程：  
1. 从`main()`函数顶部开始执行，首条语句输出`Starting main()`  
2. `main()`中第二条语句调用`doPrint()`函数（尾随圆括号表明函数调用）  

> **警告**  
> 调用函数时勿遗漏函数名后的圆括号`()`，否则可能导致编译失败（即使通过编译，函数也不会被调用）  

函数调用导致`main()`执行中断，转至`doPrint()`函数顶部。`doPrint()`中唯一语句输出`In doPrint()`。函数结束后返回调用者`main()`，从调用点之后继续执行，下条语句输出`Ending main()`。  

多次调用函数  
----------------  
函数的重要特性是可重复调用。示例程序：  
```cpp
#include <iostream> // 用于std::cout

void doPrint()
{
    std::cout << "In doPrint()\n";
}

// main()函数定义
int main()
{
    std::cout << "Starting main()\n";
    doPrint(); // 第一次调用
    doPrint(); // 第二次调用
    std::cout << "Ending main()\n";

    return 0;
}
```  
输出：  
```
Starting main()
In doPrint()
In doPrint()
Ending main()
```  

由于`main()`两次调用`doPrint()`，该函数执行两次，`In doPrint()`输出两次。  

函数嵌套调用  
----------------  
`main()`可调用其他函数（如前例中的`doPrint()`），被调函数亦可调用其他函数（可多层嵌套）。下例中`main()`调用`doA()`，后者调用`doB()`：  
```cpp
#include <iostream> // 用于std::cout

void doB()
{
    std::cout << "In doB()\n";
}

void doA()
{
    std::cout << "Starting doA()\n";
    doB();
    std::cout << "Ending doA()\n";
}

// main()函数定义
int main()
{
    std::cout << "Starting main()\n";
    doA();
    std::cout << "Ending main()\n";
    return 0;
}
```  
输出：  
```
Starting main()
Starting doA()
In doB()
Ending doA()
Ending main()
```  

不支持嵌套函数  
----------------  
在C++中，**嵌套函数（nested function）**（即定义在其他函数内部的函数）不被允许。以下程序非法：  
```cpp
#include <iostream>

int main()
{
    void foo() // 非法：该函数嵌套于main()内部
    {
        std::cout << "foo!\n";
    }

    foo(); // 调用foo()
    return 0;
}
```  

正确写法：  
```cpp
#include <iostream>

void foo() // 移出main()
{
    std::cout << "foo!\n";
}

int main()
{
    foo();
    return 0;
}
```  

术语说明  
----------------  
"foo"是无实际含义的占位名称，用于演示概念时命名不重要的情况，这类名称称为**元语法变量（metasyntactic variable）**（俗称占位名）。C++中常见占位名还有"bar"、"baz"及以"oo"结尾的三字母词（如"goo"、"moo"、"boo"）。  

词源爱好者可参阅[RFC 3092](https://datatracker.ietf.org/doc/html/rfc3092)了解相关术语演变。  

测验时间  
----------------  
**问题1**  
函数定义中，花括号及其内部语句称为什么？  
  
<details><summary>答案</summary>函数体</details>  

**问题2**  
以下程序输出什么？（勿编译，手动追踪代码）  
```cpp
#include <iostream> // 用于std::cout

void doB()
{
    std::cout << "In doB()\n";
}

void doA()
{
    std::cout << "In doA()\n";
    doB();
}

// main()函数定义
int main()
{
    std::cout << "Starting main()\n";
    doA();
    doB();
    std::cout << "Ending main()\n";
    return 0;
}
```  
  
<details><summary>答案</summary>  
Starting main()  
In doA()  
In doB()  
In doB()  
Ending main()  
</details>  

[下一课 2.2 函数返回值（值返回函数）](Chapter-2/lesson2.2-function-return-values-value-returning-functions.md)  
[返回主页](/)  
[上一课 1.x 第1章总结与测验](Chapter-1/lesson1.x-chapter-1-summary-and-quiz.md)  