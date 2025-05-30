22.6 — std::shared_ptr（std::shared_ptr）  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2017年3月16日下午4:04（太平洋夏令时间）  
2024年6月2日

与设计用于单独拥有和管理资源的std::unique_ptr（std::unique_ptr）不同，std::shared_ptr（std::shared_ptr）旨在解决需要多个智能指针共同拥有资源的场景。


这意味着允许多个std::shared_ptr指向同一资源。在内部，std::shared_ptr会追踪共享该资源的std::shared_ptr数量。只要至少有一个std::shared_ptr指向该资源，即使个别std::shared_ptr被销毁，资源也不会被释放。当最后一个管理该资源的std::shared_ptr离开作用域（或被重新指向其他内容）时，资源才会被释放。


与std::unique_ptr类似，std::shared_ptr定义在\<memory\>头文件中。


```cpp
#include <iostream>
#include <memory> // 引入std::shared_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	// 分配Resource对象并由std::shared_ptr管理
	Resource* res { new Resource };
	std::shared_ptr<Resource> ptr1{ res };
	{
		std::shared_ptr<Resource> ptr2 { ptr1 }; // 创建指向同一资源的另一个std::shared_ptr

		std::cout << "销毁一个共享指针\n";
	} // ptr2在此处离开作用域，但无操作执行

	std::cout << "销毁另一个共享指针\n";

	return 0;
} // ptr1在此处离开作用域，分配的Resource被销毁
```

输出结果：

```
Resource acquired
销毁一个共享指针
销毁另一个共享指针
Resource destroyed
```

上述代码中，我们创建动态Resource对象，并由std::shared_ptr类型的ptr1管理。在嵌套代码块中，使用拷贝构造函数创建第二个std::shared_ptr（ptr2）指向同一Resource。当ptr2离开作用域时，Resource未被释放，因为ptr1仍指向该Resource。当ptr1离开作用域时，ptr1检测到没有其他std::shared_ptr管理该资源，于是释放Resource。


注意我们是基于第一个共享指针创建第二个共享指针。这一点至关重要。考虑以下类似程序：


```cpp
#include <iostream>
#include <memory> // 引入std::shared_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	Resource* res { new Resource };
	std::shared_ptr<Resource> ptr1 { res };
	{
		std::shared_ptr<Resource> ptr2 { res }; // 直接从res创建ptr2（而非通过ptr1）

		std::cout << "销毁一个共享指针\n";
	} // ptr2在此处离开作用域，分配的Resource被销毁

	std::cout << "销毁另一个共享指针\n";

	return 0;
} // ptr1在此处离开作用域，试图再次销毁已释放的Resource
```

该程序输出：

```
Resource acquired
销毁一个共享指针
Resource destroyed
销毁另一个共享指针
Resource destroyed
```

随后会崩溃（至少在作者机器上如此）。


差异在于我们独立创建了两个std::shared_ptr。因此，尽管它们指向同一Resource，但彼此并不知晓。当ptr2离开作用域时，它认为自己是Resource的唯一拥有者，于是释放资源。当ptr1随后离开作用域时，也认为自己是唯一拥有者，试图再次删除Resource，导致错误。


幸运的是，这种情况很容易避免：如果需要多个std::shared_ptr指向同一资源，请复制现有的std::shared_ptr。


> **最佳实践**  
> 若需要多个std::shared_ptr指向同一资源，请始终复制现有std::shared_ptr。


与std::unique_ptr类似，std::shared_ptr可以是空指针，因此在使用前应检查其有效性。


std::make_shared（std::make_shared）  
----------------  

类似于C++14中用于创建std::unique_ptr的std::make_unique()，应当使用（且推荐使用）std::make_shared()创建std::shared_ptr。std::make_shared()在C++11中即可用。


以下是使用std::make_shared()的原始示例：


```cpp
#include <iostream>
#include <memory> // 引入std::shared_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	// 分配Resource对象并由std::shared_ptr管理
	auto ptr1 { std::make_shared<Resource>() };
	{
		auto ptr2 { ptr1 }; // 通过ptr1拷贝创建ptr2

		std::cout << "销毁一个共享指针\n";
	} // ptr2在此处离开作用域，但无操作执行

	std::cout << "销毁另一个共享指针\n";

	return 0;
} // ptr1在此处离开作用域，分配的Resource被销毁
```

使用std::make_shared()的理由与std::make_unique()相同——std::make_shared()更简单且更安全（此方法不会创建两个彼此独立的std::shared_ptr指向同一资源）。此外，std::make_shared()比直接构造具有更高性能，原因与std::shared_ptr追踪资源指针数量的方式有关。


深入std::shared_ptr  
----------------  

std::shared_ptr内部使用两个指针，而std::unique_ptr仅使用单个指针。第一个指针指向被管理资源，第二个指针指向"控制块（control block）"——这是一个动态分配的追踪对象，用于记录包括有多少std::shared_ptr指向该资源等信息。当通过构造函数创建std::shared_ptr时，被管理对象的内存（通常传入）和控制块的内存（由构造函数创建）是分别分配的。但使用std::make_shared()时，可优化为单次内存分配，从而提高性能。


这也解释了为何独立创建两个指向同一资源的std::shared_ptr会导致问题。每个std::shared_ptr都有一个指向资源的指针，但各自独立分配的控制块会误认为自己是资源的唯一拥有者。因此当某个std::shared_ptr离开作用域时，会释放资源，却不知还有其他std::shared_ptr也在管理该资源。


但当通过拷贝赋值克隆std::shared_ptr时，控制块数据会被正确更新以反映当前共同管理该资源的std::shared_ptr数量。


 
从unique指针创建shared指针  
----------------  

可通过接受std::unique_ptr右值的特殊构造函数，将std::unique_ptr转换为std::shared_ptr。std::unique_ptr的内容将被移动至std::shared_ptr。


但std::shared_ptr无法安全转换为std::unique_ptr。这意味着如果要创建返回智能指针的函数，最好返回std::unique_ptr，并在适当时机将其赋值给std::shared_ptr。


std::shared_ptr的隐患  
----------------  

std::shared_ptr存在与std::unique_ptr相似的挑战——若std::shared_ptr未被正确释放（或因动态分配后未删除，或因所属对象被动态分配后未删除），其管理资源也无法被释放。对于std::unique_ptr，只需确保单个智能指针正确释放；对于std::shared_ptr，则需确保所有实例都被正确销毁。若管理资源的任一std::shared_ptr未被正确销毁，资源将无法被正确释放。


std::shared_ptr与数组  
----------------  

在C++17及更早版本中，std::shared_ptr对数组的支持不完善，不应被用于管理C风格数组。自C++20起，std::shared_ptr已支持数组管理。


 
结论  
----------------  

std::shared_ptr专为需要多个智能指针共同管理同一资源的场景设计。当最后一个管理资源的std::shared_ptr被销毁时，资源将被释放。


[下一课 22.7 std::shared_ptr的循环依赖问题与std::weak_ptr](Chapter-22/lesson22.7-circular-dependency-issues-with-stdshared_ptr-and-stdweak_ptr.md)  
[返回主页](/)  
[上一课 22.5 std::unique_ptr](Chapter-22/lesson22.5-stdunique_ptr.md)