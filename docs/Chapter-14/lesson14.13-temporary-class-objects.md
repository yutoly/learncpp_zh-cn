14.13 — 临时类对象  
================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2007年12月27日（首次发布）  
2024年12月20日（更新）  

考虑以下示例：  

```cpp
#include <iostream>

int add(int x, int y)
{
    int sum{ x + y }; // 将x + y存储于变量
    return sum;       // 返回该变量的值
}

int main()
{
    std::cout << add(5, 3) << '\n';
    return 0;
}
```  

在`add()`函数中，变量`sum`用于存储表达式`x + y`的结果。该变量随后在返回语句中被求值以生成返回值。虽然这在调试时可能偶尔有用（以便在需要时检查`sum`的值），但通过定义仅使用一次的对象实际上增加了函数不必要的复杂度。  

多数情况下，若变量仅使用一次，我们实际上不需要定义变量。相反，可以用初始化变量的表达式直接替代变量使用。以下是改写后的`add()`函数：  

```cpp
#include <iostream>

int add(int x, int y)
{
    return x + y; // 直接返回x + y
}

int main()
{
    std::cout << add(5, 3) << '\n';
    return 0;
}
```  

这种做法不仅适用于返回值，也适用于多数函数参数。例如替代以下代码：  

```cpp
#include <iostream>

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    int sum{ 5 + 3 };
    printValue(sum);
    return 0;
}
```  

我们可以写成：  

```cpp
#include <iostream>

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    printValue(5 + 3);
    return 0;
}
```  

注意这种写法如何使代码更简洁。我们不需要定义变量并赋予名称，也无需扫描整个函数判断变量是否在其他地方使用。由于`5 + 3`是表达式，可知其仅在该行使用。  

此方法仅适用于接受右值表达式的情况。若需要左值表达式，则必须使用对象：  

```cpp
#include <iostream>

void addOne(int& value) // 非常量引用传参需要左值
{
    ++value;
}

int main()
{
    int sum { 5 + 3 };
    addOne(sum);   // 正确：sum是左值

    addOne(5 + 3); // 编译错误：非左值
    return 0;
}
```  

临时类对象  
----------------  

相同问题适用于类类型上下文。  

> **作者注**  
> 本节使用类进行演示，但涉及列表初始化的所有内容同样适用于通过聚合初始化（aggregate initialization）初始化的结构体（struct）。  

以下示例与上例类似，但使用自定义类`IntPair`代替`int`：  

```cpp
#include <iostream>

class IntPair
{
private:
    int m_x{};
    int m_y{};

public:
    IntPair(int x, int y)
        : m_x { x }, m_y { y }
    {}

    int x() const { return m_x; }
    int y() const { return m_y; }
};

void print(IntPair p)
{
    std::cout << "(" << p.x() << ", " << p.y() << ")\n";        
}
        
int main()
{
    // 案例1：传递变量
    IntPair p { 3, 4 };
    print(p); // 输出(3, 4)
    return 0;
}
```  

案例1中，我们实例化变量`IntPair p`后将其传递给`print()`函数。但`p`仅使用一次，且`print()`接受右值，因此无需定义变量。  

可以通过传递临时对象（temporary object）替代命名变量。**临时对象**（亦称匿名对象或无名对象）是没有名称且仅存在于单个表达式期间的对象。  

创建临时类对象的两种常见方式：  

```cpp
int main()
{
    // 案例2：构造临时IntPair并传递
    print(IntPair { 5, 6 } );

    // 案例3：隐式转换{7,8}为临时IntPair
    print( { 7, 8 } );
    return 0;
}
```  

案例2中，编译器构造用`{5,6}`初始化的`IntPair`临时对象。该对象被传递给`print()`的参数`p`，函数返回后临时对象销毁。  

案例3中，编译器根据函数参数推导出需要构造`IntPair`类型，并隐式转换`{7,8}`为临时对象。  

总结：  

```cpp
IntPair p { 1, 2 }; // 创建命名对象p
IntPair { 1, 2 };   // 创建临时对象
{ 1, 2 };           // 根据上下文转换为临时对象
```  

我们将在[14.16 — 转换构造函数与explicit关键字](Chapter-14/lesson14.16-converting-constructors-and-the-explicit-keyword.md)中详细讨论最后一种情况。  

更多示例：  

```cpp
std::string { "Hello" }; // 用"Hello"初始化的临时字符串
std::string {};          // 值初始化/默认构造的临时字符串
```  

通过直接初始化创建临时对象（可选）  
----------------  

虽然可以通过直接列表初始化（direct-list-initialization）创建临时对象，但无法使用拷贝初始化（copy initialization）语法。  

但可通过直接初始化（direct initialization）创建临时对象：  

```cpp
Foo (1, 2); // 直接初始化临时Foo（类似Foo{1,2}）
```  

忽略其类似函数调用的外观，该语法与`Foo{1,2}`效果相同（仅缺少窄化转换检查）。  

接下来展示为何不建议使用该语法。  

> **作者注**  
> 本节内容主要为阅读趣味性考虑，无需深入理解或记忆。  

无参数情况：  

```cpp
Foo();     // 值初始化临时对象（同Foo{}）
```  

注意`Foo()`在变量定义时语义不同：  

```cpp
Foo bar{}; // 变量bar的值初始化
Foo bar(); // 函数bar的声明（返回Foo）
```  

更复杂案例：  

```cpp
Foo(1);    // 函数式转换字面量1为临时Foo（类似Foo{1}）
Foo(bar);  // 定义变量bar（若bar已定义将导致重定义错误）
```  

编译器能区分字面量和标识符：`Foo(bar)`等同于`Foo bar`。  

> **关键洞察**  
> 括号（parentheses）因多重用途而复杂：函数调用、对象直接初始化、临时对象值初始化、C风格转换、符号分组、变量定义等。而花括号（curly braces）明确表示对象操作。  

返回值与临时对象  
----------------  

函数按值返回时，返回的对象是临时对象（由return语句初始化）。示例：  

```cpp
IntPair ret1() { IntPair p {3,4}; return p; } // 返回p初始化的临时对象
IntPair ret2() { return IntPair{5,6}; }       // 返回临时对象初始化的临时对象
IntPair ret3() { return {7,8}; }              // 隐式转换返回临时对象
```  

临时类对象在表达式中是右值，仅存在于定义点至所属完整表达式结束。  

static_cast与显式创建临时对象  
----------------  

在无需窄化转换的类型转换中，可选择使用`static_cast`或显式创建临时对象：  

```cpp
std::cout << static_cast<int>('a'); // 直接初始化临时int
std::cout << int{ 'a' };            // 列表初始化临时int
```  

更复杂案例（printString.h）：  

```cpp
void printString(const std::string &s);
```  

main.cpp：  

```cpp
std::string_view sv{ "Hello" };
printString(static_cast<std::string>(sv)); // 案例1：static_cast转换
printString(std::string{ sv });            // 案例2：显式列表初始化
printString(std::string(sv));              // 案例3：C风格转换（应避免）
```  

> **最佳实践**  
> * 转换基础类型时优先使用`static_cast`  
> * 转换类类型时优先列表初始化临时对象  
> * 需要窄化转换或强调行为差异时使用`static_cast`  
> * 需要列表构造或额外构造参数时创建新对象  

[下一课 14.14 拷贝构造函数简介](Chapter-14/lesson14.14-introduction-to-the-copy-constructor.md)  
[返回主页](/)  
[上一课 14.12 委托构造函数](Chapter-14/lesson14.12-delegating-constructors.md)