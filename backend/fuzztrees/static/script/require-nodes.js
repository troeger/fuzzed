define(['require-oop'], function() {

    /*
     *  Abstract node base class
     */
    function Node() {
        // epoch timestampe in milliseconds will serve as timestamp
        this.id = new Date().getTime();
        this._visualRepresentation = jQuery('<div class="node"></div>')
            .css({
                'display': 'block',
                'position': 'absolute',
                'width': 50,
                'height': 50,
                'border': '3px solid black'
                });

    };

    Node.prototype._svgPath = function() {
        throw "Abstract Method";
    };

    Node.prototype.appendTo = function(domElement) {
        jQuery(domElement).append(this._visualRepresentation);
        jsPlumb.addEndpoint(this._visualRepresentation, {
            anchor: 'BottomCenter',
            isSource: true,
            isTarget: false
        });
        jsPlumb.addEndpoint(this._visualRepresentation, {
            anchor: 'TopCenter',
            isSource: false,
            isTarget: true
        });
        jsPlumb.draggable(this._visualRepresentation);
    };

    /*
     *  Basic Event
     */
    function BasicEvent() {

    }
    BasicEvent.extend(Node);

    /*
     *  Return the collection of all nodes for require
     */
    return {
        BasicEvent: BasicEvent
    };
})