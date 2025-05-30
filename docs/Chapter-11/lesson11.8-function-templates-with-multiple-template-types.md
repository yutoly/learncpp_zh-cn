11.8 — 支持多模板类型的函数模板  
===============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月18日（首次发布于2021年6月17日）  

在课程[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)中，我们编写了计算两个值最大值的函数模板：  

```cpp
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(1, 2) << '\n';   // 实例化max(int, int)
    std::cout << max(1.5, 2.5) << '\n'; // 实例化max(double, double)
    return 0;
}
```  

现在考虑以下类似程序：  

```cpp
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n';  // 编译错误
    return 0;
}
```  

您可能会惊讶地发现该程序无法编译。编译器将输出大量（可能看似混乱的）错误信息。在Visual Studio中，作者得到如下错误：  

```
Project3.cpp(11,18): error C2672: 'max': 找不到匹配的重载函数
Project3.cpp(11,28): error C2782: 'T max(T,T)': 模板参数'T'不明确
Project3.cpp(4): message : 参见'max'的声明
Project3.cpp(11,28): message : 可能是'double'
Project3.cpp(11,28): message : 或       'int'
Project3.cpp(11,28): error C2784: 'T max(T,T)': 无法从'double'推导出'T'的模板参数
Project3.cpp(4): message : 参见'max'的声明
```  

在函数调用`max(2, 3.5)`中，我们传递了两种不同类型的参数：`int`和`double`。由于未使用尖括号指定具体类型，编译器首先会查找`max(int, double)`的非模板匹配，但无法找到。  

接着编译器尝试通过模板参数推导（参见课程[11.7 — 函数模板实例化](Chapter-11/lesson11.7-function-template-instantiation.md)）寻找函数模板匹配，但依然失败。根本原因在于：`T`只能代表单一类型，无法将函数模板`max<T>(T, T)`实例化为接受两个不同参数类型的函数。换句话说，由于函数模板的两个参数都是`T`类型，它们必须解析为相同的实际类型。  

由于既无模板匹配也无非模板匹配，函数调用解析失败并导致编译错误。  

您可能好奇为何编译器不生成`max<double>(double, double)`函数并通过数值转换将`int`参数转为`double`。答案很简单：类型转换仅用于函数重载解析，不适用于模板参数推导。  

这种不进行类型转换的设计至少有两个原因：首先保持简单性，函数调用参数必须与模板类型参数完全匹配；其次允许我们创建需要多个参数类型一致的函数模板。  

我们需要寻找其他解决方案，以下是三种可行方法：  

### 使用static_cast转换参数类型  

第一种方案是要求调用者将参数转换为匹配类型：  

```cpp
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(static_cast<double>(2), 3.5) << '\n'; // 将int转为double
    return 0;
}
```  

现在两个参数都是`double`类型，编译器将实例化`max(double, double)`。但此方案不够直观且影响可读性。  

### 显式指定模板类型参数  

若编写非模板函数`max(double, double)`，则可通过隐式转换处理`int`参数：  

```cpp
#include <iostream>

double max(double x, double y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n'; // int参数转为double
    return 0;
}
```  

对于模板版本，可通过显式指定模板类型参数来避免参数推导：  

```cpp
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<double>(2, 3.5) << '\n'; // 显式指定double类型
    return 0;
}
```  

此时编译器实例化`max<double>(double, double)`，并将`int`参数隐式转换为`double`。虽然比前方案更可读，但理想情况是调用时无需考虑类型。  

### 使用多模板类型参数的函数模板  

根本解决方案是允许参数解析为不同类型。使用两个模板类型参数`T`和`U`：  

```cpp
#include <iostream>

template <typename T, typename U> // 使用T和U两个模板参数
T max(T x, U y) // x解析为T类型，y解析为U类型
{
    return (x < y) ? y : x; // 存在窄化转换问题
}

int main()
{
    std::cout << max(2, 3.5) << '\n'; // 实例化为max<int, double>
    return 0;
}
```  

`x`和`y`可独立解析类型。调用`max(2, 3.5)`时，`T`为`int`，`U`为`double`，编译器实例化`max<int, double>(int, double)`。  

**关键洞察**  
由于`T`和`U`是独立模板参数，可解析为不同或相同类型。  

但此示例存在问题。编译运行（关闭"将警告视为错误"）会输出：  

```
3
```  

问题在于条件运算符（?:）要求操作数具有相同类型。`int`和`double`的共同类型是`double`，但函数返回类型为`T`（`int`），导致`3.5`被截断为`3`。解决方案是使用返回类型推导（`auto`）：  

```cpp
#include <iostream>

template <typename T, typename U>
auto max(T x, U y) // 编译器推导返回类型
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n'; // 正确返回3.5
    return 0;
}
```  

使用`auto`返回类型时，函数需完整定义后才能使用。若需前置声明，可使用`std::common_type_t`明确返回类型：  

```cpp
#include <iostream>
#include <type_traits>

template <typename T, typename U>
auto max(T x, U y) -> std::common_type_t<T, U>; // 返回T和U的共同类型

int main()
{
    std::cout << max(2, 3.5) << '\n';
    return 0;
}

template <typename T, typename U>
auto max(T x, U y) -> std::common_type_t<T, U>
{
    return (x < y) ? y : x;
}
```  

### C++20缩写函数模板  

C++20允许使用`auto`作为参数类型，自动生成函数模板：  

```cpp
auto max(auto x, auto y) // C++20缩写函数模板
{
    return (x < y) ? y : x;
}
```  

等效于：  

```cpp
template <typename T, typename U>
auto max(T x, U y)
{
    return (x < y) ? y : x;
}
```  

**最佳实践**  
当每个`auto`参数应为独立类型时（且使用C++20或更新标准），推荐使用缩写函数模板。  

### 函数模板重载  

函数模板可像普通函数一样重载，支持不同模板参数数量或函数参数类型：  

```cpp
#include <iostream>

// 同类型参数相加
template <typename T>
auto add(T x, T y)
{
    return x + y;
}

// 不同类型参数相加（C++20可用auto add(auto x, auto y)）
template <typename T, typename U>
auto add(T x, U y)
{
    return x + y;
}

// 三个任意类型参数相加（C++20可用auto add(auto x, auto y, auto z)）
template <typename T, typename U, typename V>
auto add(T x, U y, V z)
{
    return x + y + z;
}

int main()
{
    std::cout << add(1.2, 3.4) << '\n'; // 调用add<double>()
    std::cout << add(5.6, 7) << '\n';   // 调用add<double, int>()
    std::cout << add(8, 9, 10) << '\n'; // 调用add<int, int, int>()
    return 0;
}
```  

注意：当多个函数模板匹配时，编译器优先选择更特化的版本（如`add<T>(T, T)`比`add<T, U>(T, U)`更特化）。若无法确定，将报歧义错误。  

[下一课 11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)  
[返回主页](/)  
[上一课 11.7 — 函数模板实例化](Chapter-11/lesson11.7-function-template-instantiation.md)