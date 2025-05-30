28.4 — 字符串流类  
==================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年3月18日 下午2:58 PDT  
2024年2月27日更新  

 

截止目前，您看到的所有I/O示例都使用cout进行输出或通过cin进行输入。但C++还提供另一组**字符串流类（stream classes for strings）**，允许使用熟悉的插入（<<）和提取（>>）运算符操作字符串。与istream和ostream类似，字符串流也提供数据缓冲区。但与cin和cout不同，这些流不连接任何I/O通道（如键盘、显示器等）。字符串流的主要用途包括：缓冲输出以便后续显示，或逐行处理输入。  

C++提供六种字符串流类：  
* 普通字符流：istringstream（继承自istream）、ostringstream（继承自ostream）、stringstream（继承自iostream）  
* 宽字符流：wistringstream、wostringstream、wstringstream  
使用字符串流需要包含\<sstream\>头文件。  

**数据输入方法**  
向stringstream输入数据有两种方式：  
1. 使用插入运算符：  
```cpp
std::stringstream os {};
os << "en garde!\n"; // 将"en garde!"插入字符串流
```  
2. 使用str(string)函数设置缓冲区：  
```cpp
std::stringstream os {};
os.str("en garde!"); // 设置字符串流缓冲区为"en garde!"
```  

**数据输出方法**  
从stringstream获取数据有两种方式：  
1. 使用str()函数获取缓冲区内容：  
```cpp
std::stringstream os {};
os << "12345 67.89\n";
std::cout << os.str();
```  
输出：  
```
12345 67.89
```  
2. 使用提取运算符：  
```cpp
std::stringstream os {};
os << "12345 67.89"; // 插入数字字符串

std::string strValue {};
os >> strValue;  // 提取"12345"

std::string strValue2 {};
os >> strValue2; // 提取"67.89"

std::cout << strValue << " - " << strValue2 << '\n';
```  
输出：  
```
12345 - 67.89
```  
注意：>>运算符会遍历流中的内容——每次使用>>将返回下一个可提取的值。而str()始终返回整个缓冲区内容，即使已使用过>>运算符。  

**字符串与数字转换**  
由于插入和提取运算符支持所有基本数据类型，我们可以利用它们进行字符串与数字的转换。  

将数字转换为字符串：  
```cpp
std::stringstream os {};

constexpr int nValue { 12345 };
constexpr double dValue { 67.89 };
os << nValue << ' ' << dValue;  // 插入数字

std::string strValue1, strValue2;
os >> strValue1 >> strValue2;   // 提取为字符串

std::cout << strValue1 << ' ' << strValue2 << '\n';  // 输出：12345 67.89
```  

将数字字符串转换为数字：  
```cpp
std::stringstream os {};
os << "12345 67.89";  // 插入数字字符串

int nValue {};
double dValue {};
os >> nValue >> dValue;  // 提取为数字

std::cout << nValue << ' ' << dValue << '\n';  // 输出：12345 67.89
```  

**清空字符串流复用**  
清空stringstream缓冲区的几种方法：  
1. 使用空C风格字符串设置str()：  
```cpp
std::stringstream os {};
os << "Hello ";
os.str("");  // 清空缓冲区
os << "World!";
std::cout << os.str();  // 输出：World!
```  
2. 使用空std::string对象设置str()：  
```cpp
std::stringstream os {};
os << "Hello ";
os.str(std::string{});  // 清空缓冲区
os << "World!";
std::cout << os.str();  // 输出：World!
```  

建议在清空时同时调用clear()：  
```cpp
std::stringstream os {};
os << "Hello ";
os.str("");  // 清空缓冲区
os.clear();  // 重置错误标志
os << "World!";
std::cout << os.str();
```  
clear()会重置可能设置的错误标志，使流回到正常状态（关于流状态和错误标志将在下一课详细讲解）。  

[下一课 28.5 — 流状态与输入验证](Chapter-28/lesson28.5-stream-states-and-input-validation.md)  
[返回主页](/)  
[上一课 28.3 — ostream与ios的输出](Chapter-28/lesson28.3-output-with-ostream-and-ios.md)