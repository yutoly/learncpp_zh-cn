27.8 — 异常机制的隐患与缺点  
=======================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年10月26日，下午12:27（太平洋夏令时）  
2024年10月31日  

如同所有具备优势的事物，异常机制也存在潜在缺陷。本文并非详尽分析，仅指出使用异常（或决定是否使用时）需考虑的主要问题。  

**资源清理**  
新手使用异常时最常见的问题是异常发生时的资源清理。观察以下示例：  

```cpp
#include <iostream>

try
{
    openFile(filename);
    writeFile(filename, data);
    closeFile(filename);
}
catch (const FileException& exception)
{
    std::cerr << "Failed to write to file: " << exception.what() << '\n';
}
```  

若`writeFile()`失败并抛出`FileException`会怎样？此时文件已打开，但控制流跳转至异常处理程序，打印错误后退出。注意文件始终未关闭！应修改如下：  

```cpp
#include <iostream>

try
{
    openFile(filename);
    writeFile(filename, data);
}
catch (const FileException& exception)
{
    std::cerr << "Failed to write to file: " << exception.what() << '\n';
}

// 确保文件关闭
closeFile(filename);
```  

处理动态分配内存时此类错误常以另一种形式出现：  

```cpp
#include <iostream>

try
{
    auto* john { new Person{ "John", 18, PERSON_MALE } };
    processPerson(john);
    delete john;
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}
```  

若`processPerson()`抛出异常，控制流跳转至`catch`处理程序，导致`john`未被释放！此案例比前例更复杂——由于`john`是`try`块的局部变量，`try`块退出时其作用域结束。这意味着异常处理程序无法访问`john`（其已被销毁），故无法释放内存。  

有两种相对简单的修复方案。其一：在`try`块外声明`john`，使其不随`try`块退出而销毁：  

```cpp
#include <iostream>

Person* john{ nullptr };

try
{
    john = new Person("John", 18, PERSON_MALE);
    processPerson(john);
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}

delete john;
```  

由于`john`在`try`块外声明，其在`try`块和`catch`处理程序中均可访问，使异常处理程序能正确清理。  

其二：使用具有自动清理能力的局部类变量（常称"智能指针"）。标准库提供**std::unique_ptr**类实现此功能，该模板类持有指针并在作用域结束时自动释放：  

```cpp
#include <iostream>
#include <memory> // 引入std::unique_ptr

try
{
    auto* john { new Person("John", 18, PERSON_MALE) };
    std::unique_ptr<Person> upJohn { john }; // upJohn现在接管john

    ProcessPerson(john);

    // upJohn作用域结束时自动删除john
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}
```  

> **相关内容**  
> `std::unique_ptr`详见课程[22.5 — std::unique_ptr](Chapter-22/lesson22.5-stdunique_ptr.md)。  

最佳方案（尽可能）是优先使用实现RAII（构造时自动分配资源，析构时自动释放）的栈分配对象。这样资源管理对象无论因何原因离开作用域，都会自动执行适当清理。  

**异常与析构函数**  
构造函数中抛出异常可有效表示对象创建失败，但析构函数中**绝不应**抛出异常。  

问题发生在栈展开（stack unwinding）过程中从析构函数抛出异常时。此时编译器无法决定应继续栈展开还是处理新异常，最终导致程序立即终止。  

因此最佳实践是完全避免在析构函数中使用异常，可改为向日志文件写入消息。  

> **核心规则**  
> 若栈展开期间从析构函数抛出异常，程序将被终止。  

**性能考量**  
异常机制会带来轻微性能代价：增加可执行文件大小，且因需额外检查可能导致运行变慢。但主要性能损耗发生在实际抛出异常时，此时必须展开栈并查找匹配的异常处理程序，这是相对昂贵的操作。  

需注意：部分现代计算机架构支持**零开销异常（zero-cost exceptions）**模型。若支持此模型，在无错误情况下（最关注性能的场景）无额外运行时开销，但在发生异常时代价更高。  

**何时应使用异常？**  
异常处理最适合以下所有条件成立时：  
* 被处理的错误发生频率较低  
* 错误严重且无法继续执行  
* 错误无法在发生位置处理  
* 无更好方法向调用方返回错误码  

以函数需要用户传入磁盘文件名场景为例：函数将打开文件、读取数据、关闭文件并向调用方返回结果。假设用户传入不存在的文件名或空字符串，此时是否适用异常？  

前两点显然满足——此情况不常发生，且无数据时函数无法计算结果。函数自身也无法处理错误——其职责不包括重新提示用户输入文件名（根据程序设计可能也不合适）。第四点是关键：是否存在向调用方返回错误码的更好替代方案？这取决于程序细节。若存在（如返回空指针或失败状态码），可能是更佳选择；若不存在，则异常机制合理。  

[下一课 27.9 异常规范与noexcept](Chapter-27/lesson27.9-exception-specifications-and-noexcept.md)  
[返回主页](/)  
[上一课 27.7 函数try块](Chapter-27/lesson27.7-function-try-blocks.md)