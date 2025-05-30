4.x — 第4章 小结与测验  
=================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月11日 下午5:42（太平洋夏令时）  
2024年11月29日  

本章回顾  
----------------  

内存的最小单位是**二进制位（bit）**。可直接寻址的最小内存单元是**字节（byte）**。现代标准规定1字节等于8位。  

**数据类型（data type）**指示编译器如何有意义地解释内存内容。  

C++支持多种基础数据类型，包括浮点数、整数、布尔值、字符、空指针和void类型。  

**Void**用于表示无类型，主要用于指示函数不返回值。  

不同数据类型占用不同内存量，具体内存用量可能因机器而异。  

> **相关内容**  
> 各基础类型的最小尺寸表见课程[4.3 — 对象大小与sizeof运算符](Chapter-4/lesson4.3-object-sizes-and-the-sizeof-operator.md)  

**sizeof运算符**可用于获取类型的字节大小。  

**有符号整数（signed integers）**用于存储正负整数和0。数据类型能保存的值集合称为**范围（range）**。使用整数时需注意溢出和整数除法问题。  

**无符号整数（unsigned integers）**仅存储正数和0，通常应避免使用（位操作除外）。  

**固定宽度整数类型（fixed-width integers）**保证尺寸但可能不兼容所有架构。fast和least类型分别表示至少某尺寸的最快/最小整数类型。通常应避免使用`std::int8_t`和`std::uint8_t`，因其行为类似字符而非整数。  

**size_t**是无符号整型，用于表示对象的大小或长度。  

**科学计数法（scientific notation）**是书写长数字的简写方式。C++支持结合浮点数使用科学计数法。有效数（e前部分）中的数字称为**有效数字（significant digits）**。  

**浮点数（floating point）**类型用于存储实数（含小数）。**精度（precision）**定义数字能无损表示的有效数字位数。当存储超过精度的有效数字时会发生**舍入误差（rounding error）**。舍入误差普遍存在，即使简单如0.1的数字也会发生，因此不应直接比较浮点数。  

**布尔（boolean）**类型用于存储`true`或`false`值。  

**if语句（if statements）**允许在条件为真时执行代码块。if语句的条件表达式被解释为布尔值。**else语句**用于在先前if条件为假时执行代码。  

**字符（char）**用于存储ASCII字符值。使用字符时需注意区分ASCII码值和数字。用整数形式打印字符需使用`static_cast`。  

尖括号通常用于表示需要参数化类型的场景。例如`static_cast<int>(x)`将x的值转换为int类型。  

测验时间  
----------------  

**问题1**  
为以下场景选择最合适的数据类型。尽可能具体。若答案为整数，根据范围选择int（尺寸无关）或固定宽度整数类型：  

a) 用户年龄（岁）（假设类型尺寸不重要）  
  
<details><summary>答案</summary>int</details>  

b) 用户是否检查更新  
  
<details><summary>答案</summary>bool</details>  

c) 圆周率π（3.14159265）  
  
<details><summary>答案</summary>double</details>  

d) 教材页数（假设尺寸不重要）  
  
<details><summary>答案</summary>int（书籍通常不超过32,767页）</details>  

e) 沙发长度（英尺，保留两位小数）（尺寸重要）  
  
<details><summary>答案</summary>float</details>  

f) 出生至今眨眼次数（百万级）  
  
<details><summary>答案</summary>std::int32_t</details>  

g) 用户通过字母选择菜单项  
  
<details><summary>答案</summary>char</details>  

h) 出生年份（尺寸重要）  
  
<details><summary>答案</summary>std::int16_t（正数表示公元后，负数表示公元前）</details>  

**问题2**  
编写程序：用户输入两个double值，再输入运算符（+、-、*、/），程序计算并输出结果。无效符号不输出。  

[查看提示](javascript:void(0))  
<details><summary>提示1</summary>编写三个函数：获取double值、获取运算符、计算并输出结果</details>  
<details><summary>提示2</summary>使用if语句和operator==比较运算符</details>  
<details><summary>提示3</summary>无效操作时使用提前返回</details>  

  
<details><summary>代码</summary>

```cpp
#include <iostream>

double getDouble()
{
    std::cout << "Enter a double value: ";
    double x{};
    std::cin >> x;
    return x;
}

char getOperator()
{
    std::cout << "Enter +, -, *, or /: ";
    char operation{};
    std::cin >> operation;
    return operation;
}

void printResult(double x, char operation, double y)
{
    double result{};

    if (operation == '+')
        result = x + y;
    else if (operation == '-')
        result = x - y;
    else if (operation == '*')
        result = x * y;
    else if (operation == '/')
        result = x / y;
    else        // 无效操作
        return; // 提前返回

    std::cout << x << ' ' << operation << ' ' << y << " is " << result << '\n';
}

int main()
{
    double x { getDouble() };
    double y { getDouble() };

    char operation { getOperator() };

    printResult(x, operation, y);

    return 0;
}
```
</details>  

**问题3（附加题）**  
模拟球体从塔顶坠落：输入塔高（米），考虑重力（9.8m/s²）且初速为0。输出0-5秒后球体高度（不低于地面）。  

  
<details><summary>代码</summary>

```cpp
#include <iostream>

// 从用户获取塔高并返回
double getTowerHeight()
{
	std::cout << "Enter the height of the tower in meters: ";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// 计算seconds秒后的球体高度
double calculateBallHeight(double towerHeight, int seconds)
{
	double gravity { 9.8 };
    
	// 公式：s = (u * t) + (a * t²)/2（初速u=0）
	double fallDistance { gravity * (seconds * seconds) / 2.0 };
	double ballHeight { towerHeight - fallDistance };

	return (ballHeight < 0.0) ? 0.0 : ballHeight;
}

// 打印球体高度
void printBallHeight(double ballHeight, int seconds)
{
	if (ballHeight > 0.0)
		std::cout << "At " << seconds << " seconds, the ball is at height: " << ballHeight << " meters\n";
	else
		std::cout << "At " << seconds << " seconds, the ball is on the ground.\n";
}

// 计算并打印高度的辅助函数
void calculateAndPrintBallHeight(double towerHeight, int seconds)
{
	printBallHeight(calculateBallHeight(towerHeight, seconds), seconds);
}

int main()
{
	double towerHeight{ getTowerHeight() };

	calculateAndPrintBallHeight(towerHeight, 0);
	calculateAndPrintBallHeight(towerHeight, 1);
	calculateAndPrintBallHeight(towerHeight, 2);
	calculateAndPrintBallHeight(towerHeight, 3);
	calculateAndPrintBallHeight(towerHeight, 4);
	calculateAndPrintBallHeight(towerHeight, 5);
       
	return 0;
}
```
</details>  

[下一课 5.1 — 常量变量（命名常量）](Chapter-5/lesson5.1-constant-variables-named-constants.md)  
[返回主页](/)  
[上一课 4.12 — 类型转换与static_cast简介](Chapter-4/lesson4.12-introduction-to-type-conversion-and-static_cast.md)