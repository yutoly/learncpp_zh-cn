6.2 — 算术运算符  
===========================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月13日 下午5:14（PDT）  
2025年2月14日更新  

一元算术运算符  
----------------  

C++提供两个一元算术运算符：正号（\+）和负号（\-）。需注意，**一元运算符（unary operator）**是仅接受单个操作数的运算符。

| 运算符符号 | 形式   | 操作                  |
|------------|--------|-----------------------|
| 一元正号 + | \+x    | 返回x的值             |
| 一元负号 - | \-x    | 返回x的负值（即x乘以-1） |

**一元负号运算符**返回操作数乘以-1的结果。例如，若x=5，则\-x为-5。  

**一元正号运算符**直接返回操作数值。例如，\+5等于5，\+x等于x。该运算符通常冗余，其存在主要是为了与一元负号运算符形成对称。  

为提高可读性，这两个运算符都应紧邻操作数（如`-x`而非`- x`）。  

注意区分**一元负号运算符**与**二元减法运算符**，虽然它们使用相同符号。例如在表达式`x = 5 - -3;`中，第一个减号是二元减法运算符，第二个是一元负号运算符。  

二元算术运算符  
----------------  

C++提供5个二元算术运算符。**二元运算符（binary operator）**需要左右两个操作数。

| 运算符符号 | 形式   | 操作                  |
|------------|--------|-----------------------|
| 加法 +     | x + y  | x加y                 |
| 减法 -     | x - y  | x减y                 |
| 乘法 *     | x * y  | x乘y                 |
| 除法 /     | x / y  | x除以y               |
| 取余 %     | x % y  | x除以y的余数         |

加法、减法和乘法运算符的行为与现实数学运算一致，没有特殊注意事项。  

除法和取余运算需要额外说明。本节讨论除法，下一课讲解取余运算。  

整数与浮点数除法  
----------------  

除法运算符有两种不同的"模式"：  
- 当任一（或两个）操作数为浮点数时，执行**浮点除法（floating point division）**，保留小数部分。例如`7.0 / 4 = 1.75`，`7 / 4.0 = 1.75`，`7.0 / 4.0 = 1.75`。所有浮点运算都可能存在舍入误差。  
- 当两个操作数均为整数时，执行**整数除法（integer division）**，丢弃小数部分返回整数。例如`7 / 4 = 1`，`-7 / 4 = -1`。  

使用static_cast<>实现整数转浮点除法  
----------------  

对于两个整数需要保留小数部分的除法，可使用`static_cast<>`将整数转换为浮点数：  

```cpp
#include <iostream>

int main()
{
    constexpr int x{ 7 };
    constexpr int y{ 4 };

    std::cout << "int / int = " << x / y << '\n';
    std::cout << "double / int = " << static_cast<double>(x) / y << '\n';
    std::cout << "int / double = " << x / static_cast<double>(y) << '\n';
    std::cout << "double / double = " << static_cast<double>(x) / static_cast<double>(y) << '\n';

    return 0;
}
```

输出结果：  
```
int / int = 1
double / int = 1.75
int / double = 1.75
double / double = 1.75
```

该示例表明只要任一操作数为浮点数，即执行浮点除法。  

除以0与0.0  
----------------  

整数除法中除数为`0`会导致**未定义行为（undefined behavior）**，因为数学上该运算无定义：  

```cpp
#include <iostream>

int main()
{
	constexpr int apples { 12 };
	std::cout << "你有" << apples << "个苹果。输入分配人数：";
	int x {};
	std::cin >> x;

	std::cout << "每人获得" << apples / x << "个完整苹果。\n"; // 整数除法

	return 0;
}
```

若输入`0`，程序可能崩溃。  

浮点数除以`0.0`的结果是**实现定义（implementation-defined）**。支持IEEE754浮点标准的架构会返回`NaN`（非数字）或`Inf`（无穷大），其他架构可能产生未定义行为。  

相关阅读：  
- `NaN`与`Inf`详见课程[4.8 — 浮点数](Chapter-4/lesson4.8-floating-point-numbers.md)  

可通过以下程序测试除以0或0.0的行为：  

```cpp
#include <iostream>

int main()
{
	constexpr int apples { 12 };
	std::cout << "你有" << apples << "个苹果。输入所需份数：";

	double d {};
	std::cin >> d;

	std::cout << "每份包含" << apples / d << "个苹果。\n"; // 浮点除法

	return 0;
}
```

算术赋值运算符  
----------------  

| 运算符符号 | 形式    | 操作                  |
|------------|---------|-----------------------|
| 加法赋值 +=  | x += y  | 将y加到x             |
| 减法赋值 -=  | x -= y  | 从x中减去y           |
| 乘法赋值 *=  | x *= y  | 将x乘以y             |
| 除法赋值 /=  | x /= y  | 将x除以y             |
| 取余赋值 %=  | x %= y  | 将x除以y的余数存入x  |

传统写法：  
```cpp
x = x + 4; // 给x加4
```  

算术赋值运算符简化形式：  
```cpp
x += 4; // 等价于x = x + 4
```  

修饰与非修饰运算符  
----------------  

能修改操作数值的运算符称为**修饰运算符（modifying operator）**。C++中大部分运算符是**非修饰运算符（non-modifying operator）**，但以下两类除外：  
1. 赋值运算符（包括标准赋值`=`、算术赋值`+=`等、位运算赋值`<<=`等）  
2. 自增自减运算符`++`和`--`（详见课程[6.4 — 自增/自减运算符及副作用](Chapter-6/lesson6.4-increment-decrement-operators-and-side-effects.md)）  

注意：`==`, `!=`, `<=`, `>=`是**非修饰关系运算符（non-modifying relational operator）**，详见课程[6.7 — 关系运算符与浮点数比较](Chapter-6/lesson6.7-relational-operators-and-floating-point-comparisons.md)。  

高级知识：  
重载运算符可能修改内置运算符的行为，例如输出流使用的`operator<<`会修改左操作数（输出流对象）。  

[下一课 6.3 取余与幂运算](Chapter-6/lesson6.3-remainder-and-exponentiation.md)  
[返回主页](/)  
[上一课 6.1 运算符优先级与结合性](Chapter-6/lesson6.1-operator-precedence-and-associativity.md)