const URL = '/onboarding'

let canvas = document.querySelector('.canvas');

let info = {
    details: {
        firstname: '',
        surname: ''
    }, 
    income: [],
    expense: []
}

let incomeExpense = ""



function displayIncomeExpense() {
    canvas.innerHTML = incomeExpense;
    let incomeRow = '<input type="text" name="incomeSource[]" placeholder="Income Source"><input type="number" name="incomeAmount[]" placeholder="Amount"><button type="button" class="removeRow">Remove</button>';
    let expenseRow = '<input type="text" name="expenseSource[]" placeholder="Expense Source"><input type="number" name="expenseAmount[]" placeholder="Amount"><button type="button" class="removeRow">Remove</button>';

    document.querySelector('#addIncome').addEventListener('click', function() {
        const newRow = document.createElement('div');
        newRow.classList.add('incomeRow');
        newRow.innerHTML = incomeRow;
        document.getElementById('incomeForm').insertBefore(newRow, this)
        attachRemoveEvent(newRow.querySelector('.removeRow'));
    })

    document.querySelector('#addExpense').addEventListener('click', function() {
        const newRow = document.createElement('div');
        newRow.classList.add('expenseRow');
        newRow.innerHTML = expenseRow;
        document.getElementById('expenseForm').insertBefore(newRow, this)
        attachRemoveEvent(newRow.querySelector('.removeRow'));
    })
}

function attachRemoveEvent(button) {
    button.style.display = 'inline-block';
    button.addEventListener('click', function() {
        this.parentElement.remove();
    })
}

let button = document.getElementById('submitDetails');

button.addEventListener('click', function () {
    info.details.firstname = document.querySelector('#firstname').value;
    info.details.surname = document.querySelector('#surname').value;
    displayIncomeExpense();
})