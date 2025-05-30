10.4 — 窄化转换（narrowing conversions）、列表初始化（list initialization）与constexpr初始化器（constexpr initializers）  
==============================================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年5月5日（2024年2月16日修订）  

在前一课程（[10.3 — 数值转换](Chapter-10/lesson10.3-numeric-conversions.md)）中，我们讨论了基础类型间的各类数值转换。  

窄化转换（Narrowing conversions）  
----------------  

在C++中，**窄化转换（narrowing conversion）**是指可能不安全的数值转换，目标类型可能无法容纳源类型的所有值。以下转换被定义为窄化：  
* 浮点类型到整型  
* 浮点类型到更窄或更低等级的浮点类型（除非被转换的值是constexpr且在目标类型范围内）  
* 整型到浮点类型（除非被转换的值是constexpr且可精确存储）  
* 整型到无法表示原类型所有值的其他整型（除非被转换的值是constexpr且可精确存储）  

大多数情况下，隐式窄化转换会导致编译器警告（有符号/无符号转换可能根据编译器配置产生警告）。应尽可能避免窄化转换，因其存在安全隐患。  

> **最佳实践**  
> 由于存在安全隐患和错误风险，应尽量避免窄化转换。  

显式声明窄化转换  
----------------  

虽然应尽量避免，但某些情况（如函数参数类型不匹配）仍需进行窄化转换。此时应使用`static_cast`进行显式转换，既表明意图又可抑制编译器警告：  
```cpp
void someFcn(int i)
{
}

int main()
{
    double d{ 5.0 };
    
    someFcn(d); // 错误做法：隐式窄化转换将产生编译器警告

    // 正确做法：显式声明转换意图
    someFcn(static_cast<int>(d)); // 无警告
    
    return 0;
}
```  

> **最佳实践**  
> 必须进行窄化转换时，使用`static_cast`显式转换。  

列表初始化禁止窄化转换  
----------------  

列表初始化（花括号初始化）禁止窄化转换（这也是推荐使用此形式的原因），尝试操作将导致编译错误：  
```cpp
int main()
{
    int i { 3.5 }; // 编译失败
    
    return 0;
}
```  
Visual Studio报错示例：  
```
error C2397: 从'double'到'int'的转换需要窄化转换
```  
如需在列表初始化中进行窄化转换，应使用`static_cast`：  
```cpp
int main()
{
    double d { 3.5 };

    int i { static_cast<int>(d) }; // 显式转换
    
    return 0;
}
```  

constexpr转换的特殊性  
----------------  

当窄化转换的源值是constexpr时，编译器可检查转换是否保留值。若保留则不视为窄化转换：  
```cpp
#include <iostream>

int main()
{
    constexpr int n1{ 5 };   // constexpr
    unsigned int u1 { n1 };  // 合法：值被保留

    constexpr int n2 { -5 }; // constexpr
    unsigned int u2 { n2 };  // 编译错误：值未保留
    
    return 0;
}
```  
例外情况：  
1. 浮点转整型始终视为窄化  
2. constexpr浮点转更窄浮点类型即使丢失精度也不视为窄化  

> **警告**  
> constexpr浮点类型向更窄浮点类型的转换即使丢失精度也不视为窄化。  

constexpr初始化器的列表初始化  
----------------  

利用constexpr例外条款，可简化非整型/非双精度类型的初始化：  
```cpp
int main()
{
    unsigned int u { 5 }; // 无需使用5u后缀
    float f { 1.5 };      // 无需使用1.5f后缀

    constexpr int n{ 5 };
    double d { n };       // 无需static_cast
    short s { 5 };        // short无后缀也可初始化
    
    return 0;
}
```  
注意：目标浮点类型只要在值范围内即可初始化，即使丢失精度：  
```cpp
int main()
{
    float f { 1.23456789 }; // 合法但丢失精度
    
    return 0;
}
```  
（GCC/Clang使用-Wconversion编译标志时可能产生警告）  

[下一课 10.5 — 算术转换](Chapter-10/lesson10.5-arithmetic-conversions.md)  
[返回主页](/)  
[上一课 10.3 — 数值转换](Chapter-10/lesson10.3-numeric-conversions.md)