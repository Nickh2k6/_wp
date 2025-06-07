from fastapi import FastAPI, Request, Response, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from typing import Optional, List
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from uuid import UUID, uuid4
import secrets
from fastapi.templating import Jinja2Templates
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware

# 資料庫設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 資料模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    title = Column(String)
    body = Column(String)

# Pydantic 模型
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class PostCreate(BaseModel):
    title: str
    body: str

# 建立資料庫表格
Base.metadata.create_all(bind=engine)

# FastAPI 應用程式
app = FastAPI()

# 加入 session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key-here",
    session_cookie="blog_session"
)

# 設定模板
templates = Jinja2Templates(directory="templates")

# 依賴項
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 檢查用戶登入狀態的輔助函數
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# 路由
@app.get("/", response_class=HTMLResponse)
async def list_posts(
    request: Request,
    db: Session = Depends(get_db)
):
    posts = db.query(Post).all()
    user = request.session.get("user")
    print(f'user={user} posts={posts}')
    r = templates.TemplateResponse(
        "list.html",
        {"request": request, "posts": posts, "user": user}
    )
    template = templates.get_template("list.html")
    rendered_text = template.render(request=request, posts=posts, user=user)
    print(f'rendered_text={rendered_text}')
    return r

@app.get("/signup", response_class=HTMLResponse)
async def signup_ui(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(username=username, password=password, email=email)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login", response_class=HTMLResponse)
async def login_ui(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    request.session["user"] = {"username": username}
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/post/new", response_class=HTMLResponse)
async def new_post(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return templates.TemplateResponse("new_post.html", {"request": request})

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def show_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user = request.session.get("user")
    # 檢查是否為文章作者，用於顯示刪除按鈕
    is_author = user and user.get("username") == post.username
    
    return templates.TemplateResponse(
        "show_post.html",
        {"request": request, "post": post, "user": user, "is_author": is_author}
    )

@app.post("/post")
async def create_post(
    request: Request,
    title: str = Form(...),
    body: str = Form(...),
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    new_post = Post(username=user["username"], title=title, body=body)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# 新增：刪除文章功能
@app.post("/post/{post_id}/delete")
async def delete_post(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    # 檢查用戶是否已登入
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # 查找要刪除的文章
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 檢查是否為文章作者（只能刪除自己的文章）
    if post.username != user["username"]:
        raise HTTPException(
            status_code=403, 
            detail="You can only delete your own posts"
        )
    
    # 刪除文章
    db.delete(post)
    db.commit()
    
    # 重導向到首頁並顯示成功訊息
    return RedirectResponse(url="/?deleted=success", status_code=status.HTTP_303_SEE_OTHER)

# 新增：確認刪除頁面
@app.get("/post/{post_id}/delete", response_class=HTMLResponse)
async def confirm_delete_post(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    # 檢查用戶是否已登入
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # 查找要刪除的文章
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 檢查是否為文章作者
    if post.username != user["username"]:
        raise HTTPException(
            status_code=403, 
            detail="You can only delete your own posts"
        )
    
    return templates.TemplateResponse(
        "confirm_delete.html",
        {"request": request, "post": post, "user": user}
    )

# 新增：我的文章列表
@app.get("/my-posts", response_class=HTMLResponse)
async def my_posts(
    request: Request,
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # 只顯示當前用戶的文章
    posts = db.query(Post).filter(Post.username == user["username"]).all()
    
    return templates.TemplateResponse(
        "my_posts.html",
        {"request": request, "posts": posts, "user": user}
    )