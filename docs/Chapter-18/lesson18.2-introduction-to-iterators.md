18.2 — 迭代器（iterator）简介  
================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2019年12月17日 上午10:38（PST时区）  
2025年2月11日更新  

在编程中遍历数组（或其他数据结构）是非常常见的操作。迄今为止，我们已经学习过多种遍历方式：带索引的循环（`for`循环和`while`循环）、指针与指针算术运算，以及基于范围的`for`循环（range-based for-loop）：  
```cpp
#include <array>
#include <cstddef>
#include <iostream>

int main()
{
    // C++17中变量arr的类型推导为std::array<int, 7>
    // 若编译报错请参阅下方警告说明
    std::array arr{ 0, 1, 2, 3, 4, 5, 6 };
    std::size_t length{ std::size(arr) };

    // 带显式索引的while循环
    std::size_t index{ 0 };
    while (index < length)
    {
        std::cout << arr[index] << ' ';
        ++index;
    }
    std::cout << '\n';

    // 带显式索引的for循环
    for (index = 0; index < length; ++index)
    {
        std::cout << arr[index] << ' ';
    }
    std::cout << '\n';

    // 指针实现的for循环（注意：ptr不能为const，因为需要递增）
    for (auto ptr{ &arr[0] }; ptr != (&arr[0] + length); ++ptr)
    {
        std::cout << *ptr << ' ';
    }
    std::cout << '\n';

    // 基于范围的for循环
    for (int i : arr)
    {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    return 0;
}
```  

> **警告**  
> 本课示例使用C++17的**类模板参数推导（class template argument deduction）**特性，根据初始化器推导模板变量的模板参数。上例中，当编译器看到`std::array arr{ 0, 1, 2, 3, 4, 5, 6 };`时，会推导出我们需要`std::array<int, 7> arr { 0, 1, 2, 3, 4, 5, 6 };`。  
>  
> 若编译器未启用C++17，将出现类似"missing template arguments before ‘arr’"的错误。此时建议按照课程[0.12 — 配置编译器：选择语言标准](Chapter-0/lesson0.12-configuring-your-compiler-choosing-a-language-standard.md)启用C++17。若无法启用，可将使用类模板参数推导的代码替换为显式模板参数（例如将`std::array arr{ 0, 1, 2, 3, 4, 5, 6 };`替换为`std::array<int, 7> arr { 0, 1, 2, 3, 4, 5, 6 };`）。  

若仅通过索引访问元素，使用索引循环会涉及不必要的冗余代码。此外，这种方式仅适用于容器（如数组）直接支持元素访问的情况（链表等容器不具备此特性）。  

指针与指针算术实现的循环较为冗长，且不熟悉指针算术规则的读者可能难以理解。这种方式也要求元素内存连续（数组满足此条件，但链表、树、映射等容器不满足）。  

> **进阶阅读**  
> 指针（不含算术运算）也可用于遍历某些非连续结构。例如链表中，每个元素通过指针连接前驱元素，可通过指针链遍历整个链表。  

基于范围的`for`循环更为灵活，其遍历机制对用户透明，且适用于各种数据结构（数组、链表、树、映射等）。其实现原理是什么？答案就是迭代器。  

迭代器（iterator）  
----------------  

**迭代器（iterator）**是专门设计用于遍历容器（如数组中的值或字符串中的字符）的对象，可依次访问每个元素。  

容器可能提供多种迭代器类型。例如数组容器可能提供正序迭代器（向前遍历）和反向迭代器（逆向遍历）。  

创建适当类型的迭代器后，程序员即可使用迭代器提供的接口来遍历和访问元素，无需关心具体的遍历方式或容器内部的数据存储结构。由于C++迭代器通常采用统一接口进行遍历（`operator++`移至下一元素）和访问（`operator*`访问当前元素），我们可使用一致的方法遍历各种不同类型的容器。  

指针作为迭代器  
----------------  

最简单的迭代器是指针，通过指针算术运算可遍历内存连续存储的数据。让我们通过指针算术重新实现数组遍历：  
```cpp
#include <array>
#include <iostream>

int main()
{
    std::array arr{ 0, 1, 2, 3, 4, 5, 6 };

    auto begin{ &arr[0] };
    // 注意此处指向最后一个元素之后的位置
    auto end{ begin + std::size(arr) };

    // 指针实现的for循环
    for (auto ptr{ begin }; ptr != end; ++ptr) // ++移至下一元素
    {
        std::cout << *ptr << ' '; // 解引用获取当前元素值
    }
    std::cout << '\n';

    return 0;
}
```  
输出：  
```
0 1 2 3 4 5 6 
```  

上述代码定义了两个变量：`begin`（指向容器起始位置）和`end`（标记结束位置）。对于数组，结束标记通常是容器末元素后一位的内存地址。  

指针在`begin`与`end`之间迭代，通过解引用访问当前元素。  

> **警告**  
> 避免使用以下方式计算结束标记：  
> ```cpp
> int* end{ &arr[std::size(arr)] };
> ```  
> 这将导致未定义行为，因为`arr[std::size(arr)]`隐式解引用越界元素。  
>  
> 正确做法：  
> ```cpp
> int* end{ arr.data() + std::size(arr) }; // data()返回首元素指针
> ```  

标准库迭代器  
----------------  

遍历操作如此常见，因此所有标准库容器都直接支持迭代。通过成员函数`begin()`和`end()`可便捷获取容器的起始与结束迭代器：  
```cpp
#include <array>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // 通过begin和end成员函数获取迭代器
    auto begin{ array.begin() };
    auto end{ array.end() };

    for (auto p{ begin }; p != end; ++p) // ++移至下一元素
    {
        std::cout << *p << ' '; // 解引用获取当前元素值
    }
    std::cout << '\n';

    return 0;
}
```  
输出：  
```
1 2 3 
```  

`<iterator>`头文件还包含两个通用函数`std::begin`和`std::end`：  

> **提示**  
> C风格数组的`std::begin`和`std::end`定义于\<iterator\>头文件。  
> 支持迭代器的容器的`std::begin`和`std::end`定义于各自头文件（如\<array\>、\<vector\>）。  

```cpp
#include <array>    // 包含<iterator>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // 使用std::begin和std::end获取迭代器
    auto begin{ std::begin(array) };
    auto end{ std::end(array) };

    for (auto p{ begin }; p != end; ++p) // ++移至下一元素
    {
        std::cout << *p << ' '; // 解引用获取当前元素值
    }
    std::cout << '\n';

    return 0;
}
```  
输出同上。  

目前无需关注迭代器的具体类型（后续章节详解），关键点在于迭代器封装了遍历容器的细节。我们只需关注四个要素：起始点、结束点、`operator++`移至下一元素，`operator*`访问当前元素。  

迭代器的operator<与operator!=  
----------------  

在课程[8.10 — for语句](Chapter-8/lesson8.10-for-statements.md)中，我们建议循环条件中使用`operator<`而非`operator!=`进行数值比较：  
```cpp
    for (index = 0; index < length; ++index)
```  

对于迭代器，惯例使用`operator!=`检测是否到达结束元素：  
```cpp
    for (auto p{ begin }; p != end; ++p)
```  
因为部分迭代器类型不支持关系比较，而`operator!=`适用于所有迭代器类型。  

回归基于范围的for循环  
----------------  

所有具有`begin()`和`end()`成员函数，或支持`std::begin()`和`std::end()`的类型，均可用于基于范围的`for`循环：  
```cpp
#include <array>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // 与前文循环实现完全相同
    for (int i : array)
    {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    return 0;
}
```  

底层机制中，基于范围的`for`循环调用容器类型的`begin()`和`end()`。`std::array`具有这两个成员函数，因此可用于该循环。C风格固定数组也可通过`std::begin`和`std::end`实现遍历，但动态C风格数组（或退化的C风格数组）不可用，因其类型信息不包含数组长度。  

后续章节将学习如何为自定义类型添加这些函数以支持基于范围的`for`循环。  

基于范围的`for`循环并非唯一使用迭代器的场景，`std::sort`等算法也依赖迭代器。了解迭代器后，您会发现标准库中广泛使用它们。  

迭代器失效（悬空迭代器）  
----------------  

与指针和引用类似，当被迭代元素地址变化或被销毁时，迭代器可能变为"悬空状态"。此时称迭代器**失效（invalidated）**，访问失效迭代器会导致未定义行为。  

某些修改容器的操作（如向`std::vector`添加元素）可能导致元素地址变化，此时指向这些元素的迭代器将失效。优质的C++参考文档应注明哪些容器操作可能导致迭代器失效，例如[cppreference中std::vector的"迭代器失效"章节](https://en.cppreference.com/w/cpp/container/vector#Iterator_invalidation)。  

由于基于范围的`for`循环底层使用迭代器，必须避免在遍历容器时导致其迭代器失效：  
```cpp
#include <vector>

int main()
{
    std::vector v { 0, 1, 2, 3 };

    for (auto num : v) // 隐式迭代v
    {
        if (num % 2 == 0)
            v.push_back(num + 1); // 导致v的迭代器失效时，将产生未定义行为
    }

    return 0;
}
```  

另一失效示例：  
```cpp
#include <iostream>
#include <vector>

int main()
{
	std::vector v{ 1, 2, 3, 4, 5, 6, 7 };

	auto it{ v.begin() };

	++it; // 移至第二个元素
	std::cout << *it << '\n'; // 正常：输出2

	v.erase(it); // 删除当前迭代元素

	// erase()会使指向被删除元素（及后续元素）的迭代器失效
	// 迭代器"it"现已失效

	++it; // 未定义行为
	std::cout << *it << '\n'; // 未定义行为

	return 0;
}
```  

失效迭代器可通过重新赋值有效迭代器（如`begin()`、`end()`或其他返回迭代器的函数）恢复有效性。`erase()`函数返回指向被删元素下一位置的迭代器（若删除末元素则返回`end()`）。因此可修正代码如下：  
```cpp
#include <iostream>
#include <vector>

int main()
{
	std::vector v{ 1, 2, 3, 4, 5, 6, 7 };

	auto it{ v.begin() };

	++it; // 移至第二个元素
	std::cout << *it << '\n';

	it = v.erase(it); // 删除当前元素，将it设为下一元素

	std::cout << *it << '\n'; // 现在正常，输出3

	return 0;
}
```  

[下一课 18.3 标准库算法简介](Chapter-18/lesson18.3-introduction-to-standard-library-algorithms.md)  
[返回主页](/)  
[上一课 18.1 使用选择排序对数组排序](Chapter-18/lesson18.1-sorting-an-array-using-selection-sort.md)  
（感谢nascardriver对本课的重要贡献）