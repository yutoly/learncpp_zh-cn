20.7 — Lambda捕获
=======================

[*nascardriver*](https://www.learncpp.com/author/nascardriver/ "查看 nascardriver 的所有文章")

2020年1月3日，太平洋标准时间上午5:19  
2024年12月4日

捕获子句与值捕获
----------------

上节课程（[20.6 — Lambda表达式（匿名函数）简介](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)）中我们引入了此示例：

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  auto found{ std::find_if(arr.begin(), arr.end(),
                           [](std::string_view str)
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

现在修改此示例，让用户选择要搜索的子字符串。结果可能不如预期直观：

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>
#include <string>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  // 要求用户输入搜索内容
  std::cout << "search for: ";

  std::string search{};
  std::cin >> search;

  auto found{ std::find_if(arr.begin(), arr.end(), [](std::string_view str) {
    // 搜索@search而非"nut"
    return str.find(search) != std::string_view::npos; // 错误：此作用域无法访问search
  }) };

  if (found == arr.end())
  {
    std::cout << "Not found\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
```

此代码无法编译。与嵌套块（外部块中所有可访问标识符在嵌套块中均可用）不同，Lambda仅能访问外部定义的特定类型对象，包括：
* 具有静态（或线程局部）存储期的对象（含全局变量和静态局部变量）
* constexpr对象（显式或隐式）

由于`search`不满足上述条件，Lambda无法访问它。

> **技巧**  
> Lambda仅能访问外部定义的特定类型对象，包括具有静态存储期的对象（如全局变量、静态局部变量）及constexpr对象。

为在Lambda内访问`search`，需使用捕获子句。

捕获子句
--------

**捕获子句（capture clause）**用于（间接）让Lambda访问外围作用域中通常无法访问的变量。只需在捕获子句中列出需访问的实体。本例中需让Lambda访问变量`search`的值，故将其加入捕获子句：

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>
#include <string>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  std::cout << "search for: ";

  std::string search{};
  std::cin >> search;

  // 捕获@search                                vvvvvv
  auto found{ std::find_if(arr.begin(), arr.end(), [search](std::string_view str) {
    return str.find(search) != std::string_view::npos;
  }) };

  if (found == arr.end())
  {
    std::cout << "Not found\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
```

用户现在可搜索数组元素。

输出：
```
search for: nana
Found banana
```

捕获机制如何运作？
----------------

虽然上例中的Lambda看似直接访问`main`的`search`变量，实则不然。Lambda看似嵌套块，但运作机制略有不同（此差异很重要）。

> **关键洞察**  
> Lambda捕获的变量是外部作用域变量的*副本*，而非原始变量。

> **进阶阅读**  
> 尽管Lambda形似函数，实则为可像函数般调用的对象（称为**函数对象（functors）**——后续课程将探讨如何从头创建函数对象）。  
> 编译器遇到Lambda定义时，会为其生成自定义对象定义。每个捕获变量成为该对象的数据成员。  
> 运行时遇到Lambda定义时实例化Lambda对象，此时初始化其成员。

捕获变量默认为const
------------------

调用Lambda时，会调用`operator()`。默认此运算符将捕获变量视为const，即Lambda不允许修改这些捕获变量。

下例尝试捕获变量`ammo`并递减：

```cpp
#include <iostream>

int main()
{
  int ammo{ 10 };

  // 定义Lambda并存入变量"shoot"
  auto shoot{
    [ammo]() {
      // 非法，ammo不可修改
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  // 调用Lambda
  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
```

此代码无法编译，因Lambda内`ammo`被视为const。

可变捕获
--------

为允许修改捕获变量，可将Lambda标记为`mutable`：

```cpp
#include <iostream>

int main()
{
  int ammo{ 10 };

  auto shoot{
    [ammo]() mutable { // 现在可变
      // 现在允许修改ammo
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  shoot();
  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
```

输出：
```
Pew! 9 shot(s) left.
Pew! 8 shot(s) left.
10 shot(s) left
```

虽然编译通过，但存在逻辑错误。原因何在？调用Lambda时，Lambda捕获的是`ammo`的*副本*。当Lambda将`ammo`从`10`递减至`9`再到`8`时，修改的是其自身副本，而非`main()`中的原始`ammo`值。

> **注意**  
> 由于捕获变量是Lambda对象的成员，其值在多次Lambda调用间持续存在！

> **警告**  
> 捕获变量是Lambda对象的成员，其值在多次调用间持久化！

引用捕获
--------

类似函数可通过引用传递修改实参值，我们也可通过引用捕获变量使Lambda影响参数值。

要引用捕获变量，在捕获子句的变量名前添加`&`符号。与值捕获不同，引用捕获的变量为非const（除非被捕获变量本身为`const`）。只要通常倾向于函数传引用（如非基础类型），应优先引用捕获而非值捕获。

下例通过引用捕获`ammo`：

```cpp
#include <iostream>

int main()
{
  int ammo{ 10 };

  auto shoot{
    // 不再需要mutable
    [&ammo]() { // &ammo表示通过引用捕获ammo
      // 修改ammo将影响main的ammo
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
```

输出符合预期：
```
Pew! 9 shot(s) left.
9 shot(s) left
```

现在使用引用捕获统计`std::sort`排序数组时的比较次数：

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

struct Car
{
  std::string_view make{};
  std::string_view model{};
};

int main()
{
  std::array<Car, 3> cars{ { { "Volkswagen", "Golf" },
                             { "Toyota", "Corolla" },
                             { "Honda", "Civic" } } };

  int comparisons{ 0 };

  std::sort(cars.begin(), cars.end(),
    // 通过引用捕获@comparisons
    [&comparisons](const auto& a, const auto& b) {
      // 通过引用捕获comparisons，无需"mutable"即可修改
      ++comparisons;

      // 按制造商排序
      return a.make < b.make;
  });

  std::cout << "Comparisons: " << comparisons << '\n';

  for (const auto& car : cars)
  {
    std::cout << car.make << ' ' << car.model << '\n';
  }

  return 0;
}
```

可能输出：
```
Comparisons: 2
Honda Civic
Toyota Corolla
Volkswagen Golf
```

捕获多个变量
-----------

多个变量可通过逗号分隔捕获，可混合值捕获与引用捕获：

```cpp
int health{ 33 };
int armor{ 100 };
std::vector<CEnemy> enemies{};

// 值捕获health和armor，引用捕获enemies
[health, armor, &enemies](){};
```

默认捕获
-------

显式列出需捕获变量可能繁琐。若修改Lambda，可能遗漏增删捕获变量。幸运的是，可借助编译器自动生成需捕获变量列表。

**默认捕获（default capture）**（亦称**捕获默认（capture-default）**）会捕获Lambda中提及的所有变量。未提及的变量即使使用默认捕获也不会被捕获。

要值捕获所有已用变量，使用捕获值`=`。  
要引用捕获所有已用变量，使用捕获值`&`。

下例展示值默认捕获：

```cpp
#include <algorithm>
#include <array>
#include <iostream>

int main()
{
  std::array areas{ 100, 25, 121, 40, 56 };

  int width{};
  int height{};

  std::cout << "Enter width and height: ";
  std::cin >> width >> height;

  auto found{ std::find_if(areas.begin(), areas.end(),
                           [=](int knownArea) { // 默认值捕获width和height
                             return width * height == knownArea; // 因在此处提及
                           }) };

  if (found == areas.end())
  {
    std::cout << "I don't know this area :(\n";
  }
  else
  {
    std::cout << "Area found :)\n";
  }

  return 0;
}
```

默认捕获可与常规捕获混合使用。可值捕获部分变量并引用捕获其他变量，但每个变量仅能捕获一次。

```cpp
int health{ 33 };
int armor{ 100 };
std::vector<CEnemy> enemies{};

// 值捕获health和armor，引用捕获enemies
[health, armor, &enemies](){};

// 引用捕获enemies，值捕获其余变量
[=, &enemies](){};

// 值捕获armor，引用捕获其余变量
[&, armor](){};

// 非法，已声明引用捕获所有变量
[&, &armor](){};

// 非法，已声明值捕获所有变量
[=, armor](){};

// 非法，armor重复出现
[armor, &health, &armor](){};

// 非法，默认捕获必须是捕获组首元素
[armor, &](){};
```

Lambda捕获中定义新变量
---------------------

有时需捕获稍作修改的变量，或声明仅Lambda作用域内可见的新变量。可通过在Lambda捕获中定义变量实现（无需指定类型）：

```cpp
#include <array>
#include <iostream>
#include <algorithm>

int main()
{
  std::array areas{ 100, 25, 121, 40, 56 };

  int width{};
  int height{};

  std::cout << "Enter width and height: ";
  std::cin >> width >> height;

  // 存储areas，但用户输入width和height
  // 需先计算面积才能搜索
  auto found{ std::find_if(areas.begin(), areas.end(),
                           // 声明仅Lambda可见的新变量
                           // userArea类型自动推导为int
                           [userArea{ width * height }](int knownArea) {
                             return userArea == knownArea;
                           }) };

  if (found == areas.end())
  {
    std::cout << "I don't know this area :(\n";
  }
  else
  {
    std::cout << "Area found :)\n";
  }

  return 0;
}
```

`userArea`仅在Lambda定义时计算一次。计算结果存入Lambda对象，每次调用均相同。若可变Lambda修改了捕获中定义的变量，将覆盖原始值。

> **最佳实践**  
> 仅当变量值简短且类型明确时，方在捕获中初始化变量。否则应在Lambda外部定义变量并捕获。

悬挂捕获变量
-----------

变量在Lambda定义时捕获。若引用捕获的变量先于Lambda消亡，Lambda将持有悬挂引用。

例如：

```cpp
#include <iostream>
#include <string>

// 返回Lambda
auto makeWalrus(const std::string& name)
{
  // 引用捕获name并返回Lambda
  return [&]() {
    std::cout << "I am a walrus, my name is " << name << '\n'; // 未定义行为
  };
}

int main()
{
  // 创建名为Roofus的新海象
  // sayName是makeWalrus返回的Lambda
  auto sayName{ makeWalrus("Roofus") };

  // 调用makeWalrus返回的Lambda函数
  sayName();

  return 0;
}
```

`makeWalrus()`调用从字符串字面量`"Roofus"`创建临时`std::string`。`makeWalrus()`中的Lambda通过引用捕获此临时字符串。临时字符串在包含`makeWalrus()`调用的完整表达式结束时消亡，但Lambda`sayName`仍持有其引用。因此调用`sayName`时将访问悬挂引用，导致未定义行为。

注意：若`"Roofus"`通过值传递给`makeWalrus()`也会发生此情况。参数`name`在`makeWalrus()`结束时消亡，Lambda仍持有悬挂引用。

> **警告**  
> 引用捕获变量（尤其是默认引用捕获）时需格外谨慎。被捕获变量必须比Lambda生命周期更长。

若希望捕获的`name`在Lambda使用时有效，需改为值捕获（显式或默认值捕获）。

可变Lambda的意外拷贝
-------------------

由于Lambda是对象，可被拷贝。某些情况下会导致问题。考虑以下代码：

```cpp
#include <iostream>

int main()
{
  int i{ 0 };

  // 创建新Lambda命名count
  auto count{ [i]() mutable {
    std::cout << ++i << '\n';
  } };

  count(); // 调用count

  auto otherCount{ count }; // 创建count的拷贝

  // 调用count及其拷贝
  count();
  otherCount();

  return 0;
}
```

输出：
```
1
2
2
```

代码未输出1,2,3而是输出了两次2。创建`otherCount`作为`count`的拷贝时，复制的是`count`的当前状态。`count`的`i`为1，故`otherCount`的`i`也为1。由于`otherCount`是`count`的拷贝，两者各有自己的`i`。

再看稍复杂的例子：

```cpp
#include <iostream>
#include <functional>

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // 递增并打印其局部副本@i
    auto count{ [i]() mutable {
      std::cout << ++i << '\n';
    } };

    myInvoke(count);
    myInvoke(count);
    myInvoke(count);

    return 0;
}
```

输出：
```
1
1
1
```

此问题与前例相同但更隐蔽。

调用`myInvoke(count)`时，编译器发现`count`（Lambda类型）与引用参数类型（`std::function<void()>`）不匹配。会将Lambda转换为临时`std::function`使引用参数可绑定，这将创建Lambda的拷贝。因此`fn()`实际执行的是临时`std::function`中的Lambda拷贝，而非原始Lambda。

若需传递可变Lambda并避免意外拷贝，有两种选择：
1. 使用无捕获Lambda——上例中可移除捕获并用静态局部变量跟踪状态。但静态局部变量难以追踪且降低代码可读性。
2. 从源头防止Lambda拷贝。由于无法影响`std::function`（或其他标准库函数/对象）的实现，如何操作？

方案一（感谢读者Dck）：立即将Lambda存入`std::function`。这样调用`myInvoke()`时，引用参数`fn`可绑定到`std::function`，且不创建临时拷贝：

```cpp
#include <iostream>
#include <functional>

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // 递增并打印其局部副本@i
    std::function count{ [i]() mutable { // Lambda对象存入std::function
      std::cout << ++i << '\n';
    } };

    myInvoke(count); // 调用时不创建拷贝
    myInvoke(count); // 调用时不创建拷贝
    myInvoke(count); // 调用时不创建拷贝

    return 0;
}
```

输出符合预期：
```
1
2
3
```

替代方案是使用引用包装器。C\+\+在\<functional\>头文件中提供便捷类型`std::reference_wrapper`，允许像传递引用般传递普通类型。为简化操作，可用`std::ref()`函数创建`std::reference_wrapper`。通过将Lambda包装进`std::reference_wrapper`，任何尝试拷贝Lambda的操作实际拷贝的是reference_wrapper（避免拷贝Lambda）。

更新后的代码使用`std::ref`：

```cpp
#include <iostream>
#include <functional> // 含std::reference_wrapper和std::ref

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // 递增并打印其局部副本@i
    auto count{ [i]() mutable {
      std::cout << ++i << '\n';
    } };

    // std::ref(count)确保count被视为引用
    // 任何尝试拷贝count的操作实际拷贝的是引用
    // 确保仅存在一个count副本
    myInvoke(std::ref(count));
    myInvoke(std::ref(count));
    myInvoke(std::ref(count));

    return 0;
}
```

输出符合预期：
```
1
2
3
```

此方法在`myInvoke`按值（而非引用）接收`fn`时依然有效！

> **规则**  
> 标准库函数可能拷贝函数对象（注：Lambda是函数对象）。若需提供含可变捕获变量的Lambda，请使用`std::ref`通过引用传递。

> **最佳实践**  
> 尽量避免可变Lambda。不可变Lambda更易理解且不受上述问题影响，在并行执行时也不会引发更危险的问题。

测验时间
--------

**问题1**  
以下哪些变量可在`main`的Lambda中不显式捕获直接使用？

```cpp
int i{};
static int j{};

int getValue()
{
  return 0;
}

int main()
{
  int a{};
  constexpr int b{};
  static int c{};
  static constexpr int d{};
  const int e{};
  const int f{ getValue() };
  static const int g{}; 
  static const int h{ getValue() }; 

  [](){
    // 尝试不显式捕获直接使用变量
    a;
    b;
    c;
    d;
    e;
    f;
    g;
    h;
    i;
    j;
  }();

  return 0;
}
```



| 变量 | 无需显式捕获 | 原因 |
|------|--------------|------|
| `a`  | 否           | `a`具有自动存储期 |
| `b`  | 是           | `b`可用于常量表达式 |
| `c`  | 是           | `c`具有静态存储期 |
| `d`  | 是           | 同上 |
| `e`  | 是           | `e`可用于常量表达式 |
| `f`  | 否           | `f`的值依赖`getValue()`（需程序运行） |
| `g`  | 是           | 具有静态存储期 |
| `h`  | 是           | `h`具有静态存储期 |
| `i`  | 是           | `i`是全局变量 |
| `j`  | 是           | `j`在整个文件可访问 |

**问题2**  
以下代码输出什么？（勿运行代码，思考作答）

```cpp
#include <iostream>
#include <string>

int main()
{
  std::string favoriteFruit{ "grapes" };

  auto printFavoriteFruit{
    [=]() {
      std::cout << "I like " << favoriteFruit << '\n';
    }
  };

  favoriteFruit = "bananas with chocolate";

  printFavoriteFruit();

  return 0;
}
```



```
I like grapes
```

`printFavoriteFruit`通过值捕获`favoriteFruit`。修改`main`的`favoriteFruit`不影响Lambda的`favoriteFruit`。

**问题3**  
编写平方数（可表示为整数自乘的数：1,4,9,16,25,...）小游戏。

游戏设置：
* 要求用户输入起始数字（如3）
* 要求用户指定生成数量
* 随机选取2至4间的整数作为乘数
* 生成用户指定数量的值。从起始数开始，每个值应为下一个平方数乘以乘数

游戏流程：
* 用户输入猜测
* 若匹配任意生成值，移除该值并允许再次猜测
* 若猜中所有生成值，获胜
* 若未匹配生成值，失败并提示最近未猜中值

参考游戏会话：

```
Start where? 4
How many? 5
I generated 5 square numbers. Do you know what each number is after multiplying it by 2?
> 32
Nice! 4 number(s) left.
> 72
Nice! 3 number(s) left.
> 50
Nice! 2 number(s) left.
> 126
126 is wrong! Try 128 next time.
```

* 起始数4生成后5个平方数：16,25,36,49,64
* 程序随机选取乘数2，故每个平方数乘以2：32,50,72,98,128
* 用户猜测
* 32在列表中
* 72在列表中
* 126不在列表，用户失败。最近未猜中值为128

```
Start where? 1
How many? 3
I generated 3 square numbers. Do you know what each number is after multiplying it by 4?
> 4
Nice! 2 number(s) left.
> 16
Nice! 1 number(s) left.
> 36
Nice! You found all numbers, good job!
```

* 起始数1生成后3个平方数：1,4,9
* 程序随机选取乘数4，故每个平方数乘以4：4,16,36
* 用户猜中所有数字获胜

提示：
* 使用Random.h（[8.15 — 全局随机数（Random.h）](Chapter-8/lesson8.15-global-random-numbers-random-h.md)）生成随机数
* 使用`std::find()`（[18.3 — 标准库算法简介](introduction-to-standard-library-algorithms/#std_find)）搜索列表中的数字
* 使用`std::vector::erase()`移除元素，例如：

```cpp
auto found{ std::find(/* ... */) };

// 确保找到元素
myVector.erase(found);
```

* 使用`std::min_element`和Lambda查找最接近用户猜测的数。`std::min_element`运作方式类似上节测验中的`std::max_element`

[查看提示](javascript:void(0))

提示：使用\<cmath\>中的`std::abs`计算两数绝对差：
```cpp
int distance{ std::abs(3 - 5) }; // 2
```



```cpp
#include <algorithm> // std::find, std::min_element
#include <cmath> // std::abs
#include <cstddef> // std::size_t
#include <iostream>
#include <vector>
#include "Random.h"

using Numbers = std::vector<int>;

namespace config
{
    constexpr int multiplierMin{ 2 };
    constexpr int multiplierMax{ 6 };
}

// 生成从@start*@start开始的@count个数
// 每个平方数乘以@multiplier
Numbers generateNumbers(int start, int count, int multiplier)
{
    Numbers numbers(static_cast<std::size_t>(count));

    for (int index = 0; index < count; ++index)
    {
        std::size_t uindex{ static_cast<std::size_t>(index) };
        numbers[uindex] = (start + index) * (start + index) * multiplier;
    }

    return numbers;
}

// 要求用户输入起始数，随后生成数字数组
Numbers setupGame()
{
    int start{};
    std::cout << "Start where? ";
    std::cin >> start;

    int count{};
    std::cout << "How many? ";
    std::cin >> count;

    int multiplier{ Random::get(config::multiplierMin, config::multiplierMax) };

    std::cout << "I generated " << count
        << " square numbers. Do you know what each number is after multiplying it by "
        << multiplier << "?\n";

    return generateNumbers(start, count, multiplier);
}

// 获取用户猜测
int getUserGuess()
{
    int guess{};

    std::cout << "> ";
    std::cin >> guess;

    return guess;
}

// 在@numbers中搜索@guess并移除
// 若找到值则返回true，否则false
bool findAndRemove(Numbers& numbers, int guess)
{
    auto found{ std::find(numbers.begin(), numbers.end(), guess) };

    if (found == numbers.end())
        return false;

    numbers.erase(found);
    return true;
}

// 在@numbers中查找最接近@guess的值
int findClosestNumber(const Numbers& numbers, int guess)
{
    return *std::min_element(numbers.begin(), numbers.end(),
        [=](int a, int b)
        {
            return std::abs(a - guess) < std::abs(b - guess);
        });
}

// 用户猜中数字时调用
void printSuccess(const Numbers& numbers)
{
    std::cout << "Nice! ";

    if (numbers.size() == 0)
    {
        std::cout << "You found all numbers, good job!\n";
    }
    else
    {
        std::cout << numbers.size() << " number(s) left.\n";
    }
}

// 用户猜中不在numbers中的数字时调用
void printFailure(const Numbers& numbers, int guess)
{
    int closest{ findClosestNumber(numbers, guess) };

    std::cout << guess << " is wrong!\n";

    std::cout << "Try " << closest << " next time.\n";
}

int main()
{
    Numbers numbers{ setupGame() };

    while (true)
    {
        int guess{ getUserGuess() };

        if (!findAndRemove(numbers, guess))
        {
            printFailure(numbers, guess);
            break;
        }
        
        printSuccess(numbers);
        if (numbers.size() == 0)
            break;
    }

    return 0;
}
```

[下一课 20.x — 第20章总结与测验](Chapter-20/lesson20.x-chapter-20-summary-and-quiz.md)  
[返回主页](/)    
[上一课 20.6 — Lambda表达式（匿名函数）简介](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)