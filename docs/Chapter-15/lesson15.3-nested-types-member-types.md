15.3 — 嵌套类型（成员类型）  
===================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月27日（首次发布于2016年12月21日）  

考虑以下简短程序：  
```
#include <iostream>

enum class FruitType
{
	apple,
	banana,
	cherry
};

class Fruit
{
private:
	FruitType m_type { };
	int m_percentageEaten { 0 };

public:
	Fruit(FruitType type) :
		m_type { type }
	{
	}

	FruitType getType() { return m_type; }
	int getPercentageEaten() { return m_percentageEaten; }

	bool isCherry() { return m_type == FruitType::cherry; }

};

int main()
{
	Fruit apple { FruitType::apple };
	
	if (apple.getType() == FruitType::apple)
		std::cout << "I am an apple";
	else
		std::cout << "I am not an apple";
	
	return 0;
}
```  
该程序本身没有问题。但由于`enum class FruitType`需要与`Fruit`类配合使用，让它独立于类存在会让人需要推断它们的关联关系。  

嵌套类型（成员类型）  
----------------  

迄今为止，我们见过包含两种成员的类类型：数据成员（data members）和成员函数（member functions）。上例中的`Fruit`类同时包含这两者。  

类类型还支持第三种成员：**嵌套类型（nested types）**（亦称**成员类型（member types）**）。要创建嵌套类型，只需在类定义内部、合适的访问说明符下定义该类型。  

以下是改写后的相同程序，使用嵌套在`Fruit`类中的类型：  
```
#include <iostream>

class Fruit
{
public:
	// FruitType 已移至类内部，位于 public 访问说明符下
        // 我们将其重命名为 Type 并改为普通枚举（非枚举类）
	enum Type
	{
		apple,
		banana,
		cherry
	};

private:
	Type m_type {};
	int m_percentageEaten { 0 };

public:
	Fruit(Type type) :
		m_type { type }
	{
	}

	Type getType() { return m_type;  }
	int getPercentageEaten() { return m_percentageEaten;  }

	bool isCherry() { return m_type == cherry; } // 在 Fruit 成员内部，枚举量无需 FruitType:: 前缀
};

int main()
{
	// 注意：类外部访问枚举量需使用 Fruit:: 前缀
	Fruit apple { Fruit::apple };
	
	if (apple.getType() == Fruit::apple)
		std::cout << "I am an apple";
	else
		std::cout << "I am not an apple";
	
	return 0;
}
```  
有几点值得注意：  

首先，`FruitType`现在定义在类内部，并重命名为`Type`（原因稍后讨论）。  

其次，嵌套类型`Type`定义在类顶部。嵌套类型名称必须在使用前完整定义，因此通常置于类首。  

最佳实践  
----------------  
在类类型顶部定义所有嵌套类型。  

第三，嵌套类型遵循常规访问规则。`Type`定义在`public`访问说明符下，因此类型名和枚举量可被公共访问。  

第四，类类型为其内部声明名称形成作用域（与命名空间类似）。因此`Type`的完全限定名是`Fruit::Type`，`apple`枚举量的完全限定名是`Fruit::apple`。  

在类成员内部，无需使用完全限定名。例如在成员函数`isCherry()`中，我们直接访问`cherry`枚举量而无需`Fruit::`作用域限定符。  

在类外部，必须使用完全限定名（如`Fruit::apple`）。我们将`FruitType`重命名为`Type`以便访问为`Fruit::Type`（而非冗余的`Fruit::FruitType`）。  

最后，我们将枚举类型从作用域枚举改为普通枚举。由于类本身已作为作用域，再使用作用域枚举略显冗余。改为普通枚举后，可以`Fruit::apple`方式访问枚举量，而非更冗长的`Fruit::Type::apple`。  

嵌套typedef与类型别名  
----------------  
类类型也可包含嵌套typedef或类型别名：  
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
public:
    using IDType = int;

private:
    std::string m_name{};
    IDType m_id{};
    double m_wage{};

public:
    Employee(std::string_view name, IDType id, double wage)
        : m_name { name }
        , m_id { id }
        , m_wage { wage }
    {
    }

    const std::string& getName() { return m_name; }
    IDType getId() { return m_id; } // 类内部可使用非限定名
};

int main()
{
    Employee john { "John", 1, 45000 };
    Employee::IDType id { john.getId() }; // 类外部必须使用完全限定名

    std::cout << john.getName() << " has id: " << id << '\n';

    return 0;
}
```  
输出：  
```
John has id: 1

```  
注意类内部可直接使用`IDType`，而外部必须使用完全限定名`Employee::IDType`。  

我们在课程[10.7 — typedef与类型别名](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)讨论过类型别名的优势，此处用途相同。C++标准库中的类普遍使用嵌套typedef。截至本文撰写时，`std::string`定义了10个嵌套typedef！  

嵌套类与访问外部类成员  
----------------  
类包含其他类作为嵌套类型的情况相对少见，但确实可行。在C++中，嵌套类无法访问外层类（包含类）的`this`指针，因此不能直接访问外层类成员。这是因为嵌套类可独立于外层类实例化（此时将无外层类成员可访问！）  

但由于嵌套类是外层类的成员，它们可以访问外层类在作用域内的任何私有成员。  

通过示例说明：  
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
public:
    using IDType = int;

    class Printer
    {
    public:
        void print(const Employee& e) const
        {
            // Printer 无法访问 Employee 的 `this` 指针
            // 因此不能直接打印 m_name 和 m_id
            // 必须传入 Employee 对象使用
            // 由于 Printer 是 Employee 的成员
            // 可直接访问私有成员 e.m_name 和 e.m_id
            std::cout << e.m_name << " has id: " << e.m_id << '\n';
        }
    };

private:
    std::string m_name{};
    IDType m_id{};
    double m_wage{};

public:
    Employee(std::string_view name, IDType id, double wage)
        : m_name{ name }
        , m_id{ id }
        , m_wage{ wage }
    {
    }

    // 本例中移除了访问函数（因未使用）
};

int main()
{
    const Employee john{ "John", 1, 45000 };
    const Employee::Printer p{}; // 实例化内部类对象
    p.print(john);

    return 0;
}
```  
输出：  
```
John has id: 1

```  
有一种情况嵌套类更常见：标准库中，大多数迭代器类作为容器类的嵌套类实现。例如`std::string::iterator`是`std::string`的嵌套类。我们将在后续章节讨论迭代器。  

嵌套类型与前向声明  
----------------  
嵌套类型可在包含类内部前向声明，随后在包含类内部或外部定义。例如：  
```
#include <iostream>

class outer
{
public:
    class inner1;   // 正确：在包含类内部前向声明
    class inner1{}; // 正确：定义前向声明的类型
    class inner2;   // 正确：在包含类内部前向声明
};

class inner2 // 正确：在包含类外部定义前向声明的类型
{
};

int main()
{
    return 0;
}
```  
但嵌套类型不能在包含类定义之前前向声明。  
```
#include <iostream>

class outer;         // 正确：可前向声明非嵌套类型
class outer::inner1; // 错误：无法在包含类定义前前向声明嵌套类型

class outer
{
public:
    class inner1{}; // 注意：嵌套类型在此声明
};

class outer::inner1; // 正确（但冗余）因嵌套类型已在包含类定义中声明

int main()
{
    return 0;
}
```  
虽然可在包含类定义后前向声明嵌套类型，但由于包含类已包含该嵌套类型的声明，此操作是冗余的。  

[下一课 15.4 — 析构函数简介](Chapter-15/lesson15.4-introduction-to-destructors.md)  
[返回主页](/)  
[上一课 15.2 — 类与头文件](Chapter-15/lesson15.2-classes-and-header-files.md)