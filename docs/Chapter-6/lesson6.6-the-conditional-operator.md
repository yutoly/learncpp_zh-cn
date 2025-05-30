6.6 — 条件运算符  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月14日（首次发布于2023年10月23日）  

| 运算符符号 | 形式 | 含义 |  
| --- | --- | --- |  
| 条件运算符 | ?: | c ? x : y | 若条件`c`为`true`则求值`x`，否则求值`y` |  

**条件运算符（conditional operator）**（`?:`）（有时也称为**算术if运算符（arithmetic if）**）是三元运算符（接受3个操作数的运算符）。由于历史上是C++唯一的二元运算符，故有时也被称为"三元运算符（ternary operator）"。该运算符为特定类型的if-else语句提供了简写形式。相关阅读我们将在[4.10 — if语句简介](Chapter-4/lesson4.10-introduction-to-if-statements.md)中讲解if-else语句。



回顾if-else语句的基本结构：
```
if (条件)
    语句1;
else
    语句2;
```
若`条件`求值为`true`则执行`语句1`，否则执行`语句2`。`else`和`语句2`是可选的。条件运算符的形式为：
```
条件 ? 表达式1 : 表达式2;
```
若`条件`求值为`true`则求值`表达式1`，否则求值`表达式2`。`:`和`表达式2`不可省略。考虑如下if-else语句：
```
if (x > y)
    max = x;
else
    max = y;
```
可改写为：
```
max = ((x > y) ? x : y);
```
在此类场景中，条件运算符能在保持可读性的前提下精简代码。示例程序：
```
#include <iostream>

int getValue()
{
    std::cout << "请输入一个数字：";
    int x{};
    std::cin >> x;
    return x;
}

int main()
{
    int x { getValue() };
    int y { getValue() };
    int max { (x > y) ? x : y };
    std::cout << x << "和" << y << "的最大值是" << max << ".\n";
    return 0;
}
```
首先输入`5`和`7`时，`x`为5，`y`为7。初始化`max`时求值`(5 > 7) ? 5 : 7`，因条件为假，结果为`7`。程序输出：
```
5和7的最大值是7.
```
若输入`7`和`5`，求值`(7 > 5) ? 7 : 5`结果为`7`，输出：
```
7和5的最大值是7.
```
条件运算符作为表达式的一部分由于条件运算符在表达式中求值，因此可出现在任何接受表达式的位置。当条件运算符的操作数为常量表达式时，该运算符也可用于常量表达式。这使得条件运算符能用于无法使用语句的场合。例如变量初始化：
```
#include <iostream>

int main()
{
    constexpr bool 大教室模式 { false };
    constexpr int 班级人数 { 大教室模式 ? 30 : 20 };
    std::cout << "班级人数：" << 班级人数 << '\n';
    return 0;
}
```
此时无法用if-else直接替代。若尝试：
```
#include <iostream>

int main()
{
    constexpr bool 大教室模式 { false };

    if (大教室模式)
        constexpr int 班级人数 { 30 };
    else
        constexpr int 班级人数 { 20 }; 

    std::cout << "班级人数：" << 班级人数 << '\n'; // 编译错误：班级人数未定义
    return 0;
}
```
将导致编译错误，因为if/else语句中定义的`班级人数`会在语句结束时销毁。改用函数实现：
```
#include <iostream>

int 获取班级人数(bool 大教室模式)
{
    if (大教室模式)
        return 30;
    else
        return 20;
}

int main()
{
    const int 班级人数 { 获取班级人数(false) };
    std::cout << "班级人数：" << 班级人数 << '\n';
    return 0;
}
```
此方案可行但代码冗余，直接使用条件运算符更简洁。条件运算符的括号使用由于C++运算符优先级规则，条件运算符容易引发意外求值顺序。相关阅读运算符优先级将在[6.1 — 运算符优先级与结合性](Chapter-6/lesson6.1-operator-precedence-and-associativity.md)详细讲解。



示例：
```
#include <iostream>

int main()
{
    int x { 2 };
    int y { 1 };
    int z { 10 - x > y ? x : y };
    std::cout << z; // 输出2而非预期的8
    return 0;
}
```
实际求值为`(10 - x) > y ? x : y`而非预期的`10 - (x > y ? x : y)`。另一个常见错误：
```
#include <iostream>

int main()
{
    int x { 2 };
    std::cout << (x < 0) ? "负数" : "非负数"; // 输出0而非"非负数"
    return 0;
}
```
可选解析此例中，`x < 0`求值为`false`，表达式变为`std::cout << false ? "负数" : "非负数"`。由于`operator<<`优先级高于`?:`，实际求值为`(std::cout << false) ? "负数" : "非负数"`。首先输出`0`，然后`std::cout`转换为`bool`（可能为`false`），最终表达式求值为`"非负数"`但无输出效果。

为避免此类问题，条件运算符应遵循以下括号规则：* 在复合表达式中使用时，整个条件运算（含操作数）需加括号* 为提高可读性，当条件包含运算符时建议给条件加括号（函数调用运算符除外）

操作数本身无需括号。括号使用示例：
```
return 被击晕 ? 0 : 剩余移动;           // 非复合表达式，条件无运算符
int z { (x > y) ? x : y };              // 非复合表达式，条件含运算符
std::cout << (是否下午() ? "PM" : "AM"); // 复合表达式，条件无运算符（函数调用除外）
std::cout << ((x > y) ? x : y);         // 复合表达式，条件含运算符
```
最佳实践在复合表达式中使用时，为整个条件运算加括号。当条件含运算符时，建议为条件加括号以提高可读性。



表达式类型匹配要求为满足C++类型检查规则，需满足以下条件之一：* 第二、第三操作数类型相同* 编译器能找到将操作数转换为相同类型的方法（转换规则复杂，可能产生意外结果）

进阶阅读若任一操作数为throw表达式也允许，详见[27.2 — 基础异常处理](Chapter-27/lesson27.2-basic-exception-handling.md)。



示例：
```
#include <iostream>

int main()
{
    std::cout << (true ? 1 : 2) << '\n';    // 正确：两操作数均为int

    std::cout << (false ? 1 : 2.2) << '\n'; // 正确：int 1转换为double

    std::cout << (true ? -1 : 2u) << '\n';  // 意外结果：-1转为无符号整型
    return 0;
}
```
假设int为4字节，输出：
```
1
2.2
4294967295
```
通常，混合基础类型操作数可行（但需避免有符号与无符号混用）。若非基础类型，建议显式转换类型。相关阅读混合有符号/无符号值的意外结果源于[10.5 — 算术转换](Chapter-10/lesson10.5-arithmetic-conversions.md)的规则。



若编译器无法找到共同类型，将产生编译错误：
```
#include <iostream>

int main()
{
    constexpr int x{ 5 };
    std::cout << ((x != 5) ? x : "x是5"); // 错误：无法为int和C风格字符串找共同类型
    return 0;
}
```
此时可显式转换或使用if-else：
```
#include <iostream>
#include <string>

int main()
{
    int x{ 5 }; // 特例设为非constexpr

    // 显式转换类型
    std::cout << ((x != 5) ? std::to_string(x) : std::string{"x是5"}) << '\n';

    // 使用if-else
    if (x != 5)
        std::cout << x << '\n';
    else
        std::cout << "x是5" << '\n';
    return 0;
}
```
进阶阅读若`x`为constexpr，应优先使用`if constexpr`（详见[8.4 — constexpr if语句](Chapter-8/lesson8.4-constexpr-if-statements.md)）。本例设为非constexpr以避免警告。



适用场景条件运算符最适用于：* 用两个值初始化对象* 为对象赋值两个值之一* 向函数传递两个值之一* 从函数返回两个值之一* 输出两个值之一

复杂表达式应避免使用条件运算符，因其易错且可读性差。最佳实践避免在复杂表达式中使用条件运算符。



[下一课 6.7 关系运算符与浮点数比较](Chapter-6/lesson6.7-relational-operators-and-floating-point-comparisons.md)  
[返回主页](/)  
[上一课 6.5 逗号运算符](Chapter-6/lesson6.5-the-comma-operator.md)