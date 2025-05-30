10.8 — 使用auto关键字进行对象类型推导  
=========================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月25日（首次发布于2015年7月30日）  

在这个简单的变量定义中，存在一个微妙的冗余现象：  

```cpp
double d{ 5.0 };
```  

在C++中，所有对象必须显式指定类型。因此我们明确声明变量`d`是double类型。  

然而，用于初始化`d`的字面值`5.0`本身也具有double类型（通过字面值格式隐式确定）。  

> **相关内容**  
> 字面值类型的确定详见课程[5.2 — 字面值](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)。  

当我们需要变量与其初始化器具有相同类型时，实际上是在重复提供相同的类型信息。  

初始化变量的类型推导  
----------------  

**类型推导（type deduction）**（有时称为**类型推断（type inference）**）允许编译器根据对象的初始化器推断其类型。定义变量时，可用`auto`关键字代替显式类型声明来启用类型推导：  

```cpp
int main()
{
    auto d { 5.0 };  // 5.0是double字面值，d推导为double类型
    auto i { 1 + 2 };// 1+2结果为int，i推导为int类型
    auto x { i };    // i是int，x推导为int类型

    return 0;
}
```  

第一种情况中，由于`5.0`是double字面值，编译器将推导变量`d`为`double`类型。第二种情况，表达式`1+2`生成int结果，因此变量`i`推导为`int`类型。第三种情况，`i`先前已推导为`int`类型，故`x`同样推导为`int`类型。  

> **警告**  
> 在C++17之前，`auto d{5.0};`会将`d`推导为`std::initializer_list<double>`而非`double`。此问题已在C++17修复，且许多编译器（如gcc和Clang）已将此更改向后移植至早期语言标准。  
>  
> 若使用C++14或更早版本且示例无法编译，请改用拷贝初始化语法（`auto d = 5.0`）。  

由于函数调用是有效表达式，我们甚至可以在初始化器为非void函数调用时使用类型推导：  

```cpp
int add(int x, int y)
{
    return x + y;
}

int main()
{
    auto sum { add(5, 6) }; // add()返回int，sum推导为int类型

    return 0;
}
```  

`add()`函数返回`int`值，因此编译器将推导变量`sum`为`int`类型。  

字面值后缀可与类型推导结合使用以指定特定类型：  

```cpp
int main()
{
    auto a { 1.23f }; // f后缀使a推导为float
    auto b { 5u };    // u后缀使b推导为unsigned int

    return 0;
}
```  

使用类型推导的变量也可配合其他说明符/限定符（如`const`或`constexpr`）：  

```cpp
int main()
{
    int a { 5 };            // a是int

    const auto b { 5 };     // b是const int
    constexpr auto c { 5 }; // c是constexpr int

    return 0;
}
```  

类型推导必须有推导依据  
----------------  

类型推导不适用于以下情况：  
* 无初始化器的对象  
* 空初始化器  
* 初始化器为void类型（或其他不完整类型）  

因此以下代码无效：  

```cpp
#include <iostream>

void foo()
{
}

int main()
{
    auto a;           // 无法推导a的类型
    auto b { };       // 无法推导b的类型
    auto c { foo() }; // 无效：c不能具有不完整类型void
    
    return 0;
}
```  

虽然对基础数据类型使用类型推导仅能节省少量输入，但在后续课程中我们将看到类型变得复杂冗长的案例（有时甚至难以确定类型）。此时使用`auto`可显著减少输入量（及拼写错误）。  

> **相关内容**  
> 指针和引用的类型推导规则较为复杂，详见[12.14 — 指针、引用和const的类型推导](Chapter-12/lesson12.14-type-deduction-with-pointers-references-and-const.md)。  

类型推导会去除const限定  
----------------  

大多数情况下，类型推导会去除推导类型中的`const`限定：  

```cpp
int main()
{
    const int a { 5 }; // a是const int
    auto b { a };      // b是int（去除const）

    return 0;
}
```  

此例中`a`是`const int`，但使用`a`初始化变量`b`时，推导类型为`int`而非`const int`。  

若需要推导类型保持const，必须显式添加`const`限定：  

```cpp
int main()
{
    const int a { 5 };  // a是const int
    const auto b { a }; // b是const int（去除后重新应用）

    return 0;
}
```  

此例中从`a`推导的类型是`int`（去除const），但变量`b`定义时重新添加了`const`限定，故`b`为`const int`类型。  

字符串字面值的类型推导  
----------------  

由于历史原因，C++中的字符串字面值具有特殊类型。因此以下代码可能不符合预期：  

```cpp
auto s { "Hello, world" }; // s推导为const char*而非std::string
```  

若希望字符串字面值推导为`std::string`或`std::string_view`，需使用`s`或`sv`字面值后缀（分别在[5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)和[5.8 — std::string_view简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)中介绍）：  

```cpp
#include <string>
#include <string_view>

int main()
{
    using namespace std::literals; // 访问s和sv后缀的最简方式

    auto s1 { "goo"s };  // "goo"s是std::string字面值，s1推导为std::string
    auto s2 { "moo"sv }; // "moo"sv是std::string_view字面值，s2推导为std::string_view

    return 0;
}
```  

但在此类情况下，可能更适合显式指定类型。  

类型推导与constexpr  
----------------  

由于`constexpr`不属于类型系统，无法通过类型推导获得。但`constexpr`变量隐式具有const属性，该const属性在类型推导时会被去除（可按需重新添加）：  

```cpp
int main()
{
    constexpr double a { 3.4 };  // a类型为const double（constexpr非类型部分，const隐式存在）

    auto b { a };                // b类型为double（去除const）
    const auto c { a };          // c类型为const double（去除后重新应用）
    constexpr auto d { a };      // d类型为const double（去除后由constexpr隐式重新应用）

    return 0;
}
```  

类型推导的优缺点  
----------------  

类型推导不仅方便，还有其他优势：  

1. **提高可读性**：当多个变量连续定义时，对齐的变量名更易阅读  
```cpp
// 较难阅读
int a { 5 };
double b { 6.7 };

// 更易阅读
auto c { 5 };
auto d { 6.7 };
```  

2. **防止未初始化变量**：类型推导要求变量必须初始化  
```cpp
int x; // 忘记初始化x（编译器可能不报错）
auto y; // 编译器报错（无法推导y类型）
```  

3. **避免性能损耗的隐式转换**  
```cpp
std::string_view getString();   // 返回std::string_view的函数

std::string s1 { getString() }; // 错误：std::string_view到std::string的昂贵转换
auto s2 { getString() };        // 正确：无需转换
```  

类型推导的缺点：  

1. **类型信息不透明**：虽然IDE可显示推导类型，但仍可能引发类型相关错误  
```cpp
auto y { 5 }; // 本意是double，但误用int字面值导致y推导为int
```  

另一个示例：  
```cpp
#include <iostream>

int main()
{
     auto x { 3 };
     auto y { 2 };

     std::cout << x / y << '\n'; // 本意是浮点除法

     return 0;
}
```  

此例中整数除法的意图不够明显。  

2. **类型变更传播**：当初始化器类型改变时，推导类型可能意外改变  
```cpp
auto sum { add(5, 6) + gravity };
```  

若`add()`返回类型或`gravity`类型从int改为double，`sum`类型也会相应改变。  

现代共识认为类型推导通常可安全使用，且能通过弱化类型信息提升代码可读性，使逻辑更突出。  

> **最佳实践**  
> * 当对象类型无关紧要时使用类型推导  
> * 当需要特定类型或明确类型信息更有助于理解时，使用显式类型  

> **作者注**  
> 后续课程中，当展示类型信息有助于理解概念或示例时，我们仍会使用显式类型。  

[下一课 10.9 — 函数类型推导](Chapter-10/lesson10.9-type-deduction-for-functions.md)  
[返回主页](/)  
[上一课 10.7 — 类型别名与typedef](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)