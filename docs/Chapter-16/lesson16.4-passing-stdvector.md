16.4 — 传递std::vector  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日 PDT下午2:28  
2024年3月21日  

传递std::vector对象  
----------------  

`std::vector`类型的对象可以像其他对象一样传递给函数。这意味着如果我们按值（by value）传递`std::vector`，会产生昂贵的拷贝。因此，通常我们通过（常量）引用（const reference）传递`std::vector`以避免此类拷贝。  

由于`std::vector`的元素类型是其类型信息的一部分，因此当我们将`std::vector`作为函数参数时，必须显式指定元素类型：  

```cpp
#include <iostream>
#include <vector>

void passByRef(const std::vector<int>& arr) // 必须显式指定<int>
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes); // 正确：传递std::vector<int>

    return 0;
}
```  

传递不同元素类型的vector  
----------------  

由于`passByRef()`函数需要`std::vector<int>`参数，我们无法传递其他元素类型的vector：  

```cpp
int main()
{
    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl); // 编译错误：std::vector<double>无法转换为std::vector<int>
}
```  

在C++17或更新标准中，若尝试使用CTAD（类模板参数推导）解决此问题：  

```cpp
void passByRef(const std::vector& arr) // 编译错误：CTAD不能用于推导函数参数
```  

虽然CTAD可在定义vector时根据初始化器推导元素类型，但目前不支持函数参数推导。  

函数模板解决方案  
----------------  

我们可以创建参数化元素类型的函数模板（function template）：  

```cpp
template <typename T>
void passByRef(const std::vector<T>& arr)
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 }; // 实例化passByRef(const std::vector<int>&)
    std::vector dbl{ 1.1, 2.2, 3.3 };     // 实例化passByRef(const std::vector<double>&)
}
```  

通过模板参数`T`，该函数模板可处理任意元素类型的`std::vector`。  

通用模板与缩写函数模板  
----------------  

我们也可创建接受任意类型对象的通用模板：  

```cpp
template <typename T>
void passByRef(const T& arr) // 接受支持operator[]的任何类型
{
    std::cout << arr[0] << '\n';
}
```  

在C++20中，可使用缩写函数模板（abbreviated function template）：  

```cpp
void passByRef(const auto& arr) // 缩写函数模板
```  

这两种方法适用于`std::array`、`std::string`等类型，但需注意类型语义是否合理。  

数组长度断言  
----------------  

考虑以下模板函数：  

```cpp
template <typename T>
void printElement3(const std::vector<T>& arr)
{
    std::cout << arr[3] << '\n'; // 存在越界风险
}
```  

当传入长度不足的vector时会导致未定义行为（undefined behavior）。建议：  

1. 在调试构建中使用运行时断言（runtime assert）检查`arr.size()`  
2. 优先使用支持`constexpr`的容器（如`std::array`）  
3. 避免依赖vector最小长度的函数设计  

测验  
----------------  

**问题1**  
编写函数：接收`std::vector`和索引参数，越界时输出错误，否则打印元素值。  

样例程序应输出：  

```
元素值为2  
无效索引  
元素值为1.1  
无效索引  
```  

[查看答案]  
```cpp
template <typename T>
void printElement(const std::vector<T>& arr, int index)
{
    if (index < 0 || index >= static_cast<int>(arr.size()))
        std::cout << "无效索引\n";
    else
        std::cout << "元素值为" << arr[static_cast<std::size_t>(index)] << '\n';
}
```  

[下一课 16.5 返回std::vector与移动语义简介](Chapter-16/lesson16.5-returning-stdvector-and-an-introduction-to-move-semantics.md)  
[返回主页](/)    
[上一课 16.3 std::vector的无符号长度与下标问题](Chapter-16/lesson16.3-stdvector-and-the-unsigned-length-and-subscript-problem.md)