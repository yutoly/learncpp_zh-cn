5\.x — 第5章总结与测验  
=================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2023年10月23日 PDT下午1:50  
2024年12月2日  

本章回顾  
----------------  

**常量（constant）**是在程序执行期间不可修改的值。C++支持两种常量类型：具名常量（named constants）和字面常量（literals）。  

**具名常量**是与标识符关联的常量值。**字面常量**是不关联标识符的常量值。  

值不可变的变量称为**常量变量（constant variable）**。**const**关键字用于创建常量变量。常量变量必须初始化。避免在按值传递或按值返回时使用`const`。  

**类型限定符（type qualifier）**是应用于类型的关键字，用于修改类型行为。截至C++23，C++仅支持`const`和`volatile`作为类型限定符。  

**常量表达式（constant expression）**是可在编译期求值的表达式。非常量表达式有时称为**运行时表达式（runtime expression）**。  

**编译期常量（compile-time constant）**是值在编译期已知的常量。**运行时常量（runtime constant）**是初始化值直到运行时才确定的常量。  

**constexpr**变量必须是编译期常量，并用常量表达式初始化。函数参数不能是constexpr。  

**字面量（literals）**是直接插入代码的值。字面量具有类型，可通过字面量后缀（literal suffixes）改变默认类型。  

**魔法数字（magic number）**是具有模糊含义或可能需要后期修改的字面量（通常为数字）。避免在代码中使用魔法数字，应使用符号常量。  

日常生活中使用**十进制（decimal）**数字（含10个数字）。计算机使用**二进制（binary）**（仅含2个数字）。C++也支持**八进制（octal）**（基8）和**十六进制（hexadecimal）**（基16）。这些都属于**数制系统（numeral systems）**，即用于表示数字的符号（数字）集合。  

**字符串（string）**是用于表示文本（如名称、词语、句子）的字符序列。字符串字面量始终置于双引号内。C++中的字符串字面量是C风格字符串（C-style strings），其类型特殊且难以操作。  

**std::string**提供处理文本字符串的简便安全方式，定义于\<string\>头文件。`std::string`的初始化（或赋值）和复制成本较高。  

**std::string_view**提供对现有字符串（C风格字符串字面量、std::string或字符数组）的只读访问，无需复制。若被查看的字符串已销毁，则对应的`std::string_view`称为**悬空视图（dangling view）**。修改`std::string`时，所有指向它的视图将**失效（invalidated）**，使用失效视图（除重新验证外）会导致未定义行为。  

因C风格字符串字面量存在于整个程序周期中，可将`std::string_view`设为C风格字符串字面量，甚至从函数返回此类视图。  

**子串（substring）**是现有字符串中的连续字符序列。  

测验时间  
----------------  

**问题1**  
为何具名常量通常优于字面常量？  
  
<details><summary>答案</summary>使用字面常量（即魔法数字）会降低代码可读性和可维护性。符号常量能明确数值含义，且修改声明处即可全局生效。</details>  

为何const/constexpr变量通常优于#define符号常量？  
  
<details><summary>答案</summary>#define常量不显示于调试器且更易引发命名冲突。</details>  

**问题2**  
找出以下代码中的3个问题：  
```cpp
#include <cstdint> // 引入std::uint8_t
#include <iostream>

int main()
{
  std::cout << "How old are you?\n";

  std::uint8_t age{};
  std::cin >> age;

  std::cout << "Allowed to drive a car in Texas: ";

  if (age >= 16)
      std::cout << "Yes";
  else
      std::cout << "No";

  std::cout << '.\n';

  return 0;
}
```  
  
<details><summary>答案</summary>  
1. 第8行`age`定义为`std::uint8_t`，因其通常为字符类型，输入/输出将视为字符而非数值。应改用普通`int`并移除`#include <cstdint>`  
2. 第13行使用魔法数字`16`，应改用`constexpr`变量  
3. 第18行`'.\n'`为多字符字面量，应改为双引号`".\n"`  
</details>  

**问题3**  
`std::string`与`std::string_view`的主要区别？使用`std::string_view`可能引发什么问题？  
  
<details><summary>答案</summary>  
`std::string`提供可修改字符串，初始化与复制成本高。`std::string_view`提供只读视图，成本低。当被查看字符串先于视图销毁时，视图将悬空引发风险。  
</details>  

**问题4**  
编写程序询问两人姓名年龄并输出年长者。  
[查看提示](javascript:void(0))  
<details><summary>提示</summary>使用`std::getline()`输入姓名</details>  
  
<details><summary>答案</summary>  
```cpp
#include <iostream>
#include <string>
#include <string_view>

std::string getName(int num)
{
    std::cout << "Enter the name of person #" << num << ": ";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // 读取整行文本到name

    return name;
}

int getAge(std::string_view sv)
{
    std::cout << "Enter the age of " << sv << ": ";
    int age{};
    std::cin >> age;

    return age;
}

void printOlder(std::string_view name1, int age1, std::string_view name2, int age2)
{
    if (age1 > age2)
        std::cout << name1 << " (age " << age1 <<") 比 " << name2 << " (age " << age2 <<") 年长。\n";
    else
        std::cout << name2 << " (age " << age2 <<") 比 " << name1 << " (age " << age1 <<") 年长。\n";
}

int main()
{
    const std::string name1{ getName(1) };
    const int age1 { getAge(name1) };
    
    const std::string name2{ getName(2) };
    const int age2 { getAge(name2) };

    printOlder(name1, age1, name2, age2);

    return 0;
}
```  
</details>  

**问题5**  
上题解答中，为何`main`中的变量`age1`不能是constexpr？  
  
<details><summary>答案</summary>constexpr变量需要常量表达式初始化，而`getAge()`调用不符合常量表达式要求，故只能声明为const。</details>  

[下一课 6.1 运算符优先级与结合性](Chapter-6/lesson6.1-operator-precedence-and-associativity.md)  
[返回主页](/)  
[上一课 5.9 std::string_view（下）](Chapter-5/lesson5.9-stdstring_view-part-2.md)