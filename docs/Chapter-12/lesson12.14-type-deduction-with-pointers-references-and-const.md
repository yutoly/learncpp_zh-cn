12.14 — 指针、引用与const的类型推导  
============================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月21日（首次发布于2022年2月2日）  

在课程[10.8 — 使用auto关键字进行对象类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)中，我们讨论了如何用`auto`关键字让编译器从初始化式推导变量类型：  

```cpp
int main()
{
    int a { 5 };
    auto b { a }; // b推导为int

    return 0;
}
```  

我们还提到，默认情况下类型推导会丢弃类型的`const`限定符：  

```cpp
int main()
{
    const double a { 7.8 }; // a的类型是const double
    auto b { a };           // b的类型是double（const被丢弃）

    constexpr double c { 7.8 }; // c的类型是const double（constexpr隐式应用const）
    auto d { c };               // d的类型是double（const被丢弃）

    return 0;
}
```  

可以通过在推导类型定义中重新添加`const`（或`constexpr`）限定符来恢复const：  

```cpp
int main()
{
    double a { 7.8 };    // a的类型是double
    const auto b { a };  // b的类型是const double（重新应用const）

    constexpr double c { 7.8 }; // c的类型是const double
    const auto d { c };         // d是const double（const被丢弃后重新应用）
    constexpr auto e { c };     // e是constexpr double（const被丢弃后重新应用constexpr）

    return 0;
}
```  

类型推导会丢弃引用  
----------------  

除了丢弃const外，类型推导还会丢弃引用：  

```cpp
#include <string>

std::string& getRef(); // 某个返回引用的函数

int main()
{
    auto ref { getRef() }; // 类型推导为std::string（非std::string&）

    return 0;
}
```  

上例中，变量`ref`使用类型推导。虽然`getRef()`返回`std::string&`，但引用限定符被丢弃，因此`ref`的类型推导为`std::string`。  

与丢弃`const`类似，若希望推导类型为引用，可在定义时重新应用引用：  

```cpp
#include <string>

std::string& getRef(); // 某个返回引用的函数

int main()
{
    auto ref1 { getRef() };  // std::string（引用被丢弃）
    auto& ref2 { getRef() }; // std::string&（引用被丢弃后重新应用）

    return 0;
}
```  

顶层const与底层const  
----------------  

**顶层const（top-level const）**是直接应用于对象本身的const限定符。例如：  

```cpp
const int x;    // 此const应用于x，是顶层const
int* const ptr; // 此const应用于ptr，是顶层const
// 引用没有顶层const语法，因为它们隐式具有顶层const
```  

**底层const（low-level const）**是应用于被引用或指向对象的const限定符：  

```cpp
const int& ref; // 此const应用于被引用对象，是底层const
const int* ptr; // 此const应用于指向对象，是底层const
```  

指向const值的引用始终是底层const。指针可以同时具有顶层和底层const：  

```cpp
const int* const ptr; // 左侧const是底层，右侧是顶层
```  

类型推导仅会丢弃顶层const，底层const不会被丢弃。  

类型推导与const引用  
----------------  

若初始化式是const引用，首先丢弃引用（需要时重新应用），然后丢弃结果中的顶层const：  

```cpp
#include <string>

const std::string& getConstRef(); // 返回const引用的函数

int main()
{
    auto ref1{ getConstRef() }; // std::string（先丢弃引用，再丢弃结果的顶层const）

    return 0;
}
```  

本例中，`getConstRef()`返回`const std::string&`，首先丢弃引用得到`const std::string`。此时const成为顶层const，因此被丢弃，最终推导类型为`std::string`。  

关键洞见  
----------------  

丢弃引用可能将底层const转为顶层const：`const std::string&`是底层const，但丢弃引用后得到`const std::string`成为顶层const。  

可重新应用引用和/或const：  

```cpp
#include <string>

const std::string& getConstRef(); // 返回const引用的函数

int main()
{
    auto ref1{ getConstRef() };        // std::string（引用和顶层const被丢弃）
    const auto ref2{ getConstRef() };  // const std::string（引用丢弃后重新应用const）

    auto& ref3{ getConstRef() };       // const std::string&（引用重新应用，底层const保留）
    const auto& ref4{ getConstRef() }; // const std::string&（引用重新应用，底层const保留）

    return 0;
}
```  

`ref3`的情况值得注意：由于重新应用了引用，类型保持`const std::string&`，底层const未被丢弃。`ref4`显式添加`const`虽冗余，但能明确代码意图。  

最佳实践  
----------------  

即使非必要，也建议重新应用`const`限定符以明确意图，防止错误。  

关于constexpr引用  
----------------  

constexpr不属于表达式类型，因此不会被`auto`推导。定义constexpr引用到const变量时，需同时应用`constexpr`（应用于引用）和`const`（应用于被引用类型）。  

类型推导与指针  
----------------  

与引用不同，类型推导不会丢弃指针：  

```cpp
#include <string>

std::string* getPtr(); // 返回指针的函数

int main()
{
    auto ptr1{ getPtr() }; // std::string*

    return 0;
}
```  

可用`auto*`明确指针类型：  

```cpp
#include <string>

std::string* getPtr(); // 返回指针的函数

int main()
{
    auto ptr1{ getPtr() };  // std::string*
    auto* ptr2{ getPtr() }; // std::string*

    return 0;
}
```  

关键洞见  
----------------  

引用和指针语义不同导致类型推导差异：  

* 引用推导得到被引用对象类型，指针推导得到指针本身类型  
* 使用`auto*`时，指针限定符在类型推导后重新应用  

auto与auto*的区别（可选）  
----------------  

使用`auto*`时，若初始化式非指针将导致编译错误：  

```cpp
#include <string>

std::string* getPtr(); // 返回指针的函数

int main()
{
    auto ptr3{ *getPtr() };      // std::string（解引用指针）
    auto* ptr4{ *getPtr() };     // 编译错误（初始化式非指针）

    return 0;
}
```  

类型推导与const指针（可选）  
----------------  

指针类型推导中，仅顶层const被丢弃：  

```cpp
#include <string>

std::string* getPtr(); // 返回指针的函数

int main()
{
    const auto ptr1{ getPtr() };  // std::string* const
    auto const ptr2 { getPtr() }; // std::string* const

    const auto* ptr3{ getPtr() }; // const std::string*
    auto* const ptr4{ getPtr() }; // std::string* const

    return 0;
}
```  

初始化式为const指针时：  

```cpp
#include <string>

int main()
{
    std::string s{};
    const std::string* const ptr { &s };

    auto ptr1{ ptr };  // const std::string*
    auto* ptr2{ ptr }; // const std::string*

    auto const ptr3{ ptr };  // const std::string* const
    const auto ptr4{ ptr };  // const std::string* const

    auto* const ptr5{ ptr }; // const std::string* const
    const auto* ptr6{ ptr }; // const std::string*

    const auto const ptr7{ ptr };  // 错误：const不能重复应用
    const auto* const ptr8{ ptr }; // const std::string* const

    return 0;
}
```  

最佳实践  
----------------  

建议显式声明const指针、指向const的指针或const指针到const，即使冗余也应明确意图。  

提示  
----------------  

推导指针类型时优先使用`auto*`，可明确指针类型并帮助编译器检查。  

总结  
----------------  

关键点回顾：  

* **顶层const vs 底层const**  
* 类型推导行为：  
  - 先丢弃引用（除非显式声明引用）  
  - 再丢弃顶层const（除非显式声明const）  
  - constexpr需显式应用  
* 指针推导不丢弃指针  
* 推荐显式声明引用、const、constexpr  
* **指针推导建议**：  
  - 优先使用`auto*`  
  - `auto*`要求指针初始化式  
  - const位置影响指针类型  

[下一课 12.15 — std::optional](Chapter-12/lesson12.15-stdoptional.md)  
[返回主页](/)  
[上一课 12.13 — 输入输出参数](Chapter-12/lesson12.13-in-and-out-parameters.md)