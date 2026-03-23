// =====================================================
// TODO App JavaScript - 実習用スターター
// 第7回: フロントエンドとバックエンドの結合
//
// 第4回の正解をベースに、fetch API でサーバーと通信します。
// GET は実装済み。POST / PUT / DELETE を実装してください。
// =====================================================

// -----------------------------------------------------
// TODO一覧を取得して画面に表示する（GET）— 実装済み
// -----------------------------------------------------
async function loadTodos() {
  try {
    const response = await fetch("/todos");
    const todos = await response.json();
    renderTodos(todos);
  } catch (error) {
    console.error("TODO取得エラー:", error);
  }
}

// -----------------------------------------------------
// 新しいTODOを追加する（POST）— 実装済み
// -----------------------------------------------------
async function addTodo() {
  const input = document.getElementById("todo-input");
  const title = input.value.trim();
  if (!title) return;

  try {
    await fetch("/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title }),
    });

    input.value = "";
    await loadTodos();
  } catch (error) {
    console.error("TODO追加エラー:", error);
  }
}

// -----------------------------------------------------
// TODOの完了状態を切り替える（PUT）
// -----------------------------------------------------
async function toggleTodo(id, currentDone) {
  try {
    // ヒント: PUTリクエストを送信
    //   await fetch(`/todos/${id}`, {
    //     method: "PUT",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify({ done: !currentDone }),
    //   });

    await loadTodos();
  } catch (error) {
    console.error("TODO更新エラー:", error);
  }
}

// -----------------------------------------------------
// TODOを削除する（DELETE）
// -----------------------------------------------------
async function deleteTodo(id) {
  try {
    // ヒント: DELETEリクエストを送信
    //   await fetch(`/todos/${id}`, {
    //     method: "DELETE",
    //   });

    await loadTodos();
  } catch (error) {
    console.error("TODO削除エラー:", error);
  }
}

// -----------------------------------------------------
// TODO一覧をDOMに描画する — 実装済み
// -----------------------------------------------------
function renderTodos(todos) {
  const todoList = document.getElementById("todo-list");
  todoList.innerHTML = "";

  todos.forEach(function (todo) {
    const li = document.createElement("li");
    li.className = "todo-item" + (todo.done ? " done" : "");

    // チェックボックス
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "todo-checkbox";
    checkbox.checked = todo.done;
    checkbox.addEventListener("change", function () {
      toggleTodo(todo.id, todo.done);
    });

    // TODOタイトル（textContentを使用 — XSS対策）
    const titleSpan = document.createElement("span");
    titleSpan.className = "todo-title";
    titleSpan.textContent = todo.title;

    // 削除ボタン
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-button";
    deleteBtn.textContent = "削除";
    deleteBtn.addEventListener("click", function () {
      deleteTodo(todo.id);
    });

    li.appendChild(checkbox);
    li.appendChild(titleSpan);
    li.appendChild(deleteBtn);
    todoList.appendChild(li);
  });

}

// -----------------------------------------------------
// イベントリスナー
// -----------------------------------------------------
document.getElementById("add-button").addEventListener("click", addTodo);

document.getElementById("todo-input").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    addTodo();
  }
});

// ページ読み込み時にTODO一覧を取得
loadTodos();
