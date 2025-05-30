12.4 — 对const的左值引用  
==================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2017年6月7日 下午3:30（PDT）  
2025年2月23日  

 

在上节课（[12.3 — 左值引用](Chapter-12/lesson12.3-lvalue-references.md)）中，我们讨论了左值引用只能绑定到可修改的左值。这意味着以下代码是非法的：  

```cpp
int main()
{
    const int x { 5 }; // x是不可修改的（const）左值
    int& ref { x };    // 错误：ref不能绑定到不可修改的左值

    return 0;
}
```  

该操作被禁止的原因是：通过非const引用（ref）可以修改const变量（x）。  

但如果我们想创建指向const变量的引用该怎么办？普通的左值引用（指向非const值）无法满足需求。  

 

对const的左值引用  
----------------  

通过在声明左值引用时使用`const`关键字，我们让左值引用将其指向的对象视为const。这种引用称为**对const值的左值引用**（有时简称为**const引用**或**常量引用**）。  

对const的左值引用可以绑定到不可修改的左值：  

```cpp
int main()
{
    const int x { 5 };    // x是不可修改的左值
    const int& ref { x }; // 正确：ref是对const值的左值引用

    return 0;
}
```  

由于对const的左值引用将其指向的对象视为const，它们可以用于访问但不能修改被引用的值：  

```cpp
#include <iostream>

int main()
{
    const int x { 5 };    // x是不可修改的左值
    const int& ref { x }; // 正确：ref是对const值的左值引用

    std::cout << ref << '\n'; // 正确：可以访问const对象
    ref = 6;                  // 错误：不能通过const引用修改对象
    
    return 0;
}
```  

 

用可修改左值初始化对const的左值引用  
----------------  

对const的左值引用也可以绑定到可修改的左值。在这种情况下，通过引用访问时被引用对象被视为const（即使底层对象是非const的）：  

```cpp
#include <iostream>

int main()
{
    int x { 5 };          // x是可修改的左值
    const int& ref { x }; // 正确：可以将const引用绑定到可修改的左值

    std::cout << ref << '\n'; // 正确：可以通过const引用访问对象
    ref = 7;                  // 错误：不能通过const引用修改对象

    x = 6;                // 正确：x是可修改左值，仍可通过原始标识符修改

    return 0;
}
```  

在上面的程序中，我们将const引用`ref`绑定到可修改左值`x`。之后可以通过`ref`访问`x`，但由于`ref`是const的，不能通过`ref`修改`x`的值。不过仍然可以直接使用标识符`x`修改其值。  

 

最佳实践  
----------------  

优先使用`对const的左值引用`而非`对非const的左值引用`，除非需要修改被引用对象。  

 

用右值初始化对const的左值引用  
----------------  

令人惊讶的是，对const的左值引用也可以绑定到右值：  

```cpp
#include <iostream>

int main()
{
    const int& ref { 5 }; // 正确：5是右值

    std::cout << ref << '\n'; // 打印5

    return 0;
}
```  

当这种情况发生时，会创建一个临时对象并用右值初始化，const引用将绑定到该临时对象。  

 

相关知识点  
----------------  

我们在课程[2.5 — 局部作用域简介](Chapter-2/lesson2.5-introduction-to-local-scope.md)中讨论过临时对象。  

 

用不同类型值初始化对const的左值引用  
----------------  

对const的左值引用甚至可以绑定到不同类型的值，只要这些值可以隐式转换为引用类型：  

```cpp
#include <iostream>

int main()
{
    // 案例1
    const double& r1 { 5 };  // 用值5初始化临时double，r1绑定到临时对象

    std::cout << r1 << '\n'; // 打印5

    // 案例2
    char c { 'a' };
    const int& r2 { c };     // 用值'a'初始化临时int，r2绑定到临时对象

    std::cout << r2 << '\n'; // 打印97（因为r2是int引用）

    return 0;
}
```  

在案例1中，创建了类型为`double`的临时对象并用int值`5`初始化。然后`const double& r1`绑定到该临时double对象。  

在案例2中，创建了类型为`int`的临时对象并用char值`a`初始化。然后`const int& r2`绑定到该临时int对象。  

在这两个案例中，引用类型与临时对象类型匹配。  

 

关键洞察  
----------------  

如果尝试将const左值引用绑定到不同类型的值，编译器会创建与引用类型相同的临时对象，用该值初始化，然后将引用绑定到临时对象。  

还需注意，当打印`r2`时会输出int而非char。这是因为`r2`是int对象的引用（指向创建的临时int），而不是指向char`c`。  

尽管这看起来有些奇怪，但我们将在课程[12.6 — 通过const左值引用传递](Chapter-12/lesson12.6-pass-by-const-lvalue-reference.md)中看到这种用法的实际案例。  

 

警告  
----------------  

我们通常假设引用与其绑定对象完全相同——但当引用绑定到对象的临时副本或转换产生的临时对象时，这种假设会被打破。后续对原始对象的修改将不会反映到引用中（因为引用指向不同对象），反之亦然。  

以下示例演示了这种情况：  

```cpp
#include <iostream>

int main()
{
    short bombs { 1 };         // 我有炸弹！（注意类型是short）
    
    const int& you { bombs };  // 你也有炸弹（注意类型是int&）
    --bombs;                   // 炸弹用完

    if (you)                   // 你还有吗？
    {
        std::cout << "Bombs away!  Goodbye, cruel world.\n"; // 炸弹引爆
    }

    return 0;
}
```  

在上例中，`bombs`是`short`类型，`you`是`const int&`类型。由于`you`只能绑定到`int`对象，当用`bombs`初始化`you`时，编译器会隐式转换`bombs`为`int`，从而创建临时`int`对象（值为`1`）。`you`最终绑定到这个临时对象而非`bombs`。  

当`bombs`递减时，`you`不受影响，因为它引用的是不同对象。因此尽管预期`if (you)`评估为`false`，实际结果为`true`。  

 

绑定到临时对象的const引用会延长临时对象的生命周期  
----------------  

临时对象通常在其创建的表达式结束时销毁。  

对于语句`const int& ref { 5 };`，如果为保存右值`5`创建的临时对象在初始化`ref`的表达式结束时销毁，引用`ref`将悬空（指向已销毁对象），访问`ref`会导致未定义行为。  

为避免这种情况，C++有特殊规则：当const左值引用**直接**绑定到临时对象时，临时对象的生命周期将延长以匹配引用。  

```cpp
#include <iostream>

int main()
{
    const int& ref { 5 }; // 保存值5的临时对象生命周期被延长以匹配ref

    std::cout << ref << '\n'; // 因此可以安全使用

    return 0;
} // ref和临时对象在此处销毁
```  

在上例中，当`ref`用右值`5`初始化时，创建临时对象并将`ref`绑定到它。临时对象的生命周期与`ref`一致。因此可以在后续语句安全地打印`ref`的值。之后`ref`和临时对象在块结束时销毁。  

 

关键洞察  
----------------  

左值引用只能绑定到可修改左值。  

对const的左值引用可以绑定到可修改左值、不可修改左值和右值。这使其成为更灵活的引用类型。  

 

进阶阅读  
----------------  

生命周期延长仅适用于const引用直接绑定临时对象的情况。从函数返回的临时对象（即使通过const引用返回）不符合生命周期延长条件。  

我们在课程[12.12 — 通过引用返回与通过地址返回](Chapter-12/lesson12.12-return-by-reference-and-return-by-address.md)中展示了相关示例。  

对于类类型右值，绑定到成员的引用会延长整个对象的生命周期。  

 

为什么C++允许const引用绑定右值？我们将在下节课解答！  

 

constexpr左值引用（可选内容）  
----------------  

当应用于引用时，`constexpr`允许引用在常量表达式中使用。constexpr引用有特殊限制：只能绑定到具有静态存储期的对象（全局或静态局部变量）。因为编译器知道静态对象的内存地址，可以将其视为编译时常量。  

constexpr引用不能绑定到（非静态）局部变量。因为局部变量地址直到定义它们的函数被调用时才能确定。  

```cpp
int g_x { 5 };

int main()
{
    [[maybe_unused]] constexpr int& ref1 { g_x }; // 正确：可绑定到全局变量

    static int s_x { 6 };
    [[maybe_unused]] constexpr int& ref2 { s_x }; // 正确：可绑定到静态局部变量

    int x { 6 };
    [[maybe_unused]] constexpr int& ref3 { x }; // 编译错误：不能绑定到非静态对象

    return 0;
}
```  

定义指向const变量的constexpr引用时，需要同时应用`constexpr`（作用于引用）和`const`（作用于被引用类型）：  

```cpp
int main()
{
    static const int s_x { 6 }; // const int
    [[maybe_unused]] constexpr const int& ref2 { s_x }; // 需要同时使用constexpr和const

    return 0;
}
```  

由于这些限制，constexpr引用通常不常用。  

 

[下一课 12.5 — 通过左值引用传递](Chapter-12/lesson12.5-pass-by-lvalue-reference.md)  
[返回主页](/)  
[上一课 12.3 — 左值引用](Chapter-12/lesson12.3-lvalue-references.md)