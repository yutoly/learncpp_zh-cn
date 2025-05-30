7.2 — 用户自定义命名空间（user-defined namespaces）与作用域解析运算符（scope resolution operator）  
=================================================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2007年8月17日（首次发布）  
2024年6月28日（最后更新）  

在课程[2.9 — 命名冲突与命名空间简介](Chapter-2/lesson2.9-naming-collisions-and-an-introduction-to-namespaces.md)中，我们介绍了`命名冲突（naming collision）`和`命名空间（namespace）`的概念。当两个相同标识符（identifier）出现在同一作用域（scope）时，编译器无法确定应使用哪个，就会发生命名冲突。此时编译器或链接器（linker）将产生错误信息。  

**关键洞察**  
随着程序规模扩大，标识符数量增加导致命名冲突概率呈指数级增长。因此建议将标识符定义在尽可能小的作用域中。  

以下示例展示`foo.cpp`和`goo.cpp`中同名函数导致的命名冲突：  

foo.cpp:  
```cpp
// 此doSomething()函数执行参数加法运算
int doSomething(int x, int y)
{
    return x + y;
}
```  

goo.cpp:  
```cpp
// 此doSomething()函数执行参数减法运算
int doSomething(int x, int y)
{
    return x - y;
}
```  

main.cpp:  
```cpp
#include <iostream>

int doSomething(int x, int y); // doSomething的前向声明（forward declaration）

int main()
{
    std::cout << doSomething(4, 3) << '\n'; // 将调用哪个doSomething？
    return 0;
}
```  

当同时编译这两个文件时，链接器将报错：  
```
goo.cpp:3: 'doSomething(int, int)'的多重定义；foo.cpp:3: 首次定义在此处
```  

通过命名空间解决冲突  
----------------  

C++允许使用`namespace`关键字定义**用户自定义命名空间**：  
```cpp
namespace NamespaceIdentifier
{
    // 命名空间内容
}
```  

传统风格建议命名空间名称小写，但现代风格推荐首字母大写。我们将原示例改造为：  

foo.cpp:  
```cpp
namespace Foo // 定义Foo命名空间
{
    int doSomething(int x, int y)
    {
        return x + y;
    }
}
```  

goo.cpp:  
```cpp
namespace Goo // 定义Goo命名空间
{
    int doSomething(int x, int y)
    {
        return x - y;
    }
}
```  

此时main.cpp需要显式指定命名空间：  

```cpp
#include <iostream>

int main()
{
    std::cout << Foo::doSomething(4, 3) << '\n'; // 使用Foo命名空间的版本
    std::cout << Goo::doSomething(4, 3) << '\n'; // 使用Goo命名空间的版本
    return 0;
}
```  

输出：  
```
7
1
```  

作用域解析运算符（::）  
----------------  

作用域解析运算符用于指定标识符所在的命名空间：  
```cpp
命名空间名::标识符
```  

空前缀时表示全局命名空间：  
```cpp
#include <iostream>

namespace Foo
{
    void print() { std::cout << "Hello"; }
}

void print() { std::cout << " there\n"; }

int main()
{
    Foo::print(); // Foo命名空间的print
    ::print();    // 全局命名空间的print
    return 0;
}
```  

输出：  
```
Hello there
```  

命名空间特性  
----------------  

* **多文件声明**：命名空间可分散在多个文件中  
* **前向声明**：头文件（header file）中的声明需在命名空间内  
* **嵌套命名空间**：支持C++17风格的`命名空间1::命名空间2`语法  
* **命名空间别名**：使用`namespace 别名 = 原命名空间`简化调用  

合理使用建议  
----------------  

* 个人小型项目可不使用命名空间  
* 分发代码必须使用命名空间防止冲突  
* 多团队协作建议使用层级命名空间（如`公司::项目::模块`）  
* 避免超过三层的深层嵌套命名空间  

后续课程将介绍[7.14 — 未命名与内联命名空间](Chapter-7/lesson7.14-unnamed-and-inline-namespaces.md)。  

[下一课 7.3 局部变量](Chapter-7/lesson7.3-local-variables.md)  
[返回主页](/)  
[上一课 7.1 复合语句（块）](Chapter-7/lesson7.1-compound-statements-blocks.md)