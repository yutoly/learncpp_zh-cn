8.10 — for语句  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月19日（首次发布于2007年6月25日）  

在C++中，使用最广泛的循环语句当属for语句。**for语句（for-statement）**（也称为**for循环（for-loop）**）在有明确循环变量（loop variable）时最为适用，因为它能简洁地定义、初始化、测试和修改循环变量。


自C++11起，存在两种不同类型的for循环。本章讲解经典for语句，更新的范围for语句（range-based for-loop）将在后续课程[16.8 — 基于范围的for循环（for-each）](Chapter-16/lesson16.8-range-based-for-loops-for-each.md)中介绍。


抽象形式中的for语句结构如下：

```
for (初始化语句; 条件; 末尾表达式)
   语句;
```

理解for语句工作原理的最佳方式，是将其转换为等效的while语句：

```
{ // 注意此处代码块
    初始化语句; // 用于定义循环变量
    while (条件)
    {
        语句; 
        末尾表达式; // 在条件重新评估前修改循环变量
    }
} // 循环内定义的变量在此处离开作用域
```

for语句的执行流程  
----------------  

for语句分三步执行：

1. **初始化语句（init-statement）**首先执行。该过程仅在循环初始化时发生一次。初始化语句通常用于变量定义与初始化，这些变量具有"循环作用域（loop scope）"——本质上是块作用域（block scope）的一种形式，变量从定义点存在至循环结束。在等效的while循环中，可见初始化语句位于包含循环的代码块内，因此当外层代码块结束时变量即离开作用域。

2. 每次循环迭代时，**条件（condition）**被评估。若结果为`true`，执行语句；若为`false`，循环终止，程序继续执行后续代码。

3. 语句执行后，评估**末尾表达式（end-expression）**。通常该表达式用于增减初始化语句中定义的循环变量。末尾表达式执行后，流程返回第二步（再次评估条件）。

> **关键洞察**  
> for语句各部分的执行顺序：  
> * 初始化语句  
> * 条件（若为false则在此终止循环）  
> * 循环体  
> * 末尾表达式（然后跳转回条件）  
>  
> 注意末尾表达式在循环体语句*之后*执行，随后才重新评估条件。


示例分析：  
```cpp
#include <iostream>

int main()
{
    for (int i{ 1 }; i <= 10; ++i)
        std::cout << i << ' ';

    std::cout << '\n';
    return 0;
}
```

1. 声明循环变量`i`并初始化为`1`  
2. 评估`i <= 10`，因`i`为1，结果为`true`，执行输出`1 `  
3. 执行`++i`将`i`递增至2，返回第二步  
循环持续直至`i`变为11时条件不满足，退出循环。最终输出：  
```
1 2 3 4 5 6 7 8 9 10 
```

等效while循环实现：  
```cpp
#include <iostream>

int main()
{
    { // 代码块确保i的作用域
        int i{ 1 }; // 初始化语句
        while (i <= 10) // 条件
        {
            std::cout << i << ' '; // 语句
            ++i; // 末尾表达式
        }
    }
    std::cout << '\n';
}
```

进阶示例  
----------------  

**指数计算函数**：  
```cpp
#include <cstdint> // 固定宽度整数类型

// 返回base^exponent ——注意溢出风险
std::int64_t pow(int base, int exponent)
{
    std::int64_t total{ 1 };
    for (int i{ 0 }; i < exponent; ++i)
        total *= base;
    return total;
}
```

**递减循环**：  
```cpp
#include <iostream>

int main()
{
    for (int i{ 9 }; i >= 0; --i)
        std::cout << i << ' ';
    std::cout << '\n';
    return 0;
}
// 输出：9 8 7 6 5 4 3 2 1 0
```

**步长修改**：  
```cpp
#include <iostream>

int main()
{
    for (int i{ 0 }; i <= 10; i += 2) // 每次递增2
        std::cout << i << ' ';
    std::cout << '\n';
    return 0;
}
// 输出：0 2 4 6 8 10
```

条件表达式陷阱  
----------------  
使用`operator!=`进行数值比较可能导致意外行为：  
```cpp
for (int i{ 0 }; i != 10; ++i) {
    if (i == 9) ++i; // 跳过10导致无限循环
}
```

> **最佳实践**  
> 在for循环条件中避免使用`operator!=`，优先使用`operator<`或`operator<=`。


常见错误  
----------------  
**差一错误（Off-by-one errors）**：  
```cpp
for (int i{ 1 }; i < 5; ++i) // 应使用<=
    std::cout << i << ' '; // 输出1 2 3 4（漏掉5）
```

省略表达式  
----------------  
可省略部分表达式，但需谨慎：  
```cpp
int i{ 0 };
for ( ; i < 10; ) { // 省略初始化和末尾表达式
    std::cout << i << ' ';
    ++i;
}
```

无限循环写法（不建议）：  
```cpp
for (;;) // 等效while(true)
    statement;
```

多变量控制  
----------------  
```cpp
#include <iostream>

int main()
{
    for (int x{0}, y{9}; x < 10; ++x, --y)
        std::cout << x << ' ' << y << '\n';
    return 0;
}
// 输出：
// 0 9
// 1 8 ... 9 0
```

嵌套循环  
----------------  
```cpp
#include <iostream>

int main()
{
    for (char c{'a'}; c <= 'e'; ++c) {
        std::cout << c;
        for (int i{0}; i < 3; ++i)
            std::cout << i;
        std::cout << '\n';
    }
    return 0;
}
// 输出：
// a012
// b012 ... e012
```

变量作用域  
----------------  
> **最佳实践**  
> 仅在循环内使用的变量应定义在循环作用域内。


结论  
----------------  
for语句因其将循环变量、条件和修改操作集中声明而成为最常用的循环结构。对于存在明确计数变量的场景优先使用for循环，无明确计数变量时选择while循环更合适。


测验  
----------------  

**问题1**  
编写打印0到20所有偶数的for循环：  
<details><summary>答案</summary>
```cpp
for (int i{0}; i <= 20; i += 2)
    std::cout << i << '\n';
```
</details>

**问题2**  
实现1到value求和的`sumTo()`函数：  
<details><summary>答案</summary>
```cpp
int sumTo(int value) {
    int total{0};
    for (int i{1}; i <= value; ++i)
        total += i;
    return total;
}
```
</details>

**问题3**  
以下代码错误原因：  
```cpp
for (unsigned i{9}; i >= 0; --i) // 无限循环
```
<details><summary>答案</summary>无符号变量i无法为负，条件永远为真导致死循环。</details>

**问题4**  
FizzBuzz游戏实现：  
<details><summary>答案</summary>
```cpp
void fizzbuzz(int count) {
    for (int i{1}; i <= count; ++i) {
        if (i % 15 == 0) std::cout << "fizzbuzz\n";
        else if (i % 3 == 0) std::cout << "fizz\n";
        else if (i % 5 == 0) std::cout << "buzz\n";
        else std::cout << i << '\n';
    }
}
```
</details>

**问题5**  
添加"pop"规则的优化版FizzBuzz：  
<details><summary>答案</summary>
```cpp
void fizzbuzz(int count) {
    for (int i{1}; i <= count; ++i) {
        bool printed{false};
        if (i % 3 == 0) { std::cout << "fizz"; printed = true; }
        if (i % 5 == 0) { std::cout << "buzz"; printed = true; }
        if (i % 7 == 0) { std::cout << "pop"; printed = true; }
        if (!printed) std::cout << i;
        std::cout << '\n';
    }
}
```
</details>

[下一课 8.11 break与continue](Chapter-8/lesson8.11-break-and-continue.md)  
[返回主页](/)  
[上一课 8.9 do while语句](Chapter-8/lesson8.9-do-while-statements.md)