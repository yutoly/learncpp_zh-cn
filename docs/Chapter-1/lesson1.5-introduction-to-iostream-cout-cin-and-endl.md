1.5 — 输入/输出流库（iostream）简介：cout、cin与endl  
====================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年1月12日，下午4:53（首次发布于2025年2月5日）  

本章将深入探讨我们在《Hello world!》程序中用于向控制台输出文本的`std::cout`，并学习如何通过用户输入实现交互式程序。  

输入/输出库（io library）  
----------------  

**输入/输出库（io library）**是C++标准库中处理基础输入输出的组成部分。我们将使用该库功能实现键盘输入与控制台输出。*iostream*中的*io*即代表*输入/输出（input/output）*。  

要使用`iostream`库的功能，需在代码文件顶部包含其头文件：  
```cpp
#include <iostream>

// 此处使用iostream功能的代码
```  

std::cout  
----------------  

`iostream`库包含若干预定义变量，其中**std::cout**允许我们将数据发送至控制台输出为文本。*cout*意为“字符输出（character output）”。  

回顾《Hello world》程序：  
```cpp
#include <iostream> // 引入std::cout

int main()
{
    std::cout << "Hello world!"; // 向控制台输出Hello world!
    return 0;
}
```  
本例中，包含`iostream`以获得`std::cout`访问权。在`main`函数内，使用**插入运算符（`<<`）**将文本发送至控制台。  

`std::cout`不仅能输出文本，还可打印数字：  
```cpp
#include <iostream>

int main()
{
    std::cout << 4; // 输出数字4
    return 0;
}
```  
输出结果：  
```
4
```  
亦能输出变量值：  
```cpp
#include <iostream>

int main()
{
    int x{5};        // 定义初始化为5的整型变量x
    std::cout << x;  // 输出x的值（5）
    return 0;
}
```  
输出结果：  
```
5
```  

要单行输出多项内容，可通过多次使用插入运算符串联输出：  
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello" << " world!";  // 两次使用<<运算符
    return 0;
}
```  
输出结果：  
```
Hello world!
```  

**技巧**  
可将`<<`和`>>`运算符想象为传送带，将数据沿箭头方向传输。当内容传至`std::cout`时即被输出。  

混合输出文本与变量值：  
```cpp
#include <iostream>

int main()
{
    int x{5};
    std::cout << "x等于：" << x;  // 混合输出文本与变量
    return 0;
}
```  
输出结果：  
```
x等于：5
```  

**相关内容**  
关于`std::`前缀的详细说明见课程[2.9 — 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)。  

使用std::endl换行  
----------------  

以下程序输出结果如何？  
```cpp
#include <iostream>

int main()
{
    std::cout << "你好！";
    std::cout << "我是Alex。";
    return 0;
}
```  
实际输出：  
```
你好！我是Alex。
```  
多个输出语句不会自动换行。要实现换行需输出**换行符（newline）**，即操作系统特定的控制字符序列。  

使用`std::endl`（"end line"缩写）输出换行：  
```cpp
#include <iostream>

int main()
{
    std::cout << "你好！" << std::endl;  // 光标移至下一行
    std::cout << "我是Alex。" << std::endl;
    return 0;
}
```  
输出结果：  
```
你好！
我是Alex。
```  

**技巧**  
虽然第二个`std::endl`在程序结束时并非必要，但其作用包括：  
1. 表示输出语句完整性（类似英文句号）  
2. 确保后续输出从新行开始  
3. 保持命令行提示符显示在新行首  

**最佳实践**  
完成每行输出后应换行。  

std::cout的缓冲机制  
----------------  

`std::cout`的输出通常不会立即发送至控制台，而是存储在**缓冲区（buffer）**中。周期性地，缓冲区内容会被**刷新（flush）**至目标设备。  

**关键洞察**  
缓冲输出的对立面是**非缓冲输出（unbuffered output）**，后者每次输出请求都直接发送至设备。缓冲区机制通过批量处理显著提升性能。  

std::endl与\n对比  
----------------  

使用`std::endl`效率较低，因其同时执行两项操作：输出换行符与刷新缓冲区。推荐使用`\n`仅输出换行（不强制刷新）：  
```cpp
#include <iostream>

int main()
{
    int x{5};
    std::cout << "x等于：" << x << '\n';  // 单引号（常规）
    std::cout << "确认。" << "\n";       // 双引号（非常规但可用）
    std::cout << "这就是全部了！\n";     // 嵌入双引号文本（常规）
    return 0;
}
```  
输出结果：  
```
x等于：5
确认。
这就是全部了！
```  

**高级阅读**  
`\n`在源码中表现为两个符号，但编译器视其为单个换行符（ASCII 10）。输出时，系统会将其转换为适合OS的换行序列。  

**最佳实践**  
控制台输出优先使用`\n`而非`std::endl`。  

**警告**  
使用反斜杠`\n`而非正斜杠`/n`。错误使用会导致意外输出（如`std::cout << '/n';`可能输出`12142`）。  

std::cin  
----------------  

`std::cin`（"字符输入"）用于读取键盘输入，通过**提取运算符（`>>`）**将输入存入变量：  
```cpp
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    int x{};         // 定义存储输入的变量
    std::cin >> x;   // 从键盘获取数字
    std::cout << "你输入了" << x << '\n';
    return 0;
}
```  
输入`4`时输出：  
```
输入数字：4
你输入了4
```  

**技巧**  
接受输入时无需额外换行，用户按回车键即会换行。  

多值输入示例：  
```cpp
#include <iostream>

int main()
{
    std::cout << "输入两个以空格分隔的数字：";
    int x{}, y{};
    std::cin >> x >> y;  // 获取两个数字
    std::cout << "你输入了" << x << "和" << y << '\n';
    return 0;
}
```  
输入`5 6`时输出：  
```
输入两个以空格分隔的数字：5 6
你输入了5和6
```  

**关键洞察**  
输入值应以空白字符（空格/制表符/换行）分隔。  

std::cin的缓冲机制  
----------------  

输入处理分两阶段：  
1. 输入字符（含回车符`\n`）存入输入缓冲区  
2. 提取运算符从前端取出字符并转换为变量值  

示例程序分析：  
```cpp
#include <iostream>

int main()
{
    std::cout << "输入两个数字：";
    int x{}, y{};
    std::cin >> x;  // 首次提取
    std::cin >> y;  // 二次提取
    std::cout << "你输入了" << x << "和" << y << '\n';
    return 0;
}
```  
运行情况：  
- 输入`4`后回车：`x=4`，等待`y`输入  
- 输入`4 5`：`x=4`，`y`自动获取缓冲区中的`5`  

**关键洞察**  
`std::cin`缓冲机制允许分离输入动作与提取操作，支持单次输入多次提取。  

提取运算符工作原理  
----------------  

提取过程简化步骤：  
1. 若`std::cin`状态异常（如之前提取失败），中止操作  
2. 跳过前导空白字符  
3. 缓冲区为空则等待输入  
4. 提取有效字符直至遇到无效字符或换行符  

结果：  
- 成功：转换值赋给变量  
- 失败：变量赋0（C++11起），后续提取失败直至`std::cin`重置  

未提取字符（含换行符）保留供后续提取。  

**相关内容**  
输入错误处理详见课程[9.5 — std::cin与无效输入处理](Chapter-9/lesson9.5-stdcin-and-handling-invalid-input.md)。  

运算符<<与>>对比  
----------------  

记忆要点：  
- `std::cout`与`std::cin`始终位于运算符左侧  
- `std::cout <<`输出数据（流向控制台）  
- `std::cin >>`输入数据（流向变量）  

测验解析  
----------------  

**问题1**  
分析以下输入对程序的影响：  
a) 输入字母`h` → 输出`0`（提取失败）  
b) 输入`3.2` → 输出`3`（舍弃小数部分）  
c) 输入`-3` → 正常输出  
d) 输入`Hello` → 输出`0`（无效字符）  
e) 超大数据 → 输出系统最大整数值  
f) `123abc` → 输出`123`（剩余字符保留）  
g) `abc123` → 输出`0`（首字符无效）  
h) `   +5` → 输出`5`（跳过空格）  
i) `5b6` → 输出`5`（`b`无效）  

**问题2**  
实现三数输入输出程序：  
```cpp
#include <iostream>

// 获取用户输入的三个数字并格式化输出
int main()
{
    std::cout << "输入三个数字：";
    int x{}, y{}, z{};
    std::cin >> x >> y >> z;
    std::cout << "你输入了" << x << "、" << y << "和" << z << "。\n";
    return 0;
}
```  

[下一课 1.6 — 未初始化变量与未定义行为](Chapter-1/lesson1.6-uninitialized-variables-and-undefined-behavior.md)  
[返回主页](/)  
[上一课 1.4 — 变量赋值与初始化](Chapter-1/lesson1.4-variable-assignment-and-initialization.md)