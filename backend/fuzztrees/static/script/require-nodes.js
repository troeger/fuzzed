define(['require-config', 'require-properties', 'require-oop'], function(Config, Properties) {

    /*
     *  Abstract Node Base Class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;

        // fetch editor instance
        this._editor               = jQuery('#' + Config.IDs.CANVAS).data(Config.Keys.EDITOR);
        this._id                   = this._generateId();
        this._properties           = this._defineProperties();
        this._visualRepresentation = this._setupVisualRepresentation();
    }

    Node.prototype.appendTo = function(domElement) {
        // some visual stuff, interaction and endpoints need to go here since they require the elements to be
        // already in the DOM. This is why we cannot initialize all of it already in the constructor
        this._visualRepresentation.appendTo(domElement);

        this._resize();
        this._setupEndpoints();
        this._setupDragging();
        this._setupMouse();

        return this;
    }

    Node.prototype.deselect = function() {
        this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_NORMAL);
        return this;
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

    Node.prototype.properties = function() {
        return this._properties;
    }

    Node.prototype.remove = function() {
        jsPlumb.deleteEndpoint(this._sourceEndpoint);
        jsPlumb.deleteEndpoint(this._targetEndpoint);
        this._visualRepresentation.remove();
    }

    Node.prototype.select = function() {
        this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_SELECTED);
        return this;
    }

    Node.prototype.type = function() {
        throw 'Abstract Method - override type in subclass';
    }

    Node.prototype._defineProperties = function() {
        // the basic node does not have any properties therefore the empty array
        // overwrite in subclasses in order to set any
        return [];
    }

    Node.prototype._generateId = function() {
        // epoch timestamp will do
        return new Date().getTime();
    }

    Node.prototype._resize = function() {
        // find the node's svg element and path groups
        var image = this._visualRepresentation.children('.' + Config.Classes.NODE_IMAGE);
        var svg   = image.children('svg');
        var g     = svg.children('g');

        // calculate the scale factor
        var marginOffset = image.outerWidth(true) - image.width();
        var scaleFactor  = (Config.Grid.SIZE - marginOffset) / svg.height();

        // resize the svg and the groups
        svg.width (svg.width()  * scaleFactor);
        svg.height(svg.height() * scaleFactor);
        g.attr('transform', 'scale(' + scaleFactor + ') ' + g.attr('transform'));
    }

    Node.prototype._setupDragging = function() {
        var _this = this;

        jsPlumb.draggable(this._visualRepresentation, {
            containment: 'parent',
            opacity:     Config.Dragging.OPACITY,
            cursor:      Config.Dragging.CURSOR,
            grid:        [Config.Grid.SIZE, Config.Grid.SIZE],
            stack:       '.' + Config.Classes.NODE,
            start:       function() {
                _this._editor.selection.of(_this);
            }
        });
    }

    Node.prototype._setupEndpoints = function() {     
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

    Node.prototype._setupMouse = function() {
        var _this = this;

        // click on the node
        this._visualRepresentation.click(
            function(eventObject) {
                eventObject.stopPropagation();
                _this._editor.selection.of(_this);
            }
        );

        // hovering
        this._visualRepresentation.hover(
            function() {
                if (!_this._editor.selection.contains(_this)) {
                    _this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_HOVER);
                }
            },
            function() {
                if (!_this._editor.selection.contains(_this)) {
                    _this._visualRepresentation.find('path').css('stroke', Config.Node.STROKE_NORMAL);
                }
            }
        );
    }

    Node.prototype._setupVisualRepresentation = function() {
        // get the thumbnail, clone it and wrap it with a container (for labels)
        var container = jQuery('<div>');
        var thumbnail = jQuery('#' + Config.IDs.SHAPES_MENU + ' #' + this.type()).clone();

        container
            .attr('id', thumbnail.attr('id') + this._id)
            .addClass(Config.Classes.NODE)
            .css('position', 'absolute')
            .data(Config.Keys.NODE, this);

        thumbnail
            // cleanup the thumbnail's specific properties
            .removeClass('ui-draggable')
            .removeClass(Config.Classes.NODE_THUMBNAIL)
            .removeAttr('id')
            // add new classes for the actual node
            .addClass(Config.Classes.NODE_IMAGE)
            .appendTo(container);

        return container;
    }

    /*
     *  Abstract Event Base Class
     */
    function Event() {
        if (this.constructor === Event) return;
        Event.Super.constructor.apply(this, arguments);
    }
    Event.Extends(Node);

    Event.prototype._defineProperties = function() {
        return [
            new Properties.Text(this, {
                name:  'Name',
                value: 'Event',
                label: true
            }),
            new Properties.Text(this, {
                name:  'Probability',
                value: '0' 
            }),
        ];
    }

    Event.prototype._setupVisualRepresentation = function() {
        var container = Event.Super._setupVisualRepresentation.call(this);

        // add label for events
        jQuery('<span>Event</span>')
            .addClass(Config.Classes.NODE_LABEL)
            .appendTo(container);

        return container;
    }

    /*
     *  Abstract Gate Base Class
     */
    function Gate() {
        if (this.constructor === Gate) return;
        Gate.Super.constructor.apply(this, arguments);
    }
    Gate.Extends(Node);

    /*
     *  Basic Event
     */
    function BasicEvent() {
        BasicEvent.Super.constructor.apply(this, arguments);
    }
    BasicEvent.Extends(Event);

    BasicEvent.prototype.type = function() {
        return Config.Types.BASIC_EVENT;
    }

    /*
     *  Multi Event
     */
    function MultiEvent() {
        MultiEvent.Super.constructor.apply(this, arguments);
    }
    MultiEvent.Extends(Event);

    MultiEvent.prototype.type = function() {
        return Config.Types.MULTI_EVENT;
    }

    /*
     *  Undeveloped Event
     */
    function UndevelopedEvent() {
        UndevelopedEvent.Super.constructor.apply(this, arguments);
    }
    UndevelopedEvent.Extends(Event);

    UndevelopedEvent.prototype.type = function() {
       return Config.Types.UNDEVELOPED_EVENT;
    }

    /*
     *  Fault Event
     */
    function FaultEvent() {
        FaultEvent.Super.constructor.apply(this, arguments);
    }
    FaultEvent.Extends(Event);

    FaultEvent.prototype.type = function() {
       return Config.Types.FAULT_EVENT;
    }

    /*
     *  AndGate
     */
    function AndGate() {
        AndGate.Super.constructor.apply(this, arguments);
    } 
    AndGate.Extends(Gate);

    AndGate.prototype.type = function() {
       return Config.Types.AND_GATE;
    }

    /*
     *  OrGate
     */
    function OrGate() {
        OrGate.Super.constructor.apply(this, arguments);
    } 
    OrGate.Extends(Gate);

    OrGate.prototype.type = function() {
        return Config.Types.OR_GATE;
    }

    /*
     *  XorGate
     */
    function XorGate() {
        XorGate.Super.constructor.apply(this, arguments);
    } 
    XorGate.Extends(Gate);

    XorGate.prototype.type = function() {
        return Config.Types.XOR_GATE;
    }

    /*
     *  PriorityAndGate
     */
    function PriorityAndGate() {
        PriorityAndGate.Super.constructor.apply(this, arguments);
    } 
    PriorityAndGate.Extends(Gate);

    PriorityAndGate.prototype.type = function() {
        return Config.Types.PRIORITY_AND_GATE;
    }

    /*
     *  VotingOrGate
     */
    function VotingOrGate() {
        VotingOrGate.Super.constructor.apply(this, arguments);
    } 
    VotingOrGate.Extends(Gate);

    VotingOrGate.prototype.type = function() {
        return Config.Types.VOTING_OR_GATE;
    }

    /*
     *  InhibitGate
     */
    function InhibitGate() {
        InhibitGate.Super.constructor.apply(this, arguments);
    } 
    InhibitGate.Extends(Gate);

    InhibitGate.prototype.type = function() {
        return Config.Types.INHIBIT_GATE;
    }

    /*
     *  ChoiceEvent
     */
    function ChoiceEvent() {
        ChoiceEvent.Super.constructor.apply(this, arguments);
    } 
    ChoiceEvent.Extends(Event);

    ChoiceEvent.prototype.type = function() {
        return Config.Types.CHOICE_EVENT;
    }

    /*
     *  RedundancyEvent
     */
    function RedundancyEvent() {
        RedundancyEvent.Super.constructor.apply(this, arguments);
    } 
    RedundancyEvent.Extends(Event);

    RedundancyEvent.prototype.type = function() {
        return Config.Types.REDUNDANCY_EVENT;
    }

    /*
     *  House Event
     */
    function HouseEvent() {
        HouseEvent.Super.constructor.apply(this, arguments);
    }
    HouseEvent.Extends(Event);

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