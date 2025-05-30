16.x — 第16章总结与测验
===================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2023年9月11日，下午2:56（太平洋夏令时）
2025年2月4日

**鼓励话语**  
本章内容不易，我们涵盖了大量知识，并揭示了C++的一些缺陷。恭喜您完成学习！  
数组是解锁C++程序强大功能的关键之一。

**章节回顾**  
**容器（container）** 是一种为无名对象集合（称为**元素（elements）**）提供存储的数据类型。通常在需要处理一组相关值时使用容器。  
容器中元素的数量常称为其**长度（length）**（有时也称**数量（count）**）。在C++中，**大小（size）** 也常用于表示容器元素数量。在多数编程语言（包括C++）中，容器是**同质的（homogenous）**，即要求容器元素具有相同类型。  

**容器库（Containers library）** 是C++标准库的一部分，包含实现常见容器类型的各种类类型。实现容器的类类型有时称为**容器类（container class）**。  
**数组（array）** 是一种以**连续（contiguously）** 方式（即每个元素置于相邻内存位置且无间隙）存储值序列的容器数据类型。数组允许快速直接访问任意元素。  
C++包含三种主要数组类型：（C风格）数组、`std::vector`容器类和`std::array`容器类。  

`std::vector`是C++标准容器库中实现数组的容器类之一。`std::vector`在\<vector\>头文件中定义为类模板，其模板类型参数决定元素类型。因此，`std::vector<int>`声明元素类型为`int`的`std::vector`。  
容器通常具有名为**列表构造函数（list constructor）** 的特殊构造函数，允许使用初始化列表构造容器实例。使用含值列表的列表初始化可构造具有这些元素值的容器。  

在C++中，访问数组元素最常用的方式是通过数组名结合下标运算符（`operator[]`）。要选择特定元素，需在下标运算符的方括号内提供标识所需元素的整数值，该值称为**下标（subscript）**（或非正式称为**索引（index）**）。首个元素用索引0访问，第二个用索引1，依此类推。因索引从0而非1开始，我们说C++中的数组是**基于零（zero-based）** 的。  

`operator[]`不执行任何**边界检查（bounds checking）**，即不检查索引是否在0到N-1（含）范围内。向`operator[]`传递无效索引将导致未定义行为。  
数组是少数允许**随机访问（random access）** 的容器类型之一，即无论容器中有多少元素，每个元素都能直接且以同等速度访问。  

构造类类型对象时，匹配的列表构造函数优先于其他匹配构造函数。当使用非元素值的初始化器构造容器（或任何具有列表构造函数的类型）时，应使用直接初始化：  
```
std::vector v1 { 5 }; // 定义含单个元素`5`的向量
std::vector v2 ( 5 ); // 定义含5个值初始化元素的向量
```  
`std::vector`可设为const但不可设为constexpr。  

标准库容器类均定义名为`size_type`的嵌套typedef成员（有时写作`T::size_type`），它是容器长度（及支持的索引）所用类型的别名。`size_type`几乎总是`std::size_t`的别名，但（在极少数情况下）可被重写为其他类型。我们可合理假设`size_type`是`std::size_t`的别名。  
访问容器类的`size_type`成员时，必须用容器类的完整模板名限定作用域。例如`std::vector<int>::size_type`。  

可通过`size()`成员函数获取容器类对象的长度，该函数返回无符号`size_type`类型的长度。在C++17中，也可使用`std::size()`非成员函数。  
在C++20中，`std::ssize()`非成员函数返回大型*有符号*整型（通常为`std::ptrdiff_t`，即通常作为`std::size_t`有符号对应类型的类型）的长度。  

使用`at()`成员函数访问数组元素会执行运行时边界检查（若越界则抛出`std::out_of_range`类型异常）。若未捕获异常，程序将终止。  
`operator[]`和`at()`成员函数均支持使用非常量索引，但两者均期望索引为`size_type`类型（无符号整型）。当索引非constexpr时会导致符号转换问题。  

`std::vector`类型对象可像其他对象一样传递给函数。若按值传递`std::vector`，将产生昂贵拷贝。因此，我们通常通过（const）引用传递`std::vector`以避免此类拷贝。  
可使用函数模板将含任意元素类型的`std::vector`传入函数。可通过`assert()`确保传入的向量具有正确长度。  

**拷贝语义（copy semantics）** 指决定对象拷贝方式的规则。当说拷贝语义被调用时，意味着我们执行了会创建对象副本的操作。  
当数据所有权从一个对象转移到另一个对象时，我们称数据已被**移动（moved）**。  
**移动语义（move semantics）** 指决定如何将数据从一个对象移动到另一对象的规则。调用移动语义时，任何可移动的数据成员将被移动，不可移动的则被拷贝。用移动替代拷贝的能力使移动语义比拷贝语义更高效，尤其当可用廉价移动替代昂贵拷贝时。  

通常，当对象使用相同类型对象初始化或赋值时，会使用拷贝语义（假设拷贝未被省略）。若对象类型支持移动语义且初始化器或赋值对象是右值，则会自动改用移动语义。  
可按值返回支持移动的类型（如`std::vector`和`std::string`）。此类类型将廉价地移动其值而非进行昂贵拷贝。  

按特定顺序访问容器各元素称为**遍历（traversal）** 或**遍历容器（traversing the container）**。遍历有时也称**迭代（iterating over）** 容器。  
循环常用于遍历数组，循环变量用作索引。注意差一错误（循环体执行次数过多或过少）。  

**基于范围的for循环（range-based for loop）**（有时称**foreach循环**）允许遍历容器而无需显式索引。遍历容器时，优先选择基于范围的for循环而非常规for循环。  
使用类型推导（`auto`）配合基于范围的for循环，让编译器推导数组元素类型。当通常需按（const）引用传递元素类型时，元素声明应使用（const）引用。除非需要处理拷贝，否则始终考虑使用`const auto&`，这将确保即使元素类型后续改变也不会产生拷贝。  

非限定作用域枚举可作为索引使用，有助于提供索引含义的相关信息。  
当需要表示数组长度的枚举项时，添加额外的“count”枚举项非常有用。可通过assert或static_assert确保数组长度等于count枚举项，从而验证数组是否以预期数量的初始化器初始化。  

长度必须在实例化时定义且后续不可更改的数组称为**固定大小数组（fixed-size arrays）** 或**固定长度数组（fixed-length arrays）**。**动态数组（dynamic array）**（也称**可调整大小数组**）是实例化后大小可变的数组。这种调整大小的能力正是`std::vector`的特殊之处。  

`std::vector`实例化后可通过调用`resize()`成员函数（传入新长度）调整大小。  
在`std::vector`上下文中，**容量（capacity）** 是`std::vector`已分配存储空间的元素数量，**长度（length）** 是当前使用的元素数量。可通过`capacity()`成员函数获取`std::vector`的容量。  

当`std::vector`更改其管理存储量时，此过程称为**重新分配（reallocation）**。因重新分配通常需拷贝数组每个元素，故为高开销过程。因此，我们应尽可能避免重新分配。  
下标运算符（`operator[]`）和`at()`成员函数的有效索引基于向量的长度而非容量。  

`std::vector`的`shrink_to_fit()`成员函数请求向量将容量缩减至与其长度匹配。此请求无约束力。  

物品添加到栈和移出的顺序可描述为**后进先出（LIFO）**。最后添加的盘子将是首个移出的。在编程中，**栈（stack）** 是一种以LIFO方式插入和移除元素的容器数据类型，通常通过名为**压入（push）** 和**弹出（pop）** 的两个操作实现。  

`std::vector`的`push_back()`和`emplace_back()`成员函数将增加`std::vector`的长度。若容量不足以插入值，将触发重新分配。压入触发重新分配时，`std::vector`通常会分配额外容量，以便下次添加元素时无需再次触发重新分配。  
`resize()`成员函数改变向量的长度（及必要时的容量）。  
`reserve()`成员函数仅改变容量（必要时）  

增加`std::vector`元素数量的方法：  
* 通过索引访问向量时使用`resize()`。这会改变向量长度，使索引有效。  
* 使用栈操作访问向量时使用`reserve()`。这会增加容量而不改变向量长度。  

`push_back()`和`emplace_back()`均将元素压入栈。若待压入对象已存在，两者等效。但在为压入目的创建临时对象时，`emplace_back()`可能更高效。向容器添加新临时对象或需访问显式构造函数时，优先选用emplace_back()，否则优先选用push_back()。  

`std::vector<bool>`有特殊实现，可能通过将8个布尔值压缩为一个字节来节省空间。  
`std::vector<bool>`不是向量（无需内存连续），也不保存`bool`值（保存位集合），且不符合C++的容器定义。尽管`std::vector<bool>`在多数情况下行为类似向量，但与标准库其余部分不完全兼容。适用于其他元素类型的代码可能不适用于`std::vector<bool>`。因此，通常应避免使用`std::vector<bool>`。  

**测验时间**  
**问题1**  
为以下内容写出定义。尽可能使用CTAD（[13.14 — 类模板实参推导（CTAD）与推导指引](Chapter-13/lesson13.14-class-template-argument-deduction-ctad-and-deduction-guides.md)）。  
a) 用前6个偶数初始化的`std::vector`。  
[显示答案](javascript:void(0))  
```
std::vector evens { 2, 4, 6, 8, 10, 12 };
```  
b) 用值`1.2`、`3.4`、`5.6`和`7.8`初始化的常量`std::vector`。  
[显示答案](javascript:void(0))  
```
const std::vector d { 1.2, 3.4, 5.6, 7.8 }; // 提醒：std::vector不能为constexpr
```  
c) 用名称“Alex”、“Brad”、“Charles”和“Dave”初始化的`std::string_view`常量`std::vector`。  
[显示答案](javascript:void(0))  
```
using namespace std::literals::string_view_literals; // 使用sv后缀
const std::vector names { "Alex"sv, "Brad"sv, "Charles"sv, "Dave"sv }; // 需sv后缀使CTAD推断std::string_view
```  
d) 含单个元素值`12`的`std::vector`。  
[显示答案](javascript:void(0))  
```
std::vector v { 12 };
```  
使用元素值初始化`std::vector`时，应使用列表初始化。  

e) 含12个int元素（初始化为默认值）的`std::vector`。  
[显示提示](javascript:void(0))  
提示：思考此情况是否适用CTAD。  
[显示答案](javascript:void(0))  
```
std::vector<int> v( 12 );
```  
用初始长度初始化`std::vector`时，必须使用直接初始化。且必须显式指定类型模板实参，因无初始化器可推断元素类型。  

**问题2**  
假设您正在编写玩家可持有3类物品的游戏：生命药水、火把和箭。  
> **步骤1**  
> 在命名空间中定义非限定作用域枚举以标识不同物品类型。定义`std::vector`存储玩家携带的每类物品数量。玩家初始应有1个生命药水、5个火把和10支箭。使用assert确保数组具有正确数量的初始化器。  
> 提示：定义count枚举项并在assert中使用。  
> 程序应输出：  
> ```
> 你共有16件物品
> ```  
> [显示答案](javascript:void(0))  
> ```
> #include <cassert>
> #include <iostream>
> #include <vector>
> 
> namespace Items
> {
>     enum Type
>     {
>         health_potion,
>         torch,
>         arrow,
>         max_items
>     };
> }
> 
> // 物品数量应为整型，此处无需函数模板
> int countTotalItems(const std::vector<int>& inventory)
> {
>     int sum { 0 };
>     for (auto e: inventory)
>         sum += e;
>     return sum;
> }
> 
> int main()
> {
>     std::vector inventory { 1, 5, 10 };
>     assert(std::size(inventory) == Items::max_items); // 确保库存初始化器数量正确
> 
>     std::cout << "你共有 " << countTotalItems(inventory) << " 件物品\n";
>     
>     return 0;
> }
> ```  
> > **步骤2**  
> > 修改上步程序使其输出：  
> > ```
> > 你有1个生命药水
> > 你有5个火把
> > 你有10支箭
> > 你共有16件物品
> > ```  
> > 使用循环输出每项库存物品的数量和名称。正确处理名称复数形式。  
> > [显示答案](javascript:void(0))  
> > ```
> > #include <cassert>
> > #include <iostream>
> > #include <string_view>
> > #include <type_traits> // 用于std::is_integral和std::is_enum
> > #include <vector>
> > 
> > namespace Items
> > {
> >     enum Type: int
> >     {
> >         health_potion,
> >         torch,
> >         arrow,
> >         max_items
> >     };
> > }
> > 
> > std::string_view getItemNamePlural(Items::Type type)
> > {
> >     switch (type)
> >     {
> >         case Items::health_potion:  return "生命药水";
> >         case Items::torch:          return "火把";
> >         case Items::arrow:          return "箭";
> > 
> >         default:                    return "???";
> >     }
> > }
> > 
> > std::string_view getItemNameSingular(Items::Type type)
> > {
> >     switch (type)
> >     {
> >         case Items::health_potion:  return "生命药水";
> >         case Items::torch:          return "火把";
> >         case Items::arrow:          return "箭";
> > 
> >         default:                    return "???";
> >     }
> > }
> > 
> > // 辅助函数：将`value`转换为std::size_t类型对象
> > // UZ是std::size_t类型字面量的后缀
> > template <typename T>
> > constexpr std::size_t toUZ(T value)
> > {
> >     // 确保T为整型或枚举类型
> >     static_assert(std::is_integral<T>() || std::is_enum<T>());
> >     
> >     return static_cast<std::size_t>(value);
> > }
> > 
> > 
> > void printInventoryItem(const std::vector<int>& inventory, Items::Type type)
> > {
> >     bool plural { inventory[toUZ(type)] != 1 };
> >     std::cout << "你有 " << inventory[toUZ(type)] << ' ';
> >     std::cout << (plural ? getItemNamePlural(type) : getItemNameSingular(type)) << '\n';
> > }
> > 
> > // 物品数量应为整型，此处无需函数模板
> > int countTotalItems(const std::vector<int>& inventory)
> > {
> >     int sum { 0 };
> >     for (auto e: inventory)
> >         sum += e;
> >     return sum;
> > }
> > 
> > int main()
> > {
> >     std::vector inventory { 1, 5, 10 };
> >     assert(std::size(inventory) == Items::max_items); // 确保库存初始化器数量正确
> > 
> >     // 因无法用范围for迭代枚举类型，需使用传统for循环
> >     for (int i=0; i < Items::max_items; ++i)
> >     {
> >         auto item { static_cast<Items::Type>(i) };
> >         printInventoryItem(inventory, item);
> >     }
> > 
> >     std::cout << "你共有 " << countTotalItems(inventory) << " 件物品\n";
> > 
> >     return 0;
> > }
> > ```  

**问题3**  
编写函数：接受`std::vector`，返回包含数组中最小值和最大值元素索引的`std::pair`。`std::pair`文档见[此处](https://en.cppreference.com/w/cpp/utility/pair)。对以下两个向量调用函数：  
```
    std::vector v1 { 3, 8, 2, 5, 7, 8, 3 };
    std::vector v2 { 5.5, 2.7, 3.3, 7.6, 1.2, 8.8, 6.6 };
```  
程序应输出：  
```
数组 ( 3, 8, 2, 5, 7, 8, 3 )：
最小元素索引2，值2
最大元素索引1，值8

数组 ( 5.5, 2.7, 3.3, 7.6, 1.2, 8.8, 6.6 )：
最小元素索引4，值1.2
最大元素索引5，值8.8
```  
[显示答案](javascript:void(0))  
```
#include <iostream>
#include <vector>

template <typename T>
std::pair<std::size_t, std::size_t> findMinMaxIndices(const std::vector<T>& v)
{
    // 假设元素0为最小值和最大值
    std::size_t minIndex { 0 };
    std::size_t maxIndex { 0 };

    // 遍历剩余元素寻找更小/更大元素
    for (std::size_t index { 1 }; index < v.size(); ++index)
    {
        if (v[index] < v[minIndex])
            minIndex = index;
        if (v[index] > v[maxIndex])
            maxIndex = index;
    }

    return { minIndex, maxIndex };
}

template <typename T>
void printArray(const std::vector<T>& v)
{
    bool comma { false };
    std::cout << "数组 ( ";
    for (const auto& e: v)
    {
        if (comma)
            std::cout << ", ";

        std::cout << e;
        comma = true;
    }
    std::cout << " )：\n";
}

int main()
{
    std::vector v1 { 3, 8, 2, 5, 7, 8, 3 };
    printArray(v1);
    
    auto m1 { findMinMaxIndices(v1) };
    std::cout << "最小元素索引 " << m1.first << "，值 " << v1[m1.first] << '\n';
    std::cout << "最大元素索引 " << m1.second << "，值 " << v1[m1.second] << '\n';

    std::cout << '\n';
    
    std::vector v2 { 5.5, 2.7, 3.3, 7.6, 1.2, 8.8, 6.6 };
    printArray(v2);

    auto m2 { findMinMaxIndices(v2) };
    std::cout << "最小元素索引 " << m2.first << "，值 " << v2[m2.first] << '\n';
    std::cout << "最大元素索引 " << m2.second << "，值 " << v2[m2.second] << '\n';

    return 0;
}
```  

**问题4**  
修改前题程序，允许用户输入任意数量整数，输入`-1`时停止。  
打印向量并查找最小和最大元素。  
输入`3 8 5 2 3 7 -1`时，程序应输出：  
```
输入要添加的数字（输入-1停止）：3 8 5 2 3 7 -1
数组 ( 3, 8, 5, 2, 3, 7 )：
最小元素索引3，值2
最大元素索引1，值8
```  
当用户首个输入为`-1`时进行合理处理。  
[显示答案](javascript:void(0))  
```
#include <iostream>
#include <limits>
#include <vector>

template <typename T>
std::pair<std::size_t, std::size_t> findMinMaxIndices(const std::vector<T>& v)
{
    // 假设元素0为最小值和最大值
    std::size_t minIndex { 0 };
    std::size_t maxIndex { 0 };

    // 遍历剩余元素寻找更小/更大元素
    for (std::size_t index { 1 }; index < v.size(); ++index)
    {
        if (v[index] < v[minIndex])
            minIndex = index;
        if (v[index] > v[maxIndex])
            maxIndex = index;
    }

    return { minIndex, maxIndex };
}

template <typename T>
void printArray(const std::vector<T>& v)
{
    bool comma { false };
    std::cout << "数组 ( ";
    for (const auto& e: v)
    {
        if (comma)
            std::cout << ", ";

        std::cout << e;
        comma = true;
    }
    std::cout << " )：\n";
}

int main()
{
    std::vector<int> v1 { };
    std::cout << "输入要添加的数字（输入-1停止）：";

    while (true)
    {
        int input{};
        std::cin >> input;
        if (input == -1)
            break;

        if (!std::cin) // 若上次提取失败
        {
            std::cin.clear(); // 恢复正常操作模式
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 移除错误输入
            continue;
        }

        v1.push_back(input);
    }

    // 若数组为空
    if (v1.size() == 0)
    {
        std::cout << "数组无元素\n";
    }
    else
    {
        printArray(v1);

        auto m1 { findMinMaxIndices(v1) };
        std::cout << "最小元素索引 " << m1.first << "，值 " << v1[m1.first] << '\n';
        std::cout << "最大元素索引 " << m1.second << "，值 " << v1[m1.second] << '\n';
    }

    return 0;
}
```  

**问题5**  
我们来实现C++man游戏（经典儿童绞刑游戏[Hangman](https://en.wikipedia.org/wiki/Hangman_(game%29)的变体）。  
若您从未玩过，以下是简化规则：  
**高层规则**：  
* 计算机随机选词并为每个字母绘制下划线  
* 玩家在犯X次错误猜测前猜中所有字母则获胜（X可配置）  

**每轮操作**：  
* 玩家猜单字母  
* 若玩家已猜过该字母，不计入并继续  
* 若下划线代表该字母，则替换为字母并继续  
* 若无下划线代表该字母，玩家消耗一次错误猜测  

**状态显示**：  
* 玩家应知剩余错误猜测次数  
* 玩家应知错误猜测的字母（按字母顺序排序）  

因是C++man，用`+`符号表示剩余错误猜测次数。若`+`耗尽则失败。  
以下是完整游戏输出示例：  
```
欢迎来到C++man（绞刑游戏变体）
获胜条件：猜中单词。失败条件：耗尽加号。

单词：________   错误猜测：++++++
输入字母：a
错误，'a'不在单词中！

单词：________   错误猜测：+++++a
输入字母：b
正确，'b'在单词中！

单词：b_______   错误猜测：+++++a
输入字母：c
正确，'c'在单词中！

单词：b__cc___   错误猜测：+++++a
输入字母：d
错误，'d'不在单词中！

单词：b__cc___   错误猜测：++++ad
输入字母：%
输入无效，请重试。

单词：b__cc___   错误猜测：++++ad
输入字母：d
已猜过该字母，请重试。

单词：b__cc___   错误猜测：++++ad
输入字母：e
错误，'e'不在单词中！

单词：b__cc___   错误猜测：+++ade
输入字母：f
错误，'f'不在单词中！

单词：b__cc___   错误猜测：++adef
输入字母：g
错误，'g'不在单词中！

单词：b__cc___   错误猜测：+adefg
输入字母：h
错误，'h'不在单词中！

单词：b__cc___   错误猜测：adefgh
你输了！单词是：broccoli
```  
> **步骤1**  
> 目标：  
> * 首先定义单词列表并编写随机选词器。可使用[8.15 — 全局随机数（Random.h）](global-random-numbers-random-h/#RandomH)中的Random.h辅助。  

> 任务：  
> * 定义名为`WordList`的命名空间。初始单词列表："mystery", "broccoli", "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage"（可自增）。  
> * 编写随机选词函数并显示所选词。多次运行程序确保单词随机化。  

> 此步骤输出示例：  
> ```
> 欢迎来到C++man（绞刑游戏变体）
> 获胜条件：猜中单词。失败条件：耗尽加号。
> 
> 单词是：broccoli
> ```  
> [显示答案](javascript:void(0))  
> ```
> #include <iostream>
> #include <vector>
> #include "Random.h"
> 
> namespace WordList
> {
>     // 在此定义单词列表
>     std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };
> 
>     std::string_view getRandomWord()
>     {
>         return words[Random::get<std::size_t>(0, words.size()-1)];
>     }
> }
> 
> int main()
> {
>     std::cout << "欢迎来到C++man（绞刑游戏变体）\n";
>     std::cout << "获胜条件：猜中单词。失败条件：耗尽加号。\n";
> 
>     std::cout << "单词是：" << WordList::getRandomWord();
>   
>     return 0;
> }
> ```  

> > **步骤2**  
> > 开发复杂程序时，我们希望增量工作，每次添加一两个功能并验证。接下来添加什么？  
> > 目标：  
> > * 绘制游戏基础状态，将单词显示为下划线  
> > * 接收用户输入的字母，进行基础错误验证  
> > 
> > 此步骤暂不跟踪用户输入过的字母。  
> > 输出示例：  
> > ```
> > 欢迎来到C++man（绞刑游戏变体）
> > 获胜条件：猜中单词。失败条件：耗尽加号。
> > 
> > 单词：________
> > 输入字母：%
> > 输入无效，请重试。
> > 输入字母：a
> > 你输入了：a
> > ```  
> > 任务：  
> > * 创建`Session`类存储游戏会话所需数据（目前只需随机单词）  
> > * 创建函数显示游戏基础状态（单词显示为下划线）  
> > * 创建函数接收用户输入的字母，过滤非字母或无关输入  
> > 
> > [显示答案](javascript:void(0))  
> > ```
> > #include <iostream>
> > #include <string_view>
> > #include <vector>
> > #include "Random.h"
> > 
> > namespace WordList
> > {
> >     // 在此定义单词列表
> >     std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };
> > 
> >     std::string_view getRandomWord()
> >     {
> >         return words[Random::get<std::size_t>(0, words.size()-1)];
> >     }
> > }
> > 
> > class Session
> > {
> > private:
> >     // 游戏会话数据
> >     std::string_view m_word { WordList::getRandomWord() };
> > 
> > public:
> >     std::string_view getWord() const { return m_word; }
> > };
> > 
> > void draw(const Session& s)
> > {
> >     std::cout << '\n';
> > 
> >     std::cout << "单词：";
> >     for ([[maybe_unused]] auto c: s.getWord()) // 遍历单词每个字母
> >     {
> >         std::cout << '_';
> >     }
> > 
> >     std::cout << '\n';
> > }
> > 
> > char getGuess()
> > {
> >     while (true)
> >     {
> >         std::cout << "输入字母：";
> > 
> >         char c{};
> >         std::cin >> c;
> > 
> >         // 若用户输入错误，重试
> >         if (!std::cin)
> >         {
> >             // 修复
> >             std::cin.clear();
> >             std::cout << "输入无效，请重试。\n";
> >             std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
> >             continue;
> >         }
> >         
> >         // 清除无关输入
> >         std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
> > 
> >         // 若输入无效字符，重试
> >         if (c < 'a' || c > 'z')
> >         {
> >             std::cout << "输入无效，请重试。\n";
> >             continue;
> >         }
> > 
> >         return c;
> >     }
> > }
> > 
> > int main()
> > {
> >     std::cout << "欢迎来到C++man（绞刑游戏变体）\n";
> >     std::cout << "获胜条件：猜中单词。失败条件：耗尽加号。\n";
> > 
> >     Session s{};
> > 
> >     draw(s);
> >     char c { getGuess() };
> >     std::cout << "你猜了：" << c << '\n';
> >     
> >     return 0;
> > }
> > ```  

> > > **步骤3**  
> > > 现已能显示游戏状态并获取用户输入，将其整合到游戏中。  
> > > 目标：  
> > > * 跟踪用户已猜字母  
> > > * 显示正确猜中的字母  
> > > * 实现基础游戏循环  
> > > 
> > > 任务：  
> > > * 更新Session类跟踪已猜字母  
> > > * 修改游戏状态函数显示下划线和正确字母  
> > > * 更新输入例程拒绝已猜字母  
> > > * 编写执行6次后退出的循环（以测试上述功能）  
> > > 
> > > 此步骤不告知用户所猜字母是否在单词中（但会在游戏状态中显示）。  
> > > 关键点是决定存储用户已猜字母信息的方式。有几种可行方法。提示：字母数量固定且需频繁操作。  
> > > [显示提示](javascript:void(0))  
> > > 提示：为每个字母使用`bool`比维护字母列表并搜索更简单高效。  
> > > [显示提示](javascript:void(0))  
> > > 提示：因不使用标准库其他功能，此处使用`std::vector<bool>`无妨。  
> > > [显示提示](javascript:void(0))  
> > > 提示：可通过`(字母 % 32)-1`将字母转为数组索引（大小写均适用）。  
> > > 
> > > 输出示例：  
> > > ```
> > > 欢迎来到C++man（绞刑游戏变体）
> > > 获胜条件：猜中单词。失败条件：耗尽加号。
> > > 
> > > 单词：________
> > > 输入字母：a
> > > 
> > > 单词：____a___
> > > 输入字母：a
> > > 已猜过该字母，请重试。
> > > 输入字母：b
> > > 
> > > 单词：____a___
> > > 输入字母：c
> > > 
> > > 单词：____a___
> > > 输入字母：d
> > > 
> > > 单词：d___a___
> > > 输入字母：e
> > > 
> > > 单词：d___a__e
> > > 输入字母：f
> > > 
> > > 单词：d___a__e
> > > 输入字母：g
> > > ```  
> > > [显示答案](javascript:void(0))  
> > > ```
> > > #include <iostream>
> > > #include <string_view>
> > > #include <vector>
> > > #include "Random.h"
> > > 
> > > namespace WordList
> > > {
> > >     // 在此定义单词列表
> > >     std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };
> > > 
> > >     std::string_view getRandomWord()
> > >     {
> > >         return words[Random::get<std::size_t>(0, words.size()-1)];
> > >     }
> > > }
> > > 
> > > class Session
> > > {
> > > private:
> > >     // 游戏会话数据
> > >     std::string_view m_word { WordList::getRandomWord() };
> > >     std::vector<bool> m_letterGuessed { std::vector<bool>(26) };
> > > 
> > >     std::size_t toIndex(char c) const { return static_cast<std::size_t>((c % 32)-1); }
> > > 
> > > public:
> > >     std::string_view getWord() const { return m_word; }
> > > 
> > >     bool isLetterGuessed(char c) const { return m_letterGuessed[toIndex(c)]; }
> > >     void setLetterGuessed(char c) { m_letterGuessed[toIndex(c)] = true; }
> > > };
> > > 
> > > void draw(const Session& s)
> > > {
> > >     std::cout << '\n';
> > > 
> > >     std::cout << "单词：";
> > >     for (auto c: s.getWord()) // 遍历单词每个字母
> > >     {
> > >         if (s.isLetterGuessed(c))
> > >             std::cout << c;
> > >         else
> > >             std::cout << '_';
> > >     }
> > > 
> > >     std::cout << '\n';
> > > }
> > > 
> > > char getGuess(const Session& s)
> > > {
> > >     while (true)
> > >     {
> > >         std::cout << "输入字母：";
> > > 
> > >         char c{};
> > >         std::cin >> c;
> > > 
> > >         // 若用户输入错误，重试
> > >         if (!std::cin)
> > >         {
> > >             // 修复
> > >             std::cin.clear();
> > >             std::cout << "输入无效，请重试。\n";
> > >             std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
> > >             continue;
> > >         }
> > >         
> > >         // 清除无关输入
> > >         std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
> > > 
> > >         // 若输入无效字符，重试
> > >         if (c < 'a' || c > 'z')
> > >         {
> > >             std::cout << "输入无效，请重试。\n";
> > >             continue;
> > >         }
> > > 
> > >         // 若字母已猜过，重试
> > >         if (s.isLetterGuessed(c))
> > >         {
> > >             std::cout << "已猜过该字母，请重试。\n";
> > >             continue;
> > >         }
> > > 
> > >         // 有效猜测
> > >         return c;
> > >     }
> > > }
> > > 
> > > int main()
> > > {
> > >     std::cout << "欢迎来到C++man（绞刑游戏变体）\n";
> > >     std::cout << "获胜条件：猜中单词。失败条件：耗尽加号。\n";
> > > 
> > >     Session s {};
> > > 
> > >     int count { 6 };
> > >     while (--count)
> > >     {
> > >         draw(s);
> > >         char c { getGuess(s) };
> > >         s.setLetterGuessed(c);
> > >     }
> > > 
> > >     // 绘制游戏最终状态
> > >     draw(s);
> > >     
> > >     return 0;
> > > }
> > > ```  

> > > > **步骤4**  
> > > > 目标：完成游戏。  
> > > > 任务：  
> > > > * 添加剩余错误次数显示  
> > > > * 添加错误猜测字母显示  
> > > > * 添加胜利/失败条件及文本  
> > > > 
> > > > [显示答案](javascript:void(0))  
> > > > ```
> > > > #include <iostream>
> > > > #include <string_view>
> > > > #include <vector>
> > > > #include "Random.h"
> > > > 
> > > > namespace Settings
> > > > {
> > > >     constexpr int wrongGuessesAllowed { 6 };
> > > > }
> > > > 
> > > > namespace WordList
> > > > {
> > > >     // 在此定义单词列表
> > > >     std::vector<std::string_view> words { "mystery", "broccoli" , "account", "almost", "spaghetti", "opinion", "beautiful", "distance", "luggage" };
> > > > 
> > > >     std::string_view getRandomWord()
> > > >     {
> > > >         return words[Random::get<std::size_t>(0, words.size()-1)];
> > > >     }
> > > > }
> > > > 
> > > > class Session
> > > > {
> > > > private:
> > > >     // 游戏会话数据
> > > >     std::string_view m_word { WordList::getRandomWord() };
> > > >     int m_wrongGuessesLeft { Settings::wrongGuessesAllowed };
> > > >     std::vector<bool> m_letterGuessed { std::vector<bool>(26) };
> > > > 
> > > >     std::size_t toIndex(char c) const { return static_cast<std::size_t>((c % 32)-1); }
> > > > 
> > > > public:
> > > >     std::string_view getWord() const { return m_word; }
> > > > 
> > > >     int wrongGuessesLeft() const { return m_wrongGuessesLeft; }
> > > >     void removeGuess() { --m_wrongGuessesLeft; }
> > > > 
> > > >     bool isLetterGuessed(char c) const { return m_letterGuessed[toIndex(c)]; }
> > > >     void setLetterGuessed(char c) { m_letterGuessed[toIndex(c)] = true; }
> > > > 
> > > >     bool isLetterInWord(char c) const
> > > >     {
> > > >         for (auto ch: m_word) // 遍历单词每个字母
> > > >         {
> > > >             if (ch == c)
> > > >                 return true;
> > > >         }
> > > > 
> > > >         return false;
> > > >     }
> > > > 
> > > >     bool won()
> > > >     {
> > > >         for (auto c: m_word) // 遍历单词每个字母
> > > >         {
> > > >             if (!isLetterGuessed(c))
> > > >                 return false;
> > > >         }
> > > >         
> > > >         return true;
> > > >     }
> > > > };
> > > > 
> > > > void draw(const Session& s)
> > > > {
> > > >     std::cout << '\n';
> > > > 
> > > >     std::cout << "单词：";
> > > >     for (auto c: s.getWord()) // 遍历单词每个字母
> > > >     {
> > > >         if (s.isLetterGuessed(c))
> > > >             std::cout << c;
> > > >         else
> > > >             std::cout << '_';
> > > >     }
> > > > 
> > > >     std::cout << "   错误猜测：";
> > > >     for (int i=0; i < s.wrongGuessesLeft(); ++i)
> > > >         std::cout << '+';
> > > > 
> > > > 
> > > >     for (char c='a'; c <= 'z'; ++c)
> > > >         if (s.isLetterGuessed(c) && !s.isLetterInWord(c))
> > > >             std::cout << c;
> > > > 
> > > >     std::cout << '\n';
> > > > }
> > > > 
> > > > char getGuess(const Session& s)
> > > > {
> > > >     while (true)
> > > >     {
> > > >         std::cout << "输入字母：";
> > > > 
> > > >         char c{};
> > > >         std::cin >> c;
> > > > 
> > > >         // 若用户输入错误，重试
> > > >         if (!std::cin)
> > > >         {
> > > >             // 修复
> > > >             std::cin.clear();
> > > >             std::cout << "输入无效，请重试。\n";
> > > >             std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
> > > >             continue;
> > > >         }
> > > >         
> > > >         // 清除无关输入
> > > >         std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
> > > > 
> > > >         // 若输入无效字符，重试
> > > >         if (c < 'a' || c > 'z')
> > > >         {
> > > >             std::cout << "输入无效，请重试。\n";
> > > >             continue;
> > > >         }
> > > > 
> > > >         // 若字母已猜过，重试
> > > >         if (s.isLetterGuessed(c))
> > > >         {
> > > >             std::cout << "已猜过该字母，请重试。\n";
> > > >             continue;
> > > >         }
> > > > 
> > > >         // 有效猜测
> > > >         return c;
> > > >     }
> > > > }
> > > > 
> > > > void handleGuess(Session &s, char c)
> > > > {
> > > >     s.setLetterGuessed(c);
> > > >     
> > > >     if (s.isLetterInWord(c))
> > > >     {
> > > >         std::cout << "正确，'" << c << "'在单词中！\n";
> > > >         return;
> > > >     }
> > > >     
> > > >     std::cout << "错误，'" << c << "'不在单词中！\n";
> > > >     s.removeGuess();
> > > > }
> > > > 
> > > > int main()
> > > > {
> > > >     std::cout << "欢迎来到C++man（绞刑游戏变体）\n";
> > > >     std::cout << "获胜条件：猜中单词。失败条件：耗尽加号。\n";
> > > > 
> > > >     Session s{};
> > > > 
> > > >     while (s.wrongGuessesLeft() && !s.won())
> > > >     {
> > > >         draw(s);
> > > >         char c { getGuess(s) };
> > > >         handleGuess(s, c);
> > > >     }
> > > > 
> > > >     // 绘制游戏最终状态
> > > >     draw(s);
> > > > 
> > > >     if (!s.wrongGuessesLeft())
> > > >         std::cout << "你输了！单词是：" << s.getWord() << '\n';
> > > >     else
> > > >         std::cout << "你赢了！\n";
> > > >     
> > > >     return 0;
> > > > }
> > > > ```  

[下一课 17.1 — std::array简介](Chapter-17/lesson17.1-introduction-to-stdarray.md)  
[返回主页](/)  
[上一课 16.12 — std::vector\<bool\>](Chapter-16/lesson16.12-stdvector-bool.md)