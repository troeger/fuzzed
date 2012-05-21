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
                'width': 50,
                'height': 50,
                'border': '1px solid black'
                })
            .draggable();

    };

    Node.prototype._svgPath = function() {
        throw "Abstract Method";
    };

    Node.prototype.appendTo = function(domElement) {
        jQuery(domElement).append(this._visualRepresentation);
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