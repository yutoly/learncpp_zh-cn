13.14 — 类模板实参推导（CTAD）与推导指引
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年4月24日 PDT下午7:49 / 2024年3月25日  

类模板实参推导（CTAD） C++17  
----------------  

自C++17起，当从类模板实例化对象时，编译器可根据对象初始化器的类型推导模板类型（这称为**类模板实参推导（Class Template Argument Deduction）**，简称**CTAD**）。例如：  

```cpp
#include <utility> // 引入 std::pair

int main()
{
    std::pair<int, int> p1{ 1, 2 }; // 显式指定类模板 std::pair<int, int>（C++11起）
    std::pair p2{ 1, 2 };           // 使用CTAD从初始化器推导 std::pair<int, int>（C++17）
    return 0;
}
```  

仅当不存在模板实参列表时才会执行CTAD。因此以下两种写法均错误：  

```cpp
#include <utility> // 引入 std::pair

int main()
{
    std::pair<> p1 { 1, 2 };    // 错误：模板实参过少，两个参数均未推导
    std::pair<int> p2 { 3, 4 }; // 错误：模板实参过少，第二个参数未推导
    return 0;
}
```  

> **作者注**  
> 本教程后续课程将大量使用CTAD。若使用C++14（或更早）标准编译示例，将提示模板实参缺失错误。需显式添加模板实参才能通过编译。  

由于CTAD属于类型推导，可使用字面量后缀改变推导类型：  

```cpp
#include <utility> // 引入 std::pair

int main()
{
    std::pair p1 { 3.4f, 5.6f }; // 推导为 pair<float, float>
    std::pair p2 { 1u, 2u };     // 推导为 pair<unsigned int, unsigned int>
    return 0;
}
```  

模板实参推导指引 C++17  
----------------  

多数情况下CTAD可直接使用，但某些场景中编译器需额外引导才能正确推导模板实参。  

您可能惊讶地发现以下程序（与前文`std::pair`示例几乎相同）在C++17中无法编译：  

```cpp
// 自定义Pair类型
template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

int main()
{
    Pair<int, int> p1{ 1, 2 }; // 正确：显式指定模板实参
    Pair p2{ 1, 2 };           // C++17编译错误（C++20中正确）
    return 0;
}
```  

在C++17中编译时，可能收到“类模板实参推导失败”或“无法推导模板实参”等错误。这是因为C++17中CTAD无法推导聚合类模板的实参。为此可提供**推导指引（deduction guide）**，告知编译器如何推导类模板的实参。  

添加推导指引后的程序：  

```cpp
template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

// Pair类的推导指引（仅C++17需要）
// 用T和U类型参数初始化的Pair对象应推导为Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
    
int main()
{
    Pair<int, int> p1{ 1, 2 }; // 显式指定类模板 Pair<int, int>（C++11起）
    Pair p2{ 1, 2 };           // 使用CTAD从初始化器推导 Pair<int, int>（C++17）
    return 0;
}
```  

此示例在C++17下应能编译。  

`Pair`类的推导指引较简单，但需深入理解其原理：  

```cpp
// Pair类的推导指引（仅C++17需要）
// 用T和U类型参数初始化的Pair对象应推导为Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
```  

首先使用与`Pair`类相同的模板类型定义（因需为`Pair<T, U>`定义`T`和`U`）。箭头右侧放置需引导编译器推导的类型（此处为`Pair<T, U>`）。左侧指定编译器需匹配的声明形式（此处匹配含两个类型参数`T`和`U`的`Pair`声明）。也可写作`Pair(T t, U u)`（参数名`t`/`u`未使用时无需命名）。  

综上，我们告知编译器：若遇到含两个类型参数（分别为`T`和`U`）的`Pair`声明，应将其推导为`Pair<T, U>`。  

当编译器在程序中看到`Pair p2{ 1, 2 };`时，会识别“这是含两个`int`类型参数的`Pair`声明，使用推导指引应推导为`Pair<int, int>`”。  

单模板类型`Pair`的类似示例：  

```cpp
template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// Pair类的推导指引（仅C++17需要）
// 用两个T类型参数初始化的Pair对象应推导为Pair<T>
template <typename T>
Pair(T, T) -> Pair<T>;

int main()
{
    Pair<int> p1{ 1, 2 }; // 显式指定类模板 Pair<int>（C++11起）
    Pair p2{ 1, 2 };      // 使用CTAD从初始化器推导 Pair<int>（C++17）
    return 0;
}
```  

此推导指引将含两个`T`类型参数的`Pair(T, T)`映射到`Pair<T>`。  

> **提示**  
> C++20新增了为聚合类自动生成推导指引的功能，因此推导指引仅需用于C++17兼容。  

因此，无推导指引的`Pair`版本在C++20中应能编译。`std::pair`（及其他标准库模板类型）自带预定义推导指引，故前文`std::pair`示例在C++17中无需手动提供指引即可编译。  

> **进阶阅读**  
> C++17中非聚合类无需推导指引，因其构造函数已起相同作用。  

带默认值的类型模板形参  
----------------  

函数形参可设默认实参，模板形参亦可设默认值。当模板形参未显式指定且无法推导时将使用默认值。  

修改后的`Pair<T, U>`类模板程序（类型模板形参`T`和`U`默认设为`int`）：  

```cpp
template <typename T=int, typename U=int> // 默认T和U为int类型
struct Pair
{
    T first{};
    U second{};
};

template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;

int main()
{
    Pair<int, int> p1{ 1, 2 }; // 显式指定 Pair<int, int>（C++11起）
    Pair p2{ 1, 2 };           // CTAD推导为 Pair<int, int>（C++17）
    Pair p3;                   // 使用默认值 Pair<int, int>
    return 0;
}
```  

`p3`定义既未显式指定类型模板形参，也无初始化器供推导，故编译器使用默认值，`p3`将为`Pair<int, int>`类型。  

CTAD不适用于非静态成员初始化  
----------------  

使用非静态成员初始化（non-static member initialization）类类型成员时，CTAD在此上下文中无效，必须显式指定所有模板实参：  

```cpp
#include <utility> // 引入 std::pair

struct Foo
{
    std::pair<int, int> p1{ 1, 2 }; // 正确：显式指定模板实参
    std::pair p2{ 1, 2 };           // 编译错误：此上下文中不可用CTAD
};

int main()
{
    std::pair p3{ 1, 2 };           // 正确：此处可用CTAD
    return 0;
}
```  

CTAD不适用于函数形参  
----------------  

CTAD指类模板*实参*推导而非类模板*形参*推导，故其仅推导模板实参类型，不推导模板形参。  

因此CTAD不可用于函数形参：  

```cpp
#include <iostream>
#include <utility>

void print(std::pair p) // 编译错误：此处不可用CTAD
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    std::pair p { 1, 2 }; // p推导为 std::pair<int, int>
    print(p);
    return 0;
}
```  

此类情况应改用模板：  

```cpp
#include <iostream>
#include <utility>

template <typename T, typename U>
void print(std::pair<T, U> p)
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    std::pair p { 1, 2 }; // p推导为 std::pair<int, int>
    print(p);
    return 0;
}
```  

[下一课 13.15 — 别名模板](Chapter-13/lesson13.15-alias-templates.md)  
[返回主页](/)  
[上一课 13.13 — 类模板](Chapter-13/lesson13.13-class-templates.md)