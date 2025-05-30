27.9 — 异常规范与noexcept
=============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月31日（首次发布于2020年8月11日）  

（感谢读者Koe提供本课初稿！）

观察典型函数声明时，无法判断函数是否会抛出异常：

```
int doSomething(); // 此函数会抛出异常吗？
```

上例中，`doSomething()`会抛出异常吗？答案并不明确。但在某些上下文中这很重要。在课程[27.8 — 异常的隐患与缺点](Chapter-27/lesson27.8-exception-dangers-and-downsides.md)中，我们描述了析构函数在栈展开期间抛出异常将导致程序终止的情况。如果`doSomething()`可能抛出异常，那么在析构函数中（或其他不希望抛出异常的地方）调用它就是有风险的。虽然可以让析构函数处理`doSomething()`抛出的异常（防止异常传播出析构函数），但必须记得这样做并确保覆盖所有可能抛出的异常类型。

虽然注释可能帮助说明函数是否会抛出异常，但文档可能过时且缺乏编译器强制检查。

**异常规范（exception specifications）**是一种语言机制，最初设计用于在函数规范中说明可能抛出的异常类型。虽然大多数异常规范现已被弃用或移除，但新增了一个有用的替代规范，我们将在本课讨论。

noexcept 说明符
----------------

在C++中，所有函数被分类为*不抛出（non-throwing）*或*可能抛出（potentially throwing）*。**不抛出函数**承诺不会抛出对调用者可见的异常。**可能抛出函数**可能抛出对调用者可见的异常。

要将函数定义为不抛出，可使用**noexcept 说明符**。在函数声明中，将`noexcept`关键字置于参数列表右侧：

```
void doSomething() noexcept; // 该函数被指定为不抛出
```

注意`noexcept`实际上并不阻止函数抛出异常或调用其他可能抛出的函数。只要noexcept函数内部捕获并处理这些异常，且异常不传播出noexcept函数，这都是允许的。

如果未处理的异常即将传播出noexcept函数，将调用`std::terminate`（即使存在能处理该异常的异常处理程序）。如果从noexcept函数内部调用`std::terminate`，栈展开可能发生也可能不发生（取决于实现和优化），这意味着对象在终止前可能被正确析构也可能不。

> **关键洞察**  
> noexcept函数不向调用者抛出异常的承诺是契约性承诺，而非编译器强制。因此尽管调用noexcept函数应是安全的，但若noexcept函数中的异常处理缺陷导致契约被破坏，将导致程序终止！这不应该发生，但缺陷也同样不该存在。

因此，最好让noexcept函数完全不涉及异常，或调用不会引发异常的可能抛出函数。如果根本不可能引发异常，noexcept函数就不会有异常处理缺陷。

与仅返回值不同的函数不能重载类似，仅异常规范不同的函数也不能重载。

演示noexcept函数与异常行为
----------------

以下程序演示了不同情况下noexcept函数与异常的行为：

```
// 感谢读者yellowEmu提供本程序初稿
#include <iostream>

class Doomed
{
public:
    ~Doomed()
    {
        std::cout << "Doomed 析构\n";
    }
};

void thrower()
{
    std::cout << "抛出异常\n";
    throw 1;
}

void pt()
{
    std::cout << "调用 pt（可能抛出）\n";
    // 该对象将在栈展开时析构（如果发生）
    Doomed doomed{};
    thrower();
    std::cout << "此处永不输出\n";
}

void nt() noexcept
{
    std::cout << "调用 nt（noexcept）\n";
    // 该对象将在栈展开时析构（如果发生）
    Doomed doomed{};
    thrower();
    std::cout << "此处永不输出\n";
}

void tester(int c) noexcept
{
    std::cout << "调用 tester（noexcept）case " << c << "\n";
    try
    {
        (c == 1) ? pt() : nt();
    }
    catch (...)
    {
        std::cout << "tester 捕获异常\n";
    }
}

int main()
{
    std::cout << std::unitbuf; // 每次插入后刷新缓冲区
    std::cout << std::boolalpha; // 以true/false打印布尔值
    tester(1);
    std::cout << "测试成功\n\n";
    tester(2);
    std::cout << "测试成功\n";

    return 0;
}
```

在作者机器上，程序输出：

```
调用 tester（noexcept）case 1
调用 pt（可能抛出）
抛出异常
Doomed 析构
tester 捕获异常
测试成功

调用 tester（noexcept）case 2
调用 nt（noexcept）
抛出异常
terminate called after throwing an instance of 'int'
```

随后程序中止。

详细分析：

1. 第一个案例显示noexcept函数可以调用可能抛出函数并处理其异常。`tester(1)`调用可能抛出函数`pt`，后者调用`thrower`抛出异常。异常在`tester`中被捕获处理，栈展开时析构`doomed`对象，未违反noexcept约定。

2. 第二个案例演示noexcept函数试图传递异常给调用者的情况。`tester(2)`调用noexcept函数`nt`，后者抛出异常。由于`nt`是noexcept，异常传播给调用者违反约定，触发`std::terminate`，程序立即终止。作者机器上未发生栈展开（`doomed`未被析构）。

带布尔参数的noexcept说明符
----------------

`noexcept`说明符可接受可选布尔参数。`noexcept(true)`等价于`noexcept`，表示不抛出函数。`noexcept(false)`表示可能抛出函数。这些参数通常用于模板函数，根据参数化值动态生成不抛出或可能抛出函数。

不抛出与可能抛出函数分类
----------------

隐式不抛出的函数：
* 析构函数

隐式声明或默认函数默认不抛出：
* 构造函数：默认、拷贝、移动
* 赋值运算符：拷贝、移动
* 比较运算符（C++20起）

但如果这些函数调用（显式或隐式）了可能抛出函数，则它们将被视为可能抛出。例如类成员有可能抛出构造函数时，该类构造函数将被视为可能抛出。

可能抛出的函数（非隐式声明或默认）：
* 普通函数
* 用户定义构造函数
* 用户定义运算符

noexcept运算符
----------------

`noexcept`运算符可用于表达式内部。它接受表达式参数，返回`true`或`false`表示编译器认为是否抛出异常。该运算符在编译期静态检查，不实际求值表达式。

```
void foo() {throw -1;}
void boo() {};
void goo() noexcept {};
struct S{};

constexpr bool b1{ noexcept(5 + 3) }; // true；整型运算不抛出
constexpr bool b2{ noexcept(foo()) }; // false；foo()抛出异常
constexpr bool b3{ noexcept(boo()) }; // false；boo()隐式noexcept(false)
constexpr bool b4{ noexcept(goo()) }; // true；goo()显式noexcept(true)
constexpr bool b5{ noexcept(S{}) };   // true；结构体默认构造函数默认noexcept
```

该运算符可用于根据抛出可能性条件执行代码，满足特定**异常安全保证（exception safety guarantee）**。

异常安全保证
----------------

**异常安全保证**是关于函数或类在异常发生时的行为契约。共有四个级别：

1. 无保证 — 异常发生时无任何保证（如类可能处于不可用状态）
2. 基本保证 — 异常发生时无内存泄漏，对象仍可用，但程序状态可能改变
3. 强保证 — 异常发生时无内存泄漏且程序状态不变。函数需完全成功或失败时不产生副作用
4. 不抛/不失败保证 — 函数始终成功（不失败）或不抛出可见异常（不抛）。`noexcept`说明符对应此级别

不抛/不失败保证详解：

* 不抛保证：函数失败时不抛出异常，返回错误码或忽略问题。栈展开期间需要此保证（如所有析构函数应具备不抛保证）
* 不失败保证：函数总能成功（更强的不抛形式）。需要此保证的场景：
  - 移动构造函数/赋值（见[第22章](https://www.learncpp.com#Chapter22)）
  - swap函数
  - 容器的clear/erase/reset操作
  - std::unique_ptr操作
  - 高层不失败函数调用的底层函数

何时使用noexcept
----------------

即使代码未显式抛出异常，也不应随意添加`noexcept`。默认多数函数可能抛出，若函数调用其他可能抛出函数，则自身也可能抛出。

使用noexcept的合理场景：

1. 可被非异常安全函数（如析构函数）安全调用
2. 允许编译器优化（无需维护可展开的运行时栈）
3. 标准库容器（如`std::vector`）根据`noexcept`决定使用移动语义（更快）或拷贝语义（更慢）

标准库策略：仅在必须不抛/不失败的函数上使用`noexcept`。可能抛出但实际不抛的函数通常不标记。

自定义代码应始终标记为`noexcept`的情况：
* 移动构造函数
* 移动赋值运算符
* swap函数

考虑标记的情况：
* 需表达不抛/不失败保证的函数
* 不抛的拷贝构造函数/赋值运算符（优化用）
* 析构函数（当所有成员有noexcept析构函数时）

> **最佳实践**  
> 始终为移动构造、移动赋值和swap函数标记`noexcept`  
> 尽可能为拷贝构造/赋值标记`noexcept`  
> 用`noexcept`表达其他函数的不抛/不失败保证  

> **注意**  
> 不确定时应谨慎，不标记`noexcept`。事后添加`noexcept`会破坏接口承诺，而移除现有`noexcept`可能破坏现有代码。加强保证（后加`noexcept`）是安全的。

动态异常规范（选读）
----------------

C++11之前至C++17，使用*动态异常规范*代替`noexcept`。其语法用`throw`关键字列出可能抛出的异常类型：

```
int doSomething() throw(); // 不抛异常
int doSomething() throw(std::out_of_range, int*); // 可能抛出std::out_of_range或int指针
int doSomething() throw(...); // 可能抛出任何异常
```

由于编译器实现不全、与模板函数不兼容、常见误解及标准库未广泛使用等原因，动态异常规范在C++11被弃用，C++17/20移除。详见[此论文](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0003r0.html#2.0)。

[下一课 27.10 — std::move_if_noexcept](Chapter-27/lesson27.10-stdmove_if_noexcept.md)  
[返回主页](/)  
[上一课 27.8 — 异常的隐患与缺点](Chapter-27/lesson27.8-exception-dangers-and-downsides.md)