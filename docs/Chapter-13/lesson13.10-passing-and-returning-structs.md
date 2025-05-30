13.10 — 结构体的传递与返回  
======================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2022年1月18日 上午10:24（PST）  
2024年11月29日更新  

考虑用三个独立变量表示员工信息：  
```
int main()
{
    int id { 1 };
    int age { 24 };
    double wage { 52400.0 };

    return 0;
}
```  
若需将此员工信息传递给函数，必须传递三个变量：  
```
#include <iostream>

void printEmployee(int id, int age, double wage)
{
    std::cout << "ID:   " << id << '\n';
    std::cout << "Age:  " << age << '\n';
    std::cout << "Wage: " << wage << '\n';
}

int main()
{
    int id { 1 };
    int age { 24 };
    double wage { 52400.0 };

    printEmployee(id, age, wage);

    return 0;
}
```  
传递三个独立变量尚可接受，但若需传递10或12个员工变量时，逐个传递既费时又易错。此外，若为员工添加新属性（如姓名），则需修改所有相关函数的声明、定义及调用！  

**按引用传递结构体**  
相较于独立变量，结构体的核心优势在于可将整个结构体传递给需要操作其成员的函数。通常通过引用（常为常量引用）传递结构体以避免拷贝：  
```
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

void printEmployee(const Employee& employee) // 注意此处按引用传递
{
    std::cout << "ID:   " << employee.id << '\n';
    std::cout << "Age:  " << employee.age << '\n';
    std::cout << "Wage: " << employee.wage << '\n';
}

int main()
{
    Employee joe { 14, 32, 24.15 };
    Employee frank { 15, 28, 18.27 };

    // 打印Joe的信息
    printEmployee(joe);

    std::cout << '\n';

    // 打印Frank的信息
    printEmployee(frank);

    return 0;
}
```  
该程序输出：  
```
ID:   14
Age:  32
Wage: 24.15

ID:   15
Age:  28
Wage: 18.27
```  
无论结构体有多少成员，仅需单个参数即可传递整个对象。未来若为`Employee`添加新成员，也无需修改函数声明或调用！  

**相关内容**  
关于按值传递与按引用传递的抉择，详见课程[12.6 — 按常量左值引用传递](Chapter-12/lesson12.6-pass-by-const-lvalue-reference.md)。  

**传递临时结构体**  
前例中在传递前创建了具名Employee变量`joe`，这有助于文档化但需要两条语句。若变量仅使用一次，可改用临时对象（无标识符）：  
```
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

void printEmployee(const Employee& employee)
{
    std::cout << "ID:   " << employee.id << '\n';
    std::cout << "Age:  " << employee.age << '\n';
    std::cout << "Wage: " << employee.wage << '\n';
}

int main()
{
    // 打印Joe的信息（显式指定类型）
    printEmployee(Employee { 14, 32, 24.15 });

    std::cout << '\n';

    // 打印Frank的信息（参数推导类型）
    printEmployee({ 15, 28, 18.27 });

    return 0;
}
```  
创建临时对象的两种方式：  
1. `Employee { ... }`（推荐，明确类型）  
2. `{ ... }`（隐式转换，不适用于需显式转换的场合）  

**相关内容**  
临时对象详见课程[14.13 — 临时类对象](Chapter-14/lesson14.13-temporary-class-objects.md)。  

**临时对象的特性**：  
- 在定义点创建并初始化  
- 在完整表达式结束时销毁  
- 作为右值表达式，只能用于接受右值的场景  
- 作为函数参数时，仅能绑定到接受右值的参数（按值传递、按常量引用传递）  

**返回结构体**  
考虑返回三维空间点的函数，需返回三个坐标值。解决方案是返回结构体：  
```
#include <iostream>

struct Point3d
{
    double x { 0.0 };
    double y { 0.0 };
    double z { 0.0 };
};

Point3d getZeroPoint()
{
    Point3d temp { 0.0, 0.0, 0.0 };
    return temp;
}

int main()
{
    Point3d zero{ getZeroPoint() };

    if (zero.x == 0.0 && zero.y == 0.0 && zero.z == 0.0)
        std::cout << "The point is zero\n";
    else
        std::cout << "The point is not zero\n";

    return 0;
}
```  
输出：  
```
The point is zero
```  

优化返回方式，使用无名临时对象：  
```
Point3d getZeroPoint()
{
    return Point3d { 0.0, 0.0, 0.0 }; // 返回无名对象
}
```  
进一步简化：  
```
Point3d getZeroPoint()
{
    return { 0.0, 0.0, 0.0 }; // 隐式转换
}

// 或使用值初始化
Point3d getZeroPoint()
{
    return {}; // 值初始化
}
```  

**结构体的重要性**  
结构体不仅是独立工具，更是类（C++面向对象核心）的基础。掌握结构体（数据成员、成员选择、默认成员初始化）有助于顺利过渡到类的学习。  

**测验时间**  
**问题1**  
编写广告收益计算程序，要求：  
- 输入广告展示量、点击率、单次点击收益  
- 存储于结构体  
- 传递结构体给打印函数，计算并显示日收益  

  
<details><summary>答案</summary>  
```
#include <iostream>

struct Advertising
{
    int adsShown {};
    double clickThroughRatePercentage {};
    double averageEarningsPerClick {};
};

Advertising getAdvertising()
{
    Advertising temp {};
    std::cout << "今日广告展示量？ ";
    std::cin >> temp.adsShown;
    std::cout << "用户点击百分比？ ";
    std::cin >> temp.clickThroughRatePercentage;
    std::cout << "单次点击平均收益？ ";
    std::cin >> temp.averageEarningsPerClick;

    return temp;
}

void printAdvertising(const Advertising& ad)
{
    std::cout << "广告展示量：" << ad.adsShown << '\n';
    std::cout << "点击率：" << ad.clickThroughRatePercentage << "%\n";
    std::cout << "单次点击收益：$" << ad.averageEarningsPerClick << '\n';

    std::cout << "日收益：$"
        << (ad.adsShown * ad.clickThroughRatePercentage / 100 * ad.averageEarningsPerClick) << '\n';
}

int main()
{
    Advertising ad{ getAdvertising() };
    printAdvertising(ad);
    return 0;
}
```  
</details>  

**问题2**  
创建分数结构体，实现分数输入、相乘及打印功能。  

  
<details><summary>答案</summary>  
```
#include <iostream>

struct Fraction
{
    int numerator{ 0 };
    int denominator{ 1 };
};

Fraction getFraction()
{
    Fraction temp{};
    std::cout << "输入分子：";
    std::cin >> temp.numerator;
    std::cout << "输入分母：";
    std::cin >> temp.denominator;
    std::cout << '\n';
    return temp;
}

constexpr Fraction multiply(const Fraction& f1, const Fraction& f2)
{
    return { f1.numerator * f2.numerator, f1.denominator * f2.denominator };
}

void printFraction(const Fraction& f)
{
    std::cout << f.numerator << '/' << f.denominator << '\n';
}

int main()
{
    Fraction f1{ getFraction() };
    Fraction f2{ getFraction() };

    std::cout << "分数乘积：";
    printFraction(multiply(f1, f2));
    return 0;
}
```  
</details>  

**问题3**  
为何`getFraction()`按值返回而非引用？  
  
<details><summary>答案</summary>  
因局部变量`temp`在函数结束时销毁，返回引用会导致悬垂引用。</details>  

[下一课 13.11 结构体杂项](Chapter-13/lesson13.11-struct-miscellany.md)  
[返回主页](/)  
[上一课 13.9 默认成员初始化](Chapter-13/lesson13.9-default-member-initialization.md)