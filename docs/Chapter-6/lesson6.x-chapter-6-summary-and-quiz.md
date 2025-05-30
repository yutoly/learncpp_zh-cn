6.x — 第6章总结与测验  
=================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2011年9月11日，太平洋夏令时下午5:02  
2024年12月2日修订  

本章要点回顾  
----------------  
若运算符优先级存在疑问或可能引发混淆，始终使用括号明确优先级。  
算术运算符的行为与常规数学运算一致。取模运算符（%）返回整数除法的余数。  
递增和递减运算符可便捷地增减数值。尽可能避免使用这些运算符的后缀版本。  
警惕副作用（side effects），尤其在函数参数求值顺序方面。避免在单条语句中多次使用带有副作用的变量。  
逗号运算符可将多条语句压缩为一条。但通常更推荐分开书写语句。  
**条件运算符（conditional operator）**（`?:`）（有时也称**算术if运算符**）是三元运算符（接受三个操作数）。对于`c ? x : y`形式：若条件`c`求值为`true`则执行`x`，否则执行`y`。条件运算符通常需要按以下方式加括号：  
* 在复合表达式（含其他运算符的表达式）中使用时，整个条件运算符需加括号  
* 为提升可读性，若条件含运算符（函数调用运算符除外）则需加括号  

关系运算符可用于浮点数比较。但慎用浮点数的相等性（equality）和不等性（inequality）判断。  
逻辑运算符允许构建复合条件语句。  

编程测验  
----------------  
补全以下程序：  
```
#include <iostream>

// 在此处编写 getQuantityPhrase() 函数

// 在此处编写 getApplesPluralized() 函数

int main()
{
    constexpr int maryApples { 3 };
    std::cout << "Mary has " << getQuantityPhrase(maryApples) << ' ' << getApplesPluralized(maryApples) << ".\n";

    std::cout << "How many apples do you have? ";
    int numApples{};
    std::cin >> numApples;

    std::cout << "You have " << getQuantityPhrase(numApples) << ' ' << getApplesPluralized(numApples) << ".\n";
 
    return 0;
}
```  
样例输出：  
```
Mary has a few apples.
How many apples do you have? 1
You have a single apple.
```  
`getQuantityPhrase()`应接收表示物品数量的int参数，返回以下描述符：  
* \< 0 \= "负数（negative）"  
* 0 \= "无（no）"  
* 1 \= "单个（a single）"  
* 2 \= "一对（a couple of）"  
* 3 \= "一些（a few）"  
* \> 3 \= "许多（many）"  

`getApplesPluralized()`应接收表示苹果数量的int参数，返回以下值：  
* 1 \= "apple"（单数形式）  
* 其他数量 \= "apples"（复数形式）  

此函数需使用条件运算符。[查看提示](javascript:void(0))  
提示：函数中返回C风格字符串字面量作为`std::string_view`是可行的。  
```
#include <iostream>
#include <string_view>

std::string_view getQuantityPhrase(int num)
{
    if (num < 0)
        return "negative";
    if (num == 0)
        return "no";
    if (num == 1)
        return "a single";
    if (num == 2)
        return "a couple of";
    if (num == 3)
        return "a few";
    return "many";
}

std::string_view getApplesPluralized(int num)
{
    return (num == 1) ? "apple" : "apples";
}

int main()
{
    constexpr int maryApples { 3 };
    std::cout << "Mary has " << getQuantityPhrase(maryApples) << ' ' << getApplesPluralized(maryApples) << ".\n";

    std::cout << "How many apples do you have? ";
    int numApples{};
    std::cin >> numApples;

    std::cout << "You have " << getQuantityPhrase(numApples) << ' ' << getApplesPluralized(numApples) << ".\n";
 
    return 0;
}
```  

[下一课 O.1 — 位标志与通过std::bitset进行位操作](Chapter-O/lessonO.1-bit-flags-and-bit-manipulation-via-stdbitset.md)  
[返回主页](/)  
[上一课 6.8 — 逻辑运算符](Chapter-6/lesson6.8-logical-operators.md)