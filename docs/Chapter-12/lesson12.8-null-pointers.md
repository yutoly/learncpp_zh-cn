12.8 — 空指针  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年8月12日 下午12:53（太平洋夏令时间）  
2025年2月5日更新  

在上节课（[12.7 — 指针简介](Chapter-12/lesson12.7-introduction-to-pointers.md)）中，我们介绍了指针的基础知识——指针是存储其他对象地址的对象。可以通过解引用（dereference）运算符（*）访问该地址对应的对象：  
```cpp
#include <iostream>

int main()
{
    int x{ 5 };
    std::cout << x << '\n'; // 输出变量x的值

    int* ptr{ &x }; // ptr存储x的地址
    std::cout << *ptr << '\n'; // 通过解引用运算符输出ptr所存地址（即x的地址）对应的对象值

    return 0;
}
```
上述示例输出：  
```
5
5

```  
上节课我们还提到，指针并非必须指向某个对象。本章将深入探讨这种特殊指针（即不指向任何对象的指针）及其相关影响。  

空指针（Null pointers）  
----------------  

除了内存地址外，指针还可以持有另一种特殊值：空值（null value）。**空值**（常简称为**空（null）**）是表示"无值"的特殊值。当指针持有空值时，表示该指针未指向任何对象。这样的指针称为**空指针（null pointer）**。  

创建空指针最简单的方式是使用值初始化：  
```cpp
int main()
{
    int* ptr {}; // ptr现在是空指针，未持有任何地址
 
    return 0;
}
```  
最佳实践  
若未用有效对象地址初始化指针，应对其进行值初始化（设为空指针）。  

通过赋值操作，我们可以改变指针指向的对象。初始化为空的指针后续可被修改为指向有效对象：  
```cpp
#include <iostream>

int main()
{
    int* ptr {}; // ptr是空指针，未持有任何地址

    int x { 5 };
    ptr = &x; // ptr现在指向对象x（不再是空指针）

    std::cout << *ptr << '\n'; // 通过解引用ptr输出x的值
 
    return 0;
}
```  

nullptr关键字  
----------------  

如同`true`和`false`表示布尔字面量，**nullptr**关键字表示空指针字面量（null pointer literal）。我们可以用`nullptr`显式初始化指针或为指针赋空值：  
```cpp
int main()
{
    int* ptr { nullptr }; // 使用nullptr初始化指针为空指针

    int value { 5 };
    int* ptr2 { &value }; // ptr2是有效指针
    ptr2 = nullptr; // 通过赋值nullptr使指针成为空指针

    someFunction(nullptr); // 也可将nullptr传递给接受指针参数的函数

    return 0;
}
```  
最佳实践  
当需要为空指针进行初始化、赋值或传递空指针给函数时，应使用`nullptr`。  

解引用空指针导致未定义行为  
----------------  

与解引用悬垂指针（dangling pointer）或野指针（wild pointer）类似，解引用空指针也会导致未定义行为（undefined behavior）。多数情况下这将导致程序崩溃。以下程序演示了这种情况（尝试运行不会损坏计算机）：  
```cpp
#include <iostream>

int main()
{
    int* ptr {}; // 创建空指针
    std::cout << *ptr << '\n'; // 解引用空指针

    return 0;
}
```  
从概念上说，这种操作显然存在问题。解引用指针意味着"前往指针所指地址并访问该处值"。空指针持有空值，语义上即表示指针未指向任何对象，因此访问操作无法执行。  

意外解引用空指针和悬垂指针是C++程序员最常见的错误之一，也是实践中导致程序崩溃的主要原因。  

警告  
使用指针时，必须特别注意代码是否在解引用空指针或悬垂指针，这将导致未定义行为（通常表现为程序崩溃）。  

检查空指针  
----------------  

如同用条件语句测试布尔值的真伪，我们可用条件语句测试指针是否为`nullptr`：  
```cpp
#include <iostream>

int main()
{
    int x { 5 };
    int* ptr { &x };

    if (ptr == nullptr) // 显式判空
        std::cout << "ptr是空指针\n";
    else
        std::cout << "ptr非空\n";

    int* nullPtr {};
    std::cout << "nullPtr是" << (nullPtr==nullptr ? "空指针\n" : "非空指针\n"); // 显式判空

    return 0;
}
```  
输出：  
```
ptr非空
nullPtr是空指针

```  
在[4.9 — 布尔值](Chapter-4/lesson4.9-boolean-values.md)课程中，我们提到整型值会隐式转换为布尔值：整型`0`转为`false`，其他值转为`true`。类似地，指针也会隐式转换为布尔值：空指针转为`false`，非空指针转为`true`。这使得我们可以省略显式的`nullptr`检测，直接通过隐式转换判断指针是否为空：  
```cpp
#include <iostream>

int main()
{
    int x { 5 };
    int* ptr { &x };

    // 指针为空时转为false，非空时转为true
    if (ptr) // 隐式转换为布尔值
        std::cout << "ptr非空\n";
    else
        std::cout << "ptr是空指针\n";

    int* nullPtr {};
    std::cout << "nullPtr是" << (nullPtr ? "非空指针\n" : "空指针\n"); // 隐式转换

    return 0;
}
```  
警告  
条件语句只能区分空指针与非空指针，无法方便地判断非空指针是否指向有效对象或已成为悬垂指针。  

使用nullptr避免悬垂指针  
----------------  

前文提到解引用空指针或悬垂指针都会导致未定义行为。因此需要确保代码不执行此类操作。  

通过条件语句确保指针非空后再解引用，可避免解引用空指针：  
```cpp
// 假设ptr是可能为空指针的某个指针
if (ptr) // 若ptr非空
    std::cout << *ptr << '\n'; // 安全解引用
else
    // 执行其他不涉及解引用ptr的操作（如输出错误信息等）
```  

对于悬垂指针，由于无法检测其存在，必须通过确保所有不指向有效对象的指针都被设为`nullptr`来避免悬垂指针的产生。这样在解引用前只需检测指针是否为空，并假定所有非空指针均为有效。  

最佳实践  
指针应始终持有有效对象地址或设为nullptr。如此只需检测指针是否为空，并假定所有非空指针均有效。  

但避免悬垂指针并非易事：当对象被销毁时，指向它的所有指针都会变为悬垂指针。这些指针*不会*被自动设为`nullptr`！程序员有责任确保所有指向已销毁对象的指针被正确设为`nullptr`。  

警告  
当对象被销毁时，指向它的所有指针将变为悬垂指针（不会被自动设为`nullptr`）。程序员需检测这些情况并确保相关指针后续被设为`nullptr`。  

传统空指针字面量：0与NULL  
----------------  

在旧代码中，可能看到使用其他字面量代替`nullptr`。  

第一种是字面量`0`。在指针上下文中，`0`被特殊定义为空值，这也是唯一可将整型字面量赋值给指针的情况：  
```cpp
int main()
{
    float* ptr { 0 };  // ptr现在是空指针（示例用，勿实际使用）

    float* ptr2; // ptr2未初始化
    ptr2 = 0; // ptr2现在是空指针（示例用，勿实际使用）

    return 0;
}
```  
补充说明  
在现代架构中，地址`0`通常表示空指针。但C++标准不保证这点，某些架构可能使用其他值。当`0`用于空指针上下文时，会被转换为该架构表示空指针的地址值。  

另一种是预处理器宏`NULL`（定义于\<cstddef\>头文件）。该宏继承自C语言，常用于表示空指针：  
```cpp
#include <cstddef> // 包含NULL定义

int main()
{
    double* ptr { NULL }; // ptr是空指针

    double* ptr2; // ptr2未初始化
    ptr2 = NULL; // ptr2现在是空指针

    return 0;
}
```  
现代C++中应避免使用`0`和`NULL`（改用`nullptr`）。具体原因将在[12.11 — 按地址传递（下）](Chapter-12/lesson12.11-pass-by-address-part-2.md)讨论。  

优先使用引用而非指针  
----------------  

指针和引用都能间接访问其他对象。  

指针的额外能力包括改变指向对象和指向空值。但这些能力也带来危险：空指针可能被解引用，改变指向对象的能力也更容易产生悬垂指针：  
```cpp
int main()
{
    int* ptr { };
    
    {
        int x{ 5 };
        ptr = &x; // 将指针指向即将销毁的对象（引用无法做到）
    } // ptr现在成为悬垂指针，指向无效对象

    if (ptr) // 条件判断为true（因ptr非空）
        std::cout << *ptr; // 未定义行为

    return 0;
}
```  

由于引用不能绑定到空值，我们无需担心空引用。且引用必须在创建时绑定有效对象且不可重新绑定，因此更难产生悬垂引用。  

鉴于引用更安全，除非需要指针的额外功能，否则应优先使用引用。  

最佳实践  
除非需要指针的额外功能，否则应优先使用引用。  

趣味段子  
----------------  

听说过关于空指针的笑话吗？  
没关系，反正你解引用不了。  

测验时间  
----------------  

**问题1a**  
能否判断指针是否为空指针？如何判断？  
  
<details><summary>答案</summary>是，可在条件语句（if语句或条件运算符）中使用指针。若指针为空则转为布尔值false，否则为true。</details>  

**问题1b**  
能否判断非空指针是否有效或已成为悬垂指针？如何判断？  
  
<details><summary>答案</summary>无简便判断方法。</details>  

**问题2**  
对以下行为，判断其结果是：可预测、未定义或可能未定义。若为"可能未定义"，请说明具体情况。假设所有对象类型均与指针兼容。  

**2a** 将对象地址赋给非const指针  
  
<details><summary>答案</summary>可预测。仅复制地址到指针对象。</details>  

**2b** 给指针赋nullptr  
  
<details><summary>答案</summary>可预测。</details>  

**2c** 解引用指向有效对象的指针  
  
<details><summary>答案</summary>可预测。</details>  

**2d** 解引用悬垂指针  
  
<details><summary>答案</summary>未定义。</details>  

**2e** 解引用空指针  
  
<details><summary>答案</summary>未定义。</details>  

**2f** 解引用非空指针  
  
<details><summary>答案</summary>可能未定义（若指针是悬垂指针）。</details>  

**问题3**  
为何应将不指向有效对象的指针设为nullptr？  
  
<details><summary>答案</summary>因无法判断非空指针是否有效或悬垂，而访问悬垂指针会导致未定义行为。因此必须确保程序中不存在悬垂指针。若保证所有指针要么指向有效对象要么为nullptr，则可通过条件检测空指针来避免解引用空指针，并假定所有非空指针均有效。</details>  

[下一课 12.9 指针与const](Chapter-12/lesson12.9-pointers-and-const.md)  
[返回主页](/)  
[上一课 12.7 指针简介](Chapter-12/lesson12.7-introduction-to-pointers.md)