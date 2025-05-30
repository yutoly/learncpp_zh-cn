22.1 — 智能指针与移动语义入门  
=========================================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月4日（首次发布于2017年2月17日）  

考虑一个需要动态分配内存的函数：  
```cpp
void someFunction()
{
    Resource* ptr = new Resource(); // Resource 是结构体或类

    // 在此处使用 ptr

    delete ptr;
}
```  
虽然这段代码看似简单，但很容易忘记释放 ptr。即使记得在函数末尾删除 ptr，如果函数提前退出，仍可能导致内存未释放。例如通过提前返回实现：  
```cpp
#include <iostream>

void someFunction()
{
    Resource* ptr = new Resource();

    int x;
    std::cout << "输入整数：";
    std::cin >> x;

    if (x == 0)
        return; // 函数提前返回，ptr 未被删除！

    // 在此处使用 ptr

    delete ptr;
}
```  
或通过抛出异常：  
```cpp
#include <iostream>

void someFunction()
{
    Resource* ptr = new Resource();

    int x;
    std::cout << "输入整数：";
    std::cin >> x;

    if (x == 0)
        throw 0; // 函数提前返回，ptr 未被删除！

    // 在此处使用 ptr

    delete ptr;
}
```  
在上述程序中，提前返回或抛出异常会导致函数终止而未删除 ptr。因此为 ptr 分配的内存将泄漏（每次调用该函数并提前返回时都会重复泄漏）。  

这类问题的根源在于指针变量本身不具备自动清理机制。  

**智能指针类的救赎？**  
类的最佳特性之一是包含析构函数（destructor），当类对象离开作用域时自动执行。如果在构造函数中分配（或获取）内存，可以在析构函数中释放，确保类对象销毁时内存被释放（无论其因离开作用域还是显式删除）。这正是我们在课程[19.3 — 析构函数](Chapter-15/lesson15.4-introduction-to-destructors.md)中讨论的 RAII（资源获取即初始化）编程范式的核心。  

考虑一个专门管理指针所有权的类：  
```cpp
#include <iostream>

template <typename T>
class Auto_ptr1
{
	T* m_ptr {};
public:
	// 通过构造函数获取指针"所有权"
	Auto_ptr1(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	// 析构函数确保释放内存
	~Auto_ptr1()
	{
		delete m_ptr;
	}

	// 重载解引用和->运算符以模仿指针行为
	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
};

// 测试类
class Resource
{
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	Auto_ptr1<Resource> res(new Resource());

	return 0;
} // res 离开作用域时自动销毁 Resource
```  
程序输出：  
```
Resource acquired
Resource destroyed
```  
当 Auto_ptr1 作为局部变量声明时，无论函数如何终止，Resource 指针都会被正确销毁。这种类称为智能指针（smart pointer）。**智能指针**是管理动态内存的组合类，确保内存在其离开作用域时被释放（内置指针因此被称为"哑指针（dumb pointers）"）。  

用智能指针改造示例：  
```cpp
void someFunction()
{
    Auto_ptr1<Resource> ptr(new Resource());
 
    int x;
    std::cout << "输入整数：";
    std::cin >> x;
 
    if (x == 0)
        return; // 函数提前返回
 
    ptr->sayHi();
}
```  
无论用户输入是否为0，Resource 都会被正确释放。  

**致命缺陷**  
Auto_ptr1 类存在严重缺陷：未处理拷贝构造函数和赋值运算符。考虑以下程序：  
```cpp
int main()
{
	Auto_ptr1<Resource> res1(new Resource());
	Auto_ptr1<Resource> res2(res1); // 浅拷贝

	return 0;
} // res1 和 res2 尝试删除同一指针
```  
这将导致双重删除和未定义行为。函数传值时也会出现类似问题：  
```cpp
void passByValue(Auto_ptr1<Resource> res) {}

int main()
{
	Auto_ptr1<Resource> res1(new Resource());
	passByValue(res1); // 拷贝后导致悬空指针
	return 0;
}
```  

**移动语义（Move Semantics）**  
解决方案是转移指针所有权而非拷贝。更新后的 Auto_ptr2 实现：  
```cpp
template <typename T>
class Auto_ptr2
{
	T* m_ptr {};
public:
	// 移动语义拷贝构造函数
	Auto_ptr2(Auto_ptr2& a)
	{
		m_ptr = a.m_ptr; // 转移所有权
		a.m_ptr = nullptr; // 清空源指针
	}
	
	// 移动语义赋值运算符
	Auto_ptr2& operator=(Auto_ptr2& a)
	{
		if (&a == this) return *this;
		delete m_ptr;
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr;
		return *this;
	}
};
```  
使用示例：  
```cpp
int main()
{
	Auto_ptr2<Resource> res1(new Resource());
	Auto_ptr2<Resource> res2; 

	res2 = res1; // 所有权转移

	return 0;
}
```  
程序正确输出：  
```
Resource acquired
Resource destroyed
```  

**std::auto_ptr 及其缺陷**  
C++98 引入的 std::auto_ptr（C++17 移除）是首个标准智能指针，其实现类似 Auto_ptr2。但存在以下问题：  
1. 通过拷贝构造函数实现移动语义，导致函数传值意外转移所有权  
2. 使用非数组 delete，无法正确处理动态数组  
3. 与标准库容器算法不兼容  

**发展方向**  
C++11 正式定义移动语义，引入新智能指针：  
* std::unique_ptr（替代 auto_ptr）  
* std::shared_ptr  
* std::weak_ptr  

[下一课 22.2 — 右值引用](Chapter-22/lesson22.2-rvalue-references.md)  
[返回主页](/)  
[上一课 21.y — 第21章项目](Chapter-21/lesson21.y-chapter-21-project.md)