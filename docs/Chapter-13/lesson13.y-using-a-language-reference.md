13.y — 使用语言参考
==================================

[*nascardriver*](https://www.learncpp.com/author/nascardriver/ "查看 nascardriver 的所有文章")

2020年1月30日上午9:04（太平洋标准时间）  
2024年1月2日

根据您学习编程语言（尤其是C++）的进度，LearnCpp.com可能是您学习C++或查阅资料的唯一资源。LearnCpp.com旨在以初学者友好的方式解释概念，但无法涵盖语言的每个方面。当您开始探索教程未覆盖的主题时，难免会遇到教程未解答的问题。此时需要借助外部资源。

[Stack Overflow](https://stackoverflow.com)是此类资源之一，您可在此提问（或更佳方式是阅读前人对相同问题的解答）。但更好的首选资源是参考指南。教程通常聚焦重点主题并使用非正式/通用语言以降低学习门槛，而参考指南则使用正式术语精确描述C++。因此参考材料往往全面、准确且…难以理解。

本节通过研究3个案例，演示如何使用[cppreference](https://cppreference.com)——我们教程中引用的流行标准参考。

概述
----------------

Cppreference首页展示核心语言与库的[概览](https://en.cppreference.com/w/cpp)：

表格上半部展示当前语言特性，下半部列出技术规范（可能在未来版本添加或已部分纳入的特性）。这对了解即将推出的新功能很有帮助。

自C++11起，cppreference用绿色数字标记特性引入的标准版本（如上图链接旁的数字）。无版本标记的特性自C++98/03起可用。版本号不仅出现在概览页，还遍布整个站点，明确指示各C++版本支持的功能。

> **注意**  
> 若技术规范刚被纳入标准，搜索引擎可能优先链接技术规范而非官方参考（两者内容可能有差异）。

> **提示**  
> Cppreference同时提供C++和C的参考。由于C++与C共享部分函数名，搜索时可能进入C参考页面。URL和顶部导航栏会明确显示当前浏览的是C还是C++参考。

std::string::length
----------------

首先研究已知函数`std::string::length`（返回字符串长度）。

在cppreference右上角搜索"string"，结果列表中顶部内容最相关：

点击"Strings library"进入介绍各类字符串的页面。在"std::basic_string"区域可见类型别名列表，其中包含std::string：

点击"std::string"进入[`std::basic_string`](https://en.cppreference.com/w/cpp/string/basic_string)页面（因`std::string`是`std::basic_string<char>`的类型别名）。`<char>`表示字符串字符类型为`char`。C++还提供使用其他字符类型的字符串（适用于Unicode场景）。

同页下方的[成员函数列表](https://en.cppreference.com/w/cpp/string/basic_string#Member_functions)中可找到`length`和`size`（两者功能相同）：

点击链接进入[`length`与`size`](https://en.cppreference.com/w/cpp/string/basic_string/size)的详细说明页：

页面顶部是特性语法摘要及不同重载版本的标准支持信息：

下方说明函数参数与返回值含义：

由于`std::string::length`是简单函数，内容较少。多数页面包含示例代码（本页也有）：

学习C++时，示例中可能出现未知特性。若示例足够多，通常可理解函数用法与功能。若示例过于复杂，可搜索其他示例或查阅相关特性的参考文档（示例中的函数和类型均可点击查看说明）。

现在已了解`std::string::length`的功能（虽然之前已知）。接下来探索新内容！

std::cin.ignore
----------------

在课程[9.5 — std::cin与处理无效输入](Chapter-9/lesson9.5-stdcin-and-handling-invalid-input.md)中，我们使用`std::cin.ignore`忽略换行符前的所有内容。该函数的某个参数包含冗长值，其作用是什么？能否直接使用大数字？让我们一探究竟！

在cppreference搜索"std::cin.ignore"得到结果：

* `std::cin, std::wcin` - 我们需要`.ignore`而非`std::cin`本身
* `std::basic_istream<CharT,Traits>::ignore` - 暂跳过
* `std::ignore` - 不符要求
* `std::basic_istream` - 不符要求

未找到目标？转向[`std::cin`](https://en.cppreference.com/w/cpp/io/cin)页面。顶部可见`std::cin`和`std::wcin`的声明及所需头文件：

可见`std::cin`是`std::istream`类型对象。点击链接进入[`std::istream`](https://en.cppreference.com/w/cpp/io/basic_istream)：

注意！搜索时出现的`std::basic_istream`实为`istream`的类型别名。向下滚动可见熟悉函数列表：

我们使用过其中许多函数：`operator>>`、`get`、`getline`、`ignore`。浏览页面后点击目标函数[`ignore`](https://en.cppreference.com/w/cpp/io/basic_istream/ignore)：

顶部是函数签名和功能说明。参数后的`=`表示**默认参数**（详见课程[11.5 — 默认参数](Chapter-11/lesson11.5-default-arguments.md)）。若省略带默认值的参数，则使用默认值。

第一条说明解答了所有疑问：`std::numeric_limits<std::streamsize>::max()`对`std::cin.ignore`有特殊含义——禁用字符数检查。这意味着`std::cin.ignore`将持续忽略字符直至找到分隔符或无字符可读。

若已知函数功能但忘记参数含义，通常无需阅读完整说明。此时阅读参数或返回值描述即可：

参数描述简明扼要。虽未提及`std::numeric_limits<std::streamsize>::max()`的特殊处理或其他终止条件，但足以唤醒记忆。

语言语法示例
----------------

除标准库外，cppreference还记录语言语法。以下有效程序为例：

```cpp
#include <iostream>

int getUserInput()
{
  int i{};
  std::cin >> i;
  return i;
}

int main()
{
  std::cout << "How many bananas did you eat today? \n";

  if (int iBananasEaten{ getUserInput() }; iBananasEaten <= 2)
  {
    std::cout << "Yummy\n";
  }
  else
  {
    std::cout << iBananasEaten << " is a lot!\n";
  }

  return 0;  
}
```

为何`if语句`条件内出现变量定义？通过搜索引擎搜索"cppreference if statement"进入[if语句](https://en.cppreference.com/w/cpp/language/if)页面。顶部是语法参考：

观察`if语句`语法。移除所有可选部分后即得到已知形式。`条件`前的可选`init-statement`（初始化语句）正对应上述代码：

```
if ( init-statement condition ) statement-true
if ( init-statement condition ) statement-true else statement-false
```

语法说明下方逐部分解释（含`init-statement`），指出其通常为带初始化器的变量声明。

语法说明后是`if语句`解释及简单示例：

已知`if语句`工作原理，但示例未含`init-statement`。向下滚动找到初始化语句专节：

首先展示如何在不使用初始化语句的情况下实现相同功能。由此理解代码行为：本质是普通变量声明，只是与`if语句`合并。

后续说明特别指出：`init-statement`中的名称在*两个*分支（`statement-true`和`statement-false`）中均可用。这可能有违直觉（因通常假设变量仅限真值分支使用）。

示例中使用了未涉及的特性和类型。无需理解全部内容即可掌握`init-statement`机制。跳过复杂部分寻找可理解示例：

```cpp
// 迭代器（iterators），跳过
if (auto it = m.find(10); it != m.end()) { return it->second.size(); }

// [10]是什么？跳过
if (char buf[10]; std::fgets(buf, 10, stdin)) { m[0] += buf; }

// std::lock_guard未知，但识别为类型
if (std::lock_guard lock(mx); shared_flag) { unsafe_ping(); shared_flag = false; }

// 简单示例（整型）
if (int s; int count = ReadBytesWithSignal(&s)) { publish(count); raise(s); }

// 跳过复杂示例
if (auto keywords = {"if", "for", "while"};
    std::any_of(keywords.begin(), keywords.end(),
                [&s](const char* kw) { return s == kw; })) {
  std::cerr << "Token must not be a keyword\n";
}
```

最简示例为`整型`部分。但分号后出现另一定义…返回`std::lock_guard`示例：

```cpp
if (std::lock_guard lock(mx); shared_flag)
{
  unsafe_ping();
  shared_flag = false;
}
```

可清晰看出`init-statement`结构：先定义变量（`lock`），分号后接条件。这正是原始示例的运作方式。

关于cppreference准确性的警告
----------------

Cppreference非官方文档源（实为维基站点）。维基内容由社区贡献/修改，虽存在误加错误信息的风险，但通常能被快速修正，使其成为可靠来源。

C++唯一官方来源是[标准文档](https://isocpp.org/std/the-standard)（[GitHub免费草案](https://github.com/cplusplus/draft/tree/master/papers)），属正式文件且不易用作参考。

测验时间
----------------

**问题1**  
以下程序输出什么？勿运行代码，通过参考文档查询`erase`功能。

```cpp
#include <iostream>
#include <string>

int main()
{
  std::string str{ "The rice is cooking" };
  str.erase(4, 11);
  std::cout << str << '\n';
  return 0;
}
```

> **提示**  
> 在cppreference找到`erase`后，可忽略迭代器重载版本。  
> C++索引从0开始。字符串"House"索引0的字符是'H'，索引1是'o'，依此类推。

  
<details><summary>答案</summary>The king</details>

**解决路径**  
搜索"string"并点击"std::string"进入[`std::basic_string`](https://en.cppreference.com/w/cpp/string/basic_string)。在"成员函数"列表中找到[erase](https://en.cppreference.com/w/cpp/string/basic_string/erase)。根据提示，第一个**函数重载**接收两个`size_type`（无符号整型）参数。示例中为4和11。根据(1)的描述：删除"从`index`开始的`min(count, size() - index)`个字符"。代入参数得：从索引4开始删除`min(11, 19 - 4) = 11`个字符。

**问题2**  
修改以下代码中的`str`，使其值为"I saw a blue car yesterday."（不重复字符串）。例如勿直接赋值：

```cpp
str = "I saw a blue car yesterday.";
```

仅需调用一个函数将"red"替换为"blue"。

```cpp
#include <iostream>
#include <string>

int main()
{
  std::string str{ "I saw a red car yesterday." };  
  // ...（替换操作）
  std::cout << str << '\n'; // 输出：I saw a blue car yesterday.
  return 0;
}
```

[查看提示](javascript:void(0))  
<details><summary>提示1</summary>[`std::basic_string`](https://en.cppreference.com/w/cpp/string/basic_string)</details>  
[查看提示](javascript:void(0))  
<details><summary>提示2</summary>[`std::basic_string`的成员函数](https://en.cppreference.com/w/cpp/string/basic_string#Member_functions)</details>  
[查看提示](javascript:void(0))  
<details><summary>提示3</summary>[`std::basic_string`的修改器](https://en.cppreference.com/w/cpp/string/basic_string#modifiers)</details>  
[查看提示](javascript:void(0))  
<details><summary>提示4</summary>[`std::basic_string::replace`](https://en.cppreference.com/w/cpp/string/basic_string/replace)</details>  
  
<details><summary>答案</summary>str.replace(8, 3, "blue");</details>

[下一课 14.1 — 面向对象编程导论](Chapter-14/lesson14.1-introduction-to-object-oriented-programming.md)  
[返回主页](/)  
[上一课 13.x — 第13章总结与测验](Chapter-13/lesson13.x-chapter-13-summary-and-quiz.md)