4.9 — 布尔值  
=====================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月4日（首次发布于2007年6月9日）  

现实世界中，我们经常提出或面对可以用"是"或"否"回答的问题。例如："苹果是水果吗？" 是。"你喜欢芦笋吗？" 否。  

类似的陈述可以用"真（true）"或"假（false）"回答："苹果属于水果"显然为真，而"我喜欢芦笋"绝对为假（难吃！）。  

这种只有两种结果（是/真 或 否/假）的陈述非常普遍，因此许多编程语言引入了专门处理它们的类型——**布尔（Boolean）类型**（注：英语中"Boolean"首字母大写，因其得名于发明者乔治·布尔）。  

布尔变量  
----------------  

布尔变量是只能取两个可能值的变量：`true`和`false`。  

声明布尔变量时使用关键字`bool`：  
```cpp
bool b;
```  

初始化或赋值时使用关键字`true`和`false`：  
```cpp
bool b1 { true };
bool b2 { false };
b1 = false;
bool b3 {}; // 默认初始化为 false
```  

类似于一元负号运算符（-）可使整数变为负数，逻辑非运算符（!）可翻转布尔值：  
```cpp
bool b1 { !true };  // b1 初始化为 false
bool b2 { !false }; // b2 初始化为 true
```  

布尔值在内存中并非存储为"true"或"false"文本，而是作为整数值：`true`存为`1`，`false`存为`0`。布尔值在运算时也对应`0`（假）或`1`（真）。因此布尔类型属于整数类型。  

打印布尔值  
----------------  

使用`std::cout`打印布尔值时，默认输出`0`（false）和`1`（true）：  
```cpp
#include <iostream>

int main()
{
    std::cout << true << '\n';  // 输出 1
    std::cout << !true << '\n'; // 输出 0

    bool b {false};
    std::cout << b << '\n';  // 输出 0
    std::cout << !b << '\n'; // 输出 1
    return 0;
}
```  
输出结果：  
```
1
0
0
1
```  

使用std::boolalpha打印true/false  
----------------  

要让`std::cout`输出"true"/"false"而非0/1，需使用`std::boolalpha`（该操作符不直接输出内容，而是改变布尔值的显示方式）：  
```cpp
#include <iostream>

int main()
{
    std::cout << true << '\n';
    std::cout << false << '\n';

    std::cout << std::boolalpha; // 启用布尔文本显示

    std::cout << true << '\n';
    std::cout << false << '\n';
    return 0;
}
```  
输出结果：  
```
1
0
true
false
```  
使用`std::noboolalpha`可恢复默认显示方式。  

整数到布尔值的转换  
----------------  

使用统一初始化时，可用整数字面量`0`（对应false）和`1`（对应true）初始化布尔变量（但建议直接使用`false`/`true`）：  
```cpp
#include <iostream>

int main()
{
    bool bFalse { 0 }; // 正确：初始化为 false
    bool bTrue  { 1 }; // 正确：初始化为 true
    bool bNo    { 2 }; // 错误：禁止窄化转换

    std::cout << bFalse << bTrue << bNo << '\n';
    return 0;
}
```  

在允许整数转布尔值的上下文中，`0`转为`false`，其他整数转为`true`：  
```cpp
#include <iostream>

int main()
{
    std::cout << std::boolalpha;

    bool b1 = 4; // 拷贝初始化允许隐式转换
    std::cout << b1 << '\n'; // 输出 true

    bool b2 = 0; 
    std::cout << b2 << '\n'; // 输出 false
    return 0;
}
```  
输出结果：  
```
true
false
```  
注：`bool b1 = 4;`可能产生警告，需关闭"警告视为错误"选项才能编译。  

输入布尔值  
----------------  

使用`std::cin`输入布尔值时需注意：默认只接受`0`（false）和`1`（true）。其他数值会被视为`true`并触发失败模式，非数值输入会被视为`false`：  
```cpp
#include <iostream>

int main()
{
    bool b{}; // 默认初始化为 false
    std::cout << "请输入布尔值：";
    std::cin >> b;
    std::cout << "你输入的是：" << b << '\n';
    return 0;
}
```  
若输入"true"，程序输出：  
```
你输入的是：0
```  

要允许输入"true"/"false"，需先设置`std::boolalpha`：  
```cpp
#include <iostream>

int main()
{
    bool b{};
    std::cout << "请输入布尔值：";

    std::cin >> std::boolalpha; // 启用布尔文本输入
    std::cin >> b;

    std::cout << std::boolalpha;
    std::cout << "你输入的是：" << b << '\n';
    return 0;
}
```  
警告：启用`std::boolalpha`后，仅接受全小写的"true"/"false"，不再接受`0`/`1`。  

布尔返回值  
----------------  

布尔值常用于返回判断结果的函数，这类函数通常以is（如isEqual）或has（如hasCommonDivisor）开头：  
```cpp
#include <iostream>

// 当x等于y时返回true
bool isEqual(int x, int y)
{
    return x == y; // ==运算符返回布尔值
}

int main()
{
    std::cout << "输入整数：";
    int x{};
    std::cin >> x;

    std::cout << "输入另一整数：";
    int y{};
    std::cin >> y;

    std::cout << std::boolalpha;    
    std::cout << x << "和" << y << "相等吗？";
    std::cout << isEqual(x, y) << '\n';
    return 0;
}
```  
运行示例1：  
```
输入整数：5
输入另一整数：5
5和5相等吗？true
```  
运行示例2：  
```
输入整数：6
输入另一整数：4
6和4相等吗？false
```  

布尔值看似简单，但却是C++语言的核心组成部分，其使用频率超过其他基础类型总和！下一课我们将深入探讨布尔值的应用。  

[下一课 4.10 — if语句简介](Chapter-4/lesson4.10-introduction-to-if-statements.md)  
[返回主页](/)  
[上一课 4.8 — 浮点数](Chapter-4/lesson4.8-floating-point-numbers.md)