21.14 — 运算符重载与函数模板  
=====================================================  

[*Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2008年4月29日 下午8:14（太平洋夏令时）  
2023年9月11日  

在课程[11.7 — 函数模板实例化](Chapter-11/lesson11.7-function-template-instantiation.md)中，我们讨论了编译器如何使用函数模板（function template）实例化函数并进行编译。我们还指出，如果函数模板中的代码尝试执行某些实际类型不支持的操作（例如给`std::string`添加整数值`1`），这些函数可能无法编译。


本节我们将通过几个实例说明当实际类类型不支持某些运算符时，实例化函数（instantiated functions）如何导致编译错误，并展示如何定义这些运算符以使实例化函数通过编译。


运算符、函数调用与函数模板  
----------------  

首先创建一个简单类：  

```cpp
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};
```  

接着定义`max`函数模板：  

```cpp
template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}
```  

现在尝试用`Cents`类型对象调用`max()`：  

```cpp
#include <iostream>

class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};

template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}

int main()
{
    Cents nickel{ 5 };
    Cents dime{ 10 };

    Cents bigger { max(nickel, dime) };
    std::cout << bigger << " is bigger\n";

    return 0;
}
```  

C++将生成如下`max()`模板实例：  

```cpp
template <>
const Cents& max(const Cents& x, const Cents& y)
{
    return (x < y) ? y : x;
}
```  

编译器尝试编译此函数时会发现问题：当`x`和`y`为`Cents`类型时，无法评估`x < y`！因此将产生编译错误。


解决方法是为需要调用`max`的类重载`operator<`：  

```cpp
#include <iostream>

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }
    
    friend bool operator< (const Cents& c1, const Cents& c2)
    {
        return (c1.m_cents < c2.m_cents);
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};

template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}

int main()
{
    Cents nickel{ 5 };
    Cents dime { 10 };

    Cents bigger { max(nickel, dime) };
    std::cout << bigger << " is bigger\n";

    return 0;
}
```  

程序正常运行并输出：  

```
10 is bigger
```  

另一个示例  
----------------  

再举一个因缺少运算符重载导致函数模板无法工作的示例。


以下函数模板用于计算数组元素的平均值：  

```cpp
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

int main()
{
    int intArray[] { 5, 3, 2, 1, 4 };
    std::cout << average(intArray, 5) << '\n';

    double doubleArray[] { 3.12, 3.45, 9.23, 6.34 };
    std::cout << average(doubleArray, 4) << '\n';

    return 0;
}
```  

输出结果为：  

```
3
5.535
```  

可见该模板对内置类型有效！


现在尝试在`Cents`类上调用此函数：  

```cpp
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
```  

编译器将产生大量错误信息！首条错误如下：  

```
错误 C2679: 未找到接受右操作数为Cents类型的<<运算符
```  

注意`average()`返回`Cents`对象，而我们尝试用`operator<<`将其输出到`std::cout`，但尚未为`Cents`类定义该运算符。添加定义：  

```cpp
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Cents& cents)
    {
        out << cents.m_cents << " 分";
        return out;
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
```  

再次编译将出现新错误：  

```
错误 C2676: Cents未定义+=运算符或可接受的类型转换
```  

该错误源于调用`average(const Cents*, int)`时生成的函数模板实例。当`T`为`Cents`时，模板实例为：  

```cpp
template <>
Cents average(const Cents* myArray, int numValues)
{
    Cents sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}
```  

错误源于代码行：  

```cpp
        sum += myArray[count];
```  

此处`sum`是`Cents`对象，但未定义`operator+=`！需定义该运算符及`operator/=`：  

```cpp
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Cents& cents)
    {
        out << cents.m_cents << " 分";
        return out;
    }

    Cents& operator+= (const Cents &cents)
    {
        m_cents += cents.m_cents;
        return *this;
    }

    Cents& operator/= (int x)
    {
        m_cents /= x;
        return *this;
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
```  

最终代码成功编译运行，输出：  

```
11 分
```  

注意我们无需修改`average()`即可使其支持`Cents`类型，只需为`Cents`类定义所需的运算符，编译器将处理其余工作！



[下一课 21.x — 第21章总结与测验](Chapter-21/lesson21.x-chapter-21-summary-and-quiz.md)  
[返回主页](/)  
[上一课 21.13 — 浅拷贝与深拷贝](Chapter-21/lesson21.13-shallow-vs-deep-copying.md)