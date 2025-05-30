22.4 — std::string的字符访问及与C风格数组的转换  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2009年10月4日 PDT上午9:54  
2022年9月16日  

**字符访问**  
----------------  

std::string提供两种几乎相同的字符访问方式。更易用且更快的版本是重载的operator\[]：  

| **char\& string::operator\[] (size_type nIndex)** **const char\& string::operator\[] (size_type nIndex) const**  
* 两个函数均返回索引nIndex处的字符  
* 传递无效索引将导致未定义行为  
* 由于返回类型为char\&，可用于修改数组中的字符  

示例代码：  
```cpp  
std::string sSource{ "abcdefg" };  
std::cout << sSource[5] << '\n';  
sSource[5] = 'X';  
std::cout << sSource << '\n';  
```  
输出：  
```  
f  
abcdeXg  
```  

另一种非运算符版本使用异常检查索引有效性，因此速度较慢。当不确定nIndex是否有效时应使用此版本：  

| **char\& string::at (size_type nIndex)** **const char\& string::at (size_type nIndex) const**  
* 两个函数均返回索引nIndex处的字符  
* 传递无效索引将抛出out_of_range异常  
* 由于返回类型为char\&，可用于修改数组中的字符  

示例代码：  
```cpp  
std::string sSource{ "abcdefg" };  
std::cout << sSource.at(5) << '\n';  
sSource.at(5) = 'X';  
std::cout << sSource << '\n';  
```  
输出：  
```  
f  
abcdeXg  
```  

**与C风格数组的转换**  
----------------  

许多函数（包括所有C函数）要求字符串格式为C风格字符串而非std::string。为此，std::string提供3种转换方式：  

| **const char* string::c_str () const**  
* 以const C风格字符串形式返回字符串内容  
* 附加空终止符（null terminator）  
* C风格字符串由std::string管理，不应被删除  

示例代码：  
```cpp  
#include <cstring>  

std::string sSource{ "abcdefg" };  
std::cout << std::strlen(sSource.c_str());  
```  
输出：  
```  
7  
```  

| **const char* string::data () const**  
* 以const C风格字符串形式返回字符串内容  
* 附加空终止符。功能与`c_str()`相同  
* C风格字符串由std::string管理，不应被删除  

示例代码：  
```cpp  
#include <cstring>  

std::string sSource{ "abcdefg" };  
const char* szString{ "abcdefg" };  
// memcmp比较两个C风格字符串的前n个字符，相等时返回0  
if (std::memcmp(sSource.data(), szString, sSource.length()) == 0)  
    std::cout << "字符串相等";  
else  
    std::cout << "字符串不相等";  
```  
输出：  
```  
字符串相等  
```  

| **size_type string::copy(char* szBuf, size_type nLength, size_type nIndex = 0) const**  
* 从nIndex开始，最多复制nLength个字符到szBuf  
* 返回实际复制的字符数  
* 不附加空终止符。调用者需确保szBuf初始化为NULL或用返回值终止字符串  
* 调用者需防止szBuf溢出  

示例代码：  
```cpp  
std::string sSource{ "sphinx of black quartz, judge my vow" };  
char szBuf[20];  
int nLength{ static_cast<int>(sSource.copy(szBuf, 5, 10)) };  
szBuf[nLength] = '\0';  // 确保缓冲区字符串终止  
std::cout << szBuf << '\n';  
```  
输出：  
```  
black  
```  

在可能情况下应避免使用此函数，因其存在潜在风险（需调用者处理终止符和缓冲区溢出）。  

[下一课 22.5 — std::string的赋值与交换](Appendix-D/lesson22.5-stdstring-assignment-and-swapping.md)  
[返回主页](/)  
[上一课 22.3 — std::string的长度与容量](Appendix-D/lesson22.3-stdstring-length-and-capacity.md)