8.3 — 常见if语句问题  
===================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月29日（首次发布于2020年12月21日）  

本课程是[8.2 — if语句与代码块](Chapter-8/lesson8.2-if-statements-and-blocks.md)的延续。我们将探讨使用if语句时常见的若干问题。  

嵌套if语句与悬垂else问题  
----------------  

if语句可以嵌套在其他if语句内部：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    int x{};
    std::cin >> x;

    if (x >= 0) // 外层if语句
        // 这种嵌套方式不符合良好代码规范
        if (x <= 20) // 内层if语句
            std::cout << x << " 在0到20之间\n";

    return 0;
}
```  

观察以下程序：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    int x{};
    std::cin >> x;

    if (x >= 0) // 外层if语句
        // 这种嵌套方式不符合良好代码规范
        if (x <= 20) // 内层if语句
            std::cout << x << " 在0到20之间\n";

    // 这个else属于哪个if？
    else
        std::cout << x << " 是负数\n";

    return 0;
}
```  

上述代码引发了称为**悬垂else（dangling else）**的语义歧义问题。该else语句究竟匹配外层还是内层if语句？  

根据C++标准，else语句始终与同一代码块内最近未匹配的if语句配对。因此上例中的else实际匹配内层if语句，等效于：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    int x{};
    std::cin >> x;

    if (x >= 0) // 外层if语句
    {
        if (x <= 20) // 内层if语句
            std::cout << x << " 在0到20之间\n";
        else // 匹配内层if语句
            std::cout << x << " 是负数\n";
    }

    return 0;
}
```  

这将导致程序输出错误结果：  

```
输入数字：21
21是负数
```  

为避免嵌套if语句时的歧义，建议显式使用代码块包裹内层if语句。这样可明确else语句的归属：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    int x{};
    std::cin >> x;

    if (x >= 0)
    {
        if (x <= 20)
            std::cout << x << " 在0到20之间\n";
        else // 匹配内层if语句
            std::cout << x << " 大于20\n";
    }
    else // 匹配外层if语句
        std::cout << x << " 是负数\n";

    return 0;
}
```  

扁平化嵌套if语句  
----------------  

通过逻辑重构或使用逻辑运算符（详见课程[6.8 — 逻辑运算符](Chapter-6/lesson6.8-logical-operators.md)），可有效减少嵌套层次。扁平化的代码结构更不易出错。  

将上例改写为：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入数字：";
    int x{};
    std::cin >> x;

    if (x < 0)
        std::cout << x << " 是负数\n";
    else if (x <= 20) // 仅当x >=0时执行
        std::cout << x << " 在0到20之间\n";
    else // 仅当x >20时执行
        std::cout << x << " 大于20\n";

    return 0;
}
```  

另一个使用逻辑运算符合并条件的示例：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入整数：";
    int x{};
    std::cin >> x;

    std::cout << "输入另一个整数：";
    int y{};
    std::cin >> y;

    if (x > 0 && y > 0) // &&表示逻辑与
        std::cout << "两数均为正\n";
    else if (x > 0 || y > 0) // ||表示逻辑或
        std::cout << "至少一数为正\n";
    else
        std::cout << "两数均非正\n";

    return 0;
}
```  

空语句  
----------------  

**空语句（null statement）**是仅包含分号的表达式语句：  

```cpp
if (x > 10)
    ; // 空语句
```  

空语句不执行任何操作。通常用于语法要求存在语句但实际无需操作的场景。为提高可读性，空语句应独占一行。后续讲解循环时会有相关示例。  

在if语句中误用空语句可能引发问题。观察以下代码段：  

```cpp
if (nuclearCodesActivated()); // 注意行尾分号
    blowUpTheWorld();
```  

程序员误在if语句末尾添加分号（常见错误），编译器将代码解释为：  

```cpp
if (nuclearCodesActivated())
    ; // 分号作为空语句
blowUpTheWorld(); // 此行始终执行！
```  

> **警告**  
> 避免在if语句后误加分号，否则条件代码将无条件执行（即使位于代码块中）。  

> **小技巧**  
> Python使用`pass`关键字作为空语句占位符。C++中可通过预处理器模拟：  
> ```cpp
> #define PASS
> 
> void foo(int x, int y)
> {
>     if (x > y)
>         PASS;
>     else
>         PASS;
> }
> ```  
> `PASS`被预处理器移除，末尾分号作为空语句存在。  

条件中的运算符==与=  
----------------  

条件判断应使用相等运算符`==`而非赋值运算符`=`。观察以下程序：  

```cpp
#include <iostream>

int main()
{
    std::cout << "输入0或1：";
    int x{};
    std::cin >> x;
    if (x = 0) // 错误：使用赋值而非相等判断
        std::cout << "您输入0\n";
    else
        std::cout << "您输入1\n";

    return 0;
}
```  

该程序编译通过但输出错误：  

```
输入0或1：0
您输入1
```  

实际执行流程为：`x = 0`先将0赋给x，然后表达式值为0（布尔假），故始终执行else分支。  

[下一课 8.4 — constexpr if语句](Chapter-8/lesson8.4-constexpr-if-statements.md)  
[返回主页](/)  
[上一课 8.2 — if语句与代码块](Chapter-8/lesson8.2-if-statements-and-blocks.md)