define(['require-config', 'require-oop'], function(Config) {
    /*
     *  Abstract node base class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;
        // epoch timestamp in milliseconds will do as an id
        this._id  = new Date().getTime();

        var shape = jQuery(Config.SHAPES_MENU + ' ' + Config.FUZZED_CLASS + this.type());
        var _this = this;
        this._visualRepresentation = shape.clone()
            // remove draggable class... thank you jsPlumb for all the weird sanity checks
            .removeClass('ui-draggable')
            .css({
                'position': 'absolute',
                'width':    shape.css('width'),
                'height':   shape.css('height')
            })
            .hover(
                function(e) {
                    jQuery(_this._sourceEndpoint.endpoint.getDisplayElements()).css('visibility', '');
                    jQuery(_this._targetEndpoint.endpoint.getDisplayElements()).css('visibility', '');
                },
                function(e) {
                    function hideEndpoints() {
                        jQuery(_this._sourceEndpoint.endpoint.getDisplayElements()).css('visibility', 'hidden');
                        jQuery(_this._targetEndpoint.endpoint.getDisplayElements()).css('visibility', 'hidden');
                    }
                    setTimeout(hideEndpoints, 2000);
                }
            );
    };

    Node.prototype.id = function() {
        return this._id;
    };

    Node.prototype.type = function() {
        throw 'Abstract Method - override type in subclass';
    };

    Node.prototype.appendTo = function(domElement, x, y) {
        this._visualRepresentation
            .appendTo(domElement)
            .css({
                top:  y || 0,
                left: x || 0
        });

        this._sourceEndpoint = jsPlumb.addEndpoint(this._visualRepresentation, {
            anchor:   'BottomCenter',
            isSource: true,
            isTarget: false
        });
        this._targetEndpoint = jsPlumb.addEndpoint(this._visualRepresentation, {
            anchor:   'TopCenter',
            isSource: false,
            isTarget: true
        });

        jsPlumb.draggable(this._visualRepresentation, {
            grid: [Config.GRID_SIZE, Config.GRID_SIZE]
        });
    };

    /*
     *  Basic Event
     */
    function BasicEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    BasicEvent.Extends(Node);

    BasicEvent.prototype.type = function() {
        return 'basic';
    }

    /*
     *  Undeveloped Event
     */
    function UndevelopedEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    UndevelopedEvent.Extends(Node);

    UndevelopedEvent.prototype.type = function() {
       return 'undeveloped';
    }

    /*
     *  Return the collection of all nodes for require
     */
    return {
        BasicEvent:       BasicEvent,
        UndevelopedEvent: UndevelopedEvent
    };
})