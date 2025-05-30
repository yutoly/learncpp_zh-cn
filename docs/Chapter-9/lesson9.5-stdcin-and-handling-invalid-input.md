9.5 — std::cin与无效输入处理
==========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月29日（首次发布于2016年4月21日）

大多数具有用户界面的程序都需要处理用户输入。在您编写的程序中，通常使用std::cin获取用户输入的文本。由于文本输入的自由格式特性（用户可输入任何内容），很容易出现非预期输入。

编写程序时，应始终考虑用户可能（有意或无意）误用的情况。能够妥善处理异常情况的程序称为健壮（robust）程序。本节将重点讨论用户通过std::cin输入无效文本的情形，并展示多种处理方法。

运算符>>的工作机制回顾
----------------

在讨论std::cin和operator>>可能产生的错误前，先回顾其工作原理（详见课程[1.5 — iostream简介：cout、cin与endl](introduction-to-iostream-cout-cin-and-endl/#extraction)）：

1. 首先丢弃输入缓冲区中的前导空白字符（空格、制表符、换行符）
2. 若缓冲区为空，operator>>将等待用户输入（再次丢弃前导空白）
3. 提取连续字符直到遇到换行符或与目标变量类型不符的字符

提取结果：
- 成功提取：字符转换为目标类型并赋值给变量
- 提取失败（C++11起）：变量赋值为0，后续提取直接失败（直至调用std::cin.clear）

输入验证（input validation）
----------------

输入验证指检查用户输入是否符合程序预期的过程，主要有三种方式：

1. **即时验证**：通过GUI或高级文本界面逐字符验证（std::cin不支持）
2. **字符串后处理**：先读取完整字符串再验证和转换（较少使用）
3. **提取后处理**：借助std::cin自动转换，处理错误情况（本节重点）

示例程序分析
----------------

以下计算器程序未作错误处理：

```cpp
#include <iostream>

double getDouble()
{
    std::cout << "输入小数：";
    double x{};
    std::cin >> x;
    return x;
}

char getOperator()
{
    std::cout << "输入运算符（+、-、*、/）：";
    char op{};
    std::cin >> op;
    return op;
}

// ... printResult和main函数 ...
```

当用户输入无效数据时可能引发的问题：

**错误类型1：有效提取但输入无意义**  
用户输入无效运算符（如'k'）时，程序无法正确处理，导致错误输出。

解决方案：在getOperator()中添加输入验证：

```cpp
char getOperator()
{
    while (true) {
        // ... 输入代码 ...
        switch (operation) {
            case '+': case '-': case '*': case '/': return operation;
            default: std::cout << "无效输入，请重试\n";
        }
    }
}
```

**错误类型2：有效提取但存在额外输入**  
用户输入"5*7"时，第一个提取操作获取5，剩余字符导致后续输入混乱。

解决方案：添加行清理函数：

```cpp
#include <limits>
void ignoreLine() {
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// 在getDouble()中调用：
ignoreLine();
```

**错误类型3：提取失败**  
用户输入非数字字符（如'a'）导致提取失败，程序陷入死循环。

解决方案：检测并清除错误状态：

```cpp
double getDouble() {
    while (true) {
        // ... 输入代码 ...
        if (!std::cin) {
            std::cin.clear();
            ignoreLine();
            continue;
        }
        // ...
    }
}
```

**错误类型4：数值溢出**  
用户输入超出变量范围的数值（如将40000存入int16_t变量），导致赋值32767。

处理方式：与提取失败相同，通过清除错误状态处理。

完整解决方案整合
----------------

最终计算器程序整合了所有错误处理：

```cpp
#include <cstdlib>
#include <iostream>
#include <limits>

void ignoreLine() { /* 同上 */ }

bool clearFailedExtraction() {
    if (!std::cin) {
        if (std::cin.eof()) std::exit(0);
        std::cin.clear();
        ignoreLine();
        return true;
    }
    return false;
}

double getDouble() {
    while (true) {
        // ... 输入代码 ...
        if (clearFailedExtraction()) {
            std::cout << "无效输入，请重试\n";
            continue;
        }
        ignoreLine();
        return x;
    }
}

// ... 其他函数 ...
```

关键处理流程：
1. 使用clearFailedExtraction()处理EOF和提取失败
2. 通过ignoreLine()清理缓冲区残留
3. 循环验证直至获得有效输入

总结
----------------

编写程序时需考虑以下输入问题：
- 提取是否可能失败
- 是否存在额外输入
- 输入是否有意义
- 数值是否可能溢出

建议实践：
- 使用ignoreLine()清理缓冲区
- 通过clearFailedExtraction()处理错误
- 使用循环强制用户重新输入

后续课程可能简化输入验证以突出重点，但实际开发中应始终保证程序健壮性。

[下一课 9.6 — assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md)  
[返回主页](/)  
[上一课 9.4 — 错误检测与处理](Chapter-9/lesson9.4-detecting-and-handling-errors.md)