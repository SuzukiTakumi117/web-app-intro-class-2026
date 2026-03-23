"""
データベース初期化スクリプト
第8回: セキュリティの基礎 & 総仕上げ

このスクリプトを実行すると、todo.db を初期化し、
サンプルデータを3件挿入します。

使い方:
  python init_db.py
"""

import sqlite3

DATABASE = "todo.db"


def init_database():
    """データベースを初期化する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 既存のテーブルがあれば削除して再作成
    cursor.execute("DROP TABLE IF EXISTS todos")

    # todosテーブルを作成
    cursor.execute("""
        CREATE TABLE todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)

    # サンプルデータを挿入（パラメータバインディングを使用）
    sample_todos = [
        ("買い物に行く", 0),
        ("レポートを書く", 0),
        ("本を読む", 1),
    ]

    cursor.executemany(
        "INSERT INTO todos (title, done) VALUES (?, ?)",
        sample_todos,
    )

    conn.commit()

    # 確認用に全データを表示
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()

    print(f"データベース '{DATABASE}' を初期化しました。")
    print(f"テーブル 'todos' にサンプルデータ {len(todos)} 件を挿入しました。")
    print()
    print("--- TODO一覧 ---")
    for todo in todos:
        status = "完了" if todo[2] else "未完了"
        print(f"  ID:{todo[0]} | {todo[1]} | {status}")

    conn.close()


if __name__ == "__main__":
    init_database()
