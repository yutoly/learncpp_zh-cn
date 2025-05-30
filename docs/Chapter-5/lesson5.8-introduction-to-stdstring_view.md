5.8 — std::string\_view 简介  
========================================

[*作者：nascardriver*](https://www.learncpp.com/author/nascardriver/ "查看 nascardriver 的所有文章")  
2019年11月2日 上午7:17（太平洋时区）  
2024年11月26日修订  

观察以下程序：  
```cpp
#include <iostream>

int main()
{
    int x { 5 }; // x复制其初始化器的值
    std::cout << x << '\n';

    return 0;
}
```  
当执行`x`的定义时，初始化值`5`被复制到为整型变量`x`分配的内存中。对于基本类型，初始化和复制变量是高效的。  

再观察类似程序：  
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string s{ "Hello, world!" }; // s复制其初始化器的值
    std::cout << s << '\n';

    return 0;
}
```  
当初始化`s`时，C风格字符串字面量`"Hello, world!"`被复制到为`std::string s`分配的内存中。与基本类型不同，`std::string`的初始化和复制是低效的。  

在上例中，我们仅将`s`的值打印到控制台后即销毁。本质上我们为打印操作创建了"Hello, world!"的副本后又立即销毁，这种操作效率低下。  

类似情况也出现在下例：  
```cpp
#include <iostream>
#include <string>

void printString(std::string str) // str复制其初始化器的值
{
    std::cout << str << '\n';
}

int main()
{
    std::string s{ "Hello, world!" }; // s复制其初始化器的值
    printString(s);

    return 0;
}
```  
本例创建了两次"C风格字符串"Hello, world!"的副本：第一次在`main()`中初始化`s`时，第二次在`printString()`中初始化参数`str`时。这种仅为打印字符串而进行的多次复制显然效率低下。  

std::string\_view（C++17引入）  
----------------  
为解决`std::string`初始化（或复制）开销大的问题，C++17在\<string_view\>头文件中引入了`std::string_view`。该类型提供对*现有*字符串（C风格字符串、`std::string`或其他`std::string_view`）的**只读**访问，无需进行复制操作。  

将前例中的`std::string`替换为`std::string_view`：  
```cpp
#include <iostream>
#include <string_view> // C++17

// str提供对传入参数的只读访问
void printSV(std::string_view str) // 现在改为std::string_view
{
    std::cout << str << '\n';
}

int main()
{
    std::string_view s{ "Hello, world!" }; // 现在改为std::string_view
    printSV(s);

    return 0;
}
```  
该程序输出结果与前例相同，但全程未创建"Hello, world!"的副本。当用C风格字符串字面量初始化`std::string_view s`时，`s`无需复制即可提供对"Hello, world!"的只读访问。将`s`传递给`printSV()`时，参数`str`通过`s`初始化，同样无需复制。  

> **最佳实践**  
> 当需要只读字符串时，优先选用`std::string_view`而非`std::string`，尤其在函数参数中。  

std::string\_view 的灵活初始化  
----------------  
`std::string_view`支持多种字符串类型初始化：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view s1 { "Hello, world!" }; // 使用C风格字符串字面量初始化
    std::cout << s1 << '\n';

    std::string s{ "Hello, world!" };
    std::string_view s2 { s };  // 使用std::string初始化
    std::cout << s2 << '\n';

    std::string_view s3 { s2 }; // 使用std::string_view初始化
    std::cout << s3 << '\n';
       
    return 0;
}
```  

std::string\_view 参数的广泛接受性  
----------------  
C风格字符串和`std::string`均可隐式转换为`std::string_view`。因此`std::string_view`参数可接受以下类型参数：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view str)
{
    std::cout << str << '\n';
}

int main()
{
    printSV("Hello, world!"); // 传入C风格字符串字面量

    std::string s2{ "Hello, world!" };
    printSV(s2); // 传入std::string

    std::string_view s3 { s2 };
    printSV(s3); // 传入std::string_view
       
    return 0;
}
```  

std::string\_view 到 std::string 的转换限制  
----------------  
由于`std::string`会复制其初始化器（开销大），C++不允许`std::string_view`隐式转换为`std::string`，以防止意外传递`std::string_view`参数给`std::string`参数导致不必要的复制。  

如需转换，可通过两种方式实现：  
1. 显式构造`std::string`对象  
2. 使用`static_cast`转换  

示例：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

void printString(std::string str)
{
	std::cout << str << '\n';
}

int main()
{
	std::string_view sv{ "Hello, world!" };

	// printString(sv);   // 编译错误：拒绝隐式转换
	std::string s{ sv }; // 合法：显式构造std::string
	printString(s);      // 传入std::string对象

	printString(static_cast<std::string>(sv)); // 合法：显式类型转换

	return 0;
}
```  

赋值改变查看目标  
----------------  
对`std::string_view`赋新值会使其指向新字符串，但不会修改原有字符串：  
```cpp
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string name { "Alex" };
    std::string_view sv { name }; // sv当前查看name
    std::cout << sv << '\n'; // 输出Alex

    sv = "John"; // sv现在查看"John"（不修改name）
    std::cout << sv << '\n'; // 输出John

    std::cout << name << '\n'; // 输出Alex

    return 0;
}
```  

std::string\_view 字面量  
----------------  
双引号字符串字面量默认是C风格字符串。使用`sv`后缀可创建`std::string_view`字面量（必须小写）：  
```cpp
#include <iostream>
#include <string>      // 提供std::string
#include <string_view> // 提供std::string_view

int main()
{
    using namespace std::string_literals;      // 启用s后缀
    using namespace std::string_view_literals; // 启用sv后缀

    std::cout << "foo\n";   // 无后缀：C风格字符串字面量
    std::cout << "goo\n"s;  // s后缀：std::string字面量
    std::cout << "moo\n"sv; // sv后缀：std::string_view字面量

    return 0;
}
```  

> **相关内容**  
> 关于`using namespace`的讨论详见课程[5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)，相关建议同样适用。  

constexpr 支持  
----------------  
与`std::string`不同，`std::string_view`全面支持constexpr：  
```cpp
#include <iostream>
#include <string_view>

int main()
{
    constexpr std::string_view s{ "Hello, world!" }; // s是字符串符号常量
    std::cout << s << '\n'; // 编译时s将被替换为"Hello, world!"

    return 0;
}
```  
这使得`constexpr std::string_view`成为需要字符串符号常量时的首选。  

[下一课 5.9 — std::string_view（下）](Chapter-5/lesson5.9-stdstring_view-part-2.md)  
[返回主页](/)  
[上一课 5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)