15.4 — 析构函数（destructor）简介  
===================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2024年9月23日（首次发布于2023年9月11日）  

清理（cleanup）问题  
----------------  

假设您正在编写需要通过网络发送数据的程序。由于建立服务器连接成本较高，您希望收集批量数据后一次性发送。对应的类可能如下：  

```cpp
// 此示例因（故意）不完整而无法编译
class NetworkData
{
private:
    std::string m_serverName{};  // 服务器名称
    DataStore m_dataQueue{};     // 数据队列

public:
	NetworkData(std::string_view serverName)
		: m_serverName { serverName }
	{
	}

	void addData(std::string_view data)  // 添加数据
	{
		m_dataQueue.add(data);
	}

	void sendData()  // 发送数据
	{
		// 连接服务器
		// 发送所有数据
		// 清空队列
	}
};

int main()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    n.sendData();

    return 0;
}
```  

该`NetworkData`类存在潜在问题：依赖用户在程序关闭前显式调用`sendData()`。若用户忘记此操作，数据将无法发送并在程序退出时丢失。在更复杂的场景中，例如以下函数：  

```cpp
bool someFunction()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    if (someCondition)
        return false;  // 条件成立时提前返回

    n.sendData();
    return true;
}
```  

当`someCondition`为`true`时，函数提前返回导致`sendData()`未执行。这类错误更易发生，因为代码中虽然存在发送调用，但并非所有执行路径都会触发。  

使用资源（如内存、文件、数据库、网络连接等）的类，通常需要在对象销毁前显式发送或关闭资源。有时还需执行销毁前的记录工作（如写入日志或发送遥测数据）。**清理（clean up）**指类对象销毁前必须完成的任务集合。若依赖用户手动调用清理函数，极易引发错误。  

析构函数（destructor）的解决方案  
----------------  

构造函数（constructor）用于初始化成员变量和准备对象（见课程[14.9 — 构造函数简介](Chapter-14/lesson14.9-introduction-to-constructors.md)）。同理，**析构函数（destructor）**是类在对象销毁时自动调用的特殊成员函数，用于执行必要的清理操作。  

析构函数命名规则  
----------------  

1. 名称与类名相同，前缀波浪号（~）  
2. 不能接受参数  
3. 无返回类型  

每个类只能有一个析构函数。通常不应显式调用析构函数（对象销毁时自动调用），因为重复清理对象的情况极少。析构函数可安全调用其他成员函数，因为对象在析构函数执行完成后才被销毁。  

析构函数示例  
----------------  

```cpp
#include <iostream>

class Simple
{
private:
    int m_id {};

public:
    Simple(int id)
        : m_id { id }
    {
        std::cout << "构造 Simple " << m_id << '\n';
    }

    ~Simple() // 析构函数
    {
        std::cout << "析构 Simple " << m_id << '\n';
    }

    int getID() const { return m_id; }
};

int main()
{
    Simple simple1{ 1 };
    {
        Simple simple2{ 2 };
    } // simple2在此处销毁

    return 0;
} // simple1在此处销毁
```  

输出结果：  
```
构造 Simple 1  
构造 Simple 2  
析构 Simple 2  
析构 Simple 1  
```  

注意销毁顺序：`simple2`在代码块结束时销毁，`simple1`在`main()`结束时销毁。静态变量（包括全局变量和静态局部变量）在程序启动时构造，程序关闭时销毁。  

改进NetworkData程序  
----------------  

通过析构函数自动调用`sendData()`：  

```cpp
class NetworkData
{
private:
    std::string m_serverName{};
    DataStore m_dataQueue{};

public:
	NetworkData(std::string_view serverName)
		: m_serverName { serverName }
	{
	}

	~NetworkData()
	{
		sendData(); // 对象销毁前确保发送数据
	}

	void addData(std::string_view data)
	{
		m_dataQueue.add(data);
	}

	void sendData()
	{
		// 连接服务器
		// 发送所有数据
		// 清空队列
	}
};

int main()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    return 0;
}
```  

此时`NetworkData`对象销毁前总会发送数据，自动完成清理，减少出错可能。  

隐式析构函数（implicit destructor）  
----------------  

若类未声明析构函数，编译器将生成空函数体的隐式析构函数。若类无需清理操作，可不定义析构函数，由编译器生成。  

关于`std::exit()`的警告  
----------------  

使用`std::exit()`立即终止程序时（见课程[8.12 — 提前终止程序](Chapter-8/lesson8.12-halts-exiting-your-program-early.md)），局部变量不会销毁，析构函数不会调用。若依赖析构函数执行必要清理，需特别注意此情况。  

高级内容  
----------------  

未处理的异常也会导致程序终止，且可能不进行栈展开（stack unwinding）。若未展开栈，程序终止前不会调用析构函数。  

[下一课 15.5 — 包含成员函数的类模板](Chapter-15/lesson15.5-class-templates-with-member-functions.md)  
[返回主页](/)  
[上一课 15.3 — 嵌套类型（成员类型）](Chapter-15/lesson15.3-nested-types-member-types.md)