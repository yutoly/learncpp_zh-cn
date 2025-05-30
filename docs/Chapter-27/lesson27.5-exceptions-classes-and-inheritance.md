27.5 — 异常、类与继承  
============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月29日（首次发布于2008年10月26日）  

**异常与成员函数**  

在本教程至此，我们仅见过非成员函数中的异常应用。然而异常在成员函数中同样有效，特别是在重载运算符中。考虑以下作为简单整型数组类组成部分的重载[]运算符：  

```cpp
int& IntArray::operator[](const int index)
{
    return m_data[index];
}
```  

虽然该函数在索引有效时表现良好，但缺乏完善的错误检查机制。我们可以添加断言语句确保索引有效性：  

```cpp
int& IntArray::operator[](const int index)
{
    assert (index >= 0 && index < getLength());
    return m_data[index];
}
```  

现在若用户传入无效索引，程序将触发断言错误。由于重载运算符对参数数量和类型有严格限制，无法通过返回错误码或布尔值通知调用者。但异常机制不改变函数签名，在此处可发挥重要作用：  

```cpp
int& IntArray::operator[](const int index)
{
    if (index < 0 || index >= getLength())
        throw index;

    return m_data[index];
}
```  

此时若传入无效索引，operator[]将抛出int类型异常。  

**构造函数失败处理**  

构造函数是类中另一个适合使用异常的场景。若构造函数因故失败（如用户传入非法输入），可通过抛出异常表明对象创建失败。此时对象构造中止，所有已初始化的类成员将按常规流程析构。  

但类的析构函数不会执行（因对象未完成构造）。由于析构函数未调用，不能依赖其清理已分配资源。  

若在构造函数中分配资源后发生异常，如何确保资源正确释放？一种方法是将可能失败的代码包裹在try块中，用catch块捕获异常并清理，随后重新抛出异常（详见课程[27.6 — 重新抛出异常](Chapter-27/lesson27.6-rethrowing-exceptions.md)）。但这种方法使代码冗长且易错，特别是涉及多资源分配时。  

更优解是利用类成员析构的特性：若资源分配由类成员（而非构造函数自身）完成，成员析构时将自动清理资源。示例：  

```cpp
#include <iostream>

class Member
{
public:
	Member() { std::cerr << "Member分配了资源\n"; }
	~Member() { std::cerr << "Member清理资源\n"; }
};

class A
{
private:
	int m_x{};
	Member m_member;

public:
	A(int x) : m_x{x}
	{
		if (x <= 0) throw 1;
	}
	
	~A() { std::cerr << "~A\n"; } // 不会执行
};

int main()
{
	try { A a{0}; }
	catch (int) { std::cerr << "异常发生\n"; }
	return 0;
}
```  

输出：  

```
Member分配了资源
Member清理资源
异常发生
```  

当类A抛出异常时，其所有成员将被析构。m_member的析构函数得以调用，完成资源清理。这正是RAII（资源获取即初始化，见课程[19.3 — 析构函数](Chapter-15/lesson15.4-introduction-to-destructors.md)）的核心优势——即使在异常情况下，RAII类也能自我清理。  

建议使用标准库提供的RAII类管理资源，如文件（std::fstream，见[28.6 — 基础文件I/O](Chapter-28/lesson28.6-basic-file-io.md)）和动态内存（std::unique_ptr等智能指针，见[22.1 — 智能指针与移动语义简介](Chapter-22/lesson22.1-introduction-to-smart-pointers-move-semantics.md)）。例如：  

```cpp
// 改进前
class Foo {
    int* ptr; // 需手动管理
};

// 改进后
class Foo {
    std::unique_ptr<int> ptr; // 自动管理
};
```  

**异常类（Exception Classes）**  

使用基本数据类型（如int）作为异常类型的核心问题是含义模糊。更严重的问题在于try块中多个语句可能抛出相同类型异常时难以区分。  

解决方案是使用异常类（exception class）——专门设计用于抛出的常规类。为IntArray类设计异常类示例：  

```cpp
#include <string>
#include <string_view>

class ArrayException
{
private:
	std::string m_error;

public:
	ArrayException(std::string_view error) : m_error{error} {}
	const std::string& getError() const { return m_error; }
};
```  

完整示例程序：  

```cpp
class IntArray
{
private:
	int m_data[3]{};

public:
	int& operator[](const int index)
	{
		if (index < 0 || index >= 3)
			throw ArrayException{"无效索引"};
		return m_data[index];
	}
};

int main()
{
	IntArray array;
	try { int value{ array[5] }; }
	catch (const ArrayException& e) {
		std::cerr << "数组异常：" << e.getError() << '\n';
	}
	return 0;
}
```  

通过此类设计，异常可携带具体错误描述。由于ArrayException是唯一类型，可专门捕获数组类异常并区别处理。  

> **最佳实践**  
> 捕获类类型异常时应使用（const）引用，避免昂贵拷贝和对象切割（object slicing）。基础类型异常可值捕获。  

**异常与继承**  

由于异常类可继承，需注意派生类异常的处理顺序。示例：  

```cpp
try { throw Derived(); }
catch (const Base&) { std::cerr << "捕获基类"; }
catch (const Derived&) { std::cerr << "捕获派生类"; } // 不会执行
```  

输出：`捕获基类`。派生类异常会被基类处理器捕获，因此应将派生类处理器前置。  

**std::exception**  

标准库多数异常类派生自std::exception（定义于\<exception\>头文件）。通过捕获std::exception引用，可处理所有标准异常：  

```cpp
#include <exception>
#include <iostream>
#include <string>

int main()
{
	try {
		std::string s;
		s.resize(std::numeric_limits<size_t>::max());
	}
	catch (const std::exception& e) {
		std::cerr << "标准异常：" << e.what() << '\n';
	}
	return 0;
}
```  

std::exception提供虚函数what()返回异常描述。多数派生类重写此函数。  

**自定义异常类**  

可从std::exception或std::runtime_error派生自定义异常类。示例：  

```cpp
#include <stdexcept>

class ArrayException : public std::runtime_error
{
public:
	ArrayException(const std::string& error)
		: std::runtime_error{error} {}
};

// 使用
int& operator[](int index)
{
	if (index < 0 || index >= 3)
		throw ArrayException("无效索引");
	return m_data[index];
}
```  

**异常对象生命周期**  

异常对象通常是栈上的临时对象，但在抛出时会被复制到专用存储区，确保栈展开后仍存在。因此异常对象必须可复制。若抛出不可复制的派生类对象将导致编译错误：  

```cpp
class Derived : public Base {
public:
	Derived(const Derived&) = delete; // 不可复制
};

int main()
{
	Derived d;
	throw d; // 错误：拷贝构造函数被删除
}
```  

异常对象不应持有栈对象的指针/引用，因栈展开可能导致悬垂引用。  

[下一课 27.6 重新抛出异常](Chapter-27/lesson27.6-rethrowing-exceptions.md)  
[返回主页](/)  
[上一课 27.4 未捕获异常与通用处理器](Chapter-27/lesson27.4-uncaught-exceptions-catch-all-handlers.md)