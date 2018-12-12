odoo.define("website_sale_algolia.search_autocomplete", function(require) {
    "use strict";
    require('web.dom_ready');
    const ajax = require('web.ajax');
    ajax.jsonRpc("/shop/get_algolia_settings/").then(function (data) {
        if(!data) return;
        display_algolia(data.index, data.app, data.key);
        });
    function display_algolia(index, app, key) {
        const client = algoliasearch(app, key);
        const index_client = client.initIndex(index);
        $(".search-autocomplete").autocomplete({ hint: false}, [
            {
                source: $.fn.autocomplete.sources.hits(index_client, { hitsPerPage: 8 }),
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
            window.location.replace(window.location.origin +
                '/shop/product/' + suggestion.objectID);
        });
        $.each($(".search-autocomplete"), function(index, value) {value.autocomplete='off'})
        // TODO: add catch
    };
});