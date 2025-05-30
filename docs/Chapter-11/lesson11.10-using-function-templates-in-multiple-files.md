11.10 — 在多个文件中使用函数模板
===================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年6月11日，上午11:06（太平洋夏令时）  
2024年10月20日

以下程序无法正常运行：

main.cpp：
```cpp
#include <iostream>

template <typename T>
T addOne(T x); // 函数模板前向声明

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';
    return 0;
}
```

add.cpp：
```cpp
template <typename T>
T addOne(T x) // 函数模板定义
{
    return x + 1;
}
```

若`addOne`是非模板函数，此程序可正常运行：在*main.cpp*中，编译器会接受`addOne`的前向声明，链接器会将*main.cpp*中对`addOne()`的调用连接到*add.cpp*的函数定义。

但由于`addOne`是模板，程序无法工作并产生链接器错误：
```
1>Project6.obj : error LNK2019: 无法解析的外部符号 "int __cdecl addOne<int>(int)" (??$addOne@H@@YAHH@Z)，函数 _main 中引用了该符号
1>Project6.obj : error LNK2019: 无法解析的外部符号 "double __cdecl addOne<double>(double)" (??$addOne@N@@YANN@Z)，函数 _main 中引用了该符号
```

在*main.cpp*中，我们调用了`addOne<int>`和`addOne<double>`。然而由于编译器无法看到函数模板`addOne`的定义，它无法在*main.cpp*内部实例化这些函数。虽然编译器看到了`addOne`的前向声明，但会假设这些函数存在于其他位置并在后续链接。

当编译器编译*add.cpp*时，会看到函数模板`addOne`的定义。但*add.cpp*中未使用该模板，因此编译器不会实例化任何内容。最终结果是链接器无法将*main.cpp*中对`addOne<int>`和`addOne<double>`的调用连接到实际函数，因为这些函数从未被实例化。

> **补充说明**  
> 若*add.cpp*实例化了这些函数，程序本可通过编译并链接。但此类解决方案脆弱且应避免：若*add.cpp*的代码后续修改导致这些函数不再实例化，程序将再次链接失败。或者若*main.cpp*调用`addOne`的其他版本（如`addOne<float>`）但未在*add.cpp*实例化，同样会出现此问题。

最常规的解决方案是将所有模板代码置于头文件（.h）而非源文件（.cpp）中：

add.h：
```cpp
#ifndef ADD_H
#define ADD_H

template <typename T>
T addOne(T x) // 函数模板定义
{
    return x + 1;
}

#endif
```

main.cpp：
```cpp
#include "add.h" // 导入函数模板定义
#include <iostream>

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';
    return 0;
}
```

这样任何需要访问模板的文件都可`#include`相关头文件，预处理器会将模板定义复制到源文件中。编译器随后能实例化所需的任何函数。

您可能疑惑为何这不违反单一定义规则（ODR）。ODR允许类型、模板、内联函数和内联变量在不同文件中有相同定义。因此将模板定义复制到多个文件没有问题（只要每个定义完全相同）。

> **相关内容**  
> 我们在课程[2.7 — 前向声明与定义](forward-declarations/#ODR)中介绍了ODR。

但实例化的函数本身呢？若函数在多个文件中实例化，如何不违反ODR？答案是：从模板隐式实例化的函数是隐式内联（implicitly inline）的。如您所知，只要每个定义完全相同，内联函数可在多个文件中定义。

> **关键洞察**  
> 模板定义不受单一定义规则中"每个程序仅允许一个定义"的限制，因此将相同模板定义通过`#include`放入多个源文件没有问题。从函数模板隐式实例化的函数是隐式内联的，故可在多个文件中定义（只要每个定义完全相同）。  
>   
> 模板本身并非内联，因为内联概念仅适用于变量和函数。

以下是函数模板置于头文件（以便包含到多个源文件）的另一个示例：

max.h：
```cpp
#ifndef MAX_H
#define MAX_H

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

#endif
```

foo.cpp：
```cpp
#include "max.h" // 导入 max<T>(T, T) 的模板定义
#include <iostream>

void foo()
{
	std::cout << max(3, 2) << '\n';
}
```

main.cpp：
```cpp
#include "max.h" // 导入 max<T>(T, T) 的模板定义
#include <iostream>

void foo(); // 函数 foo 的前向声明

int main()
{
    std::cout << max(3, 5) << '\n';
    foo();
    return 0;
}
```

上例中，main.cpp 和 foo.cpp 都通过`#include "max.h"`导入模板定义，因此两个文件中的代码都能使用`max<T>(T, T)`函数模板。

> **最佳实践**  
> 在多个文件中需要的模板应在头文件中定义，并通过`#include`在需要处导入。这使得编译器能看到完整模板定义并在需要时实例化模板。

[下一课 11.x — 第11章总结与测验](Chapter-11/lesson11.x-chapter-11-summary-and-quiz.md)  
[返回主页](/)  
[上一课 11.9 — 非类型模板参数](Chapter-11/lesson11.9-non-type-template-parameters.md)