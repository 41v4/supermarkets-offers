// Used for resetting wishlist form when refreshing the page

// Get the form element by its ID
var form = document.getElementById('wishlist-form-id');

// Reset the form when the page is loaded
window.onload = function() {
    form.reset();
}