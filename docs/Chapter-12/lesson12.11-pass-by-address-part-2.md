12.11 — 传地址（下）  
==================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2022年1月18日，上午10:15（太平洋标准时间）  
2024年4月25日  

本章是[12.10 — 传地址](Chapter-12/lesson12.10-pass-by-address.md)的续篇。  

传地址实现"可选"参数  
----------------  

传地址最常见的用途之一是允许函数接受"可选（optional）"参数。通过示例更容易说明这个概念：  

```
#include <iostream>

void printIDNumber(const int *id=nullptr)
{
    if (id)
        std::cout << "您的ID号码是" << *id << "。\n";
    else
        std::cout << "您的ID号码未知。\n";
}

int main()
{
    printIDNumber(); // 此时尚不知用户ID

    int userid { 34 };
    printIDNumber(&userid); // 现在已知用户ID

    return 0;
}
```  

输出结果：  

```
您的ID号码未知。
您的ID号码是34。
```  

程序中，`printIDNumber()`函数的参数通过地址传递并默认设为`nullptr`。第一次调用时未提供参数，`id`参数保持`nullptr`，输出未知信息。第二次调用传递了`userid`地址，函数输出具体ID。  

但多数情况下，使用函数重载（function overloading）是更好的选择：  

```
#include <iostream>

void printIDNumber()
{
    std::cout << "ID未知\n";
}

void printIDNumber(int id)
{
    std::cout << "您的ID是" << id << "\n";
}

int main()
{
    printIDNumber(); // 未知ID

    int userid { 34 };
    printIDNumber(userid); // 已知ID为34

    printIDNumber(62); // 现在支持右值参数
    
    return 0;
}
```  

这种方法优势明显：无需担心空指针解引用，且支持字面量（literal）和右值（rvalue）参数。  

修改指针参数指向  
----------------  

传递地址时，地址会从实参复制到指针参数。考虑以下程序：  

```
#include <iostream>

// [[maybe_unused]]消除ptr2未使用的编译警告
void nullify([[maybe_unused]] int* ptr2) 
{
    ptr2 = nullptr; // 将参数设为空指针
}

int main()
{
    int x{ 5 };
    int* ptr{ &x }; // ptr指向x

    std::cout << "指针状态：" << (ptr ? "非空\n" : "空\n");

    nullify(ptr);

    std::cout << "指针状态：" << (ptr ? "非空\n" : "空\n");
    return 0;
}
```  

输出结果：  

```
指针状态：非空
指针状态：非空
```  

函数内修改`ptr2`的指向不影响外部`ptr`。若需修改指针实参的指向，需使用：  

通过引用传地址  
----------------  

将指针参数改为引用即可修改外部指针：  

```
#include <iostream>

void nullify(int*& refptr) // refptr现为指针的引用
{
    refptr = nullptr; // 修改参数为空指针
}

int main()
{
    int x{ 5 };
    int* ptr{ &x }; // ptr指向x

    std::cout << "指针状态：" << (ptr ? "非空\n" : "空\n");

    nullify(ptr);

    std::cout << "指针状态：" << (ptr ? "非空\n" : "空\n");
    return 0;
}
```  

输出结果：  

```
指针状态：非空
指针状态：空
```  

由于`refptr`是`ptr`的引用，对其修改直接影响原指针。  

语法提示：指针引用类型为`int*&`（注意顺序）。  

弃用0和NULL的原因（可选）  
----------------  

字面量`0`既可解释为整型也可作为空指针。预处理器宏`NULL`可能定义为`0`、`0L`或`((void*)0)`等。考虑函数重载时可能引发问题：  

```
#include <iostream>
#include <cstddef> // 包含NULL定义

void print(int x) // 接受整型
{
	std::cout << "print(int): " << x << '\n';
}

void print(int* ptr) // 接受整型指针
{
	std::cout << "print(int*): " << (ptr ? "非空\n" : "空\n");
}

int main()
{
	int x{ 5 };
	int* ptr{ &x };

	print(ptr);   // 总是调用print(int*)
	print(0);     // 总是调用print(int)
	print(NULL);  // 可能调用任意版本或报错
	print(nullptr); // 总是调用print(int*)

	return 0;
}
```  

使用`nullptr`可消除歧义，因其类型为`std::nullptr_t`（定义于\<cstddef\>），专门表示空指针。  

std::nullptr_t（可选）  
----------------  

`std::nullptr_t`类型只能保存`nullptr`值。若需函数仅接受`nullptr`参数，可使用此类型：  

```
#include <iostream>
#include <cstddef> // 包含std::nullptr_t

void print(std::nullptr_t)
{
    std::cout << "调用print(std::nullptr_t)\n";
}

void print(int*)
{
    std::cout << "调用print(int*)\n";
}

int main()
{
    print(nullptr); // 调用指针类型版本

    int x { 5 };
    int* ptr { &x };

    print(ptr); // ptr类型为int*

    ptr = nullptr;
    print(ptr); // 仍调用int*版本

    return 0;
}
```  

`print(nullptr)`优先匹配`std::nullptr_t`版本，而持有`nullptr`的`int*`类型变量仍匹配`print(int*)`。  

所有传递本质皆为传值  
----------------  

从底层来看，引用（reference）常通过指针实现，传引用本质仍是传地址。而传地址本身传递的是地址值。因此，C++所有参数传递本质上都是传值（pass by value）！传地址和引用的特性源于对地址的解引用操作能力。  

[下一课 12.12 返回引用与返回地址](Chapter-12/lesson12.12-return-by-reference-and-return-by-address.md)  
[返回主页](/)    
[上一课 12.10 传地址](Chapter-12/lesson12.10-pass-by-address.md)