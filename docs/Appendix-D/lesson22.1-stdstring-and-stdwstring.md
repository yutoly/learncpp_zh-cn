22.1 — std::string（标准字符串）与std::wstring（宽字符串）  
========================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2009年9月12日 下午2:43（PDT）  
2023年8月12日更新  

标准库包含众多实用类——但最实用的或许是std::string。std::string（及其宽字符版本std::wstring）是一个提供赋值、比较和修改等操作的字符串类。本章我们将深入探讨这些字符串类。  

> **术语说明**  
> 本文中"C风格字符串"指代字符数组形式字符串，而std::string与std::wstring统称为"字符串"。  

> **作者提示**  
> 本章内容略有陈旧，未来更新将进行精简。建议浏览材料获取思路和实用示例，最新技术细节请参考技术文档网站（如[cppreference](https://en.cppreference.com/w/cpp/string/basic_string)）。  

**字符串类的必要性**  
在[前期课程](66-c-style-strings/)中，我们学习了使用字符数组存储字符串的C风格字符串。实际操作过C风格字符串的开发者很快会发现其存在诸多痛点：容易出错、难以调试且需要繁琐的内存管理。  

C风格字符串的主要缺陷在于需要手动管理内存。例如要将"hello!"赋值到缓冲区，必须先动态分配正确长度的内存：  
```cpp
char* strHello { new char[7] };
```  
（别忘了为终止符'\0'预留额外空间！）  

接着必须执行值拷贝：  
```cpp
strcpy(strHello, "hello!");
```  
（需确保缓冲区足够大以避免溢出！）  

最后由于是动态分配，必须记得正确释放内存：  
```cpp
delete[] strHello;
```  
（务必使用数组删除而非普通delete！）  

此外，C语言中适用于数值的直观运算符（如赋值和比较）无法直接用于C风格字符串。例如使用==比较两个C风格字符串实际进行的是指针比较而非字符串内容比较；使用=赋值执行的是指针拷贝（浅拷贝）而非内容复制。这些特性极易导致程序崩溃且难以调试！  

总结而言，使用C风格字符串需要牢记大量安全规范、使用strcat()/strcmp()等非常规命名的函数，以及繁琐的内存管理。  

幸运的是，C++标准库提供了更优解决方案：std::string和std::wstring类。通过构造函数、析构函数和运算符重载等机制，std::string实现了安全直观的字符串操作——无需内存管理、告别怪异函数名、大幅降低出错风险！  

**字符串类概览**  
所有字符串功能定义于头文件\<string>中：  
```cpp
#include <string>
```  

该头文件包含三个字符串类，其中基础类为模板类basic\_string\<\>：  
```cpp
namespace std
{
    template<class charT, class traits = char_traits<charT>, class Allocator = allocator<charT> >
        class basic_string;
}
```  
（普通用户无需直接操作该模板类，traits和Allocator参数在绝大多数情况下使用默认值即可）  

标准库提供两个basic\_string特化版本：  
```cpp
namespace std
{
    typedef basic_string<char> string;
    typedef basic_string<wchar_t> wstring;
}
```  
* std::string用于标准ASCII和UTF-8字符串  
* std::wstring用于宽字符/Unicode（UTF-16）字符串  
（标准库未内置UTF-32字符串类，但可通过扩展basic\_string\<\>实现）  

虽然用户直接使用std::string和std::wstring，但所有功能实现在basic\_string\<\>中。由于模板特性，以下列出的函数同时适用于string和wstring。但需注意模板类报错信息较为复杂——不必畏惧这些看似可怕的实际错误提示！  

**字符串类功能总览**  
以下是字符串类主要功能列表（多数函数提供多种重载形式，后续课程将详细讲解）：  

| 功能分类            | 函数                                                                 | 功能描述                                                                 |
|---------------------|----------------------------------------------------------------------|--------------------------------------------------------------------------|
| **构造与析构**      | [构造函数](17-2-ststring-construction-and-destruction/)<br>[析构函数](17-2-ststring-construction-and-destruction/) | 创建/拷贝字符串<br>销毁字符串                                            |
| **容量与长度**      | capacity()<br>empty()<br>length()/size()<br>max_size()<br>reserve() | 返回不重新分配可容纳的字符数<br>返回是否为空<br>返回字符数<br>返回最大可分配长度<br>调整容量 |
| **元素访问**        | operator[]/at()                                                     | 访问指定索引字符                                                         |
| **修改操作**        | operator=/assign()<br>operator+=/append()/push_back()<br>insert()<br>clear()<br>erase()<br>replace()<br>resize()<br>swap() | 赋值新值<br>追加字符<br>插入字符<br>清空内容<br>删除字符<br>替换字符<br>调整大小<br>交换值 |
| **输入输出**        | operator\>\>/getline()<br>operator\<\<<br>c_str()<br>copy()<br>data() | 从输入流读取<br>写入输出流<br>返回C风格字符串<br>拷贝到字符数组<br>同c_str() |
| **字符串比较**      | operator==/!=<br>operator<</<=/>>/>=<br>compare()                   | 比较相等性（返回bool）<br>比较大小（返回bool）<br>比较结果（返回-1/0/1） |
| **子串与连接**      | operator+<br>substr()                                               | 连接字符串<br>返回子串                                                   |
| **查找功能**        | find()<br>find_first_of()<br>find_first_not_of()<br>find_last_of()<br>find_last_not_of()<br>rfind() | 查找子串首位置<br>查找字符集首字符<br>查找非字符集首字符<br>查找字符集末字符<br>查找非字符集末字符<br>反向查找子串 |
| **迭代器与分配器**  | begin()/end()<br>get_allocator()<br>rbegin()/rend()                | 正向迭代器<br>获取分配器<br>反向迭代器                                    |

**功能缺失说明**  
标准库字符串类仍存在以下常见功能缺失：  
* 从数值构造字符串  
* 大小写转换函数  
* 大小写不敏感比较  
* 分词/字符串分割  
* 便捷获取左右子串  
* 空白符裁剪  
* sprintf式格式化  
* UTF-8与UTF-16互转  

对于上述功能，需自行实现或通过c_str()转换为C风格字符串后使用C库函数。后续课程将深入解析字符串类的各项功能（所有示例适用于wstring）。  

[下一课 22.2 std::string的构造与析构](Appendix-D/lesson22.2-stdstring-construction-and-destruction.md)  
[返回主页](/)  
[上一课 21.4 STL算法概览](Appendix-D/lesson21.4-stl-algorithms-overview.md)