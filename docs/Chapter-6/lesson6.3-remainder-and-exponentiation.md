6.3 — 取余与幂运算
===================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月30日（首次发布于2019年8月17日）

取余运算符（operator%）
----------------

**取余运算符**（remainder operator，常被误称为模运算符（modulo operator）或模数运算符（modulus operator））是进行整数除法后返回余数的运算符。例如 7 / 4 = 1 余 3，因此 7 % 4 = 3。又如 25 / 7 = 3 余 4，故 25 % 7 = 4。该运算符仅适用于整数操作数。

此运算符最常用于判断数字能否被另一个数整除：若 *x % y* 结果为 0，则说明 *x* 能被 *y* 整除。

```cpp
#include <iostream>

int main()
{
	std::cout << "请输入整数：";
	int x{};
	std::cin >> x;

	std::cout << "请输入另一个整数：";
	int y{};
	std::cin >> y;

	std::cout << "余数为：" << x % y << '\n';

	if ((x % y) == 0)
		std::cout << x << " 能被 " << y << " 整除\n";
	else
		std::cout << x << " 不能被 " << y << " 整除\n";

	return 0;
}
```

程序运行示例：

```
请输入整数：6
请输入另一个整数：3
余数为：0
6 能被 3 整除
```

```
请输入整数：6
请输入另一个整数：4
余数为：2
6 不能被 4 整除
```

当第二个数大于第一个数时：

```
请输入整数：2
请输入另一个整数：4
余数为：2
2 不能被 4 整除
```

余数 2 的原理是：2 / 4 的整数除法结果为 0 余 2。当第二个数更大时，第二个数会整除第一个数 0 次，故余数即为第一个数本身。

负数的取余运算
----------------

取余运算符支持负数操作数。`x % y` 的结果符号始终与 *x* 相同。

运行示例：

```
请输入整数：-6
请输入另一个整数：4
余数为：-2
-6 不能被 4 整除
```

```
请输入整数：6
请输入另一个整数：-4
余数为：2
6 不能被 -4 整除
```

可见余数的符号始终与第一个操作数一致。

术语说明
----------------

C++标准未正式命名`operator%`，但C++20标准指出："二元%运算符返回第一个表达式除以第二个表达式的余数"。

尽管常称其为"模"运算符，但在数学中模运算（modulo）与C++的取余运算（remainder）在负数处理上存在差异。例如数学中：  
-21 mod 4 = 3  
-21 rem 4 = -1

因此"取余"（remainder）是更准确的命名。

当第一个操作数可能为负时，需注意余数也可能为负。例如判断奇数的函数：

```cpp
bool isOdd(int x)
{
    return (x % 2) == 1; // 当x为-5时失效
}
```

当x为负奇数（如-5）时，`-5 % 2` 返回-1，导致判断错误。建议改为比较0：

```cpp
bool isOdd(int x)
{
    return (x % 2) != 0; // 可简写为 return (x % 2)
}
```

最佳实践
----------------
建议尽可能将取余运算结果与0比较。

幂运算实现
----------------

C++中*^*运算符表示按位异或，幂运算需使用\<cmath\>头文件中的pow()函数：

```cpp
#include <cmath>

double x{ std::pow(3.0, 4.0) }; // 3的4次方
```

注意pow()的参数和返回值为double类型，可能存在浮点精度问题。整数幂运算建议自定义函数，例如采用"快速幂"算法：

```cpp
#include <cassert>  // assert
#include <cstdint>  // std::int64_t
#include <iostream>

// 参数exp必须非负，注意无溢出检查
constexpr std::int64_t powint(std::int64_t base, int exp)
{
	assert(exp >= 0 && "powint: exp参数为负数");

	if (base == 0)
		return (exp == 0) ? 1 : 0;

	std::int64_t result{ 1 };
	while (exp > 0)
	{
		if (exp & 1)  // exp为奇数
			result *= base;
		exp /= 2;
		base *= base;
	}

	return result;
}

int main()
{
	std::cout << powint(7, 12) << '\n'; // 7的12次方
	return 0;
}
```

输出：
```
13841287201
```

相关阅读
----------------
- assert断言：见课程[9.6 — assert与static_assert](Chapter-9/lesson9.6-assert-and-static_assert.md)
- constexpr函数：见课程[F.1 — constexpr函数](Chapter-F/lessonF.1-constexpr-functions.md)

安全版幂函数（含溢出检查）：

```cpp
#include <cassert>
#include <cstdint>
#include <iostream>
#include <limits>

constexpr std::int64_t powint_safe(std::int64_t base, int exp)
{
    assert(exp >= 0 && "powint_safe: exp参数为负数");

    if (base == 0)
        return (exp == 0) ? 1 : 0;

    std::int64_t result{ 1 };
    bool negativeResult{ false };

    if (base < 0)
    {
        base = -base;
        negativeResult = (exp & 1);
    }

    while (exp > 0)
    {
        if (exp & 1)
        {
            if (result > std::numeric_limits<std::int64_t>::max() / base)
            {
                std::cerr << "powint_safe(): 结果溢出\n";
                return std::numeric_limits<std::int64_t>::max();
            }
            result *= base;
        }

        exp /= 2;
        if (exp <= 0) break;

        if (base > std::numeric_limits<std::int64_t>::max() / base)
        {
            std::cerr << "powint_safe(): 基数溢出\n";
            return std::numeric_limits<std::int64_t>::max();
        }

        base *= base;
    }

    return negativeResult ? -result : result;
}

int main()
{
	std::cout << powint_safe(7, 12) << '\n'; 
	std::cout << powint_safe(70, 12) << '\n'; // 触发溢出
	return 0;
}
```

测验
----------------

**问题1**  
表达式`6 + 5 * 4 % 3`的结果是？  
<details><summary>答案</summary>根据运算符优先级和结合性，计算顺序为：5*4=20 → 20%3=2 → 6+2=8</details>

**问题2**  
编写判断奇偶的constexpr函数：  
```cpp
#include <iostream>

constexpr bool isEven(int x)
{
    return (x % 2) == 0;
}

int main()
{
    std::cout << "输入整数：";
    int x{};
    std::cin >> x;

    std::cout << x << (isEven(x) ? " 是偶数\n" : " 是奇数\n");
    return 0;
}
```

[下一课 6.4 — 自增/自减运算符与副作用](Chapter-6/lesson6.4-increment-decrement-operators-and-side-effects.md)  
[返回主页](/)  
[上一课 6.2 — 算术运算符](Chapter-6/lesson6.2-arithmetic-operators.md)