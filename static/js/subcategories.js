console.log('JS file loaded successfully!');

function load_subcategories(category_id) {
  const subcategoryField = document.querySelector('select[name="subcategory"]');
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
