17\.x — 第17章总结与测验  
===================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月6日（首次发布于2015年10月5日）  

本章回顾  
----------------  

**固定长度数组（fixed-size arrays/fixed-length arrays）**要求在实例化时已知数组长度，且后续不可更改。C风格数组和`std::array`均属于固定长度数组。动态数组可在运行时调整大小，`std::vector`即为动态数组。  

`std::array`的长度必须是常量表达式，通常使用整数字面量、constexpr变量或非限定作用域枚举值。  

`std::array`是聚合类型（aggregate），没有构造函数，需通过聚合初始化（aggregate initialization）进行初始化。  

尽可能将`std::array`声明为constexpr。若非constexpr，建议改用`std::vector`。  

使用类模板参数推导（class template argument deduction，CTAD）让编译器根据初始值推导`std::array`的类型和长度。  

`std::array`的模板结构声明如下：  
```cpp
template<typename T, std::size_t N> // N是非类型模板参数
struct array;
```  
表示数组长度的非类型模板参数（non-type template parameter）`N`具有`std::size_t`类型。  

获取`std::array`长度的方法：  
* 使用`size()`成员函数（返回无符号`size_type`类型长度）  
* C++17可使用`std::size()`非成员函数（调用`size()`成员函数，返回无符号`size_type`类型）  
* C++20可使用`std::ssize()`非成员函数（返回有符号大整数类型长度，通常为`std::ptrdiff_t`）  

以上函数在被引用传递的`std::array`上调用时，返回长度不作为constexpr值。此缺陷已在C++23通过[P2280](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2280r4.html)修正。  

索引`std::array`的方法：  
* 使用下标运算符`operator[]`（无边界检查，无效索引导致未定义行为）  
* 使用`at()`成员函数（运行时边界检查，建议预先检查或使用编译时检查）  
* 使用`std::get()`函数模板（以非类型模板参数作为索引，进行编译时边界检查）  

通过函数模板`template <typename T, std::size_t N>`（C++20可用`template <typename T, auto N>`）可传递不同元素类型和长度的`std::array`。  

按值返回`std::array`会复制数组及其元素，若数组较小且元素复制成本低则可行。某些场景下使用输出参数（out parameter）更佳。  

使用结构体、类或数组初始化`std::array`且未指定元素类型时，需额外添加大括号以便编译器正确解析初始化方式。这是聚合初始化的特性，其他标准库容器类型（使用列表构造函数）无需双重大括号。  

C++中的聚合类型支持**大括号省略（brace elision）**规则，允许在特定情况下省略多重大括号。通常，使用标量值初始化`std::array`或显式指定每个元素的类类型/数组时，可省略大括号。  

不可创建引用数组，但可创建`std::reference_wrapper`数组（行为类似可修改的左值引用）。  

关于`std::reference_wrapper`的注意事项：  
* `operator=`可重定向引用（改变引用对象）  
* `std::reference_wrapper<T>`可隐式转换为`T&`  
* `get()`成员函数用于获取`T&`（更新引用对象时有用）  

`std::ref()`和`std::cref()`函数用于快速创建`std::reference_wrapper`和`const std::reference_wrapper`包装对象。  

尽可能使用`static_assert`确保通过CTAD创建的constexpr `std::array`具有正确初始值数量。  

C风格数组继承自C语言，是C++核心语言的内置特性。其特殊声明语法使用方括号（[]）表示数组类型，方括号内可选指定`std::size_t`类型的常量表达式长度。  

C风格数组是聚合类型，可通过聚合初始化。使用初始化列表初始化全部元素时，推荐省略长度让编译器推导。  

C风格数组可通过`operator[]`索引，索引可为有符号整数、无符号整数或非限定作用域枚举。这意味着C风格数组不受标准库容器类的符号转换问题影响。  

C风格数组可为const或constexpr。  

获取C风格数组长度的方法：  
* C++17使用`std::size()`非成员函数（返回无符号`std::size_t`类型）  
* C++20使用`std::ssize()`非成员函数（返回有符号大整数类型，通常为`std::ptrdiff_t`）  

多数情况下，C风格数组在表达式中使用时，会隐式转换为指向首元素的指针（索引0的地址），这种现象称为**数组退化（array decay）**。  

**指针算术（pointer arithmetic）**允许对指针应用整数算术运算符（加减、自增、自减）生成新内存地址。给定指针`ptr`，`ptr + 1`返回下一对象地址（基于所指类型）。  

从数组起始位置（元素0）索引时使用下标运算符，使索引与元素对齐。  
从给定元素相对定位时使用指针算术。  

C风格字符串是元素类型为`char`或`const char`的C风格数组，同样会发生数组退化。  

数组的**维度（dimension）**指选择元素所需的索引数量。  
仅含单维度的数组称为**一维数组（single-dimensional array/1d array）**。数组的数组称为**二维数组（two-dimensional array/2d array）**（使用双下标）。多维数组（multidimensional arrays）指维度超过一的数组。**扁平化（flattening）**指降低数组维度（通常至一维）。  

C++23中，`std::mdspan`是为连续元素序列提供多维数组接口的视图。  

测验时间  
----------------  

**问题1**  
以下代码片段有何错误？如何修复？  
a)  
```cpp
#include <array>
#include <iostream>

int main()
{
    std::array arr { 0, 1, 2, 3 };

    for (std::size_t count{ 0 }; count <= std::size(arr); ++count)
    {
        std::cout << arr[count] << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  
  
<details><summary>答案</summary>for循环存在差一错误，尝试访问不存在的索引4元素。修复：循环条件应使用<而非<=。</details>  

b)  
```cpp
#include <iostream>

void printArray(int array[])
{
    for (int element : array)
    {
        std::cout << element << ' ';
    }
}

int main()
{
    int array[] { 9, 7, 5, 3, 1 };

    printArray(array);

    std::cout << '\n';

    return 0;
}
```  
  
<details><summary>答案</summary>数组传递给printArray()时退化为指针，基于范围的for循环无法处理数组指针（因长度未知）。修复：改用不会退化的std::array。</details>  

c)  
```cpp
#include <array>
#include <iostream>

int main()
{
    std::cout << "Enter the number of test scores: ";
    std::size_t length{};
    std::cin >> length;

    std::array<int, length> scores;

    for (std::size_t i { 0 } ; i < length; ++i)
    {
        std::cout << "Enter score " << i << ": ";
        std::cin >> scores[i];
    }
    return 0;
}
```  
  
<details><summary>答案</summary>length不是常量表达式，不能用于定义std::array长度。修复：改用std::vector。</details>  

**问题2**  
实现Roscoe的药水商店程序，完整代码见原文解决方案部分。  

**问题3**  
实现纸牌游戏基础功能，完整代码见原文解决方案部分。  

**问题4**  
实现简化版21点游戏，完整代码见原文解决方案部分。  

**问题5**  
a) 修改程序处理Ace可为1或11的情况  
b) 处理平局情况  
c) 实现以上改进，完整代码见原文解决方案部分。  

[下一课 18.1 — 使用选择排序对数组排序](Chapter-18/lesson18.1-sorting-an-array-using-selection-sort.md)  
[返回主页](/)  
[上一课 17.13 — 多维std::array](Chapter-17/lesson17.13-multidimensional-stdarray.md)