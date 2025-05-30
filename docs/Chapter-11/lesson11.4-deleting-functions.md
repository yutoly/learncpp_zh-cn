11.4 — 删除函数  
==========================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年10月10日下午1:26（PDT）  
2023年12月28日  

在某些情况下，使用特定类型的值调用函数时可能导致不符合预期的行为。  

考虑以下示例：  

```cpp
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(5);    // 正常：输出5
    printInt('a');  // 输出97 — 这合理吗？
    printInt(true); // 输出1 — 这合理吗？
    
    return 0;
}
```  

此示例输出：  

```
5
97
1
```  

虽然`printInt(5)`显然合理，但另外两次`printInt()`调用存在疑问。对于`printInt('a')`，编译器会将`'a'`提升为整型值`97`以匹配函数定义。同样会将`true`提升为整型值`1`，且不会给出警告。  

假设我们认为调用`printInt()`时使用`char`或`bool`类型参数没有意义。该如何处理？  

使用`= delete`说明符删除函数  
----------------  

对于明确不希望被调用的函数，可以通过使用**= delete**说明符将其定义为删除函数（deleted function）。若编译器将函数调用匹配到已删除的函数，将停止编译并报错。  

以下是修改后的版本：  

```cpp
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

void printInt(char) = delete; // 调用此函数将终止编译
void printInt(bool) = delete; // 调用此函数将终止编译

int main()
{
    printInt(97);   // 正常

    printInt('a');  // 编译错误：函数已删除
    printInt(true); // 编译错误：函数已删除

    printInt(5.0);  // 编译错误：存在二义性匹配
    
    return 0;
}
```  

分析部分情况：`printInt('a')`直接匹配已删除的`printInt(char)`，导致编译错误。`printInt(true)`直接匹配已删除的`printInt(bool)`，同样报错。  

`printInt(5.0)`的情况值得注意。编译器首先检查是否存在精确匹配的`printInt(double)`函数（不存在）。接着寻找最佳匹配：虽然`printInt(int)`是唯一未删除的函数，但已删除函数仍参与重载解析（overload resolution）。由于没有明确的最佳匹配，编译器将报二义性错误。  

关键洞察  
----------------  

`= delete`表示"禁止此操作"，而非"此函数不存在"。  
已删除函数参与函数重载解析的所有阶段（不仅限于精确匹配阶段）。若选中已删除函数，则产生编译错误。  

面向进阶读者  
----------------  

其他类型的函数也可被删除：  
* 成员函数删除详见课程[14.14 — 拷贝构造函数简介](Chapter-14/lesson14.14-introduction-to-the-copy-constructor.md)  
* 函数模板特化删除详见课程[11.7 — 函数模板实例化](Chapter-11/lesson11.7-function-template-instantiation.md)  

删除所有不匹配的重载（进阶）  
----------------  

逐个删除函数重载可行但较为冗长。若需函数仅在参数类型完全匹配时被调用，可使用函数模板（详见即将学习的[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)）：  

```cpp
#include <iostream>

// 该函数优先处理int类型参数
void printInt(int x)
{
    std::cout << x << '\n';
}

// 该函数模板优先处理其他类型参数
// 由于模板被删除，调用时将终止编译
template <typename T>
void printInt(T x) = delete;

int main()
{
    printInt(97);   // 正常
    printInt('a');  // 编译错误
    printInt(true); // 编译错误
    
    return 0;
}
```  

[下一课 11.5 — 默认参数](Chapter-11/lesson11.5-default-arguments.md)  
[返回主页](/)  
[上一课 11.3 — 函数重载解析与二义性匹配](Chapter-11/lesson11.3-function-overload-resolution-and-ambiguous-matches.md)  