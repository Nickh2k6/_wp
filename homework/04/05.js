class Animal{
    constructor(name){
      this.name = name;
    }
  
    speak(){
      return "Generic animal sound";
    }
  }
  
  class Dog extends Animal{
    constructor(name){
      super(name);
    }
  
    speak(){
      return `Woof! I am ${this.name}`;
    }
  }
  
  const dog = new Dog("Buddy");
  console.log(dog.speak());