21.4 — 重载I/O操作符
=====================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2007年10月1日，下午4:41（太平洋夏令时）
2025年1月29日更新

对于包含多个成员变量的类，逐个打印变量会很快变得繁琐。例如以下类：
```
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }
};
```
若需打印该类的实例，需编写如下代码：
```
Point point { 5.0, 6.0, 7.0 };

std::cout << "Point(" << point.getX() << ", " <<
    point.getY() << ", " <<
    point.getZ() << ')';
```
更合理的做法是将其封装为可复用函数。在先前示例中，我们创建了如下`print()`函数：
```
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }

    void print() const
    {
        std::cout << "Point(" << m_x << ", " << m_y << ", " << m_z << ')';
    }
};
```
虽然此方案更优，但仍存在缺陷。由于`print()`返回`void`，无法在输出语句中间调用：
```
int main()
{
    const Point point { 5.0, 6.0, 7.0 };

    std::cout << "My point is: ";
    point.print();
    std::cout << " in Cartesian space.\n";
}
```
理想情况是能直接编写：
```
Point point{5.0, 6.0, 7.0};
cout << "My point is: " << point << " in Cartesian space.\n";
```
并获得相同结果。这样既无需拆分输出语句，也不必记忆打印函数名称。

通过重载`operator<<`即可实现！

### 重载operator<<
重载`operator<<`类似于重载operator+（两者均为二元操作符），但参数类型不同。

分析表达式`std::cout << point`：当操作符为`<<`时，操作数是什么？左操作数是`std::cout`对象，右操作数是`Point`类对象。`std::cout`实际是`std::ostream（标准输出流）`类型的对象。因此重载函数声明如下：
```
// std::ostream对应std::cout的类型
friend std::ostream& operator<< (std::ostream& out, const Point& point);
```
为`Point`类实现`operator<<`较为直接——因C++已知如何用`operator<<`输出double类型，且成员均为double，可直接输出`Point`的数据成员。以下是重载`operator<<`的完整`Point`类：
```
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // operator<<是Point的友元，可直接访问成员
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')'; // 实际输出

    return out; // 返回std::ostream以支持链式调用
}

int main()
{
    const Point point1 { 2.0, 3.0, 4.0 };

    std::cout << point1 << '\n';

    return 0;
}
```
实现逻辑清晰——注意输出行与先前`print()`函数的相似性。主要区别在于`std::cout`变为参数`out`（调用时将是`std::cout`的引用）。

关键点在于返回类型：算术操作符通过值返回计算结果（因需创建新结果）。但尝试以值返回`std::ostream`会导致编译错误，因`std::ostream`明确禁止拷贝。

此处通过引用返回左操作数。这既避免拷贝`std::ostream`，又支持链式输出（如`std::cout << point << '\n'`）。

思考若`operator<<`返回`void`的情况：编译器解析`std::cout << point << '\n'`时，按结合律视为`(std::cout << point) << '\n';`。`std::cout << point`调用返回void的重载函数后，表达式变为`void << '\n';`，这毫无意义！

通过返回`out`参数，`(std::cout << point)`返回`std::cout`，使表达式变为`std::cout << '\n';`，从而正确执行。

若需重载二元操作符支持链式调用，应通过引用返回左操作数。此场景中安全，因左操作数由调用方传入，返回时仍存在。

为验证可行性，使用上述重载`operator<<`的`Point`类：
```
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';
    return out;
}

int main()
{
    Point point1 { 2.0, 3.5, 4.0 };
    Point point2 { 6.0, 7.5, 8.0 };

    std::cout << point1 << ' ' << point2 << '\n';

    return 0;
}
```
输出结果：
```
Point(2, 3.5, 4) Point(6, 7.5, 8)
```
此实现中`operator<<`需设为友元以直接访问成员。若可通过getter访问成员，则可实现为非友元。

### 重载operator>>
输入操作符也可重载，方法与输出操作符类似。核心需知`std::cin`是`std::istream（标准输入流）`类型对象。为`Point`类添加重载`operator>>`：
```
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
    friend std::istream& operator>> (std::istream& out, Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';
    return out;
}

// point须为非const以便修改
std::istream& operator>> (std::istream& in, Point& point)
{
    // 此版本存在部分提取问题（见下文）
    in >> point.m_x >> point.m_y >> point.m_z;
    return in;
}

int main()
{
    std::cout << "Enter a point: ";

    Point point{ 1.0, 2.0, 3.0 }; // 非零测试数据
    std::cin >> point;

    std::cout << "You entered: " << point << '\n';

    return 0;
}
```
若用户输入`4.0 5.6 7.26`，输出为：
```
You entered: Point(4, 5.6, 7.26)
```
但当用户输入`4.0b 5.6 7.26`（`4.0`后带`b`）时：
```
You entered: Point(4, 0, 3)
```
此时对象变为混合值：一个来自输入(`4.0`)，一个零初始化(`0.0`)，一个未修改(`3.0`)。这显然不理想！

### 防范部分提取
提取单个值时，结果只有成功或失败。但提取多个值时情况更复杂。

上述`operator>>`实现可能导致部分提取。输入`4.0b 5.6 7.26`时：`m_x`成功提取`4.0`，输入流剩余`b 5.6 7.26`。`m_y`提取`b`失败，故被赋值为`0.0`且输入流进入失败模式。因未清除失败状态，`m_z`提取中止，保留原值`3.0`。

这种情况绝不可取，甚至可能引发危险。例如为`Fraction`类实现`operator>>`时，若分子提取成功而分母失败，分母被置为`0.0`可能导致除零崩溃。

如何避免？解决方案是实现事务性操作（transactional operation）。事务性操作必须完全成功或完全失败——不允许部分成功。有时称为"全有或全无"。若过程中任何步骤失败，必须撤销已进行的更改。

> **关键洞察**
> 现实中的事务操作：银行转账包含扣款和存款两步。可能情况：
> * 扣款失败（如余额不足）：事务失败，账户不变
> * 存款失败（如技术故障）：必须撤销已成功的扣款，事务失败
> * 两步均成功：事务成功，账户更新

最终只有两种结果：完全失败（账户不变）或完全成功（账户更新）。

重写`Point`的`operator>>`为事务性操作：
```
// point须为非const
// 此实现为非友元
std::istream& operator>> (std::istream& in, Point& point)
{
    double x{};
    double y{};
    double z{};
    
    if (in >> x >> y >> z)      // 若全部提取成功
        point = Point{x, y, z}; // 覆盖现有point对象
        
    return in;
}
```
此实现不直接修改成员，而是将输入提取到临时变量(`x`,`y`,`z`)。全部提取成功后，才一次性更新`Point`所有成员。

> **提示**
> `if (in >> x >> y >> z)`等价于`in >> x >> y >> z; if (in)`。每次提取返回`in`以支持链式调用。单语句版本使用最后一次提取返回的`in`作为if条件。

> **技巧**
> 事务性操作可通过不同策略实现：
> * 成功时修改：存储每个子操作结果。全部成功后替换目标数据（本例策略）
> * 失败时还原：备份可修改数据。任何子操作失败时，用备份还原先前修改
> * 失败时回滚：任何子操作失败时，逆向执行先前操作（常用于数据库）

虽然上述`operator>>`防止了部分提取，但行为与基础类型不一致。基础类型提取失败时对象被赋值为`0`（确保存在有效值）。因此为保持一致性，可让失败提取将对象重置为默认状态。

以下是重置`Point`的替代方案：
```
std::istream& operator>> (std::istream& in, Point& point)
{
    double x{};
    double y{};
    double z{};
    
    in >> x >> y >> z;
    point = in ? Point{x, y, z} : Point{}; // 成功时更新，失败时重置
        
    return in;
}
```
> **作者注**
> 此操作技术上已非事务性（因失败时执行了操作）。尚无通用术语描述"保证无部分结果"的操作，或可称"不可分割操作"。

### 处理语义无效输入
提取失败有多种情况。

当`operator>>`完全无法提取变量时，`std::cin`自动进入失败模式（见课程[9.5 — std::cin与处理无效输入](Chapter-9/lesson9.5-stdcin-and-handling-invalid-input.md)）。调用方可检查`std::cin`处理该情况。

但当用户输入可提取但语义无效的值时（如分母为`0`的`Fraction`）？因`std::cin`已提取内容，不会自动进入失败模式，调用方可能无法察觉问题。

解决方案：在重载`operator>>`中检查提取值语义有效性，若无效则手动置失败位：调用`std::cin.setstate(std::ios_base::failbit);`。

以下是带手动失败检测的事务性`operator>>`，当输入负值时触发失败模式：
```
std::istream& operator>> (std::istream& in, Point& point)
{
    double x{};
    double y{};
    double z{};
    
    in >> x >> y >> z;
    if (x < 0.0 || y < 0.0 || z < 0.0)       // 若任何输入为负
        in.setstate(std::ios_base::failbit); // 手动置失败位
    point = in ? Point{x, y, z} : Point{};
       
    return in;
}
```
### 结论
重载`operator<<`和`operator>>`能简化类对象的控制台输出与输入。

### 测验时间
**问题1**
为下方Fraction类添加重载`operator<<`和`operator>>`。要求：
- `operator>>`避免部分提取
- 分母为0时失败
- 失败时不重置Fraction

以下程序应能编译：
```
int main()
{
	Fraction f1{};
	std::cout << "Enter fraction 1: ";
	std::cin >> f1;

	Fraction f2{};
	std::cout << "Enter fraction 2: ";
	std::cin >> f2;

	std::cout << f1 << " * " << f2 << " is " << f1 * f2 << '\n'; // 注：f1 * f2结果为右值
	return 0;
}
```
预期输出：
```
Enter fraction 1: 2/3
Enter fraction 2: 3/8
2/3 * 3/8 is 1/4
```
Fraction类定义：
```
#include <iostream>
#include <numeric> // for std::gcd
 
class Fraction
{
private:
	int m_numerator{};
	int m_denominator{};
 
public:
	Fraction(int numerator=0, int denominator=1):
		m_numerator{numerator}, m_denominator{denominator}
	{
		reduce(); // 构造函数中约分确保新建分数已简化
	}

	void reduce()
	{
		int gcd{ std::gcd(m_numerator, m_denominator) };
		if (gcd)
		{
			m_numerator /= gcd;
			m_denominator /= gcd;
		}
	}
 
	friend Fraction operator*(const Fraction& f1, const Fraction& f2);
	friend Fraction operator*(const Fraction& f1, int value);
	friend Fraction operator*(int value, const Fraction& f1);
 
	void print() const
	{
		std::cout << m_numerator << '/' << m_denominator << '\n';
	}
};
 
Fraction operator*(const Fraction& f1, const Fraction& f2)
{
	return Fraction { f1.m_numerator * f2.m_numerator, f1.m_denominator * f2.m_denominator };
}
 
Fraction operator*(const Fraction& f1, int value)
{
	return Fraction { f1.m_numerator * value, f1.m_denominator };
}
 
Fraction operator*(int value, const Fraction& f1)
{
	return Fraction { f1.m_numerator * value, f1.m_denominator };
}
```
若编译器低于C++17，可用此函数替代std::gcd：
```
#include <cmath>
 
int gcd(int a, int b) {
    return (b == 0) ? std::abs(a) : gcd(b, a % b);
}
```
[参考答案](javascript:void(0))
```
#include <iostream>
#include <limits>
#include <numeric> // for std::gcd

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    Fraction(int numerator=0, int denominator = 1) :
        m_numerator{ numerator }, m_denominator{ denominator }
    {
        reduce();
    }

    void reduce()
    {
        int gcd{ std::gcd(m_numerator, m_denominator) };
        if (gcd)
        {
            m_numerator /= gcd;
            m_denominator /= gcd;
        }
    }

    friend Fraction operator*(const Fraction& f1, const Fraction& f2);
    friend Fraction operator*(const Fraction& f1, int value);
    friend Fraction operator*(int value, const Fraction& f1);

    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);

    void print() const
    {
        std::cout << m_numerator << '/' << m_denominator << '\n';
    }
};

Fraction operator*(const Fraction& f1, const Fraction& f2)
{
    return Fraction { f1.m_numerator * f2.m_numerator, f1.m_denominator * f2.m_denominator };
}

Fraction operator*(const Fraction& f1, int value)
{
    return Fraction { f1.m_numerator * value, f1.m_denominator };
}

Fraction operator*(int value, const Fraction& f1)
{
    return Fraction { f1.m_numerator * value, f1.m_denominator };
}

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
    out << f1.m_numerator << '/' << f1.m_denominator;
    return out;
}

std::istream& operator>>(std::istream& in, Fraction& f1)
{
    int numerator {};
    char ignore {};
    int denominator {};
    
    in >> numerator >> ignore >> denominator;
    if (denominator == 0)                       // 分母语义无效
        in.setstate(std::ios_base::failbit);    // 手动置失败位
    if (in)                                     // 非失败模式时
        f1 = Fraction {numerator, denominator}; // 用提取值更新对象

    return in;
}

int main()
{
    Fraction f1{};
    std::cout << "Enter fraction 1: ";
    std::cin >> f1;

    Fraction f2{};
    std::cout << "Enter fraction 2: ";
    std::cin >> f2;

    std::cout << f1 << " * " << f2 << " is " << f1 * f2 << '\n';
    return 0;
}
```
[下一课 21.5 使用成员函数重载操作符](Chapter-21/lesson21.5-overloading-operators-using-member-functions.md)
[返回主页](/)  
[上一课 21.3 使用普通函数重载操作符](Chapter-21/lesson21.3-overloading-operators-using-normal-functions.md)