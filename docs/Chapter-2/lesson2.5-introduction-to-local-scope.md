2.5 — 局部作用域入门  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月1日（首次发布于2015年2月8日）  

局部变量  
----------------  

在函数体内定义的变量称为**局部变量（local variable）**（与*全局变量*相对，后者将在后续章节讨论）：  
```cpp
int add(int x, int y)
{
    int z{ x + y }; // z是局部变量

    return z;
}
```  

函数参数通常也被视为局部变量，我们在此将其归为此类：  
```cpp
int add(int x, int y) // 函数参数x和y是局部变量
{
    int z{ x + y };

    return z;
}
```  

本课将详细探讨局部变量的特性。  

局部变量生命周期  
----------------  

在课程[1.3 — 对象与变量入门](Chapter-1/lesson1.3-introduction-to-objects-and-variables.md)中，我们讨论了`int x;`这类变量定义会在语句执行时实例化变量。函数参数在进入函数时创建并初始化，函数体内的变量在定义点创建并初始化。例如：  
```cpp
int add(int x, int y) // x和y在此处被创建并初始化
{ 
    int z{ x + y };   // z在此处被创建并初始化

    return z;
}
```  

自然会产生疑问："实例化的变量何时被销毁？"。局部变量会在其定义所在的大括号块末尾（函数参数则在函数末尾）以与创建顺序相反的顺序销毁。  
```cpp
int add(int x, int y)
{ 
    int z{ x + y };

    return z;
} // z、y、x在此处销毁
```  

类似于人的生命周期始于出生终于死亡，对象的**生命周期（lifetime）**定义为其创建到销毁的时间段。注意变量创建和销毁发生在程序运行时（即运行时属性），而非编译时。因此，生命周期是运行时属性。  

> **进阶阅读**  
> 上述创建、初始化和销毁规则是强制性保证。即对象必须在定义点或之前创建并初始化，销毁时间不得早于其所在大括号块的末尾（函数参数则为函数末尾）。  
>  
> 实际上，C++规范给予编译器很大灵活性来决定局部变量的创建和销毁时机。出于优化目的，对象可能提前创建或延迟销毁。最常见的情况是，局部变量在函数进入时创建，在函数退出时以与创建相反的顺序销毁。我们将在讨论调用栈时详细讲解此机制。  

以下是演示变量`x`生命周期的稍复杂程序：  
```cpp
#include <iostream>

void doSomething()
{
    std::cout << "Hello!\n";
}

int main()
{
    int x{ 0 };    // x的生命周期开始

    doSomething(); // 此函数调用期间x仍存活

    return 0;
} // x的生命周期结束
```  

上述程序中，`x`的生命周期从定义点持续至`main`函数结束，包括`doSomething`执行期间。  

对象销毁时会发生什么？  
----------------  

多数情况下无特殊操作，销毁对象仅使其失效。  

> **进阶阅读**  
> 若对象是类类型，销毁前会调用称为析构函数（destructor）的特殊函数。多数情况下析构函数无操作，故无额外开销。我们将在课程[15.4 — 析构函数入门](Chapter-15/lesson15.4-introduction-to-destructors.md)介绍析构函数。  

在对象销毁后使用会导致未定义行为。销毁后，对象占用的内存将被**回收（deallocated）**（释放以供重用）。  

局部作用域（块作用域）  
----------------  

标识符的**作用域（scope）**决定其在源代码中的可见范围。标识符可见时称为**在作用域内（in scope）**，不可见时称为**超出作用域（out of scope）**。作用域是编译期属性，尝试使用超出作用域的标识符会导致编译错误。  

局部变量的标识符具有局部作用域。**局部作用域（local scope）**（技术上也称**块作用域（block scope）**）的标识符从定义点开始，到包含它的最内层大括号块末尾（函数参数则为函数末尾）有效。这确保局部变量无法在定义前使用（即使编译器提前创建了它们），也无法在销毁后使用。某函数中定义的局部变量在其他被调用函数中也不可见。  

以下是演示变量`x`作用域的程序：  
```cpp
#include <iostream>

// 此函数中任何位置x都不在作用域内
void doSomething()
{
    std::cout << "Hello!\n";
}

int main()
{
    // 此处x不可用（尚未进入作用域）

    int x{ 0 }; // x进入作用域，可在本函数内使用

    doSomething();

    return 0;
} // x离开作用域，不再可用
```  

上述程序中，变量`x`在定义点进入作用域，在`main`函数右大括号处离开作用域。注意`doSomething`函数内任何位置都无法访问`x`。`main`调用`doSomething`的事实在此上下文中无关。  

"超出作用域" vs "即将离开作用域"  
----------------  

这两个术语容易让新手困惑：  
- 标识符**超出作用域**指其在代码中不可访问的区域  
- **即将离开作用域**通常用于对象而非标识符。当对象到达其实例化作用域末尾时，称其即将离开作用域  

局部变量的生命周期在离开作用域时结束，因此此时被销毁。注意并非所有变量类型都会在离开作用域时销毁，后续课程将展示相关示例。  

另一个示例  
----------------  

以下是结合生命周期（运行时属性）和作用域（编译期属性）的稍复杂示例：  
```cpp
#include <iostream>

int add(int x, int y) // x和y在此创建并进入作用域
{
    // x和y仅在add()内可用
    return x + y;
} // y和x离开作用域并被销毁

int main()
{
    int a{ 5 }; // a创建、初始化并进入作用域
    int b{ 6 }; // b创建、初始化并进入作用域

    // a和b仅在main()内可用

    std::cout << add(a, b) << '\n'; // 调用add(5,6)，x=5，y=6

    return 0;
} // b和a离开作用域并被销毁
```  

参数`x`和`y`在`add`调用时创建，仅在`add`内可见/可用，在`add`结束时销毁。变量`a`和`b`在`main`内创建，仅在`main`内可见/可用，在`main`结束时销毁。  

详细执行流程：  
1. 从`main`开始执行  
2. 创建`a`并初始化为5  
3. 创建`b`并初始化为6  
4. 调用`add(5,6)`  
5. 创建参数`x=5`和`y=6`  
6. 计算`x+y=11`  
7. 将11返回给`main`  
8. 销毁`y`和`x`  
9. 输出11  
10. `main`返回0  
11. 销毁`b`和`a`  

注意若`add`被多次调用，参数`x`和`y`会随每次调用创建和销毁。在包含大量函数调用的程序中，变量频繁创建销毁。  

函数隔离  
----------------  

考虑以下重命名示例：  
```cpp
#include <iostream>

int add(int x, int y) // add的x和y在此创建并进入作用域
{
    // add的x和y仅在此函数内可见/可用
    return x + y;
} // add的y和x离开作用域并被销毁

int main()
{
    int x{ 5 }; // main的x创建、初始化并进入作用域
    int y{ 6 }; // main的y创建、初始化并进入作用域

    std::cout << add(x, y) << '\n';

    return 0;
} // main的y和x离开作用域并被销毁
```  

虽然`main`和`add`都有名为`x`和`y`的变量，但程序仍能编译运行，因为：  
1. 这些变量是相互独立的  
2. 在`main`内，`x`和`y`指代其局部变量  
3. 在`add`内，`x`和`y`指代其参数  

由于作用域不重叠，编译器能明确区分各个变量。  

> **关键洞察**  
> 函数参数或局部变量名仅在声明它们的函数内可见。这使得各函数的局部变量命名可独立进行，保持函数间独立性。  

局部变量的定义位置  
----------------  

现代C++最佳实践是：函数体内的局部变量应尽量靠近首次使用的位置定义：  
```cpp
#include <iostream>

int main()
{
    std::cout << "输入整数：";
    int x{};       // x在此定义
    std::cin >> x; // 在此使用

    std::cout << "输入另一整数：";
    int y{};       // y在此定义
    std::cin >> y; 

    int sum{ x + y }; // sum可用预期值初始化
    std::cout << "和为：" << sum << '\n';

    return 0;
}
```  

每个变量在首次使用前定义。无需严格遵循，但应尽量保持此风格。  

> **最佳实践**  
> 将局部变量定义在尽可能靠近其首次使用的位置。  

过时的C语言风格（因旧编译器限制要求所有局部变量在函数顶部定义）存在以下缺陷：  
- 变量用途不明确  
- 初始值可能不可用  
- 初始化与使用间隔过大  

C99标准已取消此限制。  

函数参数 vs 局部变量  
----------------  

当函数体内需要变量时：  
- 使用**函数参数**：当调用者通过实参提供初始值  
- 使用**局部变量**：其他情况  

错误示例（不必要地使用函数参数）：  
```cpp
#include <iostream>

int getValueFromUser(int val) // val是函数参数
{
    std::cout << "输入值：";
    std::cin >> val;
    return val;
}

int main()
{
    int x{};
    int num{ getValueFromUser(x) }; // main必须传递x

    std::cout << "你输入了" << num << '\n';
    return 0;
}
```  

正确写法（使用局部变量）：  
```cpp
#include <iostream>

int getValueFromUser()
{
    int val{}; // val是局部变量
    std::cout << "输入值：";
    std::cin >> val;
    return val;
}

int main()
{
    int num{ getValueFromUser() }; // main无需传递参数

    std::cout << "你输入了" << num << '\n';
    return 0;
}
```  

> **最佳实践**  
> 函数内需要变量时：  
> - 使用函数参数：当调用者通过参数传递初始值  
> - 使用局部变量：其他情况  

临时对象入门  
----------------  

**临时对象（temporary object）**（也称**匿名对象（anonymous object）**）是编译器生成的未命名对象，用于短期存储值。常见产生场景：  
```cpp
#include <iostream>

int getValueFromUser()
{
    std::cout << "输入整数：";
    int input{};
    std::cin >> input;

    return input; // 将input的值返回给调用者
}

int main()
{
    std::cout << getValueFromUser() << '\n'; // 返回值存储于何处？
    return 0;
}
```  

`getValueFromUser`返回`input`的副本，但`main`未定义变量存储该值。此时返回值存储在临时对象中，该对象随后传递给`std::cout`输出。  

> **关键洞察**  
> 按值返回会向调用者传递持有返回值的临时对象。  

临时对象没有作用域（因其无标识符），在所属完整表达式结束时销毁。例如上述程序中，`getValueFromUser`返回的临时对象在`std::cout`语句执行后销毁。  

现代C++（特别是C++17后）编译器会优化临时对象的生成。例如用返回值初始化变量时，可能直接初始化而跳过临时对象。类似地，当返回值立即输出时，编译器可能跳过临时对象的创建和销毁。  

测验时间  
----------------  

**问题1**  
以下程序输出什么？  
```cpp
#include <iostream>

void doIt(int x)
{
    int y{ 4 };
    std::cout << "doIt: x = " << x << " y = " << y << '\n';

    x = 3;
    std::cout << "doIt: x = " << x << " y = " << y << '\n';
}

int main()
{
    int x{ 1 };
    int y{ 2 };

    std::cout << "main: x = " << x << " y = " << y << '\n';

    doIt(x);

    std::cout << "main: x = " << x << " y = " << y << '\n';
    return 0;
}
```  

**答案**  
```
main: x = 1 y = 2  
doIt: x = 1 y = 4  
doIt: x = 3 y = 4  
main: x = 1 y = 2  
```  

执行流程：  
1. `main`的`x=1`，`y=2`  
2. 输出`main: x=1 y=2`  
3. 调用`doIt(1)`  
4. `doIt`的`x=1`，`y=4`  
5. 输出`doIt: x=1 y=4`  
6. `doIt`的`x`修改为3  
7. 输出`doIt: x=3 y=4`  
8. 返回`main`后，`main`的`x`和`y`保持原值  

[下一课 2.6 — 函数的优势及有效使用方法](Chapter-2/lesson2.6-why-functions-are-useful-and-how-to-use-them-effectively.md)  
[返回主页](/)  
[上一课 2.4 — 函数参数与实参入门](Chapter-2/lesson2.4-introduction-to-function-parameters-and-arguments.md)