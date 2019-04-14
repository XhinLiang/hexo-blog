title: JavaScript 面向对象编程
date: 2017-5-25
tags: [JavaScript,Node.js]
categories: 前端
toc: true
---
# JavaScript 面向对象编程

### 构造函数

#### 构造函数的特点
1. 内部对`this`对象进行了赋值
2. 调用的时候需要在前面添加`new`关键字
3. 一般没有返回值

忘记使用`new`关键字，`this`会指向别的对象。

#### `new`命令的原理
1. 创建一个空对象，作为将要返回的对象实例
2. 将这个空对象的原型，指向构造函数的prototype属性
3. 将这个空对象赋值给函数内部的this关键字
4. 开始执行构造函数内部的代码

### Object 对象
Object 对象是一个基础的对象，类似与 Java 的 Object 对象。
- `Object.getOwnPropertyNames()`返回一个数组，成员是对象本身的所有属性的键名，不包含继承的属性键名。
- `Object.prototype.hasOwnProperty()`返回一个布尔值，用于判断某个属性定义在对象自身，还是定义在原型链上。
- `in` 运算符常用于检查一个属性是否存在
``` javascript
'length' in Date // true
'toString' in Date // true
```
- `for...in` 循环获得对象的所有可枚举属性
``` javascript
for (p in o2) {
  console.info(p);
}
```

### 构造函数的继承
1. 在子类的构造函数中，调用父类的构造函数。
``` javascript
function Sub(value) {
  Super.call(this);
  this.prop = value;
}
```

2. 让子类的原型指向父类的原型
``` javascript
Sub.prototype = Object.create(Super.prototype);
Sub.prototype.constructor = Sub;
```

### 多重继承
``` javascript
function Sub(value) {
  Super1.call(this);
  Super2.call(this);
  this.prop = value;
}
```

### 模块化
``` javascript
var module1 = (function () {
　var _count = 0;
　var m1 = function () {
　  //...
　};
　var m2 = function () {
　　//...
　};
　return {
　　m1 : m1,
　　m2 : m2
　};
})();
console.info(module1._count); //undefined
```

### 原型链简介
大部分面向对象的编程语言，都是以“类”（class）作为对象体系的语法基础。JavaScript 语言不是如此，它的面向对象编程基于“原型对象”。

JavaScript的每个对象都继承另一个对象，后者称为“原型”（`prototype`）对象。只有`null`除外，它没有自己的原型对象。

原型对象上的所有属性和方法，都能被派生对象共享。这就是JavaScript继承机制的基本设计。

通过构造函数生成实例对象时，会自动为实例对象分配原型对象。每一个构造函数都有一个prototype属性，这个属性就是实例对象的原型对象。

```
function Animal (name) {
  this.name = name;
}

Animal.prototype.color = 'white';

var cat1 = new Animal('大毛');
var cat2 = new Animal('二毛');

cat1.color // 'white'
cat2.color // 'white'
```

原型对象的属性不是实例对象自身的属性。只要修改原型对象，变动就立刻会体现在所有实例对象上。

```
Animal.prototype.color = 'yellow';

cat1.color // "yellow"
cat2.color // "yellow"
```

如果实例对象自身就有某个属性或方法，它就不会再去原型对象寻找这个属性或方法。

```
cat1.color = 'black';

cat2.color // 'yellow'
Animal.prototype.color // "yellow";
```

原型对象的作用，就是定义所有实例对象共享的属性和方法。这也是它被称为原型对象的含义，而实例对象可以视作从原型对象衍生出来的子对象。

#### constructor属性
`prototype`对象有一个`constructor`属性，默认指向`prototype`对象所在的构造函数。

``` javascript
function P() {}

P.prototype.constructor === P
// true
```

#### 修改原型链对象的两种写法
```
// 较好的写法
C.prototype = {
  constructor: C,
  method1: function (...) { ... },
  // ...
};

// 好的写法
C.prototype.method1 = function (...) { ... };
```

#### Object.getPrototypeOf()
获取对象的 `Prototype` 对象。

#### Object.setPrototypeOf()
设置对象的 `Prototype` 对象。





