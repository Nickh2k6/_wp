function factorial(n){
    let i,ans=1;
    for (i=2;i<=n;i++){
        ans*=i;
    }
    return ans;
}
console.log(factorial(5));