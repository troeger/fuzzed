define(function() {
    jQuery(document).ready(function () {
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
    });
});