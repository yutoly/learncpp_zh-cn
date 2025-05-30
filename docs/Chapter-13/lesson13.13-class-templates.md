13.13 — 类模板  
========================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年4月21日，下午1:48（太平洋夏令时）  
2024年12月30日  

在课程[11.6 — 函数模板](Chapter-11/lesson11.6-function-templates.md)中，我们介绍了需要为每种类型组合单独创建（重载）函数的挑战：  

```cpp
#include <iostream>

// 计算两个int值中较大者的函数
int max(int x, int y)
{
    return (x < y) ? y : x;
}

// 几乎相同的函数，用于计算两个double值中的较大者
// 唯一区别在于类型信息
double max(double x, double y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(5, 6);     // 调用max(int, int)
    std::cout << '\n';
    std::cout << max(1.2, 3.4); // 调用max(double, double)

    return 0;
}
```  

解决方案是创建函数模板，编译器可根据需要实例化为具体类型的函数：  

```cpp
#include <iostream>

// 单个max函数模板
template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(5, 6);     // 实例化并调用max<int>(int, int)
    std::cout << '\n';
    std::cout << max(1.2, 3.4); // 实例化并调用max<double>(double, double)

    return 0;
}
```  

**相关内容**  
函数模板实例化工作原理详见课程[11.7 — 函数模板实例化](Chapter-11/lesson11.7-function-template-instantiation.md)。  

### 聚合类型的类似挑战  
聚合类型（结构体/类/联合体和数组）面临类似挑战。  

例如：假设我们需要处理`int`值对并确定较大值，可能编写如下程序：  

```cpp
#include <iostream>

struct Pair
{
    int first{};
    int second{};
};

constexpr int max(Pair p) // 按值传递，因Pair体积小
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair p1{ 5, 6 };
    std::cout << max(p1) << " is larger\n";

    return 0;
}
```  

随后发现还需处理`double`值对，于是修改程序：  

```cpp
#include <iostream>

struct Pair
{
    int first{};
    int second{};
};

struct Pair // 编译错误：Pair重定义错误
{
    double first{};
    double second{};
};

constexpr int max(Pair p)
{
    return (p.first < p.second ? p.second : p.first);
}

constexpr double max(Pair p) // 编译错误：重载函数仅返回类型不同
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair p1{ 5, 6 };
    std::cout << max(p1) << " is larger\n";

    Pair p2{ 1.2, 3.4 };
    std::cout << max(p2) << " is larger\n";

    return 0;
}
```  

此程序无法编译，存在三个问题：  
1. 类型定义不可重载，编译器将第二个`Pair`视为错误重定义  
2. 重载函数不能仅通过返回类型区分  
3. 存在大量冗余（除数据类型外，每个`Pair`结构体和`max()`函数均相同）  

虽然可通过命名方案（如`PairInt`和`PairDouble`）解决前两个问题，但无法消除冗余。  

### 类模板  
函数模板用于实例化函数，**类模板（class template）**则用于实例化类类型。  

> **提示**  
> "类类型（class type）"指结构体、类或联合体类型。为简化演示，本文使用结构体，但所有内容同样适用于类。  

回顾`int`对结构体定义：  

```cpp
struct Pair
{
    int first{};
    int second{};
};
```  

将其改写为类模板：  

```cpp
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

int main()
{
    Pair<int> p1{ 5, 6 };        // 实例化Pair<int>并创建对象p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // 实例化Pair<double>并创建对象p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // 使用现有Pair<double>定义创建对象p3
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
```  

类模板定义以模板参数声明开始：  
1. 使用`template`关键字  
2. 尖括号`<>`内指定模板类型  
3. 每个模板类型使用`typename`（推荐）或`class`声明（如`T`）  

结构体定义中，模板类型`T`可替代任何需模板化的类型。  

`main()`函数中实例化`Pair`对象时：  
- `Pair<int>`触发编译器实例化`T`替换为`int`的结构体类型  
- `Pair<double>`同理实例化`double`版本  
- 已实例化的类型（如`Pair<double>`）会复用现有定义  

> **高级阅读**  
> 此示例使用了**类模板特化（class template specialization）**特性（详见课程[26.4 — 类模板特化](Chapter-26/lesson26.4-class-template-specialization.md)）。  

### 在函数中使用类模板  
要使`max()`支持不同类型，可利用参数类型差异进行重载：  

```cpp
constexpr int max(Pair<int> p)
{
    return (p.first < p.second ? p.second : p.first);
}

constexpr double max(Pair<double> p) // 合法：通过参数类型区分的重载函数
{
    return (p.first < p.second ? p.second : p.first);
}
```  

此方案未解决冗余问题。理想方案是函数能接受任意类型的`Pair`，即参数类型为`Pair<T>`（`T`为模板类型参数），这需要函数模板实现：  

```cpp
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
constexpr T max(Pair<T> p)
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair<int> p1{ 5, 6 };
    std::cout << max<int>(p1) << " is larger\n"; // 显式调用max<int>

    Pair<double> p2{ 1.2, 3.4 };
    std::cout << max(p2) << " is larger\n"; // 通过模板实参推导调用max<double>（推荐此方式）

    return 0;
}
```  

`max()`函数模板工作流程：  
1. 模板参数声明定义类型`T`  
2. 调用`max(Pair<int>)`时，实例化`int max<int>(Pair<int>)`  
3. 可显式指定模板类型（如`max<int>(p1)`）或依赖模板实参推导（如`max(p2)`）  

### 含模板类型和非模板类型成员的类模板  
类模板可混合使用模板类型和非模板类型成员：  

```cpp
template <typename T>
struct Foo
{
    T first{};    // first类型由T决定
    int second{}; // second始终为int（与T无关）
};
```  

### 含多模板类型的类模板  
若需`Pair`成员为不同类型，可定义多模板类型的类模板：  

```cpp
#include <iostream>

template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

template <typename T, typename U>
void print(Pair<T, U> p)
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}

int main()
{
    Pair<int, double> p1{ 1, 2.3 }; // int与double对
    Pair<double, int> p2{ 4.5, 6 }; // double与int对
    Pair<int, int> p3{ 7, 8 };      // int对

    print(p2);

    return 0;
}
```  

多个模板类型在声明中用逗号分隔（如`template <typename T, typename U>`）。`T`和`U`可相同或不同。  

### 使函数模板支持多类类型  
考虑上述`print()`函数模板：  

```cpp
template <typename T, typename U>
void print(Pair<T, U> p) // 仅匹配Pair<T, U>类型参数
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}
```  

若需函数模板支持任意可编译类型，可使用类型模板参数作为函数参数：  

```cpp
#include <iostream>

template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

struct Point
{
    int first{};
    int second{};
};

template <typename T>
void print(T p) // 类型模板参数匹配任意类型
{
    std::cout << '[' << p.first << ", " << p.second << ']'; // 要求类型含first和second成员
}

int main()
{
    Pair<double, int> p1{ 4.5, 6 };
    print(p1); // 匹配print(Pair<double, int>)

    std::cout << '\n';

    Point p2 { 7, 8 };
    print(p2); // 匹配print(Point)

    std::cout << '\n';
    
    return 0;
}
```  

> **注意命名冲突**  
> 以下代码中`Pair`作为模板参数会遮蔽全局类类型`Pair`：  
> ```cpp
> template <typename Pair> // 定义名为Pair的模板参数（遮蔽Pair类类型）
> void print(Pair p)       // 此处Pair指模板参数，而非类类型
> {
>     std::cout << '[' << p.first << ", " << p.second << ']';
> }
> ```  
> 此版本会匹配任意类型，推荐使用`T`/`U`等简单模板参数名避免遮蔽。  

### std::pair  
因数据处理常用，C++标准库在`<utility>`头文件中定义了`std::pair`类模板：  

```cpp
#include <iostream>
#include <utility>

template <typename T, typename U>
void print(std::pair<T, U> p)
{
    // std::pair成员预定义名称为first和second
    std::cout << '[' << p.first << ", " << p.second << ']';
}

int main()
{
    std::pair<int, double> p1{ 1, 2.3 }; // int与double对
    std::pair<double, int> p2{ 4.5, 6 }; // double与int对
    std::pair<int, int> p3{ 7, 8 };      // int对

    print(p2);

    return 0;
}
```  

实际开发中应优先使用`std::pair`而非自定义实现。  

### 在多文件中使用类模板  
类模板应定义在头文件中（与函数模板类似），模板定义和类型定义不受单一定义规则限制：  

**pair.h**  
```cpp
#ifndef PAIR_H
#define PAIR_H

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
constexpr T max(Pair<T> p)
{
    return (p.first < p.second ? p.second : p.first);
}

#endif
```  

**foo.cpp**  
```cpp
#include "pair.h"
#include <iostream>

void foo()
{
    Pair<int> p1{ 1, 2 };
    std::cout << max(p1) << " is larger\n";
}
```  

**main.cpp**  
```cpp
#include "pair.h"
#include <iostream>

void foo(); // foo()函数声明

int main()
{
    Pair<double> p2 { 3.4, 5.6 };
    std::cout << max(p2) << " is larger\n";

    foo();

    return 0;
}
```  

[下一课 13.14 — 类模板实参推导（CTAD）与推导指引](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)  
[返回主页](/)  
[上一课 13.12 — 指针和引用的成员选择](Chapter-13/lesson13.12-member-selection-with-pointers-and-references.md)