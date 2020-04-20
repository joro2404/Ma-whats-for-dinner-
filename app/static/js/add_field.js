$(document).ready(function() {
    var max_fields = 10;
    var wrapper = $(".container_fields");
    var add_button = $(".add_form_field");

    var x = 1;
    $(add_button).click(function(e) {
        e.preventDefault();
        if (x < max_fields) {
            x++;
            $(wrapper).append('\
            <div class="row">\
                <div class="col-25">\
                <label>Product ' + x + '</label>\
                </div>\
                <div class="col-75">\
                <select name="name_of_product' + x + '">\
                    {% for product in products %}\
                        <option value="{{ product.id }}">{{ product.name }} ({{ product.unit }})</option>\
                    {% endfor %}\
                </select>\
                <input type="number" name="units_of_product1" placeholder="Only number of units!">\
                </div>\
            </div>\
            '); //add input box
        } else {
            alert('You Reached the limits')
        }
    });

    $(wrapper).on("click", ".delete", function(e) {
        e.preventDefault();
        $(this).parent('div').remove();
        x--;
    })
});

document.getElementById('number_of_products').value