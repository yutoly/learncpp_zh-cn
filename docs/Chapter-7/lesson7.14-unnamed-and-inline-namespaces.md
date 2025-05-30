7.14 — 未命名（匿名）与内联命名空间
=====================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年11月26日（首次发布于2020年1月3日）

C++支持两种值得了解的命名空间变体。本节内容为可选学习项，后续课程不会基于此内容展开。

未命名（匿名）命名空间
----------------

**未命名命名空间（unnamed namespace）**（也称**匿名命名空间（anonymous namespace）**）指未指定名称的命名空间定义：

```cpp
#include <iostream>

namespace // 未命名命名空间
{
    void doSomething() // 仅限本文件访问
    {
        std::cout << "v1\n";
    }
}

int main()
{
    doSomething(); // 无需命名空间前缀即可调用

    return 0;
}
```

输出结果：

```
v1
```

未命名命名空间内的所有声明内容都视为父命名空间的组成部分。因此虽然`doSomething()`函数定义在未命名命名空间中，实际上该函数属于父命名空间（本例中是全局命名空间），故可在`main()`中直接调用。

未命名命名空间的另一个关键特性是：其内部所有标识符都具有**内部链接（internal linkage）**，即未命名命名空间的内容在定义文件之外不可见。

对于函数而言，这与将函数声明为`static`具有相同效果。以下程序与上述示例等价：

```cpp
#include <iostream>

static void doSomething() // 仅限本文件访问
{
    std::cout << "v1\n";
}

int main()
{
    doSomething();

    return 0;
}
```

当需要确保大量内容仅在当前翻译单元（translation unit）内可见时，使用未命名命名空间比逐个声明`static`更便捷。此外，未命名命名空间还能限制自定义类型的作用域（后续课程讨论），这是其他机制无法替代的。

> **技巧**  
> 可采用逆向策略——将所有非导出的内容置于未命名命名空间。

> **最佳实践**  
> * 需要限制作用域时优先使用未命名命名空间  
> * 避免在头文件中使用未命名命名空间  

内联命名空间
----------------

考虑以下程序：

```cpp
#include <iostream>

void doSomething()
{
    std::cout << "v1\n";
}

int main()
{
    doSomething();

    return 0;
}
```

输出：

```
v1
```

当需要升级`doSomething()`功能但需保持旧版本兼容时，**内联命名空间（inline namespace）**可解决版本管理问题。使用`inline`关键字定义内联命名空间：

```cpp
#include <iostream>

inline namespace V1 // 定义内联命名空间V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

namespace V2 // 定义普通命名空间V2
{
    void doSomething()
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // 调用V1版本
    V2::doSomething(); // 调用V2版本

    doSomething(); // 调用内联版本（V1）
 
    return 0;
}
```

输出：

```
V1
V2
V1
```

调用方默认使用内联版本（V1），需要新版本时可显式调用`V2::doSomething()`。若需推广新版本：

```cpp
#include <iostream>

namespace V1 // 普通命名空间V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

inline namespace V2 // 内联命名空间V2
{
    void doSomething()
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // 调用V1版本
    V2::doSomething(); // 调用V2版本

    doSomething(); // 调用内联版本（V2）
 
    return 0;
}
```

输出：

```
V1
V2
V2
```

此时默认调用V2版本，旧版本用户需显式调用`V1::doSomething()`。

混合使用内联与未命名命名空间（可选）
----------------

命名空间可同时为内联且未命名：

```cpp
#include <iostream>

inline namespace // 内联未命名命名空间
{
    void doSomething() // 具有内部链接
    {
        std::cout << "V2\n";
    }
}

int main()
{
    doSomething(); // 调用内联版本

    return 0;
}
```

更佳实践是在内联命名空间中嵌套未命名命名空间：

```cpp
#include <iostream>

inline namespace V2
{
    namespace // 未命名命名空间
    {
        void doSomething() // 内部链接
        {
            std::cout << "V2\n";
        }
    }
}

int main()
{
    V2::doSomething(); // 显式调用V2版本
    doSomething(); // 隐式调用内联版本

    return 0;
}
```

[下一课 7.x — 第7章总结与测验](Chapter-7/lesson7.x-chapter-7-summary-and-quiz.md)  
[返回主页](/)  
[上一课 7.13 — using声明与using指令](Chapter-7/lesson7.13-using-declarations-and-using-directives.md)