define(function() {
    
    function Node() {
        this._visualRepresentation = jQuery('<div class="node"></div>')
            .css({
                'display': 'block',
                'width': 50,
                'height': 50,
                'border': '1px solid black'
                })
            .draggable();

    };

    Node.prototype.appendTo = function(domElement) {
        jQuery(domElement).append(this._visualRepresentation);
    }

    return Node;
})