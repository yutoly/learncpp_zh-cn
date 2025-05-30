28.5 — 流状态与输入验证  
==========================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2024年9月9日（首次发布于2008年3月25日）  

流状态  
----------------  

ios_base类包含多个状态标志位，用于指示流操作中可能出现的各种情况：  

| 标志位（Flag） | 含义（Meaning） |  
| --- | --- |  
| goodbit（良好位） | 一切正常 |  
| badbit（错误位） | 发生致命错误（如程序试图读取文件末尾之后的内容） |  
| eofbit（文件尾位） | 流已到达文件末尾 |  
| failbit（失败位） | 发生非致命错误（如用户输入字母而程序期待整数） |  

虽然这些标志位属于ios_base类，但由于ios继承自ios_base且更便于书写，通常通过ios访问它们（例如std::ios::failbit）。  

ios类提供多个成员函数以便捷访问这些状态：  

| 成员函数（Member function） | 含义（Meaning） |  
| --- | --- |  
| good() | 若goodbit被设置则返回true（流正常） |  
| bad() | 若badbit被设置则返回true（发生致命错误） |  
| eof() | 若eofbit被设置则返回true（流处于文件末尾） |  
| fail() | 若failbit被设置则返回true（发生非致命错误） |  
| clear() | 清除所有标志位并将流恢复至goodbit状态 |  
| clear(state) | 清除所有标志位并设置传入的状态标志 |  
| rdstate() | 返回当前设置的标志位 |  
| setstate(state) | 设置传入的状态标志 |  

最常处理的标志位是failbit，当用户输入无效内容时会被设置。例如以下程序：  

```cpp
std::cout << "Enter your age: ";
int age {};
std::cin >> age;
```  

该程序期待用户输入整数。但如果用户输入非数字数据（如"Alex"），cin将无法提取有效内容到age变量，此时failbit会被设置。  

若发生错误且流被设为非goodbit状态，后续流操作将被忽略。可通过调用clear()函数清除此状态。  

输入验证  
----------------  

**输入验证（Input validation）**是检查用户输入是否符合特定标准的流程。输入验证通常可分为两类：字符串验证和数值验证。  

**字符串验证**中，我们将所有用户输入视为字符串，根据格式是否符合要求来决定接受或拒绝。例如要求用户输入电话号码时，可能需要确保输入包含十位数字。大多数语言（尤其是Perl、PHP等脚本语言）使用正则表达式实现。C++标准库也提供[正则表达式库](https://en.cppreference.com/w/cpp/regex)，但由于正则表达式性能低于手动验证，建议仅在性能（编译时与运行时）无关紧要或手动验证过于繁琐时使用。  

**数值验证**通常关注确保用户输入数值在特定范围内（如0到20之间）。但与字符串验证不同，用户可能输入非数值内容——这些情况也需处理。  

C++提供若干实用函数帮助判断字符属性（位于cctype头文件）：  

| 函数（Function） | 含义（Meaning） |  
| --- | --- |  
| std::isalnum(int) | 参数为字母或数字时返回非零值 |  
| std::isalpha(int) | 参数为字母时返回非零值 |  
| std::iscntrl(int) | 参数为控制字符时返回非零值 |  
| std::isdigit(int) | 参数为数字时返回非零值 |  
| std::isgraph(int) | 参数为可打印非空白字符时返回非零值 |  
| std::isprint(int) | 参数为可打印字符（含空格）时返回非零值 |  
| std::ispunct(int) | 参数为既非字母数字也非空白时返回非零值 |  
| std::isspace(int) | 参数为空白字符时返回非零值 |  
| std::isxdigit(int) | 参数为十六进制数字（0-9，a-f，A-F）时返回非零值 |  

字符串验证示例  
----------------  

**案例一：验证用户姓名**  
要求用户输入仅包含字母和空格：  

```cpp
#include <algorithm> // std::all_of
#include <cctype> // std::isalpha, std::isspace
#include <iostream>
#include <ranges>
#include <string>
#include <string_view>

bool isValidName(std::string_view name)
{
  return std::ranges::all_of(name, [](char ch) {
    return std::isalpha(ch) || std::isspace(ch);
  });
}

int main()
{
  std::string name{};
  do {
    std::cout << "Enter your name: ";
    std::getline(std::cin, name);
  } while (!isValidName(name));
  std::cout << "Hello " << name << "!\n";
}
```  

**案例二：验证电话号码模板**  
要求用户输入匹配"(###) ###-####"格式：  

```cpp
#include <algorithm> 
#include <cctype>
#include <iostream>
#include <map>
#include <ranges>
#include <string>
#include <string_view>

bool inputMatches(std::string_view input, std::string_view pattern)
{
    if (input.length() != pattern.length()) return false;

    static const std::map<char, int (*)(int)> validators{
      { '#', &std::isdigit }, { '_', &std::isspace },
      { '@', &std::isalpha }, { '?', [](int) { return 1; } }
    };

    return std::ranges::equal(input, pattern, [](char ch, char mask) {
        auto found{ validators.find(mask) };        
        return (found != validators.end()) ? (*found->second)(ch) : (ch == mask);
    });
}

int main()
{
    std::string phoneNumber{};
    do {
        std::cout << "Enter a phone number (###) ###-####: ";
        std::getline(std::cin, phoneNumber);
    } while (!inputMatches(phoneNumber, "(###) ###-####"));
    std::cout << "You entered: " << phoneNumber << '\n';
}
```  

数值验证  
----------------  

**方法一：直接数值提取**  

```cpp
#include <iostream>
#include <limits>

int main()
{
    int age{};
    while (true) {
        std::cout << "Enter your age: ";
        std::cin >> age;

        if (std::cin.fail()) { // 提取失败
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }

        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        if (std::cin.gcount() > 1) continue; // 清除多余输入
        if (age <= 0) continue;
        break;
    }
    std::cout << "You entered: " << age << '\n';
}
```  

**方法二：字符串转换验证**  

```cpp
#include <charconv> 
#include <iostream>
#include <limits>
#include <optional>
#include <string>
#include <string_view>

std::optional<int> extractAge(std::string_view age)
{
    int result{};
    const auto end{ age.data() + age.length() };
    if (std::from_chars(age.data(), end, result).ec != std::errc{}) return {};
    return (result > 0) ? result : std::optional<int>{};
}

int main()
{
    int age{};
    while (true) {
        std::cout << "Enter your age: ";
        std::string strAge{};
        if (!std::getline(std::cin >> std::ws, strAge)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');    
            continue;
        }
        if (auto extracted{ extractAge(strAge) }) {
            age = *extracted;
            break;
        }
    }
    std::cout << "You entered: " << age << '\n';
}
```  

C++输入验证需要较多工作，但多数任务可通过封装函数提高复用性。  

[下一课 28.6 — 基础文件I/O](Chapter-28/lesson28.6-basic-file-io.md)  
[返回主页](/)  
[上一课 28.4 — 字符串流类](Chapter-28/lesson28.4-stream-classes-for-strings.md)