class Animal(object):
    def __init__(self, name):
        self.name = name if name is not None else "animal"

    def run(self):
        print(f"{self.name} is running ...")


class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

    def run(self):
        super().run()
        print(f"My age is :{self.age}")

    def method1(self):
        return "Hello", "python", "OOP"


if __name__ == "__main__":
    dog1 = Dog("wangcai_1", 1)
    dog1.run()
    h, p, o = dog1.method1()
    print(f"{h} {p}, {o}!")
