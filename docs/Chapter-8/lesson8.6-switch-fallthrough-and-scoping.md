8.6 — Switch 的贯穿现象与作用域  
=====================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月1日（首次发布于2020年12月21日）  

本课继续探讨[8.5 — Switch 语句基础](Chapter-8/lesson8.5-switch-statement-basics.md)中介绍的 switch 语句。上节课提到，每个 case 标签下的语句组应以`break 语句`或`return 语句`结束。  

本课将深入探讨原因，并分析 switch 作用域相关的常见问题。  

贯穿现象（Fallthrough）  
----------------  

当 switch 表达式匹配 case 标签或 default 标签时，程序从匹配标签后的第一条语句开始执行。执行将持续到以下任一终止条件发生：  

* 到达 switch 块末尾  
* 控制流语句（通常为`break`或`return`）导致退出 switch 块或函数  
* 程序被外部因素中断（如操作系统关闭、宇宙坍缩等）  

需注意：其他 case 标签的存在*不*属于终止条件——因此若无`break`或`return`，执行将"贯穿"后续 case。  

以下程序演示此行为：  

```cpp
#include <iostream>

int main()
{
    switch (2)
    {
    case 1: // 不匹配
        std::cout << 1 << '\n'; // 跳过
    case 2: // 匹配
        std::cout << 2 << '\n'; // 从此处开始执行
    case 3:
        std::cout << 3 << '\n'; // 继续执行
    case 4:
        std::cout << 4 << '\n'; // 继续执行
    default:
        std::cout << 5 << '\n'; // 继续执行
    }

    return 0;
}
```  

该程序输出：  

```
2
3
4
5
```  

这通常不符合预期！当执行流从某个标签下的语句流向后续标签下的语句时，称为**贯穿（fallthrough）**。  



警告  
-----  
一旦开始执行 case 或 default 标签下的语句，执行流将贯穿后续 case。通常应使用 break 或 return 阻止该现象。  

由于贯穿通常非预期行为，多数编译器及代码分析工具会将其标记为警告。  

[[fallthrough]] 属性  
----------------  

通过注释说明贯穿意图是常见做法，但编译器无法解析注释。为此，C++17 引入`[[fallthrough]]`属性。  

**属性（attribute）**是现代 C++ 特性，允许向编译器传递代码的附加信息。属性名置于双中括号内，可出现在相关上下文的任何位置。  

`[[fallthrough]]`属性修饰**空语句（null statement）**来表明贯穿意图：  

```cpp
#include <iostream>

int main()
{
    switch (2)
    {
    case 1:
        std::cout << 1 << '\n';
        break;
    case 2:
        std::cout << 2 << '\n'; // 从此处开始执行
        [[fallthrough]]; // 注意分号表示空语句
    case 3:
        std::cout << 3 << '\n'; // 继续执行
        break;
    }

    return 0;
}
```  

程序输出：  

```
2
3
```  

此写法不会触发贯穿警告。  



最佳实践  
-----  
使用`[[fallthrough]]`属性（配合空语句）表示有意贯穿。  

连续 case 标签  
----------------  

可通过逻辑 OR 运算符组合多个条件：  

```cpp
bool isVowel(char c)
{
    return (c=='a' || c=='e' || c=='i' || c=='o' || c=='u' ||
        c=='A' || c=='E' || c=='I' || c=='O' || c=='U');
}
```  

但此写法存在与 switch 语句相同的重复判断问题。使用连续 case 标签可实现类似效果：  

```cpp
bool isVowel(char c)
{
    switch (c)
    {
    case 'a': // c 为 'a'
    case 'e': // 或 'e'
    case 'i': // 或 'i'
    case 'o': // 或 'o'
    case 'u': // 或 'u'
    case 'A': // 或 'A'
    case 'E': // 或 'E'
    case 'I': // 或 'I'
    case 'O': // 或 'O'
    case 'U': // 或 'U'
        return true;
    default:
        return false;
    }
}
```  

注意：case 标签后的第一条有效语句是`return true`，因此任何 case 匹配都将返回 true。  

这种"堆叠"case 标签的做法不视为贯穿行为，无需注释或`[[fallthrough]]`。  

标签不创建新作用域  
----------------  

在 if 语句中，条件后的单条语句隐式属于代码块：  

```cpp
if (x > 10)
    std::cout << x << " 大于 10\n"; // 隐式属于代码块
```  

但 switch 语句中，所有标签下的语句共享 switch 块作用域：  

```cpp
switch (1)
{
case 1: // 不创建隐式块
    foo(); // 属于 switch 作用域
    break; // 属于 switch 作用域
default:
    std::cout << "默认情况\n";
    break;
}
```  

case 语句中的变量声明与初始化  
----------------  

可在 switch 块内（case 标签前后）声明变量，但不可初始化：  

```cpp
switch (1)
{
    int a; // 合法：声明
    int b{ 5 }; // 非法：初始化

case 1:
    int y; // 合法但不良实践
    y = 4; // 合法
    break;

case 2:
    int z{ 4 }; // 非法：后续存在其他 case
    y = 5; // 合法：使用上方声明的 y
    break;

case 3:
    break;
}
```  

变量`y`在`case 1`声明后，可在`case 2`使用。但变量初始化需执行定义语句，因此非最后 case 中的初始化被禁止。  

若需在 case 中定义/初始化变量，最佳实践是在显式代码块中操作：  

```cpp
switch (1)
{
case 1:
{ // 显式代码块
    int x{ 4 }; // 合法
    std::cout << x;
    break;
}

default:
    std::cout << "默认情况\n";
    break;
}
```  



最佳实践  
-----  
在 case 语句中使用变量时，应在显式代码块内定义。  

测验  
----------------  

问题 #1  
编写 calculate() 函数，接收两个整数和一个代表运算符（+、-、*、/ 或 %）的 char。使用 switch 执行运算并返回结果。若运算符无效，输出错误信息。除法使用整数除法，无需处理除零错误。  

提示："operator"是关键字，变量不能以此命名。  

  

```cpp
#include <iostream>

int calculate(int x, int y, char op)
{
    switch (op)
    {
    case '+':
        return x + y;
    case '-':
        return x - y;
    case '*':
        return x * y;
    case '/':
        return x / y;
    case '%':
        return x % y;
    default:
        std::cout << "calculate(): 未知运算符\n";
        return 0;
    }
}

int main()
{
    std::cout << "输入整数：";
    int x{};
    std::cin >> x;

    std::cout << "输入另一整数：";
    int y{};
    std::cin >> y;

    std::cout << "输入运算符（+、-、*、/ 或 %）：";
    char op{};
    std::cin >> op;

    int result{ calculate(x, y, op) };
    std::cout << x << ' ' << op << ' ' << y << " = " << result << '\n';

    return 0;
}
```  

[下一课 8.7 goto 语句](Chapter-8/lesson8.7-goto-statements.md)  
[返回主页](/)  
[上一课 8.5 switch 语句基础](Chapter-8/lesson8.5-switch-statement-basics.md)