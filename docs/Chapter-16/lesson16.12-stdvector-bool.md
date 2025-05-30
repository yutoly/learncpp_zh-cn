16.12 — std::vector\<bool\>
============================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年1月10日（首次发布于2023年9月11日）  

在课程[O.1 — 位标志与通过std::bitset进行的位操作](Chapter-O/lessonO.1-bit-flags-and-bit-manipulation-via-stdbitset.md)中，我们讨论过`std::bitset`能将8个布尔值压缩到1个字节中，并可通过其成员函数操作这些位。


`std::vector`有一个有趣的隐藏特性。针对`std::vector<bool>`存在特殊实现，可能通过类似方式将8个布尔值压缩到1个字节中，从而优化空间使用。


> **面向高级读者**  
> 当模板类对特定模板类型参数有不同实现时，称为**类模板特化（class template specialization）**。我们将在课程[26.4 — 类模板特化](Chapter-26/lesson26.4-class-template-specialization.md)中深入讨论此主题。


与专为位操作设计的`std::bitset`不同，`std::vector<bool>`缺乏位操作成员函数。


使用std::vector<bool>
----------------------

在大多数情况下，`std::vector<bool>`的表现与普通`std::vector`类似：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector<bool> v { true, false, false, true, true };
    
    for (int i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // 将索引4的布尔值改为false
    v[4] = false;

    for (int i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
```

在作者的64位机器上输出：

```
1 0 0 1 1
1 0 0 1 0
```

std::vector<bool>的权衡
------------------------

但`std::vector<bool>`存在需要注意的权衡点。


首先，其具有较高的开销（在作者机器上`sizeof(std::vector<bool>)`为40字节），因此只有当分配的布尔值数量超过架构开销时才能节省内存。


其次，其性能高度依赖具体实现（因标准不强制要求优化实现）。根据[此文](https://isocpp.org/blog/2012/11/on-vectorbool)，高度优化的实现可能显著快于替代方案，而优化不足的实现则会更慢。


第三也是最重要的，`std::vector<bool>`并非真正的vector（内存不要求连续），也不存储`bool`类型值（存储的是位集合），且不满足C++对容器（container）的定义。


虽然`std::vector<bool>`多数情况下表现类似vector，但它与标准库其他部分并非完全兼容。适用于其他元素类型的代码可能无法与其协作。


例如以下模板代码在`T`为非`bool`类型时正常工作：

```cpp
template<typename T>
void foo( std::vector<T>& v )
{
    T& first = v[0]; // 获取首个元素的引用
    // 对first进行操作
}
```

避免使用std::vector<bool>
---------------------------

现代共识认为通常应避免使用`std::vector<bool>`，因其性能提升可能难以弥补兼容性问题带来的麻烦。


遗憾的是，此优化版实现是默认启用的，且无法禁用。已有提议希望弃用`std::vector<bool>`，并正在研究替代方案（可能作为未来的`std::dynamic_bitset`）。


推荐方案如下：

* 当所需位数在编译期已知、布尔值数量适中（如低于64k）且`std::bitset`的操作集（如无迭代器支持）满足需求时，使用（constexpr）`std::bitset`
* 需要可调整大小的布尔容器且无需空间优化时，优先使用`std::vector<char>`。此类型表现符合标准容器
* 需要动态位集进行位操作时，采用第三方实现（如`boost::dynamic_bitset`）。此类类型不会伪装成标准库容器


> **最佳实践**  
> 优先选择`constexpr std::bitset`、`std::vector<char>`或第三方动态位集，而非`std::vector<bool>`。


[下一课 16.x — 第16章总结与测验](Chapter-16/lesson16.x-chapter-16-summary-and-quiz.md)  
[返回主页](/)  
[上一课 16.11 — std::vector与栈行为](Chapter-16/lesson16.11-stdvector-and-stack-behavior.md)