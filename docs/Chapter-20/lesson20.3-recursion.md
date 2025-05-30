20.3 — 递归（Recursion）
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年8月13日 下午9:30（首次发布）  
2024年2月5日（最后更新）  

**递归函数（recursive function）**是能够调用自身的函数。以下是一个设计欠佳的递归函数示例：

```cpp
#include <iostream>

void countDown(int count)
{
    std::cout << "压栈 " << count << '\n';
    countDown(count-1); // countDown() 递归调用自身
}

int main()
{
    countDown(5);
    return 0;
}
```

当调用countDown(5)时，会输出"压栈 5"并调用countDown(4)。该过程将无限重复，形成递归形式的无限循环。

在课程[20.2 — 栈与堆](Chapter-20/lesson20.2-the-stack-and-the-heap.md)中我们了解到，每个函数调用都会在调用栈（call stack）上分配数据。由于countDown()永不返回（只是不断递归调用），这些数据永远不会从栈中弹出！最终将导致栈溢出（stack overflow）并使程序崩溃。在作者的机器上，该程序最终计数至-11732后终止！

> **作者注**  
> **尾调用（tail call）**指函数末尾进行的递归调用。编译器可将其优化为迭代形式以避免栈溢出。若您运行上述程序时未崩溃，可能是编译器进行了此类优化。

**递归终止条件（recursive termination）**  
递归调用与普通函数调用机制相似，但必须包含终止条件。以下为改进后的版本：

```cpp
#include <iostream>

void countDown(int count)
{
    std::cout << "压栈 " << count << '\n';

    if (count > 1) // 终止条件
        countDown(count-1);

    std::cout << "弹栈 " << count << '\n';
}

int main()
{
    countDown(5);
    return 0;
}
```

程序输出如下：

```
压栈 5
压栈 4
压栈 3
压栈 2
压栈 1
弹栈 1
弹栈 2
弹栈 3
弹栈 4
弹栈 5
```

此时调用栈状态为：

```
countDown(1)
countDown(2)
countDown(3)
countDown(4)
countDown(5)
main()
```

**实用示例**  
更典型的递归函数示例：

```cpp
// 计算1到sumto的整数和（包含两端）
// 负数返回0
int sumTo(int sumto)
{
    if (sumto <= 0)
        return 0; // 异常输入处理
    if (sumto == 1)
        return 1; // 基准情形（终止条件）

    return sumTo(sumto - 1) + sumto; // 递归调用
}
```

以sumTo(5)为例的调用过程：

```
sumTo(5) → sumTo(4)+5
sumTo(4) → sumTo(3)+4
sumTo(3) → sumTo(2)+3
sumTo(2) → sumTo(1)+2
sumTo(1) → 1
```

栈展开过程：

```
sumTo(1)返回1 → sumTo(2)=1+2=3  
sumTo(3)=3+3=6 → sumTo(4)=6+4=10  
sumTo(5)=10+5=15
```

**递归算法（recursive algorithms）**  
递归算法通常通过解决子问题来构建最终解。**基准情形（base case）**指能直接得出结果的简单输入，如sumTo(1)=1。

**斐波那契数列（Fibonacci numbers）**  
数学定义：

```
F(n) = 0（n=0）
       1（n=1）
       F(n-1)+F(n-2)（n>1）
```

递归实现：

```cpp
#include <iostream>

int fibonacci(int count)
{
    if (count == 0) return 0;
    if (count == 1) return 1;
    return fibonacci(count-1) + fibonacci(count-2);
}

int main()
{
    for (int count{0}; count < 13; ++count)
        std::cout << fibonacci(count) << ' ';
}
```

输出：`0 1 1 2 3 5 8 13 21 34 55 89 144`

**记忆化算法（memoization algorithms）**  
原始算法效率低下（调用1205次），优化版本：

```cpp
#include <iostream>
#include <vector>

int fibonacci(std::size_t count)
{
    static std::vector<int> results{0, 1};
    if (count < results.size()) return results[count];
    results.push_back(fibonacci(count-1) + fibonacci(count-2));
    return results[count];
}

int main()
{
    for (int count{0}; count < 13; ++count)
        std::cout << fibonacci(static_cast<std::size_t>(count)) << ' ';
}
```

优化后仅调用35次。

**递归 vs 迭代（recursive vs iterative）**  
递归版本通常更简洁但效率较低（函数调用开销大）。选择建议：

* 递归代码更简洁时优先使用
* 递归深度可控时
* 迭代版本需手动管理栈时
* 非性能关键代码

> **最佳实践**  
> 优先选择迭代，除非递归显著提升可读性。

**测验**  
1. 阶乘函数：

```cpp
int factorial(int n)
{
    if (n <= 0) return 1;
    return factorial(n-1) * n;
}
```

2. 数位求和：

```cpp
int sumDigits(int x)
{
    if (x < 10) return x;
    return sumDigits(x/10) + x%10;
}
```

3a. 二进制输出：

```cpp
void printBinary(int x)
{
    if (x == 0) return;
    printBinary(x/2);
    std::cout << x%2;
}
```

3b. 处理负数：

```cpp
void printBinary(unsigned int n)
{
    if (n > 1) printBinary(n/2);
    std::cout << n%2;
}

// 调用：
printBinary(static_cast<unsigned int>(x));
```

[下一课 20.4 命令行参数](Chapter-20/lesson20.4-command-line-arguments.md)  
[返回主页](/)  
[上一课 20.2 栈与堆](Chapter-20/lesson20.2-the-stack-and-the-heap.md)