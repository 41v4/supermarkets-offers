// Wait for the document to be ready before running the code
$(document).ready(function() {
    // Store references to the necessary DOM elements
    const exp_offers_tab = $('#exp-offers-tab');
    const offer_desc_tab = $('#offer-detail-tab');
    const offer_details_section = $('#offer-details-section');
    const offer_name = $('main h1');

    // Initialize current tab variable to keep track of which current tab is selected
    let current_tab = "desc";

    // Define the function to make the AJAX call
    let ajax_call = function (request_parameters) {
        const endpoint = window.location.pathname;

        $.getJSON(endpoint, request_parameters)
            .done(response => {
                // Fade out the table div, update its contents and fade it back in
                offer_details_section.fadeTo('slow', 0).promise().then(() => {
                    offer_details_section.html(response['html_from_offer_detail_view']);
                    offer_details_section.fadeTo('slow', 1);
                })
            })
    }

    // Listen for click events on the filter button
    exp_offers_tab.on("click", function() {
        console.log("Exp. offers tab clicked!")
        
        // If the current tab is exp and exp tab was clicked - then do nothing
        if (current_tab === "exp") {
            return;
        }

        // Define the parameters for the AJAX request
        const request_parameters = {
            offer_name: offer_name.text(),
            tab_clicked: "exp",
        }

        // Serialize the parameters and remove any extra characters
        let serialized_params = $.param(request_parameters);
        serialized_params = serialized_params.replace(/%5B%5D/g, '');

        ajax_call(serialized_params);

        // Set the flag to 'exp' indicating that an AJAX request has been made for this tab
        current_tab = "exp";
    });

    // Listen for click events on the filter button
    offer_desc_tab.on("click", function() {
        console.log("Offer desc. tab clicked!")
        
        // If the current tab is desc and desc tab was clicked - then do nothing
        if (current_tab === "desc") {
            return;
        }

        // Define the parameters for the AJAX request
        const request_parameters = {
            offer_name: offer_name.text(),
            tab_clicked: "desc",
        }

        // Serialize the parameters and remove any extra characters
        let serialized_params = $.param(request_parameters);
        serialized_params = serialized_params.replace(/%5B%5D/g, '');

        ajax_call(serialized_params);

        // Set the flag to 'desc' indicating that an AJAX request has been made for
        current_tab = "desc";
    });
});
