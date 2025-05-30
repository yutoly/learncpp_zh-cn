13.4 — 枚举类型与字符串的相互转换  
================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月13日（首次发布于2024年3月25日）  

在上一课（[13.3 — 无作用域枚举项的整型转换](Chapter-13/lesson13.3-unscoped-enumerator-integral-conversions.md)）中，我们展示了如下示例：  

```cpp
#include <iostream>

enum Color
{
    black, // 0
    red,   // 1
    blue,  // 2
};

int main()
{
    Color shirt{ blue };

    std::cout << "Your shirt is " << shirt << '\n';

    return 0;
}
```  

这将输出：  

```
Your shirt is 2
```  

由于 `operator<<` 无法识别如何打印 `Color` 类型，编译器会将 `Color` 隐式转换为整数值后输出。  

多数情况下，将枚举作为整数值（如 `2`）打印并非预期效果。我们通常希望打印枚举项对应的名称（例如 `blue`）。C++ 未提供内置解决方案，需自行实现。  

获取枚举项名称  
----------------  

获取枚举项名称的典型方法是编写函数：传入枚举项，返回对应的字符串名称。这需要建立枚举项与字符串的映射关系。  

常见实现方式有两种：  

在课程 [8.5 — switch 语句基础](Chapter-8/lesson8.5-switch-statement-basics.md) 中，我们提到 switch 语句可处理整型或枚举值。下例使用 switch 匹配枚举项并返回对应的颜色字符串字面量：  

```cpp
#include <iostream>
#include <string_view>

enum Color
{
    black,
    red,
    blue,
};

constexpr std::string_view getColorName(Color color)
{
    switch (color)
    {
    case black: return "black";
    case red:   return "red";
    case blue:  return "blue";
    default:    return "???";
    }
}

int main()
{
    constexpr Color shirt{ blue };

    std::cout << "Your shirt is " << getColorName(shirt) << '\n';

    return 0;
}
```  

输出：  

```
Your shirt is blue
```  

此例中，我们基于传入的枚举值 `color` 进行匹配。每个 case 分支返回对应的颜色名称（C 风格字符串字面量），该字面量隐式转换为 `std::string_view` 返回。default 分支返回 `"???"` 处理意外输入。  

重要提示  
----------------  
C 风格字符串字面量存在于整个程序生命周期，因此返回指向此类字面量的 `std::string_view` 是安全的。该函数声明为 constexpr 以便在常量表达式中使用颜色名称。  

相关内容  
----------------  
常量表达式函数详见课程 [F.1 — 常量表达式函数](Chapter-F/lessonF.1-constexpr-functions.md)。  

虽然此方法可获取枚举项名称，但使用 `std::cout << getColorName(shirt)` 不如 `std::cout << shirt` 简洁。我们将在课程 [13.5 — 重载 I/O 运算符简介](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md) 中实现枚举类型的直接输出。  

第二种映射方案是使用数组，详见课程 [17.6 — std::array 与枚举](Chapter-17/lesson17.6-stdarray-and-enumerations.md)。  

无作用域枚举的输入  
----------------  

考虑以下输入场景：定义 `Pet` 枚举类型。由于 `Pet` 是程序自定义类型，语言无法通过 `std::cin` 直接输入：  

```cpp
#include <iostream>

enum Pet
{
    cat,   // 0
    dog,   // 1
    pig,   // 2
    whale, // 3
};

int main()
{
    Pet pet { pig };
    std::cin >> pet; // 编译错误：std::cin 无法识别 Pet 类型

    return 0;
}
```  

简单解决方案是读取整数，再通过 `static_cast` 转换为对应枚举项：  

```cpp
#include <iostream>
#include <string_view>

enum Pet
{
    cat,   // 0
    dog,   // 1
    pig,   // 2
    whale, // 3
};

constexpr std::string_view getPetName(Pet pet)
{
    switch (pet)
    {
    case cat:   return "cat";
    case dog:   return "dog";
    case pig:   return "pig";
    case whale: return "whale";
    default:    return "???";
    }
}

int main()
{
    std::cout << "Enter a pet (0=cat, 1=dog, 2=pig, 3=whale): ";

    int input{};
    std::cin >> input; // 输入整数

    if (input < 0 || input > 3)
        std::cout << "You entered an invalid pet\n";
    else
    {
        Pet pet{ static_cast<Pet>(input) }; // 将整数转换为 Pet
        std::cout << "You entered: " << getPetName(pet) << '\n';
    }

    return 0;
}
```  

此方案可行但较繁琐。注意：仅在确认 `input` 值有效时才应执行 `static_cast<Pet>(input)`。  

从字符串获取枚举值  
----------------  

更优方案是让用户输入枚举项名称（如 "pig"），再将其转换为对应的 `Pet` 枚举项。这需解决两个问题：  

1. 无法对字符串使用 switch 语句，需改用 if 语句链  
2. 用户输入无效字符串时的处理方案：添加表示"无效"的枚举项或使用 `std::optional`  

相关内容  
----------------  
`std::optional` 详见课程 [12.15 — std::optional](Chapter-12/lesson12.15-stdoptional.md)。  

```cpp
#include <iostream>
#include <optional> // 引入 std::optional
#include <string>
#include <string_view>

enum Pet
{
    cat,   // 0
    dog,   // 1
    pig,   // 2
    whale, // 3
};

constexpr std::string_view getPetName(Pet pet)
{
    switch (pet)
    {
    case cat:   return "cat";
    case dog:   return "dog";
    case pig:   return "pig";
    case whale: return "whale";
    default:    return "???";
    }
}

constexpr std::optional<Pet> getPetFromString(std::string_view sv)
{
    // 使用 if 语句进行字符串匹配
    if (sv == "cat")   return cat;
    if (sv == "dog")   return dog;
    if (sv == "pig")   return pig;
    if (sv == "whale") return whale;
    
    return {}; // 返回空值
}

int main()
{
    std::cout << "Enter a pet: cat, dog, pig, or whale: ";
    std::string s{};
    std::cin >> s;
        
    std::optional<Pet> pet { getPetFromString(s) };

    if (!pet)
        std::cout << "You entered an invalid pet\n";
    else
        std::cout << "You entered: " << getPetName(*pet) << '\n';

    return 0;
}
```  

此方案通过 if 语句链匹配字符串。若匹配成功则返回对应枚举项，否则返回 `{}`（表示"无值"）。  

进阶提示  
----------------  
上述方案仅支持小写匹配。如需不区分大小写，可用以下函数将输入转为小写：  

```cpp
#include <algorithm> // 引入 std::transform
#include <cctype>    // 引入 std::tolower
#include <iterator>  // 引入 std::back_inserter
#include <string>
#include <string_view>

// 将字符串视图转为小写 std::string
std::string toASCIILowerCase(std::string_view sv)
{
    std::string lower{};
    std::transform(sv.begin(), sv.end(), std::back_inserter(lower),
        [](char c)
        { 
            return static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        });
    return lower;
}
```  

此函数通过 lambda 表达式遍历 `std::string_view`，使用 `std::tolower` 转换字符后追加到结果字符串。  

相关内容  
----------------  
Lambda 表达式详见课程 [20.6 — Lambda 表达式（匿名函数）简介](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)。  

与输出类似，更优方案是实现 `std::cin >> pet`，详见课程 [13.5 — 重载 I/O 运算符简介](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md)。  

[下一课 13.5 重载 I/O 运算符简介](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md)  
[返回主页](/)  
[上一课 13.3 无作用域枚举项的整型转换](Chapter-13/lesson13.3-unscoped-enumerator-integral-conversions.md)