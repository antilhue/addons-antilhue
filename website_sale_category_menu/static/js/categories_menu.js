odoo.define('website_sale_category_manu.categories_menu', function (require) {
    "use strict";

    require('web.dom_ready');
    $('.categories .nav')
        .mouseenter(function() {
          $('.container-opacacity').addClass('container-show');
        })
        .mouseleave(function() {
            $('.container-opacacity').removeClass('container-show')
        });
});