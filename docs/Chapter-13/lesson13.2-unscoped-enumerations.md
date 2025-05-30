13.2 — 无作用域枚举  
=============================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月28日（首次发布于2007年6月19日）  

C++包含许多有用的基础类型和复合类型（已在课程[4.1 — 基础数据类型简介](Chapter-4/lesson4.1-introduction-to-fundamental-data-types.md)和[12.1 — 复合数据类型简介](Chapter-12/lesson12.1-introduction-to-compound-data-types.md)中介绍）。但这些类型有时无法满足特定需求。例如：编写需要跟踪苹果颜色（红、黄、绿）或衬衫颜色（预设颜色列表）的程序时，若仅使用基础类型该如何实现？您可能使用整数值配合隐式映射（0=红，1=绿，2=蓝）：
```
int main()
{
    int appleColor{ 0 }; // 苹果是红色
    int shirtColor{ 1 }; // 衬衫是绿色

    return 0;
}
```
但这种方法缺乏直观性，且存在[5.2 — 字面量](Chapter-1/lesson1.9-introduction-to-literals-and-operators.md)中讨论的"魔数"问题。通过符号常量可消除魔数：
```
constexpr int red{ 0 };
constexpr int green{ 1 };
constexpr int blue{ 2 };

int main()
{
    int appleColor{ red };
    int shirtColor{ green };

    return 0;
}
```
虽然可读性有所提升，但程序员仍需推断`appleColor`和`shirtColor`（int类型）应使用颜色符号常量集合中的值（可能定义在其他文件）。使用类型别名可进一步明确：
```
using Color = int; // 定义Color类型别名

// 以下颜色值应配合Color类型使用
constexpr Color red{ 0 };
constexpr Color green{ 1 };
constexpr Color blue{ 2 };

int main()
{
    Color appleColor{ red };
    Color shirtColor{ green };

    return 0;
}
```
此时读者仍需理解这些符号常量需配合`Color`类型使用，但至少类型名称具有唯一性。由于`Color`仅是int别名，仍无法强制正确使用颜色值：
```
Color eyeColor{ 8 }; // 语法有效，语义无意义
```
调试时变量仅显示整数值（如0），而非符号含义（如red），增加调试难度。  

**枚举类型**  
**枚举（enumeration）**（也称枚举类型或enum）是一种复合数据类型，其值限定为命名的符号常量集合（称为枚举成员）。  

C++支持两种枚举：无作用域枚举（本节内容）和有作用域枚举（后续讲解）。由于枚举是程序定义类型[13.1 — 程序定义类型简介](Chapter-13/lesson13.1-introduction-to-program-defined-user-defined-types.md)，使用前需完整定义（仅前向声明不够）。  

**无作用域枚举**  
通过`enum`关键字定义无作用域枚举。以下示例定义包含颜色值的无作用域枚举：  
```
// 定义名为Color的无作用域枚举
enum Color
{
    // 枚举成员定义该类型所有可能值
    // 各成员用逗号分隔（非分号）
    red,
    green,
    blue, // 结尾逗号可选但推荐
}; // 枚举定义必须以分号结尾

int main()
{
    // 定义Color枚举类型变量
    Color apple { red };   // 苹果为红色
    Color shirt { green }; // 衬衫为绿色
    Color cup { blue };    // 杯子为蓝色

    Color socks { white }; // 错误：white不是Color的枚举成员
    Color hat { 2 };       // 错误：2不是Color的枚举成员

    return 0;
}
```
使用`enum`关键字定义名为`Color`的无作用域枚举。大括号内定义`Color`的枚举成员：`red`、`green`和`blue`，这些成员限定了该类型允许的值。每个成员用逗号分隔，最后成员可加逗号。通常每个成员独占一行，但简单情况可单行排列。`Color`类型定义以分号结束。  

`main()`中实例化三个`Color`变量：`apple`初始化为`red`，`shirt`为`green`，`cup`为`blue`。注意枚举类型初始化器必须是该类型的枚举成员。`socks`和`hat`因使用`white`和`2`导致编译错误。枚举成员隐含为constexpr。  

**术语回顾**  
- **枚举/枚举类型**：程序定义的类型（如Color）  
- **枚举成员**：枚举的具名值（如red）  

**命名规范**  
枚举类型名首字母大写（同其他程序定义类型）。警告：现代C++应避免无名枚举。枚举成员必须命名，常见命名方式包括：小写（red）、首字母大写（Red）、全大写（RED）、带前缀全大写（COLOR_RED）或k前缀（kColorRed）。现代C++指南建议避免全大写（易与宏冲突）和首字母大写（保留给类型名）。  

**最佳实践**  
枚举类型名首字母大写，枚举成员名小写开头。  

**枚举类型独特性**  
每个枚举类型都是**独特类型**，编译器可区分不同枚举类型。不同枚举类型的成员不能混用：  
```
enum Pet { cat, dog, pig, whale };
enum Color { black, red, blue };

int main()
{
    Pet myPet { black }; // 错误：black不是Pet的成员
    Color shirt { pig }; // 错误：pig不是Color的成员

    return 0;
}
```
**枚举应用**  
枚举成员具有描述性，可增强代码文档性和可读性，适用于小型相关常量集合。常见应用包括星期、方位、扑克花色：  
```
enum DaysOfWeek { sunday, monday, ..., saturday };
enum CardinalDirections { north, east, south, west };
enum CardSuits { clubs, diamonds, hearts, spades };
```
函数返回状态码时，传统使用负数表示错误，但枚举更清晰：  
```
enum FileReadResult
{
    readResultSuccess,
    readResultErrorFileOpen,
    readResultErrorFileRead,
    readResultErrorFileParse,
};

FileReadResult readFileContents() { ... }
```
调用方可直接比较枚举成员：  
```
if (readFileContents() == readResultSuccess) { ... }
```
游戏开发中枚举可用于物品类型、怪物种类等：  
```
enum ItemType { sword, torch, potion };
```
函数参数使用枚举可明确选项：  
```
enum SortOrder { alphabetical, alphabeticalReverse, numerical };
void sortData(SortOrder order) { ... }
```
枚举可配合`std::bitset`定义位标志：  
```
namespace Flags { enum State { isHungry, isSad, ..., isCrying }; }

std::bitset<8> me{};
me.set(Flags::isHappy);
```
无作用域枚举成员可隐式转换为整型（下节详述）。  

**无作用域枚举的作用域**  
无作用域枚举的成员名与枚举定义同作用域，易引发命名冲突：  
```
enum Color { red, green, blue }; // red进入全局作用域

enum Feeling { happy, tired, blue }; // 错误：blue冲突
```
访问枚举成员可通过作用域解析运算符：  
```
Color raspberry { Color::red };
```
**避免命名冲突**  
方法一：枚举名前缀：  
```
enum Color { color_red, color_blue, color_green };
```
方法二：放入命名空间：  
```
namespace Color { enum Color { red, green, blue }; }
namespace Feeling { enum Feeling { happy, tired, blue }; }
```
类作用域也可放置相关枚举（见[15.3 — 嵌套类型](Chapter-15/lesson15.3-nested-types-member-types.md)）。有作用域枚举（[13.6 — 有作用域枚举](Chapter-13/lesson13.6-scoped-enumerations-enum-classes.md)）提供独立作用域。  

**最佳实践**  
优先将枚举放入命名空间或类作用域，避免污染全局命名空间。若仅单个函数使用，可在函数内定义枚举。  

**枚举比较**  
使用相等运算符测试枚举值：  
```
Color shirt{ blue };
if (shirt == blue) { ... }
```

**测验答案**  
**问题1**  
```
enum MonsterType
{
    orc,
    goblin,
    troll,
    ogre,
    skeleton,
};
```
**问题2**  
```
namespace Monster
{
    enum MonsterType { orc, goblin, troll, ogre, skeleton };
}

int main()
{
    [[maybe_unused]] Monster::MonsterType monster{ Monster::troll };
    return 0;
}
```

[下一课13.3 — 无作用域枚举的整型转换](Chapter-13/lesson13.3-unscoped-enumerator-integral-conversions.md)  
[返回主页](/)  
[上一课13.1 — 程序定义类型简介](Chapter-13/lesson13.1-introduction-to-program-defined-user-defined-types.md)