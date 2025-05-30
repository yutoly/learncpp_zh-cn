25.4 — 虚析构函数、虚赋值与覆盖虚化
==============================================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2008年2月1日下午1:50（太平洋标准时间）
2024年10月18日更新

**虚析构函数（Virtual destructors）**  
尽管C++会在未自定义析构函数时提供默认析构函数，但有时仍需自定义析构函数（特别是类需要释放内存时）。在处理继承时，应*始终*将析构函数声明为虚函数。参考以下示例：
```
#include <iostream>
class Base
{
public:
    ~Base() // 注意：非虚函数
    {
        std::cout << "Calling ~Base()\n";
    }
};

class Derived: public Base
{
private:
    int* m_array {};

public:
    Derived(int length)
      : m_array{ new int[length] }
    {
    }

    ~Derived() // 注意：非虚函数（编译器可能警告）
    {
        std::cout << "Calling ~Derived()\n";
        delete[] m_array;
    }
};

int main()
{
    Derived* derived { new Derived(5) };
    Base* base { derived };

    delete base;

    return 0;
}
```
> **注意**：编译此示例时编译器可能警告非虚析构函数（本例故意为之）。可能需要禁用"将警告视为错误"的编译选项。

由于base是Base指针，当删除base时，程序检查Base析构函数是否为虚函数。实际非虚，因此仅调用Base析构函数。输出结果可验证：
```
Calling ~Base()
```
但我们需要delete操作调用Derived的析构函数（其将自动调用Base析构函数），否则m_array不会被释放。通过将Base析构函数设为虚函数实现：
```
#include <iostream>
class Base
{
public:
    virtual ~Base() // 注意：虚函数
    {
        std::cout << "Calling ~Base()\n";
    }
};

class Derived: public Base
{
private:
    int* m_array {};

public:
    Derived(int length)
      : m_array{ new int[length] }
    {
    }

    virtual ~Derived() // 注意：虚函数
    {
        std::cout << "Calling ~Derived()\n";
        delete[] m_array;
    }
};

int main()
{
    Derived* derived { new Derived(5) };
    Base* base { derived };

    delete base;

    return 0;
}
```
现在程序输出符合预期：
```
Calling ~Derived()
Calling ~Base()
```

**核心规则**  
处理继承时，所有显式定义的析构函数必须声明为虚函数。

与普通虚成员函数类似，若基类函数为虚函数，则所有派生类覆盖函数自动视为虚函数（无论是否显式声明）。不必仅为标记虚函数而创建空的派生类析构函数。  
若需基类拥有空的虚析构函数，可定义为：
```
    virtual ~Base() = default; // 生成虚默认析构函数
```

**虚赋值（Virtual assignment）**  
可使赋值运算符虚化。但与析构函数始终需虚化不同，虚化赋值运算符会引发复杂问题（超出本教程范围）。因此建议保持赋值运算符非虚化以确保简洁性。

**忽略虚化（Ignoring virtualization）**  
极少数情况下可能需要忽略函数虚化。例如：
```
#include <string_view>
class Base
{
public:
    virtual ~Base() = default;
    virtual std::string_view getName() const { return "Base"; }
};

class Derived: public Base
{
public:
    virtual std::string_view getName() const { return "Derived"; }
};
```
若需通过指向派生类对象的基类指针调用Base::getName()而非Derived::getName()，可使用作用域解析运算符：
```
#include <iostream>
int main()
{
    Derived derived {};
    const Base& base { derived };

    // 调用Base::getName()而非虚化的Derived::getName()
    std::cout << base.Base::getName() << '\n';

    return 0;
}
```
此技巧使用频率较低，但有必要了解其可行性。

**是否应将所有析构函数设为虚函数？**  
这是新手常见问题。如首例所示，若基类析构函数未标记为虚函数，当程序员删除指向派生类对象的基类指针时可能导致内存泄漏。将所有析构函数标记为虚函数可避免此问题，但需权衡性能代价（每个类实例增加虚指针）。  
建议遵循：  
* 非明确设计为基类的类，通常不应包含虚成员和虚析构函数（仍可通过组合使用）  
* 设计为基类或含虚函数的类，必须始终拥有虚析构函数  

若决定类不可继承，则需考虑如何强制实施。传统观点（源自C++权威Herb Sutter）建议："基类析构函数应设为public+virtual或protected+non-virtual"。protected析构函数可防止通过基类指针删除派生类对象。  
但此方案存在缺陷：  
* 无法常规删除动态分配的基类对象  
* 静态分配的基类对象超出作用域时无法访问析构函数  

换言之，此方案虽保护派生类，却导致基类本身几乎不可用。引入`final`标识符后，新方案如下：  
* 设计可继承的类：析构函数设为public且virtual  
* 设计不可继承的类：使用final标记类  

[下一课 25.5 — 早绑定与晚绑定](Chapter-25/lesson25.5-early-binding-and-late-binding.md)  
[返回主页](/)    
[上一课 25.3 — override与final标识符及协变返回类型](Chapter-25/lesson25.3-the-override-and-final-specifiers-and-covariant-return-types.md)