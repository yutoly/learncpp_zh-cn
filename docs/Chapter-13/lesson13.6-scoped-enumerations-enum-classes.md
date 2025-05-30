13.6 — 限定作用域枚举（enum classes）
==========================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2015年4月23日，下午4:22（太平洋夏令时）
2025年2月11日修订

虽然非限定作用域枚举（unscoped enumeration）在C++中是独立类型，但它们不具备类型安全性，某些情况下允许执行无意义的操作。考虑以下情况：
```
#include <iostream>

int main()
{
    enum Color // 非限定作用域枚举
    {
        red,
        blue,
    };

    enum Fruit
    {
        banana,
        apple,
    };
	
    Color color { red };
    Fruit fruit { banana };

    if (color == fruit) // 编译器将color和fruit作为整数比较
        std::cout << "color和fruit相等\n"; // 结果判定相等！
    else
        std::cout << "color和fruit不相等\n";

    return 0;
}
```
输出结果：
```
color和fruit相等
```
当比较`color`和`fruit`时，编译器首先检查是否支持`Color`与`Fruit`的比较。由于不支持，编译器会尝试将`Color`和/或`Fruit`转换为整数寻找匹配方式。最终编译器决定将两者转为整数比较。由于`color`和`fruit`都对应整数值`0`，因此判定相等。这在语义上不合理，因为`color`和`fruit`属于不同枚举且本不该比较。标准枚举无法简单防止此类问题。

鉴于此类问题以及命名空间污染问题（定义在全局作用域的非限定作用域枚举会将其枚举项放入全局命名空间），C++设计者认为需要更简洁的枚举解决方案。

限定作用域枚举
----------------
解决方案是**限定作用域枚举（scoped enumeration）**（在C++中常称为**enum class**，原因后述）。

限定作用域枚举与非限定作用域枚举（[13.2 — 非限定作用域枚举](Chapter-13/lesson13.2-unscoped-enumerations.md)）类似，但有两大区别：不隐式转换为整数，且枚举项*仅*置于枚举自身的作用域内（而非枚举定义所在的作用域）。

定义限定作用域枚举需使用关键字`enum class`，其余定义方式与非限定作用域枚举相同。示例如下：
```
#include <iostream>
int main()
{
    enum class Color // "enum class"定义此为限定作用域枚举
    {
        red,  // red属于Color的作用域
        blue,
    };

    enum class Fruit
    {
        banana, // banana属于Fruit的作用域
        apple,
    };

    Color color { Color::red };   // 注意：red不可直接访问，需使用Color::red
    Fruit fruit { Fruit::banana }; // 注意：banana不可直接访问，需使用Fruit::banana
	
    if (color == fruit) // 编译错误：编译器无法比较不同类型Color和Fruit
        std::cout << "color和fruit相等\n";
    else
        std::cout << "color和fruit不相等\n";

    return 0;
}
```
此程序在第19行产生编译错误，因为限定作用域枚举不会转换为可与其他类型比较的类型。

> **补充说明**  
> `class`关键字（与`static`关键字）是C++中重载最多的关键词之一，其含义随上下文变化。虽然限定作用域枚举使用`class`关键字，但不属于"类类型"（该术语专用于struct、class和union）。  
>  
> 此上下文中`enum struct`与`enum class`功能完全相同，但不符合语言习惯，应避免使用。

限定作用域枚举定义独立作用域
----------------
非限定作用域枚举将枚举项置于与枚举自身相同的作用域，而限定作用域枚举将枚举项*仅*置于枚举的作用域内。换言之，限定作用域枚举为其枚举项提供类似命名空间的功能。这种内置命名空间机制有助于减少全局命名空间污染，以及限定作用域枚举用于全局作用域时的命名冲突风险。

访问限定作用域枚举项需通过枚举名前缀（如同访问命名空间成员）：
```
#include <iostream>

int main()
{
    enum class Color // "enum class"定义此为限定作用域枚举
    {
        red,  // red属于Color的作用域
        blue,
    };

    std::cout << red << '\n';         // 编译错误：当前作用域未定义red
    std::cout << Color::red << '\n';  // 编译错误：std::cout无法直接输出（不会隐式转为int）

    Color color { Color::blue }; // 正确

    return 0;
}
```

由于限定作用域枚举为枚举项提供隐式命名空间，通常无需将其放入其他作用域（如命名空间），除非存在其他必要原因（否则会造成冗余）。

限定作用域枚举不隐式转换为整数
----------------
与非限定作用域枚举项不同，限定作用域枚举项不会隐式转换为整数。多数情况下这是有益的，因为此类转换通常不合理，且有助于防止语义错误（如比较不同枚举的枚举项，或表达式`red + 5`）。

注意：相同限定作用域枚举内的枚举项仍可比较（因属同类型）：
```
#include <iostream>
int main()
{
    enum class Color
    {
        red,
        blue,
    };

    Color shirt { Color::red };

    if (shirt == Color::red) // Color与Color的比较有效
        std::cout << "衬衫是红色的！\n";
    else if (shirt == Color::blue)
        std::cout << "衬衫是蓝色的！\n";

    return 0;
}
```

少数场景中需将限定作用域枚举项视为整数值。此时可通过`static_cast`显式转换。C++23中更推荐使用`std::to_underlying()`（定义于\<utility\>头文件），该函数将枚举项转换为枚举底层类型的值。
```
#include <iostream>
#include <utility> // 引入std::to_underlying()（C++23）

int main()
{
    enum class Color
    {
        red,
        blue,
    };

    Color color { Color::blue };

    std::cout << color << '\n';                   // 无效：无隐式转换为int
    std::cout << static_cast<int>(color) << '\n'; // 显式转为int，输出1
    std::cout << std::to_underlying(color) << '\n'; // 转为底层类型，输出1（C++23）

    return 0;
}
```

反之，也可用`static_cast`将整数转为限定作用域枚举项（适用于处理用户输入）：
```
#include <iostream>

int main()
{
    enum class Pet
    {
        cat,   // 赋值0
        dog,   // 赋值1
        pig,   // 赋值2
        whale, // 赋值3
    };

    std::cout << "输入宠物编号 (0=猫,1=狗,2=猪,3=鲸): ";

    int input{};
    std::cin >> input; // 输入整数

    Pet pet{ static_cast<Pet>(input) }; // 将整数static_cast为Pet类型

    return 0;
}
```
自C++17起，可使用整数值直接列表初始化限定作用域枚举（无需static_cast，且不同于非限定作用域枚举，无需指定底层类型）：
```
   // 沿用上例Pet枚举
   Pet pet { 1 }; // 正确
```

> **最佳实践**  
> 除非有充分理由，否则优先选用限定作用域枚举而非非限定作用域枚举。

尽管限定作用域枚举有诸多优势，非限定作用域枚举在C++中仍广泛使用，因为某些场景需要隐式转换为int（频繁使用static_cast会降低可读性），且不需要额外命名空间。

简化限定作用域枚举项到整数的转换（高级技巧）
----------------
限定作用域枚举虽好，但缺少隐式整数转换有时带来不便。若需频繁将限定作用域枚举转为整数（例如将枚举项用作数组索引），每次使用static_cast会显著增加代码冗余。

若需简化转换过程，可重载一元运算符`operator+`实现转换：
```
#include <iostream>
#include <type_traits> // 引入std::underlying_type_t

enum class Animals
{
    chicken,  // 0
    dog,      // 1
    cat,      // 2
    elephant, // 3
    duck,     // 4
    snake,    // 5

    maxAnimals,
};

// 重载一元+运算符将枚举转为底层类型
// 改编自 https://stackoverflow.com/a/42198760，感谢Pixelchemist的创意
// C++23中可 #include <utility> 并返回 std::to_underlying(a)
template <typename T>
constexpr auto operator+(T a) noexcept
{
    return static_cast<std::underlying_type_t<T>>(a);
}

int main()
{
    std::cout << +Animals::elephant << '\n'; // 使用一元运算符+将Animals::elephant转为整数
    return 0;
}
```
输出：
```
3
```
此方法在避免意外隐式转换的同时，为显式按需转换提供了便捷途径。

`using enum`语句（C++20）
----------------
C++20引入的`using enum`语句可将枚举的所有枚举项导入当前作用域。配合enum class类型使用时，可直接访问枚举项而无需枚举名前缀。

当存在大量重复前缀时（如switch语句中）特别有用：
```
#include <iostream>
#include <string_view>

enum class Color
{
    black,
    red,
    blue,
};

constexpr std::string_view getColor(Color color)
{
    using enum Color; // 将Color所有枚举项导入当前作用域（C++20）
    // 现在可不加Color::前缀直接访问Color枚举项

    switch (color)
    {
    case black: return "黑色"; 
    case red:   return "红色";
    case blue:  return "蓝色";
    default:    return "???";
    }
}

int main()
{
    Color shirt{ Color::blue };

    std::cout << "您的衬衫是" << getColor(shirt) << "色的\n";
    return 0;
}
```
上例中，`Color`是enum class，通常需使用完全限定名（如`Color::blue`）。但在`getColor()`函数内，通过`using enum Color;`语句可直接访问枚举项，省去switch语句中大量冗余前缀。

测验
----------------
**问题1**  
定义名为Animal的enum class，包含以下动物：pig（猪）、chicken（鸡）、goat（山羊）、cat（猫）、dog（狗）、duck（鸭）。编写函数getAnimalName()，接收Animal参数并通过switch语句返回动物名称的std::string_view（C++14中使用std::string）。另编写函数printNumberOfLegs()，通过switch语句打印每种动物的腿数。确保两函数均包含打印错误信息的default分支。在main()中用cat和chicken调用printNumberOfLegs()，输出如下：
```
一只猫有4条腿。
一只鸡有2条腿。
```

```
#include <iostream>
#include <string_view> // C++17
//#include <string> // C++14

enum class Animal
{
    pig,
    chicken,
    goat,
    cat,
    dog,
    duck,
};

constexpr std::string_view getAnimalName(Animal animal) // C++17
// const std::string getAnimalName(Animal animal) // C++14
{
    // C++20支持环境下可使用 `using enum Animal` 减少Animal前缀冗余
    switch (animal)
    {
        case Animal::chicken:
            return "鸡";
        case Animal::duck:
            return "鸭";
        case Animal::pig:
            return "猪";
        case Animal::goat:
            return "山羊";
        case Animal::cat:
            return "猫";
        case Animal::dog:
            return "狗";

        default:
            return "???";
    }
}

void printNumberOfLegs(Animal animal)
{
    std::cout << "一只" << getAnimalName(animal) << "有";

    // C++20支持环境下可使用 `using enum Animal` 减少Animal前缀冗余
    switch (animal)
    {
        case Animal::chicken:
        case Animal::duck:
            std::cout << 2;
            break;

        case Animal::pig:
        case Animal::goat:
        case Animal::cat:
        case Animal::dog:
            std::cout << 4;
            break;

        default:
            std::cout << "???";
            break;
    }

    std::cout << "条腿。\n";
}

int main()
{
    printNumberOfLegs(Animal::cat);
    printNumberOfLegs(Animal::chicken);
    return 0;
}
```

[下一课 13.7 结构体、成员与成员选择简介](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)  
[返回主页](/)  
[上一课 13.5 重载I/O运算符简介](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md)