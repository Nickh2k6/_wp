class Vector {
    constructor(components) {
        this.components = components;
    }

    // 向量加法
    add(vector) {
        if (this.components.length !== vector.components.length) {
            throw new Error("向量維度不匹配");
        }
        return new Vector(this.components.map((val, index) => val + vector.components[index]));
    }

    // 向量減法
    sub(vector) {
        if (this.components.length !== vector.components.length) {
            throw new Error("向量維度不匹配");
        }
        return new Vector(this.components.map((val, index) => val - vector.components[index]));
    }

    // 向量內積
    dot(vector) {
        if (this.components.length !== vector.components.length) {
            throw new Error("向量維度不匹配");
        }
        return this.components.reduce((sum, val, index) => sum + val * vector.components[index], 0);
    }
}

// 測試
let a = new Vector([1, 2, 3]);
let b = new Vector([4, 5, 6]);

console.log(a.add(b).sub(b).dot(b)); // 結果：32
