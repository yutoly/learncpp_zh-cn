21.13 — 浅拷贝与深拷贝  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年11月9日，下午3:39（太平洋标准时间）  
2023年9月11日  

浅拷贝（Shallow copying）  
----------------  

由于C++对自定义类了解有限，其提供的默认拷贝构造函数和默认赋值运算符采用**成员逐一拷贝（memberwise copy）**（亦称**浅拷贝（shallow copy）**）机制。这意味着C++会单独拷贝类的每个成员（对重载的赋值运算符使用operator=，对拷贝构造函数使用直接初始化）。当类结构简单（例如不包含动态分配内存）时，这种方式非常有效。  

例如观察以下分数（Fraction）类：  

```cpp
#include <cassert>
#include <iostream>

class Fraction
{
private:
    int m_numerator { 0 };  // 分子
    int m_denominator { 1 }; // 分母

public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
        assert(denominator != 0); // 确保分母不为零
    }

    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1); // 友元输出运算符
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
    out << f1.m_numerator << '/' << f1.m_denominator;
    return out;
}
```  

编译器为此类生成的默认拷贝构造函数和默认赋值运算符类似如下实现：  

```cpp
#include <cassert>
#include <iostream>

class Fraction
{
private:
    int m_numerator { 0 };
    int m_denominator { 1 };

public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
        assert(denominator != 0);
    }

    // 隐式拷贝构造函数的可能实现
    Fraction(const Fraction& f)
        : m_numerator{ f.m_numerator } // 拷贝分子
        , m_denominator{ f.m_denominator } // 拷贝分母
    {
    }

    // 隐式赋值运算符的可能实现
    Fraction& operator= (const Fraction& fraction)
    {
        // 自赋值检查（self-assignment guard）
        if (this == &fraction)
            return *this;

        // 执行拷贝
        m_numerator = fraction.m_numerator;
        m_denominator = fraction.m_denominator;

        // 返回当前对象以实现链式调用
        return *this;
    }

    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1)
    {
        out << f1.m_numerator << '/' << f1.m_denominator;
        return out;
    }
};
```  

注意：由于默认版本对此类拷贝操作完全适用，因此本例无需自行实现这些函数。  

然而，当设计涉及动态内存分配的类时，成员逐一（浅）拷贝会导致严重问题！这是因为指针的浅拷贝仅复制指针地址——既不会分配新内存，也不会复制指针指向的内容！  

观察以下示例：  

```cpp
#include <cstring> // 引入strlen
#include <cassert> // 引入assert

class MyString
{
private:
    char* m_data{};     // 字符串数据指针
    int m_length{};      // 字符串长度

public:
    MyString(const char* source = "" )
    {
        assert(source); // 确保源字符串非空

        // 计算字符串长度（含终止符）
        m_length = std::strlen(source) + 1;
        
        // 分配等长缓冲区
        m_data = new char[m_length];
        
        // 将参数字符串复制到内部缓冲区
        for (int i{ 0 }; i < m_length; ++i)
            m_data[i] = source[i];
    }
 
    ~MyString() // 析构函数
    {
        // 释放字符串内存
        delete[] m_data;
    }
 
    char* getString() { return m_data; }
    int getLength() { return m_length; }
};
```  

这是一个分配内存存储传入字符串的简单字符串类。注意：我们未定义拷贝构造函数或重载赋值运算符。因此C++将提供执行浅拷贝的默认版本。拷贝构造函数类似如下形式：  

```cpp
MyString::MyString(const MyString& source)
    : m_length { source.m_length } // 拷贝长度
    , m_data { source.m_data }     // 浅拷贝指针（指向相同地址）
{
}
```  

注意：m_data仅是source.m_data的浅拷贝指针，意味着两者指向同一内存地址。  

现在分析以下代码片段：  

```cpp
#include <iostream>

int main()
{
    MyString hello{ "Hello, world!" }; // 创建hello对象
    {
        MyString copy{ hello }; // 使用默认拷贝构造函数
    } // copy是局部变量，此处被销毁。析构函数删除copy的字符串，导致hello的指针悬空

    std::cout << hello.getString() << '\n'; // 未定义行为（undefined behavior）

    return 0;
}
```  

这段看似无害的代码暗藏隐患，将导致程序出现未定义行为！  

逐行解析：  
1. `MyString hello{ "Hello, world!" };`  
   调用构造函数为hello分配内存，复制字符串"Hello, world!"。  

2. `MyString copy{ hello };`  
   使用默认拷贝构造函数执行浅拷贝，使copy.m_data与hello.m_data指向同一内存地址。  

3. `}`（作用域结束）  
   copy离开作用域时，其析构函数删除动态内存（两者共享）。导致hello.m_data成为悬空指针（dangling pointer）。  

4. `std::cout << hello.getString() << '\n';`  
   尝试访问已释放内存，触发未定义行为。  

问题根源在于拷贝构造函数的浅拷贝操作——在拷贝构造函数或重载赋值运算符中对指针进行浅拷贝几乎必然引发问题。  

深拷贝（Deep copying）  
----------------  

解决方案是对待拷贝的非空指针执行**深拷贝（deep copy）**。深拷贝会为副本分配新内存并复制实际值，使副本与源对象内存独立。这样副本与源对象完全隔离，互不影响。实现深拷贝需自定义拷贝构造函数和重载赋值运算符。  

以下展示MyString类的实现方法：  

```cpp
// 假设m_data已初始化
void MyString::deepCopy(const MyString& source)
{
    // 首先释放当前字符串持有的内存！
    delete[] m_data;

    // m_length非指针，可浅拷贝
    m_length = source.m_length;

    // m_data为指针，若源非空则需深拷贝
    if (source.m_data)
    {
        // 为副本分配内存
        m_data = new char[m_length];

        // 执行复制
        for (int i{ 0 }; i < m_length; ++i)
            m_data[i] = source.m_data[i];
    }
    else
        m_data = nullptr;
}

// 拷贝构造函数
MyString::MyString(const MyString& source)
{
    deepCopy(source); // 调用深拷贝
}
```  

可见深拷贝比浅拷贝复杂得多！首先检查源对象是否持有字符串（第11行）。若有，则分配足够内存存储副本（第14行）。最后手动复制字符串内容（第17-18行）。  

现在实现重载赋值运算符，其逻辑略复杂：  

```cpp
// 赋值运算符
MyString& MyString::operator=(const MyString& source)
{
    // 检查自赋值（self-assignment）
    if (this != &source)
    {
        // 执行深拷贝
        deepCopy(source);
    }

    return *this; // 支持链式赋值
}
```  

注意：赋值运算符与拷贝构造函数相似，但有三大区别：  
1. 添加了自赋值检查（self-assignment check）  
2. 返回*this以支持链式赋值（operator chaining）  
3. 需显式释放当前字符串内存（防止后续重分配时内存泄漏（memory leak）），该操作在deepCopy()中完成  

调用重载赋值运算符时，被赋值对象可能已持有值，需在分配新内存前清理旧值。对非动态分配变量（固定大小），新值直接覆盖旧值即可。但对动态分配变量，必须在分配新内存前显式释放旧内存，否则虽不会崩溃，但每次赋值都会因内存泄漏消耗可用内存！  

三法则（The rule of three）  
----------------  

还记得**三法则（rule of three）**吗？若类需要用户定义的析构函数、拷贝构造函数或拷贝赋值运算符，则三者通常都需要。原因在于：当需要自定义这些函数时，往往涉及动态内存管理。拷贝构造函数和赋值运算符用于处理深拷贝，析构函数则负责内存释放。  

更佳解决方案（A better solution）  
----------------  

标准库中处理动态内存的类（如std::string和std::vector）已自行管理内存，其重载的拷贝构造函数和赋值运算符能正确执行深拷贝。因此无需手动管理内存，可像基础变量一样初始化或赋值！这些类更易用、更不易出错，且无需自行编写重载函数！  

总结（Summary）  
----------------  

* 默认拷贝构造函数和默认赋值运算符执行浅拷贝，对不含动态分配变量的类适用  
* 含动态分配变量的类需定义执行深拷贝的拷贝构造函数和赋值运算符  
* 优先使用标准库类而非手动管理内存  

[下一课 21.14 — 重载运算符与函数模板](Chapter-21/lesson21.14-overloading-operators-and-function-templates.md)  
[返回主页](/)    
[上一课 21.12 — 重载赋值运算符](Chapter-21/lesson21.12-overloading-the-assignment-operator.md)