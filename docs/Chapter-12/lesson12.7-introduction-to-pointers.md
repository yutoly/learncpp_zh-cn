12.7 — 指针简介  
================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年7月10日 PDT 下午6:52  
2025年2月7日  

指针（pointer）是C++历史上的难点之一，许多学习者在此受阻。但您将发现，指针并不可怕。实际上，指针的行为与左值引用（lvalue reference）高度相似。在深入探讨前，我们先进行基础铺垫。  

**相关预备知识**  
若对左值引用不熟悉，请复习课程：[12.3 — 左值引用](https://www.learncpp.com/cpp-tutorial/lvalue-references/)、[12.4 — 指向常量的左值引用](https://www.learncpp.com/cpp-tutorial/lvalue-references-to-const/) 和 [12.5 — 按左值引用传递](https://www.learncpp.com/cpp-tutorial/pass-by-lvalue-reference/)。  

考虑以下普通变量：  
```
char x {}; // char类型占用1字节内存
```  
简化来说，执行此定义时，系统会从RAM分配一块内存给该对象。假设变量`x`被分配到内存地址`140`。当在表达式或语句中使用`x`时，程序将访问地址`140`获取存储值。  

变量的优势在于无需关注具体内存地址或对象占用的字节数。我们通过标识符引用变量，编译器会将其转换为正确地址。  

引用（reference）同样如此：  
```
int main()
{
    char x {};       // 假设分配至地址140
    char& ref { x }; // ref是x的左值引用（类型后的&表示左值引用）
    return 0;
}
```  
由于`ref`是`x`的别名，使用`ref`时程序仍访问地址`140`。  

### 取地址运算符（&)  
虽然变量地址默认不公开，但可通过**取地址运算符（&）**获取操作数的内存地址：  
```
#include <iostream>
int main()
{
    int x{ 5 };
    std::cout << x << '\n';   // 输出变量x的值
    std::cout << &x << '\n';  // 输出变量x的内存地址
    return 0;
}
```  
上述程序在作者机器输出：  
```
5
0027FEA0
```  
此例中，取地址运算符(&)获取`x`的地址并输出。内存地址通常以十六进制打印（无0x前缀）。对于多字节对象，取地址运算符返回其首字节地址。  

> **符号辨析**  
> &符号在不同上下文有不同含义：  
> * 类型名后：表示左值引用（如`int& ref`)  
> * 表达式中的一元运算：取地址运算符（如`std::cout << &x`)  
> * 表达式中的二元运算：按位与运算符（如`std::cout << x & y`)  

### 解引用运算符（*)  
仅获取地址作用有限。关键是通过地址访问存储值。**解引用运算符（*)**（亦称**间接寻址运算符**）返回给定地址的值（作为左值）：  
```
#include <iostream>
int main()
{
    int x{ 5 };
    std::cout << x << '\n';    // 输出x的值
    std::cout << &x << '\n';   // 输出x的地址
    std::cout << *(&x) << '\n'; // 输出x地址处的值（括号非必需但增强可读性）
    return 0;
}
```  
输出结果：  
```
5
0027FEA0
5
```  
> **核心洞见**  
> 解引用运算符（*）可通过内存地址获取值（作为左值）。取地址运算符（&）与解引用运算符（*）互为逆操作：前者获取对象地址，后者获取地址处的对象。  

> **运算符区分**  
> 解引用运算符（*）虽与乘号同形，但作为一元运算符（乘号为二元运算符）可区分。  

### 指针（pointer)  
**指针（pointer）**是存储*内存地址*（通常为其他变量的地址）的对象。现代C++中，此类指针称**原始指针（raw pointer）**或**哑指针（dumb pointer）**，以区别于后续引入的**智能指针（smart pointer）**（见[第22章](https://www.learncpp.com#Chapter22)）。  

指针类型（如`int*`)通过星号（*）声明：  
```
int;   // 普通int类型
int&;  // int类型的左值引用
int*;  // 指向int值的指针（存储整数值的地址）
```  
创建指针变量：  
```
int main()
{
    int x{ 5 };   // 普通变量
    int& ref{ x };// 整型引用（绑定x）
    int* ptr;     // 整型指针
    return 0;
}
```  
> **最佳实践**  
> 声明指针类型时，星号紧邻类型名。  

> **多变量声明警告**  
> 避免单行声明多个变量。若必须，每个指针变量均需带星号：  
> ```
> int* ptr1, ptr2;   // 错误：ptr1为指针，ptr2为普通int！
> int* ptr3, * ptr4; // 正确：ptr3和ptr4均为指针
> ```  

### 指针初始化  
指针默认不初始化。未初始化的指针称**野指针（wild pointer）**，其包含垃圾地址，解引用会导致未定义行为（undefined behavior）。因此必须初始化指针。  
> **最佳实践**  
> 始终初始化指针。  

```
int main()
{
    int x{ 5 };
    int* ptr;         // 未初始化指针（含垃圾地址）
    int* ptr2{};      // 空指针（下节讨论）
    int* ptr3{ &x };  // 用x地址初始化的指针
    return 0;
}
```  
初始化指针后，通过解引用运算符（*）访问目标值：  
```
#include <iostream>
int main()
{
    int x{ 5 };
    std::cout << x << '\n'; // 输出x的值
    
    int* ptr{ &x };         // ptr存储x的地址
    std::cout << *ptr << '\n'; // 解引用ptr输出x地址处的值
    return 0;
}
```  
输出：  
```
5
5
```  
![](https://www.learncpp.com/images/CppTutorial/Section6/6-Pointer.png)  
指针因此得名——`ptr`存储`x`的地址，故称`ptr`"指向"`x`。  

> **术语说明**  
> "X指针"（如整型指针）即"指向X类型的指针"。  

指针类型需与所指对象类型匹配：  
```
int main()
{
    int i{ 5 };
    double d{ 7.0 };
    int* iPtr{ &i };      // 正确：整型指针可指向int对象
    int* iPtr2{ &d };     // 错误：整型指针不可指向double
    double* dPtr{ &d };   // 正确：double指针可指向double对象
    double* dPtr2{ &i };  // 错误：double指针不可指向int
    return 0;
}
```  
下节将讨论例外情况，但字面值初始化指针通常被禁止：  
```
int* ptr{ 5 };          // 错误
int* ptr{ 0x0012FF7C }; // 错误：0x0012FF7C被视为整数字面值
```  

### 指针与赋值  
指针赋值有两种用途：  
1. 改变指针指向（赋新地址）  
2. 改变所指对象的值（给解引用指针赋新值）  

**案例1：改变指针指向**  
```
#include <iostream>
int main()
{
    int x{ 5 };
    int* ptr{ &x };      // ptr初始指向x
    std::cout << *ptr << '\n'; 

    int y{ 6 };
    ptr = &y;            // ptr改为指向y
    std::cout << *ptr << '\n'; 
    return 0;
}
```  
输出：  
```
5
6
```  

**案例2：改变所指对象值**  
```
#include <iostream>
int main()
{
    int x{ 5 };
    int* ptr{ &x }; 

    std::cout << x << '\n'; 
    std::cout << *ptr << '\n'; 

    *ptr = 6;             // 通过ptr解引用修改x的值
    std::cout << x << '\n'; 
    std::cout << *ptr << '\n'; 
    return 0;
}
```  
输出：  
```
5
5
6
6
```  
> **核心洞见**  
> * 无解引用时（`ptr`），访问指针持有的地址。修改此地址（`ptr = &y`）改变指向目标。  
> * 解引用时（`*ptr`），访问所指对象。修改此值（`*ptr = 6`）改变目标对象值。  

### 指针与左值引用的相似性  
```
#include <iostream>
int main()
{
    int x{ 5 };
    int& ref{ x };   // x的引用
    int* ptr{ &x };  // x的指针

    std::cout << x << ref << *ptr << '\n'; // 输出：555
    ref = 6;                              // 通过引用修改x
    std::cout << x << ref << *ptr << '\n'; // 输出：666
    *ptr = 7;                             // 通过指针修改x
    std::cout << x << ref << *ptr << '\n'; // 输出：777
    return 0;
}
```  
指针与引用均提供间接访问对象的方式，主要区别：  
| 特性         | 引用                     | 指针                     |  
|--------------|--------------------------|--------------------------|  
| 初始化要求   | 必须初始化               | 非必须（但应初始化）     |  
| 对象性质     | 非对象                   | 是对象                   |  
| 重绑定       | 不可重新绑定             | 可改变指向               |  
| 空值         | 必须绑定对象             | 可指向空（下节介绍）     |  
| 安全性       | 较安全（除悬垂引用外）   | 固有风险（下节讨论）     |  

### 技术细节  
**取地址运算符的返回值**  
取地址运算符（&）不返回地址字面值（因C++不支持地址字面值），而是返回指向操作数的指针（其值为操作数地址）。例如变量`int x`，`&x`返回持有`x`地址的`int*`类型指针。验证：  
```
#include <iostream>
#include <typeinfo>
int main()
{
    int x{ 4 };
    std::cout << typeid(x).name() << '\n';   // 输出x的类型
    std::cout << typeid(&x).name() << '\n';  // 输出&x的类型
    return 0;
}
```  
Visual Studio输出：  
```
int
int *
```  
gcc输出`i`（int）和`pi`（指向int的指针）。  

**指针大小**  
指针大小取决于编译目标架构：  
* 32位程序：指针32位（4字节）  
* 64位程序：指针64位（8字节）  
与所指对象大小无关：  
```
#include <iostream>
int main() // 假设为32位程序
{
    char* chPtr{};        // char占1字节
    int* iPtr{};          // int通常占4字节
    long double* ldPtr{}; // long double通常占8/12字节

    std::cout << sizeof(chPtr) << '\n'; // 输出4
    std::cout << sizeof(iPtr) << '\n';  // 输出4
    std::cout << sizeof(ldPtr) << '\n'; // 输出4
    return 0;
}
```  

**悬垂指针（dangling pointer）**  
**悬垂指针**指向已失效的对象（如被销毁的对象）。解引用悬垂指针会导致未定义行为。但标准规定：**对无效指针值的其他操作由实现定义**（如可赋新值`nullptr`），而复制或递增等操作行为由编译器实现决定。  
> **核心洞见**  
> 解引用无效指针导致未定义行为，其他无效指针操作由实现定义。  

悬垂指针示例：  
```
#include <iostream>
int main()
{
    int x{ 5 };
    int* ptr{ &x };
    std::cout << *ptr << '\n'; // 有效

    {
        int y{ 6 };
        ptr = &y;             
        std::cout << *ptr << '\n'; // 有效
    } // y离开作用域，ptr变为悬垂指针

    std::cout << *ptr << '\n'; // 解引用悬垂指针（未定义行为）
    return 0;
}
```  
可能输出（非保证）：  
```
5
6
6
```  

### 总结  
指针是存储内存地址的变量，可通过解引用运算符（*）访问地址处的值。解引用野指针、悬垂指针或空指针（null pointer）会导致未定义行为。指针比引用更灵活也更危险，后续课程将深入探讨。  

### 测验  
**问题1**  
以下程序输出什么？（假设short占2字节，32位机器）  
  
<details><summary>输出</summary>  
```
0012FF60  // &value
7         // value
0012FF60  // ptr
7         // *ptr

0012FF60  // &value
9         // value (由*ptr=9修改)
0012FF60  // ptr
9         // *ptr

0012FF54  // &otherValue
3         // otherValue
0012FF54  // ptr (指向otherValue)
3         // *ptr

4  // sizeof(ptr) 指针大小（32位=4字节）
2  // sizeof(*ptr) 所指short类型大小
```  
</details>  

**问题2**  
以下代码段有何错误？  
```
int v1{ 45 };
int* ptr{ &v1 }; // 用v1地址初始化ptr

int v2{ 78 };
*ptr = &v2;      // 将v2地址赋给ptr所指对象
```  
  
<details><summary>解析</summary>  
最后一行错误：解引用操作`*ptr`获取整数值，但`&v2`返回地址（`int*`类型），无法将地址赋给整数。正确写法应为：  
```
ptr = &v2; // 直接修改指针指向
```  
</details>  

[下一课 12.8 — 空指针](https://www.learncpp.com/cpp-tutorial/null-pointers/)  
[返回目录](/)[上一课 12.6 — 按常量左值引用传递](https://www.learncpp.com/cpp-tutorial/pass-by-const-lvalue-reference/)