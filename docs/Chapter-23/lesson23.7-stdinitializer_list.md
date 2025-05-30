23.7 — std::initializer_list（初始化列表）
==========================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2017年3月9日，太平洋标准时间下午6:32  
2024年6月5日更新  

考虑C++中的整型固定数组：
```
int array[5];
```
若要通过初始化列表语法直接初始化数组值，可以这样做：
```
#include <iostream>

int main()
{
	int array[] { 5, 4, 3, 2, 1 }; // 初始化列表
	for (auto i : array)
		std::cout << i << ' ';

	return 0;
}
```
输出结果：
```
5 4 3 2 1

```
此语法同样适用于动态分配数组：
```
#include <iostream>

int main()
{
	auto* array{ new int[5]{ 5, 4, 3, 2, 1 } }; // 初始化列表
	for (int count{ 0 }; count < 5; ++count)
		std::cout << array[count] << ' ';
	delete[] array;

	return 0;
}
```
在先前课程中介绍的IntArray容器类示例：
```
#include <cassert> // for assert()
#include <iostream>
 
class IntArray
{
private:
    int m_length{};
    int* m_data{};
 
public:
    IntArray() = default;
 
    IntArray(int length)
        : m_length{ length }
	, m_data{ new int[static_cast<std::size_t>(length)] {} }
    {
    }
 
    ~IntArray()
    {
        delete[] m_data;
    }
 
    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }
 
    int getLength() const { return m_length; }
};

int main()
{
	IntArray array { 5, 4, 3, 2, 1 }; // 编译失败
	for (int count{ 0 }; count < 5; ++count)
		std::cout << array[count] << ' ';

	return 0;
}
```
由于缺少处理初始化列表的构造函数，此代码无法编译，只能单独初始化数组元素：
```
int main()
{
	IntArray array(5);
	array[0] = 5;
	array[1] = 4;  // 冗长的手动赋值
	// ...其他元素初始化
}
```

通过std::initializer_list实现类初始化
----------------------------------
编译器遇到初始化列表时会自动将其转换为std::initializer_list对象。通过创建接受该类型参数的构造函数，即可使用初始化列表创建对象。std::initializer_list定义于`<initializer_list>`头文件。

关键特性：
- 需指定元素类型（如`std::initializer_list<int>`）
- 通过size()方法获取元素数量
- 通常按值传递（类似std::string_view的视图特性）

改进后的IntArray类：
```
#include <algorithm> // for std::copy
#include <cassert>
#include <initializer_list>
#include <iostream>

class IntArray
{
private:
	int m_length {};
	int* m_data{};

public:
	IntArray() = default;

	IntArray(int length)
		: m_length{ length }
		, m_data{ new int[static_cast<std::size_t>(length)] {} }
	{
	}

	IntArray(std::initializer_list<int> list) // 列表初始化构造函数
		: IntArray(static_cast<int>(list.size())) // 委托构造
	{
		std::copy(list.begin(), list.end(), m_data);
	}

	~IntArray() { delete[] m_data; }

	// 禁用浅拷贝
	IntArray(const IntArray&) = delete;
	IntArray& operator=(const IntArray& list) = delete;

	int& operator[](int index)
	{
		assert(index >= 0 && index < m_length);
		return m_data[index];
	}

	int getLength() const { return m_length; }
};
```
使用示例：
```
IntArray array{ 5, 4, 3, 2, 1 }; // 成功初始化
```

访问std::initializer_list元素
----------------------------
由于std::initializer_list未提供operator[]，可通过以下方式访问元素：
1. 范围for循环遍历
2. 通过begin()迭代器随机访问：
```
for (std::size_t count{}; count < list.size(); ++count)
{
	m_data[count] = list.begin()[count];
}
```

列表初始化优先级
--------------
列表初始化优先选择列表构造函数：
```
IntArray a1(5);   // 调用IntArray(int)
IntArray a2{ 5 }; // 调用IntArray(std::initializer_list<int>)
```
委托构造函数使用直接初始化避免递归调用：
```
IntArray(std::initializer_list<int> list)
	: IntArray(static_cast<int>(list.size())) // 直接初始化
```

标准容器示例：
```
std::vector<int> array(5); // 5个0
std::vector<int> array{ 5 }; // 单个元素5
```

最佳实践
-------
- 使用大括号初始化调用列表构造函数
- 使用圆括号初始化调用非列表构造函数
- 新增列表构造函数可能导致现有代码行为变更（破坏性修改）

类赋值操作
--------
通过重载赋值运算符实现列表赋值：
```
IntArray& operator=(std::initializer_list<int> list)
{
	if (list.size() != static_cast<std::size_t>(m_length)) {
		delete[] m_data;
		m_length = static_cast<int>(list.size());
		m_data = new int[list.size()]{};
	}
	std::copy(list.begin(), list.end(), m_data);
	return *this;
}
```
需注意深浅拷贝问题，避免悬垂指针。

测验解答
-------
实现列表赋值运算符后，以下代码应正确运行：
```
IntArray array { 5, 4, 3, 2, 1 };
array = { 1, 3, 5, 7, 9, 11 }; // 调用重载赋值运算符
```

总结
----
通过实现std::initializer_list构造函数和赋值运算符，可使自定义类支持列表初始化和赋值。注意维护深拷贝语义以避免内存问题。

[下一课 23.x 第23章总结与测验](Chapter-23/lesson23.x-chapter-23-summary-and-quiz.md)  
[返回主页](/)  
[上一课 23.6 容器类](Chapter-23/lesson23.6-container-classes.md)