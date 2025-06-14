28.1 — 输入与输出（I/O）流  
======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年2月28日（2023年9月11日更新）  

输入输出功能并非C++核心语言组成部分，而是通过C++标准库提供（因此位于std命名空间）。在前面的课程中，您已通过包含iostream库头文件并使用cin与cout对象进行简单I/O操作。本章我们将深入探讨iostream库。  

**iostream库**  
当包含iostream头文件时，您将获得整个负责提供I/O功能的类层次结构的访问权限（其中包含实际名为iostream的类）。非文件I/O类的层次结构图可[在此查看](https://en.cppreference.com/w/cpp/io)。  

该层次结构首先引人注目的是使用了多重继承（我们曾建议尽量避免的特性）。然而iostream库经过精心设计与全面测试，避免了典型多重继承问题，因此可放心使用。  

**流（streams）**  
第二个高频出现的术语是"流"。C++的I/O机制本质上是通过流实现的。抽象而言，**流（stream）**是一个可以顺序访问的字节序列。随着时间的推移，流可能产生或消耗无限量的数据。  

通常我们处理两种流类型：  
* **输入流（input streams）**：用于保存来自数据生产者（如键盘、文件或网络）的输入。例如当程序未预期输入时用户按下键盘，数据会存入输入流等待程序读取。  
* **输出流（output streams）**：用于保存给特定数据消费者（如显示器、文件或打印机）的输出。当向输出设备写入数据时（如打印机预热期间），数据会暂存于输出流中。  

部分设备（如文件和网络）可同时作为输入/输出源。  

流的优势在于程序员只需学习与流交互的方法，即可实现对多种设备的读写。流与实际设备的连接细节由环境或操作系统处理。  

**C++中的输入输出**  
`ios`是`std::basic_ios<char>`的类型别名，定义了输入/输出流的通用特性（后续课程详述）。  

* **istream**类：处理输入流的核心类，使用**提取运算符（>>）**从流中获取值。例如键盘按键后，键码存入输入流，程序通过提取运算符获取值。  
* **ostream**类：处理输出流的核心类，使用**插入运算符（<<）**向流中添加值。例如将值插入流后，显示器等消费者会使用这些值。  
* **iostream**类：可同时处理输入输出，支持双向I/O。  

**C++标准流**  
**标准流（standard stream）**是环境为程序提供的预连接流。C++预定义了四个标准流对象：  

1. **cin** — 绑定标准输入（通常为键盘）的istream对象  
2. **cout** — 绑定标准输出（通常为显示器）的ostream对象  
3. **cerr** — 绑定标准错误（通常为显示器）的ostream对象，提供未缓冲输出（unbuffered output）  
4. **clog** — 绑定标准错误（通常为显示器）的ostream对象，提供缓冲输出（buffered output）  

未缓冲输出通常立即处理，缓冲输出则暂存后以块形式写入。由于clog使用频率较低，常被排除在标准流列表之外。  

[下一课 28.2 — 使用istream进行输入](Chapter-28/lesson28.2-input-with-istream.md)  
[返回主页](/)    
[上一课 27.x — 第27章总结与测验](Chapter-27/lesson27.x-chapter-27-summary-and-quiz.md)