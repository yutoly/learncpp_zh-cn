27.6 — 重新抛出异常（Rethrowing exceptions）  
============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月15日（首次发布于2017年2月5日）  

 

某些情况下，您可能需要捕获异常（exception）但无法在捕获点完全处理。这在需要记录错误但将问题传递给调用者处理时很常见。


当函数使用返回码时，处理简单。参考以下示例：



```
Database* createDatabase(std::string filename)
{
    Database* d {};

    try
    {
        d = new Database{};
        d->open(filename); // 假设失败时抛出int类型异常
        return d;
    }
    catch (int exception)
    {
        // 数据库创建失败
        delete d;
        // 向全局日志文件写入错误
        g_log.logError("Database创建失败");
    }

    return nullptr;
}
```

上述代码中，函数负责创建Database对象、打开数据库并返回对象。当出现问题时（例如传入错误文件名），异常处理程序记录错误后合理返回空指针。


现在考虑以下函数：



```
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 失败时抛出int异常
    }
    catch (int exception)
    {
        // 向全局日志文件写入错误
        g_log.logError("getIntValueFromDatabase失败");

        // 但未实际处理该错误
        // 此时应如何操作？
    }
}
```

当函数成功时返回整数值——任何整数值都可能是有效值。


但getIntValue()出错时会发生什么？此时getIntValue()抛出int异常，被getIntValueFromDatabase()的catch块捕获并记录错误。但如何通知getIntValueFromDatabase()的调用者发生了错误？与第一个示例不同，此处没有合适的返回码可用（因为所有整数返回值都可能是有效的）。


**抛出新异常**


明显解决方案是抛出新异常：



```
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 失败时抛出int异常
    }
    catch (int exception)
    {
        // 向全局日志文件写入错误
        g_log.logError("getIntValueFromDatabase失败");

        // 向上抛出char类型异常'q'供调用者处理
        throw 'q'; 
    }
}
```

此例中，程序捕获getIntValue()的int异常，记录错误后抛出char值'q'的新异常。虽然在catch块抛出异常看似奇怪，但这是允许的。记住，只有try块内抛出的异常才能被捕获。这意味着catch块抛出的异常不会被当前catch块捕获，而是传播给调用者。


从catch块抛出的异常可以是任意类型——不必与捕获的异常类型相同。


**重新抛出异常（错误方式）**


另一种选择是重新抛出相同异常。实现方式如下：



```
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 失败时抛出int异常
    }
    catch (int exception)
    {
        // 向全局日志文件写入错误
        g_log.logError("getIntValueFromDatabase失败");

        throw exception;
    }
}
```

虽然可行，但此方法有两个缺点。首先，抛出的并非原始异常——而是变量exception的拷贝初始化副本。尽管编译器可能优化拷贝，但未必总能实现，可能影响性能。


更重要的是考虑以下情形：



```
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 失败时抛出派生类（Derived）异常
    }
    catch (Base& exception)
    {
        // 向全局日志文件写入错误
        g_log.logError("getIntValueFromDatabase失败");

        throw exception; // 危险：抛出Base对象而非Derived对象
    }
}
```

本例中，getIntValue()抛出派生类对象，但catch块捕获的是基类（Base）引用。这没有问题，因为基类引用可以指向派生类对象。但抛出异常时，抛出的异常是变量exception的拷贝初始化。变量exception类型为Base，因此拷贝初始化的异常也是Base类型（而非Derived）！即发生了派生类对象的切片（slicing）！


以下程序演示此问题：


```
#include <iostream>
class Base
{
public:
    Base() {}
    virtual void print() { std::cout << "Base"; }
};

class Derived: public Base
{
public:
    Derived() {}
    void print() override { std::cout << "Derived"; }
};

int main()
{
    try
    {
        try
        {
            throw Derived{};
        }
        catch (Base& b)
        {
            std::cout << "捕获Base b，实际类型是";
            b.print();
            std::cout << '\n';
            throw b; // 此处发生Derived对象切片
        }
    }
    catch (Base& b)
    {
        std::cout << "捕获Base b，实际类型是";
        b.print();
        std::cout << '\n';
    }

    return 0;
}
```

输出：

```
捕获Base b，实际类型是Derived
捕获Base b，实际类型是Base
```

第二行显示Base实际是基类而非派生类，证明发生了派生类对象切片。


**重新抛出异常（正确方式）**


幸运的是，C++提供了重新抛出相同异常的方法。只需在catch块中使用throw关键字（不带变量），如下：



```
#include <iostream>
class Base
{
public:
    Base() {}
    virtual void print() { std::cout << "Base"; }
};

class Derived: public Base
{
public:
    Derived() {}
    void print() override { std::cout << "Derived"; }
};

int main()
{
    try
    {
        try
        {
            throw Derived{};
        }
        catch (Base& b)
        {
            std::cout << "捕获Base b，实际类型是";
            b.print();
            std::cout << '\n';
            throw; // 注意：此处重新抛出原对象
        }
    }
    catch (Base& b)
    {
        std::cout << "捕获Base b，实际类型是";
        b.print();
        std::cout << '\n';
    }

    return 0;
}
```

输出：

```
捕获Base b，实际类型是Derived
捕获Base b，实际类型是Derived
```

单独使用的throw关键字会重新抛出完全相同的异常。不会创建拷贝，因此无需担心性能损耗或切片问题。


若需重新抛出异常，应优先采用此方法。


 

规则


重新抛出相同异常时，应单独使用throw关键字




[下一课 27.7 函数try块](Chapter-27/lesson27.7-function-try-blocks.md)  
[返回主页](/)  
[上一课 27.5 异常、类与继承](Chapter-27/lesson27.5-exceptions-classes-and-inheritance.md)