17.3 — 传递与返回 std::array  
========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月2日（首次发布于2023年9月11日）  

`std::array`类型的对象可以像其他对象一样传递给函数。若按值传递`std::array`，将产生昂贵的拷贝操作。因此，通常通过（const）引用传递`std::array`以避免拷贝。  

由于`std::array`的元素类型和数组长度都是类型信息的一部分，作为函数参数时需显式指定两者：  

```cpp
#include <array>
#include <iostream>

void passByRef(const std::array<int, 5>& arr) // 必须显式指定<int, 5>
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // CTAD推导为std::array<int, 5>
    passByRef(arr);
    return 0;
}
```  

当前CTAD（类模板参数推导）不适用于函数参数，因此不能仅用`std::array`让编译器推导模板参数。  

### 使用函数模板传递不同类型/长度的std::array  

要创建能接受任意元素类型和长度的函数，需定义同时模板化元素类型（T）和长度（N）的函数模板：  

```cpp
#include <array>
#include <iostream>

template <typename T, std::size_t N> // 模板参数声明与std::array一致
void passByRef(const std::array<T, N>& arr)
{
    static_assert(N != 0); // 确保非零长度
    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{9,7,5,3,1};       // std::array<int,5>
    std::array arr2{1,2,3,4,5,6};    // std::array<int,6>
    std::array arr3{1.2,3.4,5.6};    // std::array<double,3>
    passByRef(arr);  // 实例化为passByRef<int,5>
    passByRef(arr2); // 实例化为passByRef<int,6>
    passByRef(arr3); // 实例化为passByRef<double,3>
    return 0;
}
```  

> **警告**  
> `std::array`的非类型模板参数类型应为`std::size_t`而非`int`，因标准库定义为`template<class T, std::size_t N> struct array;`。使用`int`会导致模板参数不匹配。  

### 仅模板化长度  

若只需模板化长度，可显式指定元素类型：  

```cpp
template <std::size_t N> 
void passByRef(const std::array<int, N>& arr) // 元素类型固定为int
{
    static_assert(N != 0);
    std::cout << arr[0] << '\n';
}
```  

### C++20自动非类型模板参数  

C++20允许使用`auto`推导非类型模板参数类型：  

```cpp
template <typename T, auto N> // 使用auto推导N的类型
void passByRef(const std::array<T, N>& arr)
{
    static_assert(N != 0);
    std::cout << arr[0] << '\n';
}
```  

### 静态断言数组长度  

使用`static_assert`确保数组长度满足要求：  

```cpp
template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    static_assert(N > 3); // 编译时检查长度
    std::cout << arr[3] << '\n';
}
```  

### 返回std::array  

#### 按值返回  
适用于以下情况：  
- 数组不大  
- 元素类型拷贝成本低  
- 非性能敏感场景  

```cpp
template <typename T, std::size_t N>
std::array<T, N> inputArray()
{
    std::array<T, N> arr{};
    // ...填充数组逻辑
    return arr; // 返回拷贝
}
```  

#### 通过输出参数返回  
使用非常量引用避免拷贝：  

```cpp
template <typename T, std::size_t N>
void inputArray(std::array<T, N>& arr) // 输出参数
{
    // ...填充数组逻辑
}
```  

#### 返回std::vector替代  
`std::vector`支持移动语义，可高效返回：  

```cpp
std::vector<int> createVector()
{
    std::vector<int> vec;
    // ...填充逻辑
    return vec; // 移动而非拷贝
}
```  

### 测验  

**问题1**  
完成打印数组函数：  

```cpp
template <typename T, std::size_t N>
void printArray(const std::array<T, N>& arr)
{
    std::cout << "The array (";
    auto sep = "";
    for (const auto& e : arr) {
        std::cout << sep << e;
        sep = ", ";
    }
    std::cout << ") has length " << N << '\n';
}
```  

[下一课 17.4 — 类类型的std::array与大括号省略](Chapter-17/lesson17.4-stdarray-of-class-types-and-brace-elision.md)  
[返回主页](/)  
[上一课 17.2 — std::array的长度与索引](Chapter-17/lesson17.2-stdarray-length-and-indexing.md)