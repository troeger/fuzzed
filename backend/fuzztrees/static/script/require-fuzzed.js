define(['./require-node'], function(Node) {
    jQuery(document).ready(function () {
        /*
         *  Init layout
         */
        var layoutOptions = {
            defaults: {
                applyDefaultStyles: false,
                resizable: false,
                closable: false,
                spacing_open: 0
            },
            north: {
                size: 26
            }
        }

        var layout = $('body').layout(layoutOptions);

        /*
         *  Init jsPlumb
         */
        jsPlumb.importDefaults({
            EndpointStyles: [{ fillStyle: '#225588' }, { fillStyle: '#225566' }],
            Endpoints: [ ['Dot', {radius: 5}], ['Dot', {radius: 5}] ]
        });


        // XXX: test node
        var node = new Node();
        node.appendTo(jQuery('.ui-layout-center'));
    });
});