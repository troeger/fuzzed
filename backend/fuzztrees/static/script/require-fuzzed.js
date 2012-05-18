define(function() {
    jQuery(document).ready(function () {
        console.log("alive");

        var container = jQuery(".layout");
        var west = jQuery(".west");
        var east = jQuery(".east");

        function relayout() {
            container.layout({
                type:   "border",
                resize: false,
                hgap:   3,
                vgap:   3
            });
        }
        relayout();
        jQuery(window).resize(relayout);

        
        west.resizable({
            handles: "e",
            resize:  relayout
        });

        east.resizable({
            handles: "w",
            resize:  relayout
        });
    });
});