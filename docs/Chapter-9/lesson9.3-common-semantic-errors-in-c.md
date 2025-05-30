9.3 — C++中的常见语义错误  
======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看Alex的所有文章")  

2024年11月10日（首次发布于2020年12月21日）  

在课程[3.1 — 语法错误与语义错误](Chapter-3/lesson3.1-syntax-and-semantic-errors.md)中，我们介绍了**语法错误（syntax errors）**——当代码不符合C++语法规则时发生的错误。编译器会提示此类错误，因此易于捕获且通常易于修复。  

我们还介绍了**语义错误（semantic errors）**——当代码行为与预期不符时发生的错误。编译器通常无法捕获语义错误（尽管某些智能编译器可能生成警告）。  

语义错误可能导致与**未定义行为（undefined behavior）**相似的症状：程序输出错误结果、行为异常、破坏程序数据、导致程序崩溃——也可能毫无影响。  

编写程序时难免产生语义错误。通过使用程序可发现部分错误：例如编写迷宫游戏时，角色若可穿墙而过即属此类。测试程序（[9.1 — 代码测试简介](Chapter-9/lesson9.1-introduction-to-testing-your-code.md)）也有助于暴露语义错误。  

但另一有效方法是了解最常见的语义错误类型，从而在这些关键处投入更多精力确保正确性。  

本节将涵盖C++中最常见的语义错误类型（多数与流程控制相关）。  

条件逻辑错误  
----------------  

最常见的语义错误类型之一是条件逻辑错误。**条件逻辑错误（conditional logic error）**指程序员错误编写条件语句或循环条件的逻辑。示例如下：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入整数: ";
    int x{};
    std::cin >> x;

    if (x >= 5) // 错误：应使用>而非>=
        std::cout << x << " 大于 5\n";

    return 0;
}
```  

程序运行结果如下（展示条件逻辑错误）：  

```
输入整数: 5
5 大于 5
```  

当用户输入`5`时，条件表达式`x >= 5`求值为`true`，故执行相关语句。  

以下为for循环的类似案例：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入整数: ";
    int x{};
    std::cin >> x;

    // 错误：应使用<而非>
    for (int count{ 1 }; count > x; ++count)
    {
        std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  

此程序本应输出1到用户输入间的所有数字，但实际运行结果为：  

```
输入整数: 5
（无输出）
```  

这是因为for循环入口处`count > x`为`false`，导致循环完全未执行。  

无限循环  
----------------  

在课程[8.8 — 循环与while语句简介](Chapter-8/lesson8.8-introduction-to-loops-and-while-statements.md)中，我们介绍了无限循环并展示此例：  

```cpp
#include <iostream>
 
int main()
{
    int count{ 1 };
    while (count <= 10) // 此条件永不为假
    {
        std::cout << count << ' '; // 该行将重复执行
    }
 
    std::cout << '\n'; // 此行永不执行
    return 0; // 此行永不执行
}
```  

此例忘记递增`count`，导致循环条件永不为假，程序持续输出：  

```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1...
```  

直到用户终止程序。  

以下是教师钟爱的测验题案例。下列代码有何错误？  

```cpp
#include <iostream>

int main()
{
    for (unsigned int count{ 5 }; count >= 0; --count)
    {
        if (count == 0)
            std::cout << "发射! ";
        else
          std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  

程序预期输出`5 4 3 2 1 发射!`，但实际输出：  

```
5 4 3 2 1 发射! 4294967295 4294967294 4294967293 4294967292 4294967291...
```  

并持续递减。由于无符号整型的`count >= 0`永不为`false`，程序永不终止。  

差一错误  
----------------  

**差一错误（off-by-one）**指循环执行次数多一次或少一次的错误。课程[8.10 — for语句](Chapter-8/lesson8.10-for-statements.md)中的示例如下：  

```cpp
#include <iostream>

int main()
{
    for (int count{ 1 }; count < 5; ++count)
    {
        std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
```  

本意是输出`1 2 3 4 5`，但因误用关系运算符（`<`代替`<=`），循环少执行一次，仅输出`1 2 3 4`。  

运算符优先级错误  
----------------  

课程[6.8 — 逻辑运算符](Chapter-6/lesson6.8-logical-operators.md)中的程序存在运算符优先级错误：  

```cpp
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 7 };

    if (!x > y) // 错误：运算符优先级问题
        std::cout << x << " 不大于 " << y << '\n';
    else
        std::cout << x << " 大于 " << y << '\n';

    return 0;
}
```  

由于**逻辑非（logical NOT）**优先级高于**关系运算符（operator>）**，条件被解析为`(!x) > y`，不符合程序原意。  

因此程序输出：  

```
5 大于 7
```  

混合使用**逻辑或（Logical OR）**与**逻辑与（Logical AND）**时也可能发生此问题（逻辑与优先级高于逻辑或）。建议使用显式括号避免此类错误。  

浮点类型精度问题  
----------------  

以下浮点变量精度不足导致存储截断：  

```cpp
#include <iostream>

int main()
{
    float f{ 0.123456789f };
    std::cout << f << '\n';

    return 0;
}
```  

因精度限制，数字被轻微舍入：  

```
0.123457
```  

在课程[6.7 — 关系运算符与浮点数比较](Chapter-6/lesson6.7-relational-operators-and-floating-point-comparisons.md)中，我们讨论过浮点数使用`operator==`和`operator!=`时因微小舍入误差可能导致问题（以及解决方案）。示例如下：  

```cpp
#include <iostream>

int main()
{
    double d{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 }; // 预期总和为1.0

    if (d == 1.0)
        std::cout << "相等\n";
    else
        std::cout << "不相等\n";

    return 0;
}
```  

程序输出：  

```
不相等
```  

浮点数运算越多，累积的舍入误差越大。  

整数除法  
----------------  

下例本意进行浮点除法，但因操作数均为整数而执行整数除法：  

```cpp
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 3 };

    std::cout << x << " 除以 " << y << " 结果为: " << x / y << '\n'; // 整数除法

    return 0;
}
```  

输出：  

```
5 除以 3 结果为: 1
```  

课程[6.2 — 算术运算符](Chapter-6/lesson6.2-arithmetic-operators.md)展示了使用**static_cast**将整型操作数转为浮点数以执行浮点除法的方法。  

意外的空语句  
----------------  

课程[8.3 — if语句常见问题](Chapter-8/lesson8.3-common-if-statement-problems.md)介绍了**空语句（null statements）**——不执行任何操作的语句。  

以下程序本应在获得用户授权后执行操作：  

```cpp
#include <iostream>

void blowUpWorld()
{
    std::cout << "轰！\n";
} 

int main()
{
    std::cout << "要再次毁灭世界吗? (y/n): ";
    char c{};
    std::cin >> c;

    if (c == 'y');     // 意外的空语句
        blowUpWorld(); // 此语句将始终执行（不属于if语句体）
 
    return 0;
}
```  

但因意外的空语句，`blowUpWorld()`函数始终执行：  

```
要再次毁灭世界吗? (y/n): n
轰！
```  

未使用必需的复合语句  
----------------  

上述程序的另一变体（始终毁灭世界）：  

```cpp
#include <iostream>

void blowUpWorld()
{
    std::cout << "轰！\n";
} 

int main()
{
    std::cout << "要再次毁灭世界吗? (y/n): ";
    char c{};
    std::cin >> c;

    if (c == 'y')
        std::cout << "正在执行...\n";
        blowUpWorld(); // 始终执行！应包含在复合语句内
 
    return 0;
}
```  

程序输出：  

```
要再次毁灭世界吗? (y/n): n
轰！
```  

**悬垂else（dangling else）**（见课程[8.3](Chapter-8/lesson8.3-common-if-statement-problems.md)）也属此类。  

条件语句中误用赋值运算符  
----------------  

因**赋值运算符（=）**与**相等运算符（==）**相似，可能误用赋值替代相等判断：  

```cpp
#include <iostream>

void blowUpWorld()
{
    std::cout << "轰！\n";
} 

int main()
{
    std::cout << "要再次毁灭世界吗? (y/n): ";
    char c{};
    std::cin >> c;

    if (c = 'y') // 误用赋值运算符替代相等运算符
        blowUpWorld();
 
    return 0;
}
```  

程序输出：  

```
要再次毁灭世界吗? (y/n): n
轰！
```  

赋值运算符返回其左操作数。`c = 'y'`先执行，将`y`赋给`c`并返回`c`。随后`if (c)`被求值。因`c`非零，隐式转为**布尔值（bool）**`true`，故执行if语句。  

由于条件内赋值几乎非本意，现代编译器常对此发出警告。但若不重视警告处理，此类警告易被忽略。  

调用函数时遗漏函数调用运算符  
----------------  

```cpp
#include <iostream>

int getValue()
{
    return 5;
}

int main()
{
    std::cout << getValue << '\n'; // 遗漏函数调用运算符()

    return 0;
}
```  

预期输出`5`，但实际可能输出`1`（某些编译器输出十六进制内存地址）。  

未使用函数调用运算符`getValue()`（本应调用函数并返回`int`值），而是直接使用`getValue`。多数情况下，这将返回被转为`bool`值`true`的值。  

上例中，输出的`bool`值`true`被打印为`1`。  

> **进阶阅读**  
> 未调用函数而直接使用函数名通常产生指向该函数的**函数指针（function pointer）**。此类指针隐式转为`bool`值。因指针地址永不为`0`，故`bool`值恒为`true`。  
>  
> 函数指针详见课程[20.1 — 函数指针](Chapter-20/lesson20.1-function-pointers.md)。  

其他常见错误  
----------------  

上述示例代表了C++新手常见语义错误类型，但仍有更多可能。读者若有其他常见陷阱，欢迎评论区补充。  

[下一课 9.4 错误检测与处理](Chapter-9/lesson9.4-detecting-and-handling-errors.md)  
[返回主页](/)  
[上一课 9.2 代码覆盖率](Chapter-9/lesson9.2-code-coverage.md)