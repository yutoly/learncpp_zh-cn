15.10 — 引用限定符
=======================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")

2023年10月5日 下午12:59（太平洋夏令时）  
2024年9月25日

作者说明
----------------
此为可选课程。建议通读以熟悉内容，但无需完全掌握即可继续后续课程。

在课程[14.7 — 返回数据成员引用的成员函数](Chapter-14/lesson14.7-member-functions-returning-references-to-data-members.md)中，我们讨论了当隐式对象为右值时，调用返回数据成员引用的访问函数可能存在的风险。简要回顾：

```cpp
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
	std::string m_name{};

public:
	Employee(std::string_view name): m_name { name } {}
	const std::string& getName() const { return m_name; } // 访问函数返回常量引用
};

// createEmployee() 按值返回 Employee（返回值为右值）
Employee createEmployee(std::string_view name)
{
	Employee e { name };
	return e;
}

int main()
{
	// 情况1：安全 - 同一表达式内使用右值类对象成员的返回引用
	std::cout << createEmployee("Frank").getName() << '\n';

	// 情况2：危险 - 保存右值类对象成员的返回引用供后续使用
	const std::string& ref { createEmployee("Garbo").getName() }; // createEmployee()返回值销毁后引用悬垂
	std::cout << ref << '\n'; // 未定义行为

	return 0;
}
```
情况2中，`createEmployee("Garbo")`返回的右值对象在初始化`ref`后被销毁，导致`ref`引用已销毁的数据成员。后续使用`ref`将引发未定义行为。

这形成了一种两难局面：
* 若`getName()`按值返回：右值隐式对象时安全，但左值隐式对象（最常见情况）会产生昂贵且不必要的拷贝
* 若`getName()`按常量引用返回：避免`std::string`拷贝效率高，但右值隐式对象时可能被误用（导致未定义行为）

由于成员函数通常在左值隐式对象上调用，常规选择是按常量引用返回，并避免在右值隐式对象时误用返回的引用。

引用限定符
----------------
上述问题的根源在于：单个函数需服务两种场景（隐式对象为左值或右值）。对一种场景最优的方案对另一种场景并非最佳。

为解决此类问题，C++11引入了鲜为人知的**引用限定符（ref-qualifier）**特性，允许根据隐式对象是左值还是右值来重载成员函数。通过此特性，可创建两个版本的`getName()`：
* 处理左值隐式对象的版本
* 处理右值隐式对象的版本

首先从非引用限定版本开始：
```cpp
const std::string& getName() const { return m_name; } // 可被左值和右值隐式对象调用
```
添加`&`限定符使重载仅匹配左值隐式对象，`&&`限定符使重载仅匹配右值隐式对象：
```cpp
const std::string& getName() const &  { return m_name; } // & 限定符重载函数仅匹配左值隐式对象，返回引用
std::string        getName() const && { return m_name; } // && 限定符重载函数仅匹配右值隐式对象，返回值
```
因属于不同重载，它们可具有不同返回类型！左值限定版本返回常量引用，右值限定版本返回值。

完整示例如下：
```cpp
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
	std::string m_name{};

public:
	Employee(std::string_view name): m_name { name } {}

	const std::string& getName() const &  { return m_name; } // & 限定符重载函数仅匹配左值隐式对象
	std::string        getName() const && { return m_name; } // && 限定符重载函数仅匹配右值隐式对象
};

// createEmployee() 按值返回 Employee（返回值为右值）
Employee createEmployee(std::string_view name)
{
	Employee e { name };
	return e;
}

int main()
{
	Employee joe { "Joe" };
	std::cout << joe.getName() << '\n'; // Joe 是左值，调用 std::string& getName() &（返回引用）
    
	std::cout << createEmployee("Frank").getName() << '\n'; // Frank 是右值，调用 std::string getName() &&（创建拷贝）

	return 0;
}
```
此方案在隐式对象为左值时执行高效操作，为右值时执行安全操作。

进阶说明
----------------
当隐式对象是非常量临时对象时，上述`getName()`的右值重载版本在性能上可能非最优。此时隐式对象将在表达式结束时销毁，因此可让右值访问器尝试移动成员（使用`std::move`）而非返回（可能昂贵的）成员拷贝。

通过添加以下非常量右值重载访问器实现：
```cpp
// 若隐式对象是非常量右值，使用 std::move 尝试移动 m_name
std::string getName() && { return std::move(m_name); }
```
此版本可与常量右值访问器共存，或直接替代之（因常量右值较罕见）。

`std::move`详见课程[22.4 — std::move](Chapter-22/lesson22.4-stdmove.md)。

引用限定成员函数注意事项
----------------
1. 同一函数的非引用限定重载与引用限定重载不能共存，二者择一
2. 类似常量左值引用可绑定右值：若仅存在常量左值限定函数，它将接受左值和右值隐式对象
3. 任何限定重载均可显式删除（使用`= delete`）以阻止调用。例如删除右值限定版本可阻止在右值隐式对象上使用该函数

为何不推荐使用引用限定符？
----------------
尽管引用限定符很巧妙，但此方式存在缺点：
* 为每个返回引用的访问器添加右值重载会增加类冗余，仅为缓解不常见且可通过良好习惯避免的情况
* 右值重载返回值意味着即使可安全使用引用的场景（如本节开篇案例1）仍需承担拷贝（或移动）成本

此外：
* 多数C++开发者不了解此特性（可能导致使用错误或低效）
* 标准库通常未使用此特性

基于以上原因，不建议将引用限定符作为最佳实践。替代方案是：始终立即使用访问函数结果，不保存返回的引用供后续使用。

[下一课 15.x 第15章总结与测验](Chapter-15/lesson15.x-chapter-15-summary-and-quiz.md)  
[返回主页](/)    
[上一课 15.9 友元类与友元成员函数](Chapter-15/lesson15.9-friend-classes-and-friend-member-functions.md)