import { Application } from "https://deno.land/x/oak/mod.ts";

const app = new Application();

app.use((ctx) => {
  // ctx.response.status = 404
  console.log('url=', ctx.request.url)
  let pathname = ctx.request.url.pathname
  if (pathname == '/') {
    ctx.response.body = `<html>
<body>
<h1>我的自我介紹</h1>
<ol>
<li><a href="/name">姓名</a></li>
<li><a href="/age">年齡</a></li>
<li><a href="/gender">性別</a></li>
<li><a href="/studentnumber">學號</a></li>
<li><a href="/interest">興趣</a></li>
</ol>
</body>
</html>
`
  } else if (pathname == '/name') {
    ctx.response.body = '黃信惟'
  } else if (pathname == '/age') {
    ctx.response.body = '18'
  } else if (pathname == '/gender') {
    ctx.response.body = '男'
  } else if (pathname == '/studentnumber') {
    ctx.response.body = '111310514'
  } else if (pathname == '/interest') {
    ctx.response.body = '打遊戲'
  }
  // ctx.response.body = 'Not Found!'
});

console.log('start at : http://127.0.0.1:8000')
await app.listen({ port: 8000 })