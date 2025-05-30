14.6 — 访问函数  
========================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月29日（首次发布于2007年9月4日）  

在前一课程[14.5 — 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)中，我们讨论了公有（public）和私有（private）访问级别。需要记住的是，类通常将数据成员设为私有，而私有成员无法被外界直接访问。  

考虑以下`Date`类：  
```
#include <iostream>

class Date
{
private:
    int m_year{ 2020 };
    int m_month{ 10 };
    int m_day{ 14 };

public:
    void print() const
    {
        std::cout << m_year << '/' << m_month << '/' << m_day << '\n';
    }
};

int main()
{
    Date d{};  // 创建Date对象
    d.print(); // 打印日期

    return 0;
}
```  
虽然该类提供了`print()`成员函数来打印完整日期，但可能无法满足用户需求。例如，如果用户想获取年份或修改年份该怎么办？由于`m_year`是私有成员，用户无法直接访问。  

对于某些类而言，允许获取或修改私有成员变量是合理的（需根据类的具体功能判断）。  

访问函数（Access functions）  
----------------  

**访问函数（access function）**是一种简单的公有成员函数，其职责是获取或修改私有成员变量的值。  

访问函数分为两种类型：  
* **访问器（getters）**（有时称为获取函数）：返回私有成员变量值的公有成员函数  
* **修改器（setters）**（有时称为设置函数）：设置私有成员变量值的公有成员函数  

### 术语说明  
"Mutator"（修改器）常与"setter"互换使用。但更广义地说，**修改器（mutator）**指任何能修改对象状态的成员函数。根据此定义，setter是特定类型的修改器。但也存在非setter的修改器函数。  

访问器通常设为const，以便可在const和非const对象上调用。修改器应为非const，以便修改数据成员。  

为演示目的，我们更新`Date`类以包含完整的访问器和修改器：  
```
#include <iostream>

class Date
{
private:
    int m_year { 2020 };
    int m_month { 10 };
    int m_day { 14 };

public:
    void print()
    {
        std::cout << m_year << '/' << m_month << '/' << m_day << '\n';
    }

    int getYear() const { return m_year; }        // 年份访问器
    void setYear(int year) { m_year = year; }     // 年份修改器

    int getMonth() const  { return m_month; }     // 月份访问器
    void setMonth(int month) { m_month = month; } // 月份修改器

    int getDay() const { return m_day; }          // 日期访问器
    void setDay(int day) { m_day = day; }         // 日期修改器
};

int main()
{
    Date d{};
    d.setYear(2021);
    std::cout << "当前年份: " << d.getYear() << '\n';

    return 0;
}
```  
输出结果：  
```
当前年份: 2021
```  

### 访问函数命名规范  
访问函数没有统一命名规范，但以下几种较为流行：  
* **带"get"和"set"前缀**：  
```
    int getDay() const { return m_day; }  // 访问器
    void setDay(int day) { m_day = day; } // 修改器
```  
优点：明确表明访问函数性质（且调用成本低）  

* **无前缀**：  
```
    int day() const { return m_day; }  // 访问器
    void day(int day) { m_day = day; } // 修改器
```  
该风格更简洁，访问器和修改器使用相同名称（通过函数重载区分）。C++标准库采用此规范。缺点：修改操作不够直观：  
```
d.day(5); // 这看起来像是设置日期成员为5吗？
```  

* **仅修改器带"set"前缀**：  
```
    int day() const { return m_day; }     // 访问器
    void setDay(int day) { m_day = day; } // 修改器
```  

选择哪种风格取决于个人偏好。但我们强烈建议修改器使用"set"前缀。访问器可选择"get"前缀或无前缀。  

> **提示**  
> 在修改器中使用"set"前缀，能更清晰地表明对象状态将被改变。  

### 关键洞察  
私有数据成员添加"m_"前缀的最佳原因之一，是避免数据成员与访问器重名（C++不支持这种重名，但Java等语言允许）。  

访问器应返回值或const左值引用  
----------------  

访问器应提供对数据的"只读"访问。最佳实践是：  
* 若成员复制成本低，返回**值**  
* 若成员复制成本高，返回**const左值引用**  

由于通过引用返回数据成员涉及复杂问题，我们将在课程[14.7 — 返回数据成员引用的成员函数](Chapter-14/lesson14.7-member-functions-returning-references-to-data-members.md)中详细讨论。  

访问函数注意事项  
----------------  

关于访问函数的使用与否存在广泛讨论。许多开发者认为访问函数的使用违反了良好的类设计原则（该主题可单独成书）。  

目前我们推荐实用主义方法。创建类时请考虑：  
* 若类无不变式且需要大量访问函数，考虑使用结构体（struct）直接公开数据成员  
* 优先实现行为而非访问函数。例如，用`kill()`和`revive()`函数代替`setAlive(bool)`修改器  
* 仅在确实需要获取或设置单个成员值时提供访问函数  

### 为何要私有化数据又提供公开访问函数？  
这个问题将在后续课程[14.8 — 数据隐藏（封装）的优势](Chapter-14/lesson14.8-the-benefits-of-data-hiding-encapsulation.md)中解答。  

[下一课14.7 返回数据成员引用的成员函数](Chapter-14/lesson14.7-member-functions-returning-references-to-data-members.md)  
[返回主页](/)  
[上一课14.5 公有与私有成员及访问说明符](Chapter-14/lesson14.5-public-and-private-members-and-access-specifiers.md)