O.1 — 位标志（bit flags）与通过std::bitset进行位操作（bit manipulation）
====================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月15日（首次发布于2019年8月17日）

在现代计算机体系结构中，内存的最小可寻址单元是字节。由于所有对象都需要唯一内存地址，这意味着对象大小至少为一个字节。对于大多数变量类型而言这没有问题，但对于布尔（Boolean）值则略显浪费。布尔类型仅有两种状态：true（1）或 false（0），只需1位存储空间。然而变量必须占用至少1字节（8位），这意味着布尔值仅使用其中1位而浪费其余7位。

多数情况下这无关紧要——我们通常不会因7位内存浪费而过度优化（代码可理解性和可维护性更为重要）。但在存储密集型场景中，将8个独立布尔值"打包"进单个字节可显著提升存储效率。

实现这些操作需要我们在位（bit）级别操控对象。幸运的是，C++为此提供了专用工具。修改对象中单个位的过程称为**位操作（bit manipulation）**。

> **作者注**  
> 位操作常见于图形学、加密、压缩和优化等特定编程场景，但在通用编程中应用较少。因此本章为选读内容，可跳过或略读后回看。

位标志（bit flags）  
----------------  

此前我们使用变量存储单个值：
```cpp
int foo { 5 }; // 赋值5（可能占用32位存储）
std::cout << foo; // 输出5
```

但我们可将对象中的每个位视为独立布尔值。当对象中的单个位作为布尔值使用时，这些位称为**位标志**。

**术语说明**  
* 值为`0`的位称为"假"、"关闭"或"未置位"  
* 值为`1`的位称为"真"、"开启"或"置位"  
* 位值从`0`到`1`或`1`到`0`的变化称为"翻转"或"反相"

> **延伸阅读**  
> 在计算领域，**标志（flag）**是表示程序状态的信号值。位标志中的`true`值表示状态存在。类比美国邮箱侧面的小红旗：当有待取邮件时，红旗升起表示存在待发邮件。

定义位标志集合时，通常使用适当大小的无符号整型（8位、16位、32位等，根据标志数量）或`std::bitset`：
```cpp
#include <bitset> // 引入std::bitset

std::bitset<8> mybitset {}; // 8位大小可存储8个标志
```

> **最佳实践**  
> 位操作是少数应明确使用无符号整型（或`std::bitset`）的场景之一。

本章将展示通过`std::bitset`进行位操作的简易方法，后续课程将探讨更灵活但复杂的方式。

位编号与位位置（Bit numbering and bit positions）  
----------------  

给定位序列时，通常从右至左编号，起始为0（而非1）。每个编号称为**位位置**：
```
76543210  // 位位置
00000101  // 位序列
```
对于序列0000 0101，位置0和2的位值为1，其余为0。

通过std::bitset操作位  
----------------  

在[5.3 — 进制系统（十进制、二进制、十六进制与八进制）](Chapter-5/lesson5.3-numeral-systems-decimal-binary-hexadecimal-and-octal.md)课程中，我们已展示使用`std::bitset`输出二进制值。但`std::bitset`的功能远不止于此。

`std::bitset`提供四个关键成员函数：
* test()：查询位的值（0或1）
* set()：置位（若已置位则不操作）
* reset()：复位（若已复位则不操作）
* flip()：翻转位值（0↔1）

每个函数以操作位的位置作为唯一参数。

示例：
```cpp
#include <bitset>
#include <iostream>

int main()
{
    std::bitset<8> bits{ 0b0000'0101 }; // 初始位模式0000 0101
    bits.set(3);   // 位置3置1 → 0000 1101
    bits.flip(4);  // 翻转位置4 → 0001 1101
    bits.reset(4); // 位置4复位 → 0000 1101

    std::cout << "所有位: " << bits << '\n';
    std::cout << "位3的值: " << bits.test(3) << '\n';
    std::cout << "位4的值: " << bits.test(4) << '\n';

    return 0;
}
```
输出：
```
所有位: 00001101
位3的值: 1
位4的值: 0
```

> **提示**  
> 成员函数在[5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)中首次介绍。常规函数调用形式为`函数(对象)`，成员函数则为`对象.函数()`。  
> `0b`二进制字面量前缀和`'`数字分隔符详见[5.3课程](Chapter-5/lesson5.3-numeral-systems-decimal-binary-hexadecimal-and-octal.md)。

通过命名位提升代码可读性：
```cpp
#include <bitset>
#include <iostream>

int main()
{
    [[maybe_unused]] constexpr int  isHungry   { 0 }; // 饥饿
    [[maybe_unused]] constexpr int  isSad      { 1 }; // 悲伤
    [[maybe_unused]] constexpr int  isMad      { 2 }; // 愤怒
    [[maybe_unused]] constexpr int  isHappy    { 3 }; // 快乐
    [[maybe_unused]] constexpr int  isLaughing { 4 }; // 大笑
    [[maybe_unused]] constexpr int  isAsleep   { 5 }; // 睡眠
    [[maybe_unused]] constexpr int  isDead     { 6 }; // 死亡
    [[maybe_unused]] constexpr int  isCrying   { 7 }; // 哭泣

    std::bitset<8> me{ 0b0000'0101 }; // 初始位模式0000 0101
    me.set(isHappy);      // 位3置1 → 0000 1101
    me.flip(isLaughing);  // 翻转位4 → 0001 1101
    me.reset(isLaughing); // 位4复位 → 0000 1101

    std::cout << "所有位: " << me << '\n';
    std::cout << "是否快乐: " << me.test(isHappy) << '\n';
    std::cout << "是否大笑: " << me.test(isLaughing) << '\n';

    return 0;
}
```

> **相关内容**  
> `[[maybe_unused]]`属性详见[1.4 — 变量赋值与初始化](Chapter-1/lesson1.4-variable-assignment-and-initialization.md)。  
> [13.2 — 非限定作用域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)课程展示如何用枚举器（enumerator）创建更优的命名位集合。

如需同时操作多个位，`std::bitset`并不直接支持。此时需使用传统方法（后续课程将涉及）或改用无符号整型位标志。

std::bitset的大小  
----------------  

需注意`std::bitset`为速度优化而非内存节省设计。其大小通常为存储所需字节数向上取整至`sizeof(size_t)`（32位机器为4字节，64位为8字节）。因此`std::bitset<8>`实际占用4或8字节内存，尽管技术上仅需1字节存储8位。故`std::bitset`适用于便利性优先场景，而非内存敏感场景。

std::bitset的查询功能  
----------------  

其他实用成员函数：
* size()：返回bitset位数
* count()：返回置位位数
* all()：检查所有位是否置位
* any()：检查是否有位置位
* none()：检查是否无位置位

示例：
```cpp
#include <bitset>
#include <iostream>

int main()
{
    std::bitset<8> bits{ 0b0000'1101 };
    std::cout << "总位数: " << bits.size() << '\n';
    std::cout << "置位位数: " << bits.count() << '\n';

    std::cout << std::boolalpha;
    std::cout << "全置位: " << bits.all() << '\n';
    std::cout << "存在置位: " << bits.any() << '\n';
    std::cout << "无置位: " << bits.none() << '\n';
    
    return 0;
}
```
输出：
```
总位数: 8
置位位数: 3
全置位: false
存在置位: true
无置位: false
```

[下一课O.2 位运算符](Chapter-O/lessonO.2-bitwise-operators.md)  
[返回主页](/)  
[上一课6.x 第六章总结与测验](Chapter-6/lesson6.x-chapter-6-summary-and-quiz.md)