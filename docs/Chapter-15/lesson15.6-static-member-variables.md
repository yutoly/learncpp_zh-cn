15.6 — 静态成员变量  
===============================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年9月14日上午9:50（太平洋夏令时）  
2024年12月2日  

在课程[7.4 — 全局变量简介](Chapter-7/lesson7.4-introduction-to-global-variables.md)中我们介绍了全局变量，在课程[7.11 — 静态局部变量](Chapter-7/lesson7.11-static-local-variables.md)中介绍了静态局部变量。这两类变量都具有**静态存储期（static duration）**，即在程序启动时创建，程序结束时销毁。即使离开作用域，这些变量也能保持其值。  

例如：  

```cpp
#include <iostream>

int generateID()
{
    static int s_id{ 0 }; // 静态局部变量
    return ++s_id;
}

int main()
{
    std::cout << generateID() << '\n';
    std::cout << generateID() << '\n';
    std::cout << generateID() << '\n';
    return 0;
}
```  

该程序输出：  

```
1
2
3
```  

注意静态局部变量`s_id`在多次函数调用间保持了其值。  

类类型为`static`关键字带来两个新用途：**静态成员变量（static member variables）**和静态成员函数。本文将讨论静态成员变量，静态成员函数将在下节课讲解。  

### 静态成员变量  
在探讨成员变量的`static`关键字前，先观察以下类：  

```cpp
#include <iostream>

struct Something
{
    int value{ 1 };
};

int main()
{
    Something first{};
    Something second{};
    first.value = 2;
    std::cout << first.value << '\n';
    std::cout << second.value << '\n';
    return 0;
}
```  

实例化类对象时，每个对象都获得普通成员变量的独立副本。此例中声明两个`Something`对象，因此存在两个`value`副本：`first.value`和`second.value`互不相同。程序输出：  

```
2
1
```  

使用`static`关键字可将类的成员变量声明为静态。与普通成员变量不同，**静态成员变量（static member variables）**由类的所有对象共享：  

```cpp
#include <iostream>

struct Something
{
    static int s_value; // 声明静态成员变量（初始化移至下方）
};

int Something::s_value{ 1 }; // 定义并初始化s_value为1

int main()
{
    Something first{};
    Something second{};
    first.s_value = 2;
    std::cout << first.s_value << '\n';
    std::cout << second.s_value << '\n';
    return 0;
}
```  

程序输出：  

```
2
2
```  

由于`s_value`是静态成员变量，它在所有类对象间共享。因此`first.s_value`与`second.s_value`是同一变量。  

### 静态成员独立于类对象  
虽然可通过类对象访问静态成员（如上述示例），但即使未实例化任何类对象，静态成员依然存在！其生命周期与程序相同，不受类对象约束。  

> **关键洞察**  
> 静态成员本质上是存在于类作用域内的全局变量。  

因此可直接通过类名和作用域解析运算符访问静态成员（如`Something::s_value`）：  

```cpp
class Something
{
public:
    static int s_value; 
};

int Something::s_value{ 1 }; 

int main()
{
    Something::s_value = 2; // 未实例化对象直接访问
    std::cout << Something::s_value << '\n';
    return 0;
}
```  

> **最佳实践**  
> 使用类名和作用域解析运算符（::）访问静态成员。  

### 定义与初始化静态成员变量  
在类内声明静态成员变量仅告知编译器其存在，需在全局作用域显式定义（类似全局变量）：  

```cpp
int Something::s_value{ 1 }; // 全局作用域定义并初始化
```  

此行完成两项操作：实例化静态成员变量并初始化。若未提供初始值，静态成员变量默认执行**零值初始化（zero-initialized）**。  

> 注意：  
> - 静态成员定义不受访问控制限制（即使声明为private也可定义）  
> - 非模板类：头文件中定义类时，静态成员定义通常置于关联代码文件（如`Something.cpp`）  
> - 模板类：静态成员定义直接置于模板类下方  

### 类内初始化静态成员变量  
以下情况允许类内初始化：  
1. **常量整型（含char/bool）或const枚举类型**：  
   ```cpp
   class Whatever {
       static const int s_value{ 4 }; // 直接初始化
   };
   ```  
2. **C++17起支持内联变量**：  
   ```cpp
   class Whatever {
       static inline int s_value{ 4 }; // 非const也可初始化
   };
   ```  
3. **constexpr成员（C++17起隐式内联）**：  
   ```cpp
   class Whatever {
       static constexpr double s_value{ 2.2 }; // 无需inline关键字
   };
   ```  

> **最佳实践**  
> 优先将静态成员声明为`inline`或`constexpr`以便类内初始化。  

### 静态成员变量应用示例  
静态成员变量的典型应用是为类实例分配唯一ID：  

```cpp
#include <iostream>

class Something
{
private:
    static inline int s_idGenerator{ 1 }; // ID生成器
    int m_id{}; // 实例ID

public:
    Something() : m_id{ s_idGenerator++ } {} // 构造时分配递增ID
    int getID() const { return m_id; }
};

int main()
{
    Something first, second, third;
    std::cout << first.getID() << '\n';  // 输出1
    std::cout << second.getID() << '\n'; // 输出2
    std::cout << third.getID() << '\n';  // 输出3
    return 0;
}
```  

此机制保证每个`Something`对象获得按创建顺序递增的唯一ID，在调试或处理对象数组时特别有用。  

静态成员变量还适用于共享数据场景（如预计算值的**查找表（lookup table）**），避免每个对象创建副本以节省内存。  

### 仅静态成员支持类型推导  
静态成员可使用`auto`推导类型或**类模板实参推导（CTAD, Class Template Argument Deduction）**，非静态成员则禁止：  

```cpp
class Foo {
    static inline auto s_x{5};          // 合法：auto推导
    static inline std::pair s_v{1,2.3}; // 合法：CTAD推导
    
    auto m_x{5};           // 错误：非静态成员禁用auto
    std::pair m_v{1,2.3};  // 错误：非静态成员禁用CTAD
};
```  

此限制源于非静态成员使用类型推导可能引发歧义，而静态成员无此问题。  

[下一课 15.7 静态成员函数](Chapter-15/lesson15.7-static-member-functions.md)  
[返回主页](/)  
[上一课 15.5 含成员函数的类模板](Chapter-15/lesson15.5-class-templates-with-member-functions.md)