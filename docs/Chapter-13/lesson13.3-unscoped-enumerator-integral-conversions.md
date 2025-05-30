13.3 — 非限定作用域枚举的整型转换  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年1月18日（首次发布于2024年7月31日）  

在前一课程（[13.2 — 非限定作用域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)）中，我们提到枚举器是符号常量。当时未说明的是，这些枚举器的值属于整型（integral type）。

这与字符类型（[4.11 — 字符](Chapter-4/lesson4.11-chars.md)）的情况类似。考虑以下代码：

```cpp
char ch { 'A' };
```

字符实际上是1字节的整型值，字符`'A'`会被转换为整型值（本例中为`65`）并存储。

定义枚举时，每个枚举器会根据其在列表中的位置自动关联一个整数值。默认情况下，首个枚举器赋值为`0`，后续每个枚举器的值递增1：

```cpp
enum Color
{
    black,   // 0
    red,     // 1
    blue,    // 2
    green,   // 3
    white,   // 4
    cyan,    // 5
    yellow,  // 6
    magenta, // 7
};

int main()
{
    Color shirt{ blue }; // shirt实际存储整型值2
    return 0;
}
```

可显式定义枚举器的值。这些整数值可为正负，也可与其他枚举器共享相同值。未显式定义的枚举器将获得前一个枚举器值加1：

```cpp
enum Animal
{
    cat = -3,    // 允许负值
    dog,         // -2
    pig,         // -1
    horse = 5,
    giraffe = 5, // 与horse共享相同值
    chicken,     // 6 
};
```

本例中，`horse`和`giraffe`被赋予相同值。此时枚举器将失去区分性——`horse`和`giraffe`可互换。虽然C++允许此操作，但通常应避免在同一枚举中为不同枚举器赋相同值。

多数情况下默认值即符合需求，无特殊原因无需自定义。

> **最佳实践**  
> 除非有充分理由，否则避免显式指定枚举器值。

枚举的值初始化  
----------------

若枚举进行零初始化（值初始化时发生），即使无对应枚举器，该枚举仍会被赋予`0`值：

```cpp
#include <iostream>

enum Animal
{
    cat = -3,    // -3
    dog,         // -2
    pig,         // -1
    // 注意：列表中无值为0的枚举器
    horse = 5,   // 5
    giraffe = 5, // 5
    chicken,     // 6 
};

int main()
{
    Animal a {}; // 值初始化将a零初始化为0
    std::cout << a; // 输出0
    return 0;
}
```

这会引发两个语义后果：
1. 若有值为0的枚举器，值初始化会默认使用该枚举器的含义。建议将代表最佳默认含义的枚举器设为0值。
2. 若无值为0的枚举器，值初始化易创建语义无效的枚举。建议添加值为0的"invalid"或"unknown"枚举器。

> **最佳实践**  
> 让值为0的枚举器代表最佳默认含义。若无合适默认，添加值为0的"invalid"或"unknown"枚举器以明确处理该状态。

非限定作用域枚举隐式转换为整型  
----------------

虽然枚举存储整型值，但不被视为整型（属复合类型）。非限定作用域枚举可隐式转换为整型值。因枚举器是编译时常量，此为constexpr转换（见[10.4 — 窄化转换、列表初始化与constexpr初始化式](Chapter-10/lesson10.4-narrowing-conversions-list-initialization-and-constexpr-initializers.md)）。

考虑以下程序：

```cpp
#include <iostream>

enum Color
{
    black,  // 0
    red,    // 1
    blue,   // 2
    green,  // 3
    white,  // 4
    cyan,   // 5
    yellow, // 6
    magenta,// 7
};

int main()
{
    Color shirt{ blue };
    std::cout << "Your shirt is " << shirt << '\n'; // 输出2
    return 0;
}
```

编译器首先尝试匹配枚举类型的函数或运算符。若未找到，则将枚举隐式转换为整型后处理。

> **相关内容**  
> 枚举转字符串详见[13.4 — 枚举与字符串的互转](Chapter-13/lesson13.4-converting-an-enumeration-to-and-from-a-string.md)  
> 枚举输出定制详见[13.5 — 重载I/O运算符简介](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md)

枚举大小与底层类型  
----------------

枚举值的整型类型称为**底层类型（underlying type）**或**基类型（base）**。非限定作用域枚举的底层类型由实现定义，通常为int，必要时可能使用更大类型。

可显式指定枚举的底层类型（必须为整型）：

```cpp
#include <cstdint>  // 包含std::int8_t
#include <iostream>

enum Color : std::int8_t // 指定8位整型为底层类型
{
    black,
    red,
    blue,
};

int main()
{
    Color c{ black };
    std::cout << sizeof(c) << '\n'; // 输出1（字节）
    return 0;
}
```

> **最佳实践**  
> 仅在必要时指定枚举的底层类型。

> **警告**  
> 因`std::int8_t`和`std::uint8_t`通常是char的别名，用其作为基类型可能导致枚举器以字符形式输出。

整型到枚举的转换  
----------------

整型不能隐式转换为非限定作用域枚举。两种解决方案：

1. 使用`static_cast`显式转换：
```cpp
enum Pet
{
    cat, dog, pig, whale
};

int main()
{
    Pet pet { static_cast<Pet>(2) }; // 整型2转Pet
    pet = static_cast<Pet>(3);       // 转换为whale
    return 0;
}
```

2. C++17起，若枚举有显式基类型，允许用整型进行列表初始化：
```cpp
enum Pet: int
{
    cat, dog, pig, whale
};

int main()
{
    Pet pet1 { 2 }; // 合法（C++17）
    Pet pet2 (2);   // 错误：不能直接初始化
    Pet pet3 = 2;   // 错误：不能复制初始化
    return 0;
}
```

测验时间  
----------------

**问题1**  
判断真假。枚举器可被赋予：

* 整数值  
  
<details><summary>答案</summary>真</details>  

* 未显式值  
  
<details><summary>答案</summary>真（默认前值+1，首项0）</details>  

* 浮点值  
  
<details><summary>答案</summary>假</details>  

* 负值  
  
<details><summary>答案</summary>真</details>  

* 非唯一值  
  
<details><summary>答案</summary>真</details>  

* 先前枚举器的值（如magenta = red）  
  
<details><summary>答案</summary>真（通常无必要）</details>  

* 非constexpr值  
  
<details><summary>答案</summary>假（枚举器必须为constexpr）</details>  

[下一课 13.4 枚举与字符串的互转](Chapter-13/lesson13.4-converting-an-enumeration-to-and-from-a-string.md)  
[返回主页](/)  
[上一课 13.2 非限定作用域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)