6.5 — 逗号运算符
=========================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2007年6月14日 上午7:41（太平洋夏令时）  
2023年10月24日更新

| 运算符 | 符号 | 形式 | 操作 |
| --- | --- | --- | --- |
| 逗号 | , | x, y | 先计算x再计算y，返回y的值 |

**逗号运算符（comma operator）** `,` 允许在需要单个表达式的位置计算多个表达式。该运算符首先计算左操作数（left operand），然后计算右操作数（right operand），最终返回右操作数的结果。

示例：
```cpp
#include <iostream>

int main()
{
    int x{ 1 };
    int y{ 2 };

    std::cout << (++x, ++y) << '\n'; // 先递增x和y，表达式结果为右操作数的值
    return 0;
}
```

首先计算逗号运算符的左操作数，将x从1递增到2。接着计算右操作数，将y从2递增到3。逗号运算符返回右操作数的结果（3），该值随后被输出到控制台。

需要注意的是，逗号运算符在所有运算符中具有最低的优先级（precedence），甚至低于赋值运算符。因此以下两行代码具有不同行为：

```cpp
z = (a, b); // 先计算(a, b)得到b的结果，再将值赋给z
z = a, b;   // 解析为"(z = a), b"，将a的值赋给z，然后计算b并丢弃结果
```

这使得逗号运算符的使用存在一定风险。

在几乎所有情况下，使用逗号运算符的语句都可以改写成更清晰的独立语句。例如上述代码可优化为：

```cpp
#include <iostream>

int main()
{
    int x{ 1 };
    int y{ 2 };

    ++x;
    std::cout << ++y << '\n';

    return 0;
}
```

大多数程序员几乎不使用逗号运算符，唯一的例外是在**for循环（for loops）**内部，这种情况较为常见（详见未来课程[8.10 — for语句](Chapter-8/lesson8.10-for-statements.md)）。

> **最佳实践**  
> 除非在for循环内部，否则应避免使用逗号运算符。

---

### 作为分隔符的逗号

在C++中，逗号符号常被用作**分隔符（separator）**，这些用法不会触发逗号运算符。常见的分隔符用例包括：

```cpp
void foo(int x, int y) // 分隔符：函数定义中的参数分隔
{
    add(x, y); // 分隔符：函数调用中的参数分隔
    constexpr int z{ 3 }, w{ 5 }; // 分隔符：同行定义多个变量（不建议使用此写法）
}
```

除声明多个变量的情况外（该做法本身不推荐），无需避免使用作为分隔符的逗号。

[下一课 6.6 条件运算符](Chapter-6/lesson6.6-the-conditional-operator.md)  
[返回主页](/)  
[上一课 6.4 递增/递减运算符及其副作用](Chapter-6/lesson6.4-increment-decrement-operators-and-side-effects.md)