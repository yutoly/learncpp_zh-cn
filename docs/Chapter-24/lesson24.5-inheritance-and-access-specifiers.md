24.5 — 继承与访问说明符  
=========================================  

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  

2008年1月14日 PST下午1:09（首次发布于2023年9月11日）  

 

在本章之前的课程中，我们已经学习了基类继承的基础知识。迄今为止的所有示例都使用了公开继承（public inheritance），即派生类（derived class）公开继承基类（base class）。  

本节我们将深入探讨公开继承，以及另外两种继承类型（私有（private）和受保护（protected）继承）。我们还将研究不同继承类型如何与访问说明符（access specifiers）交互，以允许或限制成员访问。  

到目前为止，我们已经见过private和public访问说明符，它们决定了谁能访问类的成员。简要回顾：  
- public成员可以被任何代码访问  
- private成员只能被同一类的成员函数或友元（friend）访问  
这意味着派生类不能直接访问基类的private成员！  

```cpp
class Base
{
private:
    int m_private {}; // 仅Base成员和友元可访问（派生类不可访问）
public:
    int m_public {}; // 任何代码均可访问
};
```  

当涉及继承时，情况会变得更加复杂。  

### 受保护（protected）访问说明符  
C++第三个访问说明符专门用于继承场景。**protected**访问说明符允许类本身、友元以及派生类访问成员，但protected成员仍不可从类外部访问。  

```cpp
class Base
{
public:
    int m_public {};       // 任何代码均可访问
protected:
    int m_protected {};    // Base成员、友元和派生类可访问
private:
    int m_private {};      // 仅Base成员和友元可访问
};

class Derived: public Base
{
public:
    Derived()
    {
        m_public = 1;      // 允许：派生类可访问基类public成员
        m_protected = 2;   // 允许：派生类可访问基类protected成员
        m_private = 3;     // 禁止：派生类不可访问基类private成员
    }
};

int main()
{
    Base base;
    base.m_public = 1;     // 允许：外部可访问public成员
    base.m_protected = 2;  // 禁止：外部不可访问protected成员
    base.m_private = 3;    // 禁止：外部不可访问private成员

    return 0;
}
```  

在上述示例中，protected成员m_protected可被派生类直接访问，但不可被外部访问。  

#### 何时使用protected访问说明符？  
当基类的protected属性被修改时（如类型、含义等），通常需要同时修改基类和所有派生类。因此protected成员最适合以下场景：  
- 您或团队将自行编写派生类  
- 派生类数量可控  
这样在基类实现变更时，可以高效更新相关派生类。  

private成员能更好地隔离派生类和外部代码，但需要提供更大的公开接口。通常建议优先使用private成员。  

**最佳实践**  
优先使用private成员，仅在必要时使用protected成员。  

### 不同继承类型及其影响  
C++支持三种继承方式：  
```cpp
class Pub: public Base {};     // 公开继承
class Pro: protected Base {};  // 受保护继承
class Pri: private Base {};    // 私有继承
class Def: Base {};            // 默认私有继承
```  

继承类型会影响派生类中基类成员的访问级别：  

#### 公开继承（Public Inheritance）  
- 基类public成员保持public  
- 基类protected成员保持protected  
- 基类private成员不可访问  

| 基类访问说明符 | 公开继承后的访问级别 |  
|----------------|---------------------|  
| public         | public              |  
| protected      | protected           |  
| private        | 不可访问            |  

```cpp
class Pub: public Base
{
public:
    Pub()
    {
        m_public = 1;    // 允许：继承为public
        m_protected = 2; // 允许：继承为protected
        m_private = 3;   // 禁止
    }
};
```  

**最佳实践**  
除非有特殊需求，否则始终使用公开继承。  

#### 受保护继承（Protected Inheritance）  
- 基类public和protected成员变为protected  
- 基类private成员不可访问  

| 基类访问说明符 | 受保护继承后的访问级别 |  
|----------------|-----------------------|  
| public         | protected             |  
| protected      | protected             |  
| private        | 不可访问              |  

#### 私有继承（Private Inheritance）  
- 基类public和protected成员变为private  
- 基类private成员不可访问  

| 基类访问说明符 | 私有继承后的访问级别 |  
|----------------|---------------------|  
| public         | private             |  
| protected      | private             |  
| private        | 不可访问            |  

```cpp
class Pri: private Base
{
public:
    Pri()
    {
        m_public = 1;    // 允许：变为private
        m_protected = 2; // 允许：变为private 
        m_private = 3;   // 禁止
    }
};

int main()
{
    Pri pri;
    pri.m_public = 1;    // 禁止：在Pri中为private
    // 其他成员同理
}
```  

私有继承适用于派生类与基类没有明显关系，但需要复用基类实现的场景。实践中较少使用。  

### 综合示例  
```cpp
class Base
{
public:     int m_public {};
protected:  int m_protected {};
private:    int m_private {};
};

class D2 : private Base 
{
public:     int m_public2 {};
protected:  int m_protected2 {};
private:    int m_private2 {};
};

class D3 : public D2 
{
public:     int m_public3 {};
protected:  int m_protected3 {};
private:    int m_private3 {};
};
```  

- D2可访问Base的m_public和m_protected（变为private）  
- D3可访问D2的m_public2和m_protected2，但无法访问Base的任何成员  

### 总结  
访问说明符与继承类型的交互规则：  

| 基类访问说明符 | 公开继承 | 私有继承 | 受保护继承 |  
|----------------|----------|----------|------------|  
| public         | public   | private  | protected  |  
| protected      | protected| private  | protected  |  
| private        | 不可访问 | 不可访问 | 不可访问   |  

这些规则适用于所有成员（包括成员函数和嵌套类型）。  

[下一课 24.6 — 向派生类添加新功能](Chapter-24/lesson24.6-adding-new-functionality-to-a-derived-class.md)  
[返回主页](/)  
[上一课 24.4 — 派生类的构造函数与初始化](Chapter-24/lesson24.4-constructors-and-initialization-of-derived-classes.md)