11.3 — 函数重载解析与歧义匹配  
==========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2021年6月17日下午5:44（PDT）  
2025年1月17日  

 

在上一课（[11.2 — 函数重载的区分](Chapter-11/lesson11.2-function-overload-differentiation.md)）中，我们讨论了用于区分重载函数的属性。如果重载函数未能与同名其他重载正确区分，编译器将报错。

然而，仅有一组可区分的重载函数是不够的。当进行函数调用时，编译器还必须确保能找到匹配的函数声明。

对于非重载函数（具有唯一名称的函数），函数调用只能匹配一个可能的函数。该函数要么匹配（或在应用类型转换后匹配），要么不匹配（导致编译错误）。而重载函数可能有多个候选函数。由于函数调用只能解析到一个函数，编译器必须确定哪个重载是最佳匹配。将函数调用与特定重载函数匹配的过程称为**重载解析（overload resolution）**。

当函数参数类型与形参类型完全匹配时，解析过程通常很简单：

```cpp
#include <iostream>

void print(int x)
{
     std::cout << x << '\n';
}

void print(double d)
{
     std::cout << d << '\n';
}

int main()
{
     print(5);   // 5是int，匹配print(int)
     print(6.7); // 6.7是double，匹配print(double)
     return 0;
}
```

但当函数调用实参类型与任何重载函数的形参类型不完全匹配时会发生什么？例如：

```cpp
#include <iostream>

void print(int x)
{
     std::cout << x << '\n';
}

void print(double d)
{
     std::cout << d << '\n';
}

int main()
{
     print('a'); // char不匹配int或double
     print(5L);  // long不匹配int或double
     return 0;
}
```

此时虽然没有精确匹配，但`char`或`long`可以隐式转换为`int`或`double`。但每种情况下应选择何种转换？

本课将探讨编译器如何将函数调用匹配到特定重载函数。

重载函数调用解析
----------------

当调用重载函数时，编译器按步骤确定最佳匹配（下一节详述步骤）。

每个步骤中，编译器对实参应用不同类型的转换。每次转换后，编译器检查是否有重载函数匹配。所有转换检查完成后，可能产生三种结果：

1. 未找到匹配：继续下一步骤
2. 找到唯一匹配：确定为最佳匹配，终止后续步骤
3. 找到多个匹配：产生歧义匹配编译错误

若整个步骤序列结束仍未找到匹配，编译器报错"未找到匹配的重载函数"。

参数匹配顺序
------------

**步骤1**：编译器尝试精确匹配，分为两个阶段。首先检查实参类型与重载函数形参完全匹配的情况：

```cpp
void foo(int) {}
void foo(double) {}

int main()
{
    foo(0);   // 精确匹配foo(int)
    foo(3.4); // 精确匹配foo(double)
    return 0;
}
```

其次应用**平凡转换（trivial conversions）**：
- 左值到右值转换
- 限定符转换（如非const转const）
- 非引用到引用转换

例如：
```cpp
void foo(const int) {}
void foo(const double&) {}

int main()
{
    int x{1};
    foo(x); // x平凡转换为const int
    
    double d{2.3};
    foo(d); // d转换为const double&
    return 0;
}
```

**步骤2**：若无精确匹配，尝试数值提升（numeric promotion）。例如：
```cpp
void foo(int) {}
void foo(double) {}

int main()
{
    foo('a');  // char提升为int
    foo(true); // bool提升为int
    foo(4.5f); // float提升为double
    return 0;
}
```

**步骤3**：若无提升匹配，尝试数值转换（numeric conversion）。例如：
```cpp
#include <string>
void foo(double) {}
void foo(std::string) {}

int main()
{
    foo('a'); // char转换为double
    return 0;
}
```

**步骤4**：若无数值转换匹配，尝试用户定义转换（user-defined conversion）。例如：
```cpp
class X {
public:
    operator int() { return 0; }
};

void foo(int) {}
void foo(double) {}

int main()
{
    X x;
    foo(x); // 用户定义转换X→int
    return 0;
}
```

**步骤5**：尝试匹配使用省略号（ellipsis）的函数。

**步骤6**：若以上步骤均失败，报编译错误。

歧义匹配
--------

当编译器在同一步骤找到多个匹配时，产生**歧义匹配（ambiguous match）**。例如：
```cpp
void foo(int) {}
void foo(double) {}

int main()
{
    foo(5L); // long可转int或double
    return 0;
}
```
错误信息示例：
```
错误 C2668: 'foo': 对重载函数的调用不明确
可能是 'void foo(double)'
或       'void foo(int)'
```

解决方法：
1. 定义精确匹配的新重载
2. 显式类型转换：
```cpp
foo(static_cast<unsigned int>(x));
```
3. 使用字面量后缀：
```cpp
foo(0u); // 无符号整型字面量
```

多参数匹配
----------
当函数有多个参数时，编译器对每个参数独立应用匹配规则。最佳函数需至少有一个参数匹配优于其他候选，其余参数匹配不劣于其他候选。例如：
```cpp
void print(char, int) { /*...*/ }
void print(char, double) { /*...*/ }
void print(char, float) { /*...*/ }

int main()
{
    print('x', 'a'); // 第二个参数提升为int
    return 0;
}
```
此例选择`print(char, int)`，因第二个参数提升优于转换。

[下一课 11.4 — 删除函数](Chapter-11/lesson11.4-deleting-functions.md)  
[返回主页](/)  
[上一课 11.2 — 函数重载的区分](Chapter-11/lesson11.2-function-overload-differentiation.md)