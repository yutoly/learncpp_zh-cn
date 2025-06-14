9.4 — 错误检测与处理
====================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月17日（首次发布于2007年10月22日）  

在课程[9.3 — C++常见语义错误](Chapter-9/lesson9.3-common-semantic-errors-in-c.md)中，我们讨论了新手程序员常遇到的各种C++语义错误。如果错误源于语言特性的误用或逻辑错误，通常只需修正即可。但程序中的大多数错误并非来自语言特性的误用，而是由于程序员的错误假设和/或缺乏适当的错误检测与处理机制。  

例如，在查找学生成绩的函数中，您可能假设：  
* 被查询的学生必定存在  
* 所有学生姓名唯一  
* 课程采用字母评分制（而非通过/不通过）  

若这些假设不成立会怎样？如果程序员未预见这些情况，当它们发生时程序可能运行异常或崩溃（通常发生在函数编写完成后的某个时刻）。  

假设性错误通常出现在三个关键位置：  
1. 函数返回时，程序员可能错误假设被调用函数执行成功  
2. 程序接收输入（用户或文件）时，可能错误假设输入格式正确且语义有效  
3. 调用函数时，可能错误假设参数语义有效  

许多新手程序员只测试**理想路径**（无错误情况）。但您还应规划并测试**异常路径**（可能出错的情况）。在课程[3.10 — 在问题发生前发现问题](Chapter-3/lesson3.10-finding-issues-before-they-become-problems.md)中，我们定义**防御式编程**为：预见软件可能被终端用户或开发者误用的所有方式。预见（或发现）误用后，下一步就是处理它。  

本节讨论函数内部的错误处理策略（出错时的应对措施），后续课程将探讨用户输入验证及辅助文档化和验证假设的工具。  

函数中的错误处理  
----------------  

函数可能因各种原因失败：调用者传入无效参数值，或函数体内部操作失败。例如，打开文件的函数在文件不存在时会失败。  

此时您有多种选择，没有"最佳"错误处理方式，具体取决于问题性质和是否可修复。  

四种通用策略：  
* 在函数内部处理错误  
* 将错误传回调用者处理  
* 终止程序  
* 抛出异常  

### 函数内部处理错误  
若可能，最佳策略是在检测到错误的函数内部恢复，这样错误可被控制并修正，不影响外部代码。有两种选择：重试直到成功，或取消当前操作。  

若错误源于程序外部因素（如网络连接断开），程序可循环重试。例如显示警告并定期检查网络恢复。若用户输入无效，可提示重新输入直至成功。下节课将演示处理无效输入和重试循环的示例。  

另一种策略是忽略错误/取消操作。例如：  
```cpp
// y=0时静默失败
void printIntDivision(int x, int y)
{
    if (y != 0)
        std::cout << x / y;
}
```
此例中若y无效，直接忽略除法操作请求。主要问题在于调用者/用户无法获知错误。此时输出错误信息更有效：  
```cpp
void printIntDivision(int x, int y)
{
    if (y != 0)
        std::cout << x / y;
    else
        std::cout << "错误：无法除以零\n";
}
```
但若调用者期待返回值或副作用，仅忽略错误可能不可行。  

### 将错误传回调用者  
许多情况下，错误无法在检测函数内合理处理。例如：  
```cpp
int doIntDivision(int x, int y)
{
    return x / y;
}
```
若y为0如何处理？必须返回值，因此最佳选择是将错误传回调用者处理。  

如何实现？  
* `void`返回类型函数可改为返回`bool`表示成功状态  
例如原函数：  
```cpp
void printIntDivision(int x, int y)
{
    if (y != 0)
        std::cout << x / y;
    else
        std::cout << "错误：无法除以零\n";
}
```
可改为：  
```cpp
bool printIntDivision(int x, int y)
{
    if (y == 0)
    {
        std::cout << "错误：无法除以零\n";
        return false;
    }
    
    std::cout << x / y;
    return true;
}
```
调用者通过返回值判断函数是否失败。  

对于返回正常值的函数，若返回值范围未完全使用，可用特定**哨兵值（sentinel value）**表示错误。例如：  
```cpp
// 返回1/x的倒数，x=0时返回0.0
constexpr double error_no_reciprocal { 0.0 }; // 可置于命名空间

double reciprocal(double x)
{
    if (x == 0.0)
       return error_no_reciprocal;

    return 1.0 / x;
}
```
此处`0.0`作为哨兵值表示失败。调用者检查返回值是否等于哨兵值即可判断错误。  

但若返回值范围可能包含所有合法值，使用哨兵值将产生歧义。此时应使用`std::optional`或`std::expected`。相关讨论见课程[12.15 — std::optional](Chapter-12/lesson12.15-stdoptional.md)。  

### 致命错误  
当错误严重到程序无法继续运行时（**不可恢复错误**或**致命错误**），最佳选择是终止程序。若代码在`main()`或直接调用的函数中，让`main()`返回非零状态码即可。若在深层嵌套函数中，使用`std::exit()`等终止语句更便捷。例如：  
```cpp
double doIntDivision(int x, int y)
{
    if (y == 0)
    {
        std::cout << "错误：无法除以零\n";
        std::exit(1);
    }
    return x / y;
}
```

### 异常  
由于通过返回值传递错误复杂且易导致不一致，C++提供了异常机制。错误发生时抛出异常，若当前函数未捕获，则逐级上传至调用栈。若最终未被捕获，程序终止。异常处理详见本教程[第27章](https://www.learncpp.com#Chapter27)。  

`std::cout` vs `std::cerr` vs 日志  
----------------  

在课程[3.4 — 基础调试技巧](Chapter-3/lesson3.4-basic-debugging-tactics.md)中介绍了`std::cerr`。何时使用它们或日志文件？  

默认情况下，`std::cout`和`std::cerr`都输出到控制台。但现代操作系统支持重定向输出流至文件。  

应用类型分为：  
* **交互式应用程序**：用户持续交互（如游戏、音乐应用）  
* **非交互式应用程序**：  
  - **工具**：执行特定任务后终止（如grep命令）  
  - **服务**：后台持续运行（如病毒扫描）  

使用建议：  
* 对交互式程序：  
  - `std::cout`：面向用户的常规文本  
  - `std::cerr`或日志文件：诊断信息（技术警告、状态更新等）  
* 对非交互式程序：  
  - `std::cerr`：仅错误输出（便于分离处理）  
* 事务型应用：日志文件记录事件（处理文件、进度、时间戳等）  

[下一课 9.5 — std::cin与处理无效输入](Chapter-9/lesson9.5-stdcin-and-handling-invalid-input.md)  
[返回主页](/)  
[上一课 9.3 — C++常见语义错误](Chapter-9/lesson9.3-common-semantic-errors-in-c.md)