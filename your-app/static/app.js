async function loadData() {
    const res = await fetch('/api/data');
    const data = await res.json();
    
    document.getElementById('budget-input').value = data.budget;
    
    const list = document.getElementById('expense-list');
    list.innerHTML = '';
    let total = 0;
    
    data.items.forEach(item => {
        total += item.amount;
        const li = document.createElement('li');
        li.innerHTML = `${item.title} : ${item.amount}円 <button onclick="deleteExpense(${item.id})">削除</button>`;
        list.appendChild(li);
    });
    
    document.getElementById('total-amount').innerText = total;
    const remaining = data.budget - total;
    const remainingEl = document.getElementById('remaining-amount');
    remainingEl.innerText = remaining;
    
    if (remaining < 0) {
        remainingEl.classList.add('over');
    } else {
        remainingEl.classList.remove('over');
    }
}

document.getElementById('budget-input').addEventListener('change', async (e) => {
    await fetch('/api/budget', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ budget: parseInt(e.target.value) || 0 })
    });
    loadData();
});

async function addExpense() {
    const title = document.getElementById('title-input').value;
    const amount = parseInt(document.getElementById('amount-input').value);
    if (!title || !amount) return;
    
    await fetch('/api/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, amount })
    });
    
    document.getElementById('title-input').value = '';
    document.getElementById('amount-input').value = '';
    loadData();
}

async function deleteExpense(id) {
    await fetch(`/api/expenses/${id}`, { method: 'DELETE' });
    loadData();
}

loadData();