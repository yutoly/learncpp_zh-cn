8.11 — break 与 continue
==========================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2007年6月26日 下午4:22（太平洋夏令时）
2023年9月11日更新

break
----------------
尽管您已在 `switch` 语句（见课程 [8.5 — switch 语句基础](Chapter-8/lesson8.5-switch-statement-basics.md)）中接触过 `break` 语句，但因其同样适用于其他控制流语句，值得更深入探讨。**break 语句（break statement）** 会终止 while 循环、do-while 循环、for 循环或 switch 语句，并跳转至被中断的循环或 switch 之后的下一条语句继续执行。

**在 switch 中使用 break**
在 `switch` 语句中，`break` 通常置于每个分支末尾，表示当前分支结束（防止贯穿至后续分支）：
```cpp
#include <iostream>

void printMath(int x, int y, char ch)
{
    switch (ch)
    {
    case '+':
        std::cout << x << " + " << y << " = " << x + y << '\n';
        break; // 防止贯穿至下一分支
    case '-':
        std::cout << x << " - " << y << " = " << x - y << '\n';
        break; // 防止贯穿至下一分支
    case '*':
        std::cout << x << " * " << y << " = " << x * y << '\n';
        break; // 防止贯穿至下一分支
    case '/':
        std::cout << x << " / " << y << " = " << x / y << '\n';
        break;
    }
}

int main()
{
    printMath(2, 3, '+');
    return 0;
}
```
关于贯穿行为的详细说明及更多示例，请参阅课程 [8.6 — switch 的贯穿与作用域](Chapter-8/lesson8.6-switch-fallthrough-and-scoping.md)。

**在循环中使用 break**
在循环中，`break` 语句可提前终止循环。执行将跳转至循环结束后的下一条语句。例如：
```cpp
#include <iostream>

int main()
{
    int sum{ 0 };

    // 允许用户输入最多10个数字
    for (int count{ 0 }; count < 10; ++count)
    {
        std::cout << "输入要相加的数字（输入0退出）: ";
        int num{};
        std::cin >> num;

        // 用户输入0时退出循环
        if (num == 0)
            break; // 立即退出循环

        // 否则将数字累加到总和
        sum += num;
    }

    // break 后执行将在此继续
    std::cout << "您输入的所有数字之和为: " << sum << '\n';
    return 0;
}
```
此程序允许用户输入最多10个数字，最后显示总和。若用户输入0，break 会提前终止循环（无需输满10个数字）。程序运行示例如下：
```
输入要相加的数字（输入0退出）: 5
输入要相加的数字（输入0退出）: 2
输入要相加的数字（输入0退出）: 1
输入要相加的数字（输入0退出）: 0
您输入的所有数字之和为: 8
```
`break` 也是跳出有意设计的无限循环的常用方法：
```cpp
#include <iostream>

int main()
{
    while (true) // 无限循环
    {
        std::cout << "输入0退出，输入其他整数继续: ";
        int num{};
        std::cin >> num;

        // 用户输入0时退出循环
        if (num == 0)
            break;
    }

    std::cout << "已退出循环!\n";
    return 0;
}
```
程序运行示例：
```
输入0退出，输入其他整数继续: 5
输入0退出，输入其他整数继续: 3
输入0退出，输入其他整数继续: 0
已退出循环!
```

**break 与 return 的区别**
初学者有时难以区分 `break` 和 `return`。`break` 语句终止 switch 或循环，执行跳转至 switch 或循环之后的首条语句。`return` 语句则终止整个包含循环的函数，执行跳转至该函数的调用点。
```cpp
#include <iostream>

int breakOrReturn()
{
    while (true) // 无限循环
    {
        std::cout << "输入 'b' 中断循环或 'r' 返回函数: ";
        char ch{};
        std::cin >> ch;

        if (ch == 'b')
            break; // 执行跳转至循环后的首条语句

        if (ch == 'r')
            return 1; // 函数立即返回调用者（此处为 main()）
    }

    // 中断循环后执行在此继续
    std::cout << "已跳出循环\n";
    return 0;
}

int main()
{
    int returnValue{ breakOrReturn() };
    std::cout << "函数 breakOrReturn 返回值为 " << returnValue << '\n';
    return 0;
}
```
程序两次运行结果：
```
输入 'b' 中断循环或 'r' 返回函数: r
函数 breakOrReturn 返回值为 1
```
```
输入 'b' 中断循环或 'r' 返回函数: b
已跳出循环
函数 breakOrReturn 返回值为 0
```

continue
----------------
**continue 语句（continue statement）** 提供了一种便捷方式，可在不终止整个循环的情况下结束当前迭代。

使用 continue 的示例：
```cpp
#include <iostream>

int main()
{
    for (int count{ 0 }; count < 10; ++count)
    {
        // 若数字能被4整除，跳过本次迭代
        if ((count % 4) == 0)
            continue; // 跳转至下一迭代

        // 若不能整除则继续执行
        std::cout << count << '\n';

        // continue 语句跳转至此位置
    }
    return 0;
}
```
此程序打印0到9中不能被4整除的数字：
```
1
2
3
5
6
7
9
```
`continue` 语句通过将当前执行点跳转至当前循环底部实现功能。对于 for 循环，continue 后仍会执行 for 循环的末尾语句（上例中的 `++count`，因其在循环体结束后执行）。

**在 while 或 do-while 循环中使用 continue 的注意事项**
此类循环通常在循环体内修改条件判断所用的变量值。若 `continue` 语句导致这些代码被跳过，可能引发无限循环！考虑以下程序：
```cpp
#include <iostream>

int main()
{
    int count{ 0 };
    while (count < 10)
    {
        if (count == 5)
            continue; // 跳转至循环体末尾

        std::cout << count << '\n';

        ++count; // count 达到5后此语句永不执行

        // continue 语句跳转至此位置
    }
    return 0;
}
```
本意是打印0到9中除5以外的数字，但实际输出：
```
0
1
2
3
4
```
随后进入无限循环。当 `count` 为 `5` 时，`if` 语句结果为 `true`，`continue` 使执行跳转至循环体底部。`count` 变量未被递增，因此下次迭代时 `count` 仍为 `5`，`if` 条件仍成立，程序持续循环。显然，若存在明确的计数器变量，应使用 `for` 循环而非 `while` 或 `do while` 循环。

关于 break 和 continue 使用的争议
----------------
许多教材告诫读者不要在循环中使用 `break` 和 `continue`，原因有二：一是导致执行流跳转，二是增加逻辑跟踪难度。例如，复杂逻辑中的 `break` 可能被忽略，或其触发条件不明确。然而，明智使用 `break` 和 `continue` 可通过减少嵌套块和复杂循环逻辑提升代码可读性。

例如：
```cpp
#include <iostream>

int main()
{
    int count{ 0 }; // 统计循环迭代次数
    bool keepLooping { true }; // 控制循环是否继续
    while (keepLooping)
    {
        std::cout << "输入 'e' 退出循环，输入其他字符继续: ";
        char ch{};
        std::cin >> ch;

        if (ch == 'e')
            keepLooping = false;
        else
        {
            ++count;
            std::cout << "当前迭代次数: " << count << '\n';
        }
    }
    return 0;
}
```
此程序使用布尔变量控制循环，并在用户不退出时执行嵌套块。

**使用 break 的优化版本：**
```cpp
#include <iostream>

int main()
{
    int count{ 0 }; // 统计循环迭代次数
    while (true) // 循环直至用户终止
    {
        std::cout << "输入 'e' 退出循环，输入其他字符继续: ";
        char ch{};
        std::cin >> ch;

        if (ch == 'e')
            break;

        ++count;
        std::cout << "当前迭代次数: " << count << '\n';
    }
    return 0;
}
```
此版本通过单个 `break` 语句，避免了布尔变量（无需理解其用途和修改点）、`else` 语句和嵌套块。

**continue 的最佳实践**
`continue` 最有效的用法是在 for 循环顶部跳过满足特定条件的迭代，从而避免嵌套块。例如，替代以下写法：
```cpp
#include <iostream>

int main()
{
    for (int count{ 0 }; count < 10; ++count)
    {
        // 若数字不能被4整除...
        if ((count % 4) != 0) // 嵌套块
        {
            std::cout << count << '\n';
        }
    }
    return 0;
}
```
可优化为：
```cpp
#include <iostream>

int main()
{
    for (int count{ 0 }; count < 10; ++count)
    {
        // 若数字能被4整除，跳过本次迭代
        if ((count % 4) == 0)
            continue;

        // 无需嵌套块
        std::cout << count << '\n';
    }
    return 0;
}
```
最小化变量使用和减少嵌套块对代码可理解性的提升，远大于 `break` 或 `continue` 的潜在影响。因此，我们认为明智地使用 `break` 或 `continue` 是可接受的。

> **最佳实践**
> 当 break 和 continue 能简化循环逻辑时使用它们。

关于提前返回的争议
----------------
类似争议也存在于 **return 语句**中。函数中非最后一条语句的 return 称为**提前返回（early return）**。许多程序员认为应避免提前返回。仅在最底部包含单一 return 语句的函数具有简洁性——可假设函数处理参数、执行逻辑后无偏差地返回结果。额外的 return 会复杂化逻辑。

反方观点认为：提前返回允许函数在完成后立即退出，减少冗余逻辑阅读需求并最小化条件嵌套块，从而提升代码可读性。部分开发者采取折中方案：仅在函数顶部使用提前返回进行参数校验（捕获非法参数），之后保持单一返回。

我们的立场是：提前返回利大于弊，但承认实践中存在一定艺术性。

> **最佳实践**
> 当提前返回能简化函数逻辑时使用它们。

[下一课 8.12 — 终止（提前退出程序）](Chapter-8/lesson8.12-halts-exiting-your-program-early.md)
[返回主页](/)  
[上一课 8.10 — for 语句](Chapter-8/lesson8.10-for-statements.md)