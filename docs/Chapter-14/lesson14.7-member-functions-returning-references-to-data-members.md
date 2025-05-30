14.7 — 成员函数返回数据成员的引用  
=============================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年10月5日 下午12:55（PDT）  
2024年3月29日更新  

在课程[12.12 — 按引用返回与按地址返回](Chapter-12/lesson12.12-return-by-reference-and-return-by-address.md)中，我们学习了按引用返回。特别要注意的是，"按引用返回的对象必须在函数返回后继续存在"。这意味着我们不应该返回局部变量的引用，因为这些引用会在局部变量销毁后变成悬垂引用。不过，返回通过引用传递的函数参数或具有静态存储期（静态局部变量或全局变量）通常是安全的，因为这些变量在函数返回后不会被销毁。例如：
```
// 接收两个std::string对象，返回按字母顺序排前的那个
const std::string& firstAlphabetical(const std::string& a, const std::string& b)
{
	return (a < b) ? a : b; // 使用std::string的operator<判断字母顺序
}

int main()
{
	std::string hello { "Hello" };
	std::string world { "World" };

	std::cout << firstAlphabetical(hello, world); // 通过引用返回hello或world

	return 0;
}
```

成员函数也可以按引用返回，其安全规则与非成员函数相同。不过成员函数有一个额外需要注意的情况：返回数据成员引用的成员函数。

这种情况最常见于getter访问函数，因此我们将以getter成员函数为例说明。但需注意，本主题适用于所有返回数据成员引用的成员函数。

**按值返回数据成员的代价**  
考虑以下示例：
```
#include <iostream>
#include <string>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	std::string getName() const { return m_name; } // getter按值返回
};

int main()
{
	Employee joe{};
	joe.setName("Joe");
	std::cout << joe.getName();

	return 0;
}
```
在这个示例中，`getName()`访问函数按值返回`std::string m_name`。虽然这是最安全的方式，但也意味着每次调用`getName()`都会创建`m_name`的昂贵拷贝。由于访问函数通常会被频繁调用，这通常不是最佳选择。

**通过左值引用返回数据成员**  
成员函数也可以通过（const）左值引用返回数据成员。数据成员的生命周期与包含它们的对象相同。由于成员函数总是在某个对象上调用，而该对象必须存在于调用者的作用域中，因此成员函数按（const）左值引用返回数据成员通常是安全的（因为被返回的成员在函数返回时仍存在于调用者的作用域中）。

更新上述示例，让`getName()`通过const左值引用返回`m_name`：
```
#include <iostream>
#include <string>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	const std::string& getName() const { return m_name; } // getter返回const引用
};

int main()
{
	Employee joe{}; // joe存在至函数结束
	joe.setName("Joe");

	std::cout << joe.getName(); // 通过引用返回joe.m_name

	return 0;
}
```
现在调用`joe.getName()`时，`joe.m_name`会通过引用返回给调用者，避免了拷贝。调用者使用该引用将`joe.m_name`输出到控制台。由于`joe`在调用者的作用域中持续存在至`main()`函数结束，对`joe.m_name`的引用在相同周期内保持有效。

> **关键洞察**  
> 返回数据成员的（const）左值引用是安全的。包含该成员的隐式对象在函数返回后仍存在于调用者的作用域中，因此所有返回的引用都将保持有效。

**返回类型应与数据成员类型匹配**  
一般来说，按引用返回的成员函数的返回类型应与被返回数据成员的类型匹配。在上例中，`m_name`是`std::string`类型，因此`getName()`返回`const std::string&`。如果返回`std::string_view`则需要每次调用时创建并返回临时`std::string_view`对象，这会带来不必要的性能损失。若调用者需要`std::string_view`，可以自行转换。

> **最佳实践**  
> 按引用返回的成员函数应返回与被返回数据成员类型相同的引用，以避免不必要的转换。

对于getter，使用`auto`让编译器从被返回的成员推导返回类型，是确保不进行转换的有效方法：
```
#include <iostream>
#include <string>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	const auto& getName() const { return m_name; } // 使用auto推导返回类型
};

int main()
{
	Employee joe{}; // joe存在至函数结束
	joe.setName("Joe");

	std::cout << joe.getName(); // 通过引用返回joe.m_name

	return 0;
}
```

> **相关内容**  
> 我们在课程[10.9 — 函数的类型推导](Chapter-10/lesson10.9-type-deduction-for-functions.md)中讨论`auto`返回类型。

但使用`auto`返回类型会从文档角度隐藏getter的返回类型。例如：
```
const auto& getName() const { return m_name; } // 使用auto推导返回类型
```
无法明确该函数实际返回的字符串类型（可能是`std::string`、`std::string_view`、C风格字符串等）。因此，我们通常更推荐显式声明返回类型。

**右值隐式对象与引用返回**  
需要注意一种特殊情况。当隐式对象是右值（如按值返回的函数返回值）时，右值对象在创建它的完整表达式结束时被销毁。此时，对该右值对象成员的引用将失效并成为悬垂引用，使用这类引用会导致未定义行为。因此，右值对象成员的引用只能在创建该右值的完整表达式中安全使用。

> **提示**  
> 我们在课程[1.10 — 表达式简介](Chapter-1/lesson1.10-introduction-to-expressions.md)中讨论过完整表达式的概念。

> **警告**  
> 右值对象在创建它的完整表达式结束时被销毁。此时对其成员的任何引用都会成为悬垂引用。右值对象成员的引用只能在创建该右值的完整表达式中安全使用。

通过案例理解：
```
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
	std::string m_name{};

public:
	void setName(std::string_view name) { m_name = name; }
	const std::string& getName() const { return m_name; } // getter返回const引用
};

// createEmployee()按值返回Employee（返回值是右值）
Employee createEmployee(std::string_view name)
{
	Employee e;
	e.setName(name);
	return e;
}

int main()
{
	// 案例1：正确：在同一表达式中使用右值类对象成员的引用
	std::cout << createEmployee("Frank").getName();

	// 案例2：错误：保存右值类对象成员的引用供后续使用
	const std::string& ref { createEmployee("Garbo").getName() }; // createEmployee()返回值销毁后引用悬垂
	std::cout << ref; // 未定义行为

	// 案例3：正确：将引用值复制到局部变量供后续使用
	std::string val { createEmployee("Hans").getName() }; // 复制被引用成员
	std::cout << val; // 正确：val独立于被引用成员

	return 0;
}
```
当`createEmployee()`被调用时，会按值返回一个`Employee`对象。该返回的`Employee`对象是右值，其存在周期持续到包含`createEmployee()`调用的完整表达式结束。当该右值对象被销毁时，对其成员的引用将变成悬垂。

案例1中，`createEmployee("Frank")`返回右值`Employee`对象，调用`getName()`返回对`m_name`的引用，并立即用于打印。此时完整表达式结束，右值对象及其成员被销毁。由于之后不再使用该对象，此案例安全。

案例2中，`createEmployee("Garbo")`返回右值对象，调用`getName()`获取其`m_name`成员的引用并初始化`ref`。此时完整表达式结束，右值对象被销毁，导致`ref`成为悬垂引用。后续使用`ref`时会产生未定义行为。

> **关键洞察**  
> 完整表达式的求值在初始化器使用该表达式之后结束。这允许用同类型的右值初始化对象（右值在初始化完成后才被销毁）。

若需要保存按引用返回的成员值供后续使用，应该用该引用初始化非引用局部变量。案例3中，使用返回的引用初始化非引用局部变量`val`，这会复制被引用的成员值到`val`。初始化完成后，`val`独立于原引用。因此右值对象销毁不会影响`val`，后续输出`val`是安全的。

**安全使用返回引用的成员函数**  
尽管存在右值隐式对象的潜在危险，但按const引用返回需要高拷贝代价的类型仍是getter的常规做法。上述三个案例说明以下要点：
* 优先立即使用返回引用的成员函数返回值（案例1）。这适用于左值和右值对象，始终遵循此原则可避免问题
* 不要"保存"返回的引用供后续使用（案例2），除非确定隐式对象是左值。对右值隐式对象进行此操作会导致未定义行为
* 若需要持久化返回的引用且不确定隐式对象是否为左值，应使用该引用初始化非引用局部变量（案例3），这会复制被引用成员的值到局部变量

> **最佳实践**  
> 优先立即使用按引用返回的成员函数值，以避免右值隐式对象导致的悬垂引用问题。

**不要返回非const引用给私有数据成员**  
由于引用与被引用对象等效，返回非const引用的成员函数会直接暴露该成员（即使成员是私有的）。例如：
```
#include <iostream>

class Foo
{
private:
    int m_value{ 4 }; // 私有成员

public:
    int& value() { return m_value; } // 返回非const引用（不要这样做）
};

int main()
{
    Foo f{};                // f.m_value初始化为默认值4
    f.value() = 5;          // 等效于m_value = 5
    std::cout << f.value(); // 输出5

    return 0;
}
```
由于`value()`返回`m_value`的非const引用，调用者可以直接访问（并修改）`m_value`的值。这破坏了访问控制系统的设计初衷。

**const成员函数不能返回非const引用**  
const成员函数不允许返回数据成员的非const引用。这是合理的——const成员函数不允许修改对象状态，也不允许调用可能修改对象状态的函数。它不应做任何可能导致对象修改的操作。若允许const成员函数返回成员的非const引用，相当于为调用者提供了直接修改该成员的途径，这违反了const成员函数的意图。

[下一课14.8数据隐藏（封装）的优势](Chapter-14/lesson14.8-the-benefits-of-data-hiding-encapsulation.md)  
[返回主页](/)  
[上一课14.6访问函数](Chapter-14/lesson14.6-access-functions.md)