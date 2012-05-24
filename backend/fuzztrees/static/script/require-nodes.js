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
            .attr('id', shape.attr('id') + this._id)
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
     *  Static map from type string to class
     */
    var NodeTypes = {};

    NodeTypes[Config.BASIC_EVENT]       = BasicEvent;
    NodeTypes[Config.UNDEVELOPED_EVENT] = UndevelopedEvent;
    NodeTypes[Config.HOUSE_EVENT]       = HouseEvent;
    NodeTypes[Config.AND_GATE]          = AndGate;
    NodeTypes[Config.OR_GATE]           = OrGate;
    NodeTypes[Config.XOR_GATE]          = XorGate;
    NodeTypes[Config.PRIORITY_AND_GATE] = PriorityAndGate;
    NodeTypes[Config.VOTING_OR_GATE]    = VotingOrGate;
    NodeTypes[Config.INHIBIT_GATE]      = InhibitGate;
    NodeTypes[Config.CHOICE_EVENT]      = ChoiceEvent;
    NodeTypes[Config.REDUNDANCY_EVENT]  = RedundancyEvent;
    NodeTypes[Config.BLOCK]             = Block;

    /*
     *  fromId - creates a node instance from a shape menu node id
     */
    function fromId(nodeId) {
        if (typeof(nodeId) !== 'string') throw 'Type Error - id has to be a string';

        var node = NodeTypes[nodeId];
        return typeof(node) !== 'undefined' ? new node : null;
    }

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
        Block:            Block,

        // module functions
        fromId:           fromId
    };
})