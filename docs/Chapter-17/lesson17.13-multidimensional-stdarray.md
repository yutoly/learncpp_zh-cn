17.13 — 多维std::array
====================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日 下午4:18（PDT时间）  
2024年6月26日更新  

在上一课（[17.12 — 多维C风格数组](Chapter-17/lesson17.12-multidimensional-c-style-arrays.md)）中，我们讨论了C风格的多维数组：  
```cpp
    // C风格二维数组
    int arr[3][4] { 
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }};
```  
但正如您所知，我们通常希望避免使用C风格数组（除非用于存储全局数据）。本课我们将探讨如何用`std::array`实现多维数组。  

标准库无多维数组类  
注意`std::array`本身是单维数组实现。因此首先要问的是"标准库是否有专门的多维数组类？"答案是...没有。  

二维`std::array`  
创建二维`std::array`的标准方法是定义外层`std::array`的模板类型参数为另一个`std::array`：  
```cpp
    std::array<std::array<int, 4>, 3> arr {{  // 注意双大括号
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};
```  
需要注意以下要点：  
* 初始化多维`std::array`时需使用双大括号（原因见课程[17.4 — 类类型的std::array与括号省略](Chapter-17/lesson17.4-stdarray-of-class-types-and-brace-elision.md)）  
* 语法冗长且可读性差  
* 由于模板嵌套方式，数组维度顺序颠倒。期望3行4列的数组应使用`arr[3][4]`，但`std::array<std::array<int, 4>, 3>`顺序相反  

元素访问方式与C风格数组相同：  
```cpp
    std::cout << arr[1][2]; // 输出第1行第2列元素
```  
传递二维`std::array`给函数的方式与一维相同：  
```cpp
#include <array>
#include <iostream>

template <typename T, std::size_t Row, std::size_t Col>
void printArray(const std::array<std::array<T, Col>, Row> &arr)
{
    for (const auto& arow: arr)   // 获取每行
    {
        for (const auto& e: arow) // 获取行内元素
            std::cout << e << ' ';

        std::cout << '\n';
    }
}

int main()
{
    std::array<std::array<int, 4>, 3>  arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    printArray(arr);
    return 0;
}
```  
三维或更高维`std::array`的语法更加冗长！  

使用别名模板简化二维`std::array`  
在课程[10.7 — 类型别名与typedef](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)中，我们介绍了类型别名。但普通类型别名需显式指定所有模板参数：  
```cpp
using Array2dint34 = std::array<std::array<int, 4>, 3>;
```  
这需要为每个类型和维度组合创建别名。使用别名模板（alias template）更高效：  
```cpp
// 二维std::array的别名模板
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;
```  
现在可用`Array2d<int, 3, 4>`表示3×4的整型二维数组：  
```cpp
#include <array>
#include <iostream>

template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;

template <typename T, std::size_t Row, std::size_t Col>
void printArray(const Array2d<T, Row, Col> &arr)
{
    for (const auto& arow: arr)
    {
        for (const auto& e: arow)
            std::cout << e << ' ';
        std::cout << '\n';
    }
}

int main()
{
    Array2d<int, 3, 4> arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    printArray(arr);
    return 0;
}
```  
此方法可扩展至三维数组：  
```cpp
// 三维std::array别名模板
template <typename T, std::size_t Row, std::size_t Col, std::size_t Depth>
using Array3d = std::array<std::array<std::array<T, Depth>, Col>, Row>;
```  

获取二维数组维度长度  
一维数组可用`size()`获取长度，但二维数组的`size()`仅返回第一维长度。危险做法是访问元素后调用`size()`：  
```cpp
std::cout << "列数：" << arr[0].size(); // 若第一维长度为0将导致未定义行为
```  
更安全的方式是通过模板参数获取维度：  
```cpp
template <typename T, std::size_t Row, std::size_t Col>
constexpr int rowLength(const Array2d<T, Row, Col>&)
{
    return Row;
}

template <typename T, std::size_t Row, std::size_t Col>
constexpr int colLength(const Array2d<T, Row, Col>&)
{
    return Col;
}
```  

数组扁平化  
多维数组面临以下挑战：  
* 定义和操作更复杂  
* 获取高维长度困难  
* 迭代嵌套层级深  

**扁平化（Flattening）**是将多维数组降维（通常至一维）的过程。例如将3×4二维数组转换为12元素一维数组。需通过接口模拟多维访问：  
```cpp
#include <array>
#include <iostream>
#include <functional>

template <typename T, std::size_t Row, std::size_t Col>
using ArrayFlat2d = std::array<T, Row * Col>;

template <typename T, std::size_t Row, std::size_t Col>
class ArrayView2d
{
private:
    std::reference_wrapper<ArrayFlat2d<T, Row, Col>> m_arr {};

public:
    ArrayView2d(ArrayFlat2d<T, Row, Col> &arr) : m_arr { arr } {}

    T& operator[](int i) { return m_arr.get()[static_cast<std::size_t>(i)]; }
    const T& operator[](int i) const { return m_arr.get()[static_cast<std::size_t>(i)]; }

    T& operator()(int row, int col) { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }
    const T& operator()(int row, int col) const { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }

    int rows() const { return static_cast<int>(Row); }
    int cols() const { return static_cast<int>(Col); }
    int length() const { return static_cast<int>(Row * Col); }
};

int main()
{
    ArrayFlat2d<int, 3, 4> arr {1,2,3,4,5,6,7,8,9,10,11,12};
    ArrayView2d<int, 3, 4> arrView { arr };

    // 使用单下标访问
    for (int i=0; i < arrView.length(); ++i)
        std::cout << arrView[i] << ' ';

    // 使用双下标访问
    for (int row=0; row < arrView.rows(); ++row)
    {
        for (int col=0; col < arrView.cols(); ++col)
            std::cout << arrView(row, col) << ' ';
        std::cout << '\n';
    }
    return 0;
}
```  

C++23的std::mdspan  
C++23引入的`std::mdspan`为连续元素序列提供多维接口：  
```cpp
#include <array>
#include <iostream>
#include <mdspan>

template <typename T, std::size_t Row, std::size_t Col>
using ArrayFlat2d = std::array<T, Row * Col>;

int main()
{
    ArrayFlat2d<int, 3, 4> arr {1,2,3,4,5,6,7,8,9,10,11,12};
    std::mdspan mdView { arr.data(), 3, 4 };

    // 多维下标访问
    for (std::size_t row=0; row < mdView.extents().extent(0); ++row)
    {
        for (std::size_t col=0; col < mdView.extents().extent(1); ++col)
            std::cout << mdView[row, col] << ' ';
        std::cout << '\n';
    }
    return 0;
}
```  
注意：  
* 构造`std::mdspan`需传入数据指针（可用`std::array::data()`获取）  
* C++23支持`operator[]`多下标访问  
* C++26将引入`std::mdarray`结合`std::array`和`std::mdspan`功能  

[下一课 17.x 第17章总结与测验](Chapter-17/lesson17.x-chapter-17-summary-and-quiz.md)  
[返回主页](/)  
[上一课 17.12 多维C风格数组](Chapter-17/lesson17.12-multidimensional-c-style-arrays.md)