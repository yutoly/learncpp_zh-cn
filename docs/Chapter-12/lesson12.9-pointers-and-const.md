12.9 — 指针与const  
==========================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2025年2月12日（首次发布于2007年7月16日）  

请观察以下代码片段：  

```cpp
int main()
{
    int x { 5 };
    int* ptr { &x }; // ptr是普通（非const）指针

    int y { 6 };
    ptr = &y; // 可以指向其他值

    *ptr = 7; // 可以修改所指向地址的值

    return 0;
}
```  

对于普通（非const）指针，我们既可以改变指针指向的地址（通过给指针赋新地址），也可以改变所指地址存储的值（通过对解引用指针赋值）。  

然而，若我们想指向的值是const类型会发生什么情况呢？  

```cpp
int main()
{
    const int x { 5 }; // x现在是const
    int* ptr { &x };   // 编译错误：无法从const int*转换为int*

    return 0;
}
```  

上述代码无法编译——我们不能将普通指针指向const变量。这是合理的：const变量的值不可更改。若允许程序员将非const指针指向const值，就可以通过解引用指针修改该值，这将破坏变量的const属性。  

指向常量值的指针（Pointer to const value）  
----------------  

**指向常量值的指针（pointer to a const value，有时简称为pointer to const）**是（非const的）指向常量值的指针。  

声明指向const值的指针时，需在指针数据类型前使用`const`关键字：  

```cpp
int main()
{
    const int x{ 5 };
    const int* ptr { &x }; // 正确：ptr指向"const int"

    *ptr = 6; // 不允许：不能修改const值

    return 0;
}
```  

上述示例中，`ptr`指向`const int`。由于指向的数据类型是const，无法通过指针修改该值。  

但由于指向const的指针本身不是const，我们可以改变指针的指向地址：  

```cpp
int main()
{
    const int x{ 5 };
    const int* ptr { &x }; // ptr指向const int x

    const int y{ 6 };
    ptr = &y; // 正确：ptr现在指向const int y

    return 0;
}
```  

如同常量引用（reference to const），指向const的指针也可以指向非const变量。此时指针将所指值视为常量，无论原对象是否定义为const：  

```cpp
int main()
{
    int x{ 5 }; // 非const
    const int* ptr { &x }; // ptr指向"const int"

    *ptr = 6;  // 不允许：ptr指向"const int"，无法通过指针修改值
    x = 6; // 允许：通过非const标识符x访问时值仍可变

    return 0;
}
```  

常量指针（Const pointers）  
----------------  

我们也可以让指针本身成为常量。**常量指针（const pointer）**是在初始化后地址不可变的指针。  

声明常量指针时，需在指针声明中的星号后使用`const`关键字：  

```cpp
int main()
{
    int x{ 5 };
    int* const ptr { &x }; // 星号后的const表示这是常量指针

    return 0;
}
```  

此案例中，`ptr`是（指向非const int值的）常量指针。  

如同普通const变量，常量指针必须在定义时初始化，且不能通过赋值改变其值：  

```cpp
int main()
{
    int x{ 5 };
    int y{ 6 };

    int* const ptr { &x }; // 正确：常量指针初始化为x的地址
    ptr = &y; // 错误：常量指针初始化后不可更改

    return 0;
}
```  

但由于所指向的值是非const的，可以通过解引用常量指针来修改该值：  

```cpp
int main()
{
    int x{ 5 };
    int* const ptr { &x }; // ptr将始终指向x

    *ptr = 6; // 正确：所指向的值是非const的

    return 0;
}
```  

指向常量值的常量指针（Const pointer to a const value）  
----------------  

最后，可以通过在类型前和星号后都使用`const`关键字来声明**指向常量值的常量指针（const pointer to a const value）**：  

```cpp
int main()
{
    int value { 5 };
    const int* const ptr { &value }; // 指向常量值的常量指针

    return 0;
}
```  

指向常量值的常量指针既不能改变地址，也不能通过指针修改所指向的值。只能通过解引用获取当前指向的值。  

指针与const总结  
----------------  

总结以下4条逻辑清晰的规则：  

* **非const指针**（如`int* ptr`）可以重新赋值以改变指向地址  
* **常量指针**（如`int* const ptr`）始终指向同一地址，该地址不可变更  

* **指向非const值的指针**（如`int* ptr`）可以修改所指向的值。这类指针不能指向const值  
* **指向const值的指针**（如`const int* ptr`）通过指针访问时将值视为const，因此不能修改所指向的值。这类指针可以指向const或非const左值（但不能指向右值，因右值无地址）  

理解声明语法可能有些挑战：  

* **星号前的`const`**（如`const int* ptr`）关联于被指向的类型。因此这是指向const值的指针，不能通过指针修改值  
* **星号后的`const`**（如`int* const ptr`）关联于指针本身。因此该指针不能被赋予新地址  

```cpp
int main()
{
    int v{ 5 };
   
    int* ptr0 { &v };             // 指向"int"的非const指针。可修改值或地址
    const int* ptr1 { &v };       // 指向"const int"的非const指针。只能修改地址
    int* const ptr2 { &v };       // 指向"int"的const指针。只能修改值
    const int* const ptr3 { &v }; // 指向"const int"的const指针。值和地址均不可修改

    // 若const在星号左侧，关联于值
    // 若const在星号右侧，关联于指针

    return 0;
}
```  

[下一课 12.10 — 按地址传递](Chapter-12/lesson12.10-pass-by-address.md)  
[返回主页](/)  
[上一课 12.8 — 空指针](Chapter-12/lesson12.8-null-pointers.md)