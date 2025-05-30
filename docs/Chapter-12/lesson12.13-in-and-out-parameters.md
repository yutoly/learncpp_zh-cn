12.13 — 输入参数与输出参数  
==============================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月9日（首次发布于2023年7月31日）  

函数与调用方通过两种机制进行通信：参数（parameters）和返回值（return values）。调用函数时，调用方提供实参（arguments），函数通过其形参（parameters）接收这些实参。这些实参可通过传值（by value）、传引用（by reference）或传地址（by address）方式传递。  

通常情况下，我们使用传值或传常量引用（const reference）。但在某些情况下可能需要采用其他方式。  

输入参数（In parameters）  
----------------  

大多数情况下，函数参数仅用于接收调用方的输入。专门用于接收输入的参数称为**输入参数（in parameters）**。  
```
#include <iostream>

void print(int x) // x 是输入参数
{
    std::cout << x << '\n';
}

void print(const std::string& s) // s 是输入参数
{
    std::cout << s << '\n';
}

int main()
{
    print(5);
    std::string s { "Hello, world!" };
    print(s);

    return 0;
}
```  
输入参数通常通过传值或传常量引用方式传递。  

输出参数（Out parameters）  
----------------  

通过传非常量引用（non-const reference）或传指向非常量的指针（pointer-to-non-const）传递的实参，允许函数修改调用方的对象值。当返回值不足以满足需求时，这种方式可用于将数据返回给调用方。专门用于返回信息的函数参数称为**输出参数（out parameter）**。  

示例：  
```
#include <cmath>    // 使用 std::sin() 和 std::cos()
#include <iostream>

// sinOut 和 cosOut 是输出参数
void getSinCos(double degrees, double& sinOut, double& cosOut)
{
    // sin() 和 cos() 使用弧度而非角度，需转换
    constexpr double pi { 3.14159265358979323846 }; // π 值
    double radians = degrees * pi / 180.0;
    sinOut = std::sin(radians);
    cosOut = std::cos(radians);
}
 
int main()
{
    double sin { 0.0 };
    double cos { 0.0 };
 
    double degrees{};
    std::cout << "请输入角度：";
    std::cin >> degrees;

    // getSinCos 将计算结果存入 sin 和 cos
    getSinCos(degrees, sin, cos);
 
    std::cout << "正弦值为 " << sin << '\n';
    std::cout << "余弦值为 " << cos << '\n';

    return 0;
}
```  
此函数通过传值方式接收`degrees`参数作为输入，通过引用方式返回两个输出参数。我们将输出参数后缀命名为"out"以明确其用途，这有助于提醒调用方这些参数将被覆盖。按惯例，输出参数通常位于参数列表最右侧。  

详细流程：  
1. `main`函数创建局部变量`sin`和`cos`  
2. 通过引用传递至`getSinCos`函数  
3. `getSinCos`通过引用修改`main`中的实际变量  
4. `main`打印更新后的值  

若采用传值方式，修改的将是副本，变更不会保留。而传引用方式使修改得以持久化。  

> **扩展阅读**  
> [StackOverflow解答](https://stackoverflow.com/a/9779765) 解释了为何非常量左值引用不能绑定到右值/临时对象（类型隐式转换可能导致意外行为）。  

输出参数的语法缺陷  
----------------  

输出参数虽然有效，但存在不足：  

1. 调用方必须实例化（并初始化）对象作为实参，即使不使用这些对象  
2. 这些对象必须可被赋值（不能设为常量）  
3. 无法直接使用临时值或简化表达式  

示例：  
```
#include <iostream>

int getByValue()
{
    return 5;
}

void getByReference(int& x)
{
    x = 5;
}

int main()
{
    // 传值返回
    [[maybe_unused]] int x{ getByValue() }; // 可用于初始化对象
    std::cout << getByValue() << '\n';      // 可在表达式中使用临时返回值

    // 输出参数返回
    int y{};                // 必须预先分配可赋值对象
    getByReference(y);      // 传递至函数进行赋值
    std::cout << y << '\n'; // 之后才能使用该值

    return 0;
}
```  
输出参数的使用语法不够自然。  

传引用输出参数的问题  
----------------  

通过赋值接收返回值时，对象修改是明确的：  
```
x = getByValue(); // 明确 x 将被修改
```  
但对于函数调用：  
```
getSinCos(degrees, sin, cos);
```  
无法直观判断`sin`和`cos`是输出参数。若调用方未意识到参数会被修改，可能导致语义错误。  

使用传地址方式可增加显式性：  
```
void foo1(int x);  // 传值
void foo2(int& x); // 传引用
void foo3(int* x); // 传地址

int main()
{
    int i{};
 
    foo1(i);  // 不能修改 i
    foo2(i);  // 可能修改 i（不明确）
    foo3(&i); // 可能修改 i（较明确）

    int *ptr { &i };
    foo3(ptr); // 可能修改 i（不明确）

    return 0;
}
```  
`foo3(&i)`要求传递地址，提示`i`可能被修改。但`foo3(ptr)`仍不明确，且需处理空指针问题，增加了复杂度。  

> **最佳实践**  
> 除非别无选择，否则避免使用输出参数。  
> 对于必须的输出参数，优先使用传引用方式。  

输入输出参数（In/out parameters）  
----------------  

在极少数情况下，函数可能先使用输出参数的当前值再覆盖它，这种参数称为**输入输出参数（in-out parameter）**。输入输出参数与输出参数具有相同的问题。  

何时使用传非常量引用  
----------------  

若为避免拷贝而传引用，通常应使用常量引用。但在以下情况可考虑传非常量引用：  

1. **输入输出参数**：直接修改原有对象更直观高效  
```
void modifyFoo(Foo& inout)
{
    // 修改 inout
}

int main()
{
    Foo foo{};
    modifyFoo(foo); // 修改 foo 的内容

    return 0;
}
```  
通过良好命名提升可读性。  

2. **返回高拷贝成本对象**：当函数需要返回高开销对象时  
```
void generateExpensiveFoo(Foo& out)
{
    // 修改 out
}

int main()
{
    Foo foo{};
    generateExpensiveFoo(foo); // 直接修改 foo

    return 0;
}
```  

> **高级应用**  
> 典型场景是填充大型C风格数组或`std::array`（元素类型拷贝成本高时）。数组相关内容将在后续章节讨论。  

多数情况下，对象拷贝成本不足以证明使用非常规返回方式的合理性。  

[下一课 12.14 指针、引用与const的类型推导](Chapter-12/lesson12.14-type-deduction-with-pointers-references-and-const.md)  
[返回主页](/)  
[上一课 12.12 返回引用与返回地址](Chapter-12/lesson12.12-return-by-reference-and-return-by-address.md)