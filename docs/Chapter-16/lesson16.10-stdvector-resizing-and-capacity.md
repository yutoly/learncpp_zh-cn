16.10 — std::vector 的调整大小与容量  
==========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年1月10日（首次发布于2015年11月24日）  

本章前几课介绍了容器（container）、数组（array）和`std::vector`，讨论了数组元素访问、长度获取及遍历等主题。虽然示例中使用`std::vector`，但所述概念普遍适用于所有数组类型。

本章剩余课程将重点讨论`std::vector`与其他数组类型的主要区别：实例化后调整自身大小的能力。

固定大小数组 vs 动态数组  
----------------

多数数组类型存在重大限制：实例化时必须已知数组长度且不可更改，称为**固定大小数组（fixed-size array）**或**固定长度数组（fixed-length array）**。`std::array`和`C风格数组`均属此类，下章将详细讨论。

`std::vector`则是**动态数组（dynamic array）**，即可在实例化后改变大小的**可调整大小数组（resizable array）**。这种调整能力是其核心特性。

运行时调整`std::vector`大小  
----------------

通过调用`resize()`成员函数并指定新长度，可在运行时调整`std::vector`：

```cpp
#include <iostream>
#include <vector>

int main()
{
    std::vector v{ 0, 1, 2 }; // 创建包含3个元素的vector
    std::cout << "长度：" << v.size() << '\n';

    v.resize(5);              // 调整为5个元素
    std::cout << "长度：" << v.size() << '\n';

    for (auto i : v)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
```

输出：
```
长度：3
长度：5
0 1 2 0 0
```

注意两点：首先调整后现有元素值保留；其次新元素进行值初始化（类类型默认初始化，其他类型零初始化），故新增的`int`型元素初始化为`0`。

也可缩小vector：

```cpp
#include <iostream>
#include <vector>

void printLength(const std::vector<int>& v)
{
	std::cout << "长度：" << v.size() << '\n';
}

int main()
{
    std::vector v{ 0, 1, 2, 3, 4 }; // 初始长度5
    printLength(v);

    v.resize(3);                    // 调整为3个元素
    printLength(v);

    for (int i : v)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
```

输出：
```
长度：5
长度：3
0 1 2
```

`std::vector`的长度与容量  
----------------

假设有12栋联排房屋，其数量（长度）为12。若需知当前有人居住的房屋，需另行确认。仅有长度时，仅知存在多少事物。

考虑装5个鸡蛋的蛋盒，当前数量（长度）为5，但盒子的**容量（capacity）**为12。此时长度与容量分离：长度是当前使用量，容量是总承载量。

对于`std::vector`，**容量（capacity）**指已分配存储的元素总数，**长度（length）**（即`size()`）指当前使用中的元素数。容量为5的vector已为5个元素分配空间，若实际使用2个，则长度2，剩余3个已分配但未使用。

获取`std::vector`容量  
----------------

通过`capacity()`成员函数获取容量：

```cpp
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "容量：" << v.capacity() << " 长度：" << v.size() << '\n';
}

int main()
{
    std::vector v{ 0, 1, 2 }; // 初始长度3
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    v.resize(5); // 调整为5个元素
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
```

作者机器输出：
```
容量：3 长度：3
0 1 2 
容量：5 长度：5
0 1 2 0 0 
```

初始化时vector分配3元素容量，全部使用（长度3）。调用`resize(5)`后需扩容，完成调整后容量5，长度5。

存储重分配及其开销  
----------------

当`std::vector`调整存储空间时，发生**重分配（reallocation）**，流程如下：

1. 申请新内存并值初始化元素
2. 将旧内存元素复制（或移动）至新内存，释放旧内存
3. 更新vector容量与长度

表面是调整大小，实际是内存与元素的整体替换！

> **相关内容**  
> 运行时申请新内存称为动态内存分配，详见课程[19.1 — new与delete动态内存分配](Chapter-19/lesson19.1-dynamic-memory-allocation-with-new-and-delete.md)。

因重分配需复制所有元素，开销巨大，应尽量避免。

> **关键洞察**  
> 重分配代价高昂，需避免不必要的操作。

区分长度与容量的意义  
----------------

若仅跟踪长度，每次`resize()`都会触发重分配。分离长度与容量使`std::vector`能智能处理重分配需求。

示例：
```cpp
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "容量：" << v.capacity() << " 长度：" << v.size() << '\n';
}

int main()
{
    // 创建长度5的vector
    std::vector v{ 0, 1, 2, 3, 4 };
    v = { 0, 1, 2, 3, 4 }; // 数组长度5
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // 调整至3元素
    v.resize(3); // 也可赋值含3元素的列表
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // 调回5元素
    v.resize(5);
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
```

输出：
```
容量：5 长度：5
0 1 2 3 4 
容量：5 长度：3
0 1 2 
容量：5 长度：5
0 1 2 0 0 
```

初始容量5，长度5。调用`resize(3)`后长度3，容量仍5，未重分配。再次`resize(5)`时容量足够，无需重分配，仅重置长度并初始化新增元素。

> **关键洞察**  
> 分离容量与长度可避免部分重分配操作。

vector索引基于长度而非容量  
----------------

下标运算符（`operator[]`）和`at()`成员函数的有效索引基于长度而非容量。当容量5、长度3时，仅索引0-2有效，超出长度即越界。

> **警告**  
> 有效下标范围是0至长度（非容量）减一！

收缩`std::vector`  
----------------

增大vector会改变长度，必要时扩容。但缩小vector仅减长度，容量不变。若需回收不再需要的大量元素内存，可调用`shrink_to_fit()`成员函数请求收缩容量至当前长度。该请求无约束力，实现可自由处理。

示例：
```cpp
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "容量：" << v.capacity() << " 长度：" << v.size() << '\n';
}

int main()
{
	std::vector<int> v(1000); // 分配1000元素空间
	printCapLen(v);

	v.resize(0); // 调整至0元素
	printCapLen(v);

	v.shrink_to_fit();
	printCapLen(v);

	return 0;
}
```

作者机器输出：
```
容量：1000 长度：1000
容量：1000 长度：0
容量：0 长度：0
```

调用`shrink_to_fit()`后，容量归零，释放1000元素内存。

测验时间  
----------------

**问题1**  
vector的长度与容量分别代表什么？  
  
<details><summary>答案</summary>长度是当前使用中的元素数，容量是已分配存储的元素总数。</details>  

**问题2**  
为何区分长度与容量？  
  
<details><summary>答案</summary>避免长度变化时的部分重分配操作。</details>  

**问题3**  
`std::vector`的有效索引基于长度还是容量？  
  
<details><summary>答案</summary>长度。</details>  

[下一课 16.11 — std::vector与栈行为](Chapter-16/lesson16.11-stdvector-and-stack-behavior.md)  
[返回主页](/)  
[上一课 16.9 — 使用枚举器进行数组索引与长度计算](Chapter-16/lesson16.9-array-indexing-and-length-using-enumerators.md)