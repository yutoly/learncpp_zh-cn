7.10 — 跨多文件共享全局常量（使用内联变量）
===============================================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2024年12月14日（首次发布于2020年1月3日）

在某些应用中，某些符号常量（symbolic constants）可能需要在整个代码中使用（而不仅限于单一位置）。这些常量包括不会改变的物理或数学常数（如π或阿伏伽德罗常数），或特定应用的"调校"值（如摩擦系数或重力系数）。与其在每个需要这些常量的文件中重复定义（违反"不要重复自己"原则），更好的做法是在中心位置声明一次并在需要的地方使用。这样，当需要修改时只需改动一处，变更即可全局生效。

全局常量作为内部变量
----------------

C++17之前的解决方案如下：

1. 创建头文件存放常量
2. 在头文件中定义命名空间（详见课程[7.2 — 用户定义命名空间与作用域解析运算符](Chapter-7/lesson7.2-user-defined-namespaces-and-the-scope-resolution-operator.md)）
3. 将常量放入命名空间（确保使用*constexpr*）
4. 在需要的地方\#include该头文件

示例：

constants.h：
```cpp
#ifndef CONSTANTS_H
#define CONSTANTS_H

// 定义存放常量的命名空间
namespace constants
{
    // 默认具有内部链接
    constexpr double pi { 3.14159 };
    constexpr double avogadro { 6.0221413e23 };
    constexpr double myGravity { 9.2 }; // 米/秒²——该行星重力较小
    // ...其他相关常量
}
#endif
```

在.cpp文件中通过作用域解析运算符（::）访问常量：

main.cpp：
```cpp
#include "constants.h" // 将常量复制到当前文件
#include <iostream>

int main()
{
    std::cout << "输入半径: ";
    double radius{};
    std::cin >> radius;

    std::cout << "周长: " << 2 * radius * constants::pi << '\n';
    return 0;
}
```

当头文件被包含进.cpp文件时，这些常量会被复制到该文件。由于const全局变量具有内部链接，每个.cpp文件都拥有独立副本（编译器通常会优化掉这些constexpr变量）。

缺点：
1. 修改常量值需要重新编译所有包含该头文件的文件
2. 若常量体积较大且无法优化，可能占用大量内存

优点：
* 兼容C++17之前版本
* 可在包含该文件的任何翻译单元中用于常量表达式

全局常量作为外部变量
----------------

为避免上述问题，可将常量定义为外部变量：

constants.cpp：
```cpp
#include "constants.h"

namespace constants
{
    // 使用extern确保外部链接
    extern constexpr double pi { 3.14159 };
    extern constexpr double avogadro { 6.0221413e23 };
    extern constexpr double myGravity { 9.2 };
}
```

constants.h：
```cpp
#ifndef CONSTANTS_H
#define CONSTANTS_H

namespace constants
{
    // 前向声明需保持命名空间一致
    extern const double pi;
    extern const double avogadro;
    extern const double myGravity;
}

#endif
```

优点：
* 兼容C++17之前版本
* 单实例存储
* 修改常量只需重新编译constants.cpp

缺点：
* 前向声明与定义需同步维护
* 在定义文件外无法用于常量表达式

C++17全局常量作为内联变量
----------------

通过内联变量（inline variables）可避免重复定义：

constants.h：
```cpp
#ifndef CONSTANTS_H
#define CONSTANTS_H

namespace constants
{
    inline constexpr double pi { 3.14159 }; // 注意inline关键字
    inline constexpr double avogadro { 6.0221413e23 };
    inline constexpr double myGravity { 9.2 };
    // ...其他常量
}
#endif
```

优点：
* 支持所有翻译单元的常量表达式
* 单实例存储

缺点：
* 仅支持C++17及以上
* 修改头文件仍需重新编译包含文件

最佳实践：
* 若编译器支持C++17，优先在头文件中定义inline constexpr全局常量

相关提醒：
* 对constexpr字符串使用std::string_view（详见课程[5.8 — std::string_view简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)）

相关内容：
* 变量作用域、持续时间和链接性总结见课程[7.12 — 作用域、持续时间和链接性总结](Chapter-7/lesson7.12-scope-duration-and-linkage-summary.md)

[下一课 7.11 静态局部变量](Chapter-7/lesson7.11-static-local-variables.md)  
[返回主页](/)  
[上一课 7.9 内联函数与变量](Chapter-7/lesson7.9-inline-functions-and-variables.md)