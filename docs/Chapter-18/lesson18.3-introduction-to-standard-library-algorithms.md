18.3 — 标准库算法简介  
===================================================

[*nascardriver*](https://www.learncpp.com/author/nascardriver/ "查看 nascardriver 的所有文章")  
2024年9月4日（首次发布于2020年1月3日）  

新程序员通常花费大量时间编写自定义循环来完成相对简单的任务，例如排序、计数或搜索数组。这些循环容易出错且维护性差，因为循环结构本身可能难以理解。  

由于搜索、计数和排序是常见操作，C++标准库提供了大量函数，仅需几行代码即可完成这些任务。此外，这些标准库函数经过预测试、高效、适用于多种容器类型，许多还支持并行化（通过多CPU线程加速任务）。  

算法库的功能主要分为三类：  
* **检查器（Inspectors）** — 用于查看（不修改）容器数据。例如搜索和计数。  
* **修改器（Mutators）** — 用于修改容器数据。例如排序和洗牌。  
* **辅助器（Facilitators）** — 基于数据成员生成结果。例如数值乘法器或元素排序规则生成器。  

这些算法位于[算法库](https://en.cppreference.com/w/cpp/algorithm)。本节我们将探索常见算法——但实际更多，建议阅读参考链接了解全部内容！  

> **注意**  
> 所有算法均使用迭代器（iterator），若需复习基础知识，请参考课程[18.2 — 迭代器简介](Chapter-18/lesson18.2-introduction-to-iterators.md)。  

使用std::find按值查找元素  
----------------  
[`std::find`](https://en.cppreference.com/w/cpp/algorithm/find)在容器中搜索特定值的首次出现。接受三个参数：序列起始迭代器、结束迭代器和搜索值。返回指向元素的迭代器（找到时）或容器末尾迭代器（未找到）。  

示例：  
```
#include <algorithm>
#include <array>
#include <iostream>

int main()
{
    std::array arr{ 13, 90, 99, 5, 40, 80 };

    std::cout << "输入要查找和替换的值：";
    int search{};
    int replace{};
    std::cin >> search >> replace;

    // 输入验证省略

    auto found{ std::find(arr.begin(), arr.end(), search) };

    if (found == arr.end())
    {
        std::cout << "未找到 " << search << '\n';
    }
    else
    {
        *found = replace;
    }

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  
找到元素时的运行示例：  
```
输入要查找和替换的值：5 234
13 90 99 234 40 80
```  
未找到元素时的运行示例：  
```
输入要查找和替换的值：0 234
未找到 0
13 90 99 5 40 80
```  

使用std::find_if按条件查找元素  
----------------  
当需要匹配条件（如包含特定子串）而非精确值时，[`std::find_if`](https://en.cppreference.com/w/cpp/algorithm/find)是理想选择。该函数接受可调用对象（如函数指针或lambda），对每个元素调用该函数，返回true时表示匹配。  

示例（查找包含"nut"子串的元素）：  
```
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

bool containsNut(std::string_view str)
{
    return str.find("nut") != std::string_view::npos;
}

int main()
{
    std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

    auto found{ std::find_if(arr.begin(), arr.end(), containsNut) };

    if (found == arr.end())
    {
        std::cout << "无坚果\n";
    }
    else
    {
        std::cout << "找到 " << *found << '\n';
    }

    return 0;
}
```  
输出：  
```
找到 walnut
```  

使用std::count和std::count_if计数  
----------------  
[`std::count`](https://en.cppreference.com/w/cpp/algorithm/count)和[`std::count_if`](https://en.cppreference.com/w/cpp/algorithm/count)统计满足条件的元素出现次数。  

示例（统计包含"nut"子串的元素数量）：  
```
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

bool containsNut(std::string_view str)
{
	return str.find("nut") != std::string_view::npos;
}

int main()
{
	std::array<std::string_view, 5> arr{ "apple", "banana", "walnut", "lemon", "peanut" };

	auto nuts{ std::count_if(arr.begin(), arr.end(), containsNut) };

	std::cout << "找到 " << nuts << " 个坚果\n";

	return 0;
}
```  
输出：  
```
找到 2 个坚果
```  

使用std::sort自定义排序  
----------------  
[`std::sort`](https://en.cppreference.com/w/cpp/algorithm/sort)默认升序排序，但可通过第三个参数（比较函数）自定义排序规则。比较函数接受两个参数，返回true时第一个参数应排在前面。  

示例（使用greater函数降序排序）：  
```
#include <algorithm>
#include <array>
#include <iostream>

bool greater(int a, int b)
{
    return (a > b);
}

int main()
{
    std::array arr{ 13, 90, 99, 5, 40, 80 };

    std::sort(arr.begin(), arr.end(), greater);

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  
输出：  
```
99 90 80 40 13 5
```  

> **提示**  
> 由于降序排序常见，C++提供标准比较类型`std::greater`（需包含[functional](https://en.cppreference.com/w/cpp/header/functional)头文件）：  
> ```
> std::sort(arr.begin(), arr.end(), std::greater{}); // C++17+
> std::sort(arr.begin(), arr.end(), std::greater<int>{}); // C++17前
> ```  

深入解析std::sort原理（高级内容）  
----------------  
修改自[18.1 — 选择排序](Chapter-18/lesson18.1-sorting-an-array-using-selection-sort.md)的选择排序示例，展示比较函数工作原理：  
```
#include <functional>
#include <iostream>
#include <iterator>
#include <utility>

void sort(int* begin, int* end, std::function<bool(int, int)> compare)
{
    for (auto startElement{ begin }; startElement != end-1; ++startElement)
    {
        auto smallestElement{ startElement };

        for (auto currentElement{ std::next(startElement) }; currentElement != end; ++currentElement)
        {
            if (compare(*currentElement, *smallestElement))
            {
                smallestElement = currentElement;
            }
        }

        std::swap(*startElement, *smallestElement);
    }
}

int main()
{
    int array[]{ 2, 1, 9, 4, 5 };

    ::sort(std::begin(array), std::end(array), std::greater{});

    for (auto i : array)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  

使用std::for_each处理容器元素  
----------------  
[`std::for_each`](https://en.cppreference.com/w/cpp/algorithm/for_each)对容器所有元素应用自定义函数。示例（数组元素加倍）：  
```
#include <algorithm>
#include <array>
#include <iostream>

void doubleNumber(int& i)
{
    i *= 2;
}

int main()
{
    std::array arr{ 1, 2, 3, 4 };

    std::for_each(arr.begin(), arr.end(), doubleNumber);

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  
输出：  
```
2 4 6 8
```  

> **对比范围for循环**  
> C++20起可使用范围版本：  
> ```
> std::ranges::for_each(arr, doubleNumber);  // C++20+
> ```  
> 优势：  
> - 意图明确，避免变量误用  
> - 支持跳过元素（如`std::next(arr.begin())`跳过首元素）  
> - 可并行化处理大数据  

性能与执行顺序保证  
----------------  
多数算法提供性能保证，部分保证执行顺序。例如`std::for_each`保证顺序访问，而其他算法可能无此保证。  

> **最佳实践**  
> 使用算法前确认其性能和执行顺序是否符合需求。  

C++20范围（Ranges）  
----------------  
C++20引入范围概念，简化算法调用：  
```
std::ranges::for_each(arr, doubleNumber);  // 无需begin()/end()
```  

结论  
----------------  
算法库提供丰富功能，使代码更简洁健壮。虽然本节仅介绍部分内容，但多数算法使用方式相似，掌握基础后即可触类旁通。  

> **推荐视频**  
> [标准库算法概览](https://www.youtube.com/watch?v=2olsGf6JIkU)  

> **最佳实践**  
> 优先使用算法库函数而非自行实现相同功能。  

[下一课 18.4 代码计时](Chapter-18/lesson18.4-timing-your-code.md)  
[返回主页](/)  
[上一课 18.2 迭代器简介](Chapter-18/lesson18.2-introduction-to-iterators.md)