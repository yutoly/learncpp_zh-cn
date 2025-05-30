26.6 — 指针的部分模板特化
====================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年12月5日，太平洋标准时间晚上11:15  
2024年3月29日

在先前课程[26.4 — 类模板特化](Chapter-26/lesson26.4-class-template-specialization.md)中，我们介绍了简单的模板类`Storage`及其针对`double`类型的特化：

```cpp
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template<>
void Storage<double>::print() // 针对double类型的完全特化
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    // 定义存储单元
    Storage i { 5 };
    Storage d { 6.7 }; // 将隐式实例化Storage<double>

    // 打印值
    i.print(); // 调用Storage<int>::print（从Storage<T>实例化）
    d.print(); // 调用Storage<double>::print（来自完全特化版本）
}
```

但这个类存在隐藏缺陷：当`T`为指针类型时，程序虽能编译但行为异常。例如：

```cpp
int main()
{
    double d { 1.2 };
    double *ptr { &d };

    Storage s { ptr };
    s.print();
    
    return 0;
}
```

在作者机器上输出结果为：

```
0x7ffe164e0f50
```

原因分析：由于`ptr`是`double*`类型，`s`的类型为`Storage<double*>`，因此`m_value`成为`double*`类型。构造函数调用时，`m_value`获取了`ptr`所保存地址的副本，调用`print()`成员函数时打印的正是这个地址。

解决方案：

1. 为`double*`添加完全特化：
```cpp
template<>
void Storage<double*>::print() // 针对double*类型的完全特化
{
    if (m_value)
        std::cout << std::scientific << *m_value << '\n';
}
```
这能正确输出：
```
1.200000e+00
```
但此方案仅解决`double*`问题，无法覆盖`int*`、`char*`等其他指针类型。

2. 指针的部分模板特化  
由于函数无法部分特化（截至C++23），需对`Storage`类进行部分特化：
```cpp
template <typename T> // 仍需类型模板参数
class Storage<T*>    // 针对T*的部分特化
{
private:
    T* m_value {};
public:
    Storage(T* value)
      : m_value { value }
    {
    }

    void print()
    {
        if (m_value)
            std::cout << std::scientific << *m_value << '\n';
    }
};
```
此方案中：
- 模板参数`T`被推导为非指针类型
- `Storage<T*>`必须在主模板`Storage<T>`之后定义

3. 所有权与生命周期问题  
`Storage<T*>`存在悬垂指针风险，因其具有引用语义（reference semantics），而主模板具有拷贝语义（copy semantics）。解决方案：
- **方案1**：明确声明`Storage<T*>`为视图类（view class），由调用方保证对象生命周期（不推荐）
- **方案2**：禁止使用`Storage<T*>`，通过`static_assert`限制指针类型：
```cpp
template <typename T>
class Storage
{
    static_assert(!std::is_pointer_v<T> && !std::is_null_pointer_v<T>, 
                  "禁止实例化Storage<T*>和Storage<nullptr>");
    // ... 主模板实现
};
```
- **方案3**：在堆上创建对象副本（推荐）：
```cpp
template <typename T>
class Storage<T*>
{
private:
    std::unique_ptr<T> m_value {}; // 使用std::unique_ptr自动管理内存

public:
    Storage(T* value)
      : m_value { std::make_unique<T>(value ? *value : 0) } 
    {
    }
    // ... 其他成员函数
};
```

当需要类对指针和非指针类型进行差异化处理时，使用部分模板类特化是极为有效的技术方案。

[下一课 26.x — 第26章总结与测验](Chapter-26/lesson26.x-chapter-26-summary-and-quiz.md)  
[返回主页](/)  
[上一课 26.5 — 部分模板特化](Chapter-26/lesson26.5-partial-template-specialization.md)