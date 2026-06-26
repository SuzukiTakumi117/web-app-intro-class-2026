import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- データ通信用のモデル定義 ---
class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    done: bool

app = FastAPI(title="TODO API")

# CORS設定（フロントとバックエンドの通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "todo.db"

# 1. 一覧取得 (GET)
@app.get("/todos")
def get_todos():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM todos ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]

# 2. 新規追加 (POST)
@app.post("/todos")
def create_todo(todo: TodoCreate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, done) VALUES (?, 0)", (todo.title,))
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    return {"id": todo_id, "title": todo.title, "done": False}

# 3. 完了状態の更新 (PUT)
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT title FROM todos WHERE id = ?", (todo_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="TODO not found")
        
    cursor.execute("UPDATE todos SET done = ? WHERE id = ?", (int(todo.done), todo_id))
    conn.commit()
    conn.close()
    return {"id": todo_id, "title": existing[0], "done": todo.done}

# 4. 削除 (DELETE)
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="TODO not found")
        
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return {"message": "TODO deleted", "id": todo_id}

# 5. 静的ファイル（HTMLなど）の配信設定
# ※すべての通信を受け取るため、必ず最後に記述します
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)