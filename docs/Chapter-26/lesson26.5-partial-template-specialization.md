26.5 — 偏特化（partial template specialization）
=======================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")

2008年8月17日 下午6:59（太平洋夏令时）  
2024年3月16日

本课与下一课是面向希望深入理解C++模板的选读内容。偏特化（partial template specialization）使用频率不高（但在特定场景下非常有用）。

在课程[26.2 — 模板非类型参数](Chapter-26/lesson26.2-template-non-type-parameters.md)中，我们学习了如何用表达式参数（expression parameters）参数化模板类。

回顾之前示例中的静态数组（Static Array）类：

```cpp
template <typename T, int size> // size是表达式参数
class StaticArray
{
private:
    // 表达式参数控制数组大小
    T m_array[size]{};
 
public:
    T* getArray() { return m_array; }
	
    const T& operator[](int index) const { return m_array[index]; }
    T& operator[](int index) { return m_array[index]; }
};
```

此类接收两个模板参数：一个类型参数和一个表达式参数。

现假设需编写打印整个数组的函数。虽然可将其实现为成员函数，但作为非成员函数更便于后续示例演示。

使用模板可这样实现：

```cpp
template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
    for (int count{ 0 }; count < size; ++count)
        std::cout << array[count] << ' ';
}
```

使用示例：

```cpp
#include <iostream>

template <typename T, int size> // size是模板非类型参数
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

int main()
{
	// 声明int数组
	StaticArray<int, 4> int4{};
	int4[0] = 0;
	int4[1] = 1;
	int4[2] = 2;
	int4[3] = 3;

	// 打印数组
	print(int4);

	return 0;
}
```

输出结果：

```
0 1 2 3
```

此方案存在设计缺陷。考虑以下场景：

```cpp
#include <algorithm>
#include <iostream>
#include <string_view>

int main()
{
    // 声明char数组
    StaticArray<char, 14> char14{};

    // 复制数据
    constexpr std::string_view hello{ "Hello, world!" };
    std::copy_n(hello.begin(), hello.size(), char14.getArray());

    // 打印数组
    print(char14);

    return 0;
}
```

（关于std::strcpy的复习请参考课程[17.10 — C风格字符串](Chapter-17/lesson17.10-c-style-strings.md)）

此程序编译运行后将输出类似结果：

```
H e l l o ,   w o r l d !
```

对非char类型，元素间添加空格合理（避免粘连）。但char类型需作为C风格字符串连续打印，而当前print()函数未满足此需求。

如何解决？

### 模板特化可行吗？

可能首先考虑模板特化（template specialization）。但全特化（full template specialization）要求显式指定所有模板参数。

考虑：

```cpp
#include <algorithm>
#include <iostream>
#include <string_view>

template <typename T, int size>
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

// 为全特化的StaticArray<char, 14>重载print()
template <>
void print(const StaticArray<char, 14>& array)
{
	for (int count{ 0 }; count < 14; ++count)
		std::cout << array[count];
}

int main()
{
    StaticArray<char, 14> char14{};
    constexpr std::string_view hello{ "Hello, world!" };
    std::copy_n(hello.begin(), hello.size(), char14.getArray());
    print(char14);
    return 0;
}
```

此处为全特化的`StaticArray<char, 14>`提供了重载print函数。输出符合预期：

```
Hello, world!
```

但此方案引发新问题：全特化要求显式指定数组长度！考虑以下示例：

```cpp
int main()
{
    StaticArray<char, 12> char12{};
    constexpr std::string_view hello{ "Hello, mom!" };
    std::copy_n(hello.begin(), hello.size(), char12.getArray());
    print(char12); // 调用通用版本
    return 0;
}
```

`char12`将调用通用print()，因为重载print()仅支持`StaticArray<char, 14>`。

若需支持长度5或22的数组，则需为每个尺寸复制函数，造成代码冗余。显然全特化限制过大，此时需偏特化（partial template specialization）。

### 偏特化（partial template specialization）

偏特化允许对类（非函数！）进行部分模板参数显式指定的特化。针对上述需求，理想方案是重载print函数支持char类型的StaticArray，同时保留长度参数为模板化。偏特化可实现此目标：

```cpp
// 为偏特化的StaticArray<char, size>重载print()
template <int size> // size仍是非类型模板参数
void print(const StaticArray<char, size>& array) // 显式指定char类型
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count];
}
```

此函数显式声明仅适用于char类型的StaticArray，size仍为模板化表达式参数，故支持任意长度的char数组。

完整程序示例：

```cpp
#include <algorithm>
#include <iostream>
#include <string_view>

template <typename T, int size>
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

// 偏特化版本
template <int size>
void print(const StaticArray<char, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count];
}

int main()
{
	StaticArray<char, 14> char14{};
	constexpr std::string_view hello14{ "Hello, world!" };
	std::copy_n(hello14.begin(), hello14.size(), char14.getArray());
	print(char14);

	std::cout << ' ';

	StaticArray<char, 12> char12{};
	constexpr std::string_view hello12{ "Hello, mom!" };
	std::copy_n(hello12.begin(), hello12.size(), char12.getArray());
	print(char12);

	return 0;
}
```

输出结果：

```
Hello, world! Hello, mom!
```

偏特化仅适用于类，不适用于模板函数（函数必须全特化）。此例中`void print(StaticArray<char, size> &array)`能工作是因为它是重载模板函数（形参使用了偏特化的类类型）。

### 成员函数的偏特化

函数的偏特化限制在处理成员函数时会带来挑战。例如若StaticArray定义如下：

```cpp
template <typename T, int size>
class StaticArray
{
private:
    T m_array[size]{};
 
public:
    T* getArray() { return m_array; }
	
    const T& operator[](int index) const { return m_array[index]; }
    T& operator[](int index) { return m_array[index]; }

    void print() const;
};

template <typename T, int size> 
void StaticArray<T, size>::print() const
{
    for (int i{ 0 }; i < size; ++i)
        std::cout << m_array[i] << ' ';
    std::cout << '\n';
}
```

print()现为`StaticArray<T, int>`的成员函数。如何对其偏特化以实现不同行为？可能尝试：

```cpp
// 无效！函数不能偏特化
template <int size>
void StaticArray<double, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << std::scientific << m_array[i] << ' ';
	std::cout << '\n';
}
```

此操作被禁止，因尝试偏特化函数。

### 解决方案

可行方案是对整个类进行偏特化：

```cpp
#include <iostream>

template <typename T, int size>
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }

	void print() const;
};

template <typename T, int size> 
void StaticArray<T, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << m_array[i] << ' ';
	std::cout << '\n';
}

// 偏特化的类
template <int size>
class StaticArray<double, size>
{
private:
	double m_array[size]{};

public:
	double* getArray() { return m_array; }

	const double& operator[](int index) const { return m_array[index]; }
	double& operator[](int index) { return m_array[index]; }

	void print() const;
};

// 偏特化类的成员函数
template <int size>
void StaticArray<double, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << std::scientific << m_array[i] << ' ';
	std::cout << '\n';
}

int main()
{
	// 声明容纳6个int的数组
	StaticArray<int, 6> intArray{};
	for (int count{ 0 }; count < 6; ++count)
		intArray[count] = count;
	intArray.print();

	// 声明容纳4个double的数组
	StaticArray<double, 4> doubleArray{};
	for (int count{ 0 }; count < 4; ++count)
		doubleArray[count] = (4.0 + 0.1 * count);
	doubleArray.print();

	return 0;
}
```

输出：

```
0 1 2 3 4 5
4.000000e+00 4.100000e+00 4.200000e+00 4.300000e+00
```

此方案有效，因为`StaticArray<double, size>::print()`不再是偏特化函数——它是偏特化类`StaticArray<double, size>`的非特化成员。

但此方案导致大量代码从`StaticArray<T, size>`复制到`StaticArray<double, size>`。若能在`StaticArray<double, size>`中复用`StaticArray<T, size>`的代码将更理想。此时需继承机制（inheritance）。

可能尝试如下写法：

```cpp
template <int size>
class StaticArray<double, size>: public StaticArray<T, size> // 错误！未定义T
```

此写法无效，因使用了未定义的`T`。无语法支持此类继承。

### 替代方案

通过公共基类（common base class）实现：

```cpp
#include <iostream>

template <typename T, int size>
class StaticArray_Base
{
protected:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }

	void print() const
	{
		for (int i{ 0 }; i < size; ++i)
			std::cout << m_array[i] << ' ';
		std::cout << '\n';
	}
	// 若使用虚函数解析需虚析构函数
};

template <typename T, int size>
class StaticArray: public StaticArray_Base<T, size>
{
};

template <int size>
class StaticArray<double, size>: public StaticArray_Base<double, size>
{
public:
	void print() const
	{
		for (int i{ 0 }; i < size; ++i)
			std::cout << std::scientific << this->m_array[i] << ' ';
		// 注意：this->前缀必需
		// 原因参考：https://stackoverflow.com/a/6592617
		std::cout << '\n';
	}
};

int main()
{
	StaticArray<int, 6> intArray{};
	for (int count{ 0 }; count < 6; ++count)
		intArray[count] = count;
	intArray.print();

	StaticArray<double, 4> doubleArray{};
	for (int count{ 0 }; count < 4; ++count)
		doubleArray[count] = (4.0 + 0.1 * count);
	doubleArray.print();

	return 0;
}
```

输出同上，但显著减少代码重复。

[下一课 26.6 — 指针的偏特化](Chapter-26/lesson26.6-partial-template-specialization-for-pointers.md)  
[返回主页](/)  
[上一课 26.4 — 类模板特化](Chapter-26/lesson26.4-class-template-specialization.md)