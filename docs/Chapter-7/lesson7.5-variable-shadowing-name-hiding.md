7.5 — 变量遮蔽（名称隐藏）  
=======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2020年1月3日 上午11:01（太平洋标准时间）  
2024年7月18日更新  

每个代码块（block）都定义了自己的作用域区域。当嵌套块中的变量与外层块变量同名时会发生什么？此时，嵌套变量会在两者共同的作用域区域内"遮蔽"外层变量。这种现象称为**名称隐藏（name hiding）**或**变量遮蔽（shadowing）**。  

局部变量遮蔽  
```
#include <iostream>

int main()
{ // 外层块
    int apples { 5 }; // 外层块的 apples 变量

    { // 嵌套块
        // 此处 apples 指向外层块变量
        std::cout << apples << '\n'; // 输出外层块 apples 的值

        int apples{ 0 }; // 在嵌套块作用域定义新 apples 变量

        // 此时 apples 指向嵌套块变量
        // 外层块 apples 被临时遮蔽

        apples = 10; // 该赋值操作作用于嵌套块 apples

        std::cout << apples << '\n'; // 输出嵌套块 apples 的值
    } // 嵌套块 apples 被销毁


    std::cout << apples << '\n'; // 输出外层块 apples 的值

    return 0;
} // 外层块 apples 被销毁
```  
运行该程序将输出：  
```
5
10
5
```  

在上述程序中，首先在外层块声明名为`apples`的变量。该变量在内部块可见（通过输出值`5`可验证）。随后在嵌套块声明同名变量。从声明点到块结束，`apples`名称指向嵌套块变量。  

当赋值`10`给`apples`时，操作对象是嵌套块变量。输出该值（`10`）后，嵌套块结束，其`apples`变量被销毁。外层块`apples`不受影响，通过最终输出`5`可验证。  

若未在嵌套块定义`apples`变量，则`apples`名称仍指向外层块变量：  
```
#include <iostream>

int main()
{ // 外层块
    int apples{5}; // 外层块 apples

    { // 嵌套块
        // apples 指向外层块变量
        std::cout << apples << '\n'; // 输出外层块 apples 的值

        // 本例未定义内部块 apples

        apples = 10; // 操作作用于外层块 apples

        std::cout << apples << '\n'; // 输出外层块 apples 的值
    } // 离开嵌套块后外层块 apples 保留新值

    std::cout << apples << '\n'; // 输出外层块 apples 的值

    return 0;
} // 外层块 apples 被销毁
```  
该程序输出：  
```
5
10
10
```  

在嵌套块内部无法直接访问被遮蔽的外层变量。  

全局变量遮蔽  

类似于局部变量遮蔽，当局部变量与全局变量同名时，局部变量在其作用域内会遮蔽全局变量：  
```
#include <iostream>
int value { 5 }; // 全局变量

void foo()
{
    std::cout << "全局变量 value: " << value << '\n'; // 此处未遮蔽，指向全局 value
}

int main()
{
    int value { 7 }; // 遮蔽全局变量 value（在局部变量作用域内）

    ++value; // 递增局部 value

    std::cout << "局部变量 value: " << value << '\n';

    foo();

    return 0;
} // 局部 value 被销毁
```  
输出结果：  
```
局部变量 value: 8
全局变量 value: 5
```  

由于全局变量属于全局命名空间，可使用无前缀的域解析运算符（::）访问全局变量：  
```
#include <iostream>
int value { 5 }; // 全局变量

int main()
{
    int value { 7 }; // 遮蔽全局变量
    ++value; // 递增局部 value

    --(::value); // 递减全局 value（括号用于可读性）

    std::cout << "局部变量 value: " << value << '\n';
    std::cout << "全局变量 value: " << ::value << '\n';

    return 0;
} // 局部 value 被销毁
```  
输出结果：  
```
局部变量 value: 8
全局变量 value: 4
```  

避免变量遮蔽  

通常应避免局部变量遮蔽，因为这可能导致误用或修改错误变量。部分编译器在检测到变量遮蔽时会发出警告。同理也应避免遮蔽全局变量，可通过为全局变量添加"g\_"前缀来规避。  

**最佳实践**  
避免变量遮蔽。  

GCC用户说明  
GCC和Clang支持`-Wshadow`编译选项，可在变量被遮蔽时生成警告。该选项有多个子类型（`-Wshadow=global`、`-Wshadow=local`和`-Wshadow=compatible-local`），详情参阅[GCC文档](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html)。Visual Studio默认启用此类警告。  

[下一课 7.6 内部链接](Chapter-7/lesson7.6-internal-linkage.md)  
[返回主页](/)  
[上一课 7.4 全局变量简介](Chapter-7/lesson7.4-introduction-to-global-variables.md)