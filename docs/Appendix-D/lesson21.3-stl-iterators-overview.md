21.3 — STL迭代器（STL iterators）概览  
==============================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2011年9月11日 下午3:44（PDT）  
2023年1月27日更新  

**迭代器（Iterator）**是一种能在不暴露容器实现细节的情况下遍历容器类的对象。对于许多类（尤其是列表和关联容器），迭代器是访问元素的主要方式。

迭代器可理解为指向容器元素的指针，通过一组重载运算符提供标准化操作：

* **运算符\*** —— 解引用迭代器返回当前指向的元素
* **运算符\+\+** —— 将迭代器移动到容器中的下一个元素。多数迭代器还提供`运算符--`用于访问前一个元素
* **运算符\=\= 与 运算符!\=** —— 基础比较运算符，判断两个迭代器是否指向同一元素。要比较迭代器指向的值，需先解引用再进行比较
* **运算符\=** —— 将迭代器赋值为新位置（通常指向容器元素的起始或末尾）。要修改迭代器指向元素的值，需先解引用再赋值

每个容器提供四个基础成员函数配合运算符使用：

* **begin()** 返回指向容器元素起始位置的迭代器
* **end()** 返回指向容器末尾元素后一位置的迭代器
* **cbegin()** 返回只读（const）迭代器指向容器起始
* **cend()** 返回只读（const）迭代器指向容器末尾

`end()`不指向最后一个元素的设计看似奇怪，但主要为简化循环操作：当迭代器到达`end()`时即完成遍历。

所有容器至少提供两种迭代器类型：

* **container::iterator** 可读写迭代器
* **container::const_iterator** 只读迭代器

**遍历vector示例**

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector<int> vect;
    for (int count=0; count < 6; ++count)
        vect.push_back(count);

    std::vector<int>::const_iterator it; // 声明只读迭代器
    it = vect.cbegin(); // 指向vector起始
    while (it != vect.cend()) // 未到达末尾时循环
    {
        std::cout << *it << ' '; // 输出当前元素
        ++it; // 移至下一元素
    }

    std::cout << '\n';
}
```
输出结果：
```
0 1 2 3 4 5
```

**遍历list示例**

```cpp
#include <iostream>
#include <list>

int main()
{
    std::list<int> li;
    for (int count=0; count < 6; ++count)
        li.push_back(count);

    std::list<int>::const_iterator it; // 声明迭代器
    it = li.cbegin(); // 指向list起始
    while (it != li.cend()) // 未到达末尾时循环
    {
        std::cout << *it << ' '; // 输出当前元素
        ++it; // 移至下一元素
    }

    std::cout << '\n';
}
```
输出结果：
```
0 1 2 3 4 5
```

尽管vector与list的内部实现差异显著，但遍历代码几乎完全相同。

**遍历set示例**

```cpp
#include <iostream>
#include <set>

int main()
{
    std::set<int> myset;
    myset.insert(7);
    myset.insert(2);
    myset.insert(-6);
    myset.insert(8);
    myset.insert(1);
    myset.insert(-4);

    std::set<int>::const_iterator it; // 声明迭代器
    it = myset.cbegin(); // 指向set起始
    while (it != myset.cend()) // 未到达末尾时循环
    {
        std::cout << *it << ' '; // 输出当前元素
        ++it; // 移至下一元素
    }

    std::cout << '\n';
}
```
输出结果（自动排序）：
```
-6 -4 1 2 7 8
```

**遍历map示例**

```cpp
#include <iostream>
#include <map>
#include <string>

int main()
{
	std::map<int, std::string> mymap;
	mymap.insert(std::make_pair(4, "apple"));
	mymap.insert(std::make_pair(2, "orange"));
	mymap.insert(std::make_pair(1, "banana"));
	mymap.insert(std::make_pair(3, "grapes"));
	mymap.insert(std::make_pair(6, "mango"));
	mymap.insert(std::make_pair(5, "peach"));

	auto it{ mymap.cbegin() }; // 声明常量迭代器指向起始
	while (it != mymap.cend()) // 未到达末尾时循环
	{
		std::cout << it->first << '=' << it->second << ' '; // 输出键值对
		++it; // 移至下一元素
	}

	std::cout << '\n';
}
```
输出结果（按键排序）：
```
1=banana 2=orange 3=grapes 4=apple 5=peach 6=mango
```

**总结**  
迭代器提供无需了解容器实现即可遍历元素的便捷方式。结合STL算法和容器成员函数，迭代器功能更加强大。后续课程将演示使用迭代器在list中插入元素（list未提供直接访问元素的operator[]）。

注意：迭代器必须按类实现，因其需了解类的内部结构，故始终与特定容器类绑定。

[下一课 21.4 — STL算法概览](Appendix-D/lesson21.4-stl-algorithms-overview.md)  
[返回主页](/)  
[上一课 21.2 — STL容器概览](Appendix-D/lesson21.2-stl-containers-overview.md)