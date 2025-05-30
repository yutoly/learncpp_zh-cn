7.13 — using声明与using指令  
===============================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年11月9日，太平洋标准时间下午6:23  
2025年3月5日  

 

您可能在许多教科书和教程中见过这样的程序：  

```cpp
#include <iostream>

using namespace std;

int main()
{
    cout << "Hello world!\n";

    return 0;
}
```  

如果看到这样的代码，请立即远离。您的教材或教程可能已过时。本章将深入探讨原因。  

> **小贴士**  
> 某些IDE会自动生成类似结构的C++新项目（以便您能立即编译，而非从空白文件开始）。  

历史背景  
----------------  

在C++支持命名空间之前，现在位于`std`命名空间的所有名称都处于全局命名空间。这导致程序标识符与标准库标识符发生命名冲突。某些在旧版C++下运行的程序可能与新版C++产生冲突。  

1995年命名空间标准化后，标准库所有功能从全局命名空间移至`std`命名空间。这一变更导致仍使用非限定名的旧代码无法运行。  

对于大型代码库而言，任何修改（无论多微小）都可能破坏程序。将所有迁移至`std`命名空间的名称添加`std::`前缀风险极高，因此需要解决方案。  

回到现代视角——若频繁使用标准库，反复键入`std::`可能显得冗余，某些情况下会影响代码可读性。C++通过using语句为这两个问题提供了解决方案。  

但首先需明确两个术语。  

限定名与非限定名  
----------------  

名称可分为限定名（qualified name）与非限定名（unqualified name）。  

**限定名**包含作用域标识，通常通过作用域解析运算符（::）指定命名空间。例如：  

```cpp
std::cout // cout标识符通过std命名空间限定
::foo     // foo标识符通过全局命名空间限定
```  

> **进阶阅读**  
> 名称也可通过类名（使用::运算符）或类对象（使用.或->成员选择运算符）限定。例如：  
> ```cpp
> class C; // 某类
> 
> C::s_member; // s_member通过C类限定
> obj.x;       // x通过obj类对象限定
> ptr->y;      // y通过类对象指针ptr限定
> ```  

**非限定名**不包含作用域限定符。例如`cout`和`x`均属非限定名。  

using声明  
----------------  

减少`std::`重复输入的方法之一是使用using声明语句。**using声明（using-declaration）**允许将非限定名作为限定名的别名。  

以下基础Hello world程序在第5行使用using声明：  

```cpp
#include <iostream>

int main()
{
   using std::cout; // 该声明告知编译器cout应解析为std::cout
   cout << "Hello world!\n"; // 此处无需std::前缀！

   return 0;
} // using声明在当前作用域结束时失效
```  

`using std::cout;`声明告诉编译器我们将使用`std`命名空间中的`cout`对象。因此当编译器遇到`cout`时，会默认指代`std::cout`。若`main()`中同时存在其他`cout`定义，优先使用`std::cout`。因此在第6行可直接使用`cout`而非`std::cout`。  

此例节省的代码量有限，但若在函数内多次使用`cout`，using声明能显著提升可读性。注意每个名称需单独声明（如`std::cout`、`std::cin`等）。  

using声明从声明位置起生效，至当前作用域结束为止。  

尽管using声明不如`std::`前缀明确，但通常认为在源文件（.cpp）中使用是安全且可接受的（下文将讨论例外情况）。  

using指令  
----------------  

另一种简化方法是使用using指令。**using指令（using-directive）**允许在指令作用域内无限定地访问命名空间中的所有标识符。  

> **进阶阅读**  
> 由于技术原因，using指令实际上不会在当前作用域引入新名称含义，而是将名称引入外层作用域（具体细节参见[此处](https://quuxplusone.github.io/blog/2020/12/21/using-directive/)）。  

以下是使用第5行using指令的Hello world程序：  

```cpp
#include <iostream>

int main()
{
   using namespace std; // 现在可无限定访问std命名空间所有名称
   cout << "Hello world!\n"; // 无需std::前缀

   return 0;
} // using指令在当前作用域结束时失效
```  

`using namespace std;`指令使`std`命名空间所有名称在当前作用域（此处为`main`函数）内可无限定访问。当使用非限定标识符`cout`时，将解析为`std::cout`。  

using指令是为旧版无命名空间代码库提供的解决方案。无需手动更新所有非限定名为限定名（存在风险），只需在每个文件顶部添加using指令（`using namespace std;`），即可继续使用迁移至`std`命名空间的非限定名。  

using指令的问题（即为何应避免"using namespace std;"）  
----------------  

现代C++中，using指令的收益（节省输入）远小于风险，原因如下：  

1. using指令允许无限定访问命名空间*所有*名称（可能包含大量无用名称）  
2. using指令不会优先选择指令指定命名空间的名称  

最终结果显著增加命名冲突可能性（尤其在使用`std`命名空间时）。  

首先看说明性示例：  

```cpp
#include <iostream>

namespace A
{
	int x { 10 };
}

namespace B
{
	int x{ 20 };
}

int main()
{
	using namespace A;
	using namespace B;

	std::cout << x << '\n'; // 编译错误：x指代A::x还是B::x？

	return 0;
}
```  

此例中编译器无法判断`main`中的`x`指代`A::x`还是`B::x`，将产生"ambiguous symbol"错误。可通过移除using指令、改用using声明或限定`x`（`A::x`/`B::x`）解决。  

另一更微妙示例：  

```cpp
#include <iostream> // 导入std::cout声明

int cout() // 声明自定义cout函数
{
    return 5;
}

int main()
{
    using namespace std; // 使std::cout可简写为cout
    cout << "Hello, world!\n"; // 歧义：使用std::cout还是自定义cout？

    return 0;
}
```  

此例编译器无法确定非限定`cout`指代`std::cout`还是自定义函数，同样产生"ambiguous symbol"错误。若使用`std::cout`前缀：  

```cpp
    std::cout << "Hello, world!\n"; // 明确指定std::cout
```  

或改用using声明：  

```cpp
    using std::cout; // 声明cout指代std::cout
    cout << "Hello, world!\n"; // 即std::cout
```  

程序则无此问题。虽然您可能不会编写名为"cout"的函数，但`std`命名空间存在数百个可能冲突的名称。  

即使当前using指令未引发冲突，也会增加未来冲突风险。例如若代码包含某库的using指令，当该库更新时，新增名称可能与现有代码冲突。  

示例程序：  

第三方库FooLib.h：  

```cpp
#ifndef FOOLIB
#define FOOLIB

namespace Foo
{
    int a { 20 };
}

#endif
```  

main.cpp：  

```cpp
#include <iostream>
#include <FooLib.h> // 第三方库，使用尖括号包含

void print()
{
    std::cout << "Hello\n";
}

int main()
{
    using namespace Foo; // 懒人写法，避免Foo::前缀

    std::cout << a << '\n'; // 使用Foo::a
    print(); // 调用::print()

    return 0;
}
```  

更新FooLib.h后：  

```cpp
#ifndef FOOLIB
#define FOOLIB

namespace Foo
{
    int a { 20 };
    void print() { std::cout << "Timmah!"; } // 新增函数
}
#endif
```  

此时`main.cpp`未修改却无法编译，因为using指令使`Foo::print()`可简写为`print()`，导致与`::print()`冲突。  

更隐蔽的情况是新增函数可能成为函数调用的更优匹配。例如：  

更新前Foolib.h：  

```cpp
namespace Foo
{
    int a { 20 };
}
```  

main.cpp：  

```cpp
#include <iostream>
#include <Foolib.h>

int get(long)
{
    return 1;
}

int main()
{
    using namespace Foo;
    std::cout << a << '\n'; // Foo::a

    std::cout << get(0) << '\n'; // 调用::get(long)

    return 0;
}
```  

程序输出`1`。更新Foolib.h后：  

```cpp
namespace Foo
{
    int a { 20 };
    int get(int) { return 2; } // 新增函数
}
```  

此时程序输出变为`2`！因为字面量`0`是整型，编译器优先匹配`get(int)`而非需要转换的`get(long)`。  

若使用using声明或显式作用域限定符可避免此问题。  

最后，缺乏显式作用域前缀会降低代码可读性。例如：  

```cpp
using namespace NS;

int main()
{
    foo(); // 用户定义函数还是NS库函数？
}
```  

难以判断`foo()`的来源。现代IDE可通过悬停显示，但逐个检查非常繁琐。  

不使用using指令时更清晰：  

```cpp
int main()
{
    NS::foo(); // 明确调用库函数
    foo();     // 可能是用户定义函数
}
```  

using语句的作用域  
----------------  

若在代码块内使用using声明或指令，名称仅在该块内有效（遵循常规块作用域规则）。此举降低命名冲突风险。  

若在命名空间（含全局命名空间）中使用，名称在文件剩余部分有效（具有文件作用域）。  

禁止在头文件或#include指令前使用using语句  
----------------  

基本原则是：using语句不应影响其他文件的代码，也不应受其他文件代码影响。  

具体而言：  
- 禁止在头文件中使用using语句  
- 禁止在#include指令前使用using语句  

例如，在头文件全局命名空间使用using语句，所有包含该头文件的文件都会继承该语句，显然有害。头文件内的命名空间同理。  

函数内使用using语句是否安全？因其作用域限于函数内部。答案仍是否定的，原因与#include指令前使用using语句相同。  

using语句的行为依赖已引入的标识符，具有顺序敏感性。示例：  

FooInt.h：  

```cpp
namespace Foo
{
    void print(int)
    {
        std::cout << "print(int)\n";
    }
}
```  

FooDouble.h：  

```cpp
namespace Foo
{
    void print(double)
    {
        std::cout << "print(double)\n";
    }
}
```  

main.cpp（正常）：  

```cpp
#include <iostream>
#include "FooDouble.h"
#include "FooInt.h"

using Foo::print; // print指代Foo::print

int main()
{
    print(5);  // 调用Foo::print(int)
}
```  

输出`print(int)`。调整main.cpp顺序：  

```cpp
#include <iostream>
#include "FooDouble.h"

using Foo::print; // 在#include指令前使用
#include "FooInt.h"

int main()
{
    print(5);  // 调用Foo::print(double)
}
```  

输出变为`print(double)`！因此必须避免在头文件函数内使用using语句。  

唯一安全使用using语句的位置是源文件（.cpp）中所有#include指令之后。  

> **进阶阅读**  
> 本例使用"函数重载"概念（详见[11.1 — 函数重载简介](Chapter-11/lesson11.1-introduction-to-function-overloading.md)）。关键点：同一作用域中，参数不同的函数可同名。`int`与`double`类型不同，因此`Foo::print(int)`和`Foo::print(double)`可共存。  
>  
> 正常版本中，编译器遇到`using Foo::print`时已见过两个函数，因此均可调用。`Foo::print(int)`是更优匹配。  
>  
> 错误版本中，编译器遇到using声明时仅见过`Foo::print(double)`，因此`print(5)`只能调用该版本。  

撤销或替换using语句  
----------------  

声明using语句后，无法在作用域内撤销或替换：  

```cpp
int main()
{
    using namespace Foo;

    // 无法在此撤销"using namespace Foo"！
    // 也无法替换为其他using语句

    return 0;
}
```  

最佳方案是利用块作用域限制using语句范围：  

```cpp
int main()
{
    {
        using namespace Foo;
        // 此处调用Foo成员
    } // using指令失效
 
    {
        using namespace Goo;
        // 此处调用Goo成员
    } // using指令失效

    return 0;
}
```  

当然，最根本的解决方案是始终使用显式作用域解析运算符（::）。  

using语句最佳实践  
----------------  

> **最佳实践**  
> 优先使用显式命名空间限定而非using语句。  
>  
> 完全避免using指令（除`using namespace std::literals`访问`s`和`sv`字面后缀）。在.cpp文件的#include指令后可使用using声明。禁止在头文件中使用using语句（尤其在全局命名空间）。  

相关主题  
----------------  

`using`关键字也用于定义类型别名（与using语句无关），详见[10.7 — 类型别名与typedef](Chapter-10/lesson10.7-typedefs-and-type-aliases.md)。  

[下一课 7.14 — 匿名与内联命名空间](Chapter-7/lesson7.14-unnamed-and-inline-namespaces.md)  
[返回主页](/)  
[上一课 7.12 — 作用域、持续期与链接性总结](Chapter-7/lesson7.12-scope-duration-and-linkage-summary.md)  