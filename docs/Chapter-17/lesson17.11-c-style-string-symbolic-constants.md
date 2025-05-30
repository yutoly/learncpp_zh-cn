17.11 — C风格字符串符号常量  
===========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2015年8月15日，下午4:46 PDT  
2023年10月25日  

 

在前一课程（[17.10 — C风格字符串](Chapter-17/lesson17.10-c-style-strings.md)）中，我们讨论了如何创建和初始化C风格字符串对象：

```cpp
#include <iostream>

int main()
{
    char name[]{ "Alex" }; // C风格字符串
    std::cout << name << '\n';

    return 0;
}
```

C++支持两种不同的方式创建C风格字符串符号常量：

```cpp
#include <iostream>

int main()
{
    const char name[] { "Alex" };        // 情况1：用C风格字符串字面量初始化的const数组
    const char* const color{ "Orange" }; // 情况2：指向C风格字符串字面量的const指针

    std::cout << name << ' ' << color << '\n';

    return 0;
}
```

输出结果为：

```
Alex Orange
```

虽然上述两种方法产生相同结果，但C++处理内存分配的方式略有不同。


**情况1**中，"Alex"被存入（可能是只读的）内存某处。随后程序为长度5的C风格数组分配内存（4个显式字符加空终止符），并用字符串"Alex"初始化该内存。因此我们最终得到两个"Alex"副本——一个在全局内存中，另一个由`name`持有。由于`name`是const（且永远不会被修改），这种复制是低效的。


**情况2**中，编译器处理方式由实现定义。通常情况是编译器将"Orange"放入只读内存，然后用该字符串地址初始化指针。


出于优化目的，多个字符串字面量可能合并为单个值。例如：

```cpp
const char* name1{ "Alex" };
const char* name2{ "Alex" };
```

这是两个具有相同值的不同字符串字面量。由于这些字面量是常量，编译器可能选择将它们合并为共享字符串字面量以节省内存，使`name1`和`name2`指向相同地址。


**const C风格字符串的类型推导**  

使用C风格字符串字面量进行类型推导较为直接：

```cpp
    auto s1{ "Alex" };  // 类型推导为 const char*
    auto* s2{ "Alex" }; // 类型推导为 const char*
    auto& s3{ "Alex" }; // 类型推导为 const char(&)[5]
```


**输出指针与C风格字符串**  

您可能注意到`std::cout`处理不同类型指针的特别之处。考虑以下示例：

```cpp
#include <iostream>

int main()
{
    int narr[]{ 9, 7, 5, 3, 1 };
    char carr[]{ "Hello!" };
    const char* ptr{ "Alex" };

    std::cout << narr << '\n'; // narr将退化为int*
    std::cout << carr << '\n'; // carr将退化为char*
    std::cout << ptr << '\n';  // name本身已是char*

    return 0;
}
```

在作者机器上输出：

```
003AF738
Hello!
Alex
```

为何int数组打印地址，而字符数组打印为字符串？


答案是输出流（如`std::cout`）对用户意图进行了假设。若传递非字符指针，它将直接打印指针内容（指针持有的地址）。但若传递`char*`或`const char*`类型对象，则假定用户希望打印字符串。因此，不会打印指针值（地址），而是打印被指向的字符串！


虽然多数情况下符合预期，但可能导致意外结果。考虑以下情况：

```cpp
#include <iostream>

int main()
{
    char c{ 'Q' };
    std::cout << &c;

    return 0;
}
```

本例中程序员意图打印变量`c`的地址。然而`&c`类型为`char*`，因此`std::cout`尝试将其作为字符串打印！由于`c`未空终止，导致未定义行为。


在作者机器上输出：

```
Q╠╠╠╠╜╡4;¿■A
```

原因在于：首先将`&c`（类型为`char*`）视为C风格字符串打印'Q'，然后继续读取内存中的垃圾数据，直到遇到`0`值（解释为空终止符）才停止。实际结果取决于变量`c`之后的内存内容。


虽然实际场景中较少需要打印字符地址，但此例揭示了底层机制，以及程序如何意外失控。


若确实需要打印字符指针地址，可将其静态转型为`const void*`：

```cpp
#include <iostream>

int main()
{
    const char* ptr{ "Alex" };

    std::cout << ptr << '\n';                           // 作为C风格字符串打印
    std::cout << static_cast<const void*>(ptr) << '\n'; // 打印ptr持有的地址
    
    return 0;
}
```


**相关内容**  

关于`void*`的讨论见课程[19.5 — void指针](void-pointers/)。此处使用无需理解其工作原理。


**推荐使用std::string_view替代C风格字符串符号常量**  

现代C++中几乎没有理由使用C风格字符串符号常量。建议改用`constexpr std::string_view`对象，其效率相当（甚至更高）且行为更一致。


**最佳实践**  
避免使用C风格字符串符号常量，优先选择`constexpr std::string_view`。


[下一课 17.12 多维C风格数组](Chapter-17/lesson17.12-multidimensional-c-style-arrays.md)  
[返回主页](/)  
[上一课 17.10 C风格字符串](Chapter-17/lesson17.10-c-style-strings.md)