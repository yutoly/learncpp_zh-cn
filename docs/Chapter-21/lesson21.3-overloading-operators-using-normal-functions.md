21.3 — 使用普通函数重载运算符  
====================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日（首次发布于2016年5月23日）  

 

在前一课程中，我们将operator+重载为友元函数（friend function）：

```cpp
#include <iostream>
 
class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}

  // 通过友元函数实现Cents + Cents
  friend Cents operator+(const Cents& c1, const Cents& c2);

  int getCents() const { return m_cents; }
};
 
// 注意：此函数并非成员函数！
Cents operator+(const Cents& c1, const Cents& c2)
{
  // 使用Cents构造函数和operator+(int, int)
  // 由于是友元函数，可直接访问私有成员
  return { c1.m_cents + c2.m_cents };
}
 
int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 };
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
```

使用友元函数重载运算符非常方便，因为它能直接访问操作类的内部成员。在上述Cents示例中，我们的友元版operator+直接访问了成员变量m_cents。


但如果不需要这种访问权限，可以将重载运算符编写为普通函数。注意上述Cents类包含一个访问函数（access function）getCents()，允许我们获取m_cents而无需直接访问私有成员。因此，我们可以将重载的operator+写成非友元形式：

```cpp
#include <iostream>

class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}

  int getCents() const { return m_cents; }
};

// 注意：此函数既非成员函数也非友元函数！
Cents operator+(const Cents& c1, const Cents& c2)
{
  // 使用Cents构造函数和operator+(int, int)
  // 此处无需直接访问私有成员
  return Cents{ c1.getCents() + c2.getCents() };
}

int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 };
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
```

由于普通函数与友元函数的工作方式几乎相同（仅对私有成员的访问权限不同），通常我们不作区分。唯一区别在于：友元函数在类内的声明同时充当原型（prototype）。对于普通函数版本，需要自行提供函数原型。


Cents.h头文件：

```cpp
#ifndef CENTS_H
#define CENTS_H

class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}
  
  int getCents() const { return m_cents; }
};

// 需要显式提供operator+原型，以便其他文件使用时知晓该重载存在
Cents operator+(const Cents& c1, const Cents& c2);

#endif
```

Cents.cpp实现文件：

```cpp
#include "Cents.h"

// 注意：此函数既非成员函数也非友元函数！
Cents operator+(const Cents& c1, const Cents& c2)
{
  // 使用Cents构造函数和operator+(int, int)
  // 此处无需直接访问私有成员
  return { c1.getCents() + c2.getCents() };
}
```

main.cpp主文件：

```cpp
#include "Cents.h"
#include <iostream>

int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 }; // 若Cents.h中没有原型声明，此处将编译失败
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
```

一般而言，在现有成员函数能满足需求的情况下，应优先选择普通函数而非友元函数（接触类内部的函数越少越好）。但不要为了将运算符重载为普通函数而非友元函数，而刻意添加额外的访问函数！

 

最佳实践  
----------------

在不需要额外添加函数的前提下，优先使用普通函数进行运算符重载而非友元函数。


[下一课 21.4 — 重载I/O运算符](Chapter-21/lesson21.4-overloading-the-io-operators.md)  
[返回主页](/)  
[上一课 21.2 — 使用友元函数重载算术运算符](Chapter-21/lesson21.2-overloading-the-arithmetic-operators-using-friend-functions.md)