18.1 — 使用选择排序对数组排序  
=============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年7月3日下午1:47（太平洋夏令时间）  
2023年9月11日更新  

排序的必要性  
----------------  

数组排序是指将数组中所有元素按特定顺序排列的过程。排序数组在许多场景下都非常有用：  
* 电子邮件客户端通常按接收时间降序显示邮件（最新邮件通常相关性更高）  
* 通讯录名单通常按字母顺序排列（便于快速查找联系人）  
这些展示方式都需要在呈现前对数据进行排序。  

排序后的数组不仅能提升人类查找效率，对计算机也大有裨益。例如：  
* 在无序名单中查找某个名字需要遍历整个数组  
* 在按字母排序的名单中，当遇到首个字母顺序大于目标名字时即可停止搜索（因为后续名字必定更大）  

对于包含百万元素的数组，采用优化算法只需20次比较即可完成搜索！但排序本身是相对昂贵的操作，通常只在需要多次搜索时才值得进行。  

在某些情况下，排序能直接消除搜索需求：  
* 查找最高分时，已排序数组的最高分必然位于首/末位（取决于排序方向）  

排序原理  
----------------  

排序算法通常通过反复比较元素对并交换位置来实现。比较顺序因算法而异，交换条件取决于排序目标（升序或降序）。  

交换两个元素可使用C++标准库中的`std::swap()`函数（定义于utility头文件）：  
```cpp
#include <iostream>
#include <utility>

int main()
{
    int x{ 2 };
    int y{ 4 };
    std::cout << "交换前: x = " << x << ", y = " << y << '\n';
    std::swap(x, y); // 交换x和y的值
    std::cout << "交换后: x = " << x << ", y = " << y << '\n';
    return 0;
}
```
输出结果：  
```
交换前: x = 2, y = 4  
交换后: x = 4, y = 2  
```

选择排序  
----------------  

**选择排序（selection sort）**是最易理解的排序算法之一（尽管效率较低），其升序排序步骤如下：  
1. 从索引0开始，遍历数组找到最小值  
2. 将该最小值与索引0处的元素交换  
3. 从下一个索引开始重复步骤1-2  

示例数组`{ 30, 50, 20, 10, 40 }`的排序过程：  
1. 找到最小值10，与索引0交换 → `{10, 50, 20, 30, 40}`  
2. 从索引1找到最小值20，交换 → `{10, 20, 50, 30, 40}`  
3. 从索引2找到最小值30，交换 → `{10, 20, 30, 50, 40}`  
4. 从索引3找到最小值40，交换 → `{10, 20, 30, 40, 50}`  
5. 最后一个元素自动有序  

C++实现代码：  
```cpp
#include <iostream>
#include <iterator>
#include <utility>

int main()
{
    int array[]{ 30, 50, 20, 10, 40 };
    constexpr int length{ static_cast<int>(std::size(array)) };

    // 遍历每个元素（最后一个会自动有序）
    for (int startIndex{ 0 }; startIndex < length - 1; ++startIndex)
    {
        int smallestIndex{ startIndex }; // 当前迭代的最小元素索引

        // 在剩余数组中寻找更小元素
        for (int currentIndex{ startIndex + 1 }; currentIndex < length; ++currentIndex)
        {
            if (array[currentIndex] < array[smallestIndex])
                smallestIndex = currentIndex;
        }

        std::swap(array[startIndex], array[smallestIndex]); // 交换元素
    }

    // 打印排序结果
    for (int index{ 0 }; index < length; ++index)
        std::cout << array[index] << ' ';

    std::cout << '\n';
    return 0;
}
```
该算法使用**嵌套循环（nested loop）**：  
* 外层循环（startIndex）逐个遍历元素  
* 内层循环（currentIndex）在剩余数组中寻找最小值  
* 每次外层循环将最小值交换到正确位置  

标准库排序  
----------------  

C++标准库提供`std::sort`函数（定义于\<algorithm\>头文件）：  
```cpp
#include <algorithm>
#include <iostream>
#include <iterator>

int main()
{
    int array[]{ 30, 50, 20, 10, 40 };
    std::sort(std::begin(array), std::end(array)); // 默认升序

    for (int i{ 0 }; i < static_cast<int>(std::size(array)); ++i)
        std::cout << array[i] << ' ';

    std::cout << '\n';
    return 0;
}
```
`std::sort`使用类似快速排序的算法，效率远高于选择排序。  

测验解答  
----------------  

**问题1**  
手动演示数组`{30,60,20,50,40,10}`的选择排序过程：  
```
初始数组：30 60 20 50 40 10  
第1轮交换：10 60 20 50 40 30  
第2轮交换：10 20 60 50 40 30  
第3轮交换：10 20 30 50 40 60  
第4轮交换：10 20 30 40 50 60  
第5/6轮无交换  
```

**问题2**  
降序选择排序实现（修改比较条件）：  
```cpp
// 将比较运算符改为>
if (array[currentIndex] > array[largestIndex])
```

**问题3**  
冒泡排序（bubble sort）实现：  
```cpp
for (int iteration{0}; iteration < length-1; ++iteration) {
    for (int currentIndex{0}; currentIndex < length-1; ++currentIndex) {
        if (array[currentIndex] > array[currentIndex+1])
            std::swap(array[currentIndex], array[currentIndex+1]);
    }
}
```

**问题4**  
优化版冒泡排序（减少比较范围+提前终止）：  
```cpp
bool swapped{false};
int endOfArrayIndex{length - iteration};

// 内层循环范围优化
for (int currentIndex{0}; currentIndex < endOfArrayIndex-1; ++currentIndex) {
    if (array[currentIndex] > array[currentIndex+1]) {
        std::swap(...);
        swapped = true;
    }
}
if (!swapped) break; // 提前终止
```

[下一课 18.2 迭代器简介](Chapter-18/lesson18.2-introduction-to-iterators.md)  
[返回主页](/)  
[上一课 17.x 第17章总结与测验](Chapter-17/lesson17.x-chapter-17-summary-and-quiz.md)