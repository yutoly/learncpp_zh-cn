16.2 — std::vector与列表构造函数简介  
=========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年9月28日 PDT下午4:34（首次发布于2024年12月26日）

在上节课[16.1 — 容器与数组简介](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)中，我们介绍了容器和数组。本节将重点讲解本章的核心数组类型`std::vector（标准向量容器）`，并解决上节课提出的可扩展性挑战。

std::vector简介  
----------------

`std::vector`是C++标准容器库中实现数组功能的容器类，定义于\<vector\>头文件。作为类模板，其元素类型由模板类型参数指定。例如`std::vector<int>`声明元素类型为int的向量。

实例化`std::vector`对象示例：

```cpp
#include <vector>

int main()
{
    // 值初始化（使用默认构造函数）
    std::vector<int> empty{}; // 包含0个int元素的向量
    return 0;
}
```

变量`empty`定义为元素类型为int的`std::vector`。值初始化使向量初始为空。

用值列表初始化  
----------------

多数情况下我们需要用特定值初始化容器：

```cpp
#include <vector>

int main()
{
    // 列表构造（使用列表构造函数）
    std::vector<int> primes{ 2, 3, 5, 7 };          // 包含4个int元素的向量
    std::vector vowels { 'a', 'e', 'i', 'o', 'u' }; // 使用CTAD（C++17）推导元素类型为char
    return 0;
}
```

列表构造函数（list constructor）功能：  
* 确保容器有足够存储空间  
* 设置容器长度为初始化值数量  
* 按顺序初始化元素值  

最佳实践：使用初始化列表构造容器。

访问数组元素  
----------------

使用下标运算符`operator[]`访问元素，数组采用零基索引（zero-based）：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector primes { 2, 3, 5, 7, 11 };
    std::cout << primes[0] << '\n'; // 输出第一个元素2
    return 0;
}
```

注意：越界访问会导致未定义行为（undefined behavior）。

构造指定长度的vector  
----------------

使用显式构造函数创建指定长度向量：

```cpp
std::vector<int> data(10); // 包含10个零初始化int元素的向量
```

注意：非空初始化列表优先匹配列表构造函数：

```cpp
std::vector<int> v1{10}; // 创建单元素向量（值为10）
std::vector<int> v2(10); // 创建10元素向量（零初始化）
```

const与constexpr限制  
----------------

`std::vector`可声明为const：

```cpp
const std::vector<int> primes{2,3,5}; // 元素不可修改
```

但`std::vector`不能声明为constexpr，此时应使用`std::array`。

测验  
----------------

**问题1**  
使用CTAD定义包含前5个正平方数的向量。  
<details><summary>答案</summary>`std::vector squares{1,4,9,16,25};`</details>

**问题2**  
`vector<int> v1{5}`与`v2(5)`的区别？  
<details><summary>答案</summary>v1为单元素向量，v2为5元素零初始化向量</details>

**问题3**  
定义存储365天高温的向量。  
<details><summary>答案</summary>`std::vector<double> temperature(365);`</details>

**问题4**  
编写三整数求和程序。  
<details><summary>答案</summary>（代码实现略）</details>

[下一课 16.3 — std::vector的无符号长度与下标问题](Chapter-16/lesson16.3-stdvector-and-the-unsigned-length-and-subscript-problem.md)  
[返回主页](/)  
[上一课 16.1 — 容器与数组简介](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)