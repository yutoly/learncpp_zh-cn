16.7 — 数组、循环与符号挑战解决方案
===================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日 PDT下午2:34（首次发布于2024年10月19日）

在课程[4.5 — 无符号整数及其避免原因](Chapter-4/lesson4.5-unsigned-integers-and-why-to-avoid-them.md)中，我们强调通常倾向使用有符号值来保存数量，因为无符号值可能产生意外行为。然而在课程[16.3 — std::vector与无符号长度及下标问题](Chapter-16/lesson16.3-stdvector-and-the-unsigned-length-and-subscript-problem.md)中，我们讨论了`std::vector`（及其他容器类）如何使用无符号整型`std::size_t`表示长度和索引。

这可能导致如下问题：

```cpp
#include <iostream>
#include <vector>

template <typename T>
void printReverse(const std::vector<T>& arr)
{
    for (std::size_t index{ arr.size() - 1 }; index >= 0; --index) // index为无符号类型
    {
        std::cout << arr[index] << ' ';
    }

    std::cout << '\n';
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printReverse(arr);

    return 0;
}
```

该代码首先倒序打印数组：

```
9 1 2 8 3 7 6 4
```

随后出现未定义行为，可能输出垃圾值或导致程序崩溃。

此处存在两个问题：首先循环条件`index >= 0`对于无符号类型始终为真，导致死循环；其次当`index`为0时递减会回绕为大正值，导致数组越界访问。

使用有符号类型作为循环变量可避免此类问题，但需要类型转换：

```cpp
#include <iostream>
#include <vector>

template <typename T>
void printReverse(const std::vector<T>& arr)
{
    for (int index{ static_cast<int>(arr.size()) - 1}; index >= 0; --index) // index为有符号类型
    {
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';
    }

    std::cout << '\n';
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printReverse(arr);

    return 0;
}
```

虽然功能正常，但`static_cast`的使用降低了代码可读性。

### 可行解决方案评估

#### 禁用符号转换警告（不推荐）
默认禁用符号转换警告虽可避免编译警告，但会掩盖潜在问题，不推荐使用。

#### 使用无符号循环变量
遵循标准库设计，使用`std::vector<T>::size_type`类型：

```cpp
for (typename std::vector<T>::size_type index{ 0 }; index < arr.size(); ++index)
```

但类型名称冗长，可用`std::size_t`替代：

```cpp
for (std::size_t index{ 0 }; index < arr.size(); ++index)
```

#### 使用有符号循环变量
1. **类型选择**：
   - 常规数组使用`int`
   - 大型数组使用`std::ptrdiff_t`（指针差值类型）
   - 自定义类型别名：

```cpp
using Index = std::ptrdiff_t;
for (Index index{ 0 }; index < static_cast<Index>(arr.size()); ++index)
```

2. **长度获取**：
   - C++20前使用静态转换：

```cpp
auto length{ static_cast<Index>(arr.size()) };
```

   - C++20使用`std::ssize()`：

```cpp
for (auto index{ std::ssize(arr)-1 }; index >= 0; --index)
```

3. **索引转换**：
   - 辅助函数`toUZ()`：

```cpp
template <typename T>
constexpr std::size_t toUZ(T value) {
    return static_cast<std::size_t>(value);
}

std::cout << arr[toUZ(index)] << ' ';
```

   - 自定义视图类`SignedArrayView`：

```cpp
SignedArrayView sarr{ arr };
std::cout << sarr[index] << ' '; // 使用有符号索引
```

#### 访问底层C风格数组
调用`data()`成员函数：

```cpp
std::cout << arr.data()[index] << ' '; // 避免符号转换
```

### 最佳实践：避免索引
推荐使用范围for循环（[16.8 — 基于范围的for循环](Chapter-16/lesson16.8-range-based-for-loops-for-each.md)）或迭代器（[18.2 — 迭代器简介](Chapter-18/lesson18.2-introduction-to-iterators.md)）来遍历数组。

**核心建议**：
> 尽可能避免使用整型索引访问数组元素。

[下一课 16.8 基于范围的for循环](Chapter-16/lesson16.8-range-based-for-loops-for-each.md)  
[返回主页](/)  
[上一课 16.6 数组与循环](Chapter-16/lesson16.6-arrays-and-loops.md)