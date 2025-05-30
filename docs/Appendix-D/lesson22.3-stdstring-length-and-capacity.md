22.3 — std::string的长度与容量  
=======================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年8月15日（首次发布于2009年9月27日）  

 

创建字符串后，了解其长度通常很有帮助。这时就需要使用长度（length）和容量（capacity）相关操作。我们还将讨论将std::string转换回C风格字符串的各种方法，以便在需要char*类型字符串的函数中使用。  

**字符串长度**  

字符串长度非常简单——即字符串包含的字符数量。有两个完全相同的函数可用于确定字符串长度：  

| **size_type string::length() const** **size_type string::size() const** * 这两个函数均返回字符串当前字符数（不含空终止符） 示例代码：  ``` std::string s { "012345678" }; std::cout << s.length() << '\n'; ``` 输出：  ``` 9  ``` |  
| --- |  

虽然可以使用length()判断字符串是否为空，但更高效的方式是使用empty()函数：  

| **bool string::empty() const** * 若字符串无字符返回true，否则返回false 示例代码：  ``` std::string string1 { "Not Empty" }; std::cout << (string1.empty() ? "true" : "false") << '\n'; std::string string2; // 空字符串 std::cout << (string2.empty() ? "true" : "false")  << '\n'; ``` 输出：  ``` false true  ``` |  
| --- |  

还有一个与大小相关的函数可能极少使用，但为了完整性在此列出：  

| **size_type string::max_size() const** * 返回字符串允许包含的最大字符数 * 该值因操作系统和系统架构而异 示例代码：  ``` std::string s { "MyString" }; std::cout << s.max_size() << '\n'; ``` 输出：  ``` 4294967294  ``` |  
| --- |  

**字符串容量**  

字符串容量（capacity）反映字符串为存储内容分配的内存空间，以字符数计量（不含空终止符）。例如容量为8的字符串可存储8个字符。  

| **size_type string::capacity() const** * 返回字符串无需重新分配内存可容纳的字符数 示例代码：  ``` std::string s { "01234567" }; std::cout << "长度: " << s.length() << '\n'; std::cout << "容量: " << s.capacity() << '\n'; ``` 输出：  ``` 长度: 8 容量: 15  ``` |  
| --- |  

注意容量大于字符串长度！虽然字符串长度为8，但实际分配了15个字符的内存空间。为何如此设计？  

关键在于：若用户尝试向字符串添加超出当前容量的字符，必须重新分配更大内存。例如若字符串长度和容量均为8，添加任何字符都会强制重新分配。通过设置容量大于实际长度，为用户在需要重新分配前提供扩展缓冲空间。  

内存重分配（reallocation）存在以下弊端：  

首先，内存重分配开销较大。需分配新内存、复制所有字符到新内存（长字符串耗时明显），最后释放旧内存。频繁重分配会显著降低程序性能。  

其次，字符串重分配后内容地址改变，导致所有引用（references）、指针（pointers）和迭代器（iterators）失效！  

注意并非所有字符串的容量都大于长度。考虑以下程序：  

```  
std::string s { "0123456789abcde" };  
std::cout << "长度: " << s.length() << '\n';  
std::cout << "容量: " << s.capacity() << '\n';  
```  

输出可能为：  

```  
长度: 15  
容量: 15  
```  

（具体结果因编译器而异）  

添加字符后观察容量变化：  

```  
std::string s("0123456789abcde");  
std::cout << "长度: " << s.length() << '\n';  
std::cout << "容量: " << s.capacity() << '\n';  

// 添加新字符  
s += "f";  
std::cout << "长度: " << s.length() << '\n';  
std::cout << "容量: " << s.capacity() << '\n';  
```  

输出结果：  

```  
长度: 15  
容量: 15  
长度: 16  
容量: 31  
```  

| **void string::reserve()**  **void string::reserve(size_type unSize)** * 第二个版本设置字符串容量至少为unSize（可能更大），可能需要重新分配内存 * 第一个版本或unSize小于当前容量时，函数尝试将容量缩小至匹配长度（具体实现可能忽略此请求） 示例代码：  ``` std::string s { "01234567" }; std::cout << "长度: " << s.length() << '\n'; std::cout << "容量: " << s.capacity() << '\n';  s.reserve(200); std::cout << "长度: " << s.length() << '\n'; std::cout << "容量: " << s.capacity() << '\n';  s.reserve(); std::cout << "长度: " << s.length() << '\n'; std::cout << "容量: " << s.capacity() << '\n'; ``` 输出：  ``` 长度: 8 容量: 15 长度: 8 容量: 207 长度: 8 容量: 207  ``` |  
| --- |  

此示例展示两个要点：尽管请求容量200，实际获得207（容量保证至少满足请求）。随后请求调整容量以适应字符串时，请求被忽略。  

若预先知道将通过大量字符串操作构建大字符串，可预先预留足够容量避免多次重分配：  

```  
#include <iostream>  
#include <string>  
#include <cstdlib> // 用于rand()和srand()  
#include <ctime> // 用于time()  

int main()  
{  
    std::srand(std::time(nullptr)); // 初始化随机数生成器  

    std::string s{}; // 长度0  
    s.reserve(64); // 预留64个字符  

    // 用随机小写字母填充字符串  
    for (int count{ 0 }; count < 64; ++count)  
        s += 'a' + std::rand() % 26;  

    std::cout << s;  
}  
```  

每次执行输出不同，示例输出：  

```  
wzpzujwuaokbakgijqdawvzjqlgcipiiuuxhyfkdppxpyycvytvyxwqsbtielxpy  
```  

通过一次性设置容量，避免多次重分配，在通过拼接构建大字符串时可显著提升性能。  

[下一课 22.4 — std::string的字符访问与C风格数组转换](Appendix-D/lesson22.4-stdstring-character-access-and-conversion-to-c-style-arrays.md)  
[返回主页](/)  
[上一课 22.2 — std::string的构造与析构](Appendix-D/lesson22.2-stdstring-construction-and-destruction.md)