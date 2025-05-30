7.1 — 复合语句（块）
===================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年6月18日 下午10:06（PDT）首次发布于 2024年5月18日修订  

**复合语句（compound statement）**（亦称**块（block）**或**块语句（block statement）**）是由*零条或多条语句*组成的代码单元，编译器将其视为单条语句处理。块以`{`符号起始，`}`符号结束，内部包含待执行语句。块可应用于任何允许单条语句的语境，且块末尾无需分号。

编写函数时您已接触过块的示例，因为函数体本身就是一个块：
```cpp
int add(int x, int y)
{ // 块开始
    return x + y;
} // 块结束（无分号）

int main()
{ // 块开始

    // 多条语句
    int value {}; // 这是初始化，不是块
    add(3, 4);

    return 0;

} // 块结束（无分号）
```

块嵌套  
----------------  
尽管函数不能嵌套定义，但块*可以*嵌套于其他块中：
```cpp
int add(int x, int y)
{ // 外层块
    return x + y;
} // 外层块结束

int main()
{ // 外层块

    // 多条语句
    int value {};

    { // 内层/嵌套块
        add(3, 4);
    } // 内层/嵌套块结束

    return 0;

} // 外层块结束
```
嵌套块中的外层块通常称为**外层块（outer block）**，内嵌块称为**内层块（inner block）**或**嵌套块（nested block）**。

条件执行多语句  
----------------  
块最常见的应用场景是与`if语句`配合使用。默认情况下，`if语句`在条件为`true`时执行单条语句。若需在条件满足时执行多条语句，可用语句块替代单条语句。例如：
```cpp
#include <iostream>

int main()
{ // 外层块开始
    std::cout << "输入整数：";
    int value {};
    std::cin >> value;
    
    if (value >= 0)
    { // 嵌套块开始
        std::cout << value << " 是非负整数\n";
        std::cout << "该数的两倍是 " << value * 2 << '\n';
    } // 嵌套块结束
    else
    { // 另一嵌套块开始
        std::cout << value << " 是负整数\n";
        std::cout << "其绝对值为 " << -value << '\n';
    } // 另一嵌套块结束

    return 0;
} // 外层块结束
```
用户输入3时输出：
```
输入整数：3
3 是非负整数
该数的两倍是 6
```
用户输入-4时输出：
```
输入整数：-4
-4 是负整数
其绝对值为 4
```

块嵌套层级  
----------------  
块支持多层嵌套：
```cpp
#include <iostream>

int main()
{ // 块1，层级1
    std::cout << "输入整数：";
    int value {};
    std::cin >> value;
    
    if (value >  0)
    { // 块2，层级2
        if ((value % 2) == 0)
        { // 块3，层级3
            std::cout << value << " 是正偶数\n";
        }
        else
        { // 块4，层级3
            std::cout << value << " 是正奇数\n";
        }
    }

    return 0;
}
```
函数的**嵌套层级（nesting level）**（亦称**嵌套深度（nesting depth）**）指函数中任意位置可进入的最大嵌套块数（含外层块）。上述函数虽含4个块，但嵌套层级为3，因为最多同时处于3个块内。

C++标准要求编译器支持256层嵌套，但部分编译器支持较少（如Visual Studio）。建议将嵌套层级控制在3层以内。如同过长函数需要重构（拆分为小函数），过度嵌套的块也应重构（将最深嵌套块转为独立函数）。

> **最佳实践**  
> 保持函数嵌套层级不超过3层。若需更深嵌套，应考虑将相关代码重构为子函数。



[下一课 7.2 用户定义命名空间与作用域解析运算符](Chapter-7/lesson7.2-user-defined-namespaces-and-the-scope-resolution-operator.md)  
[返回主页](/)  
[上一课 O.4 整数的二进制与十进制转换](Chapter-O/lessonO.4-converting-integers-between-binary-and-decimal-representation.md)