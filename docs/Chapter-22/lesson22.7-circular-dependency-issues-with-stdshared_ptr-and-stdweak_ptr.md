22.7 — 使用 std::shared_ptr 时的循环依赖问题与 std::weak_ptr 解决方案
============================================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2017年3月21日发布，2024年7月22日更新  

 

在上一课中，我们了解了 std::shared_ptr（共享指针）如何让多个智能指针共同拥有同一资源。但在某些情况下，这会导致问题。请看以下案例：两个独立对象中的共享指针互相指向对方：  

```cpp
#include <iostream>
#include <memory> // 用于 std::shared_ptr
#include <string>

class Person
{
	std::string m_name;
	std::shared_ptr<Person> m_partner; // 初始化为空

public:
	Person(const std::string &name): m_name(name)
	{ 
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") }; // 创建名为"Lucy"的Person对象
	auto ricky { std::make_shared<Person>("Ricky") }; // 创建名为"Ricky"的Person对象

	partnerUp(lucy, ricky); // 让"Lucy"指向"Ricky"，反之亦然

	return 0;
}
```  

在此示例中，我们使用 make_shared() 动态分配了两个 Person 对象（确保 lucy 和 ricky 在 main() 结束时被销毁），然后建立伙伴关系。这会使 "Lucy" 内部的 std::shared_ptr 指向 "Ricky"，而 "Ricky" 内部的 std::shared_ptr 指向 "Lucy"。共享指针本应共享，因此 lucy 共享指针和 Ricky 的 m_partner 共享指针都指向 "Lucy" 是合理的（反之亦然）。  

但该程序未按预期执行：  

```
Lucy created
Ricky created
Lucy is now partnered with Ricky
```  

没有发生内存释放。原因何在？  

当 partnerUp() 调用后：  
- 两个共享指针指向 "Ricky"（ricky 和 Lucy 的 m_partner）  
- 两个共享指针指向 "Lucy"（lucy 和 Ricky 的 m_partner）  

在 main() 结束时，ricky 共享指针首先离开作用域。此时 ricky 检查是否有其他共享指针共同拥有 "Ricky"（存在 Lucy 的 m_partner），因此不释放 "Ricky"（否则 Lucy 的 m_partner 会成为悬空指针）。此时：  
- 1 个共享指针指向 "Ricky"（Lucy 的 m_partner）  
- 2 个共享指针指向 "Lucy"（lucy 和 Ricky 的 m_partner）  

接着 lucy 共享指针离开作用域，同理不释放 "Lucy"。最终两个对象均未被释放，形成互相保持存活的循环依赖。  

循环引用  
----------------  

**循环引用**（circular reference，又称**环形引用**）是指对象间相互引用形成的闭环。在共享指针语境下，这种引用表现为指针间的相互指向。  

上述案例中："Lucy"→"Ricky"→"Lucy" 形成循环。当共享指针形成循环时，每个对象都使下一个对象保持存活，最终导致没有对象能被释放。  

简化案例  
----------------  

循环引用问题甚至可能发生在单个 std::shared_ptr 身上：  

```cpp
#include <iostream>
#include <memory> 

class Resource
{
public:
	std::shared_ptr<Resource> m_ptr {}; // 初始化为空
	
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	auto ptr1 { std::make_shared<Resource>() };

	ptr1->m_ptr = ptr1; // m_ptr 现在共享包含它的 Resource

	return 0;
}
```  

当 ptr1 离开作用域时，由于 Resource 的 m_ptr 仍在共享该资源，导致资源未被释放。程序输出：  

```
Resource acquired
```  

std::weak_ptr 的作用  
----------------  

std::weak_ptr（弱指针）专为解决上述"循环所有权"问题设计。它是观察者——可访问 std::shared_ptr 管理的对象，但不参与所有权计数。  

修改 Person 案例使用 std::weak_ptr：  

```cpp
#include <iostream>
#include <memory> 
#include <string>

class Person
{
	std::string m_name;
	std::weak_ptr<Person> m_partner; // 改为 std::weak_ptr

public:	
	Person(const std::string &name): m_name(name)
	{ 
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") };
	auto ricky { std::make_shared<Person>("Ricky") };

	partnerUp(lucy, ricky);

	return 0;
}
```  

现在输出符合预期：  

```
Lucy created
Ricky created
Lucy is now partnered with Ricky
Ricky destroyed
Lucy destroyed
```  

使用 std::weak_ptr  
----------------  

std::weak_ptr 不能直接使用（无 operator->），需先转换为 std::shared_ptr。使用 lock() 成员函数进行转换：  

```cpp
class Person
{
	// ...
	std::shared_ptr<Person> getPartner() const { return m_partner.lock(); }
};

int main()
{
	// ...
	auto partner = ricky->getPartner(); // 获取 Ricky 伙伴的 shared_ptr
	std::cout << ricky->getName() << "'s partner is: " << partner->getName() << '\n';
}
```  

避免悬空指针  
----------------  

std::weak_ptr 可通过 expired() 成员函数检测对象是否有效（返回 true 表示已失效）。示例：  

```cpp
std::weak_ptr<Resource> getWeakPtr()
{
	auto ptr{ std::make_shared<Resource>() };
	return std::weak_ptr<Resource>{ ptr };
} // ptr 离开作用域，Resource 被销毁

Resource* getDumbPtr()
{
	auto ptr{ std::make_unique<Resource>() };
	return ptr.get();
} // ptr 离开作用域，Resource 被销毁

int main()
{
	auto dumb{ getDumbPtr() };
	std::cout << "Dumb pointer: " << (dumb ? "有效\n" : "无效\n"); // 错误判断

	auto weak{ getWeakPtr() };
	std::cout << "Weak pointer: " << (weak.expired() ? "已过期\n" : "有效\n"); // 正确判断
}
```  

结论  
----------------  

std::shared_ptr 适用于需要共享所有权的场景，资源在最后一个共享指针离开作用域时释放。std::weak_ptr 适用于需要访问但不参与所有权管理的场景。  

测验  
----------------  

**问题1**  
修复"简化案例"中的程序，使其正确释放资源（不修改 main()）：  

```cpp
#include <iostream>
#include <memory> 

class Resource
{
public:
	std::weak_ptr<Resource> m_ptr {}; // 改为 weak_ptr
	
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	auto ptr1 { std::make_shared<Resource>() };
	ptr1->m_ptr = ptr1; 
	return 0;
}
```  

[下一课 22.x — 第22章总结与测验](Chapter-22/lesson22.x-chapter-22-summary-and-quiz.md)  
[返回主页](/)  
[上一课 22.6 — std::shared_ptr](Chapter-22/lesson22.6-stdshared_ptr.md)