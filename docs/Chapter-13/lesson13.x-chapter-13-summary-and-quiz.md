13.x — 第13章总结与测验
===================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2020年1月3日 下午1:20（太平洋标准时间）  
2024年11月4日  

祝贺！您已顺利学完本章内容。关于结构体（struct）的知识将为我们学习C++最重要的主题——类（class）奠定基础！  

快速回顾  
----------------  

**程序定义类型（program-defined type/user-defined type）**是开发者自定的可在程序中使用的类型。枚举类型（enumerated type）和类类型（包含结构体、类与联合体）都属于程序定义类型。这类类型必须先定义后使用，其定义称为**类型定义（type definition）**，不受单一定义规则约束。  

**枚举（enumeration/enumerated type/enum）**是复合数据类型，其所有可能值均定义为符号常量（称为**枚举项（enumerator）**）。枚举属于**独立类型（distinct type）**，编译器能将其与其他类型区分（与类型别名不同）。  

**非限定作用域枚举（unscoped enumeration）**的枚举项名称位于枚举定义所在的作用域（而非像命名空间那样创建新作用域）。此类枚举会隐式转换为整数值。  

**限定作用域枚举（scoped enumeration）**不会隐式转换为整型，且枚举项仅存在于枚举自身的作用域内（不在定义枚举的上级作用域）。  

**结构体（struct/structure）**是程序定义的数据类型，可将多个变量组合为单一类型。结构体（或类）中的变量称为**数据成员（data member/member variable）**。访问成员变量时，普通结构体变量使用**成员选择运算符（member selection operator）**`.`，指针则使用`->`运算符。  

在编程中，**聚合数据类型（aggregate data type/aggregate）**指包含多个数据成员的类型。C++中，数组和仅有数据成员的结构体属于**聚合（aggregate）**。  

聚合类型使用**聚合初始化（aggregate initialization）**方式，通过**初始化列表（initializer list）**直接初始化成员。这种**逐成员初始化（memberwise initialization）**按声明顺序进行。  

C++20引入**指定初始化器（designated initializer）**，允许显式定义成员与初始化值的对应关系。成员必须按声明顺序初始化，否则报错。  

定义结构体（或类）时可为成员提供默认初始化值，这称为**非静态成员初始化（non-static member initialization）**，初始化值称为**默认成员初始化器（default member initializer）**。  

出于性能考虑，编译器可能在结构中添加间隙（称为**填充（padding）**），因此结构体大小可能超过成员尺寸之和。  

**类模板（class template）**用于实例化类类型（结构体、类或联合体）。**类模板参数推导（class template argument deduction, CTAD）**是C++17特性，允许编译器根据初始值推断模板参数类型。  

测验时间  
----------------  

**问题1**  
设计游戏时需创建怪物类型。请声明表示怪物的结构体，类型应为以下之一：食人魔（ogre）、龙（dragon）、兽人（orc）、巨型蜘蛛（giant spider）或史莱姆（slime）。每个怪物应有名称（`std::string`）和生命值。编写`printMonster()`函数输出结构体所有成员。实例化食人魔和史莱姆，使用初始化列表初始化并传递给函数。程序应输出：  
```
This Ogre is named Torg and has 145 health.
This Slime is named Blurp and has 23 health.
```  
  
```cpp
#include <iostream>
#include <string>
#include <string_view> // C++17

struct Monster
{
	enum Type
	{
		ogre,
		dragon,
		orc,
		giant_spider,
		slime,
	};

	Type type{};
	std::string name{};
	int health{};
};

constexpr std::string_view getMonsterTypeString(Monster::Type type)
{
	switch (type)
	{
	case Monster::ogre:          return "Ogre";
	case Monster::dragon:        return "Dragon";
	case Monster::orc:           return "Orc";
	case Monster::giant_spider:  return "Giant Spider";
	case Monster::slime:         return "Slime";
	}
	return "Unknown";
}

void printMonster(const Monster& monster)
{
	std::cout << "This " << getMonsterTypeString(monster.type) <<
		" is named " << monster.name <<
		" and has " << monster.health << " health.\n";
}

int main()
{
	Monster ogre{ Monster::ogre, "Torg", 145 };
	Monster slime{ Monster::slime, "Blurp", 23 };

	printMonster(ogre);
	printMonster(slime);

	return 0;
}
```  

**问题2**  
判断以下类型应通过值传递、常量地址传递还是常量引用传递（假设函数不修改参数）：  
a) `char`  
  
`char`是基础类型，应值传递。  

b) `std::string`  
  
`std::string`复制时会创建字符串副本，应常量引用传递。  

c) `unsigned long`  
  
基础类型，应值传递。  

d) `bool`  
  
基础类型，应值传递。  

e) 枚举类型  
  
枚举存储整数值（通常为int），应值传递。  

f)  
```cpp
struct Position
{
  double x{};
  double y{};
  double z{};
};
```  
  
结构体类型应常量引用传递。  

g)  
```cpp
struct Player
{
  int health{};
  // 后续将添加更多成员
};
```  
  
虽然当前仅含int，但未来会增加成员。为免后续修改多处代码，应常量引用传递。  

h) `int`（允许空值）  
  
通常值传递，若需支持空值则通过地址传递（可传入指针或`nullptr`）。  

i) `std::string_view`  
  
不复制字符串且复制成本低，应值传递。  

**问题3**  
创建名为`Triad`的类模板，包含3个相同模板类型的成员。创建函数模板`print`输出Triad。以下程序应编译：  
```cpp
int main()
{
	Triad t1{ 1, 2, 3 }; // 使用CTAD推导模板参数
	print(t1);

	Triad t2{ 1.2, 3.4, 5.6 };
	print(t2);

	return 0;
}
```  
并输出：  
```
[1, 2, 3][1.2, 3.4, 5.6]
```  
（C++17需提供推导指南）  
  
```cpp
#include <iostream>

template <typename T>
struct Triad
{
	T first{};
	T second{};
	T third{};
};

// C++17需推导指南（C++20不需要）
template <typename T>
Triad(T, T, T) -> Triad<T>;

template <typename T>
void print(const Triad<T>& t)
{
	std::cout << '[' << t.first << ", " << t.second << ", " << t.third << ']';
}

int main()
{
	Triad t1{ 1, 2, 3 };
	print(t1);

	Triad t2{ 1.2, 3.4, 5.6 };
	print(t2);

	return 0;
}
```  

[下一课 13.y — 使用语言参考](Chapter-13/lesson13.y-using-a-language-reference.md)  
[返回主页](/)  
[上一课 13.15 — 别名模板](Chapter-13/lesson13.15-alias-templates.md)