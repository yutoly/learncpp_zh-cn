13.5 — 运算符重载入门：I/O 运算符重载  
=====================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年3月25日（首次发布于2024年10月28日）  

在上一课（[13.4 — 枚举类型与字符串的互转](Chapter-13/lesson13.4-converting-an-enumeration-to-and-from-a-string.md)）中，我们展示了通过函数将枚举转换为对应字符串的示例：  

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

虽然该示例可行，但存在两个缺点：  
1. 需要记忆获取枚举项名称的函数名  
2. 调用函数会增加输出语句的冗余  

理想情况下，若能教会`operator<<`直接输出枚举类型，就能实现`std::cout << shirt`的简洁形式。  

运算符重载入门  
----------------  

在课程[11.1 — 函数重载入门](Chapter-11/lesson11.1-introduction-to-function-overloading.md)中，我们介绍了函数重载（function overloading），允许为不同数据类型创建同名函数。类似地，C++支持**运算符重载（operator overloading）**，可为用户自定义类型定义运算符行为。  

基本运算符重载规则：  
* 使用运算符名称作为函数名  
* 按左到右顺序为每个操作数定义参数类型（至少一个参数为用户定义类型）  
* 定义合理的返回类型  
* 使用return返回运算结果  

当编译器遇到用户定义类型的运算符时，会查找对应的重载函数。例如表达式`x + y`会查找`operator+(x, y)`函数。  

> **相关内容**  
> 运算符重载的详细讨论见[第21章](https://www.learncpp.com#Chapter21)  

> **进阶阅读**  
> 运算符也可作为左操作数的成员函数重载，详见课程[21.5 — 使用成员函数重载运算符](Chapter-21/lesson21.5-overloading-operators-using-member-functions.md)  

重载`operator<<`输出枚举  
----------------  

首先回顾`operator<<`的工作机制：表达式`std::cout << 5`中，`std::cout`属于`std::ostream`类型（标准库定义的用户类型），`5`是`int`类型字面量。编译器会查找能处理`std::ostream`和`int`参数的`operator<<`重载。  

为`Color`枚举实现`operator<<`重载：  

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

// 重载operator<<以输出Color类型
// std::ostream是std::cout、std::cerr等的类型
// 参数和返回类型使用引用（避免拷贝）
std::ostream& operator<<(std::ostream& out, Color color)
{
    out << getColorName(color); // 向输出流输出颜色名称
    return out;                 // 常规返回左操作数

    // 可简化为单行：return out << getColorName(color)
}

int main()
{
	Color shirt{ blue };
	std::cout << "Your shirt is " << shirt << '\n'; // 直接输出枚举

	return 0;
}
```  

输出：  
```
Your shirt is blue
```  

解析重载函数：  
* 函数名为`operator<<`  
* 左参数为`std::ostream&`类型输出流（非常量引用）  
* 右参数为`Color`枚举类型  
* 返回类型`std::ostream&`以支持链式调用  

实现逻辑：  
* 使用`std::ostream`已有的`operator<<`输出`std::string_view`  
* 参数`out`可适配任意输出流（如`std::cerr`）  
* 调用`std::cout << shirt`时，`operator<<`函数接收`std::cout`作为`out`参数，`shirt`作为`color`参数  

重载`operator>>`输入枚举  
----------------  

类似地，可重载`operator>>`实现枚举输入：  

```cpp
#include <iostream>
#include <limits>
#include <optional>
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
    if (sv == "cat")   return cat;
    if (sv == "dog")   return dog;
    if (sv == "pig")   return pig;
    if (sv == "whale") return whale;

    return {};
}

// pet是输入/输出参数
std::istream& operator>>(std::istream& in, Pet& pet)
{
    std::string s{};
    in >> s; // 获取用户输入

    std::optional<Pet> match { getPetFromString(s) };
    if (match) // 匹配成功
    {
        pet = *match; // 解引用optional获取枚举项
        return in;
    }

    // 输入无效时设置流失败状态
    in.setstate(std::ios_base::failbit);
    
    // 提取失败时，operator>>会零初始化基础类型
    // 取消注释以下代码实现相同行为
    // pet = {};

    return in;
}

int main()
{
    std::cout << "Enter a pet: cat, dog, pig, or whale: ";
    Pet pet{};
    std::cin >> pet;
        
    if (std::cin) // 匹配成功
        std::cout << "You chose: " << getPetName(pet) << '\n';
    else
    {
        std::cin.clear(); // 重置输入流
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Your pet was not valid\n";
    }

    return 0;
}
```  

关键差异：  
* 左参数类型为`std::istream&`  
* `pet`参数为非常量引用（输出参数）  
* 用户输入无效时设置流的`failbit`状态  

> **核心要点**  
> `pet`作为输出参数（out parameter），详见课程[12.13 — 输入输出参数](Chapter-12/lesson12.13-in-and-out-parameters.md)  

> **相关内容**  
> 在课程[17.6 — std::array与枚举](Chapter-17/lesson17.6-stdarray-and-enumerations.md)中，我们将展示如何使用`std::array`简化输入/输出运算符的实现。  

[下一课 13.6 作用域枚举（枚举类）](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)  
[返回主页](/)  
[上一课 13.4 枚举类型与字符串的互转](Chapter-13/lesson13.4-converting-an-enumeration-to-and-from-a-string.md)