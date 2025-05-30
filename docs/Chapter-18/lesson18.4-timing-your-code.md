18.4 — 代码计时  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2018年1月4日 下午3:10（太平洋标准时间）  
2023年10月31日  

编写代码时，有时会遇到不确定哪种方法性能更优的情况。如何判断优劣？  

一个简单方法是测量代码执行时间。C++11在chrono库中提供了相关功能，但其用法较为晦涩。好消息是我们可以将所有计时功能封装成一个类，方便在程序中复用。  

以下为计时器类实现：  

```cpp
#include <chrono> // 用于std::chrono功能

class Timer
{
private:
    // 类型别名简化嵌套类型访问
    using Clock = std::chrono::steady_clock;
    using Second = std::chrono::duration<double, std::ratio<1>>;
    
    std::chrono::time_point<Clock> m_beg{ Clock::now() };

public:
    void reset()
    {
        m_beg = Clock::now();
    }
    
    double elapsed() const
    {
        return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
    }
};
```  

使用方法：在main函数顶部（或需要开始计时的位置）实例化Timer对象，通过调用elapsed()成员函数获取运行时间：  

```cpp
#include <iostream>

int main()
{
    Timer t;

    // 待计时代码置于此处

    std::cout << "运行时间: " << t.elapsed() << " 秒\n";

    return 0;
}
```  

实际示例：比较对10000元素数组进行排序的性能。首先使用先前章节的选择排序算法：  

```cpp
#include <array>
#include <chrono> // 用于std::chrono功能
#include <cstddef> // 用于std::size_t
#include <iostream>
#include <numeric> // 用于std::iota

const int g_arrayElements{ 10000 };

// Timer类定义同上

void sortArray(std::array<int, g_arrayElements>& array)
{
    for (std::size_t startIndex{ 0 }; startIndex < (g_arrayElements - 1); ++startIndex)
    {
        std::size_t smallestIndex{ startIndex };

        for (std::size_t currentIndex{ startIndex + 1 }; currentIndex < g_arrayElements; ++currentIndex)
        {
            if (array[currentIndex] < array[smallestIndex])
            {
                smallestIndex = currentIndex;
            }
        }

        std::swap(array[startIndex], array[smallestIndex]);
    }
}

int main()
{
    std::array<int, g_arrayElements> array;
    std::iota(array.rbegin(), array.rend(), 1); // 填充数组值为10000到1

    Timer t;
    sortArray(array);
    std::cout << "耗时: " << t.elapsed() << " 秒\n";

    return 0;
}
```  

在作者机器上三次运行结果分别为0.0507、0.0506和0.0498秒，平均约0.05秒。  

改用标准库的std::sort：  

```cpp
#include <algorithm> // 用于std::sort
// 其他头文件同上

int main()
{
    std::array<int, g_arrayElements> array;
    std::iota(array.rbegin(), array.rend(), 1);

    Timer t;
    std::ranges::sort(array); // C++20起
    // 非C++20编译器使用: std::sort(array.begin(), array.end());

    std::cout << "耗时: " << t.elapsed() << " 秒\n";

    return 0;
}
```  

作者机器结果：0.000693、0.000692和0.000699秒，约0.0007秒。本例中std::sort比手动实现的选择排序快约100倍！  

影响程序性能的因素  
----------------  

计时程序运行相对简单，但结果可能受以下因素显著影响：  

1. **构建目标类型**：确保使用发布构建（release build）而非调试构建（debug build）。调试构建通常禁用优化，例如上述std::sort示例在调试构建下耗时0.0235秒（增长33倍）。  

2. **后台进程**：关闭占用CPU、内存或硬盘资源的程序（如游戏、杀毒扫描）。即使空闲浏览器也可能因广告加载突然占用CPU。关闭越多后台程序，结果波动越小。  

3. **随机数生成**：使用随机数的程序可能因随机序列不同导致耗时波动。为使结果一致，可临时使用固定种子生成随机数。但需注意这可能掩盖实际性能特征。  

4. **用户输入**：避免在计时区间包含等待用户输入的时间，可通过命令行参数或文件输入绕过交互。  

性能测量准则  
----------------  

1. **最小采样量**：至少采集3次结果。若结果相近，可视为真实性能反映。若差异大则继续测量直至获得稳定结果，注意识别离群值。  

2. **波动处理**：若结果波动较大，可能是系统后台任务或程序内部随机性导致。  

3. **测量类型**：  
   - **绝对测量**（如"耗时10秒"）仅反映特定机器性能  
   - **相对测量**（如方案A比方案B快20%）更具普适性  

4. **交叉验证**：测量新方案后，应重新测量旧方案。若旧方案结果与初始一致，可确认比较有效性。若不一致，需重新测量所有方案。  

[下一课 19.1 — new与delete动态内存分配](Chapter-19/lesson19.1-dynamic-memory-allocation-with-new-and-delete.md)  
[返回主页](/)  
[上一课 18.3 — 标准库算法简介](Chapter-18/lesson18.3-introduction-to-standard-library-algorithms.md)