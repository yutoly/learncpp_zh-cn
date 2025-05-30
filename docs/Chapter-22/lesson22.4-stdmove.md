22.4 — std::move  
=================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2024年5月8日（首次发布于2017年3月4日）  

当您开始频繁使用移动语义时，会遇到需要调用移动语义但操作对象是左值（l-value）而非右值（r-value）的情形。以下面这个交换函数为例：  

```cpp
#include <iostream>
#include <string>

template <typename T>
void mySwapCopy(T& a, T& b) 
{ 
	T tmp { a }; // 调用拷贝构造函数
	a = b; // 调用拷贝赋值运算符
	b = tmp; // 调用拷贝赋值运算符
}

int main()
{
	std::string x{ "abc" };
	std::string y{ "de" };

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	mySwapCopy(x, y);

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	return 0;
}
```  

该函数通过三次拷贝交换两个类型T（本例为std::string）对象的值。程序输出：  

```
x: abc
y: de
x: de
y: abc
```  

正如前文所述，拷贝操作可能效率低下。本例中的swap函数进行了三次拷贝，导致大量字符串创建和销毁，非常耗时。  

然而此处无需拷贝操作。我们只需交换a和b的值，这完全可以通过三次移动实现！若将拷贝语义替换为移动语义，代码性能将显著提升。  

但如何实现？问题在于参数a和b是左值引用而非右值引用，因此无法触发移动构造函数和移动赋值运算符。默认情况下，拷贝构造函数和拷贝赋值运算符会被调用。如何解决？  

 
std::move  
----------------  

在C++11中，**std::move**是一个标准库函数，通过静态转换（static_cast）将参数转为右值引用以触发移动语义。因此，我们可以使用std::move将左值转换为优先触发移动而非拷贝的类型。std::move定义于utility头文件。  

以下是与前例相同的程序，但改用mySwapMove()函数通过std::move将左值转为右值以触发移动语义：  

```cpp
#include <iostream>
#include <string>
#include <utility> // 包含std::move

template <typename T>
void mySwapMove(T& a, T& b) 
{ 
	T tmp { std::move(a) }; // 调用移动构造函数
	a = std::move(b); // 调用移动赋值运算符
	b = std::move(tmp); // 调用移动赋值运算符
}

int main()
{
	std::string x{ "abc" };
	std::string y{ "de" };

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	mySwapMove(x, y);

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	return 0;
}
```  

输出结果与前例相同：  

```
x: abc
y: de
x: de
y: abc
```  

但效率更高。初始化tmp时，使用std::move将左值变量x转为右值。由于参数是右值，触发移动语义，x的内容被移动至tmp。  

通过几次交换操作，变量x的值被移动至y，y的值被移动至x。  

 
其他示例  
----------------  

我们也可以在向容器（如std::vector）填充左值元素时使用std::move。  

以下程序中，首先使用拷贝语义向vector添加元素，然后使用移动语义添加元素：  

```cpp
#include <iostream>
#include <string>
#include <utility> // 包含std::move
#include <vector>

int main()
{
	std::vector<std::string> v;

	// 使用std::string（可移动类型，std::string_view不可移动）
	std::string str { "Knock" };

	std::cout << "拷贝str\n";
	v.push_back(str); // 调用左值版本的push_back，将str拷贝至数组元素
	
	std::cout << "str: " << str << '\n';
	std::cout << "vector: " << v[0] << '\n';

	std::cout << "\n移动str\n";

	v.push_back(std::move(str)); // 调用右值版本的push_back，将str移动至数组元素
	
	std::cout << "str: " << str << '\n'; // 结果不确定
	std::cout << "vector:" << v[0] << ' ' << v[1] << '\n';

	return 0;
}
```  

在作者机器上输出：  

```
拷贝str
str: Knock
vector: Knock

移动str
str:
vector: Knock Knock
```  

第一种情况传递左值给push_back()，使用拷贝语义添加元素，因此str保留原值。  

第二种情况通过std::move传递右值给push_back()，使用移动语义添加元素。这种方式更高效，因为vector元素可以直接"窃取"字符串值而无需拷贝。  

 
被移动对象处于有效但不确定状态  
----------------  

当从临时对象移动值时，被移动对象的残留值无关紧要，因为临时对象会立即销毁。但对于使用std::move的左值对象，我们可能在移动后继续访问它们（如上述示例中在移动后打印str的值），此时了解其残留状态很重要。  

对此有两种观点：一种认为被移动对象应重置为默认/空状态，不再持有资源；另一种认为应根据便利性处理，不强求清除被移动对象。  

C++标准规定："除非另有说明，被移动后的对象（标准库定义类型）应处于有效但未指定的状态。"  

在上例中，作者在调用std::move后打印str得到空字符串，但这并非强制要求，可能输出任何有效字符串。因此应避免使用被移动对象的值，因为结果取决于具体实现。  

某些情况下我们希望重用被移动对象（而非分配新对象）。例如上述mySwapMove()实现中，我们先将资源移出a，再将新资源移入a。这是安全的，因为在移出和赋予新值之间未使用a的值。  

对于被移动对象，调用不依赖其当前值的函数是安全的。这包括设置或重置对象值（使用operator=、clear()或reset()成员函数），或检测对象状态（如使用empty()检查是否为空）。但应避免使用operator[]或front()等依赖容器元素的函数，因为被移动容器可能为空。  

 
关键洞察  
----------------  

`std::move()`向编译器提示程序员不再需要对象的当前值。仅在需要移动持久对象的值时使用`std::move()`，之后不要对该对象的值做任何假设。允许在被移动对象上赋予新值（如使用operator=）。  

 
其他应用场景  
----------------  

std::move在排序数组元素时也很有用。许多排序算法（如选择排序和冒泡排序）通过交换元素对实现。过去我们使用拷贝语义进行交换，现在可使用更高效的移动语义。  

在需要将智能指针管理的内容移动到另一个智能指针时，std::move也很有用。  

 
相关内容  
----------------  

`std::move()`有一个变体`std::move_if_noexcept()`，若对象具有`noexcept`移动构造函数则返回可移动右值，否则返回可拷贝左值。详见课程[27.10 — std::move_if_noexcept](Chapter-27/lesson27.10-stdmove_if_noexcept.md)。  

 
总结  
----------------  

当需要将左值视为右值以触发移动语义而非拷贝语义时，均可使用std::move。  

[下一课 22.5 std::unique_ptr](Chapter-22/lesson22.5-stdunique_ptr.md)  
[返回主页](/)  
[上一课 22.3 移动构造函数与移动赋值](Chapter-22/lesson22.3-move-constructors-and-move-assignment.md)