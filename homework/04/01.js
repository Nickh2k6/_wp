function countLetters(str){
    const letterCount = new Map();

    for (const char of str){
        if (letterCount.has(char)){
            letterCount.set(char,letterCount.get(char) + 1);
        } 
        else{
            letterCount.set(char, 1);
        }
    }

    return letterCount;
}

console.log(countLetters("banana"));