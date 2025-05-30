27.1 — 异常处理的必要性  
===============================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年5月23日（首次发布于2008年10月4日）  

在前文[错误处理](712-handling-errors-assert-cerr-exit-and-exceptions/)课程中，我们讨论了使用assert()、std::cerr和exit()处理错误的方法。现在我们将探讨之前暂缓的一个主题：异常（exceptions）。  

**返回码的缺陷**  

编写可复用代码时，错误处理是必要环节。最常见的错误处理方式之一是使用返回码（return codes）。例如：  

```cpp
#include <string_view>

int findFirstChar(std::string_view string, char ch)
{
    // 遍历字符串中的每个字符
    for (std::size_t index{ 0 }; index < string.length(); ++index)
        // 若字符匹配ch，返回其索引
        if (string[index] == ch)
            return index;

    // 未找到匹配字符时返回-1
    return -1;
}
```  

该函数返回字符串中首个匹配ch字符的索引。若未找到，函数返回-1作为标识。  

此方法的主要优点是简单直接。但在复杂场景中使用返回码会暴露以下缺陷：  

首先，返回值可能含义模糊——当函数返回-1时，是表示错误还是有效结果？若不深入查看函数实现或查阅文档，往往难以判断。  

其次，函数只能返回单个值。当需要同时返回函数结果和可能的错误码时如何处理？考虑以下函数：  

```cpp
double divide(int x, int y)
{
    return static_cast<double>(x)/y;
}
```  

此函数急需错误处理，因为当y参数为0时会导致崩溃。但它同时需要返回x/y的结果。如何兼顾两者？常见解决方案是将结果或错误码通过引用参数传回，但这会导致代码冗长且使用不便。例如：  

```cpp
#include <iostream>

double divide(int x, int y, bool& outSuccess)
{
    if (y == 0)
    {
        outSuccess = false;
        return 0.0;
    }

    outSuccess = true;
    return static_cast<double>(x)/y;
}

int main()
{
    bool success {}; // 必须传入布尔值以检测调用是否成功
    double result { divide(5, 3, success) };

    if (!success) // 使用结果前需检查状态
        std::cerr << "发生错误" << std::endl;
    else
        std::cout << "结果是 " << result << '\n';
}
```  

第三，在可能连续发生错误的代码段中，需要频繁检查错误码。考虑以下解析配置文件的代码片段：  

```cpp
    std::ifstream setupIni { "setup.ini" }; // 打开setup.ini文件
    // 若文件无法打开（如缺失）返回错误枚举
    if (!setupIni)
        return ERROR_OPENING_FILE;

    // 从文件中读取多个值
    if (!readIntegerFromFile(setupIni, m_firstParameter)) // 尝试读取整型
        return ERROR_READING_VALUE; // 返回表示读取失败的枚举值

    if (!readDoubleFromFile(setupIni, m_secondParameter)) // 尝试读取双精度浮点型
        return ERROR_READING_VALUE;

    if (!readFloatFromFile(setupIni, m_thirdParameter)) // 尝试读取浮点型
        return ERROR_READING_VALUE;
```  

即使不理解文件操作细节，仍可注意到每次调用都需要错误检查并返回调用者。若需处理二十个不同类型参数，将重复二十次错误检查和返回ERROR_READING_VALUE！这些错误检查严重干扰了代码核心逻辑的可读性。  

第四，返回码与构造函数（constructors）配合不佳。若对象构造过程中发生严重错误怎么办？构造函数没有返回类型来传递状态标识，通过引用参数传回既繁琐又需显式检查。即使实现，仍需处理已创建的对象。  

最后，当错误码返回给调用者时，调用者可能不具备处理条件。若调用者不愿处理错误，要么忽略（导致错误丢失），要么将错误抛给上层调用者。这会产生与前述类似的问题。  

综上，返回码的核心问题在于错误处理代码与正常控制流紧密耦合。这不仅限制代码结构，也影响错误的合理处理方式。  

**异常机制**  

异常处理（exception handling）提供了一种机制，将错误或异常情况的处理与常规控制流解耦。这为不同场景下的错误处理提供了更大自由度，缓解了返回码导致的结构混乱问题。  

下一课我们将探讨C++中的异常处理机制。  

[下一课 27.2 基本异常处理](Chapter-27/lesson27.2-basic-exception-handling.md)  
[返回主页](/)    
[上一课 26.x 第26章总结与测验](Chapter-26/lesson26.x-chapter-26-summary-and-quiz.md)