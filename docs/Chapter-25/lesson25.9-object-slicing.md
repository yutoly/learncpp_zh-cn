25.9 — 对象切片  
======================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年10月28日（首次发布于2016年11月19日）  

让我们回顾之前的示例：  

```cpp
#include <iostream>
#include <string_view>

class Base
{
protected:
    int m_value{};
 
public:
    Base(int value)
        : m_value{ value }
    {
    }

    virtual ~Base() = default;

    virtual std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};
 
class Derived: public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }
 
   std::string_view getName() const override { return "Derived"; }
};

int main()
{
    Derived derived{ 5 };
    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';
 
    Base& ref{ derived };
    std::cout << "ref is a " << ref.getName() << " and has value " << ref.getValue() << '\n';
 
    Base* ptr{ &derived };
    std::cout << "ptr is a " << ptr->getName() << " and has value " << ptr->getValue() << '\n';
 
    return 0;
}
```  

上述示例中，ref引用且ptr指向derived对象，该对象包含Base部分和Derived部分。由于ref和ptr是Base类型，它们只能看到derived的Base部分——Derived部分仍然存在，但无法通过ref或ptr访问。通过虚函数（virtual functions）机制，我们可以访问最派生的函数版本。因此程序输出：  

```
derived is a Derived and has value 5
ref is a Derived and has value 5
ptr is a Derived and has value 5
```  

但若将Derived对象直接赋值给Base对象会发生什么？  

```cpp
int main()
{
    Derived derived{ 5 };
    Base base{ derived }; // 这里会发生什么？
    std::cout << "base is a " << base.getName() << " and has value " << base.getValue() << '\n';

    return 0;
}
```  

derived对象包含Base部分和Derived部分。当赋值给Base对象时，仅复制Derived对象中的Base部分，Derived部分被"切掉"。这种现象称为**对象切片（object slicing）**。由于base始终是Base类型，其虚函数指针仍指向Base的虚函数表。因此base.getName()解析为Base::getName()。  

程序输出：  
```
base is a Base and has value 5
```  

谨慎使用切片可能无害，但错误使用会导致意外结果。我们来分析几种典型情况。  

函数参数切片  
----------------  

考虑以下函数：  

```cpp
void printName(const Base base) // 注意：base按值传递
{
    std::cout << "我是" << base.getName() << '\n';
}
```  

当以值传递方式调用时：  

```cpp
int main()
{
    Derived d{ 5 };
    printName(d); // 注意调用端是值传递

    return 0;
}
```  

虽然期望调用派生类版本，但实际上Derived对象d被切片，仅复制Base部分。程序输出：  
```
我是Base
```  

通过改为引用传递可避免此问题：  

```cpp
void printName(const Base& base) // 改为引用传递
{
    std::cout << "我是" << base.getName() << '\n';
}

int main()
{
    Derived d{ 5 };
    printName(d);

    return 0;
}
```  

输出：  
```
我是Derived
```  

向量中的切片  
----------------  

使用std::vector实现多态时可能遇到切片问题：  

```cpp
#include <vector>

int main()
{
	std::vector<Base> v{};
	v.push_back(Base{ 5 });    // 添加Base对象
	v.push_back(Derived{ 6 }); // 添加Derived对象

	for (const auto& element : v)
		std::cout << "我是" << element.getName() << "，值为" << element.getValue() << '\n';

	return 0;
}
```  

输出：  
```
我是Base，值为5
我是Base，值为6
```  

解决方案之一是使用指针向量：  

```cpp
#include <vector>

int main()
{
	std::vector<Base*> v{};
	
	Base b{ 5 }; // 不能使用匿名对象
	Derived d{ 6 };

	v.push_back(&b); // 添加Base对象
	v.push_back(&d); // 添加Derived对象

	for (const auto* element : v)
		std::cout << "我是" << element->getName() << "，值为" << element->getValue() << '\n';

	return 0;
}
```  

输出：  
```
我是Base，值为5
我是Derived，值为6
```  

另一个方案是使用std::reference_wrapper（引用包装器）：  

```cpp
#include <functional>
#include <vector>

int main()
{
	std::vector<std::reference_wrapper<Base>> v{};

	Base b{ 5 };
	Derived d{ 6 };

	v.push_back(b); // 添加Base对象
	v.push_back(d); // 添加Derived对象

	for (const auto& element : v)
		std::cout << "我是" << element.get().getName() << "，值为" << element.get().getValue() << '\n';

	return 0;
}
```  

弗兰肯对象（Frankenobject）  
----------------  

考虑以下代码：  

```cpp
int main()
{
    Derived d1{ 5 };
    Derived d2{ 6 };
    Base& b{ d2 };

    b = d1; // 问题语句

    return 0;
}
```  

由于b是Base引用，赋值操作符调用Base的版本，仅复制Base部分。结果d2将包含d1的Base部分和自身的Derived部分，形成混合对象。这种情况称为**弗兰肯对象**。  

解决方案可通过禁止Base类的拷贝操作（删除拷贝构造函数和赋值运算符）。  

结论  
----------------  

尽管C++支持通过对象切片进行派生类到基类的赋值，但通常应避免此操作。确保函数参数使用引用（或指针），在处理派生类时尽量避免值传递。  

[下一课 25.10 — 动态转换](Chapter-25/lesson25.10-dynamic-casting.md)  
[返回主页](/)  
[上一课 25.8 — 虚基类](Chapter-25/lesson25.8-virtual-base-classes.md)