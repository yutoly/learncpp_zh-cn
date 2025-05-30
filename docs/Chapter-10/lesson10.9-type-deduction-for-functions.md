10.9 — 函数的类型推导  
====================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2021年6月17日 下午5:42（PDT时间）  
2024年12月18日修订  

考虑以下程序：  
```cpp
int add(int x, int y)
{
    return x + y;
}
```  
编译此函数时，编译器将推导`x + y`的结果类型为`int`，并确保返回值类型与函数声明的返回类型匹配（或返回值类型可转换为声明的返回类型）。  

使用`auto`的返回类型推导  
----------------  
由于编译器已需要从返回语句推导返回类型（以确保值可转换为函数的声明返回类型），在C++14中，`auto`关键字被扩展用于函数返回类型推导。通过在函数返回类型位置使用`auto`关键字实现此功能。  

例如：  
```cpp
auto add(int x, int y)
{
    return x + y;
}
```  
由于返回语句返回`int`值，编译器将推导此函数的返回类型为`int`。  

使用`auto`返回类型时，函数内所有返回语句必须返回相同类型的值，否则将导致错误。例如：  
```cpp
auto someFcn(bool b)
{
    if (b)
        return 5;    // 返回int类型
    else
        return 6.7;  // 返回double类型
}
```  
上述函数中两个返回语句返回不同类型值，编译器将报错。若因特殊需求需要此类实现，可以显式指定函数返回类型（此时编译器将尝试将不匹配的返回表达式隐式转换为显式返回类型），或将所有返回语句显式转换为相同类型。上例中可将`5`改为`5.0`，或对非字面量类型使用`static_cast`。  

返回类型推导的优势  
----------------  
返回类型推导的最大优势是消除返回类型不匹配的风险（防止意外转换）。  

当函数返回类型具有脆弱性（实现变更可能导致返回类型改变的情况）时，此功能尤其有用。此时显式声明返回类型意味着在实现变更时需要更新所有相关返回类型。若足够幸运，编译器将报错直至我们更新相关返回类型。否则可能导致不期望的隐式转换。  

在其他情况下，函数返回类型可能冗长复杂或不够直观。此时`auto`可用于简化代码：  
```cpp
// 让编译器推导unsigned short与char相加的返回类型
auto add(unsigned short x, char y)
{
    return x + y;
}
```  
更多相关讨论（及如何表达此类函数的实际返回类型）详见课程[11.8 — 多模板类型的函数模板](Chapter-11/lesson11.8-function-templates-with-multiple-template-types.md)。  

返回类型推导的缺点  
----------------  
返回类型推导有两大主要缺点：  

1. 使用`auto`返回类型的函数必须在被使用前完整定义（仅前向声明不足）。例如：  
```cpp
#include <iostream>

auto foo();

int main()
{
    std::cout << foo() << '\n'; // 此处编译器仅看到前向声明
    return 0;
}

auto foo()
{
    return 5;
}
```  
在作者机器上会产生编译错误：  
```
error C3779: 'foo'：返回'auto'的函数在被定义前无法使用
```  
这合乎逻辑：前向声明缺乏足够信息供编译器推导函数返回类型。这意味着返回`auto`的普通函数通常只能在定义它们的文件内被调用。  

2. 对象类型推导的初始化式总与声明语句共存，因此推导类型通常易于判断。函数类型推导则不同——函数原型无法体现实际返回类型。良好的编程IDE应能显示函数的推导类型，但若无此工具，用户需深入函数体内部才能确定返回类型，增加出错几率。通常我们更倾向于显式声明接口中的类型（函数声明属于接口）。  

不同于对象类型推导，函数返回类型推导的最佳实践尚未形成共识。我们建议通常避免使用函数返回类型推导。  

最佳实践  
----------------  
优先使用显式返回类型而非返回类型推导（除非返回类型不重要、难以表达或具有脆弱性）。  

尾随返回类型语法  
----------------  
`auto`关键字也可用于**尾随返回类型语法**，即将返回类型置于函数原型其余部分之后。  

考虑以下函数：  
```cpp
int add(int x, int y)
{
  return (x + y);
}
```  
使用尾随返回语法可等价写作：  
```cpp
auto add(int x, int y) -> int
{
  return (x + y);
}
```  
此例中`auto`不执行类型推导——仅作为尾随返回类型语法的组成部分。  

使用此语法的理由包括：  
1. 对复杂返回类型的函数，尾随返回类型可提升可读性：  
```cpp
#include <type_traits> // 引入std::common_type

std::common_type_t<int, double> compare(int, double);         // 较难阅读（函数名位置不明显）
auto compare(int, double) -> std::common_type_t<int, double>; // 更易阅读（除非关注返回类型否则无需细读）
```  

2. 尾随返回类型语法可对齐函数名，便于连续函数声明阅读：  
```cpp
auto add(int x, int y) -> int;
auto divide(double x, double y) -> double;
auto printSomething() -> void;
auto generateSubstring(const std::string &s, int start, int len) -> std::string;
```  

进阶内容  
----------------  
3. 当函数返回类型需根据参数类型推导时，普通返回类型语法无法满足要求，因为此时编译器尚未看到参数：  
```cpp
#include <type_traits>
// 注：decltype(x)求取x的类型

std::common_type_t<decltype(x), decltype(y)> add(int x, double y);         // 编译错误：编译器尚未看到x和y的定义
auto add(int x, double y) -> std::common_type_t<decltype(x), decltype(y)>; // 正确
```  

4. 尾随返回语法也是C++某些高级功能（如lambda表达式）的必需语法，详见课程[20.6 — Lambda表达式（匿名函数）简介](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)。  

当前建议继续使用传统函数返回语法，除非需要使用尾随返回语法的场景。  

类型推导不适用于函数参数类型  
----------------  
许多新手学习类型推导后会尝试如下写法：  
```cpp
#include <iostream>

void addAndPrint(auto x, auto y)
{
    std::cout << x + y << '\n';
}

int main()
{
    addAndPrint(2, 3);       // 情况1：使用int参数调用
    addAndPrint(4.5, 6.7);   // 情况2：使用double参数调用
    return 0;
}
```  
遗憾的是，类型推导不适用于函数参数。在C++20之前，上述程序无法编译（将报错函数参数不能使用auto类型）。  

C++20扩展了`auto`关键字使上述程序能正确编译运行——但此处的`auto`并非执行类型推导，而是触发名为`函数模板`的特性来处理此类情况。  

相关内容  
----------------  
我们在课程[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)中介绍函数模板，并在课程[11.8 — 多模板类型的函数模板](Chapter-11/lesson11.8-function-templates-with-multiple-template-types.md)中讨论`auto`在函数模板中的使用。  

[下一课 10.x — 第10章总结与测验](Chapter-10/lesson10.x-chapter-10-summary-and-quiz.md)  
[返回主页](/)  
[上一课 10.8 — 使用auto关键字进行对象类型推导](Chapter-10/lesson10.8-type-deduction-for-objects-using-the-auto-keyword.md)