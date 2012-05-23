define(['require-oop'], function() {
    /*
     *  Abstract node base class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;

        // epoch timestampe in milliseconds will serve as timestamp
        this._id  = new Date().getTime();
        this._visualRepresentation = jQuery('.shapes .fuzzed-' + this.type())
                                        .clone()
                                        .draggable();
    };

    Node.prototype.id = function() {
        return this._id;
    };

    Node.prototype.type = function() {
        throw "Abstract Method - override type in subclass";
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
        this.Super.constructor.apply(this, arguments);
    }
    BasicEvent.Extends(Node);

    BasicEvent.prototype.type = function() {
        return "basic";
    }

    /*
     *  Undeveloped Event
     */
     function UndevelopedEvent() {
        this.Super.constructor.apply(this, arguments);
     }
     UndevelopedEvent.Extends(Node);

     UndevelopedEvent.prototype.type = function() {
        return "undeveloped";
     }

    /*
     *  Return the collection of all nodes for require
     */
    return {
        BasicEvent:       BasicEvent,
        UndevelopedEvent: UndevelopedEvent
    };
})