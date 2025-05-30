12.6 — 常量左值引用传参  
======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月21日（首次发布于2023年7月26日）  

与非常量引用（只能绑定到可修改左值）不同，常量引用可以绑定到可修改左值、不可修改左值和右值。因此，若将引用参数设为常量，就能绑定任意类型的实参：  

```cpp
#include <iostream>

void printRef(const int& y) // y 是常量引用
{
    std::cout << y << '\n';
}

int main()
{
    int x { 5 };
    printRef(x);   // 正确：x 是可修改左值，y 绑定到 x

    const int z { 5 };
    printRef(z);   // 正确：z 是不可修改左值，y 绑定到 z

    printRef(5);   // 正确：5 是右值字面量，y 绑定到临时 int 对象

    return 0;
}
```

通过常量引用传参与非常量引用传参具有相同的主要优势（避免拷贝实参），同时确保函数*无法*修改被引用的值。  

例如以下代码被禁止，因为`ref`是常量：  

```cpp
void addOne(const int& ref)
{
    ++ref; // 不允许：ref 是常量
}
```

多数情况下，我们不希望函数修改实参值。  

**最佳实践**  
优先使用常量引用传参，除非有特定理由需要非常量引用（例如函数需要修改实参值）。  

现在我们可以理解允许常量左值引用绑定右值的动机：若没有此能力，就无法将字面量（或其他右值）传递给使用引用传参的函数！  

将不同类型实参传递给常量左值引用参数  
----------------  
在课程[12.4 — 常量左值引用](Chapter-12/lesson12.4-lvalue-references-to-const.md)中，我们提到只要值可转换到引用类型，常量左值引用就能绑定不同类型的值。转换会创建临时对象供引用参数绑定。  

主要动机是使传递实参到值参数或常量引用参数的方式完全相同：  

```cpp
#include <iostream>

void printVal(double d)
{
    std::cout << d << '\n';
}

void printRef(const double& d)
{
    std::cout << d << '\n';
}

int main()
{
    printVal(5); // 5 转换为临时 double，拷贝到参数 d
    printRef(5); // 5 转换为临时 double，绑定到参数 d
    
    return 0;
}
```

对于值传参，我们预期会发生拷贝，因此若先转换（导致额外拷贝）通常不成问题（编译器可能会优化掉其中一次拷贝）。  

但当我们*不希望*拷贝时，常使用引用传参。若先进行转换，通常会导致（可能昂贵的）拷贝，这可能不够理想。  

**警告**  
使用引用传参时，确保实参类型与引用类型匹配，否则会导致意外（且可能昂贵的）转换。  

混合值传参与引用传参  
----------------  
具有多个参数的函数可单独决定每个参数采用值传递还是引用传递。  

例如：  

```cpp
#include <string>

void foo(int a, int& b, const std::string& c)
{
}

int main()
{
    int x { 5 };
    const std::string s { "Hello, world!" };

    foo(5, x, s);

    return 0;
}
```

上例中，第一个参数是值传递，第二个是引用传递，第三个是常量引用传递。  

何时使用值传递 vs 引用传递  
----------------  
对于大多数 C++ 初学者，选择值传递还是引用传递并不明显。幸运的是，有个简单的经验法则适用于多数情况：  

* 基础类型和枚举类型拷贝成本低，通常使用值传递  
* 类类型拷贝成本高（有时非常显著），通常使用常量引用传递  

**最佳实践**  
作为经验法则，基础类型用值传递，类类型用常量引用传递。  

若不确定如何选择，优先使用常量引用传递，这样更不易出现意外行为。  

**提示**  
以下是其他值得注意的情况：  

以下类型通常值传递（更高效）：  
* 枚举类型（无作用域和有作用域）  
* 视图和跨度（如`std::string_view`、`std::span`）  
* 模拟引用或（非拥有）指针的类型（如迭代器、`std::reference_wrapper`）  
* 具有值语义且拷贝成本低的类类型（如元素为基础类型的`std::pair`、`std::optional`、`std::expected`）  

以下情况应使用引用传递：  
* 需要被函数修改的实参  
* 不可拷贝的类型（如`std::ostream`）  
* 拷贝涉及需要避免的所有权问题的类型（如`std::unique_ptr`、`std::shared_ptr`）  
* 具有虚函数或可能被继承的类型（因对象切片问题，详见课程[25.9 — 对象切片](Chapter-25/lesson25.9-object-slicing.md)）  

值传递 vs 引用传递的成本（高级）  
----------------  
并非所有类类型都需要引用传递（如通常值传递的`std::string_view`）。您可能疑惑为何不全部使用引用传递。本节（可选阅读）讨论值传递与引用传递的成本，并完善最佳实践。  

首先考虑函数参数初始化的成本。值传递的初始化意味着拷贝。拷贝对象的成本通常与两个因素相关：  
* 对象大小：占用更多内存的对象拷贝耗时更长  
* 额外设置成本：某些类类型实例化时有额外设置（如打开文件或数据库，分配动态内存）。每次拷贝对象都需支付这些成本  

另一方面，绑定引用到对象总是快速的（与拷贝基础类型速度相当）。  

其次考虑使用函数参数的成本。设置函数调用时，编译器可能优化将引用或小尺寸的值传递实参放入CPU寄存器（访问快）而非RAM（访问慢）。  

每次使用值参数时，程序直接访问拷贝实参的存储位置（CPU寄存器或RAM）。但使用引用参数时，程序必须先访问引用分配的存储位置（CPU寄存器或RAM）以确定被引用对象，再访问被引用对象的存储位置（RAM）。  

因此，每次值参数使用是单次CPU寄存器或RAM访问，而引用参数使用是单次访问加第二次RAM访问。  

第三，编译器有时能比引用传递更优化值传递的代码。特别是当存在**别名**（多个指针/引用访问同一对象）时，优化器需保守处理。值传递产生实参拷贝，无别名可能，允许优化器更积极。  

现在可以回答为何不全部使用引用传递：  
* 对于拷贝成本低的对象，拷贝成本与绑定相当，但访问更快且编译器优化更好  
* 对于拷贝成本高的对象，拷贝成本主导其他性能因素  

最后的问题是如何定义"低成本拷贝"。这因编译器、用例和架构而异，但可形成经验法则：若对象占用不超过两个"字"（字长近似内存地址大小）且无设置成本，则属低成本拷贝。  

以下程序定义了判断类型（或对象）是否低成本拷贝的函数式宏：  

```cpp
#include <iostream>

// 判断类型（或对象）是否小于等于两个内存地址大小的函数式宏
#define isSmall(T) (sizeof(T) <= 2 * sizeof(void*))

struct S
{
    double a;
    double b;
    double c;
};

int main()
{
    std::cout << std::boolalpha; // 输出 true/false 而非 1/0
    std::cout << isSmall(int) << '\n'; // true

    double d {};
    std::cout << isSmall(d) << '\n'; // true
    std::cout << isSmall(S) << '\n'; // false

    return 0;
}
```

**旁注**  
此处使用预处理函数式宏，以便接受对象或类型名作为参数（C++函数不允许传递类型作为参数）。  

但类类型对象是否有设置成本难以知晓。除非明确知道无设置成本，否则应假定标准库类多数有设置成本。  

**提示**  
若`sizeof(T) <= 2 * sizeof(void*)`且无额外设置成本，则类型T的对象属低成本拷贝。  

多数情况下优先使用`std::string_view`而非`const std::string&`  
----------------  
现代C++中常见问题：函数字符串参数类型应为`const std::string&`还是`std::string_view`？  

多数情况下`std::string_view`更优，因其能高效处理更广的实参类型。`std::string_view`参数还允许传递子串而无需先拷贝到独立字符串。  

```cpp
void doSomething(const std::string&);
void doSomething(std::string_view);   // 多数情况优选
```

少数情况`const std::string&`可能更合适：  
* 使用C++14或更早版本时（无`std::string_view`）  
* 函数需调用接受C风格字符串或`std::string`参数的函数时，因`std::string_view`不保证空终止（C风格字符串函数所需）且转换回`std::string`效率低  

**最佳实践**  
优先使用`std::string_view`（值传递）而非`const std::string&`，除非函数需调用要求C风格字符串或`std::string`参数的函数。  

为何`std::string_view`参数比`const std::string&`更高效（高级）  
----------------  
C++中字符串实参通常为`std::string`、`std::string_view`或C风格字符串/字面量。  

注意：  
* 若实参类型与形参不匹配，编译器尝试隐式转换  
* 转换值会创建转换类型的临时对象  
* 创建（或拷贝）`std::string_view`成本低，因其不拷贝原字符串  
* 创建（或拷贝）`std::string`成本高，因每个`std::string`对象拷贝字符串  

下表展示传递各类型时的情况：  

| 实参类型          | std::string_view参数        | const std::string&参数       |
|-------------------|-----------------------------|-----------------------------|
| std::string       | 低成本转换                  | 低成本引用绑定              |
| std::string_view  | 低成本拷贝                  | 显式转换为`std::string`成本高 |
| C风格字符串/字面量 | 低成本转换                  | 转换成本高                  |  

使用`std::string_view`值参数时：  
* 传递`std::string`实参：编译器转换为`std::string_view`（低成本）  
* 传递`std::string_view`实参：拷贝参数（低成本）  
* 传递C风格字符串或字面量：转换为`std::string_view`（低成本）  

`std::string_view`能低成本处理所有三种情况。  

使用`const std::string&`引用参数时：  
* 传递`std::string`实参：引用绑定（低成本）  
* 传递`std::string_view`实参：编译器拒绝隐式转换，产生编译错误。显式转换（`static_cast`）成本高  
* 传递C风格字符串或字面量：隐式转换为`std::string`成本高  

因此，`const std::string&`参数仅能低成本处理`std::string`实参。  

代码示例：  

```cpp
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view sv)
{
    std::cout << sv << '\n';
}

void printS(const std::string& s)
{
    std::cout << s << '\n';
}

int main()
{
    std::string s{ "Hello, world" };
    std::string_view sv { s };

    // 传递给 std::string_view 参数
    printSV(s);              // 正确：std::string 到 std::string_view 的低成本转换
    printSV(sv);             // 正确：std::string_view 的低成本拷贝
    printSV("Hello, world"); // 正确：C风格字面量到 std::string_view 的低成本转换

    // 传递给 const std::string& 参数
    printS(s);              // 正确：std::string 实参的低成本绑定
    printS(sv);             // 编译错误：无法隐式转换 std::string_view 到 std::string
    printS(static_cast<std::string>(sv)); // 不佳：创建昂贵的 std::string 临时对象
    printS("Hello, world"); // 不佳：创建昂贵的 std::string 临时对象

    return 0;
}
```

此外，需考虑函数内访问参数的成本。因`std::string_view`参数是普通对象，可直接访问被查看的字符串。访问`std::string&`参数需先获取引用对象。  

最后，若需传递现有字符串的子串，创建`std::string_view`子串成本低，可廉价传递给`std::string_view`参数。而将子串传递给`const std::string&`更昂贵，因子串需拷贝到引用参数绑定的`std::string`中。  

[下一课 12.7 — 指针简介](Chapter-12/lesson12.7-introduction-to-pointers.md)  
[返回主页](/)  
[上一课 12.5 — 左值引用传参](Chapter-12/lesson12.5-pass-by-lvalue-reference.md)