function uniqueSorted(arr){
    let i;
    arr.sort();
    for(i=0;i<arr.length;i++){
        if(arr[i]==arr[i+1]){
            arr.splice(i,1);
        }
    }
    return arr;
}

console.log(uniqueSorted([5, 3, 8, 3, 1, 5, 8])); 
//https://chatgpt.com/share/67dcde9d-9ffc-8006-9594-bcdc2aee50be