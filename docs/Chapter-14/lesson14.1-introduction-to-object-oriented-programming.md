14.1 — 面向对象编程简介  
====================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月15日（首次发布于2007年8月23日）  

过程式编程（Procedural programming）  
----------------  

回顾课程[1.3 — 对象与变量简介](Chapter-1/lesson1.3-introduction-to-objects-and-variables.md)，我们在C++中将**对象（object）**定义为"可用于存储值的内存片段"。具名对象称为**变量（variable）**。C++程序由计算机指令的序列化列表构成，这些指令通过对象定义数据，通过包含语句和表达式的函数定义数据操作。  

迄今为止，我们进行的编程类型称为**过程式编程（procedural programming）**。在过程式编程中，核心是创建实现程序逻辑的"过程（procedure）"（C++中称为函数）。我们将数据对象传递给这些函数，函数对数据进行操作，然后可能返回结果供调用者使用。  

在过程式编程中，函数与其操作的数据是分离的实体。程序员需要负责将函数与数据组合以产生预期结果。这导致代码呈现如下形式：  
```
eat(you, apple);
```  

观察周围环境，所有可见事物都是对象：书籍、建筑、食物乃至人类。这类对象包含两个主要组成部分：1）若干关联属性（如重量、颜色、尺寸、硬度、形状等）；2）若干可展现的行为（如被打开、加热其他物体等）。属性与行为不可分割。  

在编程中，属性通过对象表示，行为通过函数表示。因此，过程式编程对现实的模拟存在不足，因其将属性（对象）与行为（函数）分离。  

什么是面向对象编程？  
----------------  

在**面向对象编程（object-oriented programming，OOP）**中，核心是创建包含属性与明确定义行为集合的程序自定义数据类型。OOP中的"对象"指从这些类型实例化而来的对象。  

这导致代码呈现如下形式：  
```
you.eat(apple);
```  

这种形式更清晰地表明了主体（`you`）、被调用的行为（`eat()`）以及该行为的附属对象（`apple`）。  

由于属性与行为不再分离，对象更易于模块化，使得程序更易编写和理解，同时提高代码复用性。通过允许定义对象交互方式，这些对象提供了更直观的数据操作方式。  

我们将在下节课讨论如何创建此类对象。  

过程式与类OOP示例对比  
----------------  

以下是过程式编程风格编写的简短程序，用于输出动物名称和腿数：  
```cpp
#include <iostream>
#include <string_view>

enum AnimalType // 枚举（enum）
{
    cat,
    dog,
    chicken,
};

constexpr std::string_view animalName(AnimalType type)
{
    switch (type)
    {
    case cat: return "cat";
    case dog: return "dog";
    case chicken: return "chicken";
    default:  return "";
    }
}

constexpr int numLegs(AnimalType type)
{
    switch (type)
    {
    case cat: return 4;
    case dog: return 4;
    case chicken: return 2;
    default:  return 0;
    }
}

int main()
{
    constexpr AnimalType animal{ cat };
    std::cout << "A " << animalName(animal) << " has " << numLegs(animal) << " legs\n";
    return 0;
}
```  

在此程序中，我们编写了获取动物腿数和名称的函数。  

虽然这种方式有效，但考虑需要将动物更新为`snake`（蛇）时的情况。我们需要修改`AnimalType`枚举、`numLegs()`和`animalName()`函数。若在大型代码库中，还需更新所有使用`AnimalType`的位置，这可能需要修改大量代码（并可能引入错误）。  

现在用更接近OOP的思维编写相同程序（输出相同）：  
```cpp
#include <iostream>
#include <string_view>

struct Cat // 结构体（struct）
{
    std::string_view name{ "cat" };
    int numLegs{ 4 };
};

struct Dog
{
    std::string_view name{ "dog" };
    int numLegs{ 4 };
};

struct Chicken
{
    std::string_view name{ "chicken" };
    int numLegs{ 2 };
};

int main()
{
    constexpr Cat animal;
    std::cout << "a " << animal.name << " has " << animal.numLegs << " legs\n";
    return 0;
}
```  

在此示例中，每个动物都是独立的程序自定义类型，该类型管理与该动物相关的所有内容（本例中仅跟踪名称和腿数）。  

若需要将动物更新为蛇，只需创建`Snake`类型并替代`Cat`即可，现有代码几乎无需改动，极大降低了破坏现有功能的风险。  

如示例所示，上述`Cat`、`Dog`和`Chicken`结构体存在大量重复代码（均定义相同成员集合）。这种情况下，创建公共`Animal`结构体并为每种动物创建实例可能更优。但若需要为`Chicken`添加其他动物不适用的新成员（如`wormsPerDay`），公共`Animal`结构体将导致所有动物都拥有该成员。而采用OOP模型，可将该成员限定于`Chicken`对象。  

OOP的其他优势  
----------------  

在学校提交编程作业时，工作基本在代码完成后结束。助教运行代码验证结果正确性，根据结果评分，代码通常随后被弃置。  

但在代码提交至其他开发者使用的代码库或真实用户使用的应用程序时，情况截然不同。新操作系统或软件版本可能导致代码失效，用户可能发现逻辑错误，业务伙伴可能要求新功能，其他开发者可能需要扩展代码而不破坏原有功能。代码需要能够进化（可能是重大变更），且进化过程需耗时少、问题少、破坏小。  

实现这些目标的最佳方式是保持代码尽可能模块化（且非冗余）。为此，OOP还提供了其他实用概念：继承（inheritance）、封装（encapsulation）、抽象（abstraction）和多态（polymorphism）。  

> **作者注**  
> 语言设计者有个哲学：能用大词就不用小词。  
> 另外为什么"abbreviation"（缩写）这个词这么长？  

我们将在适当时机讲解这些概念，以及它们如何帮助减少代码冗余、简化修改和扩展。一旦熟练掌握OOP，您可能再也不愿回归纯过程式编程。  

需注意，OOP并非替代过程式编程，而是为编程工具带增添管理复杂性的新工具。  

术语"对象"的说明  
----------------  

注意"对象"一词存在多重含义，可能引发混淆。在传统编程中，对象是存储值的内存片段，仅此而已。在OOP中，"对象"意味着它既是传统编程意义上的对象，又结合了属性与行为。本教程中我们优先采用术语的传统含义，特指OOP对象时使用"类对象（class object）"。  

测验时间  
----------------  

**问题1**  
更新上述过程式动物示例，实例化蛇（snake）而非猫（cat）。  
  
```cpp
#include <iostream>
#include <string_view>

enum AnimalType
{
    cat,
    dog,
    chicken,
    snake,
};

constexpr std::string_view animalName(AnimalType type)
{
    switch (type)
    {
    case cat: return "cat";
    case dog: return "dog";
    case chicken: return "chicken";
    case snake: return "snake";
    default:  return "";
    }
}

constexpr int numLegs(AnimalType type)
{
    switch (type)
    {
    case cat: return 4;
    case dog: return 4;
    case chicken: return 2;
    case snake: return 0;
    default:  return 0;
    }
}

int main()
{
    constexpr AnimalType animal{ snake };
    std::cout << "A " << animalName(animal) << " has " << numLegs(animal) << " legs\n";
    return 0;
}
```  

**问题2**  
更新上述类OOP动物示例，实例化蛇（snake）而非猫（cat）。  
  
```cpp
#include <iostream>
#include <string_view>

struct Cat
{
    std::string_view name{ "cat" };
    int numLegs{ 4 };
};

struct Dog
{
    std::string_view name{ "dog" };
    int numLegs{ 4 };
};

struct Chicken
{
    std::string_view name{ "chicken" };
    int numLegs{ 2 };
};

struct Snake
{
    std::string_view name{ "snake" };
    int numLegs{ 0 };
};

int main()
{
    constexpr Snake animal;
    std::cout << "a " << animal.name << " has " << animal.numLegs << " legs\n";
    return 0;
}
```  

[下一课 14.2 类简介](Chapter-14/lesson14.2-introduction-to-classes.md)  
[返回主页](/)  
[
[上一课 13.y 使用语言参考](Chapter-13/lesson13.y-using-a-language-reference.md)