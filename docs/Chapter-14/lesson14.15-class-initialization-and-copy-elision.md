14.15 — 类初始化与拷贝省略（copy elision）  
==============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月14日（首次发布于2016年6月5日）  

回顾课程[1.4 — 变量赋值与初始化](Chapter-1/lesson1.4-variable-assignment-and-initialization.md)，我们讨论过基础类型的6种初始化方式：  

```cpp
int a;         // 无初始化器（默认初始化）
int b = 5;     // 等号后接初始化器（拷贝初始化）
int c(6);      // 括号包裹初始化器（直接初始化）

// 列表初始化方法（C++11）
int d{7};      // 大括号包裹初始化器（直接列表初始化）
int e = {8};   // 等号后接大括号初始化器（拷贝列表初始化）
int f{};       // 空大括号初始化器（值初始化）
```

这些初始化方式同样适用于类类型：  

```cpp
#include <iostream>

class Foo
{
public:
    // 默认构造函数
    Foo()
    {
        std::cout << "Foo()\n";
    }

    // 普通构造函数
    Foo(int x)
    {
        std::cout << "Foo(int) " << x << '\n';
    }

    // 拷贝构造函数
    Foo(const Foo&)
    {
        std::cout << "Foo(const Foo&)\n";
    }
};

int main()
{
    // 调用Foo()默认构造函数
    Foo f1;           // 默认初始化
    Foo f2{};         // 值初始化（推荐）
    
    // 调用Foo(int)普通构造函数
    Foo f3 = 3;       // 拷贝初始化（仅限非显式构造函数）
    Foo f4(4);        // 直接初始化
    Foo f5{5};        // 直接列表初始化（推荐）
    Foo f6 = {6};     // 拷贝列表初始化（仅限非显式构造函数）

    // 调用Foo(const Foo&)拷贝构造函数
    Foo f7 = f3;      // 拷贝初始化
    Foo f8(f3);       // 直接初始化
    Foo f9{f3};       // 直接列表初始化（推荐）
    Foo f10 = {f3};   // 拷贝列表初始化

    return 0;
}
```

在现代C++中，拷贝初始化、直接初始化和列表初始化本质上执行相同操作——初始化对象。  

对于所有初始化形式：  
* 初始化类类型时，将检查该类的构造函数集合，并通过重载决议确定最佳匹配的构造函数（可能涉及参数的隐式转换）  
* 初始化非类类型时，使用隐式转换规则判断是否存在隐式转换  

关键洞察  
初始化形式间的三个关键区别：  
1. 列表初始化禁止窄化转换  
2. 拷贝初始化仅考虑非显式构造函数（non-explicit constructors）/转换函数（详见[14.16 — 转换构造函数与explicit关键字](Chapter-14/lesson14.16-converting-constructors-and-the-explicit-keyword.md)）  
3. 列表初始化优先匹配列表构造函数（详见[16.2 — std::vector简介与列表构造函数](Chapter-16/lesson16.2-introduction-to-stdvector-and-list-constructors.md)）  

注意在某些情况下（如构造函数成员初始化列表），只能使用直接初始化形式，不能使用拷贝初始化。  

不必要的拷贝  
考虑以下程序：  

```cpp
#include <iostream>

class Something
{
    int m_x{};

public:
    Something(int x)
        : m_x{x}
    {
        std::cout << "普通构造函数\n";
    }

    Something(const Something& s)
        : m_x{s.m_x}
    {
        std::cout << "拷贝构造函数\n";
    }

    void print() const { std::cout << "Something(" << m_x << ")\n"; }
};

int main()
{
    Something s{ Something{5} }; // 重点观察此行
    s.print();

    return 0;
}
```

变量`s`的初始化过程中，首先构造临时`Something`对象（使用`Something(int)`构造函数），然后用此临时对象初始化`s`。由于两者类型相同，通常会调用`Something(const Something&)`拷贝构造函数。最终`s`被初始化为5。  

未优化时程序输出：  
```
普通构造函数
拷贝构造函数
Something(5)
```

但此程序效率低下，因为需要两次构造函数调用。更高效的写法：  
```cpp
Something s{5}; // 仅调用Something(int)
```

拷贝省略（copy elision）  
编译器可能优化掉不必要的拷贝，将`Something s{ Something{5} };`视为`Something s{5}`。这种优化技术称为**拷贝省略**，即编译器移除不必要的对象拷贝操作。当拷贝构造函数被优化掉时，我们称该构造函数被**省略（elided）**。  

与其他优化不同，拷贝省略豁免于"as-if"规则。即使拷贝构造函数有副作用（如输出文本），编译器仍可省略它！因此拷贝构造函数不应包含除拷贝外的副作用——若被省略，副作用将不会执行！  

相关概念  
"as-if"规则详见课程[5.4 — as-if规则与编译期优化](Chapter-5/lesson5.4-the-as-if-rule-and-compile-time-optimization.md)。  

在C++17编译器上运行示例程序，输出为：  
```
普通构造函数
Something(5)
```

拷贝构造函数调用被省略，导致"拷贝构造函数"的打印语句未执行！  

值传递与值返回时的拷贝省略  
拷贝构造函数通常用于按值传递参数或返回值时。但在某些情况下，这些拷贝可能被省略。示例程序：  

```cpp
#include <iostream>

class Something
{
public:
    Something() = default;
    Something(const Something&)
    {
        std::cout << "拷贝构造函数被调用\n";
    }
};

Something rvo()
{
    return Something{}; // 调用Something()和拷贝构造函数
}

Something nrvo()
{
    Something s{}; // 调用Something()
    return s;      // 调用拷贝构造函数
}

int main()
{
    std::cout << "初始化s1\n";
    Something s1{rvo()}; // 调用拷贝构造函数

    std::cout << "初始化s2\n";
    Something s2{nrvo()}; // 调用拷贝构造函数

    return 0;
}
```

在禁用拷贝省略的C++14或更早标准中，可能调用4次拷贝构造函数。但实际编译器可能省略多数或全部调用。无需记忆具体省略情况，只需了解这是编译器的优化行为。  

C++17中的强制拷贝省略  
C++17起，某些情况下的拷贝省略变为强制要求。对于上述示例：  
* `rvo()`返回值和`s1`初始化时的拷贝调用必须被省略  
* `s2`初始化时的拷贝省略取决于编译器和优化设置  

在可选省略情况下，即使实际调用被省略，拷贝构造函数仍需可访问（例如未删除）。在强制省略情况下，即使拷贝构造函数被删除，仍可进行省略。  

进阶阅读  
在可选拷贝省略未执行时，移动语义（move semantics）可能允许对象被移动而非拷贝（详见[16.5 — 返回std::vector与移动语义简介](Chapter-16/lesson16.5-returning-stdvector-and-an-introduction-to-move-semantics.md)）。  

[下一课 14.16 转换构造函数与explicit关键字](Chapter-14/lesson14.16-converting-constructors-and-the-explicit-keyword.md)  
[返回主页](/)  
[上一课 14.14 拷贝构造函数简介](Chapter-14/lesson14.14-introduction-to-the-copy-constructor.md)