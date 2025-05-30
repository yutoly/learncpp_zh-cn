5.9 — std::string_view（下篇）
==================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年1月2日（首次发布于2022年6月16日）

 

在前几课中，我们介绍了两种字符串类型：`std::string`（[5.7 — std::string简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)）和`std::string_view`（[5.8 — std::string_view简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)）。

由于`std::string_view`是我们首次接触的视图类型，我们将深入探讨其安全使用方式，并通过示例说明常见误用情形。最后提供`std::string`与`std::string_view`的选用指南。

 

所有者与观察者的概念
----------------

让我们通过比喻来理解这个概念。假设你要画一辆自行车，但没有实物怎么办？

**拥有者方案**：购买自行车。作为所有者，你有权使用和维护它，但需承担购置成本、维护责任和最终处置工作。所有权（ownership）需要付出较高成本，所有者需全权管理对象的生命周期。

**观察者方案**：临摹邻居的自行车。作为观察者（viewer），你无需承担维护责任，但无法修改被观察对象。观察行为（viewing）成本低廉，但存在被观察对象可能被移动或修改的风险。

 

`std::string`是唯一所有者
----------------

当`std::string`对象初始化时，它会创建初始值的独立副本。这种独立性确保即使原始值被修改或销毁，`std::string`自身依然安全。但这种安全保障需要付出拷贝的代价。

 

关键洞察
----------------
初始化完成后，初始化值可能面临两种命运：
* 若为临时值：立即被销毁
* 若为变量：调用者可自由修改或销毁

`std::string`通过拷贝确保不受这些变化影响。代价是昂贵的拷贝操作。

 

何时无需拷贝
----------------
回顾前文示例：
```cpp
void printString(std::string str) // str拷贝初始值
{
    std::cout << str << '\n';
}
```
当`printString(s)`调用时，`str`进行昂贵拷贝。若`s`在函数执行期间：
1. 不会被销毁
2. 不会被修改
3. 函数不修改字符串

则可通过`std::string_view`避免拷贝。

 

`std::string_view`作为观察者
----------------
`std::string_view`创建对已有字符串的轻量视图。其生命周期内始终依赖被观察字符串。若被观察字符串被修改或销毁，将导致未定义行为（称为悬垂视图，dangling view）。

 

警告
----------------
视图依赖被观察对象。若对象在视图使用期间被修改或销毁，将导致未定义行为。

 

`std::string_view`的最佳实践：只读函数参数
----------------
`std::string_view`最适用于作为只读函数参数，可接受C风格字符串、`std::string`或`std::string_view`参数而无需拷贝：

```cpp
void printSV(std::string_view str) // 创建参数视图
{
    std::cout << str << '\n';
}
```

 

常见误用示例
----------------

**示例1：观察局部变量**
```cpp
{
    std::string s{"Hello"};
    sv = s; // sv观察s
} // s被销毁
std::cout << sv; // 未定义行为
```

**示例2：观察函数返回值**
```cpp
std::string_view name{getName()}; // 返回临时std::string
std::cout << name; // 临时对象已销毁，未定义行为
```

**示例3：字符串字面量陷阱**
```cpp
std::string_view name{"Alex"s}; // 观察临时std::string
std::cout << name; // 临时对象已销毁，未定义行为
```

**示例4：字符串修改导致视图失效**
```cpp
std::string s{"Hello"};
std::string_view sv{s};
s = "Hi"; // 修改s导致sv失效
std::cout << sv; // 未定义行为
```

 

视图重置
----------------
可通过重新赋值使失效视图生效：
```cpp
sv = s; // 重新建立有效视图
```

 

返回`std::string_view`的风险
----------------
返回观察局部变量的视图会导致悬垂视图：
```cpp
std::string_view getBoolName(bool b){
    std::string t{"true"}, f{"false"};
    return b ? t : f; // 返回局部变量视图
} // t和f被销毁
```

安全返回情形：
1. 返回C风格字符串字面量
2. 返回函数参数（需确保参数生命周期）

 

视图修改函数
----------------
通过`remove_prefix()`和`remove_suffix()`调整视图范围（不修改原字符串）：
```cpp
std::string_view str{"Peach"};
str.remove_prefix(1); // "each"
str.remove_suffix(2); // "ea"
```

 

子字符串与空终止
----------------
`std::string_view`可观察子字符串（substring）。注意其可能非空终止（null-terminated），需通过`std::string`转换确保终止。

 

选用指南
----------------
**变量使用场景**：
- `std::string`：需修改字符串、存储用户输入或函数返回值
- `std::string_view`：只读访问现有字符串且保证其生命周期

**函数参数**：
- `std::string_view`：需要只读字符串参数
- `const std::string&`：C++14及以下标准

**返回类型**：
- `std::string`：返回局部变量或拷贝值
- `std::string_view`：返回字面量或参数视图

 

关键总结
----------------
**`std::string`要点**：
- 初始化和拷贝成本高
- 避免传值拷贝
- 修改会失效所有关联视图

**`std::string_view`要点**：
- 主要用作函数参数和返回字面量
- 观察C风格字面量始终安全
- 可能非空终止
- 失效视图导致未定义行为

[下一课 5.x — 第5章总结与测验](Chapter-5/lesson5.x-chapter-5-summary-and-quiz.md)  
[返回主页](/)  
[上一课 5.8 — std::string_view简介](Chapter-5/lesson5.8-introduction-to-stdstring_view.md)