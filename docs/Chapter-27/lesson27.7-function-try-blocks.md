27.7 — 函数try块（Function try blocks）  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月19日（首次发布于2017年2月6日）  

在多数情况下，try和catch块表现良好，但存在一个特定场景它们无法胜任。请看以下示例：  

```cpp
#include <iostream>

class A
{
private:
	int m_x;
public:
	A(int x) : m_x{x}
	{
		if (x <= 0)
			throw 1; // 此处抛出异常
	}
};

class B : public A
{
public:
	B(int x) : A{x} // 在B的成员初始化列表中初始化A
	{
		// 若A构造失败，如何在此处理？
	}
};

int main()
{
	try
	{
		B b{0};
	}
	catch (int)
	{
		std::cout << "Oops\n";
	}
}
```  

上述示例中，派生类B调用基类构造函数A，后者可能抛出异常。由于对象b的构造位于main函数的try块内，当A抛出异常时会被main的try块捕获。因此程序输出：  

```
Oops
```  

但若想在B内部捕获异常该如何处理？基类构造函数A的调用发生在成员初始化列表中，早于B构造函数体的执行。此时无法用常规try块包裹该调用。  

这种情况下，我们需要使用称为**函数try块（function try block）**的特殊语法。  

函数try块  
----------------  

函数try块允许为整个函数体（而非代码块）建立异常处理机制。  

其语法较特殊，以下通过示例说明：  

```cpp
#include <iostream>

class A
{
private:
	int m_x;
public:
	A(int x) : m_x{x}
	{
		if (x <= 0)
			throw 1; // 此处抛出异常
	}
};

class B : public A
{
public:
	B(int x) try : A{x} // 注意此处添加try关键字
	{
	}
	catch (...) // 注意与函数体保持相同缩进
	{
                // 成员初始化列表或构造函数体抛出的异常在此捕获

                std::cerr << "捕获到异常\n";

                throw; // 重新抛出当前异常
	}
};

int main()
{
	try
	{
		B b{0};
	}
	catch (int)
	{
		std::cout << "Oops\n";
	}
}
```  

运行此程序将输出：  

```
捕获到异常
Oops
```  

详细解析程序流程：  

1. `try`关键字置于成员初始化列表前，表示后续内容（至函数体结束）均处于try块中  
2. catch块与函数体同级缩进，覆盖从try开始到函数结束的所有异常  
3. 构造b时，B的构造函数调用A的构造函数抛出异常  
4. B构造函数的函数try块捕获异常，打印信息后重新抛出  
5. main中的catch块最终捕获处理  

> **最佳实践**  
> 当构造函数需要处理成员初始化列表抛出的异常时，使用函数try块。  

函数catch块的限制  
----------------  

常规catch块有三种处理方式：抛出新异常、重新抛出当前异常或解决异常（通过return或自然结束catch块）。  

构造函数中的函数级catch块必须抛出新异常或重新抛出——不允许解决异常！不允许return语句，catch块结束将隐式重新抛出。  

析构函数中的函数级catch块可以抛出、重新抛出或通过return解决异常。结束catch块将隐式重新抛出。  

其他函数的函数级catch块可以抛出、重新抛出或通过return解决异常。非值返回函数结束catch块将解决异常，值返回函数则导致未定义行为！  

以下表格总结函数级catch块的限制：  

| 函数类型       | 能否通过return解决异常 | catch块结束时的行为       |
|----------------|------------------------|---------------------------|
| 构造函数       | 否，必须抛出或重新抛出 | 隐式重新抛出              |
| 析构函数       | 是                     | 隐式重新抛出              |
| 非值返回函数   | 是                     | 解决异常                  |
| 值返回函数     | 是                     | 未定义行为                |  

由于不同函数类型的行为差异巨大（尤其是值返回函数的未定义行为），建议始终显式处理异常。  

> **最佳实践**  
> 避免让控制流到达函数级catch块末尾，应显式抛出、重新抛出或返回。  

在上例中，若未显式重新抛出，构造函数catch块结束时将隐式重新抛出，结果相同。  

虽然函数try块也可用于非成员函数，但实际主要用于构造函数。  

函数try块可捕获基类和当前类异常  
----------------  

函数try块既能捕获基类构造异常，也能捕获当前类异常。以下示例将异常抛出点移至B类：  

```cpp
#include <iostream>

class A
{
private:
	int m_x;
public:
	A(int x) : m_x{x}
	{
	}
};

class B : public A
{
public:
	B(int x) try : A{x}
	{
		if (x <= 0) // 从A移至B
			throw 1; 
	}
	catch (...)
	{
                std::cerr << "捕获到异常\n";
                // 若未显式抛出，将隐式重新抛出当前异常
	}
};

int main()
{
	try
	{
		B b{0};
	}
	catch (int)
	{
		std::cout << "Oops\n";
	}
}
```  

输出结果相同：  

```
捕获到异常
Oops
```  

不要用函数try块清理资源  
----------------  

对象构造失败时，析构函数不会执行。虽然可能想用函数try块清理部分分配的资源，但此时访问失败对象的成员属于未定义行为（对象在catch块执行前已"死亡"）。  

若需清理资源，应遵循构造函数失败时的标准清理规则（参见课程[27.5 — 异常、类与继承](Chapter-27/lesson27.5-exceptions-classes-and-inheritance.md)中的"构造函数失败时"小节）。  

函数try块主要用于在传递异常前记录日志，或修改异常类型。  

[下一课 27.8 — 异常的风险与缺点](Chapter-27/lesson27.8-exception-dangers-and-downsides.md)  
[返回主页](/)    
[上一课 27.6 — 重新抛出异常](Chapter-27/lesson27.6-rethrowing-exceptions.md)