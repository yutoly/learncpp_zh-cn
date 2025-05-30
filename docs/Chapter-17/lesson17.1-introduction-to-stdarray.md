17.1 — std::array简介  
==================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年9月14日，下午4:39（太平洋夏令时）  
2024年7月22日  

在课程[16.1 — 容器与数组简介](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)中，我们介绍了容器与数组。总结如下：  
* 容器为无名对象集合（称为元素）提供存储  
* 数组在内存中连续分配元素，并通过下标索引支持快速直接访问  
* C++常用三种数组类型：`std::vector`、`std::array`和C风格数组  

在课程[16.10 — std::vector的调整大小与容量](Chapter-16/lesson16.10-stdvector-resizing-and-capacity.md)中，我们提到数组分为两类：  
* 固定大小数组（fixed-size arrays）要求在实例化时确定长度，后续不可更改。C风格数组和`std::array`均属此类  
* 动态数组（dynamic arrays）可在运行时调整大小。`std::vector`属于动态数组  

上一章我们重点讨论`std::vector`，因其快速、易用且功能多样。这使其成为需要数组容器时的首选类型。  

**为何不全程使用动态数组？**  
动态数组强大便捷，但与其他事物一样，其优势需付出代价：  
* `std::vector`性能略低于固定大小数组（多数情况下差异不明显，除非代码低效导致频繁重分配）  
* `std::vector`仅在极有限场景支持`constexpr`  

在现代C++中，后者尤为关键。constexpr数组能编写更健壮的代码，且编译器可进行更深度优化。应尽可能使用constexpr数组——若需constexpr数组，`std::array`是应选的容器类。  

> **最佳实践**  
> constexpr数组用`std::array`，非constexpr数组用`std::vector`  

**定义`std::array`**  
`std::array`定义于\<array\>头文件，设计理念类似`std::vector`，二者相似点多于差异。  
声明差异示例如下：  
```cpp
#include <array>  // std::array
#include <vector> // std::vector

int main()
{
    std::array<int, 5> a {};  // 5个int的std::array
    std::vector<int> b(5);    // 5个int的std::vector（对比）
    return 0;
}
```  
`std::array`声明含两个模板参数：首参数（`int`）为元素类型，次参数（`5`）为定义数组长度的整型非类型模板参数。  

> **相关内容**  
> 非类型模板参数详见课程[11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)  

**`std::array`长度必须是常量表达式**  
与可在运行时调整大小的`std::vector`不同，`std::array`长度必须是常量表达式。通常使用整数字面量、constexpr变量或无作用域枚举值：  
```cpp
#include <array>
int main()
{
    std::array<int, 7> a {};       // 字面常量
    constexpr int len { 8 };
    std::array<int, len> b {};     // constexpr变量
    enum Colors{ red, green, blue, max_colors };
    std::array<int, max_colors> c {}; // 枚举值
    #define DAYS_PER_WEEK 7        // 宏（不推荐，应改用constexpr变量）
    std::array<int, DAYS_PER_WEEK> d {};
    return 0;
}
```  
注意：非const变量和运行时常量不可用于长度：  
```cpp
#include <array>
#include <iostream>
void foo(const int length) // length是运行时常量
{
    std::array<int, length> e {}; // 错误：非常量表达式
}
int main()
{
    int numStudents{};       // 非const变量
    std::cin >> numStudents;
    std::array<int, numStudents> {}; // 错误：非常量表达式
    foo(7);
    return 0;
}
```  

> **警告**  
> 零长度`std::array`是合法但特殊的无数据类。调用任何访问其数据的成员函数（含`operator[]`）将导致未定义行为。可用`empty()`成员函数检测（返回`true`表示零长度）。  

**`std::array`的聚合初始化**  
`std::array`是聚合类型（aggregate），无构造函数，需通过聚合初始化（aggregate initialization）。聚合初始化允许直接初始化成员：使用花括号包裹的逗号分隔值列表。  

> **相关内容**  
> 结构体的聚合初始化详见课程[13.8 — 结构体的聚合初始化](Chapter-13/lesson13.8-struct-aggregate-initialization.md)  

```cpp
#include <array>
int main()
{
    std::array<int, 6> fibonnaci = { 0, 1, 1, 2, 3, 5 }; // 拷贝列表初始化
    std::array<int, 5> prime { 2, 3, 5, 7, 11 };          // 直接列表初始化（推荐）
    return 0;
}
```  
初始化按元素顺序执行（从索引0开始）。  
未提供初始化器时，元素默认初始化（default initialized），通常导致未初始化。推荐使用值初始化（value initialization）确保元素初始化：  
```cpp
#include <array>
#include <vector>
int main()
{
    std::array<int, 5> a;   // 默认初始化（int元素未初始化）
    std::array<int, 5> b{}; // 值初始化（int元素零初始化）（推荐）
    std::vector<int> v(5);  // 值初始化（对比）
    return 0;
}
```  
初始化器超长将编译错误；不足时剩余元素值初始化：  
```cpp
#include <array>
int main()
{
    std::array<int, 4> a { 1, 2, 3, 4, 5 }; // 错误：初始化器过多
    std::array<int, 4> b { 1, 2 };          // b[2]和b[3]值初始化
    return 0;
}
```  

**const与constexpr的`std::array`**  
`std::array`可声明为const：  
```cpp
#include <array>
int main()
{
    const std::array<int, 5> prime { 2, 3, 5, 7, 11 };
    return 0;
}
```  
即使元素未显式标记const，仍被视为const（因整个数组为const）。  
`std::array`完整支持constexpr：  
```cpp
#include <array>
int main()
{
    constexpr std::array<int, 5> prime { 2, 3, 5, 7, 11 };
    return 0;
}
```  
constexpr支持是选用`std::array`的关键原因。  

> **最佳实践**  
> 尽可能将`std::array`定义为constexpr。若非constexpr，考虑改用`std::vector`  

**C++17的类模板参数推导（CTAD）**  
C++17中，通过CTAD（class template argument deduction）可从初始化器推导`std::array`的元素类型和长度：  
```cpp
#include <array>
int main()
{
    constexpr std::array a1 { 9, 7, 5, 3, 1 }; // 推导为std::array<int, 5>
    constexpr std::array a2 { 9.7, 7.31 };     // 推导为std::array<double, 2>
    return 0;
}
```  
推荐优先使用此语法。若编译器不支持C++17，需显式提供类型和长度模板参数。  

> **最佳实践**  
> 使用类模板参数推导（CTAD）让编译器从初始化器推导`std::array`的类型和长度  

截至C++23，CTAD不支持部分省略模板参数，无法仅省略长度或类型：  
```cpp
#include <array>
int main()
{
    constexpr std::array<int> a1 {};     // 错误：缺少长度参数
    constexpr std::array<5> a2 {};       // 错误：缺少类型参数
    return 0;
}
```  

**C++20的`std::to_array`（省略长度）**  
函数模板实参推导（TAD）支持部分省略模板参数。C++20起可通过`std::to_array`辅助函数省略长度：  
```cpp
#include <array>
int main()
{
    constexpr auto myArray1 { std::to_array<int, 5>({ 9, 7, 5, 3, 1 }) }; // 指定类型和长度
    constexpr auto myArray2 { std::to_array<int>({ 9, 7, 5, 3, 1 }) };    // 仅指定类型，推导长度
    constexpr auto myArray3 { std::to_array({ 9, 7, 5, 3, 1 }) };         // 推导类型和长度
    return 0;
}
```  
注意：`std::to_array`比直接创建`std::array`开销更大，因需创建临时数组再拷贝初始化。故仅当类型无法有效推导时使用，避免在循环内重复创建。  
例如：创建`short`类型数组（无需显式指定长度）：  
```cpp
#include <array>
#include <iostream>
int main()
{
    constexpr auto shortArray { std::to_array<short>({ 9, 7, 5, 3, 1 }) };
    std::cout << sizeof(shortArray[0]) << '\n'; // 输出元素大小
    return 0;
}
```  

**通过`operator[]`访问元素**  
与`std::vector`相同，最常用下标运算符（`operator[]`）访问元素：  
```cpp
#include <array>
#include <iostream>
int main()
{
    constexpr std::array<int, 5> prime{ 2, 3, 5, 7, 11 };
    std::cout << prime[3]; // 输出索引3的值（7）
    std::cout << prime[9]; // 无效索引（未定义行为）
    return 0;
}
```  
注意：`operator[]`无边界检查。提供无效索引将导致未定义行为。  
其他索引方式将在下节课讨论。  

**测验**  
**问题1**  
`std::array`使用何种初始化方式？  
  
<details><summary>答案</summary>std::array是聚合类型，使用聚合初始化</details>  

为何未提供初始化器时应显式值初始化？  
  
<details><summary>答案</summary>无初始化器时默认初始化会使多数类型元素未初始化</details>  

**问题2**  
定义存储全年每日最高温（精确到0.1度）的`std::array`  
  
<details><summary>答案</summary><pre>#include &lt;array&gt;  
std::array&lt;double, 365&gt; highTemp {};</pre></details>  

**问题3**  
初始化含值‘h’, ‘e’, ‘l’, ‘l’, ‘o’的`std::array`，输出索引1的元素  
  
<details><summary>答案</summary><pre>#include &lt;array&gt;  
#include &lt;iostream&gt;  
int main()  
{  
    constexpr std::array arr { 'h', 'e', 'l', 'l', 'o' };  
    std::cout << arr[1] << '\n';  
    return 0;  
}</pre></details>  

[下一课 17.2 std::array的长度与索引](Chapter-17/lesson17.2-stdarray-length-and-indexing.md)  
[返回主页](/)  
[上一课 16.x 第16章总结与测验](Chapter-16/lesson16.x-chapter-16-summary-and-quiz.md)