21.2 — STL容器概览  
===============================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2011年9月11日 下午3:41（首次发布）  
2021年9月19日更新  

迄今为止，STL库中最常用的功能是STL容器类。如需快速复习容器类概念，请参考课程[23.6 — 容器类](Chapter-23/lesson23.6-container-classes.md)。  

STL包含多种适用于不同场景的容器类。总体上，容器类可分为三大基本类别：序列容器（sequence container）、关联容器（associative container）和容器适配器（container adapter）。本节将简要概述各类容器。  

**序列容器**  
序列容器是保持元素顺序的容器类，其核心特征是可以选择插入元素的位置。最常见的序列容器示例是数组：若向数组插入四个元素，元素将严格保持插入顺序。  

自C++11起，STL包含6种序列容器：std::vector（向量）、std::deque（双端队列）、std::array（数组）、std::list（链表）、std::forward_list（前向链表）和std::basic_string（基础字符串）。  

* 学过物理的读者可能认为向量（vector）是具有大小和方向的实体。STL中**向量（vector）**类实际上是动态数组，可随元素增加自动扩展。通过operator[]运算符可随机访问元素，在向量末尾插入和删除元素通常效率较高。  

以下程序向向量插入6个数字，并使用重载的[]运算符访问元素进行打印：  
```cpp
#include <vector>
#include <iostream>

int main()
{
    std::vector<int> vect;
    for (int count=0; count < 6; ++count)
        vect.push_back(10 - count); // 在数组末尾插入

    for (int index=0; index < vect.size(); ++index)
        std::cout << vect[index] << ' ';

    std::cout << '\n';
}
```  
程序输出结果：  
10 9 8 7 6 5  

* **双端队列（deque）**类（发音同"deck"）实现为可从两端扩展的动态数组：  
```cpp
#include <iostream>
#include <deque>

int main()
{
    std::deque<int> deq;
    for (int count=0; count < 3; ++count)
    {
        deq.push_back(count); // 在数组末尾插入
        deq.push_front(10 - count); // 在数组前端插入
    }

    for (int index=0; index < deq.size(); ++index)
        std::cout << deq[index] << ' ';

    std::cout << '\n';
}
```  
程序输出结果：  
8 9 10 0 1 2  

* **链表（list）**是一种特殊的序列容器，称为双向链表。每个元素包含指向前后元素的指针。链表仅提供首尾访问能力，不支持随机访问。若需查找中间元素，必须从一端开始遍历。链表的优势在于已知插入位置时插入效率极高，通常使用迭代器（iterator）进行遍历。我们将在后续课程深入讨论链表和迭代器。  

* 虽然STL**字符串（string）**（及wstring）类通常不被归类为序列容器，但其本质上可视为元素类型为char（或wchar）的向量。  

**关联容器**  
关联容器在插入元素时自动进行排序，默认使用operator<进行元素比较。  

* **集合（set）**存储唯一元素，禁止重复。元素按值排序。  
* **多重集合（multiset）**允许重复元素的集合。  
* **映射（map）**（亦称关联数组）存储键值对（key/value pair），键用于排序和索引且必须唯一，值存储实际数据。  
* **多重映射（multimap）**（亦称字典）允许重复键。现实字典即为多重映射：键是单词，值是对应释义。所有按键升序排列，可通过键查找值。某些单词有多个释义，故字典属于多重映射而非普通映射。  

**容器适配器**  
容器适配器是为特定用途定制的预定义容器，其特点是可以选择底层序列容器类型。  

* **栈（stack）**遵循LIFO（后进先出）原则，元素从容器末尾插入（push）和移除（pop）。默认使用双端队列作为底层容器（尽管向量似乎更自然），也可选择向量或链表。  
* **队列（queue）**遵循FIFO（先进先出）原则，元素插入（push）至末尾，移除（pop）自前端。默认使用双端队列，也可选择链表。  
* **优先队列（priority queue）**是保持元素排序（通过operator<）的特殊队列。元素插入时自动排序，从前端移除元素将返回优先级最高的项。  

[下一课 21.3 — STL迭代器概览](Appendix-D/lesson21.3-stl-iterators-overview.md)  
[返回主页](/)  
[上一课 21.1 — 标准库](Appendix-D/lesson21.1-the-standard-library.md)