odoo.define("website_sale_algolia.search_autocomplete", function(require) {
    "use strict";
    require('web.dom_ready');
    const algolia_app_id = $('input[name=algolia_app_id]').val();
    const algolia_key_search = $('input[name=algolia_key_search]').val();
    const algolia_index = $('input[name=algolia_index]').val();
    if ( !algolia_app_id || ! algolia_key_search){
        return;
    }
    const client = algoliasearch(algolia_app_id, algolia_key_search);
    const index = client.initIndex(algolia_index);
    $(".search-complete").autocomplete({ hint: false, debug: true}, [
        {
            source: $.fn.autocomplete.sources.hits(index, { hitsPerPage: 8 }),
            displayKey: 'name',
            templates: {
                suggestion: function(suggestion) {
                    return '<div><img class="picture" src="/website/image/product.template/'
                        + suggestion.objectID + '/image/90x90"/><div class="text-container"><span>'
                        + suggestion._highlightResult.name.value + '</span></div></div>';

                }
            }
        }
    ]).on('autocomplete:selected', function(event, suggestion, dataset) {
        console.log(suggestion, dataset);
        window.location.replace(window.location.origin +
            '/shop/product/' + suggestion.objectID);
    });
});