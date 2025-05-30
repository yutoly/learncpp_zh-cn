20.6 — Lambda表达式（匿名函数）简介
=====================================================

[*作者：nascardriver*](https://www.learncpp.com/author/nascardriver/ "查看nascardriver的所有文章")  
2020年1月3日 上午5:19（太平洋标准时间）  
2024年6月14日更新  

请观察我们在课程[18.3 — 标准库算法简介](Chapter-18/lesson18.3-introduction-to-standard-library-algorithms.md)中介绍的代码片段：
```
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

// 若元素匹配则返回true
bool containsNut(std::string_view str)
{
    // 若未找到子串，std::string_view::find返回std::string_view::npos
    return str.find("nut") != std::string_view::npos;
}

int main()
{
    constexpr std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

    // 扫描数组查找包含"nut"子串的元素
    auto found{ std::find_if(arr.begin(), arr.end(), containsNut) };

    if (found == arr.end())
    {
        std::cout << "No nuts\n";
    }
    else
    {
        std::cout << "Found " << *found << '\n';
    }

    return 0;
}
```
这段代码虽然有效，但仍有改进空间。核心问题在于`std::find_if`需要函数指针参数，这迫使我们定义仅使用一次的具名全局函数。对于简短函数，通过代码理解其功能往往比通过名称和注释更直观。

Lambda是匿名函数
----------------
**lambda表达式**（lambda或闭包（closure））允许在函数内部定义匿名函数。这种嵌套特性既能避免命名空间污染，又能就近定义函数（提供更多上下文信息）。

lambda语法是C++中最奇特的形式之一，其基本结构为：
```
[捕获子句] (参数) -> 返回类型
{
    语句;
}
```
* 若无捕获需求，捕获子句可为空  
* 若无参数需求，参数列表可为空（指定返回类型时必须保留空括号）  
* 返回类型可省略（此时自动推导为`auto`）。虽然通常不建议函数返回类型自动推导，但lambda函数因简洁性可例外使用  

匿名lambda没有名称，因此无需命名。

> **旁注**  
> 最简单的lambda定义示例：
> ```
> [] {}; // 省略返回类型、无捕获、无参数的lambda
> ```

使用lambda重写示例：
```
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  // 在使用处直接定义函数
  auto found{ std::find_if(arr.begin(), arr.end(),
                           [](std::string_view str) // 定义lambda，无捕获子句
                           {
                             return str.find("nut") != std::string_view::npos;
                           }) };

  if (found == arr.end())
  {
    std::cout << "No nuts\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
```
此实现与函数指针版本功能相同，输出结果一致：
```
Found walnut
```

> **最佳实践**  
> 遵循"最小作用域"和"就近定义"原则，在需要传递简单一次性函数时优先使用lambda。

Lambda的类型
----------------
上述示例中，lambda直接定义在使用处，这种用法称为**函数字面量（function literal）**。但行内定义可能影响可读性。与变量初始化类似，我们可以先定义lambda变量再后续使用。合理命名的lambda能提升代码可读性。

例如，使用`std::all_of`检查数组元素是否全为偶数：
```
// 较差：需阅读lambda才能理解逻辑
return std::all_of(array.begin(), array.end(), [](int i){ return ((i % 2) == 0); });

// 较好：将lambda存入命名变量
auto isEven{
  [](int i)
  {
    return (i % 2) == 0;
  }
};
return std::all_of(array.begin(), array.end(), isEven);
```

> **关键洞察**  
> 将lambda存入变量可赋予其有意义名称，提升代码可读性，并支持重复使用。

lambda的实际类型由编译器生成唯一类型，无法显式指定。对于空捕获的lambda，可使用常规函数指针。其他情况下可使用`std::function`或`auto`：
```
#include <functional>

int main()
{
  // 常规函数指针（仅适用于空捕获lambda）
  double (*addNumbers1)(double, double){
    [](double a, double b) { return a + b; }
  };

  // 使用std::function（可处理非空捕获）
  std::function addNumbers2{ // C++17前需指定std::function<double(double, double)>
    [](double a, double b) { return a + b; }
  };

  // 使用auto（存储实际类型）
  auto addNumbers3{
    [](double a, double b) { return a + b; }
  };

  return 0;
}
```

> **最佳实践**  
> 存储lambda时使用`auto`类型。传递lambda给函数时：  
> * 支持C++20则用`auto`参数  
> * 否则使用模板参数或`std::function`（无捕获时可用函数指针）

通用Lambda
----------------
C++14起允许lambda参数使用`auto`（C++20扩展至常规函数）。当lambda含`auto`参数时，编译器根据调用推断参数类型，这类lambda称为**通用lambda（generic lambda）**。

示例：查找首字母相同的连续月份：
```
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array months{ // C++17前使用std::array<const char*, 12>
    "January", "February", /*...*/ "December"
  };

  const auto sameLetter{ std::adjacent_find(months.begin(), months.end(),
                                      [](const auto& a, const auto& b) {
                                        return a[0] == b[0];
                                      }) };

  if (sameLetter != months.end())
  {
    std::cout << *sameLetter << " 与 " << *std::next(sameLetter)
              << " 首字母相同\n";
  }
}
```
输出：
```
June 与 July 首字母相同
```

常量表达式Lambda
----------------
C++17起，若lambda结果满足常量表达式要求，则隐式成为`constexpr`。主要要求：  
* 无捕获或所有捕获为`constexpr`  
* 调用的函数必须`constexpr`（许多标准库算法和数学函数在C++20/23才支持）

示例：统计5字母月份（C++20起可`constexpr`）：
```
constexpr auto fiveLetterMonths{ std::count_if(months.begin(), months.end(),
                                       [](std::string_view str) {
                                         return str.length() == 5;
                                       }) };
```

通用Lambda与静态变量
----------------
通用lambda为每个推断类型生成独立lambda，各自拥有静态局部变量副本：
```
auto print{
  [](auto value) {
    static int callCount{ 0 }; // 每个类型独立计数
    std::cout << callCount++ << ": " << value << '\n';
  }
};
print("hello"); // 0: hello（字符串版本）
print(1);       // 0: 1（整数版本）
```

返回类型推断
----------------
使用返回类型推断时，所有`return`语句必须返回相同类型。若类型不同需显式指定返回类型：
```
auto divide{ [](int x, int y, bool intDivision) -> double {
  if (intDivision)
    return x / y; // 隐式转换为double
  else
    return static_cast<double>(x) / y;
} };
```

标准库函数对象
----------------
常见操作（如比较、算术）可使用标准库函数对象（定义于<functional>）替代自定义lambda：
```
#include <functional>
std::sort(arr.begin(), arr.end(), std::greater{}); // 使用标准库比较器
```

结语
----------------
lambda与算法库结合能在简洁代码中实现强大功能，比循环更易维护且支持并行。但非平凡或可重用场景仍应使用常规函数。

测验
----------------
**问题1**  
创建`Student`结构体，使用`std::max_element`查找最高分学生：
```
// 解决方案关键lambda
[](const auto& a, const auto& b) { return a.points < b.points; }
```

**问题2**  
使用`std::sort`按温度升序排列季节：
```
std::sort(seasons.begin(), seasons.end(),
          [](const auto& a, const auto& b) {
            return a.averageTemperature < b.averageTemperature;
          });
```

[下一课 20.7 — Lambda捕获](Chapter-20/lesson20.7-lambda-captures.md)  
[返回主页](/)  
[上一课 20.5 — 省略号（及其弊端）](Chapter-20/lesson20.5-ellipsis-and-why-to-avoid-them.md)