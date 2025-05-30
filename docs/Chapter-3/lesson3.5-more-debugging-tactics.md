3.5 — 进阶调试策略  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年8月26日（首次发布于2019年2月1日）  

 

在上节课（[3.4 — 基础调试策略](Chapter-3/lesson3.4-basic-debugging-tactics.md)）中，我们探讨了手动调试的基本方法。该课程指出了使用打印语句输出调试信息的局限性：  

1. 调试语句污染代码结构  
2. 调试输出干扰程序正常输出  
3. 调试语句的增删操作可能引入新错误  
4. 调试完成后必须移除语句，无法复用  

本节将介绍优化调试代码的进阶技术。  

条件化调试代码  
----------------  

考虑以下包含调试语句的示例程序：  

```cpp
#include <iostream>
 
int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}
 
int main()
{
std::cerr << "main() called\n";
    int x{ getUserInput() };
    std::cout << "You entered: " << x << '\n';
 
    return 0;
}
```  

调试完成后需移除或注释调试语句，再次需要时又需恢复。通过预处理器指令（preprocessor directive）实现条件化调试可简化此流程：  

```cpp
#include <iostream>
 
#define ENABLE_DEBUG // 注释此行可禁用调试

int getUserInput()
{
#ifdef ENABLE_DEBUG
std::cerr << "getUserInput() called\n";
#endif
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}
 
int main()
{
#ifdef ENABLE_DEBUG
std::cerr << "main() called\n";
#endif
    int x{ getUserInput() };
    std::cout << "You entered: " << x << '\n';
 
    return 0;
}
```  

通过注释/取消注释`#define ENABLE_DEBUG`即可全局控制调试输出。在多文件项目中，可将该宏定义置于头文件中统一管理。此方法虽然解决了调试代码移除问题，但增加了代码冗余。若存在拼写错误或头文件未包含，可能导致部分调试失效。  

日志系统应用  
----------------  

更优的解决方案是使用**日志（log）**系统。日志（logging）是带有时间戳的事件记录，通常保存为**日志文件（log file）**。将调试信息输出到日志文件可避免与程序输出混杂，便于后期分析或共享诊断。  

C++标准库提供`std::clog`流用于日志记录，但其默认输出到标准错误流（与`std::cerr`相同）。实际开发中推荐使用第三方日志库（如[plog](https://github.com/SergiusTheBest/plog)）：  

```cpp
#include <plog/Log.h> // 步骤1：包含日志头文件
#include <plog/Initializers/RollingFileInitializer.h>
#include <iostream>

int getUserInput()
{
	PLOGD << "getUserInput() called"; // PLOGD由plog定义

	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	plog::init(plog::debug, "Logfile.txt"); // 步骤2：初始化日志

	PLOGD << "main() called"; // 步骤3：像控制台输出一样写入日志

	int x{ getUserInput() };
	std::cout << "You entered: " << x << '\n';

	return 0;
}
```  

日志文件`Logfile.txt`输出示例：  

```
2018-12-26 20:03:33.295 DEBUG [4752] [main@19] main() called
2018-12-26 20:03:33.296 DEBUG [4752] [getUserInput@7] getUserInput() called
```  

通过修改初始化参数可关闭日志记录：  

```cpp
plog::init(plog::none , "Logfile.txt"); // plog::none 关闭日志
```  

 

安装说明  
----------------  

在项目中使用plog需遵循以下步骤：  

1. 访问[plog仓库](https://github.com/SergiusTheBest/plog)  
2. 点击绿色"Code"按钮，选择"Download ZIP"  
3. 解压至本地目录  
4. 在IDE中添加`plog-master\include\`为包含目录  

日志文件默认生成在可执行文件同目录。  

> **性能提示**  
> 大型或性能敏感项目推荐使用[spdlog](https://github.com/gabime/spdlog)等高效日志库。  

[下一课 3.6 — 使用集成调试器：单步执行](Chapter-3/lesson3.6-using-an-integrated-debugger-stepping.md)  
[返回主页](/)  
[上一课 3.4 — 基础调试策略](Chapter-3/lesson3.4-basic-debugging-tactics.md)