function loadSubcategories(selectElement) {
  const category_id = selectElement.value;
  const row = selectElement.closest('tr'); // Find the closest parent row element
  const rowIndex = Array.from(row.parentNode.children).indexOf(row); // Get the index of the row within its parent
  const subcategoryField = document.querySelectorAll('select[name="subcategory"]')[rowIndex];
  console.log("Here we go:")
  console.log(rowIndex)
  console.log(subcategoryField)
  const url = `/offers/get_subcategories/?category_id=${category_id}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      subcategoryField.innerHTML = '';
      const defaultOption = document.createElement('option');
      defaultOption.value = '';
      defaultOption.text = '---------';
      subcategoryField.appendChild(defaultOption);

      for (const subcategory of data.subcategories) {
        const option = document.createElement('option');
        option.value = subcategory.id;
        option.text = subcategory.name;
        subcategoryField.appendChild(option);
      }
    })
    .catch(error => console.log(error));
}

function getDataFromTable() {
  var rows = document.querySelectorAll('tbody tr');
  var data = [];

  rows.forEach(function(row) {
    var offerId = row.querySelector('span.product_name').getAttribute('offer-id');
    var categoryId = row.querySelector('select[name="category"]').value;
    var subcategoryId = row.querySelector('select[name="subcategory"]').value;

    data.push({
      offerId: offerId,
      categoryId: categoryId,
      subcategoryId: subcategoryId
    });
  });

  console.log(JSON.stringify(data))
  // return JSON.stringify(data);
  var csrfToken = document.getElementById("csrf_token").value;
  $.ajax({
    url: '/offers/save_categories/',
    type: 'POST',
    headers: {
        'X-CSRFToken': csrfToken
    },
    data: JSON.stringify(data),
    dataType: 'json',
    contentType: 'application/json',
    success: function(response) {
        // Handle success
    },
    error: function(response) {
        // Handle error
    }
});
}
