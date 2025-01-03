const URL = '/onboarding'

let canvas = document.querySelector('.canvas');

let info = {

    incomeSource: [],
    incomeAmount: [],
    expenseSource: [],
    expenseAmount: []

}
incomeRow = '<input type="text" name="incomeSource[]" placeholder="Income Source"><input type="number" name="incomeAmount[]" placeholder="Amount"><button type="button" class="removeRow hero-button" style="display: none;"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg></button>'
expenseRow = '<input type="text" name="expenseSource[]" placeholder="Expense Source"><input type="number" name="expenseAmount[]" placeholder="Amount"><button type="button" class="removeRow hero-button style=" display: none;"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg></button>'

function attachRemoveEvent(button) {
    button.style.display = 'inline-block';
    button.addEventListener('click', function () {
        this.parentElement.remove();
    })
}


document.querySelector('#addIncome').addEventListener('click', function () {
    const newRow = document.createElement('div');
    newRow.classList.add('incomeRow');
    newRow.innerHTML = incomeRow;
    document.getElementById('incomeForm').insertBefore(newRow, this)
    attachRemoveEvent(newRow.querySelector('.removeRow'));
})

document.querySelector('#addExpense').addEventListener('click', function () {
    const newRow = document.createElement('div');
    newRow.classList.add('expenseRow');
    newRow.innerHTML = expenseRow;
    document.getElementById('expenseForm').insertBefore(newRow, this)
    attachRemoveEvent(newRow.querySelector('.removeRow'));
})

submitButton = document.querySelector('#submitIncome');
submitButton.addEventListener('click', function () {
    const inputs = document.querySelectorAll('input');

    // Check for empty input fields
    for (const element of inputs) {
        if (String(element.value.trim()) === '') {
            alert('Cannot continue with empty input fields.');
            return; // Exit the function if an empty input is found
        }
    }

    // If no empty input is found, proceed with the rest of the code
    info.incomeSource = Array.from(document.querySelectorAll('input[name="incomeSource[]"]')).map(input => input.value);
    info.incomeAmount = Array.from(document.querySelectorAll('input[name="incomeAmount[]"]')).map(input => input.value);
    info.expenseSource = Array.from(document.querySelectorAll('input[name="expenseSource[]"]')).map(input => input.value);
    info.expenseAmount = Array.from(document.querySelectorAll('input[name="expenseAmount[]"]')).map(input => input.value);

    // Fetch request
    fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(info)
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            window.location.replace(data.url);
        });
});
