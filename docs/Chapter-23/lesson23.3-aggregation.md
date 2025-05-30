23.3 — 聚合（Aggregation）  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年12月7日（2024年4月16日更新）  

 

在前文[23.2 — 组合（Composition）](Chapter-23/lesson23.2-composition.md)中，我们提到对象组合（object composition）是从简单对象构建复杂对象的过程。我们讨论了对象组合的一种类型——组合关系（composition）。在组合关系中，整体对象负责部分对象的存在。


本章我们将讨论对象组合的另一种子类型：**聚合（aggregation）**。


聚合  
----------------  

要构成**聚合**，整体对象与其部分必须满足以下关系：


* 部分（成员）属于对象（类）的组成部分
* 部分（成员）可以（根据需要）同时属于多个对象（类）
* 部分（成员）的*存在*不*由对象（类）管理
* 部分（成员）不知道对象（类）的存在


与组合类似，聚合仍是部分-整体关系，部分被包含在整体中，属于单向关系。但与组合不同的是，聚合中的部分可同时属于多个对象，且整体对象不负责部分的存在和生命周期。创建聚合时，不负责创建部分；销毁聚合时，也不负责销毁部分。


例如，考虑个人与其家庭住址的关系。本例中为简化说明，假设每个人都有地址。但该地址可同时属于多人：比如你与室友或伴侣。然而地址不由个人管理——地址可能在个人入住前已存在，并在搬离后继续存在。此外，个人知道自己的地址，但地址不知道居住者。因此这是聚合关系。


再考虑汽车与引擎的关系。汽车引擎是汽车的组成部分。虽然引擎属于汽车，但它也可属于车主等其他实体。汽车不负责引擎的创建或销毁。汽车知道它拥有引擎（需要引擎才能行驶），但引擎不知道自己是汽车的一部分。


在建模物理对象时，"销毁"的表述可能稍显微妙。有人可能会说："如果陨石摧毁了汽车，部件不也都被销毁了吗？"确实如此，但这是陨石的责任。关键在于汽车本身不负责部件的销毁（外部因素可能介入）。


我们可以说聚合建模"具有"（has-a）关系（如部门拥有教师，汽车具有引擎）。


与组合类似，聚合的部分可以是单一或多个。


实现聚合  
----------------  

由于聚合与组合都是部分-整体关系，其实现方式几乎相同，区别主要在语义层面。在组合中，通常使用普通成员变量（或由组合类管理分配/释放的指针）添加部件。


在聚合中，我们同样使用成员变量添加部件。但这些成员变量通常是引用（reference）或指针（pointer），指向类作用域外创建的对象。因此，聚合通常通过构造函数参数接收指向对象，或初始为空并通过访问函数/运算符后续添加部件。


由于这些部件存在于类作用域之外，当类销毁时，指针或引用成员变量会被销毁（但指向的对象不会被删除）。因此部件本身仍存在。


以教师（Teacher）与院系（Department）为例详细说明。本例做两点简化：院系仅包含一名教师；教师不知道自己所属院系。



```
#include <iostream>
#include <string>
#include <string_view>

class Teacher
{
private:
  std::string m_name{};

public:
  Teacher(std::string_view name)
      : m_name{ name }
  {
  }

  const std::string& getName() const { return m_name; }
};

class Department
{
private:
  const Teacher& m_teacher; // 简化处理，院系仅包含一名教师

public:
  Department(const Teacher& teacher)
      : m_teacher{ teacher }
  {
  }
};

int main()
{
  // 在Department作用域外创建教师
  Teacher bob{ "Bob" }; // 创建教师对象

  {
    // 创建院系并通过构造函数参数传递教师
    Department department{ bob };

  } // department在此处离开作用域并被销毁

  // bob仍存在，但department已不存在

  std::cout << bob.getName() << " still exists!\n";

  return 0;
}
```

本例中，`bob`独立于`department`创建，随后传入`department`构造函数。当`department`销毁时，`m_teacher`引用被销毁，但教师对象本身未被销毁，因此在`main()`后续仍存在。


选择适合建模的关系  
----------------  

虽然上例中教师不知所属院系看似奇怪，但在特定程序上下文中可能完全合理。确定实现何种关系时，应选择满足需求的最简单关系，而非看似符合现实场景的关系。


例如，编写车身修理模拟器时，可将汽车与引擎实现为聚合，以便引擎可拆卸存放。但在赛车模拟中，可能将汽车与引擎实现为组合，因为引擎在该上下文中不会独立存在。


> **最佳实践**  
> 实现满足程序需求的最简单关系类型，而非看似符合现实的关系。


组合与聚合总结  
----------------  

**组合**：

* 通常使用普通成员变量
* 若类自行处理对象分配/释放，可使用指针成员
* 负责部件的创建/销毁

**聚合**：

* 通常使用指向或引用聚合类作用域外对象的指针/引用成员
* 不负责部件的创建/销毁


需注意组合与聚合概念可在同一类中混合使用。完全可能编写负责部分（而非全部）部件创建/销毁的类。例如，Department类可包含名称（组合）和教师（聚合）：名称随Department创建/销毁，而教师独立管理。


尽管聚合非常有用，但潜在风险更高，因为聚合不处理部件的释放。释放工作由外部负责。若外部不再持有被弃部件的指针/引用，或忘记清理（假设类会处理），则会导致内存泄漏。


因此应优先选择组合。


注意事项  
----------------  

由于历史和语境原因，聚合的定义不如组合精确——不同资料可能有不同定义。这属正常现象，注意区分即可。


最后注意：在课程[13.7 — 结构体、成员与成员选择简介](Chapter-13/lesson13.7-introduction-to-structs-members-and-member-selection.md)中，我们将聚合数据类型（如结构体和类）定义为组合多个变量的类型。在C++学习中可能遇到"聚合类"（aggregate class）术语，指没有构造函数、析构函数、重载赋值，所有成员公开且不使用继承的结构体/类（即POD类型）。尽管名称相似，聚合类与聚合关系不同，需注意区分。


std::reference_wrapper  
----------------  

在Department/Teacher示例中，我们使用引用存储教师。这在单教师时有效，但若院系有多名教师呢？我们希望将教师存储在某种列表（如`std::vector`）中，但固定数组和标准库容器无法存储引用（因元素需可赋值，而引用不可重新赋值）。



```
std::vector<const Teacher&> m_teachers{}; // 非法
```

可用指针替代，但可能引入空指针风险。在Department/Teacher示例中，我们不希望允许空指针。为此可使用`std::reference_wrapper`。


本质上，`std::reference_wrapper`是行为类似引用的类，但允许赋值和复制，因此兼容`std::vector`等容器。


好消息是无需深入理解其原理即可使用。只需掌握三点：


1. `std::reference_wrapper`位于\<functional\>头文件
2. 创建`std::reference_wrapper`包装对象时，不能使用匿名对象（因匿名对象具有表达式作用域，会导致悬垂引用）
3. 从`std::reference_wrapper`提取对象时，使用`get()`成员函数


在`std::vector`中使用`std::reference_wrapper`的示例：



```
#include <functional> // std::reference_wrapper
#include <iostream>
#include <vector>
#include <string>

int main()
{
  std::string tom{ "Tom" };
  std::string berta{ "Berta" };

  std::vector<std::reference_wrapper<std::string>> names{ tom, berta }; // 通过引用存储字符串

  std::string jim{ "Jim" };

  names.emplace_back(jim);

  for (auto name : names)
  {
    // 使用get()成员函数获取引用字符串
    name.get() += " Beam";
  }

  std::cout << jim << '\n'; // 输出 Jim Beam

  return 0;
}
```

要创建常量引用向量，需在`std::string`前加const：



```
// 常量引用std::string的向量
std::vector<std::reference_wrapper<const std::string>> names{ tom, berta };
```

测验  
----------------  

**问题1**  
以下情况更可能实现为组合还是聚合？  
a) 具有颜色的球  
b) 雇佣多人的雇主  
c) 大学的院系  
d) 你的年龄  
e) 一袋弹珠  

  
<details><summary>答案</summary>  
a) 组合：颜色是球的固有属性  
b) 聚合：雇主初始无员工，且破产时不销毁员工  
c) 组合：大学不存在则院系无法存在  
d) 组合：年龄是个人固有属性  
e) 聚合：袋子与弹珠独立存在  
</details>  

**问题2**  
修改Department/Teacher示例以支持多名教师。以下代码应可运行：



```
#include <iostream>

// ...

int main()
{
  Teacher t1{ "Bob" };
  Teacher t2{ "Frank" };
  Teacher t3{ "Beth" };

  {
    Department department{};
    department.add(t1);
    department.add(t2);
    department.add(t3);
    std::cout << department;
  }

  std::cout << t1.getName() << " still exists!\n";
  std::cout << t2.getName() << " still exists!\n";
  std::cout << t3.getName() << " still exists!\n";

  return 0;
}
```

预期输出：

```
Department: Bob Frank Beth
Bob still exists!
Frank still exists!
Beth still exists!
```

[查看提示](javascript:void(0))  
<details><summary>提示</summary>使用`std::vector`存储教师：  
`std::vector<std::reference_wrapper<const Teacher>> m_teachers{};`  
</details>  

  
<details><summary>解答</summary>  

```
#include <functional>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Teacher
{
private:
  std::string m_name{};

public:
  Teacher(std::string_view name)
      : m_name{ name }
  {
  }

  const std::string& getName() const { return m_name; }
};

class Department
{
private:
  std::vector<std::reference_wrapper<const Teacher>> m_teachers{};

public:
  Department() = default;

  void add(const Teacher& teacher)
  {
    m_teachers.emplace_back(teacher);
  }

  friend std::ostream& operator<<(std::ostream& out, const Department& department)
  {
    out << "Department: ";
    for (const auto& teacher : department.m_teachers)
      out << teacher.get().getName() << ' ';
    out << '\n';
    return out;
  }
};

int main()
{
  Teacher t1{ "Bob" };
  Teacher t2{ "Frank" };
  Teacher t3{ "Beth" };

  {
    Department department{};
    department.add(t1);
    department.add(t2);
    department.add(t3);
    std::cout << department;
  }

  std::cout << t1.getName() << " still exists!\n";
  std::cout << t2.getName() << " still exists!\n";
  std::cout << t3.getName() << " still exists!\n";

  return 0;
}
```  
</details>  

[下一课 23.4 — 关联（Association）](Chapter-23/lesson23.4-association.md)  
[返回主页](/)  
[上一课 23.2 — 组合（Composition）](Chapter-23/lesson23.2-composition.md)