# TypeScript Handbook

# Table of Contents
1. [Introduction](#introduction)
2. [Boolean](#boolean)
3. [Number](#number)
4. [String](#string)
5. [Array](#array)
6. [Tuple](#tuple)
7. [Enum](#enum)
8. [Any](#any)
9. [Void](#void)
10. [Null and Undefined](#null-and-undefined)
11. [Never](#never)
12. [Object](#object)
13. [Type assertions](#type-assertions)
14. [A note about 'let'](#a-note-about-let)

# Introduction

For programs to be useful, we need to be able to work with some of the simplest units of data: numbers, strings, structures, boolean values, and the like.
In TypeScript, we support much the same types as you would expect in JavaScript, with a convenient enumeration type thrown in to help things along.

# Boolean

The most basic datatype is the simple true/false value, which JavaScript and TypeScript call a `boolean` value.

```ts
let isDone: boolean = false;
```

# Number

As in JavaScript, all numbers in TypeScript are floating point values.
These floating point numbers get the type `number`.
In addition to hexadecimal and decimal literals, TypeScript also supports binary and octal literals introduced in ECMAScript 2015.

```ts
let decimal: number = 6;
let hex: number = 0xf00d;
let binary: number = 0b1010;
let octal: number = 0o744;
```

# String

Another fundamental part of creating programs in JavaScript for webpages and servers alike is working with textual data.
As in other languages, we use the type `string` to refer to these textual datatypes.
Just like JavaScript, TypeScript also uses double quotes (`"`) or single quotes (`'`) to surround string data.

```ts
let color: string = "blue";
color = 'red';
```

You can also use *template strings*, which can span multiple lines and have embedded expressions.
These strings are surrounded by the backtick/backquote (`` ` ``) character, and embedded expressions are of the form `${ expr }`.

```ts
let fullName: string = `Bob Bobbington`;
let age: number = 37;
let sentence: string = `Hello, my name is ${ fullName }.

I'll be ${ age + 1 } years old next month.`;
```

This is equivalent to declaring `sentence` like so:

```ts
let sentence: string = "Hello, my name is " + fullName + ".\n\n" +
    "I'll be " + (age + 1) + " years old next month.";
```

# Array

TypeScript, like JavaScript, allows you to work with arrays of values.
Array types can be written in one of two ways.
In the first, you use the type of the elements followed by `[]` to denote an array of that element type:

```ts
let list: number[] = [1, 2, 3];
```

The second way uses a generic array type, `Array<elemType>`:

```ts
let list: Array<number> = [1, 2, 3];
```

# Tuple

Tuple types allow you to express an array with a fixed number of elements whose types are known, but need not be the same. For example, you may want to represent a value as a pair of a `string` and a `number`:

```ts
// Declare a tuple type
let x: [string, number];
// Initialize it
x = ["hello", 10]; // OK
// Initialize it incorrectly
x = [10, "hello"]; // Error
```

When accessing an element with a known index, the correct type is retrieved:

```ts
console.log(x[0].substring(1)); // OK
console.log(x[1].substring(1)); // Error, 'number' does not have 'substring'
```

Accessing an element outside the set of known indices fails with an error:

```ts
x[3] = "world"; // Error, Property '3' does not exist on type '[string, number]'.

console.log(x[5].toString()); // Error, Property '5' does not exist on type '[string, number]'.
```

# Enum

A helpful addition to the standard set of datatypes from JavaScript is the `enum`.
As in languages like C#, an enum is a way of giving more friendly names to sets of numeric values.

```ts
enum Color {Red, Green, Blue}
let c: Color = Color.Green;
```

By default, enums begin numbering their members starting at `0`.
You can change this by manually setting the value of one of its members.
For example, we can start the previous example at `1` instead of `0`:

```ts
enum Color {Red = 1, Green, Blue}
let c: Color = Color.Green;
```

Or, even manually set all the values in the enum:

```ts
enum Color {Red = 1, Green = 2, Blue = 4}
let c: Color = Color.Green;
```

A handy feature of enums is that you can also go from a numeric value to the name of that value in the enum.
For example, if we had the value `2` but weren't sure what that mapped to in the `Color` enum above, we could look up the corresponding name:

```ts
enum Color {Red = 1, Green, Blue}
let colorName: string = Color[2];

console.log(colorName); // Displays 'Green' as its value is 2 above
```

# Any

We may need to describe the type of variables that we do not know when we are writing an application.
These values may come from dynamic content, e.g. from the user or a 3rd party library.
In these cases, we want to opt-out of type checking and let the values pass through compile-time checks.
To do so, we label these with the `any` type:

```ts
let notSure: any = 4;
notSure = "maybe a string instead";
notSure = false; // okay, definitely a boolean
```

The `any` type is a powerful way to work with existing JavaScript, allowing you to gradually opt-in and opt-out of type checking during compilation.
You might expect `Object` to play a similar role, as it does in other languages.
However, variables of type `Object` only allow you to assign any value to them. You can't call arbitrary methods on them, even ones that actually exist:

```ts
let notSure: any = 4;
notSure.ifItExists(); // okay, ifItExists might exist at runtime
notSure.toFixed(); // okay, toFixed exists (but the compiler doesn't check)

let prettySure: Object = 4;
prettySure.toFixed(); // Error: Property 'toFixed' doesn't exist on type 'Object'.
```

> Note: Avoid using `Object` in favor of the non-primitive `object` type as described in our [Do's and Don'ts](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html#general-types) section.

The `any` type is also handy if you know some part of the type, but perhaps not all of it.
For example, you may have an array but the array has a mix of different types:

```ts
let list: any[] = [1, true, "free"];

list[1] = 100;
```

# Void

`void` is a little like the opposite of `any`: the absence of having any type at all.
You may commonly see this as the return type of functions that do not return a value:

```ts
function warnUser(): void {
    console.log("This is my warning message");
}
```

Declaring variables of type `void` is not useful because you can only assign `null` (only if `--strictNullChecks` is not specified, see next section) or `undefined` to them:

```ts
let unusable: void = undefined;
unusable = null; // OK if `--strictNullChecks` is not given
```

# Null and Undefined

In TypeScript, both `undefined` and `null` actually have their own types named `undefined` and `null` respectively.
Much like `void`, they're not extremely useful on their own:

```ts
// Not much else we can assign to these variables!
let u: undefined = undefined;
let n: null = null;
```

By default `null` and `undefined` are subtypes of all other types.
That means you can assign `null` and `undefined` to something like `number`.

However, when using the `--strictNullChecks` flag, `null` and `undefined` are only assignable to `any` and their respective types (the one exception being that `undefined` is also assignable to `void`).
This helps avoid *many* common errors.
In cases where you want to pass in either a `string` or `null` or `undefined`, you can use the union type `string | null | undefined`.

Union types are an advanced topic that we'll cover in a later chapter.

> As a note: we encourage the use of `--strictNullChecks` when possible, but for the purposes of this handbook, we will assume it is turned off.

# Never

The `never` type represents the type of values that never occur.
For instance, `never` is the return type for a function expression or an arrow function expression that always throws an exception or one that never returns;
Variables also acquire the type `never` when narrowed by any type guards that can never be true.

The `never` type is a subtype of, and assignable to, every type; however, *no* type is a subtype of, or assignable to, `never` (except `never` itself).
Even `any` isn't assignable to `never`.

Some examples of functions returning `never`:

```ts
// Function returning never must have unreachable end point
function error(message: string): never {
    throw new Error(message);
}

// Inferred return type is never
function fail() {
    return error("Something failed");
}

// Function returning never must have unreachable end point
function infiniteLoop(): never {
    while (true) {
    }
}
```

# Object

`object` is a type that represents the non-primitive type, i.e. anything that is not `number`, `string`, `boolean`, `bigint`, `symbol`, `null`, or `undefined`.

With `object` type, APIs like `Object.create` can be better represented. For example:

```ts
declare function create(o: object | null): void;

create({ prop: 0 }); // OK
create(null); // OK

create(42); // Error
create("string"); // Error
create(false); // Error
create(undefined); // Error
```

# Type assertions

Sometimes you'll end up in a situation where you'll know more about a value than TypeScript does.
Usually this will happen when you know the type of some entity could be more specific than its current type.

*Type assertions* are a way to tell the compiler "trust me, I know what I'm doing."
A type assertion is like a type cast in other languages, but performs no special checking or restructuring of data.
It has no runtime impact, and is used purely by the compiler.
TypeScript assumes that you, the programmer, have performed any special checks that you need.

Type assertions have two forms.
One is the "angle-bracket" syntax:

```ts
let someValue: any = "this is a string";

let strLength: number = (<string>someValue).length;
```

And the other is the `as`-syntax:

```ts
let someValue: any = "this is a string";

let strLength: number = (someValue as string).length;
```

The two samples are equivalent.
Using one over the other is mostly a choice of preference; however, when using TypeScript with JSX, only `as`-style assertions are allowed.

# A note about `let`

You may've noticed that so far, we've been using the `let` keyword instead of JavaScript's `var` keyword which you might be more familiar with.
The `let` keyword was introduced to JavaScript in ES2015 and is now considered the standard because it's safer than `var`.
We'll discuss the details later, but many common problems in JavaScript are alleviated by using `let`, so you should use it instead of `var` whenever possible.

# Introduction

One of TypeScript's core principles is that type checking focuses on the *shape* that values have.
This is sometimes called "duck typing" or "structural subtyping".
In TypeScript, interfaces fill the role of naming these types, and are a powerful way of defining contracts within your code as well as contracts with code outside of your project.

# Our First Interface

The easiest way to see how interfaces work is to start with a simple example:

```ts
function printLabel(labeledObj: { label: string }) {
    console.log(labeledObj.label);
}

let myObj = {size: 10, label: "Size 10 Object"};
printLabel(myObj);
```

The type checker checks the call to `printLabel`.
The `printLabel` function has a single parameter that requires that the object passed in has a property called `label` of type `string`.
Notice that our object actually has more properties than this, but the compiler only checks that *at least* the ones required are present and match the types required.
There are some cases where TypeScript isn't as lenient, which we'll cover in a bit.

We can write the same example again, this time using an interface to describe the requirement of having the `label` property that is a string:

```ts
interface LabeledValue {
    label: string;
}

function printLabel(labeledObj: LabeledValue) {
    console.log(labeledObj.label);
}

let myObj = {size: 10, label: "Size 10 Object"};
printLabel(myObj);
```

The interface `LabeledValue` is a name we can now use to describe the requirement in the previous example.
It still represents having a single property called `label` that is of type `string`.
Notice we didn't have to explicitly say that the object we pass to `printLabel` implements this interface like we might have to in other languages.
Here, it's only the shape that matters. If the object we pass to the function meets the requirements listed, then it's allowed.

It's worth pointing out that the type checker does not require that these properties come in any sort of order, only that the properties the interface requires are present and have the required type.

# Optional Properties

Not all properties of an interface may be required.
Some exist under certain conditions or may not be there at all.
These optional properties are popular when creating patterns like "option bags" where you pass an object to a function that only has a couple of properties filled in.

Here's an example of this pattern:

```ts
interface SquareConfig {
    color?: string;
    width?: number;
}

function createSquare(config: SquareConfig): {color: string; area: number} {
    let newSquare = {color: "white", area: 100};
    if (config.color) {
        newSquare.color = config.color;
    }
    if (config.width) {
        newSquare.area = config.width * config.width;
    }
    return newSquare;
}

let mySquare = createSquare({color: "black"});
```

Interfaces with optional properties are written similar to other interfaces, with each optional property denoted by a `?` at the end of the property name in the declaration.

The advantage of optional properties is that you can describe these possibly available properties while still also preventing use of properties that are not part of the interface.
For example, had we mistyped the name of the `color` property in `createSquare`, we would get an error message letting us know:

```ts
interface SquareConfig {
    color?: string;
    width?: number;
}

function createSquare(config: SquareConfig): { color: string; area: number } {
    let newSquare = {color: "white", area: 100};
    if (config.clor) {
        // Error: Property 'clor' does not exist on type 'SquareConfig'
        newSquare.color = config.clor;
    }
    if (config.width) {
        newSquare.area = config.width * config.width;
    }
    return newSquare;
}

let mySquare = createSquare({color: "black"});
```

# Readonly properties

Some properties should only be modifiable when an object is first created.
You can specify this by putting `readonly` before the name of the property:

```ts
interface Point {
    readonly x: number;
    readonly y: number;
}
```

You can construct a `Point` by assigning an object literal.
After the assignment, `x` and `y` can't be changed.

```ts
let p1: Point = { x: 10, y: 20 };
p1.x = 5; // error!
```

TypeScript comes with a `ReadonlyArray<T>` type that is the same as `Array<T>` with all mutating methods removed, so you can make sure you don't change your arrays after creation:

```ts
let a: number[] = [1, 2, 3, 4];
let ro: ReadonlyArray<number> = a;
ro[0] = 12; // error!
ro.push(5); // error!
ro.length = 100; // error!
a = ro; // error!
```

On the last line of the snippet you can see that even assigning the entire `ReadonlyArray` back to a normal array is illegal.
You can still override it with a type assertion, though:

```ts
a = ro as number[];
```

## `readonly` vs `const`

The easiest way to remember whether to use `readonly` or `const` is to ask whether you're using it on a variable or a property.
Variables use `const` whereas properties use `readonly`.

# Excess Property Checks

In our first example using interfaces, TypeScript lets us pass `{ size: number; label: string; }` to something that only expected a `{ label: string; }`.
We also just learned about optional properties, and how they're useful when describing so-called "option bags".

However, combining the two naively would allow an error to sneak in. For example, taking our last example using `createSquare`:

```ts
interface SquareConfig {
    color?: string;
    width?: number;
}

function createSquare(config: SquareConfig): { color: string; area: number } {
    // ...
}

let mySquare = createSquare({ colour: "red", width: 100 });
```

Notice the given argument to `createSquare` is spelled *`colour`* instead of `color`.
In plain JavaScript, this sort of thing fails silently.

You could argue that this program is correctly typed, since the `width` properties are compatible, there's no `color` property present, and the extra `colour` property is insignificant.

However, TypeScript takes the stance that there's probably a bug in this code.
Object literals get special treatment and undergo *excess property checking* when assigning them to other variables, or passing them as arguments.
If an object literal has any properties that the "target type" doesn't have, you'll get an error:

```ts
// error: Object literal may only specify known properties, but 'colour' does not exist in type 'SquareConfig'. Did you mean to write 'color'?
let mySquare = createSquare({ colour: "red", width: 100 });
```

Getting around these checks is actually really simple.
The easiest method is to just use a type assertion:

```ts
let mySquare = createSquare({ width: 100, opacity: 0.5 } as SquareConfig);
```

However, a better approach might be to add a string index signature if you're sure that the object can have some extra properties that are used in some special way.
If `SquareConfig` can have `color` and `width` properties with the above types, but could *also* have any number of other properties, then we could define it like so:

```ts
interface SquareConfig {
    color?: string;
    width?: number;
    [propName: string]: any;
}
```

We'll discuss index signatures in a bit, but here we're saying a `SquareConfig` can have any number of properties, and as long as they aren't `color` or `width`, their types don't matter.

One final way to get around these checks, which might be a bit surprising, is to assign the object to another variable:
Since `squareOptions` won't undergo excess property checks, the compiler won't give you an error.

```ts
let squareOptions = { colour: "red", width: 100 };
let mySquare = createSquare(squareOptions);
```

The above workaround will work as long as you have a common property between `squareOptions` and `SquareConfig`.
In this example, it was the property `width`. It will however, fail if the variable does not have any common object property. For example:

```ts
let squareOptions = { colour: "red" };
let mySquare = createSquare(squareOptions);
```

Keep in mind that for simple code like above, you probably shouldn't be trying to "get around" these checks.
For more complex object literals that have methods and hold state, you might need to keep these techniques in mind, but a majority of excess property errors are actually bugs.
That means if you're running into excess property checking problems for something like option bags, you might need to revise some of your type declarations.
In this instance, if it's okay to pass an object with both a `color` or `colour` property to `createSquare`, you should fix up the definition of `SquareConfig` to reflect that.

# Function Types

Interfaces are capable of describing the wide range of shapes that JavaScript objects can take.
In addition to describing an object with properties, interfaces are also capable of describing function types.

To describe a function type with an interface, we give the interface a call signature.
This is like a function declaration with only the parameter list and return type given. Each parameter in the parameter list requires both name and type.

```ts
interface SearchFunc {
    (source: string, subString: string): boolean;
}
```

Once defined, we can use this function type interface like we would other interfaces.
Here, we show how you can create a variable of a function type and assign it a function value of the same type.

```ts
let mySearch: SearchFunc;
mySearch = function(source: string, subString: string) {
    let result = source.search(subString);
    return result > -1;
}
```

For function types to correctly type check, the names of the parameters do not need to match.
We could have, for example, written the above example like this:

```ts
let mySearch: SearchFunc;
mySearch = function(src: string, sub: string): boolean {
    let result = src.search(sub);
    return result > -1;
}
```

Function parameters are checked one at a time, with the type in each corresponding parameter position checked against each other.
If you do not want to specify types at all, TypeScript's contextual typing can infer the argument types since the function value is assigned directly to a variable of type `SearchFunc`.
Here, also, the return type of our function expression is implied by the values it returns (here `false` and `true`).

```ts
let mySearch: SearchFunc;
mySearch = function(src, sub) {
    let result = src.search(sub);
    return result > -1;
}
```

Had the function expression returned numbers or strings, the type checker would have made an error that indicates return type doesn't match the return type described in the `SearchFunc` interface.

```ts
let mySearch: SearchFunc;

// error: Type '(src: string, sub: string) => string' is not assignable to type 'SearchFunc'.
// Type 'string' is not assignable to type 'boolean'.
mySearch = function(src, sub) {
  let result = src.search(sub);
  return "string";
};
```

# Indexable Types

Similarly to how we can use interfaces to describe function types, we can also describe types that we can "index into" like `a[10]`, or `ageMap["daniel"]`.
Indexable types have an *index signature* that describes the types we can use to index into the object, along with the corresponding return types when indexing.
Let's take an example:

```ts
interface StringArray {
    [index: number]: string;
}

let myArray: StringArray;
myArray = ["Bob", "Fred"];

let myStr: string = myArray[0];
```

Above, we have a `StringArray` interface that has an index signature.
This index signature states that when a `StringArray` is indexed with a `number`, it will return a `string`.

There are two types of supported index signatures: string and number.
It is possible to support both types of indexers, but the type returned from a numeric indexer must be a subtype of the type returned from the string indexer.
This is because when indexing with a `number`, JavaScript will actually convert that to a `string` before indexing into an object.
That means that indexing with `100` (a `number`) is the same thing as indexing with `"100"` (a `string`), so the two need to be consistent.

```ts
class Animal {
    name: string;
}
class Dog extends Animal {
    breed: string;
}

// Error: indexing with a numeric string might get you a completely separate type of Animal!
interface NotOkay {
    [x: number]: Animal;
    [x: string]: Dog;
}
```

While string index signatures are a powerful way to describe the "dictionary" pattern, they also enforce that all properties match their return type.
This is because a string index declares that `obj.property` is also available as `obj["property"]`.
In the following example, `name`'s type does not match the string index's type, and the type checker gives an error:

```ts
interface NumberDictionary {
    [index: string]: number;
    length: number;    // ok, length is a number
    name: string;      // error, the type of 'name' is not a subtype of the indexer
}
```

However, properties of different types are acceptable if the index signature is a union of the property types:

```ts
interface NumberOrStringDictionary {
    [index: string]: number | string;
    length: number;    // ok, length is a number
    name: string;      // ok, name is a string
}
```

Finally, you can make index signatures `readonly` in order to prevent assignment to their indices:

```ts
interface ReadonlyStringArray {
    readonly [index: number]: string;
}
let myArray: ReadonlyStringArray = ["Alice", "Bob"];
myArray[2] = "Mallory"; // error!
```

You can't set `myArray[2]` because the index signature is readonly.

# Class Types

## Implementing an interface

One of the most common uses of interfaces in languages like C# and Java, that of explicitly enforcing that a class meets a particular contract, is also possible in TypeScript.

```ts
interface ClockInterface {
    currentTime: Date;
}

class Clock implements ClockInterface {
    currentTime: Date = new Date();
    constructor(h: number, m: number) { }
}
```

You can also describe methods in an interface that are implemented in the class, as we do with `setTime` in the below example:

```ts
interface ClockInterface {
    currentTime: Date;
    setTime(d: Date): void;
}

class Clock implements ClockInterface {
    currentTime: Date = new Date();
    setTime(d: Date) {
        this.currentTime = d;
    }
    constructor(h: number, m: number) { }
}
```

Interfaces describe the public side of the class, rather than both the public and private side.
This prohibits you from using them to check that a class also has particular types for the private side of the class instance.

## Difference between the static and instance sides of classes

When working with classes and interfaces, it helps to keep in mind that a class has *two* types: the type of the static side and the type of the instance side.
You may notice that if you create an interface with a construct signature and try to create a class that implements this interface you get an error:

```ts
interface ClockConstructor {
    new (hour: number, minute: number);
}

class Clock implements ClockConstructor {
    currentTime: Date;
    constructor(h: number, m: number) { }
}
```

This is because when a class implements an interface, only the instance side of the class is checked.
Since the constructor sits in the static side, it is not included in this check.

Instead, you would need to work with the static side of the class directly.
In this example, we define two interfaces, `ClockConstructor` for the constructor and `ClockInterface` for the instance methods.
Then, for convenience, we define a constructor function `createClock` that creates instances of the type that is passed to it:

```ts
interface ClockConstructor {
    new (hour: number, minute: number): ClockInterface;
}
interface ClockInterface {
    tick(): void;
}

function createClock(ctor: ClockConstructor, hour: number, minute: number): ClockInterface {
    return new ctor(hour, minute);
}

class DigitalClock implements ClockInterface {
    constructor(h: number, m: number) { }
    tick() {
        console.log("beep beep");
    }
}
class AnalogClock implements ClockInterface {
    constructor(h: number, m: number) { }
    tick() {
        console.log("tick tock");
    }
}

let digital = createClock(DigitalClock, 12, 17);
let analog = createClock(AnalogClock, 7, 32);
```

Because `createClock`'s first parameter is of type `ClockConstructor`, in `createClock(AnalogClock, 7, 32)`, it checks that `AnalogClock` has the correct constructor signature.

Another simple way is to use class expressions:

```ts
interface ClockConstructor {
  new (hour: number, minute: number);
}

interface ClockInterface {
  tick();
}

const Clock: ClockConstructor = class Clock implements ClockInterface {
  constructor(h: number, m: number) {}
  tick() {
      console.log("beep beep");
  }
}
```


# Extending Interfaces

Like classes, interfaces can extend each other.
This allows you to copy the members of one interface into another, which gives you more flexibility in how you separate your interfaces into reusable components.

```ts
interface Shape {
    color: string;
}

interface Square extends Shape {
    sideLength: number;
}

let square = {} as Square;
square.color = "blue";
square.sideLength = 10;
```

An interface can extend multiple interfaces, creating a combination of all of the interfaces.

```ts
interface Shape {
    color: string;
}

interface PenStroke {
    penWidth: number;
}

interface Square extends Shape, PenStroke {
    sideLength: number;
}

let square = {} as Square;
square.color = "blue";
square.sideLength = 10;
square.penWidth = 5.0;
```

# Hybrid Types

As we mentioned earlier, interfaces can describe the rich types present in real world JavaScript.
Because of JavaScript's dynamic and flexible nature, you may occasionally encounter an object that works as a combination of some of the types described above.

One such example is an object that acts as both a function and an object, with additional properties:

```ts
interface Counter {
    (start: number): string;
    interval: number;
    reset(): void;
}

function getCounter(): Counter {
    let counter = (function (start: number) { }) as Counter;
    counter.interval = 123;
    counter.reset = function () { };
    return counter;
}

let c = getCounter();
c(10);
c.reset();
c.interval = 5.0;
```

When interacting with 3rd-party JavaScript, you may need to use patterns like the above to fully describe the shape of the type.

# Interfaces Extending Classes

When an interface type extends a class type it inherits the members of the class but not their implementations.
It is as if the interface had declared all of the members of the class without providing an implementation.
Interfaces inherit even the private and protected members of a base class.
This means that when you create an interface that extends a class with private or protected members, that interface type can only be implemented by that class or a subclass of it.

This is useful when you have a large inheritance hierarchy, but want to specify that your code works with only subclasses that have certain properties.
The subclasses don't have to be related besides inheriting from the base class.
For example:

```ts
class Control {
    private state: any;
}

interface SelectableControl extends Control {
    select(): void;
}

class Button extends Control implements SelectableControl {
    select() { }
}

class TextBox extends Control {
    select() { }
}

// Error: Property 'state' is missing in type 'Image'.
class Image implements SelectableControl {
    private state: any;
    select() { }
}

class Location {

}
```

In the above example, `SelectableControl` contains all of the members of `Control`, including the private `state` property.
Since `state` is a private member it is only possible for descendants of `Control` to implement `SelectableControl`.
This is because only descendants of `Control` will have a `state` private member that originates in the same declaration, which is a requirement for private members to be compatible.

Within the `Control` class it is possible to access the `state` private member through an instance of `SelectableControl`.
Effectively, a `SelectableControl` acts like a `Control` that is known to have a `select` method.
The `Button` and `TextBox` classes are subtypes of `SelectableControl` (because they both inherit from `Control` and have a `select` method), but the `Image` and `Location` classes are not.

# Introduction

Traditional JavaScript uses functions and prototype-based inheritance to build up reusable components, but this may feel a bit awkward to programmers more comfortable with an object-oriented approach, where classes inherit functionality and objects are built from these classes.
Starting with ECMAScript 2015, also known as ECMAScript 6, JavaScript programmers will be able to build their applications using this object-oriented class-based approach.
In TypeScript, we allow developers to use these techniques now, and compile them down to JavaScript that works across all major browsers and platforms, without having to wait for the next version of JavaScript.

# Classes

Let's take a look at a simple class-based example:

```ts
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
    greet() {
        return "Hello, " + this.greeting;
    }
}

let greeter = new Greeter("world");
```

The syntax should look familiar if you've used C# or Java before.
We declare a new class `Greeter`. This class has three members: a property called `greeting`, a constructor, and a method `greet`.

You'll notice that in the class when we refer to one of the members of the class we prepend `this.`.
This denotes that it's a member access.

In the last line we construct an instance of the `Greeter` class using `new`.
This calls into the constructor we defined earlier, creating a new object with the `Greeter` shape, and running the constructor to initialize it.

# Inheritance

In TypeScript, we can use common object-oriented patterns.
One of the most fundamental patterns in class-based programming is being able to extend existing classes to create new ones using inheritance.

Let's take a look at an example:

```ts
class Animal {
    move(distanceInMeters: number = 0) {
        console.log(`Animal moved ${distanceInMeters}m.`);
    }
}

class Dog extends Animal {
    bark() {
        console.log('Woof! Woof!');
    }
}

const dog = new Dog();
dog.bark();
dog.move(10);
dog.bark();
```

This example shows the most basic inheritance feature: classes inherit properties and methods from base classes.
Here, `Dog` is a *derived* class that derives from the `Animal` *base* class using the `extends` keyword.
Derived classes are often called *subclasses*, and base classes are often called *superclasses*.

Because `Dog` extends the functionality from `Animal`, we were able to create an instance of `Dog` that could both `bark()` and `move()`.

Let's now look at a more complex example.

```ts
class Animal {
    name: string;
    constructor(theName: string) { this.name = theName; }
    move(distanceInMeters: number = 0) {
        console.log(`${this.name} moved ${distanceInMeters}m.`);
    }
}

class Snake extends Animal {
    constructor(name: string) { super(name); }
    move(distanceInMeters = 5) {
        console.log("Slithering...");
        super.move(distanceInMeters);
    }
}

class Horse extends Animal {
    constructor(name: string) { super(name); }
    move(distanceInMeters = 45) {
        console.log("Galloping...");
        super.move(distanceInMeters);
    }
}

let sam = new Snake("Sammy the Python");
let tom: Animal = new Horse("Tommy the Palomino");

sam.move();
tom.move(34);
```

This example covers a few other features we didn't previously mention.
Again, we see the `extends` keywords used to create two new subclasses of `Animal`: `Horse` and `Snake`.

One difference from the prior example is that each derived class that contains a constructor function *must* call `super()` which will execute the constructor of the base class.
What's more, before we *ever* access a property on `this` in a constructor body, we *have* to call `super()`.
This is an important rule that TypeScript will enforce.

The example also shows how to override methods in the base class with methods that are specialized for the subclass.
Here both `Snake` and `Horse` create a `move` method that overrides the `move` from `Animal`, giving it functionality specific to each class.
Note that even though `tom` is declared as an `Animal`, since its value is a `Horse`, calling `tom.move(34)` will call the overriding method in `Horse`:

```Text
Slithering...
Sammy the Python moved 5m.
Galloping...
Tommy the Palomino moved 34m.
```

# Public, private, and protected modifiers

## Public by default

In our examples, we've been able to freely access the members that we declared throughout our programs.
If you're familiar with classes in other languages, you may have noticed in the above examples we haven't had to use the word `public` to accomplish this; for instance, C# requires that each member be explicitly labeled `public` to be visible.
In TypeScript, each member is `public` by default.

You may still mark a member `public` explicitly.
We could have written the `Animal` class from the previous section in the following way:

```ts
class Animal {
    public name: string;
    public constructor(theName: string) { this.name = theName; }
    public move(distanceInMeters: number) {
        console.log(`${this.name} moved ${distanceInMeters}m.`);
    }
}
```

## ECMAScript Private Fields

With TypeScript 3.8, TypeScript supports the new JavaScript syntax for private fields:

```ts
class Animal {
    #name: string;
    constructor(theName: string) { this.#name = theName; }
}

new Animal("Cat").#name; // Property '#name' is not accessible outside class 'Animal' because it has a private identifier.
```

This syntax is built into the JavaScript runtime and can have better guarantees about the isolation of each private field.
Right now, the best documentation for these private fields is in the TypeScript 3.8 [release notes](https://devblogs.microsoft.com/typescript/announcing-typescript-3-8-beta/#ecmascript-private-fields).

## Understanding TypeScript's `private`

TypeScript also has it's own way to declare a member as being marked `private`, it cannot be accessed from outside of its containing class. For example:

```ts
class Animal {
    private name: string;
    constructor(theName: string) { this.name = theName; }
}

new Animal("Cat").name; // Error: 'name' is private;
```

TypeScript is a structural type system.
When we compare two different types, regardless of where they came from, if the types of all members are compatible, then we say the types themselves are compatible.

However, when comparing types that have `private` and `protected` members, we treat these types differently.
For two types to be considered compatible, if one of them has a `private` member, then the other must have a `private` member that originated in the same declaration.
The same applies to `protected` members.

Let's look at an example to better see how this plays out in practice:

```ts
class Animal {
    private name: string;
    constructor(theName: string) { this.name = theName; }
}

class Rhino extends Animal {
    constructor() { super("Rhino"); }
}

class Employee {
    private name: string;
    constructor(theName: string) { this.name = theName; }
}

let animal = new Animal("Goat");
let rhino = new Rhino();
let employee = new Employee("Bob");

animal = rhino;
animal = employee; // Error: 'Animal' and 'Employee' are not compatible
```

In this example, we have an `Animal` and a `Rhino`, with `Rhino` being a subclass of `Animal`.
We also have a new class `Employee` that looks identical to `Animal` in terms of shape.
We create some instances of these classes and then try to assign them to each other to see what will happen.
Because `Animal` and `Rhino` share the `private` side of their shape from the same declaration of `private name: string` in `Animal`, they are compatible. However, this is not the case for `Employee`.
When we try to assign from an `Employee` to `Animal` we get an error that these types are not compatible.
Even though `Employee` also has a `private` member called `name`, it's not the one we declared in `Animal`.

## Understanding `protected`

The `protected` modifier acts much like the `private` modifier with the exception that members declared `protected` can also be accessed within deriving classes. For example,

```ts
class Person {
    protected name: string;
    constructor(name: string) { this.name = name; }
}

class Employee extends Person {
    private department: string;

    constructor(name: string, department: string) {
        super(name);
        this.department = department;
    }

    public getElevatorPitch() {
        return `Hello, my name is ${this.name} and I work in ${this.department}.`;
    }
}

let howard = new Employee("Howard", "Sales");
console.log(howard.getElevatorPitch());
console.log(howard.name); // error
```

Notice that while we can't use `name` from outside of `Person`, we can still use it from within an instance method of `Employee` because `Employee` derives from `Person`.

A constructor may also be marked `protected`.
This means that the class cannot be instantiated outside of its containing class, but can be extended. For example,

```ts
class Person {
    protected name: string;
    protected constructor(theName: string) { this.name = theName; }
}

// Employee can extend Person
class Employee extends Person {
    private department: string;

    constructor(name: string, department: string) {
        super(name);
        this.department = department;
    }

    public getElevatorPitch() {
        return `Hello, my name is ${this.name} and I work in ${this.department}.`;
    }
}

let howard = new Employee("Howard", "Sales");
let john = new Person("John"); // Error: The 'Person' constructor is protected
```

# Readonly modifier

You can make properties readonly by using the `readonly` keyword.
Readonly properties must be initialized at their declaration or in the constructor.

```ts
class Octopus {
    readonly name: string;
    readonly numberOfLegs: number = 8;
    constructor (theName: string) {
        this.name = theName;
    }
}
let dad = new Octopus("Man with the 8 strong legs");
dad.name = "Man with the 3-piece suit"; // error! name is readonly.
```

## Parameter properties

In our last example, we had to declare a readonly member `name` and a constructor parameter `theName` in the `Octopus` class. This is needed in order to have the value of `theName` accessible after the `Octopus` constructor is executed.
*Parameter properties* let you create and initialize a member in one place.
Here's a further revision of the previous `Octopus` class using a parameter property:

```ts
class Octopus {
    readonly numberOfLegs: number = 8;
    constructor(readonly name: string) {
    }
}
```

Notice how we dropped `theName` altogether and just use the shortened `readonly name: string` parameter on the constructor to create and initialize the `name` member.
We've consolidated the declarations and assignment into one location.

Parameter properties are declared by prefixing a constructor parameter with an accessibility modifier or `readonly`, or both.
Using `private` for a parameter property declares and initializes a private member; likewise, the same is done for `public`, `protected`, and `readonly`.

# Accessors

TypeScript supports getters/setters as a way of intercepting accesses to a member of an object.
This gives you a way of having finer-grained control over how a member is accessed on each object.

Let's convert a simple class to use `get` and `set`.
First, let's start with an example without getters and setters.

```ts
class Employee {
    fullName: string;
}

let employee = new Employee();
employee.fullName = "Bob Smith";
if (employee.fullName) {
    console.log(employee.fullName);
}
```

While allowing people to randomly set `fullName` directly is pretty handy, we may also want enforce some constraints when `fullName` is set.

In this version, we add a setter that checks the length of the `newName` to make sure it's compatible with the max-length of our backing database field. If it isn't we throw an error notifying client code that something went wrong.

To preserve existing functionality, we also add a simple getter that retrieves `fullName` unmodified.

```ts
const fullNameMaxLength = 10;

class Employee {
    private _fullName: string;

    get fullName(): string {
        return this._fullName;
    }

    set fullName(newName: string) {
        if (newName && newName.length > fullNameMaxLength) {
            throw new Error("fullName has a max length of " + fullNameMaxLength);
        }
        
        this._fullName = newName;
    }
}

let employee = new Employee();
employee.fullName = "Bob Smith";
if (employee.fullName) {
    console.log(employee.fullName);
}
```

To prove to ourselves that our accessor is now checking the length of values, we can attempt to assign a name longer than 10 characters and verify that we get an error.

A couple of things to note about accessors:

First, accessors require you to set the compiler to output ECMAScript 5 or higher.
Downleveling to ECMAScript 3 is not supported.
Second, accessors with a `get` and no `set` are automatically inferred to be `readonly`.
This is helpful when generating a `.d.ts` file from your code, because users of your property can see that they can't change it.

# Static Properties

Up to this point, we've only talked about the *instance* members of the class, those that show up on the object when it's instantiated.
We can also create *static* members of a class, those that are visible on the class itself rather than on the instances.
In this example, we use `static` on the origin, as it's a general value for all grids.
Each instance accesses this value through prepending the name of the class.
Similarly to prepending `this.` in front of instance accesses, here we prepend `Grid.` in front of static accesses.

```ts
class Grid {
    static origin = {x: 0, y: 0};
    calculateDistanceFromOrigin(point: {x: number; y: number;}) {
        let xDist = (point.x - Grid.origin.x);
        let yDist = (point.y - Grid.origin.y);
        return Math.sqrt(xDist * xDist + yDist * yDist) / this.scale;
    }
    constructor (public scale: number) { }
}

let grid1 = new Grid(1.0);  // 1x scale
let grid2 = new Grid(5.0);  // 5x scale

console.log(grid1.calculateDistanceFromOrigin({x: 10, y: 10}));
console.log(grid2.calculateDistanceFromOrigin({x: 10, y: 10}));
```

# Abstract Classes

Abstract classes are base classes from which other classes may be derived.
They may not be instantiated directly.
Unlike an interface, an abstract class may contain implementation details for its members.
The `abstract` keyword is used to define abstract classes as well as abstract methods within an abstract class.

```ts
abstract class Animal {
    abstract makeSound(): void;
    move(): void {
        console.log("roaming the earth...");
    }
}
```

Methods within an abstract class that are marked as abstract do not contain an implementation and must be implemented in derived classes.
Abstract methods share a similar syntax to interface methods.
Both define the signature of a method without including a method body.
However, abstract methods must include the `abstract` keyword and may optionally include access modifiers.

```ts
abstract class Department {

    constructor(public name: string) {
    }

    printName(): void {
        console.log("Department name: " + this.name);
    }

    abstract printMeeting(): void; // must be implemented in derived classes
}

class AccountingDepartment extends Department {

    constructor() {
        super("Accounting and Auditing"); // constructors in derived classes must call super()
    }

    printMeeting(): void {
        console.log("The Accounting Department meets each Monday at 10am.");
    }

    generateReports(): void {
        console.log("Generating accounting reports...");
    }
}

let department: Department; // ok to create a reference to an abstract type
department = new Department(); // error: cannot create an instance of an abstract class
department = new AccountingDepartment(); // ok to create and assign a non-abstract subclass
department.printName();
department.printMeeting();
department.generateReports(); // error: method doesn't exist on declared abstract type
```

# Advanced Techniques

## Constructor functions

When you declare a class in TypeScript, you are actually creating multiple declarations at the same time.
The first is the type of the *instance* of the class.

```ts
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
    greet() {
        return "Hello, " + this.greeting;
    }
}

let greeter: Greeter;
greeter = new Greeter("world");
console.log(greeter.greet()); // "Hello, world"
```

Here, when we say `let greeter: Greeter`, we're using `Greeter` as the type of instances of the class `Greeter`.
This is almost second nature to programmers from other object-oriented languages.

We're also creating another value that we call the *constructor function*.
This is the function that is called when we `new` up instances of the class.
To see what this looks like in practice, let's take a look at the JavaScript created by the above example:

```ts
let Greeter = (function () {
    function Greeter(message) {
        this.greeting = message;
    }
    Greeter.prototype.greet = function () {
        return "Hello, " + this.greeting;
    };
    return Greeter;
})();

let greeter;
greeter = new Greeter("world");
console.log(greeter.greet()); // "Hello, world"
```

Here, `let Greeter` is going to be assigned the constructor function.
When we call `new` and run this function, we get an instance of the class.
The constructor function also contains all of the static members of the class.
Another way to think of each class is that there is an *instance* side and a *static* side.

Let's modify the example a bit to show this difference:

```ts
class Greeter {
    static standardGreeting = "Hello, there";
    greeting: string;
    greet() {
        if (this.greeting) {
            return "Hello, " + this.greeting;
        }
        else {
            return Greeter.standardGreeting;
        }
    }
}

let greeter1: Greeter;
greeter1 = new Greeter();
console.log(greeter1.greet()); // "Hello, there"

let greeterMaker: typeof Greeter = Greeter;
greeterMaker.standardGreeting = "Hey there!";

let greeter2: Greeter = new greeterMaker();
console.log(greeter2.greet()); // "Hey there!"
```

In this example, `greeter1` works similarly to before.
We instantiate the `Greeter` class, and use this object.
This we have seen before.

Next, we then use the class directly.
Here we create a new variable called `greeterMaker`.
This variable will hold the class itself, or said another way its constructor function.
Here we use `typeof Greeter`, that is "give me the type of the `Greeter` class itself" rather than the instance type.
Or, more precisely, "give me the type of the symbol called `Greeter`," which is the type of the constructor function.
This type will contain all of the static members of Greeter along with the constructor that creates instances of the `Greeter` class.
We show this by using `new` on `greeterMaker`, creating new instances of `Greeter` and invoking them as before.

## Using a class as an interface

As we said in the previous section, a class declaration creates two things: a type representing instances of the class and a constructor function.
Because classes create types, you can use them in the same places you would be able to use interfaces.

```ts
class Point {
    x: number;
    y: number;
}

interface Point3d extends Point {
    z: number;
}

let point3d: Point3d = {x: 1, y: 2, z: 3};
```

# Introduction

Functions are the fundamental building block of any application in JavaScript.
They're how you build up layers of abstraction, mimicking classes, information hiding, and modules.
In TypeScript, while there are classes, namespaces, and modules, functions still play the key role in describing how to *do* things.
TypeScript also adds some new capabilities to the standard JavaScript functions to make them easier to work with.

# Functions

To begin, just as in JavaScript, TypeScript functions can be created both as a named function or as an anonymous function.
This allows you to choose the most appropriate approach for your application, whether you're building a list of functions in an API or a one-off function to hand off to another function.

To quickly recap what these two approaches look like in JavaScript:

```ts
// Named function
function add(x, y) {
    return x + y;
}

// Anonymous function
let myAdd = function(x, y) { return x + y; };
```

Just as in JavaScript, functions can refer to variables outside of the function body.
When they do so, they're said to *capture* these variables.
While understanding how this works (and the trade-offs when using this technique) is outside of the scope of this article, having a firm understanding how this mechanic works is an important piece of working with JavaScript and TypeScript.

```ts
let z = 100;

function addToZ(x, y) {
    return x + y + z;
}
```

# Function Types

## Typing the function

Let's add types to our simple examples from earlier:

```ts
function add(x: number, y: number): number {
    return x + y;
}

let myAdd = function(x: number, y: number): number { return x + y; };
```

We can add types to each of the parameters and then to the function itself to add a return type.
TypeScript can figure the return type out by looking at the return statements, so we can also optionally leave this off in many cases.

## Writing the function type

Now that we've typed the function, let's write the full type of the function out by looking at each piece of the function type.

```ts
let myAdd: (x: number, y: number) => number =
    function(x: number, y: number): number { return x + y; };
```

A function's type has the same two parts: the type of the arguments and the return type.
When writing out the whole function type, both parts are required.
We write out the parameter types just like a parameter list, giving each parameter a name and a type.
This name is just to help with readability.
We could have instead written:

```ts
let myAdd: (baseValue: number, increment: number) => number =
    function(x: number, y: number): number { return x + y; };
```

As long as the parameter types line up, it's considered a valid type for the function, regardless of the names you give the parameters in the function type.

The second part is the return type.
We make it clear which is the return type by using a fat arrow (`=>`) between the parameters and the return type.
As mentioned before, this is a required part of the function type, so if the function doesn't return a value, you would use `void` instead of leaving it off.

Of note, only the parameters and the return type make up the function type.
Captured variables are not reflected in the type.
In effect, captured variables are part of the "hidden state" of any function and do not make up its API.

## Inferring the types

In playing with the example, you may notice that the TypeScript compiler can figure out the type even if you only have types on one side of the equation:


```ts
// myAdd has the full function type
let myAdd = function(x: number, y: number): number { return  x + y; };

// The parameters 'x' and 'y' have the type number
let myAdd: (baseValue: number, increment: number) => number =
    function(x, y) { return x + y; };
```

This is called "contextual typing", a form of type inference.
This helps cut down on the amount of effort to keep your program typed.

# Optional and Default Parameters

In TypeScript, every parameter is assumed to be required by the function.
This doesn't mean that it can't be given `null` or `undefined`, but rather, when the function is called, the compiler will check that the user has provided a value for each parameter.
The compiler also assumes that these parameters are the only parameters that will be passed to the function.
In short, the number of arguments given to a function has to match the number of parameters the function expects.

```ts
function buildName(firstName: string, lastName: string) {
    return firstName + " " + lastName;
}

let result1 = buildName("Bob");                  // error, too few parameters
let result2 = buildName("Bob", "Adams", "Sr.");  // error, too many parameters
let result3 = buildName("Bob", "Adams");         // ah, just right
```

In JavaScript, every parameter is optional, and users may leave them off as they see fit.
When they do, their value is `undefined`.
We can get this functionality in TypeScript by adding a `?` to the end of parameters we want to be optional.
For example, let's say we want the last name parameter from above to be optional:

```ts
function buildName(firstName: string, lastName?: string) {
    if (lastName)
        return firstName + " " + lastName;
    else
        return firstName;
}

let result1 = buildName("Bob");                  // works correctly now
let result2 = buildName("Bob", "Adams", "Sr.");  // error, too many parameters
let result3 = buildName("Bob", "Adams");         // ah, just right
```

Any optional parameters must follow required parameters.
Had we wanted to make the first name optional, rather than the last name, we would need to change the order of parameters in the function, putting the first name last in the list.

In TypeScript, we can also set a value that a parameter will be assigned if the user does not provide one, or if the user passes `undefined` in its place.
These are called default-initialized parameters.
Let's take the previous example and default the last name to `"Smith"`.

```ts
function buildName(firstName: string, lastName = "Smith") {
    return firstName + " " + lastName;
}

let result1 = buildName("Bob");                  // works correctly now, returns "Bob Smith"
let result2 = buildName("Bob", undefined);       // still works, also returns "Bob Smith"
let result3 = buildName("Bob", "Adams", "Sr.");  // error, too many parameters
let result4 = buildName("Bob", "Adams");         // ah, just right
```

Default-initialized parameters that come after all required parameters are treated as optional, and just like optional parameters, can be omitted when calling their respective function.
This means optional parameters and trailing default parameters will share commonality in their types, so both

```ts
function buildName(firstName: string, lastName?: string) {
    // ...
}
```

and

```ts
function buildName(firstName: string, lastName = "Smith") {
    // ...
}
```

share the same type `(firstName: string, lastName?: string) => string`.
The default value of `lastName` disappears in the type, only leaving behind the fact that the parameter is optional.

Unlike plain optional parameters, default-initialized parameters don't *need* to occur after required parameters.
If a default-initialized parameter comes before a required parameter, users need to explicitly pass `undefined` to get the default initialized value.
For example, we could write our last example with only a default initializer on `firstName`:

```ts
function buildName(firstName = "Will", lastName: string) {
    return firstName + " " + lastName;
}

let result1 = buildName("Bob");                  // error, too few parameters
let result2 = buildName("Bob", "Adams", "Sr.");  // error, too many parameters
let result3 = buildName("Bob", "Adams");         // okay and returns "Bob Adams"
let result4 = buildName(undefined, "Adams");     // okay and returns "Will Adams"
```

# Rest Parameters

Required, optional, and default parameters all have one thing in common: they talk about one parameter at a time.
Sometimes, you want to work with multiple parameters as a group, or you may not know how many parameters a function will ultimately take.
In JavaScript, you can work with the arguments directly using the `arguments` variable that is visible inside every function body.

In TypeScript, you can gather these arguments together into a variable:

```ts
function buildName(firstName: string, ...restOfName: string[]) {
    return firstName + " " + restOfName.join(" ");
}

// employeeName will be "Joseph Samuel Lucas MacKinzie"
let employeeName = buildName("Joseph", "Samuel", "Lucas", "MacKinzie");
```

*Rest parameters* are treated as a boundless number of optional parameters.
When passing arguments for a rest parameter, you can use as many as you want; you can even pass none.
The compiler will build an array of the arguments passed in with the name given after the ellipsis (`...`), allowing you to use it in your function.

The ellipsis is also used in the type of the function with rest parameters:

```ts
function buildName(firstName: string, ...restOfName: string[]) {
    return firstName + " " + restOfName.join(" ");
}

let buildNameFun: (fname: string, ...rest: string[]) => string = buildName;
```

# `this`

Learning how to use `this` in JavaScript is something of a rite of passage.
Since TypeScript is a superset of JavaScript, TypeScript developers also need to learn how to use `this` and how to spot when it's not being used correctly.
Fortunately, TypeScript lets you catch incorrect uses of `this` with a couple of techniques.
If you need to learn how `this` works in JavaScript, though, first read Yehuda Katz's [Understanding JavaScript Function Invocation and "this"](http://yehudakatz.com/2011/08/11/understanding-javascript-function-invocation-and-this/).
Yehuda's article explains the inner workings of `this` very well, so we'll just cover the basics here.

## `this` and arrow functions

In JavaScript, `this` is a variable that's set when a function is called.
This makes it a very powerful and flexible feature, but it comes at the cost of always having to know about the context that a function is executing in.
This is notoriously confusing, especially when returning a function or passing a function as an argument.

Let's look at an example:

```ts
let deck = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    createCardPicker: function() {
        return function() {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        }
    }
}

let cardPicker = deck.createCardPicker();
let pickedCard = cardPicker();

alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```

Notice that `createCardPicker` is a function that itself returns a function.
If we tried to run the example, we would get an error instead of the expected alert box.
This is because the `this` being used in the function created by `createCardPicker` will be set to `window` instead of our `deck` object.
That's because we call `cardPicker()` on its own.
A top-level non-method syntax call like this will use `window` for `this`.
(Note: under strict mode, `this` will be `undefined` rather than `window`).

We can fix this by making sure the function is bound to the correct `this` before we return the function to be used later.
This way, regardless of how it's later used, it will still be able to see the original `deck` object.
To do this, we change the function expression to use the ECMAScript 6 arrow syntax.
Arrow functions capture the `this` where the function is created rather than where it is invoked:

```ts
let deck = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    createCardPicker: function() {
        // NOTE: the line below is now an arrow function, allowing us to capture 'this' right here
        return () => {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        }
    }
}

let cardPicker = deck.createCardPicker();
let pickedCard = cardPicker();

alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```

Even better, TypeScript will warn you when you make this mistake if you pass the `--noImplicitThis` flag to the compiler.
It will point out that `this` in `this.suits[pickedSuit]` is of type `any`.

## `this` parameters

Unfortunately, the type of `this.suits[pickedSuit]` is still `any`.
That's because `this` comes from the function expression inside the object literal.
To fix this, you can provide an explicit `this` parameter.
`this` parameters are fake parameters that come first in the parameter list of a function:

```ts
function f(this: void) {
    // make sure `this` is unusable in this standalone function
}
```

Let's add a couple of interfaces to our example above, `Card` and `Deck`, to make the types clearer and easier to reuse:

```ts
interface Card {
    suit: string;
    card: number;
}
interface Deck {
    suits: string[];
    cards: number[];
    createCardPicker(this: Deck): () => Card;
}
let deck: Deck = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    // NOTE: The function now explicitly specifies that its callee must be of type Deck
    createCardPicker: function(this: Deck) {
        return () => {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        }
    }
}

let cardPicker = deck.createCardPicker();
let pickedCard = cardPicker();

alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```

Now TypeScript knows that `createCardPicker` expects to be called on a `Deck` object.
That means that `this` is of type `Deck` now, not `any`, so `--noImplicitThis` will not cause any errors.

### `this` parameters in callbacks

You can also run into errors with `this` in callbacks, when you pass functions to a library that will later call them.
Because the library that calls your callback will call it like a normal function, `this` will be `undefined`.
With some work you can use `this` parameters to prevent errors with callbacks too.
First, the library author needs to annotate the callback type with `this`:

```ts
interface UIElement {
    addClickListener(onclick: (this: void, e: Event) => void): void;
}
```

`this: void` means that `addClickListener` expects `onclick` to be a function that does not require a `this` type.
Second, annotate your calling code with `this`:

```ts
class Handler {
    info: string;
    onClickBad(this: Handler, e: Event) {
        // oops, used `this` here. using this callback would crash at runtime
        this.info = e.message;
    }
}
let h = new Handler();
uiElement.addClickListener(h.onClickBad); // error!
```

With `this` annotated, you make it explicit that `onClickBad` must be called on an instance of `Handler`.
Then TypeScript will detect that `addClickListener` requires a function that has `this: void`.
To fix the error, change the type of `this`:

```ts
class Handler {
    info: string;
    onClickGood(this: void, e: Event) {
        // can't use `this` here because it's of type void!
        console.log('clicked!');
    }
}
let h = new Handler();
uiElement.addClickListener(h.onClickGood);
```

Because `onClickGood` specifies its `this` type as `void`, it is legal to pass to `addClickListener`.
Of course, this also means that it can't use `this.info`.
If you want both then you'll have to use an arrow function:

```ts
class Handler {
    info: string;
    onClickGood = (e: Event) => { this.info = e.message }
}
```

This works because arrow functions use the outer `this`, so you can always pass them to something that expects `this: void`.
The downside is that one arrow function is created per object of type Handler.
Methods, on the other hand, are only created once and attached to Handler's prototype.
They are shared between all objects of type Handler.

# Overloads

JavaScript is inherently a very dynamic language.
It's not uncommon for a single JavaScript function to return different types of objects based on the shape of the arguments passed in.

```ts
let suits = ["hearts", "spades", "clubs", "diamonds"];

function pickCard(x): any {
    // Check to see if we're working with an object/array
    // if so, they gave us the deck and we'll pick the card
    if (typeof x == "object") {
        let pickedCard = Math.floor(Math.random() * x.length);
        return pickedCard;
    }
    // Otherwise just let them pick the card
    else if (typeof x == "number") {
        let pickedSuit = Math.floor(x / 13);
        return { suit: suits[pickedSuit], card: x % 13 };
    }
}

let myDeck = [{ suit: "diamonds", card: 2 }, { suit: "spades", card: 10 }, { suit: "hearts", card: 4 }];
let pickedCard1 = myDeck[pickCard(myDeck)];
alert("card: " + pickedCard1.card + " of " + pickedCard1.suit);

let pickedCard2 = pickCard(15);
alert("card: " + pickedCard2.card + " of " + pickedCard2.suit);
```

Here, the `pickCard` function will return two different things based on what the user has passed in.
If the users passes in an object that represents the deck, the function will pick the card.
If the user picks the card, we tell them which card they've picked.
But how do we describe this to the type system?

The answer is to supply multiple function types for the same function as a list of overloads.
This list is what the compiler will use to resolve function calls.
Let's create a list of overloads that describe what our `pickCard` accepts and what it returns.

```ts
let suits = ["hearts", "spades", "clubs", "diamonds"];

function pickCard(x: {suit: string; card: number; }[]): number;
function pickCard(x: number): {suit: string; card: number; };
function pickCard(x): any {
    // Check to see if we're working with an object/array
    // if so, they gave us the deck and we'll pick the card
    if (typeof x == "object") {
        let pickedCard = Math.floor(Math.random() * x.length);
        return pickedCard;
    }
    // Otherwise just let them pick the card
    else if (typeof x == "number") {
        let pickedSuit = Math.floor(x / 13);
        return { suit: suits[pickedSuit], card: x % 13 };
    }
}

let myDeck = [{ suit: "diamonds", card: 2 }, { suit: "spades", card: 10 }, { suit: "hearts", card: 4 }];
let pickedCard1 = myDeck[pickCard(myDeck)];
alert("card: " + pickedCard1.card + " of " + pickedCard1.suit);

let pickedCard2 = pickCard(15);
alert("card: " + pickedCard2.card + " of " + pickedCard2.suit);
```

With this change, the overloads now give us type checked calls to the `pickCard` function.

In order for the compiler to pick the correct type check, it follows a similar process to the underlying JavaScript.
It looks at the overload list and, proceeding with the first overload, attempts to call the function with the provided parameters.
If it finds a match, it picks this overload as the correct overload.
For this reason, it's customary to order overloads from most specific to least specific.

Note that the `function pickCard(x): any` piece is not part of the overload list, so it only has two overloads: one that takes an object and one that takes a number.
Calling `pickCard` with any other parameter types would cause an error.

# Introduction

A major part of software engineering is building components that not only have well-defined and consistent APIs, but are also reusable.
Components that are capable of working on the data of today as well as the data of tomorrow will give you the most flexible capabilities for building up large software systems.

In languages like C# and Java, one of the main tools in the toolbox for creating reusable components is *generics*, that is, being able to create a component that can work over a variety of types rather than a single one.
This allows users to consume these components and use their own types.

# Hello World of Generics

To start off, let's do the "hello world" of generics: the identity function.
The identity function is a function that will return back whatever is passed in.
You can think of this in a similar way to the `echo` command.

Without generics, we would either have to give the identity function a specific type:

```ts
function identity(arg: number): number {
    return arg;
}
```

Or, we could describe the identity function using the `any` type:

```ts
function identity(arg: any): any {
    return arg;
}
```

While using `any` is certainly generic in that it will cause the function to accept any and all types for the type of `arg`, we actually are losing the information about what that type was when the function returns.
If we passed in a number, the only information we have is that any type could be returned.

Instead, we need a way of capturing the type of the argument in such a way that we can also use it to denote what is being returned.
Here, we will use a *type variable*, a special kind of variable that works on types rather than values.

```ts
function identity<T>(arg: T): T {
    return arg;
}
```

We've now added a type variable `T` to the identity function.
This `T` allows us to capture the type the user provides (e.g. `number`), so that we can use that information later.
Here, we use `T` again as the return type. On inspection, we can now see the same type is used for the argument and the return type.
This allows us to traffic that type information in one side of the function and out the other.

We say that this version of the `identity` function is generic, as it works over a range of types.
Unlike using `any`, it's also just as precise (ie, it doesn't lose any information) as the first `identity` function that used numbers for the argument and return type.

Once we've written the generic identity function, we can call it in one of two ways.
The first way is to pass all of the arguments, including the type argument, to the function:

```ts
let output = identity<string>("myString");  // type of output will be 'string'
```

Here we explicitly set `T` to be `string` as one of the arguments to the function call, denoted using the `<>` around the arguments rather than `()`.

The second way is also perhaps the most common. Here we use *type argument inference* -- that is, we want the compiler to set the value of `T` for us automatically based on the type of the argument we pass in:

```ts
let output = identity("myString");  // type of output will be 'string'
```

Notice that we didn't have to explicitly pass the type in the angle brackets (`<>`); the compiler just looked at the value `"myString"`, and set `T` to its type.
While type argument inference can be a helpful tool to keep code shorter and more readable, you may need to explicitly pass in the type arguments as we did in the previous example when the compiler fails to infer the type, as may happen in more complex examples.

# Working with Generic Type Variables

When you begin to use generics, you'll notice that when you create generic functions like `identity`, the compiler will enforce that you use any generically typed parameters in the body of the function correctly.
That is, that you actually treat these parameters as if they could be any and all types.

Let's take our `identity` function from earlier:

```ts
function identity<T>(arg: T): T {
    return arg;
}
```

What if we want to also log the length of the argument `arg` to the console with each call?
We might be tempted to write this:

```ts
function loggingIdentity<T>(arg: T): T {
    console.log(arg.length);  // Error: T doesn't have .length
    return arg;
}
```

When we do, the compiler will give us an error that we're using the `.length` member of `arg`, but nowhere have we said that `arg` has this member.
Remember, we said earlier that these type variables stand in for any and all types, so someone using this function could have passed in a `number` instead, which does not have a `.length` member.

Let's say that we've actually intended this function to work on arrays of `T` rather than `T` directly. Since we're working with arrays, the `.length` member should be available.
We can describe this just like we would create arrays of other types:

```ts
function loggingIdentity<T>(arg: T[]): T[] {
    console.log(arg.length);  // Array has a .length, so no more error
    return arg;
}
```

You can read the type of `loggingIdentity` as "the generic function `loggingIdentity` takes a type parameter `T`, and an argument `arg` which is an array of `T`s, and returns an array of `T`s."
If we passed in an array of numbers, we'd get an array of numbers back out, as `T` would bind to `number`.
This allows us to use our generic type variable `T` as part of the types we're working with, rather than the whole type, giving us greater flexibility.

We can alternatively write the sample example this way:

```ts
function loggingIdentity<T>(arg: Array<T>): Array<T> {
    console.log(arg.length);  // Array has a .length, so no more error
    return arg;
}
```

You may already be familiar with this style of type from other languages.
In the next section, we'll cover how you can create your own generic types like `Array<T>`.

# Generic Types

In previous sections, we created generic identity functions that worked over a range of types.
In this section, we'll explore the type of the functions themselves and how to create generic interfaces.

The type of generic functions is just like those of non-generic functions, with the type parameters listed first, similarly to function declarations:

```ts
function identity<T>(arg: T): T {
    return arg;
}

let myIdentity: <T>(arg: T) => T = identity;
```

We could also have used a different name for the generic type parameter in the type, so long as the number of type variables and how the type variables are used line up.

```ts
function identity<T>(arg: T): T {
    return arg;
}

let myIdentity: <U>(arg: U) => U = identity;
```

We can also write the generic type as a call signature of an object literal type:

```ts
function identity<T>(arg: T): T {
    return arg;
}

let myIdentity: {<T>(arg: T): T} = identity;
```

Which leads us to writing our first generic interface.
Let's take the object literal from the previous example and move it to an interface:

```ts
interface GenericIdentityFn {
    <T>(arg: T): T;
}

function identity<T>(arg: T): T {
    return arg;
}

let myIdentity: GenericIdentityFn = identity;
```

In a similar example, we may want to move the generic parameter to be a parameter of the whole interface.
This lets us see what type(s) we're generic over (e.g. `Dictionary<string>` rather than just `Dictionary`).
This makes the type parameter visible to all the other members of the interface.

```ts
interface GenericIdentityFn<T> {
    (arg: T): T;
}

function identity<T>(arg: T): T {
    return arg;
}

let myIdentity: GenericIdentityFn<number> = identity;
```

Notice that our example has changed to be something slightly different.
Instead of describing a generic function, we now have a non-generic function signature that is a part of a generic type.
When we use `GenericIdentityFn`, we now will also need to specify the corresponding type argument (here: `number`), effectively locking in what the underlying call signature will use.
Understanding when to put the type parameter directly on the call signature and when to put it on the interface itself will be helpful in describing what aspects of a type are generic.

In addition to generic interfaces, we can also create generic classes.
Note that it is not possible to create generic enums and namespaces.

# Generic Classes

A generic class has a similar shape to a generic interface.
Generic classes have a generic type parameter list in angle brackets (`<>`) following the name of the class.

```ts
class GenericNumber<T> {
    zeroValue: T;
    add: (x: T, y: T) => T;
}

let myGenericNumber = new GenericNumber<number>();
myGenericNumber.zeroValue = 0;
myGenericNumber.add = function(x, y) { return x + y; };
```

This is a pretty literal use of the `GenericNumber` class, but you may have noticed that nothing is restricting it to only use the `number` type.
We could have instead used `string` or even more complex objects.

```ts
let stringNumeric = new GenericNumber<string>();
stringNumeric.zeroValue = "";
stringNumeric.add = function(x, y) { return x + y; };

console.log(stringNumeric.add(stringNumeric.zeroValue, "test"));
```

Just as with interface, putting the type parameter on the class itself lets us make sure all of the properties of the class are working with the same type.

As we covered in [our section on classes](./Classes.md), a class has two sides to its type: the static side and the instance side.
Generic classes are only generic over their instance side rather than their static side, so when working with classes, static members can not use the class's type parameter.

# Generic Constraints

If you remember from an earlier example, you may sometimes want to write a generic function that works on a set of types where you have some knowledge about what capabilities that set of types will have.
In our `loggingIdentity` example, we wanted to be able to access the `.length` property of `arg`, but the compiler could not prove that every type had a `.length` property, so it warns us that we can't make this assumption.

```ts
function loggingIdentity<T>(arg: T): T {
    console.log(arg.length);  // Error: T doesn't have .length
    return arg;
}
```

Instead of working with any and all types, we'd like to constrain this function to work with any and all types that also have the `.length` property.
As long as the type has this member, we'll allow it, but it's required to have at least this member.
To do so, we must list our requirement as a constraint on what T can be.

To do so, we'll create an interface that describes our constraint.
Here, we'll create an interface that has a single `.length` property and then we'll use this interface and the `extends` keyword to denote our constraint:

```ts
interface Lengthwise {
    length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
    console.log(arg.length);  // Now we know it has a .length property, so no more error
    return arg;
}
```

Because the generic function is now constrained, it will no longer work over any and all types:

```ts
loggingIdentity(3);  // Error, number doesn't have a .length property
```

Instead, we need to pass in values whose type has all the required properties:

```ts
loggingIdentity({length: 10, value: 3});
```

## Using Type Parameters in Generic Constraints

You can declare a type parameter that is constrained by another type parameter.
For example, here we'd like to get a property from an object given its name.
We'd like to ensure that we're not accidentally grabbing a property that does not exist on the `obj`, so we'll place a constraint between the two types:

```ts
function getProperty<T, K extends keyof T>(obj: T, key: K) {
    return obj[key];
}

let x = { a: 1, b: 2, c: 3, d: 4 };

getProperty(x, "a"); // okay
getProperty(x, "m"); // error: Argument of type 'm' isn't assignable to 'a' | 'b' | 'c' | 'd'.
```

## Using Class Types in Generics

When creating factories in TypeScript using generics, it is necessary to refer to class types by their constructor functions. For example,

```ts
function create<T>(c: {new(): T; }): T {
    return new c();
}
```

A more advanced example uses the prototype property to infer and constrain relationships between the constructor function and the instance side of class types.

```ts
class BeeKeeper {
    hasMask: boolean;
}

class ZooKeeper {
    nametag: string;
}

class Animal {
    numLegs: number;
}

class Bee extends Animal {
    keeper: BeeKeeper;
}

class Lion extends Animal {
    keeper: ZooKeeper;
}

function createInstance<A extends Animal>(c: new () => A): A {
    return new c();
}

createInstance(Lion).keeper.nametag;  // typechecks!
createInstance(Bee).keeper.hasMask;   // typechecks!
```

# Enums

Enums allow us to define a set of named constants.
Using enums can make it easier to document intent, or create a set of distinct cases.
TypeScript provides both numeric and string-based enums.

## Numeric enums

We'll first start off with numeric enums, which are probably more familiar if you're coming from other languages.
An enum can be defined using the `enum` keyword.

```ts
enum Direction {
    Up = 1,
    Down,
    Left,
    Right,
}
```

Above, we have a numeric enum where `Up` is initialized with `1`.
All of the following members are auto-incremented from that point on.
In other words, `Direction.Up` has the value `1`,  `Down` has `2`, `Left` has `3`, and `Right` has `4`.

If we wanted, we could leave off the initializers entirely:

```ts
enum Direction {
    Up,
    Down,
    Left,
    Right,
}
```

Here, `Up` would have the value `0`, `Down` would have `1`, etc.
This auto-incrementing behavior is useful for cases where we might not care about the member values themselves, but do care that each value is distinct from other values in the same enum.

Using an enum is simple: just access any member as a property off of the enum itself, and declare types using the name of the enum:

```ts
enum Response {
    No = 0,
    Yes = 1,
}

function respond(recipient: string, message: Response): void {
    // ...
}

respond("Princess Caroline", Response.Yes)
```

Numeric enums can be mixed in [computed and constant members (see below)](#computed-and-constant-members).
The short story is, enums without initializers either need to be first, or have to come after numeric enums initialized with numeric constants or other constant enum members.
In other words, the following isn't allowed:

```ts
enum E {
    A = getSomeValue(),
    B, // Error! Enum member must have initializer.
}
```

## String enums

String enums are a similar concept, but have some subtle [runtime differences](#enums-at-runtime) as documented below.
In a string enum, each member has to be constant-initialized with a string literal, or with another string enum member.

```ts
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT",
}
```

While string enums don't have auto-incrementing behavior, string enums have the benefit that they "serialize" well.
In other words, if you were debugging and had to read the runtime value of a numeric enum, the value is often opaque - it doesn't convey any useful meaning on its own (though [reverse mapping](#enums-at-runtime) can often help), string enums allow you to give a meaningful and readable value when your code runs, independent of the name of the enum member itself.

## Heterogeneous enums

Technically enums can be mixed with string and numeric members, but it's not clear why you would ever want to do so:

```ts
enum BooleanLikeHeterogeneousEnum {
    No = 0,
    Yes = "YES",
}
```

Unless you're really trying to take advantage of JavaScript's runtime behavior in a clever way, it's advised that you don't do this.

## Computed and constant members

Each enum member has a value associated with it which can be either *constant* or *computed*.
An enum member is considered constant if:

* It is the first member in the enum and it has no initializer, in which case it's assigned the value `0`:

  ```ts
  // E.X is constant:
  enum E { X }
  ```

* It does not have an initializer and the preceding enum member was a *numeric* constant.
  In this case the value of the current enum member will be the value of the preceding enum member plus one.

  ```ts
  // All enum members in 'E1' and 'E2' are constant.

  enum E1 { X, Y, Z }

  enum E2 {
      A = 1, B, C
  }
  ```

* The enum member is initialized with a constant enum expression.
  A constant enum expression is a subset of TypeScript expressions that can be fully evaluated at compile time.
  An expression is a constant enum expression if it is:

    1. a literal enum expression (basically a string literal or a numeric literal)
    2. a reference to previously defined constant enum member (which can originate from a different enum)
    3. a parenthesized constant enum expression
    4. one of the `+`, `-`, `~` unary operators applied to constant enum expression
    5. `+`, `-`, `*`, `/`, `%`, `<<`, `>>`, `>>>`, `&`, `|`, `^` binary operators with constant enum expressions as operands

  It is a compile time error for constant enum expressions to be evaluated to `NaN` or `Infinity`.

In all other cases enum member is considered computed.

```ts
enum FileAccess {
    // constant members
    None,
    Read    = 1 << 1,
    Write   = 1 << 2,
    ReadWrite  = Read | Write,
    // computed member
    G = "123".length
}
```

## Union enums and enum member types

There is a special subset of constant enum members that aren't calculated: literal enum members.
A literal enum member is a constant enum member with no initialized value, or with values that are initialized to

* any string literal (e.g. `"foo"`, `"bar`, `"baz"`)
* any numeric literal (e.g. `1`, `100`)
* a unary minus applied to any numeric literal (e.g. `-1`, `-100`)

When all members in an enum have literal enum values, some special semantics come to play.

The first is that enum members also become types as well!
For example, we can say that certain members can *only* have the value of an enum member:

```ts
enum ShapeKind {
    Circle,
    Square,
}

interface Circle {
    kind: ShapeKind.Circle;
    radius: number;
}

interface Square {
    kind: ShapeKind.Square;
    sideLength: number;
}

let c: Circle = {
    kind: ShapeKind.Square, // Error! Type 'ShapeKind.Square' is not assignable to type 'ShapeKind.Circle'.
    radius: 100,
}
```

The other change is that enum types themselves effectively become a *union* of each enum member.
While we haven't discussed [union types](./Advanced%20Types.md#union-types) yet, all that you need to know is that with union enums, the type system is able to leverage the fact that it knows the exact set of values that exist in the enum itself.
Because of that, TypeScript can catch silly bugs where we might be comparing values incorrectly.
For example:

```ts
enum E {
    Foo,
    Bar,
}

function f(x: E) {
    if (x !== E.Foo || x !== E.Bar) {
        //             ~~~~~~~~~~~
        // Error! This condition will always return 'true' since the types 'E.Foo' and 'E.Bar' have no overlap.
    }
}
```

In that example, we first checked whether `x` was *not* `E.Foo`.
If that check succeeds, then our `||` will short-circuit, and the body of the 'if' will run.
However, if the check didn't succeed, then `x` can *only* be `E.Foo`, so it doesn't make sense to see whether it's equal to `E.Bar`.

## Enums at runtime

Enums are real objects that exist at runtime.
For example, the following enum

```ts
enum E {
    X, Y, Z
}
```

can actually be passed around to functions

```ts
function f(obj: { X: number }) {
    return obj.X;
}

// Works, since 'E' has a property named 'X' which is a number.
f(E);
```

## Enums at compile time

Even though Enums are real objects that exist at runtime, the `keyof` keyword works differently than you might expect for typical objects. Instead, use `keyof typeof` to get a Type that represents all Enum keys as strings.

```ts
enum LogLevel {
    ERROR, WARN, INFO, DEBUG
}

/**
 * This is equivalent to:
 * type LogLevelStrings = 'ERROR' | 'WARN' | 'INFO' | 'DEBUG';
 */
type LogLevelStrings = keyof typeof LogLevel;

function printImportant(key: LogLevelStrings, message: string) {
    const num = LogLevel[key];
    if (num <= LogLevel.WARN) {
       console.log('Log level key is: ', key);
       console.log('Log level value is: ', num);
       console.log('Log level message is: ', message);
    }
}
printImportant('ERROR', 'This is a message');
```

### Reverse mappings

In addition to creating an object with property names for members, numeric enums members also get a *reverse mapping* from enum values to enum names.
For example, in this example:

```ts
enum Enum {
    A
}
let a = Enum.A;
let nameOfA = Enum[a]; // "A"
```

TypeScript might compile this down to something like the following JavaScript:

```js
var Enum;
(function (Enum) {
    Enum[Enum["A"] = 0] = "A";
})(Enum || (Enum = {}));
var a = Enum.A;
var nameOfA = Enum[a]; // "A"
```

In this generated code, an enum is compiled into an object that stores both forward (`name` -> `value`) and reverse (`value` -> `name`) mappings.
References to other enum members are always emitted as property accesses and never inlined.

Keep in mind that string enum members *do not* get a reverse mapping generated at all.

### `const` enums

In most cases, enums are a perfectly valid solution.
However sometimes requirements are tighter.
To avoid paying the cost of extra generated code and additional indirection when accessing enum values, it's possible to use `const` enums.
Const enums are defined using the `const` modifier on our enums:

```ts
const enum Enum {
    A = 1,
    B = A * 2
}
```

Const enums can only use constant enum expressions and unlike regular enums they are completely removed during compilation.
Const enum members are inlined at use sites.
This is possible since const enums cannot have computed members.

```ts
const enum Directions {
    Up,
    Down,
    Left,
    Right
}

let directions = [Directions.Up, Directions.Down, Directions.Left, Directions.Right]
```

in generated code will become

```js
var directions = [0 /* Up */, 1 /* Down */, 2 /* Left */, 3 /* Right */];
```

## Ambient enums

Ambient enums are used to describe the shape of already existing enum types.

```ts
declare enum Enum {
    A = 1,
    B,
    C = 2
}
```

One important difference between ambient and non-ambient enums is that, in regular enums, members that don't have an initializer will be considered constant if its preceding enum member is considered constant.
In contrast, an ambient (and non-const) enum member that does not have initializer is *always* considered computed.

# Introduction

Starting with ECMAScript 2015, JavaScript has a concept of modules. TypeScript shares this concept.

Modules are executed within their own scope, not in the global scope; this means that variables, functions, classes, etc. declared in a module are not visible outside the module unless they are explicitly exported using one of the [`export` forms](#export).
Conversely, to consume a variable, function, class, interface, etc. exported from a different module, it has to be imported using one of the [`import` forms](#import).

Modules are declarative; the relationships between modules are specified in terms of imports and exports at the file level.

Modules import one another using a module loader.
At runtime the module loader is responsible for locating and executing all dependencies of a module before executing it.
Well-known module loaders used in JavaScript are Node.js's loader for [CommonJS](https://en.wikipedia.org/wiki/CommonJS) modules and the [RequireJS](http://requirejs.org/) loader for [AMD](https://github.com/amdjs/amdjs-api/blob/master/AMD.md) modules in Web applications.

In TypeScript, just as in ECMAScript 2015, any file containing a top-level `import` or `export` is considered a module.
Conversely, a file without any top-level `import` or `export` declarations is treated as a script whose contents are available in the global scope (and therefore to modules as well).

# Export

## Exporting a declaration

Any declaration (such as a variable, function, class, type alias, or interface) can be exported by adding the `export` keyword.

##### StringValidator.ts

```ts
export interface StringValidator {
    isAcceptable(s: string): boolean;
}
```

##### ZipCodeValidator.ts

```ts
import { StringValidator } from "./StringValidator";

export const numberRegexp = /^[0-9]+$/;

export class ZipCodeValidator implements StringValidator {
    isAcceptable(s: string) {
        return s.length === 5 && numberRegexp.test(s);
    }
}
```

## Export statements

Export statements are handy when exports need to be renamed for consumers, so the above example can be written as:

```ts
class ZipCodeValidator implements StringValidator {
    isAcceptable(s: string) {
        return s.length === 5 && numberRegexp.test(s);
    }
}
export { ZipCodeValidator };
export { ZipCodeValidator as mainValidator };
```

## Re-exports

Often modules extend other modules, and partially expose some of their features.
A re-export does not import it locally, or introduce a local variable.

##### ParseIntBasedZipCodeValidator.ts

```ts
export class ParseIntBasedZipCodeValidator {
    isAcceptable(s: string) {
        return s.length === 5 && parseInt(s).toString() === s;
    }
}

// Export original validator but rename it
export {ZipCodeValidator as RegExpBasedZipCodeValidator} from "./ZipCodeValidator";
```

Optionally, a module can wrap one or more modules and combine all their exports using `export * from "module"` syntax.

##### AllValidators.ts

```ts
export * from "./StringValidator"; // exports 'StringValidator' interface
export * from "./ZipCodeValidator";  // exports 'ZipCodeValidator' and const 'numberRegexp' class
export * from "./ParseIntBasedZipCodeValidator"; //  exports the 'ParseIntBasedZipCodeValidator' class
                                                 // and re-exports 'RegExpBasedZipCodeValidator' as alias
                                                 // of the 'ZipCodeValidator' class from 'ZipCodeValidator.ts'
                                                 // module.
```

# Import

Importing is just about as easy as exporting from a module.
Importing an exported declaration is done through using one of the `import` forms below:

## Import a single export from a module

```ts
import { ZipCodeValidator } from "./ZipCodeValidator";

let myValidator = new ZipCodeValidator();
```

imports can also be renamed

```ts
import { ZipCodeValidator as ZCV } from "./ZipCodeValidator";
let myValidator = new ZCV();
```

## Import the entire module into a single variable, and use it to access the module exports

```ts
import * as validator from "./ZipCodeValidator";
let myValidator = new validator.ZipCodeValidator();
```

## Import a module for side-effects only

Though not recommended practice, some modules set up some global state that can be used by other modules.
These modules may not have any exports, or the consumer is not interested in any of their exports.
To import these modules, use:

```ts
import "./my-module.js";
```

## Importing Types

Prior to TypeScript 3.8, you can import a type using `import`.
With TypeScript 3.8, you can import a type using the `import` statement, or using `import type`.

```ts
// Re-using the same import
import {APIResponseType} from "./api";

// Explicitly use import type
import type {APIResponseType} from "./api";
```

`import type` is always guaranteed to be removed from your JavaScript, and tools like Babel can make better assumptions about your code via the `isolatedModules` compiler flag. 
You can read more in the [3.8 release notes](https://devblogs.microsoft.com/typescript/announcing-typescript-3-8-beta/#type-only-imports-exports).

# Default exports

Each module can optionally export a `default` export.
Default exports are marked with the keyword `default`; and there can only be one `default` export per module.
`default` exports are imported using a different import form.

`default` exports are really handy.
For instance, a library like jQuery might have a default export of `jQuery` or `$`, which we'd probably also import under the name `$` or `jQuery`.

##### [JQuery.d.ts](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/jquery/JQuery.d.ts)

```ts
declare let $: JQuery;
export default $;
```

##### App.ts

```ts
import $ from "jquery";

$("button.continue").html( "Next Step..." );
```

Classes and function declarations can be authored directly as default exports.
Default export class and function declaration names are optional.

##### ZipCodeValidator.ts

```ts
export default class ZipCodeValidator {
    static numberRegexp = /^[0-9]+$/;
    isAcceptable(s: string) {
        return s.length === 5 && ZipCodeValidator.numberRegexp.test(s);
    }
}
```

##### Test.ts

```ts
import validator from "./ZipCodeValidator";

let myValidator = new validator();
```

or

##### StaticZipCodeValidator.ts

```ts
const numberRegexp = /^[0-9]+$/;

export default function (s: string) {
    return s.length === 5 && numberRegexp.test(s);
}
```

##### Test.ts

```ts
import validate from "./StaticZipCodeValidator";

let strings = ["Hello", "98052", "101"];

// Use function validate
strings.forEach(s => {
  console.log(`"${s}" ${validate(s) ? "matches" : "does not match"}`);
});
```

`default` exports can also be just values:

##### OneTwoThree.ts

```ts
export default "123";
```

##### Log.ts

```ts
import num from "./OneTwoThree";

console.log(num); // "123"
```

## Export all as x

With TypeScript 3.8, you can use `export * as ns` as a shorthand for re-exporting another module with a name:

```ts
export * as utilities from "./utilities";
```

This takes all of the dependencies from a module and makes it an exported field, you could import it like this:

```ts
import { utilities } from "./index";
```

# `export =` and `import = require()`

Both CommonJS and AMD generally have the concept of an `exports` object which contains all exports from a module.

They also support replacing the `exports` object with a custom single object.
Default exports are meant to act as a replacement for this behavior; however, the two are incompatible.
TypeScript supports `export =` to model the traditional CommonJS and AMD workflow.

The `export =` syntax specifies a single object that is exported from the module.
This can be a class, interface, namespace, function, or enum.

When exporting a module using `export =`, TypeScript-specific `import module = require("module")` must be used to import the module.

##### ZipCodeValidator.ts

```ts
let numberRegexp = /^[0-9]+$/;
class ZipCodeValidator {
    isAcceptable(s: string) {
        return s.length === 5 && numberRegexp.test(s);
    }
}
export = ZipCodeValidator;
```

##### Test.ts

```ts
import zip = require("./ZipCodeValidator");

// Some samples to try
let strings = ["Hello", "98052", "101"];

// Validators to use
let validator = new zip();

// Show whether each string passed each validator
strings.forEach(s => {
  console.log(`"${ s }" - ${ validator.isAcceptable(s) ? "matches" : "does not match" }`);
});
```

# Code Generation for Modules

Depending on the module target specified during compilation, the compiler will generate appropriate code for Node.js ([CommonJS](http://wiki.commonjs.org/wiki/CommonJS)), require.js ([AMD](https://github.com/amdjs/amdjs-api/wiki/AMD)), [UMD](https://github.com/umdjs/umd), [SystemJS](https://github.com/systemjs/systemjs), or [ECMAScript 2015 native modules](http://www.ecma-international.org/ecma-262/6.0/#sec-modules) (ES6) module-loading systems.
For more information on what the `define`, `require` and `register` calls in the generated code do, consult the documentation for each module loader.

This simple example shows how the names used during importing and exporting get translated into the module loading code.

##### SimpleModule.ts

```ts
import m = require("mod");
export let t = m.something + 1;
```

##### AMD / RequireJS SimpleModule.js

```js
define(["require", "exports", "./mod"], function (require, exports, mod_1) {
    exports.t = mod_1.something + 1;
});
```

##### CommonJS / Node SimpleModule.js

```js
var mod_1 = require("./mod");
exports.t = mod_1.something + 1;
```

##### UMD SimpleModule.js

```js
(function (factory) {
    if (typeof module === "object" && typeof module.exports === "object") {
        var v = factory(require, exports); if (v !== undefined) module.exports = v;
    }
    else if (typeof define === "function" && define.amd) {
        define(["require", "exports", "./mod"], factory);
    }
})(function (require, exports) {
    var mod_1 = require("./mod");
    exports.t = mod_1.something + 1;
});
```

##### System SimpleModule.js

```js
System.register(["./mod"], function(exports_1) {
    var mod_1;
    var t;
    return {
        setters:[
            function (mod_1_1) {
                mod_1 = mod_1_1;
            }],
        execute: function() {
            exports_1("t", t = mod_1.something + 1);
        }
    }
});
```

##### Native ECMAScript 2015 modules SimpleModule.js

```js
import { something } from "./mod";
export var t = something + 1;
```

# Simple Example

Below, we've consolidated the Validator implementations used in previous examples to only export a single named export from each module.

To compile, we must specify a module target on the command line. For Node.js, use `--module commonjs`;
for require.js, use `--module amd`. For example:

```Shell
tsc --module commonjs Test.ts
```

When compiled, each module will become a separate `.js` file.
As with reference tags, the compiler will follow `import` statements to compile dependent files.

##### Validation.ts

```ts
export interface StringValidator {
    isAcceptable(s: string): boolean;
}
```

##### LettersOnlyValidator.ts

```ts
import { StringValidator } from "./Validation";

const lettersRegexp = /^[A-Za-z]+$/;

export class LettersOnlyValidator implements StringValidator {
    isAcceptable(s: string) {
        return lettersRegexp.test(s);
    }
}
```

##### ZipCodeValidator.ts

```ts
import { StringValidator } from "./Validation";

const numberRegexp = /^[0-9]+$/;

export class ZipCodeValidator implements StringValidator {
    isAcceptable(s: string) {
        return s.length === 5 && numberRegexp.test(s);
    }
}
```

##### Test.ts

```ts
import { StringValidator } from "./Validation";
import { ZipCodeValidator } from "./ZipCodeValidator";
import { LettersOnlyValidator } from "./LettersOnlyValidator";

// Some samples to try
let strings = ["Hello", "98052", "101"];

// Validators to use
let validators: { [s: string]: StringValidator; } = {};
validators["ZIP code"] = new ZipCodeValidator();
validators["Letters only"] = new LettersOnlyValidator();

// Show whether each string passed each validator
strings.forEach(s => {
    for (let name in validators) {
        console.log(`"${ s }" - ${ validators[name].isAcceptable(s) ? "matches" : "does not match" } ${ name }`);
    }
});
```

# Optional Module Loading and Other Advanced Loading Scenarios

In some cases, you may want to only load a module under some conditions.
In TypeScript, we can use the pattern shown below to implement this and other advanced loading scenarios to directly invoke the module loaders without losing type safety.

The compiler detects whether each module is used in the emitted JavaScript.
If a module identifier is only ever used as part of a type annotations and never as an expression, then no `require` call is emitted for that module.
This elision of unused references is a good performance optimization, and also allows for optional loading of those modules.

The core idea of the pattern is that the `import id = require("...")` statement gives us access to the types exposed by the module.
The module loader is invoked (through `require`) dynamically, as shown in the `if` blocks below.
This leverages the reference-elision optimization so that the module is only loaded when needed.
For this pattern to work, it's important that the symbol defined via an `import` is only used in type positions (i.e. never in a position that would be emitted into the JavaScript).

To maintain type safety, we can use the `typeof` keyword.
The `typeof` keyword, when used in a type position, produces the type of a value, in this case the type of the module.

##### Dynamic Module Loading in Node.js

```ts
declare function require(moduleName: string): any;

import { ZipCodeValidator as Zip } from "./ZipCodeValidator";

if (needZipValidation) {
    let ZipCodeValidator: typeof Zip = require("./ZipCodeValidator");
    let validator = new ZipCodeValidator();
    if (validator.isAcceptable("...")) { /* ... */ }
}
```

##### Sample: Dynamic Module Loading in require.js

```ts
declare function require(moduleNames: string[], onLoad: (...args: any[]) => void): void;

import * as Zip from "./ZipCodeValidator";

if (needZipValidation) {
    require(["./ZipCodeValidator"], (ZipCodeValidator: typeof Zip) => {
        let validator = new ZipCodeValidator.ZipCodeValidator();
        if (validator.isAcceptable("...")) { /* ... */ }
    });
}
```

##### Sample: Dynamic Module Loading in System.js

```ts
declare const System: any;

import { ZipCodeValidator as Zip } from "./ZipCodeValidator";

if (needZipValidation) {
    System.import("./ZipCodeValidator").then((ZipCodeValidator: typeof Zip) => {
        var x = new ZipCodeValidator();
        if (x.isAcceptable("...")) { /* ... */ }
    });
}
```

# Working with Other JavaScript Libraries

To describe the shape of libraries not written in TypeScript, we need to declare the API that the library exposes.

We call declarations that don't define an implementation "ambient".
Typically, these are defined in `.d.ts` files.
If you're familiar with C/C++, you can think of these as `.h` files.
Let's look at a few examples.

## Ambient Modules

In Node.js, most tasks are accomplished by loading one or more modules.
We could define each module in its own `.d.ts` file with top-level export declarations, but it's more convenient to write them as one larger `.d.ts` file.
To do so, we use a construct similar to ambient namespaces, but we use the `module` keyword and the quoted name of the module which will be available to a later import.
For example:

##### node.d.ts (simplified excerpt)

```ts
declare module "url" {
    export interface Url {
        protocol?: string;
        hostname?: string;
        pathname?: string;
    }

    export function parse(urlStr: string, parseQueryString?, slashesDenoteHost?): Url;
}

declare module "path" {
    export function normalize(p: string): string;
    export function join(...paths: any[]): string;
    export var sep: string;
}
```

Now we can `/// <reference>` `node.d.ts` and then load the modules using `import url = require("url");` or `import * as URL from "url"`.

```ts
/// <reference path="node.d.ts"/>
import * as URL from "url";
let myUrl = URL.parse("http://www.typescriptlang.org");
```

### Shorthand ambient modules

If you don't want to take the time to write out declarations before using a new module, you can use a shorthand declaration to get started quickly.

##### declarations.d.ts

```ts
declare module "hot-new-module";
```

All imports from a shorthand module will have the `any` type.

```ts
import x, {y} from "hot-new-module";
x(y);
```

### Wildcard module declarations

Some module loaders such as [SystemJS](https://github.com/systemjs/systemjs/blob/master/docs/overview.md#plugin-syntax)
and [AMD](https://github.com/amdjs/amdjs-api/blob/master/LoaderPlugins.md) allow non-JavaScript content to be imported.
These typically use a prefix or suffix to indicate the special loading semantics.
Wildcard module declarations can be used to cover these cases.

```ts
declare module "*!text" {
    const content: string;
    export default content;
}
// Some do it the other way around.
declare module "json!*" {
    const value: any;
    export default value;
}
```

Now you can import things that match `"*!text"` or `"json!*"`.

```ts
import fileContent from "./xyz.txt!text";
import data from "json!http://example.com/data.json";
console.log(data, fileContent);
```

### UMD modules

Some libraries are designed to be used in many module loaders, or with no module loading (global variables).
These are known as [UMD](https://github.com/umdjs/umd) modules.
These libraries can be accessed through either an import or a global variable.
For example:

##### math-lib.d.ts

```ts
export function isPrime(x: number): boolean;
export as namespace mathLib;
```

The library can then be used as an import within modules:

```ts
import { isPrime } from "math-lib";
isPrime(2);
mathLib.isPrime(2); // ERROR: can't use the global definition from inside a module
```

It can also be used as a global variable, but only inside of a script.
(A script is a file with no imports or exports.)

```ts
mathLib.isPrime(2);
```

# Guidance for structuring modules

## Export as close to top-level as possible

Consumers of your module should have as little friction as possible when using things that you export.
Adding too many levels of nesting tends to be cumbersome, so think carefully about how you want to structure things.

Exporting a namespace from your module is an example of adding too many layers of nesting.
While namespaces sometime have their uses, they add an extra level of indirection when using modules.
This can quickly become a pain point for users, and is usually unnecessary.

Static methods on an exported class have a similar problem - the class itself adds a layer of nesting.
Unless it increases expressivity or intent in a clearly useful way, consider simply exporting a helper function.

### If you're only exporting a single `class` or `function`, use `export default`

Just as "exporting near the top-level" reduces friction on your module's consumers, so does introducing a default export.
If a module's primary purpose is to house one specific export, then you should consider exporting it as a default export.
This makes both importing and actually using the import a little easier.
For example:

#### MyClass.ts

```ts
export default class SomeType {
  constructor() { ... }
}
```

#### MyFunc.ts

```ts
export default function getThing() { return "thing"; }
```

#### Consumer.ts

```ts
import t from "./MyClass";
import f from "./MyFunc";
let x = new t();
console.log(f());
```

This is optimal for consumers. They can name your type whatever they want (`t` in this case) and don't have to do any excessive dotting to find your objects.

### If you're exporting multiple objects, put them all at top-level

#### MyThings.ts

```ts
export class SomeType { /* ... */ }
export function someFunc() { /* ... */ }
```

Conversely when importing:

### Explicitly list imported names

#### Consumer.ts

```ts
import { SomeType, someFunc } from "./MyThings";
let x = new SomeType();
let y = someFunc();
```

### Use the namespace import pattern if you're importing a large number of things

#### MyLargeModule.ts

```ts
export class Dog { ... }
export class Cat { ... }
export class Tree { ... }
export class Flower { ... }
```

#### Consumer.ts

```ts
import * as myLargeModule from "./MyLargeModule.ts";
let x = new myLargeModule.Dog();
```

## Re-export to extend

Often you will need to extend functionality on a module.
A common JS pattern is to augment the original object with *extensions*, similar to how JQuery extensions work.
As we've mentioned before, modules do not *merge* like global namespace objects would.
The recommended solution is to *not* mutate the original object, but rather export a new entity that provides the new functionality.

Consider a simple calculator implementation defined in module `Calculator.ts`.
The module also exports a helper function to test the calculator functionality by passing a list of input strings and writing the result at the end.

#### Calculator.ts

```ts
export class Calculator {
    private current = 0;
    private memory = 0;
    private operator: string;

    protected processDigit(digit: string, currentValue: number) {
        if (digit >= "0" && digit <= "9") {
            return currentValue * 10 + (digit.charCodeAt(0) - "0".charCodeAt(0));
        }
    }

    protected processOperator(operator: string) {
        if (["+", "-", "*", "/"].indexOf(operator) >= 0) {
            return operator;
        }
    }

    protected evaluateOperator(operator: string, left: number, right: number): number {
        switch (this.operator) {
            case "+": return left + right;
            case "-": return left - right;
            case "*": return left * right;
            case "/": return left / right;
        }
    }

    private evaluate() {
        if (this.operator) {
            this.memory = this.evaluateOperator(this.operator, this.memory, this.current);
        }
        else {
            this.memory = this.current;
        }
        this.current = 0;
    }

    public handleChar(char: string) {
        if (char === "=") {
            this.evaluate();
            return;
        }
        else {
            let value = this.processDigit(char, this.current);
            if (value !== undefined) {
                this.current = value;
                return;
            }
            else {
                let value = this.processOperator(char);
                if (value !== undefined) {
                    this.evaluate();
                    this.operator = value;
                    return;
                }
            }
        }
        throw new Error(`Unsupported input: '${char}'`);
    }

    public getResult() {
        return this.memory;
    }
}

export function test(c: Calculator, input: string) {
    for (let i = 0; i < input.length; i++) {
        c.handleChar(input[i]);
    }

    console.log(`result of '${input}' is '${c.getResult()}'`);
}
```

Here is a simple test for the calculator using the exposed `test` function.

#### TestCalculator.ts

```ts
import { Calculator, test } from "./Calculator";


let c = new Calculator();
test(c, "1+2*33/11="); // prints 9
```

Now to extend this to add support for input with numbers in bases other than 10, let's create `ProgrammerCalculator.ts`

#### ProgrammerCalculator.ts

```ts
import { Calculator } from "./Calculator";

class ProgrammerCalculator extends Calculator {
    static digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];

    constructor(public base: number) {
        super();
        const maxBase = ProgrammerCalculator.digits.length;
        if (base <= 0 || base > maxBase) {
            throw new Error(`base has to be within 0 to ${maxBase} inclusive.`);
        }
    }

    protected processDigit(digit: string, currentValue: number) {
        if (ProgrammerCalculator.digits.indexOf(digit) >= 0) {
            return currentValue * this.base + ProgrammerCalculator.digits.indexOf(digit);
        }
    }
}

// Export the new extended calculator as Calculator
export { ProgrammerCalculator as Calculator };

// Also, export the helper function
export { test } from "./Calculator";
```

The new module `ProgrammerCalculator` exports an API shape similar to that of the original `Calculator` module, but does not augment any objects in the original module.
Here is a test for our ProgrammerCalculator class:

#### TestProgrammerCalculator.ts

```ts
import { Calculator, test } from "./ProgrammerCalculator";

let c = new Calculator(2);
test(c, "001+010="); // prints 3
```

## Do not use namespaces in modules

When first moving to a module-based organization, a common tendency is to wrap exports in an additional layer of namespaces.
Modules have their own scope, and only exported declarations are visible from outside the module.
With this in mind, namespace provide very little, if any, value when working with modules.

On the organization front, namespaces are handy for grouping together logically-related objects and types in the global scope.
For example, in C#, you're going to find all the collection types in System.Collections.
By organizing our types into hierarchical namespaces, we provide a good "discovery" experience for users of those types.
Modules, on the other hand, are already present in a file system, necessarily.
We have to resolve them by path and filename, so there's a logical organization scheme for us to use.
We can have a /collections/generic/ folder with a list module in it.

Namespaces are important to avoid naming collisions in the global scope.
For example, you might have `My.Application.Customer.AddForm` and `My.Application.Order.AddForm` -- two types with the same name, but a different namespace.
This, however, is not an issue with modules.
Within a module, there's no plausible reason to have two objects with the same name.
From the consumption side, the consumer of any given module gets to pick the name that they will use to refer to the module, so accidental naming conflicts are impossible.

> For more discussion about modules and namespaces see [Namespaces and Modules](./Namespaces%20and%20Modules.md).

## Red Flags

All of the following are red flags for module structuring. Double-check that you're not trying to namespace your external modules if any of these apply to your files:

* A file whose only top-level declaration is `export namespace Foo { ... }` (remove `Foo` and move everything 'up' a level)
* Multiple files that have the same `export namespace Foo {` at top-level (don't think that these are going to combine into one `Foo`!)

# Introduction

With the introduction of Classes in TypeScript and ES6, there now exist certain scenarios that require additional features to support annotating or modifying classes and class members.
Decorators provide a way to add both annotations and a meta-programming syntax for class declarations and members.
Decorators are a [stage 2 proposal](https://github.com/tc39/proposal-decorators) for JavaScript and are available as an experimental feature of TypeScript.

> NOTE&emsp; Decorators are an experimental feature that may change in future releases.

To enable experimental support for decorators, you must enable the `experimentalDecorators` compiler option either on the command line or in your `tsconfig.json`:

**Command Line**:

```shell
tsc --target ES5 --experimentalDecorators
```

**tsconfig.json**:

```json
{
    "compilerOptions": {
        "target": "ES5",
        "experimentalDecorators": true
    }
}
```

# Decorators

A *Decorator* is a special kind of declaration that can be attached to a [class declaration](#class-decorators), [method](#method-decorators), [accessor](#accessor-decorators), [property](#property-decorators), or [parameter](#parameter-decorators).
Decorators use the form `@expression`, where `expression` must evaluate to a function that will be called at runtime with information about the decorated declaration.

For example, given the decorator `@sealed` we might write the `sealed` function as follows:

```ts
function sealed(target) {
    // do something with 'target' ...
}
```

> NOTE&emsp; You can see a more detailed example of a decorator in [Class Decorators](#class-decorators), below.

## Decorator Factories

If we want to customize how a decorator is applied to a declaration, we can write a decorator factory.
A *Decorator Factory* is simply a function that returns the expression that will be called by the decorator at runtime.

We can write a decorator factory in the following fashion:

```ts
function color(value: string) { // this is the decorator factory
    return function (target) { // this is the decorator
        // do something with 'target' and 'value'...
    }
}
```

> NOTE&emsp; You can see a more detailed example of a decorator factory in [Method Decorators](#method-decorators), below.

## Decorator Composition

Multiple decorators can be applied to a declaration, as in the following examples:

* On a single line:

  ```ts
  @f @g x
  ```

* On multiple lines:

  ```ts
  @f
  @g
  x
  ```

When multiple decorators apply to a single declaration, their evaluation is similar to [function composition in mathematics](http://en.wikipedia.org/wiki/Function_composition). In this model, when composing functions *f* and *g*, the resulting composite (*f* ∘ *g*)(*x*) is equivalent to *f*(*g*(*x*)).

As such, the following steps are performed when evaluating multiple decorators on a single declaration in TypeScript:

1. The expressions for each decorator are evaluated top-to-bottom.
2. The results are then called as functions from bottom-to-top.

If we were to use [decorator factories](#decorator-factories), we can observe this evaluation order with the following example:

```ts
function f() {
    console.log("f(): evaluated");
    return function (target, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log("f(): called");
    }
}

function g() {
    console.log("g(): evaluated");
    return function (target, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log("g(): called");
    }
}

class C {
    @f()
    @g()
    method() {}
}
```

Which would print this output to the console:

```shell
f(): evaluated
g(): evaluated
g(): called
f(): called
```

## Decorator Evaluation

There is a well defined order to how decorators applied to various declarations inside of a class are applied:

1. *Parameter Decorators*, followed by *Method*, *Accessor*, or *Property Decorators* are applied for each instance member.
2. *Parameter Decorators*, followed by *Method*, *Accessor*, or *Property Decorators* are applied for each static member.
3. *Parameter Decorators* are applied for the constructor.
4. *Class Decorators* are applied for the class.

## Class Decorators

A *Class Decorator* is declared just before a class declaration.
The class decorator is applied to the constructor of the class and can be used to observe, modify, or replace a class definition.
A class decorator cannot be used in a declaration file, or in any other ambient context (such as on a `declare` class).

The expression for the class decorator will be called as a function at runtime, with the constructor of the decorated class as its only argument.

If the class decorator returns a value, it will replace the class declaration with the provided constructor function.

> NOTE&nbsp; Should you choose to return a new constructor function, you must take care to maintain the original prototype.
The logic that applies decorators at runtime will **not** do this for you.

The following is an example of a class decorator (`@sealed`) applied to the `Greeter` class:

```ts
@sealed
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
    greet() {
        return "Hello, " + this.greeting;
    }
}
```

We can define the `@sealed` decorator using the following function declaration:

```ts
function sealed(constructor: Function) {
    Object.seal(constructor);
    Object.seal(constructor.prototype);
}
```

When `@sealed` is executed, it will seal both the constructor and its prototype.

Next we have an example of how to override the constructor.

```ts
function classDecorator<T extends {new(...args:any[]):{}}>(constructor:T) {
    return class extends constructor {
        newProperty = "new property";
        hello = "override";
    }
}

@classDecorator
class Greeter {
    property = "property";
    hello: string;
    constructor(m: string) {
        this.hello = m;
    }
}

console.log(new Greeter("world"));
```

## Method Decorators

A *Method Decorator* is declared just before a method declaration.
The decorator is applied to the *Property Descriptor* for the method, and can be used to observe, modify, or replace a method definition.
A method decorator cannot be used in a declaration file, on an overload, or in any other ambient context (such as in a `declare` class).

The expression for the method decorator will be called as a function at runtime, with the following three arguments:

1. Either the constructor function of the class for a static member, or the prototype of the class for an instance member.
2. The name of the member.
3. The *Property Descriptor* for the member.

> NOTE&emsp; The *Property Descriptor* will be `undefined` if your script target is less than `ES5`.

If the method decorator returns a value, it will be used as the *Property Descriptor* for the method.

> NOTE&emsp; The return value is ignored if your script target is less than `ES5`.

The following is an example of a method decorator (`@enumerable`) applied to a method on the `Greeter` class:

```ts
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }

    @enumerable(false)
    greet() {
        return "Hello, " + this.greeting;
    }
}
```

We can define the `@enumerable` decorator using the following function declaration:

```ts
function enumerable(value: boolean) {
    return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        descriptor.enumerable = value;
    };
}
```

The `@enumerable(false)` decorator here is a [decorator factory](#decorator-factories).
When the `@enumerable(false)` decorator is called, it modifies the `enumerable` property of the property descriptor.

## Accessor Decorators

An *Accessor Decorator* is declared just before an accessor declaration.
The accessor decorator is applied to the *Property Descriptor* for the accessor and can be used to observe, modify, or replace an accessor's definitions.
An accessor decorator cannot be used in a declaration file, or in any other ambient context (such as in a `declare` class).

> NOTE&emsp; TypeScript disallows decorating both the `get` and `set` accessor for a single member.
Instead, all decorators for the member must be applied to the first accessor specified in document order.
This is because decorators apply to a *Property Descriptor*, which combines both the `get` and `set` accessor, not each declaration separately.

The expression for the accessor decorator will be called as a function at runtime, with the following three arguments:

1. Either the constructor function of the class for a static member, or the prototype of the class for an instance member.
2. The name of the member.
3. The *Property Descriptor* for the member.

> NOTE&emsp; The *Property Descriptor* will be `undefined` if your script target is less than `ES5`.

If the accessor decorator returns a value, it will be used as the *Property Descriptor* for the member.

> NOTE&emsp; The return value is ignored if your script target is less than `ES5`.

The following is an example of an accessor decorator (`@configurable`) applied to a member of the `Point` class:

```ts
class Point {
    private _x: number;
    private _y: number;
    constructor(x: number, y: number) {
        this._x = x;
        this._y = y;
    }

    @configurable(false)
    get x() { return this._x; }

    @configurable(false)
    get y() { return this._y; }
}
```

We can define the `@configurable` decorator using the following function declaration:

```ts
function configurable(value: boolean) {
    return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        descriptor.configurable = value;
    };
}
```

## Property Decorators

A *Property Decorator* is declared just before a property declaration.
A property decorator cannot be used in a declaration file, or in any other ambient context (such as in a `declare` class).

The expression for the property decorator will be called as a function at runtime, with the following two arguments:

1. Either the constructor function of the class for a static member, or the prototype of the class for an instance member.
2. The name of the member.

> NOTE&emsp; A *Property Descriptor* is not provided as an argument to a property decorator due to how property decorators are initialized in TypeScript.
This is because there is currently no mechanism to describe an instance property when defining members of a prototype, and no way to observe or modify the initializer for a property. The return value is ignored too.
As such, a property decorator can only be used to observe that a property of a specific name has been declared for a class.

We can use this information to record metadata about the property, as in the following example:

```ts
class Greeter {
    @format("Hello, %s")
    greeting: string;

    constructor(message: string) {
        this.greeting = message;
    }
    greet() {
        let formatString = getFormat(this, "greeting");
        return formatString.replace("%s", this.greeting);
    }
}
```

We can then define the `@format` decorator and `getFormat` functions using the following function declarations:

```ts
import "reflect-metadata";

const formatMetadataKey = Symbol("format");

function format(formatString: string) {
    return Reflect.metadata(formatMetadataKey, formatString);
}

function getFormat(target: any, propertyKey: string) {
    return Reflect.getMetadata(formatMetadataKey, target, propertyKey);
}
```

The `@format("Hello, %s")` decorator here is a [decorator factory](#decorator-factories).
When `@format("Hello, %s")` is called, it adds a metadata entry for the property using the `Reflect.metadata` function from the `reflect-metadata` library.
When `getFormat` is called, it reads the metadata value for the format.

> NOTE&emsp; This example requires the `reflect-metadata` library.
See [Metadata](#metadata) for more information about the `reflect-metadata` library.

## Parameter Decorators

A *Parameter Decorator* is declared just before a parameter declaration.
The parameter decorator is applied to the function for a class constructor or method declaration.
A parameter decorator cannot be used in a declaration file, an overload, or in any other ambient context (such as in a `declare` class).

The expression for the parameter decorator will be called as a function at runtime, with the following three arguments:

1. Either the constructor function of the class for a static member, or the prototype of the class for an instance member.
2. The name of the member.
3. The ordinal index of the parameter in the function's parameter list.

> NOTE&emsp; A parameter decorator can only be used to observe that a parameter has been declared on a method.

The return value of the parameter decorator is ignored.

The following is an example of a parameter decorator (`@required`) applied to parameter of a member of the `Greeter` class:

```ts
class Greeter {
    greeting: string;

    constructor(message: string) {
        this.greeting = message;
    }

    @validate
    greet(@required name: string) {
        return "Hello " + name + ", " + this.greeting;
    }
}
```

We can then define the `@required` and `@validate` decorators using the following function declarations:

```ts
import "reflect-metadata";

const requiredMetadataKey = Symbol("required");

function required(target: Object, propertyKey: string | symbol, parameterIndex: number) {
    let existingRequiredParameters: number[] = Reflect.getOwnMetadata(requiredMetadataKey, target, propertyKey) || [];
    existingRequiredParameters.push(parameterIndex);
    Reflect.defineMetadata(requiredMetadataKey, existingRequiredParameters, target, propertyKey);
}

function validate(target: any, propertyName: string, descriptor: TypedPropertyDescriptor<Function>) {
    let method = descriptor.value;
    descriptor.value = function () {
        let requiredParameters: number[] = Reflect.getOwnMetadata(requiredMetadataKey, target, propertyName);
        if (requiredParameters) {
            for (let parameterIndex of requiredParameters) {
                if (parameterIndex >= arguments.length || arguments[parameterIndex] === undefined) {
                    throw new Error("Missing required argument.");
                }
            }
        }

        return method.apply(this, arguments);
    }
}
```

The `@required` decorator adds a metadata entry that marks the parameter as required.
The `@validate` decorator then wraps the existing `greet` method in a function that validates the arguments before invoking the original method.

> NOTE&emsp; This example requires the `reflect-metadata` library.
See [Metadata](#metadata) for more information about the `reflect-metadata` library.

## Metadata

Some examples use the `reflect-metadata` library which adds a polyfill for an [experimental metadata API](https://github.com/rbuckton/ReflectDecorators).
This library is not yet part of the ECMAScript (JavaScript) standard.
However, once decorators are officially adopted as part of the ECMAScript standard these extensions will be proposed for adoption.

You can install this library via npm:

```shell
npm i reflect-metadata --save
```

TypeScript includes experimental support for emitting certain types of metadata for declarations that have decorators.
To enable this experimental support, you must set the `emitDecoratorMetadata` compiler option either on the command line or in your `tsconfig.json`:

**Command Line**:

```shell
tsc --target ES5 --experimentalDecorators --emitDecoratorMetadata
```

**tsconfig.json**:

```json
{
    "compilerOptions": {
        "target": "ES5",
        "experimentalDecorators": true,
        "emitDecoratorMetadata": true
    }
}
```

When enabled, as long as the `reflect-metadata` library has been imported, additional design-time type information will be exposed at runtime.

We can see this in action in the following example:

```ts
import "reflect-metadata";

class Point {
    x: number;
    y: number;
}

class Line {
    private _p0: Point;
    private _p1: Point;

    @validate
    set p0(value: Point) { this._p0 = value; }
    get p0() { return this._p0; }

    @validate
    set p1(value: Point) { this._p1 = value; }
    get p1() { return this._p1; }
}

function validate<T>(target: any, propertyKey: string, descriptor: TypedPropertyDescriptor<T>) {
    let set = descriptor.set;
    descriptor.set = function (value: T) {
        let type = Reflect.getMetadata("design:type", target, propertyKey);
        if (!(value instanceof type)) {
            throw new TypeError("Invalid type.");
        }
        set.call(target, value);
    }
}
```

The TypeScript compiler will inject design-time type information using the `@Reflect.metadata` decorator.
You could consider it the equivalent of the following TypeScript:

```ts
class Line {
    private _p0: Point;
    private _p1: Point;

    @validate
    @Reflect.metadata("design:type", Point)
    set p0(value: Point) { this._p0 = value; }
    get p0() { return this._p0; }

    @validate
    @Reflect.metadata("design:type", Point)
    set p1(value: Point) { this._p1 = value; }
    get p1() { return this._p1; }
}

```

> NOTE&emsp; Decorator metadata is an experimental feature and may introduce breaking changes in future releases.

This quick start guide will teach you how to wire up TypeScript with [React](https://reactjs.org/).
By the end, you'll have

* a project with React and TypeScript
* linting with [TSLint](https://github.com/palantir/tslint)
* testing with [Jest](https://facebook.github.io/jest/) and [Enzyme](http://airbnb.io/enzyme/), and
* state management with [Redux](https://github.com/reactjs/react-redux)

We'll use the [create-react-app](https://github.com/facebookincubator/create-react-app) tool to quickly get set up.

We assume that you're already using [Node.js](https://nodejs.org/) with [npm](https://www.npmjs.com/).
You may also want to get a sense of [the basics with React](https://reactjs.org/docs/hello-world.html).

# Install create-react-app

We're going to use the create-react-app because it sets some useful tools and canonical defaults for React projects.
This is just a command-line utility to scaffold out new React projects.

```shell
npm install -g create-react-app
```

# Create our new project

We'll create a new project called `my-app`:

```shell
create-react-app my-app --scripts-version=react-scripts-ts
```

[react-scripts-ts](https://www.npmjs.com/package/react-scripts-ts) is a set of adjustments to take the standard create-react-app project pipeline and bring TypeScript into the mix.

At this point, your project layout should look like the following:

```text
my-app/
├─ .gitignore
├─ node_modules/
├─ public/
├─ src/
│  └─ ...
├─ package.json
├─ tsconfig.json
└─ tslint.json
```

Of note:

* `tsconfig.json` contains TypeScript-specific options for our project.
* `tslint.json` stores the settings that our linter, [TSLint](https://github.com/palantir/tslint), will use.
* `package.json` contains our dependencies, as well as some shortcuts for commands we'd like to run for testing, previewing, and deploying our app.
* `public` contains static assets like the HTML page we're planning to deploy to, or images. You can delete any file in this folder apart from `index.html`.
* `src` contains our TypeScript and CSS code. `index.tsx` is the entry-point for our file, and is mandatory.

# Running the project

Running the project is as simple as running

```sh
npm run start
```

This runs the `start` script specified in our `package.json`, and will spawn off a server which reloads the page as we save our files.
Typically the server runs at `http://localhost:3000`, but should be automatically opened for you.

This tightens the iteration loop by allowing us to quickly preview changes.

# Testing the project

Testing is also just a command away:

```sh
npm run test
```

This command runs Jest, an incredibly useful testing utility, against all files whose extensions end in `.test.ts` or `.spec.ts`.
Like with the `npm run start` command, Jest will automatically run as soon as it detects changes.
If you'd like, you can run `npm run start` and `npm run test` side by side so that you can preview changes and test them simultaneously.

# Creating a production build

When running the project with `npm run start`, we didn't end up with an optimized build.
Typically, we want the code we ship to users to be as fast and small as possible.
Certain optimizations like minification can accomplish this, but often take more time.
We call builds like this "production" builds (as opposed to development builds).

To run a production build, just run

```sh
npm run build
```

This will create an optimized JS and CSS build in `./build/static/js` and `./build/static/css` respectively.

You won't need to run a production build most of the time,
but it is useful if you need to measure things like the final size of your app.

# Creating a component

We're going to write a `Hello` component.
The component will take the name of whatever we want to greet (which we'll call `name`), and optionally the number of exclamation marks to trail with (`enthusiasmLevel`).

When we write something like `<Hello name="Daniel" enthusiasmLevel={3} />`, the component should render to something like `<div>Hello Daniel!!!</div>`.
If `enthusiasmLevel` isn't specified, the component should default to showing one exclamation mark.
If `enthusiasmLevel` is `0` or negative, it should throw an error.

We'll write a `Hello.tsx`:

```ts
// src/components/Hello.tsx

import * as React from 'react';

export interface Props {
  name: string;
  enthusiasmLevel?: number;
}

function Hello({ name, enthusiasmLevel = 1 }: Props) {
  if (enthusiasmLevel <= 0) {
    throw new Error('You could be a little more enthusiastic. :D');
  }

  return (
    <div className="hello">
      <div className="greeting">
        Hello {name + getExclamationMarks(enthusiasmLevel)}
      </div>
    </div>
  );
}

export default Hello;

// helpers

function getExclamationMarks(numChars: number) {
  return Array(numChars + 1).join('!');
}
```

Notice that we defined a type named `Props` that specifies the properties our component will take.
`name` is a required `string`, and `enthusiasmLevel` is an optional `number` (which you can tell from the `?` that we wrote out after its name).

We also wrote `Hello` as a function component.
To be specific, `Hello` is a function that takes a `Props` object, and destructures it.
If `enthusiasmLevel` isn't given in our `Props` object, it will default to `1`.

Writing functions is one of two primary [ways React allows us to make components]((https://reactjs.org/docs/components-and-props.html#functional-and-class-components)).
If we wanted, we *could* have written it out as a class as follows:

```ts
class Hello extends React.Component<Props, object> {
  render() {
    const { name, enthusiasmLevel = 1 } = this.props;

    if (enthusiasmLevel <= 0) {
      throw new Error('You could be a little more enthusiastic. :D');
    }

    return (
      <div className="hello">
        <div className="greeting">
          Hello {name + getExclamationMarks(enthusiasmLevel)}
        </div>
      </div>
    );
  }
}
```

Classes are useful [when our component instances have some state](https://reactjs.org/docs/state-and-lifecycle.html).
But we don't really need to think about state in this example - in fact, we specified it as `object` in `React.Component<Props, object>`, so writing a function component tends to be shorter.
Local component state is more useful at the presentational level when creating generic UI elements that can be shared between libraries.
For our application's lifecycle, we will revisit how applications manage general state with Redux in a bit.

Now that we've written our component, let's dive into `index.tsx` and replace our render of `<App />` with a render of `<Hello ... />`.

First we'll import it at the top of the file:

```ts
import Hello from './components/Hello';
```

and then change up our `render` call:

```ts
ReactDOM.render(
  <Hello name="TypeScript" enthusiasmLevel={10} />,
  document.getElementById('root') as HTMLElement
);
```

## Type assertions

One final thing we'll point out in this section is the line `document.getElementById('root') as HTMLElement`.
This syntax is called a *type assertion*, sometimes also called a *cast*.
This is a useful way of telling TypeScript what the real type of an expression is when you know better than the type checker.

The reason we need to do so in this case is that `getElementById`'s return type is `HTMLElement | null`.
Put simply, `getElementById` returns `null` when it can't find an element with a given `id`.
We're assuming that `getElementById` will actually succeed, so we need convince TypeScript of that using the `as` syntax.

TypeScript also has a trailing "bang" syntax (`!`), which removes `null` and `undefined` from the prior expression.
So we *could* have written `document.getElementById('root')!`, but in this case we wanted to be a bit more explicit.

# Adding style 😎

Styling a component with our setup is easy.
To style our `Hello` component, we can create a CSS file at `src/components/Hello.css`.

```css
.hello {
  text-align: center;
  margin: 20px;
  font-size: 48px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
}

.hello button {
    margin-left: 25px;
    margin-right: 25px;
    font-size: 40px;
    min-width: 50px;
}
```

The tools that create-react-app uses (namely, Webpack and various loaders) allow us to just import the stylesheets we're interested in.
When our build runs, any imported `.css` files will be concatenated into an output file.
So in `src/components/Hello.tsx`, we'll add the following import.

```ts
import './Hello.css';
```

# Writing tests with Jest

We had a certain set of assumptions about our `Hello` component.
Let's reiterate what they were:

> * When we write something like `<Hello name="Daniel" enthusiasmLevel={3} />`, the component should render to something like `<div>Hello Daniel!!!</div>`.
> * If `enthusiasmLevel` isn't specified, the component should default to showing one exclamation mark.
> * If `enthusiasmLevel` is `0` or negative, it should throw an error.

We can use these requirements to write a few tests for our components.

But first, let's install Enzyme.
[Enzyme](http://airbnb.io/enzyme/) is a common tool in the React ecosystem that makes it easier to write tests for how components will behave.
By default, our application includes a library called jsdom to allow us to simulate the DOM and test its runtime behavior without a browser.
Enzyme is similar, but builds on jsdom and makes it easier to make certain queries about our components.

Let's install it as a development-time dependency.

```sh
npm install -D enzyme @types/enzyme enzyme-adapter-react-16 @types/enzyme-adapter-react-16 react-addons-test-utils 
```

Notice we installed packages `enzyme` as well as `@types/enzyme`.
The `enzyme` package refers to the package containing JavaScript code that actually gets run, while `@types/enzyme` is a package that contains declaration files (`.d.ts` files) so that TypeScript can understand how you can use Enzyme.
You can learn more about `@types` packages [here](https://www.typescriptlang.org/docs/handbook/declaration-files/consumption.html).

We had to install `react-addons-test-utils`.
This is something `enzyme` expects to be installed.

We also had to make sure `esModuleInterop` is set to `true` in the `tsconfig.json`

Now that we've got Enzyme set up, let's start writing our test!
Let's create a file named `src/components/Hello.test.tsx`, adjacent to our `Hello.tsx` file from earlier.

```ts
// src/components/Hello.test.tsx

import * as React from 'react';
import * as enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import Hello from './Hello';

Enzyme.configure({ adapter: new Adapter() });

it('renders the correct text when no enthusiasm level is given', () => {
  const hello = enzyme.shallow(<Hello name='Daniel' />);
  expect(hello.find(".greeting").text()).toEqual('Hello Daniel!')
});

it('renders the correct text with an explicit enthusiasm of 1', () => {
  const hello = enzyme.shallow(<Hello name='Daniel' enthusiasmLevel={1}/>);
  expect(hello.find(".greeting").text()).toEqual('Hello Daniel!')
});

it('renders the correct text with an explicit enthusiasm level of 5', () => {
  const hello = enzyme.shallow(<Hello name='Daniel' enthusiasmLevel={5} />);
  expect(hello.find(".greeting").text()).toEqual('Hello Daniel!!!!!');
});

it('throws when the enthusiasm level is 0', () => {
  expect(() => {
    enzyme.shallow(<Hello name='Daniel' enthusiasmLevel={0} />);
  }).toThrow();
});

it('throws when the enthusiasm level is negative', () => {
  expect(() => {
    enzyme.shallow(<Hello name='Daniel' enthusiasmLevel={-1} />);
  }).toThrow();
});
```

These tests are extremely basic, but you should be able to get the gist of things.

# Adding state management

At this point, if all you're using React for is fetching data once and displaying it, you can consider yourself done.
But if you're developing an app that's more interactive, then you may need to add state management.

## State management in general

On its own, React is a useful library for creating composable views.
However, React doesn't come with any facility for synchronizing data between your application.
As far as a React component is concerned, data flows down through its children through the props you specify on each element.

Because React on its own does not provide built-in support for state management, the React community uses libraries like Redux and MobX.

[Redux](http://redux.js.org) relies on synchronizing data through a centralized and immutable store of data, and updates to that data will trigger a re-render of our application.
State is updated in an immutable fashion by sending explicit action messages which must be handled by functions called reducers.
Because of the explicit nature, it is often easier to reason about how an action will affect the state of your program.

[MobX](https://mobx.js.org/) relies on functional reactive patterns where state is wrapped through observables and passed through as props.
Keeping state fully synchronized for any observers is done by simply marking state as observable.
As a nice bonus, the library is already written in TypeScript.

There are various merits and tradeoffs to both.
Generally Redux tends to see more widespread usage, so for the purposes of this tutorial, we'll focus on adding Redux;
however, you should feel encouraged to explore both.

The following section may have a steep learning curve.
We strongly suggest you [familiarize yourself with Redux through its documentation](http://redux.js.org/).

## Setting the stage for actions

It doesn't make sense to add Redux unless the state of our application changes.
We need a source of actions that will trigger changes to take place.
This can be a timer, or something in the UI like a button.

For our purposes, we're going to add two buttons to control the enthusiasm level for our `Hello` component.

## Installing Redux

To add Redux, we'll first install `redux` and `react-redux`, as well as their types, as a dependency.

```sh
npm install -S redux react-redux @types/react-redux
```

In this case we didn't need to install `@types/redux` because Redux already comes with its own definition files (`.d.ts` files).

## Defining our app's state

We need to define the shape of the state which Redux will store.
For this, we can create a file called `src/types/index.tsx` which will contain definitions for types that we might use throughout the program.

```ts
// src/types/index.tsx

export interface StoreState {
    languageName: string;
    enthusiasmLevel: number;
}
```

Our intention is that `languageName` will be the programming language this app was written in (i.e. TypeScript or JavaScript) and `enthusiasmLevel` will vary.
When we write our first container, we'll understand why we intentionally made our state slightly different from our props.

## Adding actions

Let's start off by creating a set of message types that our app can respond to in `src/constants/index.tsx`.

```ts
// src/constants/index.tsx

export const INCREMENT_ENTHUSIASM = 'INCREMENT_ENTHUSIASM';
export type INCREMENT_ENTHUSIASM = typeof INCREMENT_ENTHUSIASM;


export const DECREMENT_ENTHUSIASM = 'DECREMENT_ENTHUSIASM';
export type DECREMENT_ENTHUSIASM = typeof DECREMENT_ENTHUSIASM;
```

This `const`/`type` pattern allows us to use TypeScript's string literal types in an easily accessible and refactorable way.

Next, we'll create a set of actions and functions that can create these actions in `src/actions/index.tsx`.

```ts
import * as constants from '../constants'

export interface IncrementEnthusiasm {
    type: constants.INCREMENT_ENTHUSIASM;
}

export interface DecrementEnthusiasm {
    type: constants.DECREMENT_ENTHUSIASM;
}

export type EnthusiasmAction = IncrementEnthusiasm | DecrementEnthusiasm;

export function incrementEnthusiasm(): IncrementEnthusiasm {
    return {
        type: constants.INCREMENT_ENTHUSIASM
    }
}

export function decrementEnthusiasm(): DecrementEnthusiasm {
    return {
        type: constants.DECREMENT_ENTHUSIASM
    }
}
```

We've created two types that describe what increment actions and decrement actions should look like.
We also created a type (`EnthusiasmAction`) to describe cases where an action could be an increment or a decrement.
Finally, we made two functions that actually manufacture the actions which we can use instead of writing out bulky object literals.

There's clearly boilerplate here, so you should feel free to look into libraries like [redux-actions](https://www.npmjs.com/package/redux-actions) once you've got the hang of things.

## Adding a reducer

We're ready to write our first reducer!
Reducers are just functions that generate changes by creating modified copies of our application's state, but that have *no side effects*.
In other words, they're what we call *[pure functions](https://en.wikipedia.org/wiki/Pure_function)*.

Our reducer will go under `src/reducers/index.tsx`.
Its function will be to ensure that increments raise the enthusiasm level by 1, and that decrements reduce the enthusiasm level by 1, but that the level never falls below 1.

```ts
// src/reducers/index.tsx

import { EnthusiasmAction } from '../actions';
import { StoreState } from '../types/index';
import { INCREMENT_ENTHUSIASM, DECREMENT_ENTHUSIASM } from '../constants/index';

export function enthusiasm(state: StoreState, action: EnthusiasmAction): StoreState {
  switch (action.type) {
    case INCREMENT_ENTHUSIASM:
      return { ...state, enthusiasmLevel: state.enthusiasmLevel + 1 };
    case DECREMENT_ENTHUSIASM:
      return { ...state, enthusiasmLevel: Math.max(1, state.enthusiasmLevel - 1) };
  }
  return state;
}
```

Notice that we're using the *object spread* (`...state`) which allows us to create a shallow copy of our state, while replacing the `enthusiasmLevel`.
It's important that the `enthusiasmLevel` property come last, since otherwise it would be overridden by the property in our old state.

You may want to write a few tests for your reducer.
Since reducers are pure functions, they can be passed arbitrary data.
For every input, reducers can tested by checking their newly produced state.
Consider looking into Jest's [toEqual](https://facebook.github.io/jest/docs/en/expect.html#toequalvalue) method to accomplish this.

## Making a container

When writing with Redux, we will often write components as well as containers.
Components are often data-agnostic, and work mostly at a presentational level.
*Containers* typically wrap components and feed them any data that is necessary to display and modify state.
You can read more about this concept on [Dan Abramov's article *Presentational and Container Components*](https://medium.com/@dan_abramov/smart-and-dumb-components-7ca2f9a7c7d0).

First let's update `src/components/Hello.tsx` so that it can modify state.
We'll add two optional callback properties to `Props` named `onIncrement` and `onDecrement`:

```ts
export interface Props {
  name: string;
  enthusiasmLevel?: number;
  onIncrement?: () => void;
  onDecrement?: () => void;
}
```

Then we'll bind those callbacks to two new buttons that we'll add into our component.

```ts
function Hello({ name, enthusiasmLevel = 1, onIncrement, onDecrement }: Props) {
  if (enthusiasmLevel <= 0) {
    throw new Error('You could be a little more enthusiastic. :D');
  }

  return (
    <div className="hello">
      <div className="greeting">
        Hello {name + getExclamationMarks(enthusiasmLevel)}
      </div>
      <div>
        <button onClick={onDecrement}>-</button>
        <button onClick={onIncrement}>+</button>
      </div>
    </div>
  );
}
```

In general, it'd be a good idea to write a few tests for `onIncrement` and `onDecrement` being triggered when their respective buttons are clicked.
Give it a shot to get the hang of writing tests for your components.

Now that our component is updated, we're ready to wrap it into a container.
Let's create a file named `src/containers/Hello.tsx` and start off with the following imports.

```ts
import Hello from '../components/Hello';
import * as actions from '../actions/';
import { StoreState } from '../types/index';
import { connect, Dispatch } from 'react-redux';
```

The real two key pieces here are the original `Hello` component as well as the `connect` function from react-redux.
`connect` will be able to actually take our original `Hello` component and turn it into a container using two functions:

* `mapStateToProps` which massages the data from the current store to part of the shape that our component needs.
* `mapDispatchToProps` which uses creates callback props to pump actions to our store using a given `dispatch` function.

If we recall, our application state consists of two properties: `languageName` and `enthusiasmLevel`.
Our `Hello` component, on the other hand, expected a `name` and an `enthusiasmLevel`.
`mapStateToProps` will get the relevant data from the store, and adjust it if necessary, for our component's props.
Let's go ahead and write that.

```ts
export function mapStateToProps({ enthusiasmLevel, languageName }: StoreState) {
  return {
    enthusiasmLevel,
    name: languageName,
  }
}
```

Note that `mapStateToProps` only creates 2 out of 4 of the properties a `Hello` component expects.
Namely, we still want to pass in the `onIncrement` and `onDecrement` callbacks.
`mapDispatchToProps` is a function that takes a dispatcher function.
This dispatcher function can pass actions into our store to make updates, so we can create a pair of callbacks that will call the dispatcher as necessary.

```ts
export function mapDispatchToProps(dispatch: Dispatch<actions.EnthusiasmAction>) {
  return {
    onIncrement: () => dispatch(actions.incrementEnthusiasm()),
    onDecrement: () => dispatch(actions.decrementEnthusiasm()),
  }
}
```

Finally, we're ready to call `connect`.
`connect` will first take `mapStateToProps` and `mapDispatchToProps`, and then return another function that we can use to wrap our component.
Our resulting container is defined with the following line of code:

```ts
export default connect(mapStateToProps, mapDispatchToProps)(Hello);
```

When we're finished, our file should look like this:

```ts
// src/containers/Hello.tsx

import Hello from '../components/Hello';
import * as actions from '../actions/';
import { StoreState } from '../types/index';
import { connect, Dispatch } from 'react-redux';

export function mapStateToProps({ enthusiasmLevel, languageName }: StoreState) {
  return {
    enthusiasmLevel,
    name: languageName,
  }
}

export function mapDispatchToProps(dispatch: Dispatch<actions.EnthusiasmAction>) {
  return {
    onIncrement: () => dispatch(actions.incrementEnthusiasm()),
    onDecrement: () => dispatch(actions.decrementEnthusiasm()),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Hello);
```

## Creating a store

Let's go back to `src/index.tsx`.
To put this all together, we need to create a store with an initial state, and set it up with all of our reducers.

```ts
import { createStore } from 'redux';
import { enthusiasm } from './reducers/index';
import { StoreState } from './types/index';

const store = createStore<StoreState>(enthusiasm, {
  enthusiasmLevel: 1,
  languageName: 'TypeScript',
});
```

`store` is, as you might've guessed, our central store for our application's global state.

Next, we're going to swap our use of `./src/components/Hello` with `./src/containers/Hello` and use react-redux's `Provider` to wire up our props with our container.
We'll import each:

```ts
import Hello from './containers/Hello';
import { Provider } from 'react-redux';
```

and pass our `store` through to the `Provider`'s attributes:

```ts
ReactDOM.render(
  <Provider store={store}>
    <Hello />
  </Provider>,
  document.getElementById('root') as HTMLElement
);
```

Notice that `Hello` no longer needs props, since we used our `connect` function to adapt our application's state for our wrapped `Hello` component's props.

# Ejecting

If at any point, you feel like there are certain customizations that the create-react-app setup has made difficult, you can always opt-out and get the various configuration options you need.
For example, if you'd like to add a Webpack plugin, it might be necessary to take advantage of the "eject" functionality that create-react-app provides.

Simply run

```sh
npm run eject
```

and you should be good to go!

As a heads up, you may want to commit all your work before running an eject.
You cannot undo an eject command, so opting out is permanent unless you can recover from a commit prior to running an eject.

# Next steps

create-react-app comes with a lot of great stuff.
Much of it is documented in the default `README.md` that was generated for our project, so give that a quick read.

If you still want to learn more about Redux, you can [check out the official website](http://redux.js.org/) for documentation.
The same goes [for MobX](https://mobx.js.org/).

If you want to eject at some point, you may need to know a little bit more about Webpack.
You can check out our [React & Webpack walkthrough here](./React%20&%20Webpack.md).

At some point you might need routing.
There are several solutions, but [react-router](https://github.com/ReactTraining/react-router) is probably the most popular for Redux projects, and is often used in conjunction with [react-router-redux](https://github.com/reactjs/react-router-redux).

