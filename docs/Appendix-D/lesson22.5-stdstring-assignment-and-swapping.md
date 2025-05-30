22.5 — std::string 赋值与交换
===========================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2010年7月18日 下午2:21（PDT）  
2022年9月16日  

字符串赋值
----------------

给字符串（std::string）赋值最简单的方式是使用重载的赋值运算符（operator=）。此外还有一个assign()成员函数也提供了类似功能。

| **string& string::operator= (const string& str)**  
**string& string::assign (const string& str)**  
**string& string::operator= (const char* str)**  
**string& string::assign (const char* str)**  
**string& string::operator= (char c)**  
* 这些函数支持将各种类型值赋给字符串  
* 返回\*this以支持链式调用  
* 注意assign()没有接收单个字符（char）的版本  

示例代码：  
```cpp
std::string sString;

// 赋值字符串值
sString = std::string("One");
std::cout << sString << '\n';

const std::string sTwo("Two");
sString.assign(sTwo);
std::cout << sString << '\n';

// 赋值C风格字符串
sString = "Three";
std::cout << sString << '\n';

sString.assign("Four");
std::cout << sString << '\n';

// 赋值字符
sString = '5';
std::cout << sString << '\n';

// 链式赋值
std::string sOther;
sString = sOther = "Six";
std::cout << sString << ' ' << sOther << '\n';
```  
输出：  
```
One  
Two  
Three  
Four  
5  
Six Six  
```  

assign()成员函数还有其他重载形式：

| **string& string::assign (const string& str, size_type index, size_type len)**  
* 赋值str的子串，从index位置开始，长度为len  
* 若index越界会抛出out_of_range异常  
* 返回\*this以支持链式调用  

示例代码：  
```cpp
const std::string sSource("abcdefg");
std::string sDest;

sDest.assign(sSource, 2, 4); // 从索引2开始赋值4个字符
std::cout << sDest << '\n';
```  
输出：  
```
cdef  
```  

| **string& string::assign (const char* chars, size_type len)**  
* 赋值C风格数组chars的前len个字符  
* 若结果超出最大字符数会抛出length_error异常  
* 返回\*this以支持链式调用  

示例代码：  
```cpp
std::string sDest;

sDest.assign("abcdefg", 4);
std::cout << sDest << '\n';
```  
输出：  
```
abcd  
```  
该函数存在潜在风险，不建议使用。

| **string& string::assign (size_type len, char c)**  
* 赋值len个字符c  
* 若结果超出最大字符数会抛出length_error异常  
* 返回\*this以支持链式调用  

示例代码：  
```cpp
std::string sDest;

sDest.assign(4, 'g');
std::cout << sDest << '\n';
```  
输出：  
```
gggg  
```  

交换操作
----------------

要交换两个字符串的值，可以使用两个同名的swap()函数：

| **void string::swap (string& str)**  
**void swap (string& str1, string& str2)**  
* 两个函数都用于交换字符串值：成员函数交换\*this与str，全局函数交换str1与str2  
* 这些函数执行效率高，应优先于赋值操作来进行字符串交换  

示例代码：  
```cpp
std::string sStr1("red");
std::string sStr2("blue");

std::cout << sStr1 << ' ' << sStr2 << '\n';
swap(sStr1, sStr2);
std::cout << sStr1 << ' ' << sStr2 << '\n';
sStr1.swap(sStr2);
std::cout << sStr1 << ' ' << sStr2 << '\n';
```  
输出：  
```
red blue  
blue red  
red blue  
```  

[下一课 22.6 — std::string 追加操作](Appendix-D/lesson22.6-stdstring-appending.md)  
[返回主页](/)  
[上一课 22.4 — std::string 字符访问与C风格数组转换](Appendix-D/lesson22.4-stdstring-character-access-and-conversion-to-c-style-arrays.md)