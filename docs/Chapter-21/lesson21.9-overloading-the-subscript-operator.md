21.9 — 重载下标运算符（subscript operator）
==========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年10月19日上午9:50 PDT  
2025年2月2日更新  

使用数组时，我们通常通过下标运算符（\[]）来访问数组元素：
```
myArray[0] = 7; // 将值7存入数组第一个元素
```
但考虑以下包含数组成员变量的`IntList`类：
```
class IntList
{
private:
    int m_list[10]{};
};

int main()
{
    IntList list{};
    // 如何访问m_list元素？
    return 0;
}
```
由于m_list是私有成员变量，无法直接从list变量访问。这意味着我们无法直接获取或设置数组中的值。如何实现列表元素的存取？

无运算符重载的传统方法：
```
class IntList
{
private:
    int m_list[10]{};

public:
    void setItem(int index, int value) { m_list[index] = value; }
    int getItem(int index) const { return m_list[index]; }
};
```
这种方法可行但不够直观：
```
int main()
{
    IntList list{};
    list.setItem(2, 3); // 是设置第2个元素为3，还是第3个元素为2？
    return 0;
}
```
另一种方法返回整个列表：
```
class IntList
{
private:
    int m_list[10]{};

public:
    int* getList() { return m_list; }
};
```
语法略显怪异：
```
int main()
{
    IntList list{};
    list.getList()[2] = 3;
    return 0;
}
```

重载operator[]
----------------
更优方案是重载下标运算符：
```
#include <iostream>

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        return m_list[index];
    }
};

int main()
{
    IntList list{};
    list[2] = 3; // 设置值
    std::cout << list[2] << '\n'; // 获取值
    return 0;
}
```
重载后的operator[]接受整数下标，返回对应元素的引用。现在可以通过下标直接存取元素。

返回值设为引用的原因
----------------
考虑`list[2] = 3`的执行过程：
1. `list[2]`调用operator[]，返回`m_list[2]`的引用
2. 形成`m_list[2] = 3`的赋值表达式

若返回整数值而非引用，将导致`6 = 3`的无效赋值（假设原值为6）。

const对象的重载
----------------
为const对象提供重载版本：
```
class IntList
{
private:
    int m_list[10]{ 0,1,2,3,4,5,6,7,8,9 };

public:
    // 非const版本：可赋值
    int& operator[] (int index)
    {
        return m_list[index];
    }

    // const版本：仅可访问
    const int& operator[] (int index) const
    {
        return m_list[index];
    }
};
```
const对象调用const版本，返回const引用防止修改。

消除重复代码
----------------
推荐方法：
1. 在const版本中实现核心逻辑
2. 非const版本通过const_cast调用const版本

```
class IntList
{
public:
    int& operator[] (int index)
    {
        return const_cast<int&>(std::as_const(*this)[index]);
    }

    const int& operator[] (int index) const
    {
        return m_list[index];
    }
};
```

C++23改进方案（高级内容）
----------------
```
class IntList
{
public:
    auto&& operator[](this auto&& self, int index)
    {
        return self.m_list[index];
    }
};
```

下标有效性检测
----------------
添加边界检查：
```
#include <cassert>
#include <iterator>

class IntList
{
public:
    int& operator[] (int index)
    {
        assert(index >=0 && static_cast<std::size_t>(index) < std::size(m_list));
        return m_list[index];
    }
};
```
或使用异常处理：
```
class IntList
{
public:
    int& operator[] (int index)
    {
        if (!(index >=0 && ...)) 
        {
            throw std::out_of_range("Invalid index");
        }
        return m_list[index];
    }
};
```

指针对象的问题
----------------
指针调用operator[]需先解引用：
```
IntList* list = new IntList{};
(*list)[2] = 3; // 正确用法
delete list;
```

非整型参数支持
----------------
下标运算符可接受任意类型参数：
```
class Stupid
{
public:
    void operator[] (std::string_view index)
    {
        std::cout << index;
    }
};

int main()
{
    Stupid stupid{};
    stupid["Hello, world!"]; // 输出字符串
    return 0;
}
```

测验实现
----------------
学生成绩映射表示例：
```
struct StudentGrade
{
    std::string name{};
    char grade{};
};

class GradeMap
{
private:
    std::vector<StudentGrade> m_map{};

public:
    char& operator[](std::string_view name)
    {
        auto found = std::find_if(m_map.begin(), m_map.end(),
            [&](const auto& sg) { return sg.name == name; });
        
        if (found != m_map.end())
            return found->grade;

        m_map.emplace_back(std::string{name});
        return m_map.back().grade;
    }
};
```

潜在问题分析
----------------
当vector扩容时，原有引用可能失效：
```
GradeMap grades{};
char& joeGrade = grades["Joe"]; // 有效
grades["Frank"] = 'B'; // 可能导致vector扩容
joeGrade = 'A'; // 可能访问无效内存
```

标准库推荐
----------------
优先使用`std::map`：
```
#include <map>

std::map<std::string, char> grades{
    {"Joe", 'A'}, {"Frank", 'B'}};
grades["Susan"] = 'C';
```

[下一课 21.10 — 重载括号运算符](Chapter-21/lesson21.10-overloading-the-parenthesis-operator.md)  
[返回主页](/)  
[上一课 21.8 — 重载自增和自减运算符](Chapter-21/lesson21.8-overloading-the-increment-and-decrement-operators.md)