19.3 — 析构函数  
================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年9月6日 上午9:14（太平洋夏令时间）  
2023年11月30日  

**析构函数（destructor）**是另一类特殊的类成员函数，当该类的对象被销毁时执行。构造函数（constructor）用于初始化类，而析构函数则负责清理工作。

当对象正常离开作用域，或使用`delete`关键字显式删除动态分配的对象时，类析构函数会自动调用（若存在），以便在对象从内存移除前完成必要清理。对于简单类（仅初始化普通成员变量值），无需析构函数，因为C++会自动清理内存。

然而，若类对象持有任何资源（如动态内存、文件或数据库句柄），或需在对象销毁前执行维护操作，析构函数是最佳选择——它通常是对象销毁前最后执行的函数。

析构函数命名规则  
----------------

与构造函数类似，析构函数有特定命名规则：

1. 析构函数名必须与类名相同，前面加波浪号（~）
2. 析构函数不能接受参数
3. 析构函数无返回类型

一个类只能拥有一个析构函数。

通常不应显式调用析构函数（因对象销毁时会自动调用），因多次清理同一对象的情况罕见。但析构函数可安全调用其他成员函数，因析构函数执行完毕后对象才会销毁。

析构函数示例  
----------------

以下示例演示使用析构函数的简单类：

```cpp
#include <iostream>
#include <cassert>
#include <cstddef>

class IntArray
{
private:
	int* m_array{};
	int m_length{};

public:
	IntArray(int length) // 构造函数
	{
		assert(length > 0);

		m_array = new int[static_cast<std::size_t>(length)]{};
		m_length = length;
	}

	~IntArray() // 析构函数
	{
		// 释放构造函数中分配的数组
		delete[] m_array;
	}

	void setValue(int index, int value) { m_array[index] = value; }
	int getValue(int index) { return m_array[index]; }

	int getLength() { return m_length; }
};

int main()
{
	IntArray ar ( 10 ); // 分配10个整型空间
	for (int count{ 0 }; count < ar.getLength(); ++count)
		ar.setValue(count, count+1);

	std::cout << "元素5的值为：" << ar.getValue(5) << '\n';

	return 0;
} // ar在此处销毁，~IntArray()析构函数被调用
```

> **提示**  
> 若编译时出现以下错误：
> ```
> error: 'class IntArray' has pointer data members [-Werror=effc++]|
> error:   but does not override 'IntArray(const IntArray&)' [-Werror=effc++]|
> error:   or 'operator=(const IntArray&)' [-Werror=effc++]|
> ```
> 可执行以下任一操作：  
> 1. 在编译设置中移除`-Weffc++`标志  
> 2. 在类中添加以下两行：  
> ```cpp
> 	IntArray(const IntArray&) = delete;
> 	IntArray& operator=(const IntArray&) = delete;
> ```
> 我们将在课程[14.14 — 拷贝构造函数简介](Chapter-14/lesson14.14-introduction-to-the-copy-constructor.md)讨论`=delete`成员

程序输出：  
```
元素5的值为：6
```

在`main()`首行实例化`IntArray`对象`ar`，传入长度10。这会调用构造函数动态分配数组内存。必须使用动态分配，因编译时无法获知数组长度（由调用者决定）。

`main()`结束时，`ar`离开作用域，触发`~IntArray()`析构函数，释放构造函数中分配的数组！

构造与析构时序  
----------------

构造函数在对象创建时调用，析构函数在对象销毁时调用。以下示例用`cout`语句展示此时序：

```cpp
#include <iostream>

class Simple
{
private:
    int m_nID{};

public:
    Simple(int nID)
        : m_nID{ nID }
    {
        std::cout << "构造Simple " << nID << '\n';
    }

    ~Simple()
    {
        std::cout << "析构Simple" << m_nID << '\n';
    }

    int getID() { return m_nID; }
};

int main()
{
    // 在栈上分配Simple对象
    Simple simple{ 1 };
    std::cout << simple.getID() << '\n';

    // 动态分配Simple对象
    Simple* pSimple{ new Simple{ 2 } };
    
    std::cout << pSimple->getID() << '\n';

    // 动态分配需手动删除
    delete pSimple;

    return 0;
} // simple在此处离开作用域
```

输出结果：  
```
构造Simple 1
1
构造Simple 2
2
析构Simple 2
析构Simple 1
```

注意"Simple 1"在"Simple 2"之后析构，因`pSimple`在函数结束前被删除，而`simple`直到`main()`结束才销毁。

全局变量（global variables）在`main()`前构造，在`main()`后析构。

RAII（资源获取即初始化）  
----------------

RAII（Resource Acquisition Is Initialization）是通过自动生命周期对象（如非动态分配对象）管理资源的编程技术。在C++中，RAII通过含构造/析构函数的类实现。资源（如内存、文件/数据库句柄）通常在构造函数中获取（也可在对象创建后获取）。对象存活期间可使用资源，析构时释放资源。RAII主要优势是防止资源泄漏（如内存未释放），因所有资源持有对象都会自动清理。

本文顶部的`IntArray`类即RAII实现范例——构造函数分配，析构函数释放。标准库中的`std::string`和`std::vector`也遵循RAII——初始化时获取动态内存，析构时自动清理。

关于std::exit()的警告  
----------------

注意：使用`std::exit()`函数会终止程序且不调用任何析构函数。若依赖析构函数执行必要清理（如退出前写入日志或数据库），需特别注意。

总结  
----------------

可见，当构造与析构函数配合使用时，类能自主完成初始化和清理，无需程序员额外操作！这降低了出错概率并使类更易使用。

[下一课 19.4 — 指向指针的指针与动态多维数组](pointers-to-pointers/)  
[返回主页](/)  
[上一课 19.2 — 动态分配数组](Chapter-19/lesson19.2-dynamically-allocating-arrays.md)