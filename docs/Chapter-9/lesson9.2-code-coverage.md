9.2 — 代码覆盖率  
====================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月23日（首次发布于2020年12月21日）  

在上一课[9.1 — 代码测试简介](Chapter-9/lesson9.1-introduction-to-testing-your-code.md)中，我们讨论了如何编写和保存简单测试。本课将探讨如何设计有效的测试用例来确保代码正确性。  

代码覆盖率（code coverage）  
----------------  

**代码覆盖率（code coverage）**用于描述测试过程中程序源代码的执行比例。存在多种不同的覆盖率指标，本节将介绍几个实用且常用的度量标准。  

语句覆盖（statement coverage）  
----------------  

**语句覆盖（statement coverage）**指测试用例执行代码中语句的百分比。  

考虑以下函数：  
```cpp
int foo(int x, int y)
{
    int z{ y };
    if (x > y)
    {
        z = x;
    }
    return z;
}
```  
调用`foo(1, 0)`可实现该函数的完整语句覆盖，因为函数中所有语句都将被执行。  

对于`isLowerVowel()`函数：  
```cpp
bool isLowerVowel(char c)
{
    switch (c) // 语句1
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true; // 语句2
    default:
        return false; // 语句3
    }
}
```  
该函数需要两次调用来测试所有语句，因为无法在单次调用中同时执行语句2和语句3。  

虽然追求100%语句覆盖率是好的，但通常不足以确保正确性。  

分支覆盖（branch coverage）  
----------------  

**分支覆盖（branch coverage）**指已执行分支的百分比，每个可能分支单独计数。`if语句`有两个分支——条件为`true`时执行的分支和条件为`false`时执行的分支（即使没有对应的`else语句`）。`switch语句`可能包含多个分支。  

```cpp
int foo(int x, int y)
{
    int z{ y };
    if (x > y)
    {
        z = x;
    }
    return z;
}
```  
之前的`foo(1, 0)`调用实现了100%语句覆盖并测试了`x > y`的情况，但仅获得50%分支覆盖。我们还需要调用`foo(0, 1)`来测试`if语句`未执行的情况。  

```cpp
bool isLowerVowel(char c)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    default:
        return false;
    }
}
```  
`isLowerVowel()`函数需要两次调用实现100%分支覆盖：一次（如`isLowerVowel('a')`）测试前几个case，另一次（如`isLowerVowel('q')`）测试default case。共用同一代码体的多个case无需单独测试——若其中一个有效，其余都应有效。  

考虑以下函数：  
```cpp
void compare(int x, int y)
{
    if (x > y)
        std::cout << x << " 大于 " << y << '\n'; // 情况1
    else if (x < y)
        std::cout << x << " 小于 " << y << '\n'; // 情况2
    else
        std::cout << x << " 等于 " << y << '\n'; // 情况3
}
```  
需要三次调用实现100%分支覆盖：  
1. `compare(1, 0)`测试第一个`if语句`为真的情况  
2. `compare(0, 1)`测试第一个`if语句`为假、第二个`if语句`为真的情况  
3. `compare(0, 0)`测试前两个`if语句`均为假的情况  

> **最佳实践**  
> 力争实现代码的100%分支覆盖率  

循环覆盖（loop coverage）  
----------------  

**循环覆盖（loop coverage）**（俗称**0、1、2测试**）指代码中的循环应测试0次、1次和2次迭代情况。若2次迭代工作正常，则所有大于2次的迭代都应正常。这三项测试即可覆盖所有可能性（因为循环不能执行负数次）。  

考虑：  
```cpp
#include <iostream>

void spam(int timesToPrint)
{
    for (int count{ 0 }; count < timesToPrint; ++count)
         std::cout << "Spam! ";
}
```  
要正确测试该函数中的循环，应进行三次调用：  
- `spam(0)`测试0次迭代  
- `spam(1)`测试1次迭代  
- `spam(2)`测试2次迭代  
若`spam(2)`正常工作，则`spam(n)`（n > 2）也应正常工作。  

> **最佳实践**  
> 使用`0、1、2测试`确保循环在不同迭代次数下正常工作  

测试不同输入类别  
----------------  

编写接受参数的函数或处理用户输入时，需考虑不同输入类别的影响。此处"类别"指具有相似特征的输入集合。  

例如，编写整数平方根函数时应测试哪些值？可从常规值（如4）开始，但也应测试0和负数。  

类别测试基本指南：  
- **整数**：确保函数处理负值、零和正值。必要时检查溢出  
- **浮点数**：考虑处理存在精度问题的值（略大于或小于预期值）。建议测试`0.1`和`-0.1`（略大于预期）、`0.7`和`-0.7`（略小于预期）  
- **字符串**：考虑处理空字符串、字母数字串、含空白符（前导/尾部/内部）的字符串、全空白字符串  
- **指针**：不要忘记测试`nullptr`（若暂不理解可先跳过）  

> **最佳实践**  
> 测试不同输入类别以确保单元正确处理  

测验时间  
----------------  

**问题1**  
什么是分支覆盖？  
  
<details><summary>答案</summary>分支覆盖率指已执行分支的百分比，条件成立与不成立的情况分别计数。</details>  

**问题2**  
以下函数最少需要多少次测试验证？  
```cpp
bool isLowerVowel(char c, bool yIsVowel)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    case 'y':
        return yIsVowel;
    default:
        return false;
    }
}
```  
  
<details><summary>答案</summary>4次测试。一次测试a/e/i/o/u情况，一次测试default情况，一次测试isLowerVowel('y', true)，以及一次测试isLowerVowel('y', false)。</details>  

[下一课9.3 — C++常见语义错误](Chapter-9/lesson9.3-common-semantic-errors-in-c.md)  
[返回主页](/)  
[上一课9.1 — 代码测试简介](Chapter-9/lesson9.1-introduction-to-testing-your-code.md)