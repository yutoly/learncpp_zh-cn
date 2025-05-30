14.9 — 构造函数简介
====================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")
2007年9月5日 下午3:10（太平洋夏令时）
2024年12月29日

当类类型是聚合体（aggregate）时，可直接使用聚合初始化（aggregate initialization）初始化类类型：
```
struct Foo // Foo 是聚合体
{
    int x {};
    int y {};
};

int main()
{
    Foo foo { 6, 7 }; // 使用聚合初始化
    return 0;
}
```
聚合初始化执行成员逐一初始化（成员按定义顺序初始化）。因此上例实例化`foo`时，`foo.x`被初始化为`6`，`foo.y`被初始化为`7`。

> **相关内容**  
> 聚合体定义及聚合初始化详见课程[13.8 — 结构体的聚合初始化](Chapter-13/lesson13.8-struct-aggregate-initialization.md)。

然而，一旦将任何成员变量设为私有（以隐藏数据），类类型就不再是聚合体（因为聚合体不能包含私有成员）。这意味着无法继续使用聚合初始化：
```
class Foo // Foo 不是聚合体（包含私有成员）
{
    int m_x {};
    int m_y {};
};

int main()
{
    Foo foo { 6, 7 }; // 编译错误：无法使用聚合初始化
    return 0;
}
```
禁止通过聚合初始化私有成员类类型的原因包括：
* 聚合初始化需了解类实现细节（需知成员变量及其定义顺序），而隐藏数据成员正是为避免此情况
* 若类存在不变项（invariant），需依赖用户初始化方式维持该不变项

那么如何初始化含私有成员变量的类？编译器对前例的报错提示了线索："错误：找不到匹配的构造函数（no matching constructor）来初始化 'Foo'"。

我们必然需要匹配的构造函数（constructor）。但这究竟是什么？

### 构造函数（Constructors）

**构造函数**是特殊的成员函数，当非聚合类类型对象创建后，该函数会被自动调用。

定义非聚合类类型对象时，编译器会查找与调用方提供的初始值匹配的可访问构造函数：
* 若找到可访问的匹配构造函数，则分配对象内存并调用该构造函数
* 若找不到可访问的匹配构造函数，则产生编译错误

> **关键洞察**  
> 构造函数不创建对象——编译器在构造函数调用前已为对象分配内存。构造函数在未初始化对象上调用。  
> 但若找不到匹配初始值的构造函数，编译器将报错。因此构造函数虽不创建对象，缺乏匹配构造函数会阻止对象创建。

除决定对象创建方式外，构造函数通常执行两项功能：
* 通过成员初始化列表（member initialization list）初始化成员变量
* 在构造函数体内执行其他设置（如校验初始值、打开文件或数据库等）

构造函数执行完毕后，对象即完成"构造"，此时对象应处于一致且可用的状态。

> **注意**：聚合体不允许包含构造函数——向聚合体添加构造函数会使其失去聚合体资格。

### 构造函数命名规则

构造函数命名有特殊规则：
* 必须与类同名（含大小写）。模板类（template classes）名称不含模板参数
* 无返回类型（连`void`也没有）

因构造函数通常属于类的接口（interface）部分，故一般设为公开（public）。

### 基础构造函数示例

为前例添加基础构造函数：
```
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo(int x, int y) // 接收两个初始值的构造函数
    {
        std::cout << "Foo(" << x << ", " << y << ") 已构造\n";
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo{ 6, 7 }; // 调用 Foo(int, int) 构造函数
    foo.print();
    return 0;
}
```
程序现在可编译并输出：
```
Foo(6, 7) 已构造
Foo(0, 0)
```
编译器发现`Foo foo{ 6, 7 }`定义时，会寻找接收两个`int`参数的`Foo`构造函数。`Foo(int, int)`匹配成功，故允许该定义。  
运行时实例化`foo`时：先分配内存，再调用`Foo(int, int)`构造函数（参数`x`初始化为`6`，`y`初始化为`7`）。构造函数体执行后打印`Foo(6, 7) 已构造`。  
调用`print()`成员函数时，注意成员`m_x`和`m_y`值为0。这是因为构造函数虽被调用，但未实际初始化成员。下节课将展示初始化方法。

> **相关内容**  
> 使用拷贝初始化（copy）、直接初始化（direct）和列表初始化（list initialization）调用构造函数初始化对象的区别详见课程[14.15 — 类初始化与拷贝省略](Chapter-14/lesson14.15-class-initialization-and-copy-elision.md)。

### 构造函数的参数隐式转换

在课程[10.1 — 隐式类型转换](Chapter-10/lesson10.1-implicit-type-conversion.md)中，我们指出编译器会在函数调用时隐式转换参数类型以匹配函数定义：
```
void foo(int, int) { }

int main()
{
    foo('a', true); // 匹配 foo(int, int)
    return 0;
}
```
构造函数同理：`Foo(int, int)`构造函数会匹配任何参数可隐式转换为`int`的调用：
```
class Foo
{
public:
    Foo(int x, int y) { }
};

int main()
{
    Foo foo{ 'a', true }; // 匹配 Foo(int, int) 构造函数
    return 0;
}
```

### 构造函数不能为 const

构造函数需初始化被构造对象，因此构造函数不能设为 const：
```
#include <iostream>

class Something
{
private:
    int m_x{};

public:
    Something() // 构造函数必须非 const
    {
        m_x = 5; // 可在非 const 构造函数中修改成员
    }

    int getX() const { return m_x; } // const 成员函数
};

int main()
{
    const Something s{}; // const 对象隐式调用（非 const）构造函数
    std::cout << s.getX(); // 输出 5
    return 0;
}
```
通常 const 对象无法调用非 const 成员函数。但 C++ 标准明确规定（依据[class.ctor.general#5](https://eel.is/c++draft/class.ctor.general#5)）：const 不适用于构建中的对象，其效力在构造函数结束后生效。

### 构造函数 vs 设置函数（setters）

构造函数用于在实例化点初始化整个对象。设置函数用于为现有对象的单个成员赋值。

[下一课 14.10 构造函数的成员初始化列表](Chapter-14/lesson14.10-constructor-member-initializer-lists.md)  
[返回主页](/)  
[上一课 14.8 数据隐藏（封装）的优势](Chapter-14/lesson14.8-the-benefits-of-data-hiding-encapsulation.md)