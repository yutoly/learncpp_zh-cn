22.x — 第22章总结与测验
===================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2017年5月3日（更新于2025年1月6日）  

**智能指针类（smart pointer class）**是组合类，用于管理动态分配的内存，确保智能指针对象超出作用域时释放内存。  

**拷贝语义（copy semantics）**允许类对象被复制，主要通过拷贝构造函数和拷贝赋值运算符实现。  

**移动语义（move semantics）**指类对象转移资源所有权而非复制，主要通过移动构造函数和移动赋值运算符实现。  

`std::auto_ptr`已弃用，应避免使用。  

**右值引用（r-value reference）**是专门用右值初始化的引用，使用双&符号创建。接收右值引用参数的函数是合理的，但几乎不应返回右值引用。  

当构造或赋值操作的参数是左值时，唯一合理的做法是拷贝左值。我们不能假设修改左值是安全的，因为后续程序可能继续使用它。对于表达式`a = b`，我们不会期望`b`被改变。  

然而当参数是右值时，我们知道这仅是临时对象。此时无需拷贝（可能昂贵），而是直接转移资源（更高效）。这种操作是安全的，因为临时对象在表达式结束后就会被销毁。  

使用`delete`关键字可禁用类的拷贝语义，通过删除拷贝构造函数和拷贝赋值运算符实现。  

`std::move`允许将左值视为右值，用于在左值上触发移动语义而非拷贝语义。  

`std::unique_ptr`是推荐使用的智能指针类，管理不可共享的单一资源。应优先使用`std::make_unique()`（C++14起）创建实例，其禁用拷贝语义。  

`std::shared_ptr`在需要多对象访问同一资源时使用。资源直到最后一个管理它的`shared_ptr`销毁后才会释放。应优先使用`std::make_shared()`创建实例，拷贝语义用于创建指向同一对象的其他`shared_ptr`。  

`std::weak_ptr`用于需要访问`shared_ptr`管理资源但不想参与生命周期管理的场景。当`shared_ptr`销毁时，`weak_ptr`的存在不影响资源释放。  

**测验时间**  

1. 解释何时应使用以下指针类型：  

1a) `std::unique_ptr`  
  
<details><summary>答案</summary>当需要智能指针管理不共享的动态对象时使用。</details>  

1b) `std::shared_ptr`  
  
<details><summary>答案</summary>当需要智能指针管理可能被共享的动态对象时使用。对象在所有`shared_ptr`销毁后释放。</details>  

1c) `std::weak_ptr`  
  
<details><summary>答案</summary>当需要访问`shared_ptr`管理的对象，但不想绑定`weak_ptr`与资源生命周期时使用。</details>  

1d) `std::auto_ptr`  
  
<details><summary>答案</summary>`auto_ptr`已弃用并在C++17移除，不应使用。</details>  

2. 解释为何移动语义围绕右值展开  
  
<details><summary>答案</summary>右值是临时对象，使用后即销毁。传递或返回右值时，移动资源比拷贝更高效。</details>  

3. 找出以下代码问题并优化至最佳实践：  

3a)  
```cpp
#include <iostream>
#include <memory> // for std::shared_ptr

class Resource {
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
};

int main() {
    auto* res{ new Resource{} };
    std::shared_ptr<Resource> ptr1{ res };
    std::shared_ptr<Resource> ptr2{ res };
    return 0;
}
```  
  
<details><summary>答案</summary>`ptr2`应从`ptr1`而非`res`创建。直接使用`res`会导致两个独立`shared_ptr`管理同一资源。应改用`std::make_shared`自动管理。</details>  

优化后代码：  
```cpp
#include <iostream>
#include <memory>

class Resource {
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
};

int main() {
    auto ptr1{ std::make_shared<Resource>() };
    auto ptr2{ ptr1 };
    return 0;
}
```

[下一课 23.1 对象关系](Chapter-23/lesson23.1-object-relationships.md)  
[返回主页](/)  
[上一课 22.7 std::shared_ptr循环依赖问题与std::weak_ptr](Chapter-22/lesson22.7-circular-dependency-issues-with-stdshared_ptr-and-stdweak_ptr.md)