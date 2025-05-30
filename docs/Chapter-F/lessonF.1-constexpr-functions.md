F.1 — 常量表达式函数（Constexpr functions）
=========================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年3月28日，上午9:12（太平洋夏令时）  
2025年2月18日（修改）  

在课程[5.6 — 常量表达式变量（Constexpr variables）](Chapter-5/lesson5.6-constexpr-variables.md)中，我们介绍了`constexpr`关键字，用于创建编译时（符号）常量。同时引入了常量表达式（constant expressions）的概念——即在编译时而非运行时求值的表达式。  

常量表达式的一个挑战在于：普通函数的调用不允许出现在常量表达式中。这意味着在需要常量表达式的场景中无法使用此类函数调用。  

考虑以下程序：  
```
#include <iostream>

int main()
{
    constexpr double radius { 3.0 };
    constexpr double pi { 3.14159265359 };
    constexpr double circumference { 2.0 * radius * pi };
    
    std::cout << "圆的周长为：" << circumference << "\n";
    return 0;    
}
```  
输出结果：  
```
圆的周长为：18.8496
```  
这种为`circumference`设置复杂初始化器的方式并不理想（且需实例化两个辅助变量`radius`和`pi`）。因此我们改用函数实现：  
```
#include <iostream>

double calcCircumference(double radius)
{
    constexpr double pi { 3.14159265359 };
    return 2.0 * pi * radius;
}

int main()
{
    constexpr double circumference { calcCircumference(3.0) }; // 编译错误
    
    std::cout << "圆的周长为：" << circumference << "\n";
    return 0;    
}
```  
此代码更简洁，但无法通过编译。常量表达式变量`circumference`要求其初始化器为常量表达式，而`calcCircumference()`的调用不符合要求。  

本例中可将`circumference`改为非constexpr变量使程序编译。虽然会失去常量表达式的优势，但至少程序可运行。  

然而在C++某些场景中（后续课程将介绍），我们别无选择，必须使用常量表达式。此时虽然希望调用函数，但普通函数无法满足需求。解决方案是什么？  

### 常量表达式函数可在常量表达式中调用  
**常量表达式函数（constexpr function）**是允许在常量表达式中调用的函数。  

将函数声明为constexpr函数只需在函数返回类型前添加`constexpr`关键字。  

> **关键洞察**  
> `constexpr`关键字用于向编译器和其他开发者表明该函数可在常量表达式中使用。  

以下是相同示例的constexpr函数版本：  
```
#include <iostream>

constexpr double calcCircumference(double radius) // 声明为constexpr函数
{
    constexpr double pi { 3.14159265359 };
    return 2.0 * pi * radius;
}

int main()
{
    constexpr double circumference { calcCircumference(3.0) }; // 现在可编译
    
    std::cout << "圆的周长为：" << circumference << "\n";
    return 0;    
}
```  
由于`calcCircumference()`现在是constexpr函数，可在常量表达式（如`circumference`的初始化器）中使用。  

### 常量表达式函数可在编译时求值  
在课程[5.5 — 常量表达式（Constant expressions）](Chapter-5/lesson5.5-constant-expressions.md)中我们强调：在需要常量表达式的上下文（如constexpr变量初始化）中，必须在编译时完成求值。若常量表达式包含constexpr函数调用，则该调用必须在编译时求值。  

上例中，变量`circumference`是constexpr，要求其初始化器为常量表达式。由于`calcCircumference()`是该表达式的一部分，必须在编译时求值。  

当函数调用在编译时求值时，编译器会计算其返回值并替换该函数调用。因此`calcCircumference(3.0)`会被结果值`18.8496`替代。编译器实际编译的是：  
```
#include <iostream>

constexpr double calcCircumference(double radius)
{
    constexpr double pi { 3.14159265359 };
    return 2.0 * pi * radius;
}

int main()
{
    constexpr double circumference { 18.8496 };
    
    std::cout << "圆的周长为：" << circumference << "\n";
    return 0;    
}
```  
要在编译时求值，还需满足两个条件：  
* constexpr函数的调用参数必须在编译时已知（例如是常量表达式）  
* constexpr函数内的所有语句和表达式必须在编译时可求值  

> **进阶阅读**  
> 存在其他较少遇到的条件，详见[此处](https://en.cppreference.com/w/cpp/language/constexpr)。  

### 常量表达式函数也可在运行时求值  
Constexpr函数同样可在运行时求值，此时返回非constexpr结果。例如：  
```
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    int x{ 5 }; // 非constexpr
    int y{ 6 }; // 非constexpr

    std::cout << greater(x, y) << " 更大！\n"; // 在运行时求值
    return 0;
}
```  
此例中，由于参数`x`和`y`非常量表达式，函数无法在编译时解析。但仍会在运行时解析，返回期望值作为非constexpr的`int`类型。  

> **关键洞察**  
> constexpr函数在运行时求值时，行为与普通函数相同。此时`constexpr`关键字不产生实际效果。  
>  
> 允许具有constexpr返回类型的函数在编译时或运行时求值，是为了让单个函数能同时服务两种场景。否则需编写两个函数（分别具有constexpr和非constexpr返回类型），这不仅导致代码重复，两个函数还需不同名称！  

### 为何关注函数在编译时执行？  
现在正是回顾编译时编程技术优势的时机：[5.5 — 常量表达式](constant-expressions/#compiletimebenefits)。  

[下一课 F.2 常量表达式函数（第二部分）](Chapter-F/lessonF.2-constexpr-functions-part-2.md)  
[返回主页](/)  
[上一课 11.x 第11章总结与测验](Chapter-11/lesson11.x-chapter-11-summary-and-quiz.md)