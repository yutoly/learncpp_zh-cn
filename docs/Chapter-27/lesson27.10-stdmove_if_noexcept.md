27.10 — std::move\_if\_noexcept  
================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月15日（首次发布于2020年8月16日）  

（鸣谢读者 Koe 提供本课初稿！）  

在课程 [22.4 — std::move](Chapter-22/lesson22.4-stdmove.md) 中，我们介绍了 `std::move`，它将左值实参强制转换为右值以启用移动语义。在课程 [27.9 — 异常规范与 noexcept](Chapter-27/lesson27.9-exception-specifications-and-noexcept.md) 中，我们介绍了 `noexcept` 异常说明符和运算符。本节将结合这两个概念展开。  

我们还介绍了**强异常保证（strong exception guarantee）**，它确保函数若被异常中断，不会发生内存泄漏且程序状态保持不变。特别地，所有构造函数都应遵守强异常保证，以避免对象构造失败时影响程序其他状态。  

### 移动构造函数的异常问题  

考虑复制对象时因某些原因（如内存耗尽）失败的情况。此时被复制对象不会受损，因为创建副本无需修改源对象。我们可以放弃失败的副本并继续执行，**强异常保证**得以维持。  

现在考虑移动对象的情况：移动操作将资源所有权从源对象转移至目标对象。若所有权转移后移动操作被异常中断，源对象将处于被修改状态。当源对象是临时对象且移动后将被丢弃时，这没有问题——但对于非临时对象，源对象已被破坏。为满足**强异常保证**，我们需将资源移回源对象，但如果首次移动已失败，则无法保证回移操作能成功。  

### 解决方案：std::move\_if\_noexcept  

如何让移动构造函数满足强异常保证？避免在移动构造函数体内抛出异常相对简单，但移动构造函数可能调用**可能抛出异常（potentially throwing）**的其他构造函数。以 `std::pair` 的移动构造函数为例，它必须尝试将源对中的每个子对象移动构造到新对对象中：  

```cpp
// std::pair 的移动构造函数示例
// 接收'old'对，并移动构造新对的'first'和'second'子对象
template <typename T1, typename T2>
pair<T1,T2>::pair(pair&& old)
  : first(std::move(old.first)),
    second(std::move(old.second))
{}
```  

使用 `MoveClass` 和 `CopyClass` 类组成对（pair）来演示移动构造函数的强异常保证问题：  

```cpp
#include <iostream>
#include <utility>    // 提供 std::pair, std::make_pair, std::move, std::move_if_noexcept
#include <stdexcept>  // 提供 std::runtime_error

class MoveClass { /* 实现略 */ };

class CopyClass {
public:
  bool m_throw{};
  CopyClass() = default;
  
  // 当源对象 m_throw 为 true 时，复制构造函数抛出异常
  CopyClass(const CopyClass& that) : m_throw{ that.m_throw } {
    if (m_throw) throw std::runtime_error{ "abort!" };
  }
};

int main() {
  std::pair my_pair{ MoveClass{ 13 }, CopyClass{} };
  std::cout << "my_pair.first: " << my_pair.first << '\n';
  
  try {
    my_pair.second.m_throw = true;  // 触发复制构造函数异常
    
    // 下行将抛出异常
    std::pair moved_pair{ std::move(my_pair) };  // 稍后将注释此行
    // std::pair moved_pair{ std::move_if_noexcept(my_pair) }; // 稍后将取消注释
  }
  catch (const std::exception& ex) {
    std::cerr << "Error found: " << ex.what() << '\n';
  }
  std::cout << "my_pair.first: " << my_pair.first << '\n';
  return 0;
}
```  

### 关键洞察  

`std::move_if_noexcept` 在对象具有 noexcept 移动构造函数时返回可移动右值，否则返回可复制左值。通过结合 `noexcept` 说明符与 `std::move_if_noexcept`，可在存在强异常保证时使用移动语义（否则使用复制语义）。  

### 标准库实践  

标准库频繁使用 `std::move_if_noexcept` 优化 noexcept 函数。例如：  
- `std::vector::resize` 在元素类型具 noexcept 移动构造函数时使用移动语义，否则使用复制语义  
- 这意味着 `std::vector` 对具 noexcept 移动构造函数的对象通常运行更快  

> **警告**  
> 若类型同时具有可能抛出异常的移动语义和已删除的复制语义（复制构造函数/赋值运算符不可用），`std::move_if_noexcept` 将豁免强保证并调用移动语义。这种有条件豁免在标准库容器类中普遍存在。  

[下一课 27.x 第27章总结与测验](Chapter-27/lesson27.x-chapter-27-summary-and-quiz.md)  
[返回主页](/)  
[上一课 27.9 异常规范与 noexcept](Chapter-27/lesson27.9-exception-specifications-and-noexcept.md)