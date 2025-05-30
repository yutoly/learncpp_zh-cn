8.5 — Switch语句基础  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月28日（首次发布于2007年6月21日）  

虽然可以通过链式if-else语句实现多条件判断，但这种方式既难以阅读又效率低下。请看以下示例程序：  

```cpp
#include <iostream>

void printDigitName(int x)
{
    if (x == 1)
        std::cout << "One";
    else if (x == 2)
        std::cout << "Two";
    else if (x == 3)
        std::cout << "Three";
    else
        std::cout << "Unknown";
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
```  

`printDigitName()`函数中的变量`x`根据传入值最多会被求值三次（效率低下），且读者必须确认每次判断的都是`x`（而非其他变量）。  

由于对变量或表达式进行多值相等性测试是常见需求，C++提供了专用的条件语句——**switch语句（switch statement）**。以下是使用switch的等价程序：  

```cpp
#include <iostream>

void printDigitName(int x)
{
    switch (x)
    {
    case 1:
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    default:
        std::cout << "Unknown";
        return;
    }
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
```  

**switch语句**的核心机制是：对表达式（称为条件表达式）进行求值后：  

* 若表达式值与某个case标签（case label）后的值匹配，则执行该case标签后的语句  
* 若无匹配值但存在default标签（default label），则执行default标签后的语句  
* 若无匹配值且无default标签，则跳过整个switch语句  

让我们详细解析这些概念。  

启动switch语句  
----------------  

使用`switch`关键字启动switch语句，后接括号包裹的条件表达式。该表达式通常为单个变量，但也可以是任何有效表达式。  

switch的条件表达式必须求值为整型（integral type，参见[4.1 — 基础数据类型简介](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)）或枚举类型（enumerated type，将在后续课程[13.2 — 无作用域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)和[13.6 — 有作用域枚举](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)中讲解）。浮点类型、字符串等非整型不能作为switch条件。  

> **进阶阅读**  
> 为何switch仅支持整型或枚举类型？答案与编译器优化机制有关。历史上，编译器常通过[跳转表（jump tables）](https://en.wikipedia.org/wiki/Branch_table)实现switch语句——而跳转表仅支持整数值。  
>  
> 熟悉数组的读者可将跳转表视为使用整数值作为索引直接跳转到目标地址的机制，这比顺序比较更高效。  
>  
> 虽然编译器不一定使用跳转表实现switch，但截至C++23标准仍未放宽对条件类型的限制。  

在条件表达式后声明代码块，块内使用标签（label）定义待匹配值。switch语句使用两种标签类型。  

case标签  
----------------  

**case标签（case label）**使用`case`关键字声明，后接常量表达式。该表达式类型必须与条件表达式类型匹配或可转换为该类型。  

当条件表达式值与case标签匹配时，执行从该case标签后的第一条语句开始，并按顺序继续执行。示例：  

```cpp
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x被求值得到2
    {
    case 1:
        std::cout << "One";
        return;
    case 2: // 匹配此处case标签
        std::cout << "Two"; // 从此处开始执行
        return; // 返回调用者
    case 3:
        std::cout << "Three";
        return;
    default:
        std::cout << "Unknown";
        return;
    }
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
```  

该程序输出：  

```
Two
```  

case标签数量理论上无限制，但同一switch中的case标签必须唯一。以下写法非法：  

```cpp
switch (x)
{
case 54:
case 54:  // 错误：值54重复使用
case '6': // 错误：'6'转换为整型值54，已存在该case
}
```  

若条件表达式不匹配任何case标签，则不执行任何case块。  

default标签  
----------------  

**default标签（default label）**使用`default`关键字声明。当条件表达式不匹配任何case标签时，若有default标签则执行其后的语句。示例：  

```cpp
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x被求值得到5
    {
    case 1:
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    default: // 无匹配case标签
        std::cout << "Unknown"; // 从此处开始执行
        return; // 返回调用者
    }
}

int main()
{
    printDigitName(5);
    std::cout << '\n';

    return 0;
}
```  

输出：  

```
Unknown
```  

default标签是可选的，每个switch语句最多有一个default标签。按惯例，default标签置于switch块末尾。  

> **最佳实践**  
> 将default标签置于switch块末尾。  

无匹配且无default的情况  
----------------  

若条件表达式不匹配任何case标签且无default标签，则不执行switch内的任何语句。程序继续执行switch块后的代码：  

```cpp
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x被求值得到5
    {
    case 1:
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    // 无匹配case且无default标签
    }

    // 继续执行此处
    std::cout << "Hello";
}

int main()
{
    printDigitName(5);
    std::cout << '\n';

    return 0;
}
```  

此例中`x`求值为5，但无对应case标签且无default标签。因此switch块未执行任何语句，继续执行后续代码输出`Hello`。  

break语句  
----------------  

在前述示例中，我们使用return语句终止执行。但这样会直接退出整个函数。  

**break语句（break statement）**使用`break`关键字声明，可使程序跳出switch块而不退出函数。示例：  

```cpp
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x求值为3
    {
    case 1:
        std::cout << "One";
        break;
    case 2:
        std::cout << "Two";
        break;
    case 3:
        std::cout << "Three"; // 从此处开始执行
        break; // 跳转至switch块末尾
    default:
        std::cout << "Unknown";
        break;
    }

    // 继续执行此处
    std::cout << " Ah-Ah-Ah!";
}

int main()
{
    printDigitName(3);
    std::cout << '\n';

    return 0;
}
```  

输出：  

```
Three Ah-Ah-Ah!
```  

> **最佳实践**  
> 每个标签下的语句应以break或return结尾，包括最后一个标签。  

若未使用break或return终止会发生什么？我们将在下一课探讨。  

标签缩进惯例  
----------------  

在[2.9 — 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)中提过，代码通常缩进以标识嵌套作用域。虽然switch的括号创建新作用域，但标签本身不定义嵌套作用域。因此标签后的代码通常不缩进。  

若将标签与后续语句统一缩进，会导致可读性问题：  

```cpp
// 不可读版本
void printDigitName(int x)
{
    switch (x)
    {
        case 1:
        std::cout << "One";
        return;
        case 2:
        std::cout << "Two";
        return;
        case 3:
        std::cout << "Three";
        return;
        default:
        std::cout << "Unknown";
        return;
    }
}
```  

常规做法是标签不缩进：  

```cpp
// 推荐版本
void printDigitName(int x)
{
    switch (x)
    {
    case 1: // 不缩进
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    default:
        std::cout << "Unknown";
        return;
    }
}
```  

这样既突出标签，又正确反映语句属于switch块作用域。  

> **最佳实践**  
> 推荐不对标签进行缩进，避免暗示嵌套作用域。  

switch与if-else对比  
----------------  

switch语句适用于对单个整型或枚举表达式进行少量值的等值测试。当case标签过多时，可读性会降低。  

相较于等效的if-else链，switch语句更易读、能明确表达等值测试意图，且只需对表达式求值一次（更高效）。  

但if-else更具灵活性，适用于以下场景：  

* 非等值比较（如`x > 5`）  
* 多条件组合判断（如`x == 5 && y == 6`）  
* 范围判断（如`x >= 5 && x <= 10`）  
* 非整型条件表达式（如`d == 4.0`）  
* 布尔值判断  

> **最佳实践**  
> 当对单个整型或枚举表达式进行少量等值测试时，优先选择switch语句而非if-else。  

[下一课 8.6 — Switch穿透与作用域](Chapter-8/lesson8.6-switch-fallthrough-and-scoping.md)  
[返回主页](/)  
[上一课 8.4 — constexpr if语句](Chapter-8/lesson8.4-constexpr-if-statements.md)