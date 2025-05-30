22.5 — std::unique_ptr（唯一指针）
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月20日（首次发布于2017年3月15日）  

本章开篇时我们讨论过指针在某些情况下可能导致错误和内存泄漏。例如当函数提前返回或抛出异常时，指针可能无法被正确删除：  
```cpp
#include <iostream>
 
void someFunction()
{
    auto* ptr{ new Resource() };
 
    int x{};
    std::cout << "输入整数: ";
    std::cin >> x;
 
    if (x == 0)
        throw 0; // 函数提前返回，ptr 将不会被删除！
 
    // 在此使用 ptr
 
    delete ptr;
}
```  

在学习了移动语义的基础知识后，我们可以重新讨论智能指针类。智能指针的核心特征是管理用户提供的动态分配资源，并确保在适当时机（通常是智能指针离开作用域时）正确清理资源。因此，智能指针本身不应被动态分配（否则可能导致智能指针未被正确释放，进而导致内存泄漏）。通过始终在栈上分配智能指针（作为局部变量或类的组合成员），可以确保其正确离开作用域。  

C++11标准库提供4种智能指针类：std::auto_ptr（C++17移除）、std::unique_ptr（唯一指针）、std::shared_ptr（共享指针）和std::weak_ptr（弱指针）。其中std::unique_ptr是最常用的智能指针类。  

std::unique_ptr  
----------------  

std::unique_ptr是C++11用来替代std::auto_ptr的智能指针。它用于管理不被多个对象共享的动态分配对象，完全拥有其管理的对象。该类型定义于\<memory\>头文件中。  

基础示例：  
```cpp
#include <iostream>
#include <memory> // 包含 std::unique_ptr

class Resource
{
public:
	Resource() { std::cout << "资源获取\n"; }
	~Resource() { std::cout << "资源销毁\n"; }
};

int main()
{
	// 分配 Resource 对象并由 std::unique_ptr 管理
	std::unique_ptr<Resource> res{ new Resource() };

	return 0;
} // res 在此处离开作用域，管理的资源被销毁
```  

由于std::unique_ptr在栈上分配，离开作用域时会自动删除其管理的资源。与std::auto_ptr不同，std::unique_ptr正确实现了移动语义：  
```cpp
#include <utility> // 包含 std::move

int main()
{
	std::unique_ptr<Resource> res1{ new Resource{} }; // 在此创建资源
	std::unique_ptr<Resource> res2{}; // 初始化为空指针

	res2 = std::move(res1); // res2 接管所有权，res1 设为空

	return 0;
} // res2 离开作用域时销毁资源
```  

std::unique_ptr禁用拷贝语义，要转移所有权必须使用移动语义（通过std::move实现）。  

访问托管对象  
----------------  
std::unique_ptr重载了operator*和operator->用于访问托管资源。使用前应通过bool转换检查是否持有资源：  
```cpp
if (res) // 通过隐式bool转换检查资源存在
	std::cout << *res << '\n'; // 使用 operator* 访问资源
```  

数组处理  
----------------  
std::unique_ptr能自动识别标量删除和数组删除。但通常更推荐使用std::array、std::vector或std::string管理数组。  

最佳实践  
----------------  
优先使用std::array、std::vector或std::string代替智能指针管理数组或C风格字符串。  

std::make_unique  
----------------  
C++14引入的std::make_unique函数模板用于构造对象并初始化：  
```cpp
auto f1{ std::make_unique<Fraction>(3, 5) }; // 创建单个对象
auto f2{ std::make_unique<Fraction[]>(4) }; // 创建对象数组
```  

推荐使用std::make_unique而非直接new，因为：  
1. 代码更简洁  
2. 解决C++14之前的异常安全问题  
3. C++17后修复了函数参数求值顺序问题  

异常安全问题详解  
----------------  
考虑以下可能引发资源泄漏的场景：  
```cpp
some_function(std::unique_ptr<T>(new T), function_that_can_throw_exception());
```  
若先执行new T，后调用可能抛出异常的函数，将导致T泄漏。std::make_unique在函数内部完成对象创建和智能指针构造，避免了此问题。  

从函数返回std::unique_ptr  
----------------  
通过值返回std::unique_ptr是安全的：  
```cpp
std::unique_ptr<Resource> createResource()
{
     return std::make_unique<Resource>(); // C++17起支持返回值优化
}
```  

传递std::unique_ptr给函数  
----------------  
要让函数接管所有权时，应通过值传递并使用std::move：  
```cpp
void takeOwnership(std::unique_ptr<Resource> res)
{
     if (res)
          std::cout << *res << '\n';
} // 资源在此销毁

takeOwnership(std::move(ptr)); // 转移所有权
```  

若不需要所有权转移，建议传递原始指针（通过get()获取）或引用：  
```cpp
void useResource(const Resource* res)
{
	if (res)
		std::cout << *res << '\n';
}

useResource(ptr.get()); // 使用 get() 获取原始指针
```  

类中的使用  
----------------  
std::unique_ptr可作为类成员，自动管理资源生命周期。但需注意若类对象未被正确销毁，其管理的资源也会泄漏。  

常见误用  
----------------  
1. 多个智能指针管理同一资源：  
```cpp
Resource* res{ new Resource() };
std::unique_ptr<Resource> res1{ res };
std::unique_ptr<Resource> res2{ res }; // 导致重复删除
```  

2. 手动删除托管资源：  
```cpp
delete res; // 导致智能指针重复删除
```  

使用std::make_unique可避免上述问题。  

测验解答  
----------------  
将普通指针转换为std::unique_ptr的示例：  
```cpp
#include <memory>

int main()
{
	auto ptr{ std::make_unique<Fraction>(3, 5) };
	printFraction(ptr.get());
	return 0;
}
```  

[下一课 22.6 — std::shared_ptr（共享指针）](Chapter-22/lesson22.6-stdshared_ptr.md)  
[返回主页](/)  
[上一课 22.4 — std::move（移动语义）](Chapter-22/lesson22.4-stdmove.md)