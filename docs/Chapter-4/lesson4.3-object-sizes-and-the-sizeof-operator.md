4.3 — 对象尺寸与sizeof操作符  
===========================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2024年12月26日（首次发布于2007年6月6日）  

对象尺寸  
----------------  

在课程[4.1 — 基本数据类型介绍](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)中我们了解到，现代机器的内存通常组织为字节（byte）大小的单元，每个字节内存有唯一地址。到目前为止，将内存视为可以存放和检索信息的隔间或邮箱，而变量作为访问这些存储单元的名称是有效的类比方式。  

但这个类比在一个方面并不完全准确——大多数对象实际占用超过1字节内存。单个对象可能使用1、2、4、8甚至更多连续内存地址。对象使用的内存量取决于其数据类型。  

由于我们通常通过变量名访问内存（而非直接使用内存地址），编译器能够向我们隐藏对象占用字节数的细节。当我们在源代码中访问变量`x`时，编译器知道需要检索多少字节数据（基于变量`x`的类型），并将输出适当的机器语言代码来处理这个细节。  

尽管如此，了解对象占用的内存量仍有几个重要原因：  

首先，对象使用的内存越多，它能承载的信息量就越大：  

* 单个位（bit）可存储2种可能值：0或1  
* 2位可存储4种可能值  
* 3位可存储8种可能值  
* 通用公式：n位对象可存储2^n个唯一值  

因此：  
* 8位字节（byte）可存储256（2^8）种不同值  
* 2字节对象可存储65536（2^16）种不同值  

对象尺寸限制了其能存储的唯一值数量——使用更多字节的对象可存储更大范围的唯一值。我们将在讨论整数类型时进一步探讨此概念。  

其次，计算机可用内存有限。每个定义的对象在其存在期间都会占用部分可用内存。现代计算机虽内存充足，此影响通常可忽略，但对于需要大量对象或数据的程序（如渲染数百万多边形的游戏），1字节与8字节对象的差异可能非常显著。  

> **关键洞察**  
> 新手常过度关注优化代码以减少内存占用，这在多数情况下收效甚微。应优先编写可维护代码，仅在收益显著时进行优化。  

基本数据类型尺寸  
----------------  

核心问题是："给定数据类型的对象占用多少内存？" 值得注意的是，C++标准未明确定义任何基本类型的具体尺寸（以位为单位）。标准仅规定：  

* 对象必须至少占用1字节（确保每个对象有唯一内存地址）  
* 1字节至少8位  
* 整型（integral types）`char`、`short`、`int`、`long`、`long long`的最小尺寸分别为8、16、16、32、64位  
* `char`和`char8_t`严格为1字节（至少8位）  

> **命名惯例**  
> 讨论类型大小时，实际指该类型实例化对象的大小  

在本教程系列中，我们基于现代架构做出合理假设以简化说明：  
* 1字节=8位  
* 内存按字节寻址  
* 浮点数支持符合IEEE-754标准  
* 使用32位或64位架构  

基于以上假设，可得出以下结论：  

| 类别          | 类型          | 最小尺寸 | 典型尺寸       |  
|---------------|---------------|----------|----------------|  
| 布尔          | bool          | 1字节    | 1字节          |  
| 字符          | char          | 1字节    | 1字节          |  
|               | wchar_t       | 1字节    | 2或4字节       |  
|               | char8_t       | 1字节    | 1字节          |  
|               | char16_t      | 2字节    | 2字节          |  
|               | char32_t      | 4字节    | 4字节          |  
| 整型          | short         | 2字节    | 2字节          |  
|               | int           | 2字节    | 4字节          |  
|               | long          | 4字节    | 4或8字节       |  
|               | long long     | 8字节    | 8字节          |  
| 浮点型        | float         | 4字节    | 4字节          |  
|               | double        | 8字节    | 8字节          |  
|               | long double   | 8字节    | 8、12或16字节  |  
| 指针          | std::nullptr_t| 4字节    | 4或8字节       |  

> **提示**  
> 为最大限度保证可移植性，不应假设对象尺寸超过规定的最小值。  
> 若需假设类型具有非最小尺寸（如int至少4字节），可使用`static_assert`确保编译时验证（详见课程[9.6 — 断言与static_assert](assert-and-static_assert/#static_assert)）。  

> **相关内容**  
> C++标准中各类型的最小尺寸详细信息可参考[此链接](https://en.cppreference.com/w/cpp/language/types)。  

sizeof操作符  
----------------  

为确定特定机器上的数据类型尺寸，C++提供`sizeof`操作符。**sizeof操作符（sizeof operator）**是一元操作符，可接受类型或变量，返回该类型对象的大小（以字节为单位）。编译运行以下程序可查看各类型尺寸：  

```cpp  
#include <iomanip>  // 用于std::setw（设置输出宽度）  
#include <iostream>  
#include <climits>  // 用于CHAR_BIT  

int main()  
{  
    std::cout << "1字节等于" << CHAR_BIT << "位\n\n";  
    std::cout << std::left; // 左对齐输出  

    std::cout << std::setw(16) << "bool:" << sizeof(bool) << "字节\n";  
    std::cout << std::setw(16) << "char:" << sizeof(char) << "字节\n";  
    std::cout << std::setw(16) << "short:" << sizeof(short) << "字节\n";  
    std::cout << std::setw(16) << "int:" << sizeof(int) << "字节\n";  
    std::cout << std::setw(16) << "long:" << sizeof(long) << "字节\n";  
    std::cout << std::setw(16) << "long long:" << sizeof(long long) << "字节\n";  
    std::cout << std::setw(16) << "float:" << sizeof(float) << "字节\n";  
    std::cout << std::setw(16) << "double:" << sizeof(double) << "字节\n";  
    std::cout << std::setw(16) << "long double:" << sizeof(long double) << "字节\n";  

    return 0;  
}  
```  

作者机器输出示例：  
```
bool:           1字节  
char:           1字节  
short:          2字节  
int:            4字节  
long:           4字节  
long long:      8字节  
float:          4字节  
double:         8字节  
long double:    8字节  
```  

实际结果可能因编译器、架构、操作系统、编译设置（32位/64位）而异。  

> **注意**  
> 对不完整类型（如void）使用`sizeof`将导致编译错误。  

> **GCC用户注意**  
> 若未禁用编译器扩展，GCC允许`sizeof(void)`返回1而非报错（参见[指针运算](https://gcc.gnu.org/onlinedocs/gcc-4.4.2/gcc/Pointer-Arith.html#Pointer-Arith)）。禁用扩展方法见课程[0.10 — 配置编译器：编译器扩展](Chapter-0/lesson0.10-configuring-your-compiler-compiler-extensions.md)。  

`sizeof`也可用于变量名：  
```cpp  
#include <iostream>  

int main()  
{  
    int x{};  
    std::cout << "x占" << sizeof(x) << "字节\n";  
    return 0;  
}  
```  
输出示例：  
```
x占4字节  
```  

> **进阶阅读**  
> `sizeof`不包含对象使用的动态分配内存，动态内存分配将在后续课程讨论。  

基本数据类型性能  
----------------  
现代机器上基本数据类型对象的操作速度很快，通常无需担心使用或复制这些类型的性能问题。  

> **延伸讨论**  
> 可能认为较小内存类型比较大型更快，但并非总是成立。CPU通常优化处理特定尺寸数据（如32位），匹配该尺寸的类型可能处理更快。在此类机器上，32位int可能比16位short或8位char更快。  

[下一课 4.4 有符号整数](Chapter-4/lesson4.4-signed-integers.md)  
[返回主页](/)  
[上一课 4.2 Void类型](Chapter-2/lesson2.3-void-functions-non-value-returning-functions.md)