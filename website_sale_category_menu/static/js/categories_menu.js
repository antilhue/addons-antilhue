odoo.define('website_sale_category_manu.categories_menu', function (require) {
    "use strict";

    require('web.dom_ready');
    $('.mega-dropdown').hover(
        function (){
            const $category = $(this)
            window.mytimeout = setTimeout(function() {
                $('.container-opacacity').addClass('container-show');
                $category.find('.mega-dropdown-menu').addClass('category-show')
               } , 250);
        },
        function () {
            const $category = $(this)
            $category.find('.mega-dropdown-menu').removeClass('category-show')
            $('.container-opacacity').removeClass('container-show')
            clearTimeout(window.mytimeout);
    });
});