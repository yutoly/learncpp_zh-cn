16.6 — 数组与循环
================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年7月2日下午2:03（太平洋夏令时）  
2024年12月14日  

在本章导论课（[16.1 — 容器与数组简介](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)）中，我们介绍了处理多个相关独立变量时出现的可扩展性挑战。本节我们将重新审视该问题，并讨论如何利用数组优雅解决此类问题。

### 变量可扩展性挑战再探
假设需要计算某班级学生的平均考试成绩。为简化示例，设班级仅有5名学生。

使用独立变量的实现方式：
```cpp
#include <iostream>

int main()
{
    // 声明5个整型变量（名称各不相同）
    int testScore1{ 84 };
    int testScore2{ 92 };
    int testScore3{ 76 };
    int testScore4{ 81 };
    int testScore5{ 56 };

    int average { (testScore1 + testScore2 + testScore3 + testScore4 + testScore5) / 5 };

    std::cout << "班级平均分: " << average << '\n';

    return 0;
}
```
此方案存在大量变量和重复输入。若处理30名或600名学生，工作量将剧增。添加新成绩时需声明新变量、初始化并加入计算，且必须同步更新除数，否则会导致语义错误。每次修改代码都可能引入新错误。

### 数组解决方案
改用`std::vector`（标准向量）优化：
```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector testScore { 84, 92, 76, 81, 56 };
    std::size_t length { testScore.size() };
    
    int average { (testScore[0] + testScore[1] + testScore[2] + testScore[3] + testScore[4])
        / static_cast<int>(length) };

    std::cout << "班级平均分: " << average << '\n';

    return 0;
}
```
此方案显著减少变量数量，且除数直接取自数组长度。但平均计算仍需显式列出每个元素，仅适用于固定长度数组。为支持不同长度数组，必须为每种长度编写独立计算逻辑。

### 数组与循环结合
利用循环变量作为动态索引：
```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector testScore { 84, 92, 76, 81, 56 };
    std::size_t length { testScore.size() };

    int average { 0 };
    for (std::size_t index{ 0 }; index < length; ++index) // 索引从0到length-1
        average += testScore[index];                     // 累加索引对应元素值
    average /= static_cast<int>(length);                 // 计算平均值

    std::cout << "班级平均分: " << average << '\n';

    return 0;
}
```
此方案具备最佳可维护性：  
1. 循环次数由数组长度决定  
2. 循环变量自动处理所有索引  
3. 增删成绩只需修改初始化列表，其余代码自动适配  

访问容器中每个元素的过程称为**遍历（traversal）**或**迭代（iteration）**。

> **作者注**  
> 容器类使用`size_t`类型表示长度和索引，后续课程[16.7 — 数组、循环与符号挑战解决方案](Chapter-16/lesson16.7-arrays-loops-and-sign-challenge-solutions.md)将讨论有符号索引。

### 模板、数组与循环实现可扩展性
三者结合实现泛型处理能力：  
- **数组**：免去元素命名  
- **循环**：免去显式索引  
- **模板**：参数化元素类型  

通过函数模板重构平均计算：
```cpp
#include <iostream>
#include <vector>

// 计算std::vector平均值的函数模板
template <typename T>
T calculateAverage(const std::vector<T>& arr)
{
    std::size_t length { arr.size() };
    
    T average { 0 };                                     // 平均值类型与元素类型一致
    for (std::size_t index{ 0 }; index < length; ++index)// 遍历所有元素
        average += arr[index];                           // 累加元素值
    average /= static_cast<int>(length);                 // 除以元素数量（整数除法）
    
    return average;
}

int main()
{
    std::vector class1 { 84, 92, 76, 81, 56 };
    std::cout << "1班平均分: " << calculateAverage(class1) << '\n'; // 计算5个整数的平均值

    std::vector class2 { 93.2, 88.6, 64.2, 81.0 };
    std::cout << "2班平均分: " << calculateAverage(class2) << '\n'; // 计算4个双精度浮点数的平均值
    
    return 0;
}
```
输出：
```
1班平均分: 77
2班平均分: 81.75
```
此模板函数支持任意元素类型和长度的`std::vector`，要求类型`T`支持`+=`和`/=`运算符。

### 遍历容器的典型应用
1. **计算新值**：如平均值、总和  
2. **搜索元素**：精确匹配、计数、最大值  
3. **操作元素**：输出、批量修改  
4. **重排元素**：排序（通常需嵌套循环，建议使用标准库算法）

### 数组与差一错误
使用索引遍历时需精确控制循环次数。常见错误包括：  
- 使用`index <= length`导致越界访问（引发未定义行为）  
- 正确做法：`index`从`0`开始，条件为`index < length`

### 测验
**问题1**  
使用循环打印向量元素：
```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
        std::cout << arr[index] << ' ';
    if (arr.size() > 0) std::cout << '\n';
    return 0;
}
```
输出：`4 6 7 3 8 2 1 9`

**问题2**  
实现打印数组的函数模板：
```cpp
template <typename T>
void printArray(const std::vector<T>& arr) {
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
        std::cout << arr[index] << ' ';
    if (arr.size() > 0) std::cout << '\n';
}
```

**问题3**  
实现带输入验证的搜索功能：
```cpp
#include <iostream>
#include <limits>
#include <vector>

// 输入验证函数
int getValidNumber() {
    int num{};
    do {
        std::cout << "输入1-9之间的整数: ";
        std::cin >> num;
        if (!std::cin) std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    } while (num < 1 || num > 9);
    return num;
}

// 搜索函数模板
template <typename T>
int findIndex(const std::vector<T>& arr, T val) {
    for (std::size_t index{ 0 }; index < arr.size(); ++index)
        if (arr[index] == val) return static_cast<int>(index);
    return -1; // 未找到返回-1
}
```

**问题4**  
扩展支持浮点数：
```cpp
// 泛型输入验证
template <typename T>
T getValidNumber(std::string_view prompt, T low, T high) {
    T val{};
    do {
        std::cout << prompt;
        std::cin >> val;
        if (!std::cin) std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    } while (val < low || val > high);
    return val;
}
```

**问题5**  
实现最大值函数模板：
```cpp
template <typename T>
T findMax(const std::vector<T>& arr) {
    if (arr.empty()) return T{};
    T max{ arr[0] };
    for (std::size_t i{1}; i < arr.size(); ++i)
        if (arr[i] > max) max = arr[i];
    return max;
}
```

**问题6**  
FizzBuzz游戏增强版：
```cpp
#include <cassert>
#include <iostream>
#include <string_view>
#include <vector>

void fizzbuzz(int count) {
    static const std::vector divisors{ 3,5,7,11,13,17,19 };
    static const std::vector<std::string_view> words{ 
        "fizz","buzz","pop","bang","jazz","pow","boom" 
    };
    assert(divisors.size() == words.size());

    for (int i{1}; i <= count; ++i) {
        bool printed{false};
        for (std::size_t j{0}; j < divisors.size(); ++j) {
            if (i % divisors[j] == 0) {
                std::cout << words[j];
                printed = true;
            }
        }
        if (!printed) std::cout << i;
        std::cout << '\n';
    }
}
```

[下一课 16.7 — 数组、循环与符号挑战解决方案](Chapter-16/lesson16.7-arrays-loops-and-sign-challenge-solutions.md)  
[返回主页](/)  
[上一课 16.5 — 返回std::vector及移动语义简介](Chapter-16/lesson16.5-returning-stdvector-and-an-introduction-to-move-semantics.md)