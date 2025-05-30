22.2 — std::string 的构造与析构  
================================================

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2009年9月20日上午10:10（太平洋夏令时）  
2023年6月15日更新  

本课我们将学习如何构造 std::string 对象，以及如何在数字与字符串之间进行转换。


**字符串构造**  
----------------  

string 类提供了多种构造函数用于创建字符串。以下逐一介绍：


注意：string::size_type 解析为 size_t，这是与 sizeof 运算符返回类型相同的无符号整型。具体尺寸因环境而异，本教程中可将其视为 unsigned int。


| **string::string()**（默认构造函数）  
| ---  
| * 创建空字符串  
| 示例代码：  
| ```cpp  
| std::string sSource;  
| std::cout << sSource;  
| ```  
| 输出：无内容 |


| **string::string(const string& strString)**（拷贝构造函数）  
| ---  
| * 创建 strString 的副本  
| 示例代码：  
| ```cpp  
| std::string sSource{ "my string" };  
| std::string sOutput{ sSource };  
| std::cout << sOutput;  
| ```  
| 输出：  
| ```  
| my string  
| ``` |


| **string::string(const string& strString, size_type unIndex)**  
| **string::string(const string& strString, size_type unIndex, size_type unLength)**  
| ---  
| * 从 strString 的 unIndex 位置开始，最多复制 unLength 个字符  
| * 若遇到 NULL（空字符），即使未达 unLength 也终止复制  
| * 若未指定 unLength，则复制从 unIndex 开始的所有字符  
| * 若 unIndex 超出字符串长度，抛出 out_of_range 异常  
| 示例代码：  
| ```cpp  
| std::string sSource{ "my string" };  
| std::string sOutput{ sSource, 3 };  
| std::cout << sOutput << '\n';  
| std::string sOutput2(sSource, 3, 4);  
| std::cout << sOutput2 << '\n';  
| ```  
| 输出：  
| ```  
| string  
| stri  
| ``` |


| **string::string(const char* szCString)**  
| ---  
| * 从 C 风格字符串 szCString 创建（不包含 NULL 终止符）  
| * 若结果超出最大长度，抛出 length_error 异常  
| * **警告**：szCString 不可为 NULL  
| 示例代码：  
| ```cpp  
| const char* szSource{ "my string" };  
| std::string sOutput{ szSource };  
| std::cout << sOutput << '\n';  
| ```  
| 输出：  
| ```  
| my string  
| ``` |


| **string::string(const char* szCString, size_type unLength)**  
| ---  
| * 从 szCString 的前 unLength 个字符创建  
| * 若结果超出最大长度，抛出 length_error 异常  
| * **警告**：此构造函数不将 NULL 视为终止符！需注意缓冲区溢出风险  
| 示例代码：  
| ```cpp  
| const char* szSource{ "my string" };  
| std::string sOutput(szSource, 4);  
| std::cout << sOutput << '\n';  
| ```  
| 输出：  
| ```  
| my s  
| ``` |


| **string::string(size_type nNum, char chChar)**  
| ---  
| * 创建包含 nNum 个 chChar 字符的字符串  
| * 若结果超出最大长度，抛出 length_error 异常  
| 示例代码：  
| ```cpp  
| std::string sOutput(4, 'Q');  
| std::cout << sOutput << '\n';  
| ```  
| 输出：  
| ```  
| QQQQ  
| ``` |


| **template string::string(InputIterator itBeg, InputIterator itEnd)**  
| ---  
| * 使用迭代器范围 [itBeg, itEnd) 的字符创建字符串  
| * 若结果超出最大长度，抛出 length_error 异常  
| 无示例代码（此构造函数较为冷僻） |


| **string::~string()**（析构函数）  
| ---  
| * 销毁字符串并释放内存  
| 无示例代码（析构函数不会显式调用） |


**从数字构造字符串**  
----------------  

std::string 类的一个显著缺失特性是无法直接从数字创建字符串。例如：

```cpp
std::string sFour{ 4 };
```

会产生错误：

```
c:vcprojectstest2test2test.cpp(10) : error C2664: ...无法将参数 1 从 'int' 转换为 'std::basic_string...
```

如你所见，当试图将 int 转换为 string 时会失败。


最简便的解决方案是使用 std::ostringstream 类。该类支持从字符、数字、字符串等输入源接收数据，并能通过 str() 函数输出字符串。更多信息详见课程 [28.4 — 字符串流类](Chapter-28/lesson28.4-stream-classes-for-strings.md)。


以下是创建数字字符串的通用方案：

```cpp
#include <iostream>
#include <sstream>
#include <string>

template <typename T>
inline std::string ToString(T tX)
{
    std::ostringstream oStream;
    oStream << tX;
    return oStream.str();
}
```

测试代码：

```cpp
int main()
{
    std::string sFour{ ToString(4) };
    std::string sSixPointSeven{ ToString(6.7) };
    std::string sA{ ToString('A') };
    std::cout << sFour << '\n';
    std::cout << sSixPointSeven << '\n';
    std::cout << sA << '\n';
}
```

输出：

```
4
6.7
A
```

注意此方案省略了错误处理。若 tX 插入 oStream 失败，应抛出异常。


**相关内容**  

标准库提供了 `std::to_string()` 函数用于将数字转换为字符串。虽然这是更简单的解决方案，但其输出可能与 std::cout 或上述 ToString() 函数有所不同。部分差异可参考[cppreference文档](https://en.cppreference.com/w/cpp/string/basic_string/to_string)。


**字符串转数字**  
----------------  

类似方案：

```cpp
#include <iostream>
#include <sstream>
#include <string>

template <typename T>
inline bool FromString(const std::string& sString, T& tX)
{
    std::istringstream iStream(sString);
    return !(iStream >> tX).fail(); // 将值提取到 tX，返回成功与否
}
```

测试代码：

```cpp
int main()
{
    double dX;
    if (FromString("3.4", dX))
        std::cout << dX << '\n'; 
    if (FromString("ABC", dX))
        std::cout << dX << '\n'; 
}
```

输出：

```
3.4
```

注意第二个转换失败并返回 false。


[下一课 22.3 — std::string 的长度与容量](Appendix-D/lesson22.3-stdstring-length-and-capacity.md)  
[返回主页](/)  
[上一课 22.1 — std::string 与 std::wstring](Appendix-D/lesson22.1-stdstring-and-stdwstring.md)