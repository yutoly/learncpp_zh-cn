28.2 — 使用istream进行输入  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年12月23日（首次发布于2008年3月4日）  

iostream库相当复杂——我们无法在本教程中涵盖其全部内容。但我们将展示最常用的功能。本节重点探讨输入流类（istream）的各个方面。

**提取运算符**  
正如多节课程所示，我们可以使用提取运算符（>>）从输入流中读取信息。C++为所有内置数据类型预定义了提取操作，您已了解如何为自定义类[重载提取运算符](93-overloading-the-io-operators/)。

读取字符串时，提取运算符的常见问题是防止缓冲区溢出。考虑以下示例：

```cpp
char buf[10]{};
std::cin >> buf;
```

若用户输入18个字符会发生什么？缓冲区溢出将导致严重问题。通常不应假设用户输入的字符数量。

**操纵符（manipulator）**  
解决方法之一是使用操纵符。操纵符是通过提取（>>）或插入（<<）运算符修改流行为的对象。您已接触过的"std::endl"既是操纵符，它既输出换行符又刷新输出缓冲区。

C++在iomanip头文件中提供了**setw**操纵符，用于限制从流中读取的字符数：

```cpp
#include <iomanip>
char buf[10]{};
std::cin >> std::setw(10) >> buf;
```
此程序现在最多读取9个字符（留一个终止符位置），剩余字符将留在流中供下次提取。

**提取与空白字符**  
需注意，提取运算符会跳过空白字符（空格、制表符、换行符）。

观察以下程序：

```cpp
int main()
{
    char ch{};
    while (std::cin >> ch)
        std::cout << ch;
    return 0;
}
```
输入：
```
Hello my name is Alex
```
输出：
```
HellomynameisAlex
```

**get()函数**  
若需保留空白字符，istream类提供了get()函数：

```cpp
int main()
{
    char ch{};
    while (std::cin.get(ch))
        std::cout << ch;
    return 0;
}
```
相同输入将完整保留空白字符输出。

字符串版本的get()可限制读取字符数：

```cpp
int main()
{
    char strBuf[11]{};
    std::cin.get(strBuf, 11);
    std::cout << strBuf << '\n';
    return 0;
}
```
输入：
```
Hello my name is Alex
```
输出：
```
Hello my n
```

**get()的换行问题**  
需注意get()不会读取换行符：

```cpp
int main()
{
    char strBuf[11]{};
    std::cin.get(strBuf, 11);  // 读取至多10字符
    std::cout << strBuf << '\n';
    
    std::cin.get(strBuf, 11);  // 继续读取
    std::cout << strBuf << '\n';
    return 0;
}
```
输入：
```
Hello!
```
输出：
```
Hello!
```
程序直接终止，因第二个get()遇到换行符立即停止。

**getline()函数**  
getline()可提取并丢弃分隔符：

```cpp
int main()
{
    char strBuf[11]{};
    std::cin.getline(strBuf, 11);  // 读取至多10字符
    std::cout << strBuf << '\n';
    
    std::cin.getline(strBuf, 11);  // 继续读取
    std::cout << strBuf << '\n';
    return 0;
}
```

**gcount()函数**  
获取最近getline()调用读取的字符数（含丢弃的分隔符）：

```cpp
int main()
{
    char strBuf[100]{};
    std::cin.getline(strBuf, 100);
    std::cout << strBuf << '\n';
    std::cout << std::cin.gcount() << " characters were read\n";
    return 0;
}
```

**std::string专用getline()**  
string头文件中提供针对std::string的getline()版本：

```cpp
#include <string>
#include <iostream>

int main()
{
    std::string strBuf{};
    std::getline(std::cin, strBuf);
    std::cout << strBuf << '\n';
    return 0;
}
```

**其他实用istream函数**  
- **ignore()**：丢弃流中第一个字符  
- **ignore(int nCount)**：丢弃前nCount个字符  
- **peek()**：预览下一个字符而不提取  
- **unget()**：将最后读取的字符放回流中  
- **putback(char ch)**：将指定字符放回流中  

istream包含更多实用函数，详细信息可参考<https://en.cppreference.com/w/cpp/io/basic_istream>。

[下一课 28.3 — 使用ostream和ios进行输出](Chapter-28/lesson28.3-output-with-ostream-and-ios.md)  
[返回主页](/)  
[上一课 28.1 — 输入输出流](Chapter-28/lesson28.1-input-and-output-io-streams.md)