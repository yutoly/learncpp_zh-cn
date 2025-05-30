6.7 — 关系运算符与浮点数比较
==========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月15日上午10:43（PDT）  
2025年1月21日更新  

**关系运算符（relational operators）**是用于比较两个值的运算符。C++提供6种关系运算符：

| 运算符 | 符号形式 | 操作描述 |
| --- | --- | --- |
| 大于 | \> | x \> y：若x大于y则为true，否则false |
| 小于 | \< | x \< y：若x小于y则为true，否则false |
| 大于等于 | \>\= | x \>\= y：若x大于等于y则为true，否则false |
| 小于等于 | \<\= | x \<\= y：若x小于等于y则为true，否则false |
| 等于 | \=\= | x \=\= y：若x等于y则为true，否则false |
| 不等于 | !\= | x !\= y：若x不等于y则为true，否则false |

这些运算符的运算结果均为布尔值true（1）或false（0）。以下是与整数配合使用的示例代码：
```cpp
#include <iostream>

int main()
{
    std::cout << "请输入一个整数：";
    int x{};
    std::cin >> x;

    std::cout << "请输入另一个整数：";
    int y{};
    std::cin >> y;

    if (x == y)
        std::cout << x << " 等于 " << y << '\n';
    if (x != y)
        std::cout << x << " 不等于 " << y << '\n';
    if (x > y)
        std::cout << x << " 大于 " << y << '\n';
    if (x < y)
        std::cout << x << " 小于 " << y << '\n';
    if (x >= y)
        std::cout << x << " 大于等于 " << y << '\n';
    if (x <= y)
        std::cout << x << " 小于等于 " << y << '\n';

    return 0;
}
```
运行示例：
```
请输入一个整数：4
请输入另一个整数：5
4 不等于 5
4 小于 5
4 小于等于 5
```

布尔条件值的简化写法  
----------------  
在*if语句*或*条件运算符*中，默认会将条件评估为布尔值。许多新手会写出如下冗余代码：
```cpp
if (b1 == true) ...  // 冗余写法
```
应简化为：
```cpp
if (b1) ...          // 推荐写法
```
同理：
```cpp
if (b1 == false) ... // 冗余写法
```
应简化为：
```cpp
if (!b1) ...         // 推荐写法
```

> **最佳实践**  
> 避免在条件式中添加不必要的\=\=或!\=运算符，这会降低可读性且无实际价值。

浮点数计算的比较问题  
----------------  
考虑以下程序：
```cpp
#include <iostream>

int main()
{
    constexpr double d1{ 100.0 - 99.99 }; // 数学上应等于0.01
    constexpr double d2{ 10.0 - 9.99 };   // 数学上应等于0.01

    if (d1 == d2)
        std::cout << "d1 == d2" << '\n';
    else if (d1 > d2)
        std::cout << "d1 > d2" << '\n';
    else if (d1 < d2)
        std::cout << "d1 < d2" << '\n';
    
    return 0;
}
```
理论上d1和d2都应等于*0.01*，但实际输出为：
```
d1 > d2
```
调试查看会发现d1=0.010000000000005116，d2=0.0099999999999997868，两者虽接近但存在微小差异。由于浮点数的精度限制，使用关系运算符比较计算结果可能产生意外结果。

> **相关阅读**  
> 关于舍入误差的讨论详见课程[4.8 — 浮点数](Chapter-4/lesson4.8-floating-point-numbers.md)。

浮点数的比较策略  
----------------  
### 大小比较运算符（\<, \>, \<=, \>=）
当操作数差异明显时，这些运算符通常可靠。但当数值接近时可能因舍入误差产生错误结果。例如上述示例中`d1 > d2`返回true，但若误差方向相反则可能返回false。

### 相等性运算符（\=\=, !\=）
这两个运算符问题更严重。由于微小误差就会导致数值不等，`operator\=\=`极易在预期相等时返回false：
```cpp
#include <iostream>

int main()
{
    std::cout << std::boolalpha << (0.3 == 0.2 + 0.1); // 输出false
    return 0;
}
```

> **警告**  
> 避免对计算结果使用\=\=和!\=比较浮点数。

例外情况  
----------------  
以下情况可安全比较：
1. 浮点字面量与同类型变量（使用相同字面量初始化）
2. 字面量有效数字不超过类型精度（float：6位，double：15位）

例如：
```cpp
if (someFcn() == 0.0) // 安全：当函数返回0.0字面量时
```
或：
```cpp
constexpr double gravity { 9.8 };
if (gravity == 9.8)    // 安全：使用相同字面量初始化
```

> **注意**  
> 比较不同类型浮点字面量（如`9.8f`与`9.8`）通常不安全。

浮点数比较算法（进阶阅读）  
----------------  
### 绝对epsilon法
```cpp
#include <cmath>
bool approximatelyEqualAbs(double a, double b, double absEpsilon)
{
    return std::abs(a - b) <= absEpsilon;
}
```
此方法简单但需根据数值范围调整epsilon，适用性有限。

### 相对epsilon法（Knuth算法）
```cpp
#include <algorithm>
#include <cmath>
bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
    return std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon);
}
```
该算法将epsilon设为较大数的百分比，适应性更强。

### 混合算法
结合绝对和相对epsilon以处理接近零的情况：
```cpp
bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    if (std::abs(a - b) <= absEpsilon) return true;
    return approximatelyEqualRel(a, b, relEpsilon);
}
```
推荐参数：absEpsilon=1e-12，relEpsilon=1e-8。

C++23中的constexpr实现  
----------------  
```cpp
// C++23版本
#include <algorithm>
#include <cmath>
constexpr bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}
```

C++23之前的兼容实现  
----------------  
```cpp
template <typename T>
constexpr T constAbs(T x) { return (x < 0 ? -x : x); } // 自定义constexpr绝对值函数

constexpr bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    if (constAbs(a - b) <= absEpsilon) return true;
    return approximatelyEqualRel(a, b, relEpsilon);
}
```

[下一课 6.8 逻辑运算符](Chapter-6/lesson6.8-logical-operators.md)  
[返回主页](/)  
[上一课 6.6 条件运算符](Chapter-6/lesson6.6-the-conditional-operator.md)