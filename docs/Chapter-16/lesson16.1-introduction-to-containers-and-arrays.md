16.1 — 容器与数组入门  
=============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月13日（首次发布于2023年9月11日）  

变量扩展性挑战  
----------------  

假设需要记录30名学生的考试成绩并计算班级平均分。我们需要定义30个变量：  
```cpp
// 定义30个整型变量（每个都有不同名称）
int testScore1 {};
int testScore2 {};
int testScore3 {};
// ...
int testScore30 {};
```  
这需要定义大量变量！计算班级平均分时需这样操作：  
```cpp
int average { (testScore1 + testScore2 + testScore3 + testScore4 + testScore5
     + testScore6 + testScore7 + testScore8 + testScore9 + testScore10
     + testScore11 + testScore12 + testScore13 + testScore14 + testScore15
     + testScore16 + testScore17 + testScore18 + testScore19 + testScore20
     + testScore21 + testScore22 + testScore23 + testScore24 + testScore25
     + testScore26 + testScore27 + testScore28 + testScore29 + testScore30)
     / 30; };
```  
这不仅需要大量重复输入，还容易拼写错误。若要对这些值进行操作（如输出到屏幕），必须重复输入所有变量名。  

若班级新增学生，需扫描整个代码库手动添加`testScore31`，并面临更新错误风险（例如忘记将除数从30改为31）。对于成百上千的变量，单独定义变量根本无法扩展。  

尝试使用结构体（struct）：  
```cpp
struct testScores
{
// 定义30个整型变量（每个都有不同名称）
int score1 {};
int score2 {};
int score3 {};
// ...
int score30 {};
};
```  
虽然结构体提供了数据组织方式，但核心问题未解决：仍需单独定义和访问每个分数。  

C++为此类问题提供了解决方案，本章将介绍其中一种方案，后续章节探讨其变体。  

容器（Containers）  
----------------  

购买鸡蛋时不会逐个挑选，而是选择装好的蛋盒。这种**容器（container）**能容纳预定数量的鸡蛋（6、12或24枚）。同理，早餐麦片使用盒子作为容器。现实中的容器简化了物品集合管理。  

编程中的**容器**是存储无名对象集合（称为**元素（elements）**）的数据类型。  

关键洞察  
> 处理相关值集合时通常使用容器。  

您已使用过一种容器类型：字符串（string）！字符串容器存储字符集合，可输出为文本：  
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string name{ "Alex" }; // 字符串是字符容器
    std::cout << name; // 以字符序列形式输出字符串
    return 0;
}
```  

容器元素的无名性  
----------------  

容器对象本身有名称（否则无法使用），但其元素无名。这使得容器能容纳任意数量元素，无需为每个元素命名。这种特性是容器区别于其他数据结构的关键，也是普通结构体（如之前的`testScores`）不被视为容器的原因——其数据成员需要唯一名称。  

上例中字符串容器名为`name`，但内部字符（`'A'`、`'l'`、`'e'`、`'x'`）无名。  

如何访问无名元素？每种容器提供特定访问方法，具体方式取决于容器类型（下节课详述）。  

关键洞察  
> 容器元素无名以便无限扩展，通过容器特定方法访问元素。  

容器长度  
----------------  

容器的元素数量称为**长度（length）**或**计数（count）**。在[5.7 — std::string入门](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)中，`std::string`的`length`成员函数可获取字符数量：  
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string name{ "Alex" };
    std::cout << name << " 包含 " << name.length() << " 个字符\n";
    return 0;
}
```  
输出：  
```
Alex 包含 4 个字符
```  

C++中**大小（size）**也用于表示容器元素数量。这个术语选择欠佳，因为`sizeof`运算符返回的是对象占用的字节数。我们将用"长度"指元素数量，"大小"指对象存储空间。  

容器操作  
----------------  

类比蛋盒操作：  
* 获取蛋盒  
* 打开取蛋  
* 增删鸡蛋  
* 计数鸡蛋  

容器通常支持以下操作：  
* 创建容器（空容器/初始容量容器/值列表初始化）  
* 元素访问（首元素/末元素/任意元素）  
* 插入删除元素  
* 获取元素数量  

不同容器类型支持不同操作组合。例如：  
* 支持快速随机访问但无法增删元素的容器  
* 支持快速增删但只能顺序访问的容器  

选择合适容器类型对代码维护和性能至关重要，后续课程将深入讨论。  

元素类型  
----------------  

多数编程语言（含C++）使用**同质容器（homogenous container）**，要求元素类型相同。部分容器预设元素类型（如字符串使用`char`），但通常允许用户指定。C++容器多实现为类模板（class template），用户通过模板参数指定元素类型。  

旁注  
> **异质容器（heterogenous container）**允许不同元素类型，常见于脚本语言（如Python）。  

C++中的容器  
----------------  

**容器库（Containers library）**是C++标准库的一部分，提供多种容器类。C++对"容器"的定义比通用编程定义更严格：只有容器库中的类类型才被视为容器。[完整容器列表](https://en.cppreference.com/w/cpp/container)  

进阶阅读  
> 以下类型符合通用容器定义，但C++标准不视为容器：  
> * C风格数组  
> * `std::string`  
> * `std::vector<bool>`  
> 
> C++容器需满足[所有要求](https://en.cppreference.com/w/cpp/named_req/Container)，包括特定成员函数实现。上述类型未完全满足，但`std::string`和`std::vector<bool>`在多数场景表现类似容器，故称"伪容器"。  

数组（Arrays）入门  
----------------  

**数组（array）**是连续存储元素的容器类型（相邻内存无间隙），支持快速随机访问。概念简单易用，是处理相关值的首选。  

C++包含三种主要数组类型：  
1. **C风格数组（C-style array）**：继承自C语言，属于C++核心语言。现代C++中常称"裸数组"、"定长数组"或"内置数组"。其行为怪异且危险，后续章节详解。  
2. **`std::vector`容器类**：C++03引入，最灵活的数组类型，具备其他数组没有的功能。  
3. **`std::array`容器类**：C++11引入的直接替代C风格数组的类型。虽功能受限，但对小型数组更高效。  

后续计划  
----------------  

下节课将介绍首个容器类`std::vector`，展示其如何高效解决本文开头的挑战。我们将重点学习`std::vector`，因其涉及众多新概念。  

所有容器类接口相似，掌握`std::vector`后学习其他容器（如`std::array`）会更简单。后续容器主要讲解差异点。  

术语说明  
> * **容器类（container classes）**：适用于多数标准库容器类  
> * **数组（array）**：适用于所有数组类型（含其他语言实现）  
> 
> `std::vector`属于两者范畴。  

准备就绪？让我们启程！  
[下一课 16.2 — std::vector与列表构造器入门](Chapter-16/lesson16.2-introduction-to-stdvector-and-list-constructors.md)  
[返回主页](/)  
[上一课 15.x — 第15章总结与测验](Chapter-15/lesson15.x-chapter-15-summary-and-quiz.md)