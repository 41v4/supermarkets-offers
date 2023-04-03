$(document).ready(function() {
    // Get references to the necessary DOM elements
    const test_wishlist_tbody = $('#test-wishlist-tbody'); // The wishlist table
    const test_wishlist_btn = $('#test-wishlist-btn'); // The button to filter the wishlist
    const product_name = $('#id_product_name'); // The input field for the product name
    const product_brand = $('#id_product_brand'); // The input field for the product brand
    const test_wishlist_errors = $('#test-wishlist-error-id') // The wishlist test error messages block

    // Define regular expressions to match the Django URL patterns
    const create_url_regex = /(?<=\/)wishlist\/create\//;
    const update_url_regex = /(?<=\/)wishlist\/(\d+)\/update\//;

    // Get the referrer URL and match it with the URL patterns
    const referrer_url = window.location.href;
    if (create_url_regex.test(referrer_url)) {
        // The referrer URL matches the "create" pattern
        var endpoint = '/wishlist/create/';
    } else if (update_url_regex.test(referrer_url)) {
        // The referrer URL matches the "update" pattern
        const match = update_url_regex.exec(referrer_url);
        const pk = match[1]; // Extract the dynamic part of the URL
        var endpoint = '/wishlist/' + pk + '/update/';
    } else {
        // The referrer URL does not match any of the patterns
        console.log('Unknown referrer URL:', referrer_url);
    }

    console.log(endpoint)
    // Define the function to make the AJAX call
    let ajax_call = function (endpoint, request_parameters) {
        $.getJSON(endpoint, request_parameters)
            .done(response => {
                // Fade out the table div, update its contents and fade it back in
                test_wishlist_tbody.fadeTo('slow', 0).promise().then(() => {
                    if (response['html_from_wishlist_item_create_view']) {
                        test_wishlist_tbody.html(response['html_from_wishlist_item_create_view']);
                        test_wishlist_errors.html("")
                    } else {
                        test_wishlist_tbody.html("");
                        test_wishlist_errors.html(response['custom_msgs']);
                    }
                    test_wishlist_tbody.fadeTo('slow', 1);
                })
            })
    }

    // Get references to the checkboxes for the supermarkets
    var checkboxes = document.querySelectorAll('#div_id_supermarkets input[type="checkbox"]');
    var selectedValues = [];

    // Add event listeners to the checkboxes to track which ones are checked
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            selectedValues.push(checkbox.value);
        }
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                selectedValues.push(this.value);
            } else {
                var index = selectedValues.indexOf(this.value);
                if (index > -1) {
                    selectedValues.splice(index, 1);
                }
            }
            console.log(selectedValues) // Log the selected values to the console for testing purposes
        });
    });

    // Listen for click events on the filter button
    test_wishlist_btn.on("click", function() {       
        // Define the parameters for the AJAX request
        const request_parameters = {
            product_name: product_name.val(),
            product_brand: product_brand.val(),
            selected_values: selectedValues,
        }

        console.log(request_parameters) // Log the request parameters to the console for testing purposes

        // Serialize the parameters and remove any extra characters
        let serialized_params = $.param(request_parameters);
        serialized_params = serialized_params.replace(/%5B%5D/g, '');

        // Hide the dropdown menu and make the AJAX call
        ajax_call(endpoint + '?' + serialized_params)
    });
});
