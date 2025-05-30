24.x — 第24章总结与测验
===================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2016年10月29日 下午3:32（太平洋时区）  
2024年1月31日更新

**本章总结**  
继承（inheritance）允许我们建立两个对象之间的"是一个（is-a）"关系。被继承的对象称为父类（parent class）、基类（base class）或超类（superclass）。执行继承的对象称为子类（child class）、派生类（derived class）或子类（subclass）。

当派生类（derived class）继承自基类（base class）时，派生类将获得基类的所有成员。

派生类构造时，首先构造类的基类部分，然后构造派生部分。具体流程：  
1. 分配派生类内存（包含基类和派生类所需空间）  
2. 调用适当的派生类构造函数  
3. 使用基类构造函数构造基类对象（若未指定则使用默认构造函数）  
4. 派生类的初始化列表初始化派生类成员  
5. 执行派生类构造函数体  
6. 控制权返回调用者  

析构顺序相反，从最派生的类到最基类的顺序执行。

C++有三个访问说明符（access specifiers）：public、private和protected。protected访问说明符允许所属类、友元和派生类访问受保护成员，但不向公开访问开放。

类的继承方式可以是public、private或protected。实践中通常使用public继承。

以下是访问说明符与继承类型组合的对照表：

| 基类访问说明符 | 公共继承时的访问 | 私有继承时的访问 | 受保护继承时的访问 |
| --- | --- | --- | --- |
| public | public | private | protected |
| private | 不可访问 | 不可访问 | 不可访问 |
| protected | protected | private | protected |

派生类可以添加新函数、修改基类函数行为、改变继承成员的访问级别或隐藏功能。

多重继承（multiple inheritance）允许派生类从多个父类继承成员。除非替代方案会导致更复杂的设计，通常应避免使用多重继承。

**测验时间**  
**问题1**  
判断以下程序的输出结果，或指出无法编译的原因（禁止实际编译，通过代码审查解答）。

a)  
```
...代码略...
```
  
构造顺序从最父类到最子类，析构顺序相反：
```
Base()
Derived()
~Derived()
~Base()
```

b)  
```
...代码略...
```
  
局部变量按定义相反顺序析构：
```
Base()
Derived()
Base()
~Base()
~Derived()
~Base()
```

c)  
```
...代码略...
```
  
无法编译，Derived::print() 无法访问基类私有成员 m_x

d)  
```
...代码略...
```
  
```
Base()
Derived()
Derived: 5
~Derived()
~Base()
```

e)  
```
...代码略...
```
  
```
Base()  
Derived()  
D2()  
Derived: 5  
~D2()  
~Derived()  
~Base()
```

**问题2**  
a) 编写继承自Fruit类的Apple和Banana类，要求实现指定功能。  
```
...实现代码略...
```

b) 添加继承自Apple的GrannySmith类。  
```
...实现代码略...
```

**问题3**  
挑战：实现怪物战斗游戏  
a) 创建Creature类  
```
...实现代码略...
```

b) 创建Player类  
```
...实现代码略...
```

c) 创建Monster类及其Type枚举  
```
class Monster : public Creature
{
public:
    enum Type { dragon, orc, slime, max_types };
};
```

d) 实现Monster构造函数与数据表  
```
...实现代码略...
```

e) 添加随机生成怪物功能  
```
...实现代码略...
```

f) 实现完整游戏逻辑  
```
...完整游戏代码略...
```

g) 附加题：实现药剂系统  
```
...扩展代码略...
```

[下一课 25.1 — 派生类对象的基类指针与引用](Chapter-25/lesson25.1-pointers-and-references-to-the-base-class-of-derived-objects.md)  
[返回主页](/)  
[上一课 24.9 — 多重继承](Chapter-24/lesson24.9-multiple-inheritance.md)