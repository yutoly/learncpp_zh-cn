23.4 — 关联  
================================================

[*作者：Alex*](https://www.learncpp.com/author/Alex/ "查看 Alex 的所有文章")  
2023年12月7日（首次发布于2016年8月19日）  

在前两课中，我们讨论了两种对象组合类型：组合（composition）与聚合（aggregation）。对象组合用于建模由较简单对象（部件）构建复杂对象的关系。

本课我们将探讨两个无关对象之间更弱化的关系类型——**关联（association）**。与对象组合关系不同，关联关系中不存在隐含的整体/部分关系。

关联  
----------------  

要构成**关联（association）**，对象与另一对象必须满足以下关系：  

* 关联对象（成员）与主对象（类）在其他方面无关联  
* 关联对象（成员）可同时属于多个主对象（类）  
* 关联对象（成员）的生存期*不*由主对象（类）管理  
* 关联对象（成员）可能知晓或不知晓主对象（类）的存在  

与组合或聚合（部件属于整体对象）不同，在关联中，关联对象与主对象并无整体部分关系。如同聚合（aggregation）一样，关联对象可同时属于多个主对象，且不由这些对象管理。但与单向的聚合不同，关联关系可以是单向或双向的（两个对象互相知晓）。

医生与患者的关系是关联的绝佳案例。医生显然与患者存在关系，但概念上不属于部分/整体（对象组合）关系。医生每天可接诊多名患者，患者也可咨询多名医生（如寻求第二意见或专科诊疗）。双方对象的生存期互不依赖。

可以说关联建模为"使用（uses-a）"关系。医生"使用"患者（获取收入），患者使用医生（满足健康需求）。

关联的实现  
----------------  

由于关联是广泛的关系类型，可通过多种方式实现。最常见的方式是使用指针实现，即对象指向关联对象。

本例将实现双向的医生/患者关系，使医生知晓患者名单，反之亦然：

```cpp
#include <functional> // reference_wrapper（引用包装器）
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

// 由于Doctor（医生）与Patient（患者）存在循环依赖，需前向声明Patient
class Patient;

class Doctor
{
private:
    std::string m_name{}; // 姓名
    std::vector<std::reference_wrapper<const Patient>> m_patient{}; // 患者列表

public:
    Doctor(std::string_view name) : m_name{ name } {}

    void addPatient(Patient& patient);
    
    // 将在Patient定义后实现此运算符重载
    friend std::ostream& operator<<(std::ostream& out, const Doctor& doctor);

    const std::string& getName() const { return m_name; }
};

class Patient
{
private:
    std::string m_name{}; // 姓名
    std::vector<std::reference_wrapper<const Doctor>> m_doctor{}; // 医生列表

    // 设为私有以防止外部调用，应通过公开的Doctor::addPatient()管理
    void addDoctor(const Doctor& doctor)
    {
        m_doctor.push_back(doctor);
    }

public:
    Patient(std::string_view name) : m_name{ name } {}

    // 并行实现运算符重载
    friend std::ostream& operator<<(std::ostream& out, const Patient& patient);

    const std::string& getName() const { return m_name; }

    // 声明Doctor::addPatient()为友元以访问私有方法
    friend void Doctor::addPatient(Patient& patient);
};

void Doctor::addPatient(Patient& patient)
{
    m_patient.push_back(patient); // 医生添加患者
    patient.addDoctor(*this);     // 患者添加医生
}

std::ostream& operator<<(std::ostream& out, const Doctor& doctor)
{
    if (doctor.m_patient.empty())
    {
        out << doctor.m_name << " 当前无患者";
        return out;
    }

    out << doctor.m_name << " 正在接诊患者：";
    for (const auto& patient : doctor.m_patient)
        out << patient.get().getName() << ' ';

    return out;
}

std::ostream& operator<<(std::ostream& out, const Patient& patient)
{
    if (patient.m_doctor.empty())
    {
        out << patient.getName() << " 当前无接诊医生";
        return out;
    }

    out << patient.m_name << " 的接诊医生：";
    for (const auto& doctor : patient.m_doctor)
        out << doctor.get().getName() << ' ';

    return out;
}

int main()
{
    Patient dave{ "Dave" };
    Patient frank{ "Frank" };
    Patient betsy{ "Betsy" };

    Doctor james{ "James" };
    Doctor scott{ "Scott" };

    james.addPatient(dave);
    scott.addPatient(dave);
    scott.addPatient(betsy);

    std::cout << james << '\n';
    std::cout << scott << '\n';
    std::cout << dave << '\n';
    std::cout << frank << '\n';
    std::cout << betsy << '\n';

    return 0;
}
```

输出结果：  
```
James 正在接诊患者：Dave 
Scott 正在接诊患者：Dave Betsy 
Dave 的接诊医生：James Scott 
Frank 当前无接诊医生
Betsy 的接诊医生：Scott
```

通常应优先使用单向关联，双向关联会增加复杂度且更易出错。

自反关联  
----------------  

当对象与同类其他对象存在关联时，称为**自反关联（reflexive association）**。典型案例是大学课程与其先修课程（同为大学课程）的关系。

考虑简化情况：课程仅有一个先修课程：

```cpp
#include <string>
#include <string_view>

class Course // 课程
{
private:
    std::string m_name{};          // 课程名
    const Course* m_prerequisite{}; // 先修课程

public:
    Course(std::string_view name, const Course* prerequisite = nullptr)
        : m_name{ name }, m_prerequisite{ prerequisite } {}
};
```

这形成了链式关联（课程有先修课程，后者又有自己的先修课程等）。

间接关联  
----------------  

前述案例均使用指针或引用直接链接对象，但关联关系不限于此。任何能链接对象的数据形式均可。下例展示Driver（驾驶员）类通过ID与Car（汽车）建立单向关联：

```cpp
#include <iostream>
#include <string>
#include <string_view>

class Car
{
private:
    std::string m_name{}; // 车型
    int m_id{};           // 唯一标识

public:
    Car(std::string_view name, int id) : m_name{ name }, m_id{ id } {}

    const std::string& getName() const { return m_name; }
    int getId() const { return m_id; }
};

namespace CarLot // 停车场
{
    Car carLot[4]{ { "Prius", 4 }, { "Corolla", 17 }, { "Accord", 84 }, { "Matrix", 62 } };

    Car* getCar(int id)
    {
        for (auto& car : carLot)
            if (car.getId() == id)
                return &car;
        return nullptr;
    }
};

class Driver
{
private:
    std::string m_name{}; // 驾驶员姓名
    int m_carId{};        // 通过ID关联汽车

public:
    Driver(std::string_view name, int carId) : m_name{ name }, m_carId{ carId } {}

    const std::string& getName() const { return m_name; }
    int getCarId() const { return m_carId; }
};

int main()
{
    Driver d{ "Franz", 17 };         // Franz驾驶ID为17的汽车
    Car* car{ CarLot::getCar(d.getCarId()) }; // 通过ID查找汽车

    if (car)
        std::cout << d.getName() << " 驾驶 " << car->getName() << '\n';
    else
        std::cout << d.getName() << " 未找到车辆\n";

    return 0;
}
```

此例中，驾驶员通过汽车ID关联到汽车，而非直接指针。这种方式虽然查找效率较低，但具有优势：可引用非内存对象（如文件或数据库中的记录），且使用较小整数类型可节省内存空间（相比4/8字节指针）。

组合 vs 聚合 vs 关联 总结  
----------------  

下表总结三者的区别：  

| 特性          | 组合（Composition） | 聚合（Aggregation） | 关联（Association） |
|---------------|---------------------|---------------------|---------------------|
| 关系类型      | 整体/部分           | 整体/部分           | 其他无关            |
| 成员可属多类  | 否                  | 是                  | 是                  |
| 生存期管理    | 是                  | 否                  | 否                  |
| 方向性        | 单向                | 单向                | 单向/双向           |
| 关系动词      | 属于（Part-of）     | 拥有（Has-a）       | 使用（Uses-a）      |  

[下一课 23.5 — 依赖](Chapter-23/lesson23.5-dependencies.md)  
[返回主页](/)    
[上一课 23.3 — 聚合](Chapter-23/lesson23.3-aggregation.md)