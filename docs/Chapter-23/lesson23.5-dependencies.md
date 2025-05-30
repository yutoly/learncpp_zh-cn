23.5 — 依赖关系  
====================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年9月11日（首次发布于2016年8月23日）  

至此我们已经探讨了三种对象关系：组合（composition）、聚合（aggregation）和关联（association）。现在我们将最后讲解最简单的一种关系：依赖（dependency）。  

在日常交流中，我们用"依赖"一词表示某个对象需要依靠另一个对象来完成特定任务。例如：脚部受伤时需要依赖拐杖行走（未受伤时则不需要）；花朵依赖蜜蜂授粉才能结果繁衍（其他情况下则不需要）。  

**依赖关系（dependency）**发生在当一个对象需要调用另一个对象的功能来完成特定任务时。这种关系比关联（association）更弱，但被依赖对象的任何修改仍可能破坏调用方（依赖者）的功能。依赖关系始终是单向的。  

您已多次接触依赖关系的典型例子是`std::ostream`。我们使用`std::ostream`的类需要通过它来完成控制台输出任务，除此之外并无其他关联。  

示例代码：  
```cpp
#include <iostream>
 
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0): m_x{x}, m_y{y}, m_z{z}
    {
    }
 
    friend std::ostream& operator<< (std::ostream& out, const Point& point); // Point在此处依赖std::ostream
};
 
std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // 由于operator<<是Point的友元函数，可直接访问其成员
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';
 
    return out;
}
 
int main()
{
    Point point1 { 2.0, 3.0, 4.0 };
 
    std::cout << point1; // 程序在此处依赖std::cout
 
    return 0;
}
```  

上述代码中，`Point`类与`std::ostream`没有直接关联，但通过`operator<<`使用`std::ostream`输出到控制台，因此形成了依赖关系。  

**C++中依赖与关联的区别**  
依赖与关联的区分常引起困惑。  

在C++中，关联（association）关系表现为一个类通过成员变量直接或间接"链接"到关联类。例如：`Doctor`类拥有指向其`Patient`对象的指针数组成员；`Driver`类以整型成员存储其拥有的`Car`对象ID。关联方始终知晓被关联对象的信息。  

依赖关系通常不涉及成员变量。被依赖对象往往在需要时实例化（如打开文件写入数据），或作为函数参数传递（如上述重载`operator<<`中的`std::ostream`）。  

**趣味时间**  
关于依赖关系的幽默漫画（来自[xkcd](https://xkcd.com/754/)）：  

![](https://imgs.xkcd.com/comics/dependencies.png)  

当然，我们知道这实际上是一个自反关联（reflexive association）！  

[下一课 23.6 — 容器类](Chapter-23/lesson23.6-container-classes.md)  
[返回主页](/)  
[上一课 23.4 — 关联](Chapter-23/lesson23.4-association.md)