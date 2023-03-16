// Wait for the document to be ready before running the code
$(document).ready(function() {
    // Store references to the necessary DOM elements
    const offer_input = $('#offer-input');
    const table_div = $('#offers_list_ajax');
    const pagination_div = $('#pagination');
    const filter_btn = $('#filter-btn');
    const dropdown_menu = document.getElementById('dropdown');
    
    // Initialize an empty array to store the selected checkbox values
    let selectedValues = [];
    // Find all checked checkboxes and add their values to the selectedValues array
    selectedValues = $('input[type=checkbox]:checked').map(function() {
        return $(this).val();
    }).get();

    // Define the endpoint for the AJAX request and the delay time for the function
    const endpoint = '/offers/';
    const delay_by_in_ms = 700;
    let scheduled_function = false;

    // Define the function to make the AJAX call
    let ajax_call = function (endpoint, request_parameters) {
        $.getJSON(endpoint, request_parameters)
            .done(response => {
                // Fade out the table div, update its contents and fade it back in
                table_div.fadeTo('slow', 0).promise().then(() => {
                    table_div.html(response['html_from_view_offer_list']);
                    pagination_div.html(response['html_from_view_pagination']);
                    table_div.fadeTo('slow', 1);
                })
            })
    }

    // Listen for keyup events on the offer input field
    offer_input.on("keyup", function() {
        // Define the parameters for the AJAX request
        const request_parameters = {
            offer_search: $(this).val(),
            sm: selectedValues
        }

        // Serialize the parameters and remove any extra characters
        let serialized_params = $.param(request_parameters);
        serialized_params = serialized_params.replace(/%5B%5D/g, '');

        // Clear any scheduled functions and schedule the AJAX call
        if (scheduled_function) {
            clearTimeout(scheduled_function)
        }
        scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint + '?' + serialized_params)
    });

    // Listen for click events on the filter button
    filter_btn.on("click", function() {
        // Update the selectedValues array with the current checked checkboxes
        selectedValues = $('input[type=checkbox]:checked').map(function() {
            return $(this).val();
        }).get();
        
        // Define the parameters for the AJAX request
        const request_parameters = {
            offer_search: offer_input.val(),
            sm: selectedValues
        }

        // Serialize the parameters and remove any extra characters
        let serialized_params = $.param(request_parameters);
        serialized_params = serialized_params.replace(/%5B%5D/g, '');

        // Hide the dropdown menu and make the AJAX call
        dropdown_menu.style.display = 'none';
        ajax_call(endpoint + '?' + serialized_params)
    });
});
