4.10 — if语句简介  
=====================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2019年4月23日12:57 PDT（太平洋夏令时） / 2025年2月11日修订  

假设您要去超市，室友叮嘱："如果草莓特价，就买一些"。这是一个条件语句，意味着只有当条件（"草莓特价"）成立时才会执行特定动作（"购买"）。这类条件在编程中十分常见，因为它们允许我们在程序中实现条件性行为。  

C++中最基本的条件语句称为*if语句*。**if语句（if statement）**允许我们在特定条件为真时执行一行（或多行）代码。最简单的if语句形式如下：  
```
if (条件) 真值语句;
```  
为提高可读性，通常写作：  
```
if (条件)
    真值语句;
```  
**条件（condition）**（亦称**条件表达式（conditional expression）**）是一个求值为布尔值的表达式。  

若if语句的*条件*求值为布尔值*true*，则执行*真值语句*。若求值为*false*，则跳过*真值语句*。  

示例程序  
考虑以下程序：  
```cpp
#include <iostream>

int main()
{
    std::cout << "输入整数：";
    int x{};
    std::cin >> x;

    if (x == 0)
        std::cout << "值为零\n";

    return 0;
}
```  
运行示例输出：  
```
输入整数：0
值为零
```  
详细解析：  
1. 用户输入整数  
2. 条件*x == 0*被求值。**相等运算符（equality operator）**（==）用于测试两个值是否相等：当操作数相等时返回*true*，否则返回*false*。因x值为0，故条件成立  
3. 条件为真，执行后续语句输出结果  

另一运行示例：  
```
输入整数：5
```  
此时*x == 0*求值为false，跳过输出语句。  

> **警告**  
> if语句仅能条件性执行单条语句。如何条件执行多语句详见课程[8.2 — if语句与代码块](Chapter-8/lesson8.2-if-statements-and-blocks.md)。  

if-else结构  
若需告知用户输入的是非零数，可改进为：  
```cpp
if (x == 0)
    std::cout << "值为零\n";
else
    std::cout << "值为非零\n";
```  
**if-else**结构语法：  
```
if (条件)
    真值语句;
else
    假值语句;
```  
当*条件*为true时执行真值语句，否则执行假值语句。  

链式if语句  
通过将if-else串联可实现多条件检测：  
```cpp
if (x > 0)
    std::cout << "值为正\n";
else if (x < 0)
    std::cout << "值为负\n";
else 
    std::cout << "值为零\n";
```  
**小于运算符（<）**和**大于运算符（>）**分别测试数值大小关系，返回布尔值。  

布尔返回值与if语句  
结合返回布尔值的函数使用if语句：  
```cpp
bool isEqual(int x, int y)
{
    return x == y;
}

if (isEqual(x, y))
    std::cout << x << "与" << y << "相等\n";
else
    std::cout << x << "与" << y << "不相等\n";
```  

非布尔条件  
当条件表达式非布尔类型时，将转换为布尔值：非零值转为true，零值转为false。例如：  
```cpp
if (x) // 若x非零
    std::cout << "hi\n";
else
    std::cout << "bye\n";
```  

if语句与提前返回  
**提前返回（early return）**指在函数末尾之前执行的return语句。结合if语句可实现条件返回：  
```cpp
int abs(int x) 
{
    if (x < 0)
        return -x; // x为负时提前返回

    return x; // x非负时返回
}
```  

测验  
**问题1**  
什么是提前返回？其行为表现为何？  
<details><summary>答案</summary>提前返回是函数末尾之前的return语句，将立即结束函数执行返回调用者。</details>  

**问题2**  
质数判断程序实现：  
```cpp
bool isPrime(int x)
{
    if (x == 2) return true;
    else if (x == 3) return true;
    else if (x == 5) return true;
    else if (x == 7) return true;
    return false;
}
```  

**问题3**  
简化函数：  
```cpp
bool isAllowedToTakeFunRide()
{
    return height >= 140.0; // 直接返回条件结果
}
```  

[下一课 4.11 字符](Chapter-4/lesson4.11-chars.md)  
[返回主页](/)  
[上一课 4.9 布尔值](Chapter-4/lesson4.9-boolean-values.md)  