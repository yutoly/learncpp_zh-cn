22.7 — std::string的插入操作  
=============================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2010年7月18日 PDT下午9:50 / 2021年8月26日  

插入操作  
----------------  

向现有字符串插入字符可通过insert()函数实现。  

| **string& string::insert (size_type（大小类型）index, const string& str)**  
**string& string::insert (size_type index, const char* str)**  
* 两个函数都将字符串str的字符插入到当前字符串的index位置处  
* 均返回*this以便支持链式调用  
* 若index无效则抛出out_of_range（越界）异常  
* 若结果超出最大字符数则抛出length_error（长度错误）异常  
* C风格字符串版本中str不可为NULL  

示例代码：  
```cpp  
string sString("aaaa");  
cout << sString << endl;  

sString.insert(2, string("bbbb"));  
cout << sString << endl;  

sString.insert(4, "cccc");  
cout << sString << endl;  
```  
输出：  
```  
aaaa  
aabbbbaa  
aabbccccbbaa  
```  

以下版本允许将子串插入字符串的任意位置：  

| **string& string::insert (size_type index, const string& str, size_type startindex, size_type num)**  
* 将str从startindex开始的num个字符插入到当前字符串的index位置  
* 返回*this以便链式调用  
* 若index或startindex越界则抛出out_of_range异常  
* 若结果超出最大字符数则抛出length_error异常  

示例代码：  
```cpp  
string sString("aaaa");  
const string sInsert("01234567");  
sString.insert(2, sInsert, 3, 4); // 将sInsert从索引[3,7)的子串插入到sString的索引2处  
cout << sString << endl;  
```  
输出：  
```  
aa3456aa  
```  

以下版本插入C风格字符串的前段：  

| **string& string::insert(size_type index, const char* str, size_type len)**  
* 将str的前len个字符插入到当前字符串的index位置  
* 返回*this以便链式调用  
* index无效时抛出out_of_range异常  
* 结果超限时抛出length_error异常  
* 忽略特殊字符（如\0）  

示例代码：  
```cpp  
string sString("aaaa");  
sString.insert(2, "bcdef", 3);  
cout << sString << endl;  
```  
输出：  
```  
aabcdaa  
```  

以下版本用于重复插入相同字符：  

| **string& string::insert(size_type index, size_type num, char c)**  
* 在index位置插入num个字符c  
* 返回*this以便链式调用  
* index无效时抛出out_of_range异常  
* 结果超限时抛出length_error异常  

示例代码：  
```cpp  
string sString("aaaa");  
sString.insert(2, 4, 'c');  
cout << sString << endl;  
```  
输出：  
```  
aaccccaa  
```  

最后是三个基于迭代器（iterator）的版本：  

| **void insert(iterator it, size_type num, char c)**  
**iterator string::insert(iterator it, char c)**  
**void string::insert(iterator it, InputIterator（输入迭代器）begin, InputIterator end)**  
* 第一版本在迭代器it前插入num个字符c  
* 第二版本在迭代器it前插入单个字符c，返回插入位置的迭代器  
* 第三版本在迭代器it前插入[begin,end)区间所有字符  
* 所有版本在结果超限时抛出length_error异常  

[下一课](#)  
[返回主页](/)    
[上一课 22.6 — std::string的追加操作](Appendix-D/lesson22.6-stdstring-appending.md)