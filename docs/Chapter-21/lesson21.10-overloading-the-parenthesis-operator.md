21.10 — 重载括号运算符（parenthesis operator）
=============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年10月25日（首次发布于2024年11月14日）  

迄今为止所见的重载运算符都允许定义参数类型，但参数数量固定（由运算符类型决定）。例如operator==总是接受两个参数，而operator!仅接受一个。括号运算符（operator()）的特殊之处在于允许改变参数类型和数量。  

需注意两点：  
1. 括号运算符必须作为成员函数（member function）实现  
2. 在非面向对象的C++中，()运算符用于调用函数。在类语境下，operator()只是普通运算符，像其他重载运算符一样调用名为operator()的函数  

示例  
----------------  

以下示例展示适合重载此运算符的场景：  
```cpp
class Matrix
{
private:
    double data[4][4]{};
};
```  

矩阵（Matrix）是线性代数（linear algebra）的核心组件，常用于几何建模和3D计算机图形学。本例中只需理解Matrix类是4x4的双精度二维数组。  

在[重载下标运算符](98-overloading-the-subscript-operator/)课程中，我们学习了通过重载operator[]直接访问一维私有数组。但对于二维数组，C++23之前的operator[]仅支持单个参数，无法直接索引二维数组。  

由于()运算符可接受任意数量参数，我们可以声明接收两个整型索引参数的operator()来访问二维数组：  
```cpp
#include <cassert> // 用于assert()

class Matrix
{
private:
    double m_data[4][4]{};

public:
    double& operator()(int row, int col);
    double operator()(int row, int col) const; // 用于const对象
};

double& Matrix::operator()(int row, int col)
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}

double Matrix::operator()(int row, int col) const
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}
```  

现在可以声明Matrix对象并访问元素：  
```cpp
#include <iostream>

int main()
{
    Matrix matrix;
    matrix(1, 2) = 4.5;
    std::cout << matrix(1, 2) << '\n';

    return 0;
}
```  
输出结果：  
```
4.5
```  

接下来重载无参数的()运算符：  
```cpp
#include <cassert> // 用于assert()
class Matrix
{
private:
    double m_data[4][4]{};

public:
    double& operator()(int row, int col);
    double operator()(int row, int col) const;
    void operator()();
};

void Matrix::operator()()
{
    // 重置矩阵所有元素为0.0
    for (int row{ 0 }; row < 4; ++row)
    {
        for (int col{ 0 }; col < 4; ++col)
        {
            m_data[row][col] = 0.0;
        }
    }
}
```  

使用示例：  
```cpp
#include <iostream>

int main()
{
    Matrix matrix{};
    matrix(1, 2) = 4.5;
    matrix(); // 清空矩阵
    std::cout << matrix(1, 2) << '\n';

    return 0;
}
```  
输出结果：  
```
0
```  

由于()运算符的灵活性，可能被滥用于不同目的。但应避免这种做法，因为()符号无法直观表明操作意图。例如将清空功能命名为clear()或erase()（如matrix.erase()）比matrix()更易理解。  

> **注意**：C++23起支持operator[]多索引，其功能与上述operator()相同  

函数对象（functor）的应用  
----------------  

operator()常被重载用于实现**函数对象（functor）**——行为类似函数的类。相比普通函数，函数对象的优势在于可通过成员变量（member variable）存储数据。  

简单函数对象示例：  
```cpp
#include <iostream>

class Accumulator
{
private:
    int m_counter{ 0 };

public:
    int operator() (int i) { return (m_counter += i); }

    void reset() { m_counter = 0; } // 可选功能
};

int main()
{
    Accumulator acc{};
    std::cout << acc(1) << '\n'; // 输出1
    std::cout << acc(3) << '\n'; // 输出4

    Accumulator acc2{};
    std::cout << acc2(10) << '\n'; // 输出10
    std::cout << acc2(20) << '\n'; // 输出30
    
    return 0;
}
```  

注意，使用Accumulator实例就像进行普通函数调用，但该对象能存储累加值。函数对象的优势在于可同时实例化多个独立对象，还能包含其他便利成员函数（如reset()）。  

总结  
----------------  

operator()通常通过两个参数重载用于：  
- 索引多维数组  
- 获取一维数组子集（参数定义返回范围）  

其他用途建议改用描述性名称的成员函数。operator()也常用于创建函数对象。虽然简单函数对象（如上例）易于理解，但其通常用于高级编程主题，值得专门课程讲解。  

测验时间  
----------------  

**问题1**  
编写MyString类，包含std::string成员。重载operator<<输出字符串，重载operator()返回从第一个参数索引开始的子串（作为MyString），子串长度由第二个参数定义。  

以下代码应能运行：  
```cpp
int main()
{
    MyString s { "Hello, world!" };
    std::cout << s(7, 5) << '\n'; // 从索引7开始返回5个字符

    return 0;
}
```  
应输出：  
```
world
```  
提示：使用[`std::string::substr`](https://en.cppreference.com/w/cpp/string/basic_string/substr)获取子串。  

  
```cpp
#include <cassert>
#include <iostream>
#include <string>
#include <string_view>

class MyString
{
private:
	std::string m_string{};

public:
	MyString(std::string_view string = {})
		:m_string{ string }
	{
	}

	MyString operator()(int start, int length)
	{
		assert(start >= 0);
		assert(start + length <= static_cast<int>(m_string.length()) && "MyString::operator(int, int): 子串越界");

		return MyString { m_string.substr(
			static_cast<std::string::size_type>(start),
			static_cast<std::string::size_type>(length)
			)};
	}

	friend std::ostream& operator<<(std::ostream& out, const MyString& s)
	{
		out << s.m_string;

		return out;
	}
};

int main()
{
	MyString s{ "Hello, world!" };
	std::cout << s(7, 5) << '\n';

	return 0;
}
```  

**问题2（附加题）**  
\> 步骤1  
为何上述实现在不需要修改返回子串时效率低下？  
  
operator()中，std::string::substr返回std::string，意味着每次调用都会复制源字符串的部分内容。重载的operator()用其构造新MyString（包含std::string成员），产生二次复制。返回MyString给调用方时产生第三次复制。编译器可能优化部分复制，但至少保留一个包含子串的std::string。  

\> 步骤2  
如何改进？  
  
使用std::string_view可查看子串而无需复制。若operator()返回std::string_view，调用方可直接使用该视图，或在需要修改/持久化时转换为std::string或MyString。  

\> 步骤3  
修改operator()以返回std::string_view：  
  
```cpp
#include <cassert>
#include <iostream>
#include <string>
#include <string_view>

class MyString
{
private:
	std::string m_string{};

public:
	MyString(std::string_view string = {})
		:m_string{ string }
	{
	}

	std::string_view operator()(int start, int length)
	{
		assert(start >= 0);
		assert(start + length <= static_cast<int>(m_string.length()) && "MyString::operator(int, int): 子串越界");

		// 创建m_string的视图以使用std::string_view::substr()
		return std::string_view{ m_string }.substr(
			static_cast<std::string_view::size_type>(start),
			static_cast<std::string_view::size_type>(length)
		);
	}

	friend std::ostream& operator<<(std::ostream& out, const MyString& s)
	{
		out << s.m_string;

		return out;
	}
};

int main()
{
	MyString s{ "Hello, world!" };
	std::cout << s(7, 5) << '\n';

	return 0;
}
```  
解析`return std::string_view{ m_string }.substr();`：首先创建m_string的临时std::string_view（低成本操作），接着调用std::string_view::substr获取子串视图（不包含空终止符）。返回的视图仍指向m_string（仍在作用域内），因此不会产生悬挂指针（dangling pointer）。最终创建3个std::string_view而非3个std::string，效率更高。  

[下一课 21.11 重载类型转换](Chapter-21/lesson21.11-overloading-typecasts.md)  
[返回主页](/)  
[上一课 21.9 重载下标运算符](Chapter-21/lesson21.9-overloading-the-subscript-operator.md)