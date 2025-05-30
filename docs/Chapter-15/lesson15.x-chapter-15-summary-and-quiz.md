15.x — 第15章总结与测验
===================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")

2023年9月11日，下午1:08（太平洋夏令时）
2024年5月3日

本章回顾
----------------

在每个非静态（non-static）成员函数内部，关键字 **this** 是一个指向当前隐式对象地址的常量指针（const pointer）。我们可以让函数通过引用返回 `*this` 以实现**方法链式调用（method chaining）**，从而在单个表达式中对同一对象调用多个成员函数。

推荐将类定义置于与类同名的头文件中。简单成员函数（如访问函数、空构造函数的访问函数等）可在类定义内部实现。

推荐将与类同名的源文件中实现非简单成员函数。

在类类型内部定义的类型称为**嵌套类型（nested type）**（或**成员类型（member type）**）。类型别名（Type aliases）也可嵌套。

在类模板（class template）定义内部实现的成员函数可直接使用类模板自身的模板参数。在类模板外部定义的成员函数必须重新声明模板参数，并应（在同一文件中）紧接类模板定义后实现。

**静态成员变量（static member variables）** 是静态存储期成员，被类的所有对象共享。即使未实例化任何类对象，静态成员依然存在。推荐通过类名、作用域解析运算符和成员名访问它们。

将静态成员设为 `inline` 允许在类定义内部初始化。

**静态成员函数（static member functions）** 是无需对象即可调用的成员函数。它们不包含 `*this` 指针，且无法访问非静态数据成员。

在类主体内部，可使用 **友元声明（friend declaration）**（通过 `friend` 关键字）告知编译器其他类或函数成为友元。**友元（friend）** 是被授予完全访问另一个类私有（private）和保护（protected）成员权限的类或函数（成员或非成员）。**友元函数（friend function）** 是能像类成员一样访问其私有和保护成员的函数（成员或非成员）。**友元类（friend class）** 是可访问另一个类私有和保护成员的类。

测验时间
----------------

**问题1**
创建一个随机怪物生成器。

a) 首先创建名为 `MonsterType` 的作用域枚举（scoped enumeration），包含以下怪物类型：Dragon（龙）、Goblin（哥布林）、Ogre（食人魔）、Orc（兽人）、Skeleton（骷髅）、Troll（巨魔）、Vampire（吸血鬼）和Zombie（僵尸）。添加额外枚举值 maxMonsterTypes 用于统计枚举项数量。

[查看解法](javascript:void(0))
```
enum class MonsterType
{
	dragon,
	goblin,
	ogre,
	orc,
	skeleton,
	troll,
	vampire,
	zombie,
	maxMonsterTypes,
};
```

b) 创建 `Monster` 类，包含4个属性（成员变量）：类型（`MonsterType`）、名称（`std::string`）、咆哮声（`std::string`）和生命值（`int`）。

[查看解法](javascript:void(0))
```
#include <string>

enum class MonsterType
{
	dragon,
	goblin,
	ogre,
	orc,
	skeleton,
	troll,
	vampire,
	zombie,
	maxMonsterTypes,
};

class Monster
{
private:
	MonsterType m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};
};
```

c) `enum class MonsterType` 是 `Monster` 专属类型，将其改为 `Monster` 内部的非限定作用域枚举（unscoped enum）并重命名为 `Type`。

[查看解法](javascript:void(0))
```
#include <string>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:
	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};
};
```

d) 创建可初始化所有成员变量的构造函数。

以下程序应能编译：
```
int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };
	return 0;
}
```

[查看解法](javascript:void(0))
```
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:
	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{
	}
};

int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };
	return 0;
}
```

e) 实现 `getTypeString()` 返回怪物类型的字符串描述，以及匹配下方示例输出的 `print()` 函数。

以下程序应能编译：
```
int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };
	skeleton.print();

	Monster vampire{ Monster::vampire, "Nibblez", "*hiss*", 0 };
	vampire.print();
	return 0;
}
```
并输出：
```
Bones the skeleton has 4 hit points and says *rattle*.
Nibblez the vampire is dead.
```

[查看解法](javascript:void(0))
```
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:
	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{
	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case dragon:   return "dragon";
		case goblin:   return "goblin";
		case ogre:     return "ogre";
		case orc:      return "orc";
		case skeleton: return "skeleton";
		case troll:    return "troll";
		case vampire:  return "vampire";
		case zombie:   return "zombie";
		default:       return "???";
		}
	}

	void print() const
	{
		std::cout << m_name << " the " << getTypeString();
		if (m_hitPoints <= 0)
			std::cout << " is dead.\n";
		else
			std::cout << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

int main()
{
	Monster skeleton{ Monster::skeleton, "Bones", "*rattle*", 4 };
	skeleton.print();
	Monster vampire{ Monster::vampire, "Nibblez", "*hiss*", 0 };
	vampire.print();
	return 0;
}
```

f) 创建无状态的 `MonsterGenerator` 命名空间（namespace），其中包含返回 `Monster` 的 `generate()` 函数（暂返回固定值）。

以下程序应能编译：
```
int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();
	return 0;
}
```
并输出：
```
Bones the skeleton has 4 hit points and says *rattle*
```

[查看解法](javascript:void(0))
```
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:
	Type m_type{};
	std::string m_name{};
	std::string m_roar{};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, const std::string& roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{
	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case Type::dragon: return "dragon";
		case Type::goblin: return "goblin";
		case Type::ogre: return "ogre";
		case Type::orc: return "orc";
		case Type::skeleton: return "skeleton";
		case Type::troll: return "troll";
		case Type::vampire: return "vampire";
		case Type::zombie: return "zombie";
		default: return "???";
		}
	}

	void print() const
	{
		if (m_hitPoints <= 0)
			std::cout << m_name << " is dead.\n";
		else
			std::cout << m_name << " the " << getTypeString() << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

namespace MonsterGenerator
{
	Monster generate()
	{
		return Monster{ Monster::skeleton, "Bones", "*rattle*", 4 };
	}
};

int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();
	return 0;
}
```

g) 在 `MonsterGenerator` 命名空间中添加 `getName(int)` 和 `getRoar(int)` 函数（根据输入返回预设值），并更新 `generate()` 调用它们。

以下程序应能编译：
```
int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();
	return 0;
}
```
并输出（名称和咆哮声因实现而异）：
```
Blarg the skeleton has 4 hit points and says *ROAR*
```

[查看解法](javascript:void(0))
```
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:
	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{
	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case dragon:   return "dragon";
		case goblin:   return "goblin";
		case ogre:     return "ogre";
		case orc:      return "orc";
		case skeleton: return "skeleton";
		case troll:    return "troll";
		case vampire:  return "vampire";
		case zombie:   return "zombie";
		default: return "???";
		}
	}

	void print() const
	{
		std::cout << m_name << " the " << getTypeString();
		if (m_hitPoints <= 0)
			std::cout << " is dead.\n";
		else
			std::cout << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

namespace MonsterGenerator
{
    std::string_view getName(int n)
	{
        switch (n)
        {
            case 0:  return "Blarg";
            case 1:  return "Moog";
            case 2:  return "Pksh";
            case 3:  return "Tyrn";
            case 4:  return "Mort";
            case 5:  return "Hans";
            default: return "???";
        }
    }

    std::string_view getRoar(int n)
	{
        switch (n)
        {
            case 0:  return "*ROAR*";
            case 1:  return "*peep*";
            case 2:  return "*squeal*";
            case 3:  return "*whine*";
            case 4:  return "*growl*";
            case 5:  return "*burp*";
            default: return "???";
        }
    }

	Monster generate()
	{
		return Monster{ Monster::skeleton, getName(0), getRoar(0), 4 };
	}
};

int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();
	return 0;
}
```

h) 使用随机库实现怪物属性随机化。保存[8.15 — 全局随机数（Random.h）](global-random-numbers-random-h/#RandomH)中的代码至Random.h，通过`Random::get()`随机生成怪物类型、名称、咆哮声和生命值（1-100）。

以下程序应能编译：
```
#include "Random.h"
int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();
	return 0;
}
```
并输出（结果随机）：
```
Mort the zombie has 61 hit points and says *growl*
```

[查看解法](javascript:void(0))
```
#include "Random.h"
#include <iostream>
#include <string>
#include <string_view>

class Monster
{
public:
	enum Type
	{
		dragon,
		goblin,
		ogre,
		orc,
		skeleton,
		troll,
		vampire,
		zombie,
		maxMonsterTypes,
	};

private:
	Type m_type{};
	std::string m_name{"???"};
	std::string m_roar{"???"};
	int m_hitPoints{};

public:
	Monster(Type type, std::string_view name, std::string_view roar, int hitPoints)
		: m_type{ type }, m_name{ name }, m_roar{ roar }, m_hitPoints{ hitPoints }
	{
	}

	constexpr std::string_view getTypeString() const
	{
		switch (m_type)
		{
		case dragon:   return "dragon";
		case goblin:   return "goblin";
		case ogre:     return "ogre";
		case orc:      return "orc";
		case skeleton: return "skeleton";
		case troll:    return "troll";
		case vampire:  return "vampire";
		case zombie:   return "zombie";
		default: return "???";
		}
	}

	void print() const
	{
		std::cout << m_name << " the " << getTypeString();
		if (m_hitPoints <= 0)
			std::cout << " is dead.\n";
		else
			std::cout << " has " << m_hitPoints << " hit points and says " << m_roar << ".\n";
	}
};

namespace MonsterGenerator
{
    std::string_view getName(int n)
	{
        switch (n)
        {
            case 0:  return "Blarg";
            case 1:  return "Moog";
            case 2:  return "Pksh";
            case 3:  return "Tyrn";
            case 4:  return "Mort";
            case 5:  return "Hans";
            default: return "???";
        }
    }

    std::string_view getRoar(int n)
	{
        switch (n)
        {
            case 0:  return "*ROAR*";
            case 1:  return "*peep*";
            case 2:  return "*squeal*";
            case 3:  return "*whine*";
            case 4:  return "*growl*";
            case 5:  return "*burp*";
            default: return "???";
        }
    }

    Monster generate()
    {
        return Monster{
            static_cast<Monster::Type>(Random::get(0, Monster::maxMonsterTypes-1)),
            getName(Random::get(0,5)),
            getRoar(Random::get(0,5)),
            Random::get(1, 100)
            };
	}
};

int main()
{
	Monster m{ MonsterGenerator::generate() };
	m.print();
	return 0;
}
```

[下一课 16.1 — 容器与数组简介](Chapter-16/lesson16.1-introduction-to-containers-and-arrays.md)
[返回主页](/)  
[上一课 15.10 — 引用限定符](Chapter-15/lesson15.10-ref-qualifiers.md)