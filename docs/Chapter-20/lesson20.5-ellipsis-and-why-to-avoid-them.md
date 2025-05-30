20.5 — 省略号（及避免使用的原因）  
========================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年2月22日，下午4:08（PST）  
2023年9月11日  

在迄今所见的所有函数中，函数参数的数量必须预先确定（即使它们有默认值）。但在某些情况下，能够向函数传递可变数量的参数会非常有用。C++提供了称为**省略号（ellipsis）**（即"..."）的特殊说明符来实现此功能。  

由于省略号极少使用且具有潜在危险性，我们建议避免使用，本节可作为选读内容。  

使用省略号的函数形式如下：  

```
返回值类型 函数名(参数列表, ...)
```  

*参数列表*包含一个或多个常规函数参数。注意：使用省略号的函数必须至少有一个非省略号参数。传递给函数的任何实参必须优先匹配参数列表中的形参。  

省略号（以连续三个点表示）必须始终作为函数的最后一个参数。省略号会捕获所有额外实参（若有）。尽管不完全准确，但概念上可将省略号视为存储参数列表之外所有附加参数的数组。  

**省略号示例**  
理解省略号的最佳方式是通过示例。我们编写一个使用省略号的简单程序：假设需要计算多个整数的平均值，实现如下：  

```
#include <iostream>
#include <cstdarg> // 使用省略号所需头文件

// 省略号必须是最后一个参数
// count表示传递的附加参数数量
double findAverage(int count, ...)
{
    int sum{ 0 };

    // 通过va_list访问省略号，声明该类型变量
    std::va_list list;

    // 用va_start初始化va_list
    // 第一参数是待初始化的list，第二参数是最后一个非省略号形参
    va_start(list, count);

    // 遍历所有省略号值
    for (int arg{ 0 }; arg < count; ++arg)
    {
         // 用va_arg从省略号中取值
         // 第一参数是va_list，第二参数是值类型
         sum += va_arg(list, int);
    }

    // 使用后清理va_list
    va_end(list);

    return static_cast<double>(sum) / count;
}

int main()
{
    std::cout << findAverage(5, 1, 2, 3, 4, 5) << '\n';
    std::cout << findAverage(6, 1, 2, 3, 4, 5, 6) << '\n';
    return 0;
}
```  

输出结果：  

```
3
3.5
```  

此函数接收可变数量参数！现在解析示例的组成要素：  

首先必须包含`cstdarg`头文件，它定义了访问省略号参数所需的宏：`va_list`、`va_arg`、`va_start`和`va_end`。  

声明使用省略号的函数时，参数列表必须包含至少一个固定参数。本例中传递的整数表示待求平均值的数字数量，省略号始终置于末尾。  

注意：省略号参数没有名称！需通过`va_list`类型访问其值。概念上可将`va_list`视为指向省略号数组的指针。首先声明`va_list`变量（示例中简化为"list"）。  

接着让`list`指向省略号参数：调用`va_start()`并传入两个参数：`va_list`自身和函数中*最后一个*非省略号形参的名称。调用后，`va_list`将指向省略号的第一个参数。  

通过`va_arg()`获取当前指向的参数值：第一参数是`va_list`，第二参数是待访问参数的类型。注意：`va_arg()`会将`va_list`移动到下一个省略号参数！  

最后用`va_end()`清理`va_list`。  

注意：可随时再次调用`va_start()`将`va_list`重置到省略号的首参数。  

**省略号的危险性：类型检查失效**  
省略号为实现可变参数函数提供了灵活性，但也存在缺点。  

常规函数参数中，编译器通过类型检查确保实参与形参类型匹配（或可隐式转换）。这能防止向需要字符串的函数传递整数（反之亦然）。但省略号参数没有类型声明，编译器会完全跳过类型检查。这意味着可向省略号传递任意类型的实参！然而代价是：当调用函数时省略号参数不合理，编译器不再发出警告。使用省略号时，完全依赖调用者确保传递的参数类型正确，这极易导致错误。  

观察以下微妙错误示例：  

```
    std::cout << findAverage(6, 1.0, 2, 3, 4, 5, 6) << '\n';
```  

第一个省略号参数是`double`而非`int`。这能通过编译但产生意外结果：  

```
1.78782e+008
```  

为何如此？  

计算机以比特序列存储数据，变量类型决定如何将比特序列转换为有效值。但省略号丢弃了变量类型！因此，从省略号获取有效值的唯一方法是手动告知`va_arg()`下一个参数的类型（即其第二参数）。若实际类型与预期类型不匹配，通常会导致错误。  

在`findAverage`中，我们告知`va_arg()`所有参数均为`int`类型，因此每次调用都返回按整数解释的比特序列。  

此例中，传入的第一个`double`类型参数占8字节，而`va_arg(list, int)`每次调用仅返回4字节数据。首次调用读取`double`的前4字节（产生垃圾值），第二次调用读取后4字节（再产生垃圾值），最终结果即为垃圾值。  

由于类型检查失效，即使执行荒谬操作编译器也不会报错：  

```
    int value{ 7 };
    std::cout << findAverage(6, 1.0, 2, "Hello, world!", 'G', &value, &findAverage) << '\n';
```  

这将正常编译，并在作者机器上输出：  

```
1.79766e+008
```  

此结果印证了计算机科学名言："垃圾进，垃圾出（Garbage in, garbage out）"——指计算机会无条件处理无意义的输入数据并产生无意义输出。  

总之：参数类型检查失效，必须信任调用者传递正确类型参数。否则程序只会输出垃圾值（或崩溃）。  

**省略号的另一危险：参数数量未知**  
省略号不仅丢弃参数*类型*，也丢弃参数*数量*。这意味着必须自行跟踪传入省略号的参数数量，通常有三种方法：  

**方法1：传递长度参数**  
让某个固定参数表示可选参数的数量（如`findAverage`示例）。但此方法仍存在问题：  

```
    std::cout << findAverage(6, 1, 2, 3, 4, 5) << '\n'; // 声明6个参数但仅传5个
```  

此调用产生垃圾结果：`va_arg()`前5次返回传入值，第6次返回栈中的垃圾值。更隐蔽的错误：  

```
    std::cout << findAverage(6, 1, 2, 3, 4, 5, 6, 7) << '\n'; // 声明6个参数但传7个
```  

输出`3.5`看似正确，但实际遗漏了最后一个数字（因函数仅处理前6个参数）。这类错误难以排查。  

**方法2：使用哨兵值（sentinel）**  
**哨兵值**是用于终止循环的特殊值。例如字符串以空终止符标记结尾。省略号中通常将哨兵值作为最后一个参数传递：  

```
#include <iostream>
#include <cstdarg>

double findAverage(int first, ...)
{
	int sum{ first }; // 需单独处理首个参数
	std::va_list list;
	va_start(list, first);

	int count{ 1 };
	while (true)
	{
		int arg{ va_arg(list, int) };
		if (arg == -1) // 哨兵值检测
			break;
		sum += arg;
		++count;
	}
	va_end(list);
	return static_cast<double>(sum) / count;
}

int main()
{
	std::cout << findAverage(1, 2, 3, 4, 5, -1) << '\n'; // 以-1结尾
	std::cout << findAverage(1, 2, 3, 4, 5, 6, -1) << '\n';
	return 0;
}
```  

挑战：  
1. C++要求至少一个固定参数（此处`first`作为首个待平均值）  
2. 若用户遗漏哨兵值或传递错误值，函数将无限循环直至遇到匹配哨兵值的垃圾数据（或崩溃）  
3. 哨兵值`-1`仅适用于正数，处理负数需选择有效集外的值  

**方法3：使用解码字符串（decoder string）**  
传递"解码字符串"指示程序如何解析参数：  

```
#include <iostream>
#include <string_view>
#include <cstdarg>

double findAverage(std::string_view decoder, ...)
{
	double sum{ 0 };
	std::va_list list;
	va_start(list, decoder);

	for (auto codetype: decoder)
	{
		switch (codetype)
		{
		case 'i': // 整数类型
			sum += va_arg(list, int);
			break;
		case 'd': // 双精度类型
			sum += va_arg(list, double);
			break;
		}
	}
	va_end(list);
	return sum / std::size(decoder);
}

int main()
{
	std::cout << findAverage("iiiii", 1, 2, 3, 4, 5) << '\n';
	std::cout << findAverage("iiiiii", 1, 2, 3, 4, 5, 6) << '\n';
	std::cout << findAverage("iiddi", 1, 2, 3.5, 4.5, 5) << '\n';
	return 0;
}
```  

此方法支持混合类型参数（如`printf`）。但缺点明显：解码字符串晦涩难懂，若可选参数数量或类型不匹配，仍会导致错误。  

**安全使用省略号的建议**  
1. **尽量避免使用**：通常存在更安全的替代方案（如`findAverage`可改为传递动态整数数组）  
2. **统一参数类型**：所有省略号参数应为相同类型（如全`int`或全`double`），混合类型易引发错误  
3. **优先选用计数/解码法**：比哨兵值更安全，可确保循环在合理次数内终止  

**进阶阅读**  
为改进省略号功能，C++11引入**参数包（parameter packs）**和**可变参数模板（variadic templates）**，在提供类似功能的同时保证强类型检查。但因可用性问题未能广泛采用。  

C++17新增**折叠表达式（fold expressions）**，显著提升了参数包的实用性，现已成为可行替代方案。  

我们将在后续站点更新中介绍这些主题。  

[下一课 20.6 — Lambda表达式入门（匿名函数）](Chapter-20/lesson20.6-introduction-to-lambdas-anonymous-functions.md)  
[返回主页](/)  
[上一课 20.4 — 命令行参数](Chapter-20/lesson20.4-command-line-arguments.md)