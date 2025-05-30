23.2 — 组合  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年12月4日（最后更新于2023年9月11日）  

对象组合（Object composition）  
----------------  

现实生活中，复杂对象通常由更小、更简单的对象构成。例如：汽车由金属框架、发动机、轮胎、变速箱、方向盘等部件组成；个人计算机由CPU、主板、内存等部件构成；甚至人体本身也是由头部、躯干、四肢等部分组成。这种通过简单对象构建复杂对象的过程称为**对象组合（object composition）**。  

广义而言，对象组合建模了两个对象之间的"具有"（has-a）关系。汽车"具有"（has-a）变速箱，计算机"具有"CPU，你"具有"心脏。复杂对象通常称为整体（whole）或父对象（parent），简单对象则称为部分（part）、子对象（child）或组件（component）。  

在C++中，您已经了解到结构体和类可以包含各种类型的数据成员（基本类型或其他类）。当我们构建包含数据成员的类时，实际上就是在通过简单部件构造复杂对象，这正是对象组合。因此，结构体和类有时被称为**复合类型（composite types）**。  

对象组合在C++中非常实用，因为它允许我们通过组合更简单、更易管理的部件来创建复杂类。这种方法降低了复杂性，使我们能够更快地编写代码并减少错误，因为我们可以复用经过编写、测试和验证的现有代码。  

对象组合的类型（Types of object composition）  
----------------  

对象组合有两个基本子类型：组合（composition）和聚合（aggregation）。本章重点讨论组合，下一章将讨论聚合。  

> **术语说明**  
> "组合"（composition）一词常被用于统称组合与聚合两种类型。在本教程中，当指代两种类型时使用"对象组合"（object composition），特指子类型时使用"组合"（composition）。  

组合（Composition）  
----------------  

要成为**组合**（composition），对象与部分必须满足以下关系：  

* 部分（成员）是对象（类）的组成部分  
* 部分（成员）同一时间只能属于一个对象（类）  
* 部分（成员）的生命周期由对象（类）管理  
* 部分（成员）不知道对象（类）的存在  

现实生活中的典型组合案例是人体与心脏的关系。让我们详细分析这些特征：  

组合关系是部分-整体关系，其中部分必须构成整体对象的一部分。例如，心脏是人体的一部分。组合中的部分同一时间只能属于一个对象——属于某个人体的心脏不能同时属于其他人。  

在组合关系中，对象负责部分的存在。通常这意味着部分随对象创建而创建，随对象销毁而销毁。更广义地说，对象管理部分的生命周期，使用者无需干预。例如，人体创建时心脏也随之创建，人体销毁时心脏也随之销毁。因此，组合有时被称为"死亡关系"（death relationship）。  

最后，部分不知道整体的存在。您的心脏在运作时并不知道自己是更大结构的一部分。我们称之为**单向**（unidirectional）关系，因为人体知道心脏的存在，但反之则不然。  

> **注意**  
> 组合关系不涉及部分的可转移性。心脏可以通过移植从一个身体转移到另一个身体。但即使移植后，仍然满足组合要求（心脏现在属于受体，除非再次转移，否则只能作为受体对象的一部分）。  

我们常用的分数类（Fraction class）是组合的绝佳示例：  

```cpp
class Fraction
{
private:
	int m_numerator;    // 分子
	int m_denominator;  // 分母
 
public:
	Fraction(int numerator=0, int denominator=1)
		: m_numerator{ numerator }, m_denominator{ denominator }
	{
	}
};
```  

该类有两个数据成员：分子和分母。分子和分母是分数（Fraction）的组成部分，不能同时属于多个分数。分子和分母不知道自己属于分数，它们只是存储整数值。当分数实例创建时，分子分母随之创建；当分数实例销毁时，分子分母也同时销毁。  

虽然对象组合建模了"具有"（has-a）类型的关系（人体具有心脏，分数具有分母），但我们可以更精确地说组合建模了"部分-属于"（part-of）关系（心脏属于人体，分子属于分数）。组合常用于建模物理关系，即一个对象物理上包含在另一个对象中。  

组合的组成部分可以是单一或多个的。例如，心脏是人体的单一组成部分，但人体包含10根手指（可以建模为数组）。  

组合的实现（Implementing compositions）  
----------------  

组合是C++中最易实现的关系类型之一。通常通过结构体或类的普通数据成员来实现。由于这些数据成员直接作为结构体/类的一部分存在，它们的生命周期与类实例本身绑定。  

需要进行动态内存分配/释放的组合可以通过指针数据成员实现。在这种情况下，组合类应负责所有必要的内存管理（而非类使用者）。  

通常，如果可以通过组合设计类，就应该使用组合。基于组合设计的类简单、灵活且健壮（能良好地进行自我清理）。  

更多示例（More examples）  
----------------  

许多游戏和模拟程序都有在棋盘、地图或屏幕上移动的生物或物体。这些生物/物体的共同点是都拥有位置属性。本示例将创建使用Point类存储位置的Creature类。  

首先设计Point类。我们的生物存在于2D世界，因此Point类需要X和Y两个维度，并假设世界由离散方块构成，故维度始终为整数。  

Point2D.h：  

```cpp
#ifndef POINT2D_H
#define POINT2D_H

#include <iostream>

class Point2D
{
private:
    int m_x;  // X坐标
    int m_y;  // Y坐标

public:
    // 默认构造函数（default constructor）
    Point2D()
        : m_x{ 0 }, m_y{ 0 }
    {
    }

    // 带参数的构造函数（specific constructor）
    Point2D(int x, int y)
        : m_x{ x }, m_y{ y }
    {
    }

    // 重载输出运算符（overloaded output operator）
    friend std::ostream& operator<<(std::ostream& out, const Point2D& point)
    {
        out << '(' << point.m_x << ", " << point.m_y << ')';
        return out;
    }

    // 位置设置函数（access functions）
    void setPoint(int x, int y)
    {
        m_x = x;
        m_y = y;
    }

};

#endif
```  

注意：为保持示例简洁，所有函数实现在头文件中完成，因此没有Point2D.cpp文件。  

Point2D类是其组成部分的组合：坐标值x和y属于Point2D，其生命周期与Point2D实例绑定。  

现在设计Creature类。我们的生物具有名称（字符串类型）和位置（Point2D类类型）属性：  

Creature.h：  

```cpp
#ifndef CREATURE_H
#define CREATURE_H

#include <iostream>
#include <string>
#include <string_view>
#include "Point2D.h"

class Creature
{
private:
    std::string m_name;     // 名称
    Point2D m_location;     // 位置

public:
    Creature(std::string_view name, const Point2D& location)
        : m_name{ name }, m_location{ location }
    {
    }

    // 重载输出运算符
    friend std::ostream& operator<<(std::ostream& out, const Creature& creature)
    {
        out << creature.m_name << " 位于 " << creature.m_location;
        return out;
    }

    // 移动函数
    void moveTo(int x, int y)
    {
        m_location.setPoint(x, y);
    }
};
#endif
```  

该Creature类也是其组成部分的组合。生物的名称和位置有唯一父对象，其生命周期与所属Creature实例绑定。  

main.cpp：  

```cpp
#include <string>
#include <iostream>
#include "Creature.h"
#include "Point2D.h"

int main()
{
    std::cout << "输入生物名称：";
    std::string name;
    std::cin >> name;
    Creature creature{ name, { 4, 7 } };
	
    while (true)
    {
        // 打印生物名称和位置
        std::cout << creature << '\n';

        std::cout << "输入新X坐标（-1退出）：";
        int x{ 0 };
        std::cin >> x;
        if (x == -1)
            break;

        std::cout << "输入新Y坐标（-1退出）：";
        int y{ 0 };
        std::cin >> y;
        if (y == -1)
            break;
		
        creature.moveTo(x, y);
    }

    return 0;
}
```  

运行示例：  

```
输入生物名称：Marvin
Marvin 位于 (4, 7)
输入新X坐标（-1退出）：6
输入新Y坐标（-1退出）：12
Marvin 位于 (6, 12)
输入新X坐标（-1退出）：3
输入新Y坐标（-1退出）：2
Marvin 位于 (3, 2)
输入新X坐标（-1退出）：-1
```  

组合的变体（Variants on the composition theme）  
----------------  

尽管大多数组合在创建时直接创建其部分，在销毁时直接销毁其部分，但存在一些变体：  

* 组合可能延迟创建某些部分直到需要时。例如，字符串类可能在用户赋值前不创建动态字符数组  
* 组合可能选择使用外部提供的部分而非自行创建  
* 组合可能将部分的销毁委托给其他对象（如垃圾回收机制）  

关键点在于：组合应自行管理其部分，使用者无需参与管理。  

组合与类成员（Composition and class members）  
----------------  

新程序员常问："何时应使用类成员而非直接实现功能？"。例如，我们可以直接在Creature类中添加两个整型变量处理位置，而非使用Point2D类。但将Point2D作为独立类（并作为Creature的成员）有以下优势：  

1. 每个类保持相对简单，专注于单一任务。这使得类更易编写和理解  
2. 每个类自成体系，具有可复用性。例如，Point2D可复用于其他完全不同的应用  
3. 外部类可让成员完成大部分工作，自身专注于协调数据流。这降低了外部类的复杂性  

> **重要提示**  
> 好的经验法则是：每个类应专注于完成单一任务。该任务可以是存储和操作某种数据（如Point2D、std::string），或是协调其成员（如Creature）。理想情况下不应同时承担两种职责。  

在本示例中，Creature无需关心Point如何实现或名称如何存储。Creature的职责是协调数据流，确保各成员知晓自己的任务。具体实现细节由各成员类自行处理。  

[下一课 23.3 — 聚合](Chapter-23/lesson23.3-aggregation.md)  
[返回主页](/)    
[上一课 23.1 — 对象关系](Chapter-23/lesson23.1-object-relationships.md)