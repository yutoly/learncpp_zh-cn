25.8 — 虚基类（virtual base classes）  
============================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日（首次发布于2008年1月28日）  

在上一章课程[24.9 — 多重继承](Chapter-24/lesson24.9-multiple-inheritance.md)中，我们遗留了"菱形问题"的讨论。本节将深入探讨该问题。  

注意：本节为高级主题，可视需要跳过或略读。  

**菱形问题**  
以下示例（包含构造函数）展示了菱形继承问题：  
```cpp
#include <iostream>

class PoweredDevice
{
public:
    PoweredDevice(int power)
    {
		std::cout << "PoweredDevice: " << power << '\n';
    }
};

class Scanner: public PoweredDevice
{
public:
    Scanner(int scanner, int power)
        : PoweredDevice{ power }
    {
		std::cout << "Scanner: " << scanner << '\n';
    }
};

class Printer: public PoweredDevice
{
public:
    Printer(int printer, int power)
        : PoweredDevice{ power }
    {
		std::cout << "Printer: " << printer << '\n';
    }
};

class Copier: public Scanner, public Printer
{
public:
    Copier(int scanner, int printer, int power)
        : Scanner{ scanner, power }, Printer{ printer, power }
    {
    }
};
```  
虽然预期继承关系应如下图所示：  
![](https://www.learncpp.com/images/CppTutorial/Section11/PoweredDevice.gif)  
但实际创建Copier类对象时，默认会生成两份PoweredDevice实例（分别来自Printer和Scanner），结构如下：  
![](https://www.learncpp.com/images/CppTutorial/Section11/PoweredDevice2.gif)  

通过以下示例验证：  
```cpp
int main()
{
    Copier copier{ 1, 2, 3 };
    return 0;
}
```  
输出结果：  
```
PoweredDevice: 3
Scanner: 1
PoweredDevice: 3
Printer: 2
```  
可见PoweredDevice被构造了两次。虽然有时需要此行为，但有时可能需要Scanner和Printer共享同一份PoweredDevice实例。  

**虚基类（virtual base classes）**  
要共享基类，只需在派生类继承列表中添加`virtual`关键字，创建**虚基类（virtual base class）**。此时继承树中仅存在一个基类对象，且只构造一次。简例：  
```cpp
class PoweredDevice {};

class Scanner: virtual public PoweredDevice {};
class Printer: virtual public PoweredDevice {};

class Copier: public Scanner, public Printer {};
```  
现在创建Copier对象时，Scanner和Printer将共享同一份PoweredDevice实例。  

但引发新问题：若Scanner和Printer共享PoweredDevice，由谁负责构造？答案是由Copier负责。Copier构造函数直接调用非直接父类构造函数：  
```cpp
#include <iostream>

class PoweredDevice
{
public:
    PoweredDevice(int power)
    {
		std::cout << "PoweredDevice: " << power << '\n';
    }
};

class Scanner: virtual public PoweredDevice // 注意：虚继承
{
public:
    Scanner(int scanner, int power)
        : PoweredDevice{ power } // 创建Scanner对象时需要此行，但此处被忽略
    {
		std::cout << "Scanner: " << scanner << '\n';
    }
};

class Printer: virtual public PoweredDevice // 注意：虚继承
{
public:
    Printer(int printer, int power)
        : PoweredDevice{ power } // 创建Printer对象时需要此行，但此处被忽略
    {
		std::cout << "Printer: " << printer << '\n';
    }
};

class Copier: public Scanner, public Printer
{
public:
    Copier(int scanner, int printer, int power)
        : PoweredDevice{ power }, // PoweredDevice在此构造
          Scanner{ scanner, power }, Printer{ printer, power }
    {
    }
};
```  
运行相同示例：  
```cpp
int main()
{
    Copier copier{ 1, 2, 3 };
    return 0;
}
```  
输出结果：  
```
PoweredDevice: 3
Scanner: 1
Printer: 2
```  
此时PoweredDevice仅构造一次。  

**关键细节**  
1. **构造顺序**：最末层派生类（most derived class）的虚基类优先于非虚基类构造，确保基类先于派生类构造。  
2. **构造函数调用**：Scanner和Printer的构造函数仍保留对PoweredDevice的调用。创建Copier时这些调用被忽略，但单独创建Scanner/Printer对象时仍会使用。  
3. **构造责任**：若类继承自虚基类，最末层派生类必须负责构造虚基类。即使单继承情况下（如Copier仅继承Printer），Copier仍需构造PoweredDevice。  
4. **内存开销**：所有继承虚基类的类都会包含虚表指针（virtual table pointer），增加实例大小。  

Scanner和Printer通过虚表机制定位共享的PoweredDevice子对象（存储子类到基类子对象的偏移量）。  

[下一课 25.9 对象切片](Chapter-25/lesson25.9-object-slicing.md)  
[返回主页](/)    
[上一课 25.7 纯虚函数、抽象基类与接口类](Chapter-25/lesson25.7-pure-virtual-functions-abstract-base-classes-and-interface-classes.md)