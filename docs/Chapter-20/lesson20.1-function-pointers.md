20.1 — 函数指针（Function Pointers）  
=========================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月14日（首次发布于2007年8月8日）  

在课程[12.7 — 指针简介](Chapter-12/lesson12.7-introduction-to-pointers.md)中，我们学习了指针是存储变量地址的变量。函数指针（function pointer）类似，但其指向的是函数而非变量！  

考虑以下函数：  
```
int foo()
{
    return 5;
}
```  
标识符`foo()`是函数名。但函数的类型是什么？函数拥有自己的函数类型（function type）——本例中即返回整数且无参数的函数类型。如同变量，函数在内存中有固定地址（因此是左值）。  

调用函数时（通过`operator()`），执行流程会跳转到被调用函数的地址：  
```
int foo() // foo的代码起始于内存地址0x002717f0
{
    return 5;
}

int main()
{
    foo(); // 跳转到地址0x002717f0
    return 0;
}
```  

编程过程中可能会出现这样的常见错误：  
```
#include <iostream>

int foo() // 代码起始于内存地址0x002717f0
{
    return 5;
}

int main()
{
    std::cout << foo << '\n'; // 本意是调用foo()，却直接打印了函数本身！
    return 0;
}
```  
此时未调用函数`foo()`而是直接将函数`foo`传递给`std::cout`。当函数被名称引用（不带括号）时，C++会将其转换为函数指针。由于`operator<<`无法打印函数指针，标准规定此时函数指针应转换为布尔值（bool）打印。由于`foo`的函数指针非空，将始终输出布尔值`true`，因此打印：  
```
1
```  

> **提示**  
> 部分编译器（如Visual Studio）会打印函数地址：  
> ```
> 0x002717f0
> ```  
> 若需强制打印地址，可将其转换为void指针：  
> ```
> std::cout << reinterpret_cast<void*>(foo) << '\n'; // 实现定义行为
> ```  

函数指针声明  
----------------  
声明非常量函数指针的语法较为复杂：  
```
// fcnPtr是指向无参数返回整数的函数的指针
int (*fcnPtr)();
```  
`*fcnPtr`的括号是必须的，否则`int* fcnPtr()`会被解析为返回整型指针的函数声明。常量函数指针的声明：  
```
int (*const fcnPtr)();
```  

函数指针赋值  
----------------  
函数指针可用函数初始化（非常量指针可重新赋值）：  
```
int main()
{
    int (*fcnPtr)(){ &foo }; // 指向foo
    fcnPtr = &goo; // 改为指向goo
    return 0;
}
```  
常见错误`fcnPtr = goo();`会导致将返回值赋值给指针。函数指针类型必须与函数完全匹配。  

函数指针调用  
----------------  
两种调用方式：显式解引用和隐式解引用。建议调用前检查指针是否为空：  
```
if (fcnPtr) // 确保非空
    fcnPtr(5); // 隐式解引用调用
```  

默认参数与函数指针  
----------------  
通过函数指针调用时，默认参数不生效（因解析发生在运行时）：  
```
void print(int x, int y = 10); 

static_cast<void(*)(int)>(print)(1); // 必须显式指定参数版本
```  

回调函数（Callback Functions）  
----------------  
函数指针常用于将函数作为参数传递。以选择排序（selection sort）为例，允许调用者自定义比较逻辑：  
```
void selectionSort(int* array, int size, bool (*comparisonFcn)(int, int))
{
    if (comparisonFcn(array[bestIndex], array[currentIndex]))
        // 执行比较...
}
```  
调用示例：  
```
selectionSort(array, 9, descending); // 降序排序
selectionSort(array, 9, evensFirst); // 自定义偶数优先排序
```  

类型别名与std::function  
----------------  
使用类型别名（type alias）简化函数指针声明：  
```
using ValidateFunction = bool(*)(int, int);
```  
C++11引入的`std::function`（需包含<functional>头文件）提供更灵活的封装：  
```
std::function<int()> fcnPtr{ &foo }; // 声明函数指针
fcnPtr(); // 调用函数
```  

自动类型推断  
----------------  
`auto`关键字可推断函数指针类型：  
```
auto fcnPtr{ &foo }; // 自动推断为函数指针类型
```  

总结  
----------------  
函数指针主要用于存储函数或传递函数参数。推荐使用`std::function`增强可读性和安全性。  

测验  
----------------  
1a-1e：实现基础计算器程序，使用函数指针处理四则运算。完整代码参见原文。  

[下一课 20.2 — 栈与堆](Chapter-20/lesson20.2-the-stack-and-the-heap.md)  
[返回主页](/)  
[上一课 19.5 — void指针](void-pointers/)