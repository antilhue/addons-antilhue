odoo.define('website_sale_category_manu.categories_menu', function (require) {
    "use strict";

    require('web.dom_ready');

    $('.categories .nav').hover(function(){
        let a = $('.container-opacacity');
        a.toggleClass('container-show');
        console.log(a)
    });

});