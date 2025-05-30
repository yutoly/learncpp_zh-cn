15.7 — 静态成员函数  
===============================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月18日（首次发布于2007年9月18日）  

在前文[15.6 — 静态成员变量](Chapter-15/lesson15.6-static-member-variables.md)中，我们学习了静态成员变量属于类而非类对象的特性。若静态成员变量为公有（public），可直接通过类名和作用域解析运算符访问：  

```cpp
#include <iostream>

class Something
{
public:
    static inline int s_value { 1 };
};

int main()
{
    std::cout << Something::s_value; // s_value为公有，可直接访问
}
```  

但如果静态成员变量是私有（private）的呢？考虑以下示例：  

```cpp
#include <iostream>

class Something
{
private: // 现在为私有
    static inline int s_value { 1 };
};

int main()
{
    std::cout << Something::s_value; // 错误：s_value为私有，无法在类外直接访问
}
```  

此时无法从`main()`直接访问`Something::s_value`，因为它是私有成员。通常我们通过公有成员函数访问私有成员。虽然可以创建普通公有成员函数来访问`s_value`，但需要实例化类对象才能调用该函数！  

```cpp
#include <iostream>

class Something
{
private:
    static inline int s_value { 1 };

public:
    int getValue() { return s_value; }
};

int main()
{
    Something s{};
    std::cout << s.getValue(); // 可行，但需要实例化对象来调用getValue()
}
```  

我们可以优化这个方法。  


静态成员函数  
----------------  

成员变量并非唯一可静态化的成员类型，成员函数也可声明为静态。以下是使用静态成员函数访问器的改进示例：  

```cpp
#include <iostream>

class Something
{
private:
    static inline int s_value { 1 };

public:
    static int getValue() { return s_value; } // 静态成员函数
};

int main()
{
    std::cout << Something::getValue() << '\n';
}
```  

由于静态成员函数不与特定对象关联，可通过类名和作用域解析运算符直接调用（如`Something::getValue()`）。与静态成员变量类似，也可通过类对象调用，但不推荐此做法。  


### 静态成员函数无`this`指针  
静态成员函数有两个重要特性：  
1. 由于静态成员函数不依附于对象，它们没有`this`指针。这合乎逻辑——`this`指针总指向成员函数操作的对象，而静态成员函数无需操作对象  
2. 静态成员函数可直接访问其他静态成员（变量或函数），但不能访问非静态成员。因为非静态成员必须属于类对象，而静态成员函数没有关联的类对象  

### 类外定义静态成员  
静态成员函数也可在类声明外定义，方式与普通成员函数相同：  

```cpp
#include <iostream>

class IDGenerator
{
private:
    static inline int s_nextID { 1 };

public:
     static int getNextID(); // 静态函数声明
};

// 类外定义静态函数，不使用static关键字
int IDGenerator::getNextID() { return s_nextID++; } 

int main()
{
    for (int count{ 0 }; count < 5; ++count)
        std::cout << "下一个ID是: " << IDGenerator::getNextID() << '\n';

    return 0;
}
```  

该程序输出：  

```
下一个ID是: 1
下一个ID是: 2
下一个ID是: 3
下一个ID是: 4
下一个ID是: 5
```  

注意由于类中所有数据和函数均为静态，无需实例化对象即可使用其功能！该类使用静态成员变量保存下一个待分配ID值，并通过静态成员函数返回并递增该ID。  

如[15.2 — 类与头文件](Chapter-15/lesson15.2-classes-and-header-files.md)所述，类内定义的成员函数隐式内联（inline）。类外定义的成员函数需显式使用`inline`关键字声明为内联，以避免头文件被多次包含时违反单一定义规则（ODR）。  

### 纯静态类的注意事项  
编写全静态成员的类时需谨慎。虽然这种"纯静态类"（又称"单态类"）有其用途，但也存在潜在缺陷：  

1. 由于所有静态成员仅实例化一次，无法拥有多个纯静态类的副本（除非克隆类并重命名）  
2. 与全局变量类似，任何代码都可能修改静态成员值，导致看似无关的代码出错。纯静态类本质上等同于在全局命名空间声明函数和变量  

建议优先编写普通类并实例化全局对象（全局变量具有静态存储期），这样既可使用全局实例，也可在需要时创建局部实例。  

### 纯静态类 vs 命名空间  
纯静态类与命名空间（namespace）功能有重叠。两者都允许定义具有静态存储期的变量和函数。主要区别在于类具有访问控制而命名空间没有。  

通常，当需要静态数据成员或访问控制时选择静态类，否则优先使用命名空间。  

### C++不支持静态构造函数  
虽然现代语言普遍支持静态构造函数来初始化静态成员变量，但C++不提供此功能。  

若静态变量可直接初始化，则无需构造函数：可在定义点初始化静态成员变量（即使其为私有）。如前述`IDGenerator`示例。另一个示例：  

```cpp
#include <iostream>

struct Chars
{
    char first{};
    char second{};
    char third{};
    char fourth{};
    char fifth{};
};

struct MyClass
{
	static inline Chars s_mychars { 'a', 'e', 'i', 'o', 'u' }; // 在定义点初始化静态变量
};

int main()
{
    std::cout << MyClass::s_mychars.third; // 输出i
    return 0;
}
```  

若初始化需要执行代码（如循环），可采用多种间接方法。通用方法是通过函数创建对象并填充数据，再将返回值复制到初始化对象中：  

```cpp
#include <iostream>

struct Chars
{
    char first{};
    char second{};
    char third{};
    char fourth{};
    char fifth{};
};

class MyClass
{
private:
    static Chars generate()
    {
        Chars c{};
        c.first = 'a';
        c.second = 'e';
        c.third = 'i';
        c.fourth = 'o';
        c.fifth = 'u';
        return c;
    }

public:
	static inline Chars s_mychars { generate() }; // 复制返回对象到s_mychars
};

int main()
{
    std::cout << MyClass::s_mychars.third; // 输出i
    return 0;
}
```  

相关应用可参考[8.15 — 全局随机数（Random.h）](global-random-numbers-random-h/#RandomH)中的实践案例。  

测验时间  
----------------  

**问题1**  
将以下`Random`命名空间转换为含静态成员的类：  

```cpp
// 原命名空间实现
#include <chrono>
#include <random>
#include <iostream>

namespace Random
{
	inline std::mt19937 generate()
	{
		std::random_device rd{};
		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
				rd(), rd(), rd(), rd(), rd(), rd(), rd() };
		return std::mt19937{ ss };
	}

	inline std::mt19937 mt{ generate() };

	inline int get(int min, int max)
	{
		return std::uniform_int_distribution{min, max}(mt);
	}
}

// 转换为类后的实现
#include <chrono>
#include <random>
#include <iostream>

class Random
{
private:
	static std::mt19937 generate()
	{
		std::random_device rd{};
		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
				rd(), rd(), rd(), rd(), rd(), rd(), rd() };
		return std::mt19937{ ss };
	}

	static inline std::mt19937 mt{ generate() };

public:
	static int get(int min, int max)
	{
		return std::uniform_int_distribution{min, max}(mt);
	}
};
```  

命名空间中的对象是全局变量，而类中的静态内联（static inline）成员`mt`作为`Random`类的组成部分存在，保证整个程序使用单个`std::mt19937`实例。将成员函数设为静态后，无需实例化`Random`对象即可调用。  

[下一课 15.8 — 友元非成员函数](Chapter-15/lesson15.8-friend-non-member-functions.md)  
[返回主页](/)  
[上一课 15.6 — 静态成员变量](Chapter-15/lesson15.6-static-member-variables.md)