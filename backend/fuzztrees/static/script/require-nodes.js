define(['require-config', 'require-oop'], function(Config) {
    /*
     *  Abstract node base class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;
        // epoch timestamp in milliseconds will do as an id
        this._id  = new Date().getTime();

        var shape = jQuery(Config.Selectors.IDs.SHAPES_MENU + ' #' + this.type());
        var _this = this;
        this._visualRepresentation = shape
            .clone()
            // remove draggable class... thank you jsPlumb for all the weird sanity checks
            .attr('id', shape.attr('id') + this._id)
            .removeClass('ui-draggable')
            .removeClass(Config.Selectors.Classes.NODE_THUMBNAIL.substr(1))
            .addClass(Config.Selectors.Classes.NODE.substr(1))
            .css({
                'position': 'absolute',
                'width':    shape.css('width'),
                'height':   shape.css('height')
            })
            .hover(
                // hover in
                function(e) {
                    clearTimeout(this._hideEndpointsTimeout);
                    var node = jQuery(this).data(Config.Keys.NODE);
                    jQuery(node._sourceEndpoint.endpoint.getDisplayElements()).css('visibility', '');
                    jQuery(node._targetEndpoint.endpoint.getDisplayElements()).css('visibility', '');
                },
                // hover out
                function(e) {
                    var _this = this;
                    function hideEndpoints() {
                        var node = jQuery(_this).data(Config.Keys.NODE);
                        jQuery(node._sourceEndpoint.endpoint.getDisplayElements()).css('visibility', 'hidden');
                        jQuery(node._targetEndpoint.endpoint.getDisplayElements()).css('visibility', 'hidden');
                    }
                    this._hideEndpointsTimeout = setTimeout(hideEndpoints, 2000);
                }
            )
            .click(function() {
                var node = jQuery(this).data(Config.Keys.NODE);
                jQuery(Config.Selectors.Classes.NODE).removeClass(Config.Selectors.Classes.SELECTED);
                jQuery(this).addClass(Config.Selectors.Classes.SELECTED);
            });

        // link back to Node object
        this._visualRepresentation.data(Config.Keys.NODE, this);
    };

    Node.prototype.id = function() {
        return this._id;
    };

    Node.prototype.type = function() {
        throw 'Abstract Method - override type in subclass';
    };

    Node.prototype.appendTo = function(domElement) {
        this._visualRepresentation
            .appendTo(domElement)
            .css({
                width:  Config.Grid.SIZE,
                height: Config.Grid.SIZE
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
            opacity:     Config.Dragging.OPACITY,
            cursor:      Config.Dragging.CURSOR,
            grid:        [Config.Grid.SIZE, Config.Grid.SIZE],
            stack:       Config.Selectors.Classes.NODE
        });

        return this;
    };

    Node.prototype.moveTo = function(x, y) {
        this._visualRepresentation.css({
            left: x || 0,
            top:  y || 0
        });

        return this;
    }

    /*
     *  Basic Event
     */
    function BasicEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    BasicEvent.Extends(Node);

    BasicEvent.prototype.type = function() {
        return Config.Types.BASIC_EVENT;
    }

    /*
     *  Multi Event
     */
    function MultiEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    MultiEvent.Extends(Node);

    MultiEvent.prototype.type = function() {
        return Config.Types.MULTI_EVENT;
    }

    /*
     *  Undeveloped Event
     */
    function UndevelopedEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    UndevelopedEvent.Extends(Node);

    UndevelopedEvent.prototype.type = function() {
       return Config.Types.UNDEVELOPED_EVENT;
    }

    /*
     *  House Event
     */
    function HouseEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    HouseEvent.Extends(Node);

    HouseEvent.prototype.type = function() {
       return Config.Types.HOUSE_EVENT;
    }

    /*
     *  AndGate
     */
    function AndGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    AndGate.Extends(Node);

    AndGate.prototype.type = function() {
       return Config.Types.AND_GATE;
    }

    /*
     *  OrGate
     */
    function OrGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    OrGate.Extends(Node);

    OrGate.prototype.type = function() {
        return Config.Types.OR_GATE;
    }

    /*
     *  XorGate
     */
    function XorGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    XorGate.Extends(Node);

    XorGate.prototype.type = function() {
        return Config.Types.XOR_GATE;
    }

    /*
     *  PriorityAndGate
     */
    function PriorityAndGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    PriorityAndGate.Extends(Node);

    PriorityAndGate.prototype.type = function() {
        return Config.Types.PRIORITY_AND_GATE;
    }

    /*
     *  VotingOrGate
     */
    function VotingOrGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    VotingOrGate.Extends(Node);

    VotingOrGate.prototype.type = function() {
        return Config.Types.VOTING_OR_GATE;
    }

    /*
     *  InhibitGate
     */
    function InhibitGate() {
        this.Super.constructor.apply(this, arguments);
    } 
    InhibitGate.Extends(Node);

    InhibitGate.prototype.type = function() {
        return Config.Types.INHIBIT_GATE;
    }

    /*
     *  ChoiceEvent
     */
    function ChoiceEvent() {
        this.Super.constructor.apply(this, arguments);
    } 
    ChoiceEvent.Extends(Node);

    ChoiceEvent.prototype.type = function() {
        return Config.Types.CHOICE_EVENT;
    }

    /*
     *  RedundancyEvent
     */
    function RedundancyEvent() {
        this.Super.constructor.apply(this, arguments);
    } 
    RedundancyEvent.Extends(Node);

    RedundancyEvent.prototype.type = function() {
        return Config.Types.REDUNDANCY_EVENT;
    }

    /*
     *  Associate the constructors with the thumbnails in the shape menu
     */
    jQuery('#' + Config.Types.BASIC_EVENT)      .data(Config.Keys.CONSTRUCTOR, BasicEvent);
    jQuery('#' + Config.Types.MULTI_EVENT)      .data(Config.Keys.CONSTRUCTOR, MultiEvent);
    jQuery('#' + Config.Types.UNDEVELOPED_EVENT).data(Config.Keys.CONSTRUCTOR, UndevelopedEvent);
    jQuery('#' + Config.Types.HOUSE_EVENT)      .data(Config.Keys.CONSTRUCTOR, HouseEvent);
    jQuery('#' + Config.Types.AND_GATE)         .data(Config.Keys.CONSTRUCTOR, AndGate);
    jQuery('#' + Config.Types.OR_GATE)          .data(Config.Keys.CONSTRUCTOR, OrGate);
    jQuery('#' + Config.Types.XOR_GATE)         .data(Config.Keys.CONSTRUCTOR, XorGate);
    jQuery('#' + Config.Types.PRIORITY_AND_GATE).data(Config.Keys.CONSTRUCTOR, PriorityAndGate);
    jQuery('#' + Config.Types.VOTING_OR_GATE)   .data(Config.Keys.CONSTRUCTOR, VotingOrGate);
    jQuery('#' + Config.Types.INHIBIT_GATE)     .data(Config.Keys.CONSTRUCTOR, InhibitGate);
    jQuery('#' + Config.Types.CHOICE_EVENT)     .data(Config.Keys.CONSTRUCTOR, ChoiceEvent);
    jQuery('#' + Config.Types.REDUNDANCY_EVENT) .data(Config.Keys.CONSTRUCTOR, RedundancyEvent);

    /*
     *  Return the collection of all nodes for require
     */
    return {
        // classes
        BasicEvent:       BasicEvent,
        MultiEvent:       MultiEvent,
        UndevelopedEvent: UndevelopedEvent,
        HouseEvent:       HouseEvent,
        AndGate:          AndGate,
        OrGate:           OrGate,
        XorGate:          XorGate,
        PriorityAndGate:  PriorityAndGate,
        VotingOrGate:     VotingOrGate,
        InhibitGate:      InhibitGate,
        ChoiceEvent:      ChoiceEvent,
        RedundancyEvent:  RedundancyEvent
    };
})