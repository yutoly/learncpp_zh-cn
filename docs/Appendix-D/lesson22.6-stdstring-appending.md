22.6 — std::string 追加操作  
===============================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2010年7月18日（更新于2022年8月24日）  

**追加操作**  

在现有字符串末尾追加内容，可使用 operator+=、append() 或 push_back() 实现。  

| **string\& string::operator\+\= (const string\& str)** **string\& string::append (const string\& str)** * 两个函数都将str的字符追加到原字符串末尾 * 均返回\*this以支持链式调用 * 若结果超出最大字符数限制会抛出length_error异常 示例代码：  ``` std::string sString{"one"};  sString += std::string{" two"};  std::string sThree{" three"}; sString.append(sThree);  std::cout << sString << '\n'; ```  输出：  ``` one two three  ``` |
| --- |  

另有可追加子字符串的append()变体：  

| **string\& string::append (const string\& str, size\_type index, size\_type num)** * 将str从index位置开始的num个字符追加到字符串 * 返回\*this以支持链式调用 * 若index越界抛出out_of_range异常 * 若结果超出最大字符数抛出length_error异常 示例代码：  ``` std::string sString{"one "};  const std::string sTemp{"twothreefour"}; sString.append(sTemp, 3, 5); // 追加sTemp从索引3开始的5个字符 std::cout << sString << '\n'; ```  输出：  ``` one three  ``` |
| --- |  

operator+= 和 append() 也支持C风格字符串：  

| **string\& string::operator\+\= (const char\* str)** **string\& string::append (const char\* str)** * 两个函数都将str的字符追加到原字符串末尾 * 均返回\*this以支持链式调用 * 若结果超出最大字符数限制会抛出length_error异常 * str不可为NULL 示例代码：  ``` std::string sString{"one"};  sString += " two"; sString.append(" three"); std::cout << sString << '\n'; ```  输出：  ``` one two three  ``` |
| --- |  

append() 还有另一个针对C风格字符串的变体：  

| **string\& string::append (const char\* str, size\_type len)** * 追加str的前len个字符到字符串 * 返回\*this以支持链式调用 * 若结果超出最大字符数抛出length_error异常 * 忽略特殊字符（包括空终止符） 示例代码：  ``` std::string sString{"one "};  sString.append("threefour", 5); std::cout << sString << '\n'; ```  输出：  ``` one three  ```  此函数存在安全隐患，不建议使用。 |
| --- |  

以下函数用于追加单个字符。注意：追加单个字符的非运算符函数名为push_back()而非append()！  

| **string\& string::operator\+\= (char c)** **void string::push\_back (char c)** * 两个函数都将字符c追加到字符串末尾 * operator+=返回\*this以支持链式调用 * 若结果超出最大字符数抛出length_error异常 示例代码：  ``` std::string sString{"one"};  sString += ' '; sString.push_back('2'); std::cout << sString << '\n'; ```  输出：  ``` one 2  ``` |
| --- |  

你可能会疑惑为何使用push_back()而非append()命名。这遵循栈结构的命名惯例——push_back()用于向栈顶添加元素。若将字符串视为字符栈，用push_back()追加字符是合理的。但缺乏append()函数在笔者看来仍不够一致！  

实际上存在以下字符追加的append()变体：  

| **string\& string::append (size\_type num, char c)** * 追加num个字符c到字符串 * 返回\*this以支持链式调用 * 若结果超出最大字符数抛出length_error异常 示例代码：  ``` std::string sString{"aaa"};  sString.append(4, 'b'); std::cout << sString << '\n'; ```  输出：  ``` aaabbbb  ``` |
| --- |  

最后一个append()变体支持迭代器：  

| **string\& string::append (InputIterator start, InputIterator end)** * 追加[start, end)区间内的所有字符（包含start，不包含end） * 返回\*this以支持链式调用 * 若结果超出最大字符数抛出length_error异常 |
| --- |  

[下一课 22.7 — std::string插入操作](Appendix-D/lesson22.7-stdstring-inserting.md)  
[返回主页](/)  
[上一课 22.5 — std::string赋值与交换](Appendix-D/lesson22.5-stdstring-assignment-and-swapping.md)