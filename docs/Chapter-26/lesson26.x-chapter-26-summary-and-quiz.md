26.x — 第26章 小结与测验
===================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年12月19日，下午2:07（首次发布于2023年9月11日）  

模板（template）允许我们使用占位符类型编写函数或类，从而通过不同类型生成相同版本的函数或类。被实例化（instantiated）的函数或类称为函数实例（function instance）或类实例（class instance）。

所有模板函数或类必须以模板参数声明（template parameter declaration）开头，告知编译器后续内容属于模板。在模板参数声明中，需指定模板类型参数（template type parameters）或表达式参数（expression parameters）。模板类型参数是占位符类型，通常命名为T、T1、T2等单字母形式。表达式参数通常是整型，但也可以是指向函数、类对象或成员函数的指针或引用。

模板类定义与成员函数定义的分离方式与普通类不同——不能将类定义放在头文件而成员函数定义放在.cpp文件中。通常最佳做法是将所有内容保留在头文件中，成员函数定义置于类下方。

当需要为特定类型覆盖模板函数或类的默认行为时，可使用模板特化（template specialization）。若所有类型都被覆盖，称为全特化（full specialization）。类还支持部分特化（partial specialization），即仅特化部分模板参数。函数不能进行部分特化。

C++标准库中的许多类使用模板，包括std::array和std::vector。模板常用于实现容器类（container classes），因此容器只需编写一次即可适用于任何合适类型。

测验时间
----------------

**问题1**  
有时需要定义成对数据。编写名为Pair1的模板类，允许用户定义一个模板类型用于配对中的两个值。以下函数应正常工作：

```cpp
int main()
{
	Pair1<int> p1 { 5, 8 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair1<double> p2 { 2.3, 4.5 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
```

并输出：

```
Pair: 5 8
Pair: 2.3 4.5
```

  
<details><summary>答案</summary>

```cpp
#include <iostream>

template <typename T>
class Pair1
{
private:
	T m_x {};
	T m_y {};

public:
	Pair1(const T& x, const T& y)
		: m_x{ x }, m_y{ y }
	{
	}

	T& first() { return m_x; }
	T& second() { return m_y; }
	const T& first() const { return m_x; }
	const T& second() const { return m_y; }
};

int main()
{
	Pair1<int> p1 { 5, 8 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair1<double> p2 { 2.3, 4.5 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
```
</details>

**问题2**  
编写Pair类，允许为配对中的两个值指定不同类型。

注意：由于C++目前不允许仅模板参数数量或类型不同的"重载"类，故需采用不同类名。

以下程序应正常工作：

```cpp
int main()
{
	Pair<int, double> p1 { 5, 6.7 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair<double, int> p2 { 2.3, 4 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
```

并输出：

```
Pair: 5 6.7
Pair: 2.3 4
```

  
<details><summary>答案</summary>

```cpp
#include <iostream>

template <typename T, typename S>
class Pair
{
private:
	T m_x;
	S m_y;

public:
	Pair(const T& x, const S& y)
		: m_x{x}, m_y{y}
	{
	}

	T& first() { return m_x; }
	S& second() { return m_y; }
	const T& first() const { return m_x; }
	const S& second() const { return m_y; }
};

int main()
{
	Pair<int, double> p1 { 5, 6.7 };
	std::cout << "Pair: " << p1.first() << ' ' << p1.second() << '\n';

	const Pair<double, int> p2 { 2.3, 4 };
	std::cout << "Pair: " << p2.first() << ' ' << p2.second() << '\n';

	return 0;
}
```
</details>

**问题3**  
字符串-值配对（string-value pair）是一种特殊配对类型，第一个值始终为字符串类型，第二个值可为任意类型。编写名为StringValuePair的模板类，继承自部分特化的Pair类（使用std::string作为第一个类型，允许用户指定第二个类型）。

以下程序应运行：

```cpp
int main()
{
	StringValuePair<int> svp { "Hello", 5 };
	std::cout << "Pair: " << svp.first() << ' ' << svp.second() << '\n';

	return 0;
}
```

并输出：

```
Pair: Hello 5
```

  
<details><summary>答案</summary>

```cpp
#include <iostream>
#include <string>
#include <string_view>

template <typename T, typename S>
class Pair
{
private:
	T m_x{};
	S m_y{};

public:
	Pair(const T& x, const S& y)
		: m_x{ x }, m_y{ y }
	{
	}

	T& first() { return m_x; }
	S& second() { return m_y; }
	const T& first() const { return m_x; }
	const S& second() const { return m_y; }
};

template <typename S>
class StringValuePair : public Pair<std::string, S>
{
public:
	StringValuePair(std::string_view key, const S& value)
                // std::string_view不会隐式转换为std::string，必须显式转换
		: Pair<std::string, S>{ static_cast<std::string>(key), value }
	{
	}
};

int main()
{
	StringValuePair<int> svp{ "Hello", 5 };
	std::cout << "Pair: " << svp.first() << ' ' << svp.second() << '\n';

	return 0;
}
```
</details>

[下一课 27.1 — 异常处理的必要性](Chapter-27/lesson27.1-the-need-for-exceptions.md)  
[返回主页](/)  
[上一课 26.6 — 指针的部分模板特化](Chapter-26/lesson26.6-partial-template-specialization-for-pointers.md)