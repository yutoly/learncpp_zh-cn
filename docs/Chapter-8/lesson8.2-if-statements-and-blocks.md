8.2 — if语句（if statements）与语句块（blocks）
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月21日上午10:01（首次发布）  
2025年3月5日（修订）

 

我们将要讨论的第一类控制流语句是条件语句（conditional statement）。**条件语句（conditional statement）**是用于指定是否执行关联语句的语句。


C++支持两种基本条件结构：`if语句（if statements）`（在课程[4.10 — if语句简介](Chapter-4/lesson4.10-introduction-to-if-statements.md)中已初步介绍）和`switch语句（switch statements）`（后续课程将涉及）。


if语句快速回顾
----------------

C++中最基本的条件语句是`if语句（if statement）`，其基本形式如下：



```
if (条件)
    真值语句;
```

或带可选`else语句（else statement）`：



```
if (条件)
    真值语句;
else
    假值语句;
```

若`条件`评估为`true`，则执行`真值语句`；若评估为`false`且存在`else语句`，则执行`假值语句`。


 
以下示例程序演示带`else语句`的`if语句`：



```
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    int x{};
    std::cin >> x;

    if (x > 10)
        std::cout << x << "大于10\n";
    else
        std::cout << x << "不大于10\n";

    return 0;
}
```

程序运行示例如下：



```
输入数字：15
15大于10

```


```
输入数字：4
4不大于10

```

多条件语句的if/else
----------------

新手常犯以下错误：



```
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "输入身高（厘米）：";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "身高符合要求\n";
    else
        std::cout << "身高不足\n";
        std::cout << "很遗憾！\n"; // 注意此行

    return 0;
}
```

运行示例如下：


 

```
输入身高（厘米）：180
身高符合要求
很遗憾！

```

问题根源在于`真值语句`和`假值语句`只能包含单个语句。缩进格式误导了代码逻辑——实际等效于：



```
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "输入身高（厘米）：";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "身高符合要求\n";
    else
        std::cout << "身高不足\n";

    std::cout << "很遗憾！\n"; // 注意此行

    return 0;
}
```

显然"很遗憾！"会始终执行。


如需执行多语句，应使用复合语句（语句块（block））：



```
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "输入身高（厘米）：";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "身高符合要求\n";
    else
    { // 此处添加语句块
        std::cout << "身高不足\n";
        std::cout << "很遗憾！\n";
    }

    return 0;
}
```

此时程序运行正常：



```
输入身高（厘米）：180
身高符合要求

```


```
输入身高（厘米）：130
身高不足
很遗憾！

```

隐式语句块
----------------

若未在`if语句`或`else语句`中显式声明语句块（block），编译器将隐式生成。因此：


 

```
if (条件)
    真值语句;
else
    假值语句;
```

实际等效于：



```
if (条件)
{
    真值语句;
}
else
{
    假值语句;
}
```

多数情况下无影响，但新手可能尝试在隐式块中定义变量：



```
#include <iostream>

int main()
{
    if (true)
        int x{ 5 };
    else
        int x{ 6 };

    std::cout << x << '\n';

    return 0;
}
```

此代码将编译失败，因为等效于：



```
#include <iostream>

int main()
{
    if (true)
    {
        int x{ 5 };
    } // x在此销毁
    else
    {
        int x{ 6 };
    } // x在此销毁

    std::cout << x << '\n'; // x已超出作用域

    return 0;
}
```

变量`x`具有块作用域（block scope），在块外无法访问。


单语句是否使用语句块
----------------

编程界对于单语句是否应使用语句块存在争议。


支持使用语句块的理由：

1. 避免意外添加看似有条件执行实则无条件的语句。例如：



```
if (年龄 >= 最低饮酒年龄)
    购买啤酒();
```

若匆忙添加新功能：



```
if (年龄 >= 最低饮酒年龄)
    购买啤酒();
    赌博(); // 始终执行
```

导致未成年人可赌博。


2. 调试更困难。考虑：



```
if (年龄 >= 最低饮酒年龄)
    添加啤酒到购物车(); // 有条件执行

结账(); // 始终执行
```

若注释掉函数：


 

```
if (年龄 >= 最低饮酒年龄)
//    添加啤酒到购物车();

结账(); // 变为有条件执行
```

3. C++23引入的`if constexpr`要求使用语句块，保持语法一致性。


反对使用语句块的主要理由是垂直间距影响代码紧凑性。


行业趋势更倾向使用语句块，但非绝对。


最佳实践
----------------

**建议**  
初学阶段建议为`if`/`else`的单语句添加语句块。经验丰富的开发者可能选择紧凑格式。


折中方案是将单语句与条件写在同一行：


 

```
if (年龄 >= 最低饮酒年龄) 购买啤酒();
else std::cout << "禁止饮酒\n";
```

此方式避免前述问题，但可能影响调试：

* 条件与语句同行时，难以单独设置断点
* 调试时难以区分是否执行了语句


if-else与if-if的选择
----------------

新手常困惑何时使用if-else链或连续if语句：

* 使用if-else链时，仅执行首个满足条件的代码
* 使用连续if时，执行所有满足条件的代码


示例程序：


 

```
#include <iostream>

void ifelse(bool a, bool b, bool c)
{
    if (a)      // 始终评估
        std::cout << "a";
    else if (b) // 仅当a为false时评估
        std::cout << "b";
    else if (c) // 仅当b为false时评估
        std::cout << "c";
    std::cout << '\n';
}

void ifif(bool a, bool b, bool c)
{
    if (a) // 始终评估
        std::cout << "a";
    if (b) // 始终评估
        std::cout << "b";
    if (c) // 始终评估
        std::cout << "c";
    std::cout << '\n';
}

int main()
{
    ifelse(false, true, true); // 输出"b"
    ifif(false, true, true);   // 输出"bc"

    return 0;
}
```

当所有关联语句都返回值时，可省略else：



```
char 获取首个匹配字符(bool a, bool b, bool c)
{
    if (a)
        return 'a';
    if (b)
        return 'b';
    if (c)
        return 'c';

    return 0;
}
```

此写法与带else的版本等效，但更简洁。


关键洞见
----------------

**核心原则**  
当所有关联语句都返回时，可省略else关键字，因为其不再提供额外价值。


下节课将继续探讨if语句的常见问题。


[下一课 8.3 — if语句的常见问题](Chapter-8/lesson8.3-common-if-statement-problems.md)  
[返回主页](/)  
[上一课 8.1 — 控制流简介](Chapter-8/lesson8.1-control-flow-introduction.md)