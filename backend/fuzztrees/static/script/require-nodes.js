define(['require-config', 'require-oop'], function(Config) {
    /*
     *  Abstract node base class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;
        // epoch timestamp in milliseconds will do as an id
        this._id  = new Date().getTime();

        var shape = jQuery(Config.SHAPES_MENU + ' #' + this.type());
        var _this = this;
        this._visualRepresentation = shape
            .clone()
            // remove draggable class... thank you jsPlumb for all the weird sanity checks
            .attr('id', shape.attr('id') + this._id)
            .removeClass('ui-draggable')
            .removeClass(Config.NODE_THUMBNAIL_CLASS.substr(1))
            .addClass(Config.NODE_CLASS.substr(1))
            .css({
                'position': 'absolute',
                'width':    shape.css('width'),
                'height':   shape.css('height')
            })
            .hover(
                // hover in
                function(e) {
                    clearTimeout(this._hideEndpointsTimeout);
                    var node = jQuery(this).data(Config.DATA_NODE);
                    jQuery(node._sourceEndpoint.endpoint.getDisplayElements()).css('visibility', '');
                    jQuery(node._targetEndpoint.endpoint.getDisplayElements()).css('visibility', '');
                },
                // hover out
                function(e) {
                    var _this = this;
                    function hideEndpoints() {
                        var node = jQuery(_this).data(Config.DATA_NODE);
                        jQuery(node._sourceEndpoint.endpoint.getDisplayElements()).css('visibility', 'hidden');
                        jQuery(node._targetEndpoint.endpoint.getDisplayElements()).css('visibility', 'hidden');
                    }
                    this._hideEndpointsTimeout = setTimeout(hideEndpoints, 2000);
                }
            )
            .click(function() {
                var node = jQuery(this).data(Config.DATA_NODE);
                jQuery(Config.NODE_CLASS).removeClass('fuzzed-node-selected'); //TODO: config
                jQuery(this).addClass('fuzzed-node-selected');
            });

        // link back to Node object
        this._visualRepresentation.data(Config.DATA_NODE, this);
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
            containment: 'parent',
            opacity:     Config.DRAGGING_OPACITY,
            cursor:      Config.DRAGGING_CURSOR,
            grid:        [Config.GRID_SIZE, Config.GRID_SIZE],
            stack:       Config.NODES_CLASS
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
        return Config.BASIC_EVENT;
    }

    /*
     *  Undeveloped Event
     */
    function UndevelopedEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    UndevelopedEvent.Extends(Node);

    UndevelopedEvent.prototype.type = function() {
       return Config.UNDEVELOPED_EVENT;
    }

    /*
     *  House Event
     */
    function HouseEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    HouseEvent.Extends(Node);

    HouseEvent.prototype.type = function() {
       return Config.HOUSE_EVENT;
    }

    /*
     *  AndGate
     */
    function AndGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    AndGate.Extends(Node);

    AndGate.prototype.type = function() {
       return Config.AND_GATE;
    }

    /*
     *  OrGate
     */
    function OrGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    OrGate.Extends(Node);

    OrGate.prototype.type = function() {
        return Config.OR_GATE;
    }

    /*
     *  XorGate
     */
    function XorGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    XorGate.Extends(Node);

    XorGate.prototype.type = function() {
        return Config.XOR_GATE;
    }

    /*
     *  PriorityAndGate
     */
    function PriorityAndGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    PriorityAndGate.Extends(Node);

    PriorityAndGate.prototype.type = function() {
        return Config.PRIORITY_AND_GATE;
    }

    /*
     *  VotingOrGate
     */
    function VotingOrGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    VotingOrGate.Extends(Node);

    VotingOrGate.prototype.type = function() {
        return Config.VOTING_OR_GATE;
    }

    /*
     *  InhibitGate
     */
    function InhibitGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    InhibitGate.Extends(Node);

    InhibitGate.prototype.type = function() {
        return Config.INHIBIT_GATE;
    }

    /*
     *  ChoiceEvent
     */
    function ChoiceEvent() {
        this.Super.constructor.apply(this, arguments);
    } 
    ChoiceEvent.Extends(Node);

    ChoiceEvent.prototype.type = function() {
        return Config.CHOICE_EVENT;
    }

    /*
     *  RedundancyEvent
     */
    function RedundancyEvent() {
        this.Super.constructor.apply(this, arguments);
    } 
    RedundancyEvent.Extends(Node);

    RedundancyEvent.prototype.type = function() {
        return Config.REDUNDANCY_EVENT;
    }

    /*
     *  Block
     */
    function Block() {
        this.Super.constructor.apply(this, arguments);
    } 
    Block.Extends(Node);

    Block.prototype.type = function() {
        return Config.BLOCK;
    }

    /*
     *  Associate the constructors with the thumbnails in the shape menu
     */
    jQuery('#' + Config.BASIC_EVENT)      .data(Config.DATA_CONSTRUCTOR, BasicEvent);
    jQuery('#' + Config.UNDEVELOPED_EVENT).data(Config.DATA_CONSTRUCTOR, UndevelopedEvent);
    jQuery('#' + Config.HOUSE_EVENT)      .data(Config.DATA_CONSTRUCTOR, HouseEvent);
    jQuery('#' + Config.AND_GATE)         .data(Config.DATA_CONSTRUCTOR, AndGate);
    jQuery('#' + Config.OR_GATE)          .data(Config.DATA_CONSTRUCTOR, OrGate);
    jQuery('#' + Config.XOR_GATE)         .data(Config.DATA_CONSTRUCTOR, XorGate);
    jQuery('#' + Config.PRIORITY_AND_GATE).data(Config.DATA_CONSTRUCTOR, PriorityAndGate);
    jQuery('#' + Config.VOTING_OR_GATE)   .data(Config.DATA_CONSTRUCTOR, VotingOrGate);
    jQuery('#' + Config.INHIBIT_GATE)     .data(Config.DATA_CONSTRUCTOR, InhibitGate);
    jQuery('#' + Config.CHOICE_EVENT)     .data(Config.DATA_CONSTRUCTOR, ChoiceEvent);
    jQuery('#' + Config.REDUNDANCY_EVENT) .data(Config.DATA_CONSTRUCTOR, RedundancyEvent);
    jQuery('#' + Config.BLOCK)            .data(Config.DATA_CONSTRUCTOR, Block);

    /*
     *  Return the collection of all nodes for require
     */
    return {
        // classes
        BasicEvent:       BasicEvent,
        UndevelopedEvent: UndevelopedEvent,
        HouseEvent:       HouseEvent,
        AndGate:          AndGate,
        OrGate:           OrGate,
        XorGate:          XorGate,
        PriorityAndGate:  PriorityAndGate,
        VotingOrGate:     VotingOrGate,
        InhibitGate:      InhibitGate,
        ChoiceEvent:      ChoiceEvent,
        RedundancyEvent:  RedundancyEvent,
        Block:            Block
    };
})