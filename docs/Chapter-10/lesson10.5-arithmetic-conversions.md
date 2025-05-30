10.5 — 算术转换
==============================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月11日（首次发布于2021年6月17日）  

在课程[6\.1 — 操作符优先级与结合性](Chapter-6/lesson6.1-operator-precedence-and-associativity.md)中，我们讨论了操作符优先级与结合性如何影响表达式的求值顺序。考虑以下表达式：
```cpp
int x { 2 + 3 };
```
二元操作符`operator+`接受两个`int`类型的操作数。由于两操作数类型相同，计算结果将保持该类型，返回值也为同类型。因此`2 + 3`将得到`int`类型的值`5`。  

但当二元操作符的操作数类型不同时会发生什么？
```cpp
??? y { 2 + 3.5 };
```
此时`operator+`接受一个`int`和一个`double`类型的操作数。返回值应为`int`、`double`还是其他类型？  

在C++中，特定操作符要求操作数类型一致。若使用不同类型操作数调用这些操作符，将根据**通常算术转换（usual arithmetic conversions）**规则隐式转换一个或两个操作数。转换后得到的匹配类型称为操作数的**公共类型（common type）**。  

需要操作数类型一致的操作符  
----------------  
以下操作符要求操作数类型一致：
* 二元算术操作符：+、-、*、/、%
* 二元关系操作符：<、>、<=、>=、==、!=
* 二元位运算操作符：&、^、|
* 条件操作符?:（条件部分需为`bool`类型，其余操作数需类型一致）  

> **面向进阶读者**  
> 重载操作符不受通常算术转换规则约束。  

通常算术转换规则  
----------------  
通常算术转换规则较为复杂，此处进行简化说明。编译器维护的类型优先级列表如下（由高至低）：
* long double（最高优先级）
* double
* float
* long long
* long
* int（最低优先级）  

转换规则分两步执行：  
**步骤1**：
* 若一个操作数为整型（integral），另一个为浮点类型（floating point），整型操作数转换为浮点类型（不进行整型提升）
* 否则，所有整型操作数进行数值提升（参见[10.2 — 浮点与整型提升](Chapter-10/lesson10.2-floating-point-and-integral-promotion.md)）  

**步骤2**：
* 提升后，若操作数有符号（signed）与无符号（unsigned）混合，应用特殊规则（见下文）
* 否则，低优先级类型转换为高优先级类型  

> **面向进阶读者**  
> 有符号与无符号整型的特殊匹配规则：
> * 若无符号操作数的优先级≥有符号操作数，有符号操作数转换为无符号类型
> * 若有符号类型能表示无符号类型的所有值，无符号类型转换为有符号类型
> * 否则两者都转换为有符号类型对应的无符号类型  

相关资源  
----------------  
完整通常算术转换规则参见[cppreference](https://en.cppreference.com/w/cpp/language/usual_arithmetic_conversions)。  

示例分析  
----------------  
以下示例使用`typeid`操作符（需包含\<typeinfo\>头文件）展示表达式结果类型。  

**示例1**：`int`与`double`相加：
```cpp
#include <iostream>
#include <typeinfo> // 包含typeid()

int main()
{
    int i{ 2 };
    std::cout << typeid(i).name() << '\n'; // 显示变量i的类型名称

    double d{ 3.5 };
    std::cout << typeid(d).name() << '\n'; // 显示变量d的类型名称

    std::cout << typeid(i + d).name() << ' ' << i + d << '\n'; // 显示i+d的类型与值

    return 0;
}
```
在此例中，`double`操作数优先级更高，因此`int`类型操作数被转换为`double`值`2.0`。两个`double`值相加得到`5.5`。作者机器上输出：
```
int
double
double 5.5
```
注意`typeid.name()`的输出名称可能因编译器而异。  

**示例2**：两个`short`相加：
```cpp
#include <iostream>
#include <typeinfo> // 包含typeid()

int main()
{
    short a{ 4 };
    short b{ 5 };
    std::cout << typeid(a + b).name() << ' ' << a + b << '\n'; // 显示a+b的类型与值

    return 0;
}
```
由于`short`不在优先级列表中，两者先进行整型提升为`int`。两个`int`相加结果为`int`：
```
int 9
```

有符号与无符号问题  
----------------  
混合有符号和无符号值时，优先级层次和转换规则可能导致意外结果。  

**示例3**：
```cpp
#include <iostream>
#include <typeinfo> // 包含typeid()

int main()
{
    std::cout << typeid(5u-10).name() << ' ' << 5u - 10 << '\n'; // 5u表示无符号整型5

    return 0;
}
```
预期结果应为`-5`，但实际输出：
```
unsigned int 4294967291
```
根据转换规则，`int`操作数转换为`unsigned int`。由于`-5`超出无符号整型范围，产生意外结果。  

**示例4**：
```cpp
#include <iostream>

int main()
{
    std::cout << std::boolalpha << (-3 < 5u) << '\n';

    return 0;
}
```
虽然`5`明显大于`-3`，但`-3`被转换为大值无符号整型，导致输出`false`而非预期的`true`。  

这是避免使用无符号整型的主要原因——与有符号整型混合运算时易产生意外结果，且编译器通常不发出警告。  

`std::common_type`与`std::common_type_t`  
----------------  
在后续课程中，了解两个类型的公共类型非常有用。`std::common_type`及其类型别名`std::common_type_t`（定义于\<type_traits\>头文件）可实现此目的。  

例如：
* `std::common_type_t<int, double>`返回`int`与`double`的公共类型
* `std::common_type_t<unsigned int, long>`返回`unsigned int`与`long`的公共类型  

具体应用示例见课程[11.8 — 多模板类型的函数模板](Chapter-11/lesson11.8-function-templates-with-multiple-template-types.md)。  

[下一课 10.6 — 显式类型转换（casting）与static_cast](Chapter-10/lesson10.6-explicit-type-conversion-casting-and-static-cast.md)  
[返回主页](/)  
[上一课 10.4 — 窄化转换、列表初始化与constexpr初始化器](Chapter-10/lesson10.4-narrowing-conversions-list-initialization-and-constexpr-initializers.md)