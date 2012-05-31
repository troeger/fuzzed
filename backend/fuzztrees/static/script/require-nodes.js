define(['require-config', 'require-oop'], function(Config) {
    /*
     *  Abstract node base class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;

        this._generateId();
        this._locateEditor();
        this._initializeVisualRepresentation();
    }

    Node.prototype.appendTo = function(domElement) {
        // some visual stuff, interaction and endpoints need to go here since they require the elements to be
        // already in the DOM. This is why we cannot initialize all of it already in the constructor
        this._visualRepresentation.appendTo(domElement);

        this._resizeOnDrop();
        this._initializeEndpoints();
        this._makeInteractive();

        return this;
    }

    Node.prototype.deselect = function() {
        this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_NORMAL);
    }

    Node.prototype.id = function() {
        return this._id;
    }

    Node.prototype.moveTo = function(x, y) {
        this._visualRepresentation.css({
            left: x || 0,
            top:  y || 0
        });

        return this;
    }

    Node.prototype.remove = function() {
        jsPlumb.deleteEndpoint(this._sourceEndpoint);
        jsPlumb.deleteEndpoint(this._targetEndpoint);
        this._visualRepresentation.remove();
    }

    Node.prototype.select = function() {
        this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_SELECTED);
    }

    Node.prototype.type = function() {
        throw 'Abstract Method - override type in subclass';
    }

    Node.prototype._generateId = function() {
        // epoch timestamp will do
        this._id = new Date().getTime();

        return this._id;
    }

    Node.prototype._locateEditor = function() {
        this._editor = jQuery('#' + Config.IDs.CANVAS).data(Config.Keys.EDITOR);
    }

    Node.prototype._initializeVisualRepresentation = function() {
        // get the thumbnail and clone it
        var container = jQuery('<div>');
        var label     = jQuery('<span>Foo</span>');
        var thumbnail = jQuery('#' + Config.IDs.SHAPES_MENU + ' #' + this.type()).clone();

        container
            .attr('id', thumbnail.attr('id') + this._id)
            .addClass(Config.Classes.NODE)
            .css({
                position: 'absolute',
                width:    Config.Grid.SIZE,
                height:   Config.Grid.SIZE
            });

        thumbnail
            // cleanup the thumbnail's specific properties
            .removeClass('ui-draggable')
            .removeClass(Config.Classes.NODE_THUMBNAIL)
            .removeAttr('id')
            // add new stuff
            .addClass(Config.Classes.NODE_IMAGE)
            .appendTo(container);

        label
            .addClass(Config.Classes.NODE_LABEL)
            .appendTo(container);

        this._visualRepresentation = container;

        // give visual representation a back-link to this object
        this._visualRepresentation.data(Config.Keys.NODE, this); 
    }

    Node.prototype._resizeOnDrop = function() {
        // find the nodes
        var image = this._visualRepresentation.children('.' + Config.Classes.NODE_IMAGE);
        var svg   = image.children('svg');
        var g     = svg.children('g');

        // calculate the scale factor
        var marginOffset = image.outerWidth(true) - image.width();
        var scaleFactor  = (Config.Grid.SIZE - Config.Node.LABEL_HEIGHT - marginOffset) / svg.height();

        // resize the svg and its elements
        svg.width(svg.width() * scaleFactor);
        svg.height(svg.height() * scaleFactor);
        g.attr('transform', 'scale(' + scaleFactor + ') ' + g.attr('transform'));
    }

    Node.prototype._initializeEndpoints = function() {     
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
    }

    Node.prototype._makeInteractive = function() {
        var _this = this;

        // make the node draggable
        jsPlumb.draggable(this._visualRepresentation, {
            containment: 'parent',
            opacity:     Config.Dragging.OPACITY,
            cursor:      Config.Dragging.CURSOR,
            grid:        [Config.Grid.SIZE, Config.Grid.SIZE],
            stack:       '.' + Config.Classes.NODE,
            start:       function() {
                _this._editor.selection(_this);
            }
        });

        // hovering over a node
        this._visualRepresentation.hover(
            function() {
                if (!_this._editor.isSelected(_this)) {
                    _this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_HOVER);
                }
            },
            function() {
                if (!_this._editor.isSelected(_this)) {
                    _this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_NORMAL);
                }
            }
        );

        // clicking on a node
        this._visualRepresentation.click(
            function(eventObject) {
                eventObject.stopPropagation();
                _this._editor.selection(_this);
            }
        );
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
     *  Fault Event
     */
    function FaultEvent() {
        this.Super.constructor.apply(this, arguments);
    }
    FaultEvent.Extends(Node);

    FaultEvent.prototype.type = function() {
       return Config.Types.FAULT_EVENT;
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
     *  Associate the constructors with the thumbnails in the shape menu
     */
    jQuery('#' + Config.Types.BASIC_EVENT)      .data(Config.Keys.CONSTRUCTOR, BasicEvent);
    jQuery('#' + Config.Types.MULTI_EVENT)      .data(Config.Keys.CONSTRUCTOR, MultiEvent);
    jQuery('#' + Config.Types.UNDEVELOPED_EVENT).data(Config.Keys.CONSTRUCTOR, UndevelopedEvent);
    jQuery('#' + Config.Types.FAULT_EVENT)      .data(Config.Keys.CONSTRUCTOR, FaultEvent);
    jQuery('#' + Config.Types.AND_GATE)         .data(Config.Keys.CONSTRUCTOR, AndGate);
    jQuery('#' + Config.Types.OR_GATE)          .data(Config.Keys.CONSTRUCTOR, OrGate);
    jQuery('#' + Config.Types.XOR_GATE)         .data(Config.Keys.CONSTRUCTOR, XorGate);
    jQuery('#' + Config.Types.PRIORITY_AND_GATE).data(Config.Keys.CONSTRUCTOR, PriorityAndGate);
    jQuery('#' + Config.Types.VOTING_OR_GATE)   .data(Config.Keys.CONSTRUCTOR, VotingOrGate);
    jQuery('#' + Config.Types.INHIBIT_GATE)     .data(Config.Keys.CONSTRUCTOR, InhibitGate);
    jQuery('#' + Config.Types.CHOICE_EVENT)     .data(Config.Keys.CONSTRUCTOR, ChoiceEvent);
    jQuery('#' + Config.Types.REDUNDANCY_EVENT) .data(Config.Keys.CONSTRUCTOR, RedundancyEvent);
    jQuery('#' + Config.Types.HOUSE_EVENT)      .data(Config.Keys.CONSTRUCTOR, HouseEvent);

    /*
     *  Return the collection of all nodes for require
     */
    return {
        // classes
        BasicEvent:       BasicEvent,
        MultiEvent:       MultiEvent,
        UndevelopedEvent: UndevelopedEvent,
        FaultEvent:       FaultEvent,
        AndGate:          AndGate,
        OrGate:           OrGate,
        XorGate:          XorGate,
        PriorityAndGate:  PriorityAndGate,
        VotingOrGate:     VotingOrGate,
        InhibitGate:      InhibitGate,
        ChoiceEvent:      ChoiceEvent,
        RedundancyEvent:  RedundancyEvent,
        HouseEvent:       HouseEvent
    };
})