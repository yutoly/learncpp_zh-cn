17.8 — C 风格数组退化  
============================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年7月11日 PDT时间下午6:20  
2025年1月17日  

C 风格数组传参的挑战  
C 语言的设计者面临一个难题。考虑以下简单程序：  
```cpp
#include <iostream>

void print(int val)
{
    std::cout << val;
}

int main()
{
    int x { 5 };
    print(x);

    return 0;
}
```  
当调用`print(x)`时，实参`x`的值（`5`）被拷贝到形参`val`中。函数体内将`val`的值（`5`）输出到控制台。由于`x`的拷贝成本低廉，此处没有问题。  

现在考虑使用1000元素的C风格整型数组替代单个整数的类似程序：  
```cpp
#include <iostream>

void printElementZero(int arr[1000])
{
    std::cout << arr[0]; // 输出第一个元素的值
}

int main()
{
    int x[1000] { 5 };   // 定义含1000元素的数组，x[0]初始化为5
    printElementZero(x);

    return 0;
}
```  
该程序同样能编译并输出预期值（`5`）。  

虽然此例代码与前例类似，但其工作机制与预期不同（下文将解释）。这是C设计者为解决两大挑战提出的方案：  

1. 每次函数调用时拷贝1000元素数组代价高昂（若元素是昂贵拷贝类型则更甚），需避免。但如何实现？C语言没有引用，无法通过传引用避免拷贝。  
2. 需编写能接受不同长度数组参数的函数。理想情况下，上述`printElementZero()`应能接受任意长度数组（因元素0必然存在）。不希望为每个可能长度都编写不同函数。但如何实现？C语法不支持"任意长度"数组，也不支持模板，且不同长度数组无法相互转换（因涉及高成本拷贝）。  

C设计者提出巧妙解决方案（出于兼容性被C++继承），完美解决这两个问题：  
```cpp
#include <iostream>

void printElementZero(int arr[1000]) // 不进行拷贝
{
    std::cout << arr[0]; // 输出第一个元素的值
}

int main()
{
    int x[7] { 5 };      // 定义7元素数组
    printElementZero(x); // 仍可运行！

    return 0;
}
```  
此例将7元素数组传递给预期1000元素的函数，且无任何拷贝。本节将解析其原理。  

同时探讨C设计者方案的缺陷及其在现代C++中的不适用性。  

数组到指针的转换（数组退化）  
多数情况下，C风格数组在表达式中使用时会被隐式转换为指向首元素（索引0）地址的指针。这被称为**数组退化（array decay）**或简称为**退化（decay）**。  

通过以下程序可验证：  
```cpp
#include <iomanip> // 用于std::boolalpha
#include <iostream>

int main()
{
    int arr[5]{ 9, 7, 5, 3, 1 }; // 数组元素类型为int

    // 验证arr退化为int*指针
    auto ptr{ arr }; // 求值导致退化，类型推导应为int*
    std::cout << std::boolalpha << (typeid(ptr) == typeid(int*)) << '\n'; // 若ptr类型是int*则输出true

    // 验证指针保存数组首元素地址
    std::cout << std::boolalpha << (&arr[0] == ptr) << '\n';

    return 0;
}
```  
在作者机器上输出：  
```
true
true
```  

退化生成的指针无特殊性，仅是保存首元素地址的普通指针。类似地，常量数组（如`const int arr[5]`）退化为指向常量的指针（`const int*`）。  

> **提示**  
> C++中少数情况C风格数组不会退化：  
> 1. 作为`sizeof()`或`typeid()`的参数  
> 2. 使用`operator&`获取数组地址  
> 3. 作为类类型成员传递  
> 4. 通过引用传递  

常见误解是将数组等同于指针。数组对象是元素序列，而指针对象仅保存地址。数组类型与退化指针类型不同：上例中`arr`类型为`int[5]`，退化后类型为`int*`。关键区别在于`int[5]`包含长度信息，而`int*`不包含。  

> **关键洞见**  
> 退化后的数组指针不知晓所指数组长度。"退化"一词正体现长度信息的丢失。  

对C风格数组的下标操作实际作用于退化指针  
由于C风格数组在求值时退化，下标操作实际作用于退化指针：  
```cpp
#include <iostream>

int main()
{
    const int arr[] { 9, 7, 5, 3, 1 };
    std::cout << arr[2]; // 对退化数组下标操作获取元素2，输出5

    return 0;
}
```  
也可直接在指针上使用`operator[]`：  
```cpp
#include <iostream>

int main()
{
    const int arr[] { 9, 7, 5, 3, 1 };
    
    const int* ptr{ arr };  // arr退化为指针
    std::cout << ptr[2];    // 对指针下标操作获取元素2，输出5

    return 0;
}
```  
此特性在特定场景下带来便利，下节课[17.9 — 指针算术与下标操作](Chapter-17/lesson17.9-pointer-arithmetic-and-subscripting.md)将深入解析指针行为。  

数组退化解决传参问题  
数组退化完美解决本节开篇的两个挑战：  
1. 传递C风格数组时，数组退化为指针，函数接收的是保存首元素地址的指针，避免拷贝。  
2. 不同长度的同类型数组（如`int[5]`和`int[7]`）将退化为相同指针类型（`int*`），实现类型兼容。  

> **关键洞见**  
> C风格数组以地址传递，即使表面看似值传递。  
> 同元素类型不同长度的C风格数组将退化为相同指针类型。  

以下示例演示：  
```cpp
#include <iostream>

void printElementZero(const int* arr) // 通过常量地址传递
{
    std::cout << arr[0];
}

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 };
    const int squares[] { 1, 4, 9, 25, 36, 49, 64, 81 };

    printElementZero(prime);   // prime退化为const int*指针
    printElementZero(squares); // squares退化为const int*指针

    return 0;
}
```  
程序输出：  
```
2
1
```  

C风格数组函数参数语法  
使用`int* arr`声明参数会模糊参数类型（数组指针还是单个整数指针）。推荐使用`int arr[]`语法：  
```cpp
#include <iostream>

void printElementZero(const int arr[]) // 与const int*等效
{
    std::cout << arr[0];
}

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 };
    const int squares[] { 1, 4, 9, 25, 36, 49, 64, 81 };

    printElementZero(prime);  // prime退化为指针
    printElementZero(squares); // squares退化为指针

    return 0;
}
```  
编译器将`const int arr[]`视为`const int*`，但更明确参数应为退化数组。注意方括号内长度信息会被忽略。  

> **最佳实践**  
> 接受C风格数组的函数参数应使用数组语法（如`int arr[]`）而非指针语法（如`int *arr`）。  

数组退化的隐患  
虽然退化方案巧妙，但长度信息丢失易导致错误：  
1. `sizeof()`对数组和退化指针返回不同值：  
```cpp
#include <iostream>

void printArraySize(int arr[])
{
    std::cout << sizeof(arr) << '\n'; // 输出4（假设32位地址）
}

int main()
{
    int arr[]{ 3, 2, 1 };
    std::cout << sizeof(arr) << '\n'; // 输出12（假设4字节int）
    printArraySize(arr);
    return 0;
}
```  
2. 重构代码时，非退化数组代码可能因退化导致编译失败或静默错误。  
3. 缺乏长度信息导致无法校验数组边界：  
```cpp
#include <iostream>

void printElement2(int arr[])
{
    std::cout << arr[2] << '\n'; // 如何确保数组至少有3元素？
}

int main()
{
    int a[]{ 3, 2, 1 };
    printElement2(a);  // 正常

    int b[]{ 7, 6 };
    printElement2(b);  // 编译通过但引发未定义行为

    int c{ 9 };
    printElement2(&c); // 编译通过但引发未定义行为

    return 0;
}
```  

解决长度问题的传统方法  
1. 同时传递数组和长度参数：  
```cpp
#include <cassert>
#include <iostream>

void printElement2(const int arr[], int length)
{
    assert(length > 2 && "printElement2: 数组过短");
    std::cout << arr[2] << '\n';
}

int main()
{
    constexpr int a[]{ 3, 2, 1 };
    printElement2(a, static_cast<int>(std::size(a)));  // 正常

    constexpr int b[]{ 7, 6 };
    printElement2(b, static_cast<int>(std::size(b)));  // 触发断言

    return 0;
}
```  
但存在调用者需确保长度匹配、符号转换问题、运行时断言局限等问题。  

2. 使用终止符标记数组结尾（如C风格字符串的`\0`）：  
- 优点：适用于隐式函数调用  
- 缺点：若终止符缺失导致越界、需特殊处理终止符、语义长度与实际长度不匹配  

现代C++应避免使用C风格数组  
由于非标准传参语义（地址传递替代值传递）及退化导致长度信息丢失的风险，建议尽可能避免使用C风格数组。  

> **最佳实践**  
> 尽可能避免使用C风格数组：  
> - 只读字符串用`std::string_view`  
> - 可变字符串用`std::string`  
> - 非全局constexpr数组用`std::array`  
> - 非constexpr数组用`std::vector`  

例外情况：  
1. 存储constexpr全局/静态局部数据（避免退化问题，索引无符号转换问题）  
2. 需要直接处理非constexpr C风格字符串参数（避免`std::string_view`转换开销）  

测验  
问题1  
什么是数组退化？其问题根源是什么？  
  
<details><summary>答案</summary>C风格数组在多数上下文中隐式转换为元素类型指针。退化导致长度信息丢失，易引发长度相关错误。</details>  

问题2  
为何C风格字符串使用空终止符？  
  
<details><summary>答案</summary>退化后数组丢失长度信息，空终止符使函数能确定字符串长度。</details>  

问题3（附加）  
为何C风格字符串使用空终止符而非显式传递长度？  
  
<details><summary>答案</summary>显式传递需维护字符串与长度的一致性，易出错。空终止符在隐式调用（如运算符重载）时更实用。</details>  

[下一课 17.9 指针算术与下标操作](Chapter-17/lesson17.9-pointer-arithmetic-and-subscripting.md)  
[返回主页](/)  
[上一课 17.7 C风格数组简介](Chapter-17/lesson17.7-introduction-to-c-style-arrays.md)