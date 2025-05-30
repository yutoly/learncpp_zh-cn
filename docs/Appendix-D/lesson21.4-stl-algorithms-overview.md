21.4 — STL算法概述  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2011年9月11日下午3:45（太平洋夏令时）  
最后更新于2021年10月21日  

 

STL除容器类（container classes）和迭代器（iterators）外，还提供了大量用于操作容器元素的**泛型算法（generic algorithms）**。这些算法可实现元素搜索、排序、插入、重排、删除及拷贝等功能。


需注意，这些算法通过迭代器操作实现为函数。这种设计使得每个算法只需实现一次，即可自动适用于所有提供迭代器的容器（包括自定义容器类）。虽然这种机制功能强大且能快速编写复杂代码，但也存在潜在风险：某些算法与容器类型的组合可能无法运行、导致死循环，或性能极差。因此使用时需谨慎。


STL提供大量算法——本章仅介绍部分常用且易用的算法，完整内容将在STL算法专题章节详述。


使用STL算法时需包含算法头文件：


**min_element与max_element**  
`std::min_element`和`std::max_element`算法用于查找容器中的最小与最大元素。`std::iota`用于生成连续序列值。


```cpp
#include <algorithm> // std::min_element与std::max_element
#include <iostream>
#include <list>
#include <numeric> // std::iota

int main()
{
    std::list<int> li(6);
    // 用从0开始的数字填充li
    std::iota(li.begin(), li.end(), 0);

    std::cout << *std::min_element(li.begin(), li.end()) << ' '
              << *std::max_element(li.begin(), li.end()) << '\n';
    
    return 0;
}
```

输出结果：

```
0 5
```

**find（及list::insert）**  
本例使用`std::find()`算法在链表（list）中查找值，并通过`list::insert()`方法在指定位置插入新值。


```cpp
#include <algorithm>
#include <iostream>
#include <list>
#include <numeric>

int main()
{
    std::list<int> li(6);
    std::iota(li.begin(), li.end(), 0);

    // 在链表中查找数值3
    auto it{ std::find(li.begin(), li.end(), 3) };
    
    // 在3之前插入8
    li.insert(it, 8);

    for (int i : li) // 基于迭代器的for循环
        std::cout << i << ' ';
        
    std::cout << '\n';

    return 0;
}
```

输出结果：

```
0 1 2 8 3 4 5
```

当搜索算法未找到目标时，会返回结束迭代器（end iterator）。若不确定链表是否包含3，需在操作返回的迭代器前进行验证：


```cpp
if (it == li.end())
{
  std::cout << "未找到数值3\n";
}
else
{
  // ...
}
```

**sort与reverse**  
本例演示如何对向量（vector）排序并逆序：


```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
    std::vector<int> vect{ 7, -3, 6, 2, -5, 0, 4 };

    // 向量排序
    std::sort(vect.begin(), vect.end());

    for (int i : vect)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    // 向量逆序
    std::reverse(vect.begin(), vect.end());

    for (int i : vect)
    {
        std::cout << i << ' ';
    }
     
    std::cout << '\n';

    return 0;
}
```

输出结果：

```
-5 -3 0 2 4 6 7
7 6 4 2 0 -3 -5
```

也可向`std::sort`传递自定义比较函数。\<functional\>头文件提供多个比较函数，无需自行编写。例如传递`std::greater`可实现从高到低排序，省去`std::reverse`调用：


注意`std::sort()`不适用于链表容器——链表类提供专用的`sort()`成员函数，其效率远高于泛型版本。


**结语**  
本章虽仅浅尝STL算法，但已展示其与迭代器及基础容器类配合使用的便捷性。更多算法内容将在专题章节详解！


[下一课 22.1 — std::string与std::wstring](Appendix-D/lesson22.1-stdstring-and-stdwstring.md)  
[返回主页](/)    
[上一课 21.3 — STL迭代器概述](Appendix-D/lesson21.3-stl-iterators-overview.md)