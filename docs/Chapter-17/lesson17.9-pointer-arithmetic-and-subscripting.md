17.9 — 指针算术与下标操作  
===========================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月10日（首次发布于2015年8月15日）  

在课程[16.1 — 容器与数组简介](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)中，我们提到数组在内存中按顺序存储。本课将深入探讨数组索引的数学原理。尽管后续课程不会直接使用索引数学，但本课内容将帮助您理解基于范围的for循环（range-based for loop）的底层机制，并为后续学习迭代器（iterator）奠定基础。  

指针算术（Pointer arithmetic）  
----------------  

**指针算术**允许我们对指针应用特定的整数算术运算符（加法、减法、递增或递减）来生成新的内存地址。  

给定指针`ptr`，`ptr + 1`返回内存中下一个对象（基于指向类型）的地址。例如，若`ptr`是`int*`类型且`int`占4字节，则`ptr + 1`将返回`ptr`之后4字节的地址，`ptr + 2`返回8字节后的地址。  
```cpp
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // 假设int占4字节

    std::cout << ptr << ' ' << (ptr + 1) << ' ' << (ptr + 2) << '\n';

    return 0;
}
```
作者机器输出：  
```
00AFFD80 00AFFD84 00AFFD88
```
每个地址间隔4字节。  

减法运算同理，`ptr - 1`返回前一个对象地址：  
```cpp
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // 假设int占4字节

    std::cout << ptr << ' ' << (ptr - 1) << ' ' << (ptr - 2) << '\n';

    return 0;
}
```
输出：  
```
00AFFD80 00AFFD7C 00AFFD78
```
每个地址递减4字节。  

> **关键洞察**  
> 指针算术返回的是下一个/前一个对象的地址（基于类型），而非单纯递增/递减地址。  

递增（`++`）和递减（`--`）运算符直接修改指针地址：  
```cpp
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // 假设int占4字节

    std::cout << ptr << '\n';

    ++ptr; // ptr = ptr + 1
    std::cout << ptr << '\n';

    --ptr; // ptr = ptr - 1
    std::cout << ptr << '\n';

    return 0;
}
```
输出：  
```
00AFFD80 00AFFD84 00AFFD80
```
> **警告**  
> 根据C++标准，指针算术仅在数组范围内（或尾后位置）有效。但现代编译器通常不强制此限制。  

下标操作实现原理  
----------------  

在[17.8 — C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)中，我们提到`operator[]`可应用于指针：  
```cpp
#include <iostream>

int main()
{
    const int arr[] { 9, 7, 5, 3, 1 };
    
    const int* ptr{ arr }; // 普通指针指向元素0
    std::cout << ptr[2];   // 输出元素2，打印5

    return 0;
}
```
下标操作`ptr[n]`等价于`*((ptr) + (n))`。初始化`ptr`指向数组首元素后，`ptr[2]`即`*(ptr + 2)`，获取索引2的元素。  

示例：  
```cpp
#include <iostream>

int main()
{
    const int arr[] { 3, 2, 1 };

    // 下标获取地址和值
    std::cout << &arr[0] << ' ' << &arr[1] << ' ' << &arr[2] << '\n';
    std::cout << arr[0] << ' ' << arr[1] << ' ' << arr[2] << '\n';

    // 指针算术等价操作
    std::cout << arr << ' ' << (arr + 1) << ' ' << (arr + 2) << '\n';
    std::cout << *arr << ' ' << *(arr + 1) << ' ' << *(arr + 2) << '\n';

    return 0;
}
```
输出：  
```
00AFFD80 00AFFD84 00AFFD88
3 2 1
00AFFD80 00AFFD84 00AFFD88
3 2 1
```
数组元素连续存储，故`*(arr + n)`返回第n个元素。这是数组从0开始索引的原因（避免减1运算）。  

> **趣闻**  
> 由于`ptr[n]`转换为`*((ptr) + (n))`，因此`n[ptr]`也合法，但应避免使用以免混淆。  

相对地址概念  
----------------  

数组下标本质是相对位置。若`ptr`指向元素3，则`ptr[1]`返回元素4：  
```cpp
#include <array>
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };
    const int *ptr { arr }; // 指向元素0

    std::cout << *ptr << ptr[0] << '\n'; // 99
    std::cout << *(ptr+1) << ptr[1] << '\n'; // 88

    ptr = &arr[3]; // 指向元素3

    std::cout << *ptr << ptr[0] << '\n'; // 66
    std::cout << *(ptr+1) << ptr[1] << '\n'; // 55
 
    return 0;
}
```
建议仅在从数组起始位置索引时使用下标操作，相对定位时使用指针算术。  

> **最佳实践**  
> 从数组起始位置（元素0）索引时优先使用下标，其他相对定位使用指针算术。  

负索引  
----------------  

C风格数组支持负下标。`ptr[-1]`等价于`*(ptr - 1)`：  
```cpp
#include <array>
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };
    const int* ptr { &arr[3] }; // 指向元素3

    std::cout << *ptr << ptr[0] << '\n'; // 66
    std::cout << *(ptr-1) << ptr[-1] << '\n'; // 77
 
    return 0;
}
```

遍历数组  
----------------  

指针算术常用于遍历C风格数组：  
```cpp
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	const int* begin{ arr };                // begin指向起始元素
	const int* end{ arr + std::size(arr) }; // end指向尾后元素

	for (; begin != end; ++begin)           // 遍历至end（不包含）
	{
		std::cout << *begin << ' ';     // 解引用获取当前元素
	}

	return 0;
}
```
输出：  
```
9 7 5 3 1
```
`end`指向尾后地址是合法的（只要不解引用）。  

> **提示**  
> 指针算术结果需在数组有效范围内或尾后位置，否则是未定义行为。  

重构示例：  
```cpp
#include <iostream>

void printArray(const int* begin, const int* end)
{
	for (; begin != end; ++begin)
	{
		std::cout << *begin << ' ';
	}
	std::cout << '\n';
}

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	const int* begin{ arr };
	const int* end{ arr + std::size(arr) };

	printArray(begin, end);

	return 0;
}
```
该程序无需显式传递数组即可编译运行，`begin`和`end`包含遍历所需信息。  

基于范围的for循环实现  
----------------  

基于范围的for循环底层使用指针算术：  
```cpp
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	for (auto e : arr)         // 从begin遍历到end
	{
		std::cout << e << ' ';
	}

	return 0;
}
```
其实现类似于：  
```cpp
{
    auto __begin = arr;                // 起始表达式
    auto __end = arr + std::size(arr); // 终止表达式

    for ( ; __begin != __end; ++__begin)
    {
        auto e = *__begin;         // 范围声明
        std::cout << e << ' ';     // 循环语句
    }
}
```

测验时间  
----------------  

**问题1a**  
为何`arr[0]`等同于`*arr`？  
  
<details><summary>答案</summary>`arr[0]`等价于`*((arr) + (0))`，即`*arr`。</details>  

[下一课 17.10 C风格字符串](Chapter-17/lesson17.10-c-style-strings.md)  
[返回主页](/)  
[上一课 17.8 C风格数组退化](Chapter-17/lesson17.8-c-style-array-decay.md)