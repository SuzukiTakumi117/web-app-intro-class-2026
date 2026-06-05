"""
第5回 実習3: Pythonスクリプトの作成

スライドの手順に従って、このファイルを編集してください。
  1. TODOリスト（辞書のリスト）を定義する
  2. show_todos 関数を実装する
  3. show_todos(todos) を呼び出す

実行方法:
  python basics.py

期待される出力例:
  [ ] 1: 課題を出す
  [x] 2: 買い物する
  [ ] 3: 自分のTODO
"""

# 1. TODOリスト（辞書のリスト）を定義する
todos = [
    {"id": 1, "title": "課題を出す", "done": False},
    {"id": 2, "title": "買い物する", "done": True},
    {"id": 3, "title": "自分のTODO", "done": False},
]


# 2. show_todos 関数を実装する
def show_todos(todo_list):
    for todo in todo_list:
        # doneがTrueなら"[x]"、Falseなら"[ ]"を代入する（三項演算子）
        status = "[x]" if todo["done"] else "[ ]"
        # f文字列（f-string）を使って指定のフォーマットで出力
        print(f'{status} {todo["id"]}: {todo["title"]}')


# 3. show_todos(todos) を呼び出す
show_todos(todos)