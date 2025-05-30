11.1 — 函数重载简介
============================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年8月3日 PDT时间20:25  
2023年12月28日更新  

考虑以下函数：
```
int add(int x, int y)
{
    return x + y;
}
```
这个简单的函数将两个整数相加并返回整数结果。但如果我们需要一个能计算两个浮点数的加法函数呢？现有的`add()`函数并不适用，因为任何浮点参数都会被转换为整数，导致小数部分丢失。  

一种解决方案是为不同参数类型定义名称略有差异的函数：
```
int addInteger(int x, int y)
{
    return x + y;
}

double addDouble(double x, double y)
{
    return x + y;
}
```
这种方法需要为不同参数类型维护一致的命名规范，记忆各函数名称，并确保调用正确的版本。当需要处理三个整数相加的情况时，管理这些唯一名称会变得非常繁琐。  

函数重载简介  
----------------  

C++提供了优雅的解决方案——**函数重载（function overloading）**。该特性允许创建多个同名函数，只要每个同名函数的参数类型不同（或可通过其他方式区分）。共享同一名称（在相同作用域内）的函数称为**重载函数（overloaded function）**（简称**重载（overload）**）。  

要重载`add()`函数，只需声明接收double参数的版本：
```
double add(double x, double y)
{
    return x + y;
}
```
现在同一作用域内存在两个`add()`版本：
```
int add(int x, int y) // 整数版本
{
    return x + y;
}

double add(double x, double y) // 浮点版本
{
    return x + y;
}

int main()
{
    return 0;
}
```
该程序可以正常编译。虽然表面看起来存在命名冲突，但由于参数类型不同，编译器能区分这些函数，将它们视为共享名称的不同函数。  

> **关键洞察**  
> 只要编译器能区分各个重载函数，函数即可重载。若重载函数无法区分，将产生编译错误。  

相关概念  
----------------  
运算符（operator）也可用类似方式重载，详见课程[21.1 — 运算符重载简介](Chapter-21/lesson21.1-introduction-to-operator-overloading.md)。  

重载解析简介  
----------------  
调用重载函数时，编译器会根据实参类型匹配对应的重载版本，此过程称为**重载解析（overload resolution）**。  

示例演示：
```
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

double add(double x, double y)
{
    return x + y;
}

int main()
{
    std::cout << add(1, 2); // 调用add(int, int)
    std::cout << '\n';
    std::cout << add(1.2, 3.4); // 调用add(double, double)

    return 0;
}
```
程序输出：
```
3
4.6
```
当传入整型参数`add(1, 2)`时，编译器调用`add(int, int)`；传入浮点参数`add(1.2, 3.4)`时，调用`add(double, double)`。  

编译要求  
----------------  
使用重载函数的程序需满足：  
1. 每个重载函数必须能被区分（详见[11.2 — 函数重载的区分](Chapter-11/lesson11.2-function-overload-differentiation.md)）  
2. 每次函数调用必须能解析到具体重载（详见[11.3 — 函数重载解析与二义性匹配](Chapter-11/lesson11.3-function-overload-resolution-and-ambiguous-matches.md)）  

若重载函数无法区分，或函数调用无法解析到具体重载，将导致编译错误。  

结语  
----------------  
函数重载通过减少需记忆的函数名称有效降低程序复杂度，应合理运用。  

> **最佳实践**  
> 使用函数重载简化程序结构。  

[下一课 11.2 函数重载的区分](Chapter-11/lesson11.2-function-overload-differentiation.md)  
[返回主页](/)  
[上一课 10.x 第10章总结与测验](Chapter-10/lesson10.x-chapter-10-summary-and-quiz.md)