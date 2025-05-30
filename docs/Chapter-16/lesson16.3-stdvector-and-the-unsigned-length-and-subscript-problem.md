16.3 — std::vector与无符号长度及下标问题
=================================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日 PDT下午2:28（更新于2024年11月11日）

在上一课[16.2 — std::vector与列表构造器简介](Chapter-16/lesson16.2-introduction-to-stdvector-and-list-constructors.md)中，我们介绍了`operator[]`运算符，该运算符可用于通过下标访问数组元素。

本课将探讨访问数组元素的其他方法，以及获取容器类长度（当前包含元素数量）的几种不同方式。但在深入之前，我们需要先讨论C++设计者的一个重大设计失误及其对标准库容器类的影响。

容器长度符号问题
----------------

首先明确一个基本观点：数组下标的类型应当与存储数组长度的类型相匹配，这样才能索引到最长可能数组的所有元素且不超出范围。

据Bjarne Stroustrup[回忆](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1428r0.pdf)，1997年左右设计C++标准库容器类时，设计者需要选择长度（及数组下标）使用有符号还是无符号类型。他们最终选择了无符号类型。

当时的理由包括：标准库数组类型的下标不能为负值，使用无符号类型可借助额外位获得更大的数组长度（这在16位时代很重要），范围检查只需一个条件判断（无需检查是否小于零）。但如今普遍认为这是错误的选择。我们现在知道：由于隐式转换规则（负值会隐式转换为大无符号数导致错误结果），使用无符号类型强制非负性并不可靠；在32位或64位系统上通常不需要额外位（因为很少需要创建超过20亿元素的数组）；常用的`operator[]`也不做范围检查。

在课程[4.5 — 无符号整数及其避免原因](Chapter-4/lesson4.5-unsigned-integers-and-why-to-avoid-them.md)中，我们讨论过优先使用有符号类型存储数量的原因，并指出混合有符号与无符号类型容易导致意外行为。标准库容器类对长度（及索引）使用无符号类型，使得使用这些类型时无法避免无符号值，这是当前无法改变的设计局限。

符号转换回顾：窄化转换与constexpr例外
----------------

在课程[10.4 — 窄化转换、列表初始化与constexpr初始化器](Chapter-10/lesson10.4-narrowing-conversions-list-initialization-and-constexpr-initializers.md)中，我们讨论过符号转换（有符号与无符号整型间转换）的要点，这对本章内容至关重要。

符号转换被视为窄化转换，因为一方类型无法容纳另一方类型的所有值。在运行时进行此类转换时，编译器会在禁止窄化转换的上下文中报错（如列表初始化），在其他允许的上下文中可能发出警告。

例如：

```cpp
#include <iostream>

void foo(unsigned int)
{
}

int main()
{
    int s { 5 };
    
    [[maybe_unused]] unsigned int u { s }; // 编译错误：列表初始化禁止窄化转换
    foo(s);                                // 可能警告：拷贝初始化允许窄化转换

    return 0;
}
```

但当转换值是constexpr且可安全转换时，符号转换不被视为窄化。例如：

```cpp
#include <iostream>

void foo(unsigned int)
{
}

int main()
{
    constexpr int s { 5 };                 // constexpr
    [[maybe_unused]] unsigned int u { s }; // 允许：s可安全转换
    foo(s);                                // 允许：同上

    return 0;
}
```

std::vector的长度与下标类型size_type
----------------

在课程[10.7 — 类型别名与typedef](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)中提及，标准库容器类定义了嵌套typedef成员`size_type`（有时写作`T::size_type`），用于表示容器的长度和下标类型。

`size_type`通常是`std::size_t`的别名，但在极少数情况下可能被覆盖。访问容器类的`size_type`成员时，需用完整模板名限定，如`std::vector<int>::size_type`。

关键洞察
----------------
`size_type`是标准库容器类中定义的类型别名，用于表示容器的长度和下标类型，默认情况下即为`std::size_t`。

获取std::vector长度的方式
----------------

1. **size()成员函数**  
返回无符号`size_type`类型长度：

```cpp
std::vector prime { 2, 3, 5, 7, 11 };
std::cout << "长度：" << prime.size(); // 返回size_type（即std::size_t）
```

2. **std::size()非成员函数（C++17）**  
调用容器的size()成员函数：

```cpp
std::cout << "长度：" << std::size(prime); // C++17
```

若需存储为有符号类型，建议使用static_cast：

```cpp
int length { static_cast<int>(prime.size()) };
```

3. **std::ssize()非成员函数（C++20）**  
返回有符号类型（通常为std::ptrdiff_t）：

```cpp
std::cout << "长度：" << std::ssize(prime); // C++20
auto length { std::ssize(prime) }; // 自动推导有符号类型
```

数组元素访问
----------------

1. **operator[]无边界检查**  
快速但存在未定义行为风险：

```cpp
std::cout << prime[9]; // 无效下标（未定义行为）
```

2. **at()成员函数进行运行时边界检查**  
安全但较慢：

```cpp
std::cout << prime.at(9); // 无效下标（抛出异常）
```

下标类型处理
----------------

- **constexpr有符号下标**  
允许隐式安全转换：

```cpp
constexpr int index { 3 };
std::cout << prime[index]; // 允许：非窄化转换
```

- **非constexpr有符号下标**  
可能产生窄化警告：

```cpp
int index { 3 };
std::cout << prime[index]; // 警告：隐式符号转换
```

建议改用`data()`成员函数访问底层C风格数组：

```cpp
std::cout << prime.data()[index]; // 无符号转换警告
```

测验
----------------

**问题1**  
初始化包含'h','e','l','l','o'的std::vector，输出长度和索引1的元素：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector arr { 'h', 'e', 'l', 'l', 'o' };
    std::cout << "数组有" << std::size(arr) << "个元素。\n";
    std::cout << arr[1] << arr.at(1);
    return 0;
}
```

**问题2**  
a) `size_type`是标准库容器中表示长度和下标的嵌套类型别名。  
b) 默认为无符号类型`std::size_t`。  
c) `size()`成员函数和`std::size()`返回`size_type`。

[下一课 16.4 传递std::vector](Chapter-16/lesson16.4-passing-stdvector.md)  
[返回主页](/)  
[上一课 16.2 std::vector与列表构造器简介](Chapter-16/lesson16.2-introduction-to-stdvector-and-list-constructors.md)