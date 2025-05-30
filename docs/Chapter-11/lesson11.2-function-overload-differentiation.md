11.2 — 函数重载的区分
=========================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2021年6月17日下午5:43（太平洋夏令时）  
2024年12月11日  

在上一课（[11.1 — 函数重载简介](Chapter-11/lesson11.1-introduction-to-function-overloading.md)）中，我们介绍了函数重载的概念，它允许我们创建多个同名函数，只要每个同名函数的参数类型不同（或可通过其他方式区分）。

本课将深入探讨重载函数的区分机制。未能正确区分的重载函数将导致编译器报错。

重载函数的区分机制

| 函数属性         | 是否用于区分 | 说明                                   |
|------------------|--------------|----------------------------------------|
| 参数数量         | 是           |                                        |
| 参数类型         | 是           | 不包括typedef、类型别名和值参数的const限定符。包含省略号。 |
| 返回值类型       | 否           |                                        |

注意：函数返回值类型不用于区分重载函数，后文将详细讨论。

进阶阅读  
对于成员函数，额外的函数级限定符也会被考虑：  

| 函数级限定符      | 是否用于重载 |
|-------------------|--------------|
| const 或 volatile | 是           |
| 引用限定符        | 是           |

例如：const成员函数可与参数相同的非const成员函数区分（即使参数列表完全一致）。

相关内容  
省略号详见课程[20.5 — 省略号（及避免使用的原因）](Chapter-20/lesson20.5-ellipsis-and-why-to-avoid-them.md)。

基于参数数量的重载  
当重载函数具有不同参数数量时即可区分。例如：  
```cpp
int add(int x, int y)         // 两参数版本
{
    return x + y;
}

int add(int x, int y, int z)  // 三参数版本
{
    return x + y + z;
}
```
编译器可明确识别：两个整型参数的调用应匹配`add(int, int)`，三个整型参数的调用应匹配`add(int, int, int)`。

基于参数类型的重载  
当重载函数的参数类型列表不同时也可区分。例如以下重载均可区分：  
```cpp
int add(int x, int y);         // 整数版本
double add(double x, double y); // 浮点数版本
double add(int x, double y);    // 混合版本
double add(double x, int y);    // 混合版本
```
由于类型别名（typedef）不是独立类型，使用类型别名的重载函数无法与原始类型区分。以下重载均无法区分（将导致编译错误）：
```cpp
typedef int Height;         // typedef
using Age = int;            // 类型别名

void print(int value);
void print(Age value);      // 无法与print(int)区分
void print(Height value);   // 无法与print(int)区分
```
对于按值传递的参数，const限定符同样不被考虑。因此以下函数无法区分：
```cpp
void print(int);
void print(const int);      // 无法与print(int)区分
```

进阶阅读  
省略号参数被视为特殊参数类型：
```cpp
void foo(int x, int y);
void foo(int x, ...);       // 可与foo(int, int)区分
```
因此`foo(4, 5)`将匹配`foo(int, int)`而非`foo(int, ...)`。

函数返回值类型不参与区分  
函数返回值类型不用于区分重载函数。  
假设需要返回随机数的函数：一个返回int，另一个返回double。若尝试：
```cpp
int getRandomValue();
double getRandomValue();
```
在Visual Studio 2019中将产生编译错误：
```
error C2556: 'double getRandomValue(void)': 重载函数仅返回值类型与'int getRandomValue(void)'不同
```
原因明确：当编译器遇到`getRandomValue()`调用时，无法确定应调用哪个重载版本。

延伸说明  
这是有意为之的设计：确保函数调用的行为可独立于表达式其余部分确定，简化复杂表达式的理解。换言之，我们仅需根据函数调用的实参即可确定调用版本。若使用返回值区分，则无法通过语法直观判断调用的是哪个重载版本——还需分析返回值的使用方式，大幅增加理解成本。

最佳解决方案是为函数赋予不同名称：
```cpp
int getRandomInt();
double getRandomDouble();
```

类型签名  
函数的**类型签名（type signature）**（通常简称**签名（signature）**）指用于函数区分的函数头部分。在C++中包括：函数名、参数数量、参数类型和函数级限定符。尤其不包括返回值类型。

名称修饰（Name mangling）  
延伸说明  
编译器编译函数时会进行**名称修饰**：根据参数数量和类型等标准修改函数编译后的名称（"修饰"），确保链接器使用唯一名称。  
例如：原型为`int fcn()`的函数可能被修饰为`__fcn_v`，而`int fcn(int)`可能变为`__fcn_i`。因此在源代码中两个重载函数共享`fcn()`名称，但在编译代码中修饰名称唯一（`__fcn_v`与`__fcn_i`）。  
名称修饰规则无统一标准，不同编译器会产生不同的修饰名称。

[下一课 11.3 函数重载解析与歧义匹配](Chapter-11/lesson11.3-function-overload-resolution-and-ambiguous-matches.md)  
[返回主页](/)  
[上一课 11.1 函数重载简介](Chapter-11/lesson11.1-introduction-to-function-overloading.md)