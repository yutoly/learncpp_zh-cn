17.6 — std::array 与枚举类型
===================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月1日（首次发布于2023年9月11日）  

在课程[16.9 — 使用枚举类型进行数组索引与长度计算](Chapter-16/lesson16.9-array-indexing-and-length-using-enumerators.md)中，我们讨论了数组与枚举类型。现在我们已经掌握了`constexpr std::array`工具，将继续深入讨论并展示更多技巧。  

使用静态断言确保数组初始值数量正确  
----------------  

当使用CTAD（类模板参数推导）初始化`constexpr std::array`时，编译器会根据初始值数量推导数组长度。如果初始值数量少于预期，数组将比预期短，索引访问可能导致未定义行为。例如：  
```
#include <array>
#include <iostream>

enum StudentNames
{
    kenny,    // 0
    kyle,     // 1
    stan,     // 2
    butters,  // 3
    cartman,  // 4
    max_students // 5
};

int main()
{
    constexpr std::array testScores { 78, 94, 66, 77 }; // 错误：仅有4个初始值

    std::cout << "Cartman的分数是" << testScores[StudentNames::cartman] << '\n'; // 无效索引导致未定义行为

    return 0;
}
```  

当`constexpr std::array`的初始值数量可以进行合理性检查时，可以使用静态断言（static_assert）：  
```
#include <array>
#include <iostream>

enum StudentNames
{
    kenny,    // 0
    kyle,     // 1
    stan,     // 2
    butters,  // 3
    cartman,  // 4
    max_students // 5
};

int main()
{
    constexpr std::array testScores { 78, 94, 66, 77 };

    // 确保测试分数数量与学生数量一致
    static_assert(std::size(testScores) == max_students); // 编译错误：static_assert条件不满足

    std::cout << "Cartman的分数是" << testScores[StudentNames::cartman] << '\n';

    return 0;
}
```  

这样，如果后续添加新枚举项但忘记在`testScores`中添加对应初始值，程序将无法编译。您还可以使用静态断言确保两个不同`constexpr std::array`具有相同长度。  

使用constexpr数组优化枚举输入输出  
----------------  

在课程[13.5 — 输入输出运算符重载简介](Chapter-13/lesson13.5-introduction-to-overloading-the-i-o-operators.md)中，我们介绍了枚举项名称输入输出的几种方法。为此我们编写了辅助函数将枚举项与字符串互相转换，这些函数各自维护重复的字符串字面量，并需要专门编写检查逻辑：  
```
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
    if (sv == "cat")   return cat;
    if (sv == "dog")   return dog;
    if (sv == "pig")   return pig;
    if (sv == "whale") return whale;

    return {};
}
```  

这意味着添加新枚举项时需要记得更新这些函数。让我们优化这些函数：当枚举项值从0开始顺序递增时（大多数枚举类型如此），可以使用数组存储各枚举项名称。这允许我们：  
1. 通过枚举值索引数组获取对应名称  
2. 使用循环遍历所有名称，根据索引关联名称与枚举项  

```
#include <array>
#include <iostream>
#include <string>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    // 使用sv后缀使std::array推断类型为std::string_view
    using namespace std::string_view_literals; // 启用sv后缀
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    // 确保为所有颜色定义了字符串
    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    // 使用枚举项索引数组获取名称
    return Color::colorName[static_cast<std::size_t>(color)];
}

// 教导operator<<如何打印Color类型
// std::ostream是std::cout的类型
// 返回类型和参数类型均为引用（防止拷贝）！
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

// 教导operator>>如何通过名称输入Color
// 通过非常量引用传递color以允许修改其值
std::istream& operator>> (std::istream& in, Color::Type& color)
{
    std::string input {};
    std::getline(in >> std::ws, input);

    // 遍历名称列表寻找匹配项
    for (std::size_t index=0; index < Color::colorName.size(); ++index)
    {
        if (input == Color::colorName[index])
        {
            // 找到匹配项后根据索引获取枚举值
            color = static_cast<Color::Type>(index);
            return in;
        }
    }

    // 未找到匹配项，输入无效
    // 将输入流设为失败状态
    in.setstate(std::ios_base::failbit);

    // 提取失败时，operator>>会初始化基础类型为0
    // 取消注释以下行使本运算符执行相同操作
    // color = {};
    return in;
}

int main()
{
    auto shirt{ Color::blue };
    std::cout << "您的衬衫是" << shirt << '\n';

    std::cout << "输入新颜色：";
    std::cin >> shirt;
    if (!std::cin)
        std::cout << "无效输入\n";
    else
        std::cout << "您的衬衫现在是" << shirt << '\n';

    return 0;
}
```  

输出示例：  
```
您的衬衫是blue
输入新颜色：red
您的衬衫现在是red
```  

基于范围的for循环与枚举类型  
----------------  

有时需要遍历枚举类型的枚举项。虽然可以使用整数索引的for循环，但这需要大量将整型索引静态转换为枚举类型：  
```
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    using namespace std::string_view_literals;
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    // 使用for循环遍历所有颜色
    for (int i=0; i < Color::max_colors; ++i )
        std::cout << static_cast<Color::Type>(i) << '\n';

    return 0;
}
```  

遗憾的是，基于范围的for循环无法直接遍历枚举类型的枚举项：  
```
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    using namespace std::string_view_literals;
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    for (auto c: Color::Type) // 编译错误：无法遍历枚举类型
        std::cout << c << '\n';

    return 0;
}
```  

对此有多种创新解决方案。由于可以对数组使用基于范围的for循环，最直接的解决方案是创建包含所有枚举项的`constexpr std::array`并进行遍历。此方法仅在所有枚举项具有唯一值时有效：  
```
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,     // 0
        red,       // 1
        blue,      // 2
        max_colors // 3
    };

    using namespace std::string_view_literals;
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };
    static_assert(std::size(colorName) == max_colors);

    constexpr std::array types { black, red, blue }; // 包含所有枚举项的std::array
    static_assert(std::size(types) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    for (auto c: Color::types) // 正常：可以对std::array使用基于范围的for循环
        std::cout << c << '\n';

    return 0;
}
```  

输出：  
```
black
red
blue
```  

测验  
----------------  

定义一个名为`Animal`的命名空间，其中包含枚举类型：chicken（鸡）、dog（狗）、cat（猫）、elephant（大象）、duck（鸭）、snake（蛇）。同时定义`Data`结构体存储每个动物的名称、腿数和叫声。创建`std::array`存储所有动物的Data，并填充每个动物的数据。  

要求用户输入动物名称，若未找到匹配则提示，否则显示该动物数据，随后显示其他所有动物的数据。示例：  
```
输入动物：dog
狗有4条腿，叫声是woof.

其他动物数据：
鸡有2条腿，叫声是cluck.
猫有4条腿，叫声是meow.
大象有4条腿，叫声是pawoo.
鸭有2条腿，叫声是quack.
蛇有0条腿，叫声是hissss.
```  

```
输入动物：frog
未找到该动物.

其他动物数据：
鸡有2条腿，叫声是cluck.
狗有4条腿，叫声是woof.
猫有4条腿，叫声是meow.
大象有4条腿，叫声是pawoo.
鸭有2条腿，叫声是quack.
蛇有0条腿，叫声是hissss.
```  

问题 #1  
```
#include <array>
#include <iostream>
#include <string>
#include <string_view>

namespace Animal
{
    enum Type
    {
        chicken,
        dog,
        cat,
        elephant,
        duck,
        snake,
        max_animals
    };

    struct Data
    {
        std::string_view name{};
        int legs{};
        std::string_view sound{};
    };

    constexpr std::array types { chicken, dog, cat, elephant, duck, snake };
    constexpr std::array data {
        Data{ "chicken",    2, "cluck" },
        Data{ "dog",        4, "woof" },
        Data{ "cat",        4, "meow" },
        Data{ "elephant",   4, "pawoo" },
        Data{ "duck",       2, "quack" },
        Data{ "snake",      0, "hissss" },
    };

    static_assert(std::size(types) == max_animals);
    static_assert(std::size(data) == max_animals);
}

std::istream& operator>> (std::istream& in, Animal::Type& animal)
{
    std::string input {};
    std::getline(in >> std::ws, input);

    for (std::size_t index=0; index < Animal::data.size(); ++index)
    {
        if (input == Animal::data[index].name)
        {
            animal = static_cast<Animal::Type>(index);
            return in;
        }
    }

    in.setstate(std::ios_base::failbit);
    return in;
}

void printAnimalData(Animal::Type type)
{
    const Animal::Data& animal { Animal::data[type] };
    std::cout << animal.name << "有" << animal.legs << "条腿，叫声是" << animal.sound << ".\n";    
}

int main()
{
    std::cout << "输入动物：";
    Animal::Type type{};
    std::cin >> type;

    if (!std::cin)
    {
        std::cin.clear();
        std::cout << "未找到该动物.\n";
        type = Animal::max_animals; // 设为无效值避免匹配
    }
    else
        printAnimalData(type);

    std::cout << "\n其他动物数据：\n";
    for (auto a : Animal::types)
    {
        if (a != type)
            printAnimalData(a);
    }

    return 0;
}
```  

[下一课 17.7 C风格数组简介](Chapter-17/lesson17.7-introduction-to-c-style-arrays.md)  
[返回主页](/)  
[上一课 17.5 通过std::reference_wrapper实现引用数组](Chapter-17/lesson17.5-arrays-of-references-via-stdreference_wrapper.md)