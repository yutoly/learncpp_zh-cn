25.5 — 早期绑定与晚期绑定
======================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2024年10月20日（首次发布于2008年2月7日）

本节及下一节中，我们将深入探讨虚函数（virtual functions）的实现机制。虽然这些知识并非有效使用虚函数的必要条件，但仍具启发性。您可将这两节视为选读内容。

程序执行时，从`main()`函数顶部开始顺序执行。遇到函数调用时，执行点跳转至被调用函数的起始位置。CPU如何实现这一过程？

程序编译时，编译器将C++语句转换为若干行机器语言指令。每行机器指令都有唯一的顺序地址。函数同样如此——遇到函数时，其被转换为机器语言并获得下一个可用地址。因此每个函数都有唯一地址。

绑定与调度
----------------

程序中包含众多名称（标识符、关键字等）。每个名称都关联一组属性：例如变量名包含类型、值、内存地址等属性。

以`int x`为例，我们指示编译器将名称`x`与类型`int`关联。后续若出现`x = 5`，编译器可利用此关联进行类型检查以确保赋值有效。

在编程中，**绑定（binding）**是将名称与属性相关联的过程。**函数绑定（function binding）**（或称**方法绑定（method binding）**）是确定函数调用关联哪个函数定义的过程。实际调用已绑定函数的过程称为**调度（dispatching）**。

在C++中，"绑定"一词使用更宽泛（调度通常被视为绑定的一部分）。下文将探讨这些术语在C++中的用法。

术语说明
----------------
"绑定"是多义词。其他语境中可能指：
* 引用（reference）与对象的绑定
* `std::bind`
* 语言绑定（language binding）

早期绑定
----------------
编译器遇到的大多数函数调用属于直接函数调用（direct function call），即直接调用函数的语句。例如：
```cpp
#include <iostream>

struct Foo
{
    void printValue(int value)
    {
        std::cout << value;
    }
};

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    printValue(5);   // 直接调用printValue(int)

    Foo f{};
    f.printValue(5); // 直接调用Foo::printValue(int)
    return 0;
}
```
在C++中，当直接调用非成员函数或非虚成员函数时，编译器可确定调用应匹配的函数定义。此过程称为**早期绑定（early binding）**（或**静态绑定（static binding）**），因其在编译期完成。编译器（或链接器）随后生成机器指令，指示CPU直接跳转至函数地址。

进阶阅读
> 查看调用`printValue(5)`生成的汇编代码（clang x86-64）：
> ```
>         mov     edi, 5           ; 将参数5复制到edi寄存器
>         call    printValue(int)  ; 直接调用printValue(int)
> ```
> 可清晰看出这是对printValue(int)的直接调用。

重载函数和函数模板的调用同样可在编译期解析：
```cpp
#include <iostream>

template <typename T>
void printValue(T value)
{
    std::cout << value << '\n';
}

void printValue(double value)
{
    std::cout << value << '\n';
}

void printValue(int value)
{
    std::cout << value << '\n';
}

int main()
{
    printValue(5);   // 直接调用printValue(int)
    printValue<>(5); // 直接调用printValue<int>(int)
    return 0;
}
```

以下简单计算器程序演示早期绑定的应用：
```cpp
#include <iostream>

int add(int x, int y) { return x + y; }
int subtract(int x, int y) { return x - y; }
int multiply(int x, int y) { return x * y; }

int main()
{
    int x{}, y{}, op{};
    std::cout << "输入数字: "; std::cin >> x;
    std::cout << "输入另一数字: "; std::cin >> y;
    std::cout << "选择操作 (0=加,1=减,2=乘): "; std::cin >> op;

    int result{};
    switch (op) // 通过早期绑定直接调用目标函数
    {
        case 0: result = add(x, y); break;
        case 1: result = subtract(x, y); break;
        case 2: result = multiply(x, y); break;
        default: std::cout << "无效操作符\n"; return 1;
    }
    std::cout << "结果: " << result << '\n';
    return 0;
}
```
由于`add()`, `subtract()`, `multiply()`都是对非成员函数的直接调用，编译器在编译期即可匹配函数定义。

注意：实际调用哪个函数由运行时switch语句决定。但这属于执行路径问题，而非绑定问题。

晚期绑定
----------------
某些情况下，函数调用需延迟到运行时解析。在C++中，此过程称为**晚期绑定（late binding）**（虚函数解析场景下也称**动态调度（dynamic dispatch）**）。

作者注
> 编程术语中，"晚期绑定"通常指无法仅靠静态类型信息确定调用函数，必须借助动态类型信息解析的情况。
> C++中该术语更宽泛，指编译器或链接器在函数调用处无法确定实际调用函数的情况。

在C++中，实现晚期绑定的方式之一是使用函数指针（function pointers）。简言之，函数指针是一种指向函数（而非变量）的指针类型。通过函数指针调用函数时，需对指针使用函数调用运算符`()`。

例如以下代码通过函数指针调用`printValue()`：
```cpp
#include <iostream>

void printValue(int value) { std::cout << value << '\n'; }

int main()
{
    auto fcn { printValue }; // 创建函数指针并指向printValue
    fcn(5);                  // 通过函数指针间接调用printValue
    return 0;
}
```
通过函数指针调用函数也称为间接函数调用（indirect function call）。执行`fcn(5)`时，编译器在编译期无法确定实际调用的函数。相反，在运行时通过函数指针持有的地址进行间接调用。

进阶阅读
> 查看调用`fcn(5)`生成的汇编代码（clang x86-64）：
> ```
>         lea     rax, [rip + printValue(int)] ; 确定printValue地址并存入rax
>         mov     qword ptr [rbp - 8], rax     ; 将rax值存入fcn变量内存
>         mov     edi, 5                       ; 复制参数5到edi寄存器
>         call    qword ptr [rbp - 8]          ; 调用fcn变量地址处的函数
> ```
> 可清晰看出这是通过地址间接调用printValue(int)。

以下计算器程序功能与早期绑定示例相同，但改用函数指针：
```cpp
#include <iostream>

int add(int x, int y) { return x + y; }
int subtract(int x, int y) { return x - y; }
int multiply(int x, int y) { return x * y; }

int main()
{
    int x{}, y{}, op{};
    std::cout << "输入数字: "; std::cin >> x;
    std::cout << "输入另一数字: "; std::cin >> y;
    std::cout << "选择操作 (0=加,1=减,2=乘): "; std::cin >> op;

    using FcnPtr = int (*)(int, int); // 为复杂函数指针类型创建别名
    FcnPtr fcn { nullptr };           // 创建函数指针对象并初始化为空

    switch (op) // 使fcn指向用户选择的函数
    {
        case 0: fcn = add; break;
        case 1: fcn = subtract; break;
        case 2: fcn = multiply; break;
        default: std::cout << "无效操作符\n"; return 1;
    }
    std::cout << "结果: " << fcn(x, y) << '\n'; // 通过指针调用函数
    return 0;
}
```
此例中，我们未直接调用`add()`, `subtract()`或`multiply()`，而是将`fcn`指向目标函数后通过指针调用。

编译器无法使用早期绑定解析`fcn(x, y)`调用，因其在编译期无法确定`fcn`指向的函数！

晚期绑定效率略低，因其涉及额外间接层。早期绑定中CPU可直接跳转至函数地址；晚期绑定则需先读取指针存储的地址再跳转，多出一步操作。但晚期绑定的优势在于灵活性更高，因调用决策可延迟至运行时。

下一节我们将探讨如何利用晚期绑定实现虚函数。

[下一课 25.6 虚函数表](Chapter-25/lesson25.6-the-virtual-table.md)  
[返回主页](/)  
[上一课 25.4 虚析构函数、虚赋值与覆盖虚化](Chapter-25/lesson25.4-virtual-destructors-virtual-assignment-and-overriding-virtualization.md)