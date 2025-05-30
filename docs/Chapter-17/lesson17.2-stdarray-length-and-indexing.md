17.2 — std::array的长度与索引
======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月15日（首次发布于2023年9月11日）

在课程[16.3 — std::vector的无符号长度与下标问题](Chapter-16/lesson16.3-stdvector-and-the-unsigned-length-and-subscript-problem.md)中，我们讨论了标准库容器类使用无符号值表示长度和索引的设计缺陷。由于`std::array`同属标准库容器类，它也面临相同问题。

本章将回顾`std::array`的索引获取与长度查询方法。虽然`std::vector`与`std::array`接口相似，但`std::array`对constexpr（常量表达式）有更全面的支持，因此我们将重点讨论相关特性。

建议先复习"符号转换属于窄化转换（constexpr时例外）"（见[16.3 — std::vector的无符号长度与下标问题](stdvector-and-the-unsigned-length-and-subscript-problem/#constexprconversions)）。

std::array的长度类型是std::size_t
----------------

`std::array`的实现基于模板结构体，其声明如下：

```cpp
template<typename T, std::size_t N> // N是非类型模板参数
struct array;
```

可见，表示数组长度的非类型模板参数`N`的类型为`std::size_t`。`std::size_t`是大型无符号整型。

> **相关内容**  
> 类模板（含结构体模板）详见[13.13 — 类模板](Chapter-13/lesson13.13-class-templates.md)  
> 非类型模板参数详见[11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)

定义`std::array`时，长度参数必须具有`std::size_t`类型或可转换为该类型。由于该值必须为constexpr，使用有符号整型时不会引发符号转换问题，编译器会在编译期将值转换为`std::size_t`且不视为窄化转换。

> **补充说明**  
> C++23前无`std::size_t`字面量后缀，因为`int`到`std::size_t`的隐式编译期转换通常能满足需求。新增后缀主要用于类型推导场景，例如`constexpr auto x { 0 }`推导为`int`而非`std::size_t`时，使用`0UZ`可明确类型。

std::array的长度与索引类型均为size_type（即std::size_t）
----------------

与`std::vector`类似，`std::array`定义了名为`size_type`的嵌套类型别名，用于表示容器长度（及支持的索引）类型。对`std::array`而言，`size_type`始终是`std::size_t`的别名。

注意定义`std::array`长度的非类型模板参数显式使用`std::size_t`而非`size_type`，因为此时`size_type`尚未定义。这是唯一显式使用`std::size_t`之处，其他位置均使用`size_type`。

获取std::array的长度
----------------

获取`std::array`长度有三种常用方式：

**方式一**：通过`size()`成员函数获取无符号`size_type`类型长度：

```cpp
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 9.0, 7.2, 5.4, 3.6, 1.8 };
    std::cout << "length: " << arr.size() << '\n'; // 返回`size_type`类型长度
    return 0;
}
```

输出：

```
length: 5
```

**方式二**（C++17起）：使用非成员函数`std::size()`，其内部调用`size()`成员函数：

```cpp
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr{ 9, 7, 5, 3, 1 };
    std::cout << "length: " << std::size(arr); // C++17，返回`size_type`类型
    return 0;
}
```

**方式三**（C++20起）：使用非成员函数`std::ssize()`，返回有符号大整型（通常为`std::ptrdiff_t`）：

```cpp
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 9, 7, 5, 3, 1 };
    std::cout << "length: " << std::ssize(arr); // C++20，返回有符号类型
    return 0;
}
```

获取constexpr类型的std::array长度
----------------

由于`std::array`长度是constexpr，上述函数即使对非constexpr对象调用也会返回constexpr值！这意味着我们可在常量表达式中使用这些函数，且返回值可隐式转换为`int`（非窄化转换）：

```cpp
#include <array>
#include <iostream>

int main()
{
    std::array arr { 9, 7, 5, 3, 1 }; // 注意：本示例中非constexpr
    constexpr int length{ std::size(arr) }; // 正确：返回constexpr std::size_t，可转换为int

    std::cout << "length: " << length << '\n';
    return 0;
}
```

> **Visual Studio用户注意**  
> 该示例可能错误触发警告C4365，[问题已提交微软](https://developercommunity.visualstudio.com/t/Bug:-C4365-triggers-incorrectly-for-cons/10372737)。

> **警告**  
> 由于语言缺陷，当`std::array`作为（const）引用参数传递时，上述函数返回非constexpr值：

```cpp
#include <array>
#include <iostream>

void printLength(const std::array<int, 5> &arr)
{
    constexpr int length{ std::size(arr) }; // 编译错误！
    std::cout << "length: " << length << '\n';
}

int main()
{
    std::array arr { 9, 7, 5, 3, 1 };
    constexpr int length{ std::size(arr) }; // 正常
    printLength(arr);
    return 0;
}
```

该缺陷已在C++23中通过[P2280提案](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2280r4.html)修复，目前支持该特性的编译器较少。

**解决方案**：将函数设为模板，数组长度作为非类型模板参数：

```cpp
template <auto Length>
void printLength(const std::array<int, Length> &arr)
{
    std::cout << "length: " << Length << '\n';
}
```

通过operator[]或at()成员函数索引std::array
----------------

在[17.1 — std::array简介](Chapter-17/lesson17.1-introduction-to-stdarray.md)中，我们提到最常用的索引方式是下标运算符`operator[]`，此时不进行边界检查，无效索引导致未定义行为。

与`std::vector`类似，`std::array`的`at()`成员函数执行运行时边界检查。建议避免使用该函数，因通常希望预先检查边界或需要编译期检查。

这两个函数均要求索引类型为`size_type`（`std::size_t`）。若使用constexpr值调用，编译器将执行constexpr转换至`std::size_t`，不视为窄化转换。

若使用非constexpr有符号整型索引，转换至`std::size_t`视为窄化转换，可能触发编译器警告。详见[16.3 — std::vector的无符号长度与下标问题](Chapter-16/lesson16.3-stdvector-and-the-unsigned-length-and-subscript-problem.md)。

std::get()为constexpr索引提供编译期边界检查
----------------

由于`std::array`长度是constexpr，若索引也是constexpr值，编译器可在编译期验证索引是否越界（越界则终止编译）。

`operator[]`默认不检查边界，`at()`仅运行时检查。由于函数参数不能是constexpr（即使对于constexpr或consteval函数），如何传递constexpr索引？

使用`std::get()`函数模板可对constexpr索引进行编译期边界检查，索引作为非类型模板参数：

```cpp
#include <array>
#include <iostream>

int main()
{
    constexpr std::array prime{ 2, 3, 5, 7, 11 };

    std::cout << std::get<3>(prime); // 打印索引3的元素
    std::cout << std::get<9>(prime); // 无效索引（编译错误）
    return 0;
}
```

`std::get()`内部通过static_assert检查非类型模板参数是否小于数组长度，否则触发编译错误。由于模板参数必须为constexpr，`std::get()`只能用constexpr索引调用。

测验时间
----------------

**问题1**  
初始化包含'h','e','l','l','o'的`std::array`，打印长度，并使用`operator[]`、`at()`和`std::get()`打印索引1的元素。预期输出：

```
The length is 5
eee
```

  
<details><summary>答案</summary>

```cpp
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 'h', 'e', 'l', 'l', 'o' };
    std::cout << "The length is " << std::size(arr) << '\n';
    std::cout << arr[1] << arr.at(1) << std::get<1>(arr) << '\n';
    return 0;
}
```
</details>

[下一课 17.3 — 传递与返回std::array](Chapter-17/lesson17.3-passing-and-returning-stdarray.md)  
[返回主页](/)  
[上一课 17.1 — std::array简介](Chapter-17/lesson17.1-introduction-to-stdarray.md)