12.10 — 按地址传递（Pass by address）  
========================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月13日（首次发布于2007年7月25日）  

在前面的课程中，我们介绍了两种向函数传递参数的方法：按值传递（pass by value）（[2.4 — 函数形参与实参简介](Chapter-2/lesson2.4-introduction-to-function-parameters-and-arguments.md)）和按引用传递（pass by reference）（[12.5 — 按左值引用传递](Chapter-12/lesson12.5-pass-by-lvalue-reference.md)）。以下示例程序展示了`std::string`对象按值传递与按引用传递的区别：  
```
#include <iostream>
#include <string>

void printByValue(std::string val) // 形参是str的副本
{
    std::cout << val << '\n'; // 通过副本打印值
}

void printByReference(const std::string& ref) // 形参是绑定到str的引用
{
    std::cout << ref << '\n'; // 通过引用打印值
}

int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // 按值传递str，创建副本
    printByReference(str); // 按引用传递str，不创建副本

    return 0;
}
```  
当按值传递实参`str`时，函数形参`val`接收实参的副本。由于形参是实参的副本，对`val`的任何修改都作用于副本而非原实参。  

当按引用传递实参`str`时，引用形参`ref`绑定到实际实参，避免创建副本。由于引用形参是const类型，我们不能修改`ref`。但如果`ref`是非const类型，对`ref`的修改会改变`str`。  

在这两种情况下，调用者都提供实际对象（`str`）作为函数调用的实参。  

按地址传递（Pass by address）  
C++提供了第三种参数传递方式——**按地址传递（pass by address）**。使用这种方式时，调用者不直接传递对象，而是传递对象的*地址*（通过指针）。该指针（持有对象地址）会被复制到被调函数的指针形参中（此时形参也持有对象地址）。函数随后可通过解引用指针访问目标对象。  

以下是添加了按地址传递版本的改进程序：  
```
#include <iostream>
#include <string>

void printByValue(std::string val) // 形参是str的副本
{
    std::cout << val << '\n'; // 通过副本打印值
}

void printByReference(const std::string& ref) // 形参是绑定到str的引用
{
    std::cout << ref << '\n'; // 通过引用打印值
}

void printByAddress(const std::string* ptr) // 形参是持有str地址的指针
{
    std::cout << *ptr << '\n'; // 通过解引用指针打印值
}

int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // 按值传递str，创建副本
    printByReference(str); // 按引用传递str，不创建副本
    printByAddress(&str); // 按地址传递str，不创建副本

    return 0;
}
```  
注意这三个版本的相似性。让我们深入分析按地址传递版本：  

首先，由于我们希望`printByAddress()`使用按地址传递，因此将形参声明为名为`ptr`的指针。因为`printByAddress()`以只读方式使用`ptr`，所以这是一个指向const值的指针：  
```
void printByAddress(const std::string* ptr)
{
    std::cout << *ptr << '\n'; // 通过解引用指针打印值
}
```  
在`printByAddress()`函数内部，我们对指针形参`ptr`解引用以访问目标对象的值。  

其次，调用函数时不能直接传递`str`对象，必须传递`str`的地址。最简单的方法是使用取址运算符（&）获取持有`str`地址的指针：  
```
printByAddress(&str); // 使用取址运算符(&)获取str地址的指针
```  
执行此调用时，`&str`将创建持有`str`地址的指针。该地址随后作为函数调用的一部分被复制到形参`ptr`中。由于`ptr`现在持有`str`的地址，当函数解引用`ptr`时，将获得`str`的值并打印到控制台。  

如果已存在持有`str`地址的指针变量，也可以直接使用该指针：  
```
int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); 
    printByReference(str); 
    printByAddress(&str); 

    std::string* ptr { &str }; // 定义持有str地址的指针变量
    printByAddress(ptr); // 按地址传递str，不创建副本    

    return 0;
}
```  

术语说明  
使用`operator&`传递变量地址作为实参时，我们称该变量按地址传递。  
当指针变量持有对象地址，并将该指针作为实参传递给同类型形参时，我们称对象按地址传递，而指针按值传递。  

按地址传递不创建对象副本  
考虑以下语句：  
```
std::string str{ "Hello, world!" };
printByAddress(&str); // 使用取址运算符(&)获取str地址的指针
```  
如[12.5 — 按左值引用传递](Chapter-12/lesson12.5-pass-by-lvalue-reference.md)所述，复制`std::string`开销较大，应当避免。按地址传递`std::string`时，不会复制实际对象，仅将指针（持有对象地址）从调用者复制到被调函数。由于地址通常为4或8字节，复制指针总是高效的。  

因此，与按引用传递类似，按地址传递高效且避免创建实参对象的副本。  

按地址传递允许函数修改实参值  
按地址传递对象时，函数接收实参对象的地址（可通过解引用访问）。由于这是实际实参对象的地址（而非副本），若形参为非const指针，函数可通过指针形参修改实参：  
```
#include <iostream>

void changeValue(int* ptr) // 注意：本例中ptr是非const指针
{
    *ptr = 6; // 修改值为6
}

int main()
{
    int x{ 5 };

    std::cout << "x = " << x << '\n';

    changeValue(&x); // 将x的地址传递给函数

    std::cout << "x = " << x << '\n';

    return 0;
}
```  
输出：  
```
x = 5
x = 6
```  
可见实参被修改，且该修改在`changeValue()`执行结束后仍然有效。  

若函数不应修改传入对象，形参应声明为指向const的指针：  
```
void changeValue(const int* ptr) // 注意：ptr现在是指向const的指针
{
    *ptr = 6; // 错误：不能修改const值
}
```  

基于与常规（非指针、非引用）形参不常使用`const`相同的原因（参见[5.1 — 常量变量](Chapter-5/lesson5.1-constant-variables-named-constants.md)），我们通常也不对指针形参使用`const`。需明确两点：  
* 使用`const`声明指针形参为常量指针（const pointer）价值有限（因其不影响调用者，主要作为指针不会改变的文档说明）  
* 使用`const`区分指向const的指针（pointer-to-const）与可修改实参的非const指针（pointer-to-non-const）意义重大（调用者需知函数是否可能修改实参值）  

最佳实践  
优先使用指向const的指针形参，除非函数需要修改传入对象。  
除非有特殊原因，否则不要将函数形参声明为常量指针（const pointer）。  

空指针检查（Null checking）  
考虑以下看似无害的程序：  
```
#include <iostream>

void print(int* ptr)
{
	std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	print(&x);

	int* myPtr {};
	print(myPtr);

	return 0;
}
```  
运行时将打印`5`后崩溃。在`print(myPtr)`调用中，`myPtr`是空指针（null pointer），形参`ptr`也将是空指针。解引用空指针会导致未定义行为（undefined behavior）。  

按地址传递参数时，应在解引用前检查指针是否为空。方法之一是使用条件语句：  
```
#include <iostream>

void print(int* ptr)
{
    if (ptr) // 若ptr非空
    {
        std::cout << *ptr << '\n';
    }
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
```  
虽然适用于简单函数，但在复杂函数中可能导致冗余逻辑（多次检查指针是否为空）或主逻辑嵌套。  

更有效的方法是将空指针检查作为前置条件（[9.6 — 断言与静态断言](Chapter-9/lesson9.6-assert-and-static_assert.md)）并立即处理异常情况：  
```
#include <iostream>

void print(int* ptr)
{
    if (!ptr) // 若ptr为空指针，立即返回
        return;

    // 执行至此可假定ptr有效
    // 无需额外检查或嵌套

    std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
```  
若不应传递空指针，可使用`assert`（参见[9.6 — 断言与静态断言](Chapter-9/lesson9.6-assert-and-static_assert.md)）来记录不应发生的情况：  
```
#include <iostream>
#include <cassert>

void print(const int* ptr) // 现在是指向const int的指针
{
	assert(ptr); // 调试模式下若传递空指针则终止程序

	// （可选）生产模式中处理为错误情况以避免崩溃
	if (!ptr)
		return;

	std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
```  

优先使用按（const）引用传递  
注意上例中的`print()`函数对空值的处理并不理想——实际上只是中止函数。既然如此，为何允许用户传入空值？按引用传递具有按地址传递的所有优点，且没有意外解引用空指针的风险。  

按const引用传递相比按地址传递还有以下优势：  
1. 按地址传递要求对象必须具有地址，因此只能传递左值（lvalue）（因右值（rvalue）无地址）。按const引用传递更灵活，可接受左值和右值：  
```
#include <iostream>

void printByValue(int val) // 形参是实参的副本
{
    std::cout << val << '\n'; 
}

void printByReference(const int& ref) // 形参是绑定到实参的引用
{
    std::cout << ref << '\n'; 
}

void printByAddress(const int* ptr) // 形参是持有实参地址的指针
{
    std::cout << *ptr << '\n'; 
}

int main()
{
    printByValue(5);     // 有效（但创建副本）
    printByReference(5); // 有效（因形参是const引用）
    printByAddress(&5);  // 错误：无法获取右值地址

    return 0;
}
```  
2. 按引用传递语法更自然，可直接传递字面量或对象。按地址传递会使代码充斥&和*符号。  

在现代C++中，多数按地址传递的场景可通过其他方法更好实现。遵循通用准则："尽可能按引用传递，必要时才按地址传递"。  

最佳实践  
除非有特殊需求，否则优先使用按引用传递而非按地址传递。  

[下一课 12.11 按地址传递（下）](Chapter-12/lesson12.11-pass-by-address-part-2.md)  
[返回主页](/)  
[  
[上一课 12.9 指针与const](Chapter-12/lesson12.9-pointers-and-const.md)