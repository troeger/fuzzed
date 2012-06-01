define(['require-config', 'require-properties', 'require-oop'], function(Config, Properties) {

    /*
     *  Abstract Node Base Class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;

        // default node configuration
        this._maxInConnections = -1; // infinite
        this._maxOutConnections = 1;

        this._generateId();
        this._locateEditor();
        this._initializeVisualRepresentation();
        this._initializeProperties();
    }

    Node.prototype.appendTo = function(domElement) {
        // some visual stuff, interaction and endpoints need to go here since they require the elements to be
        // already in the DOM. This is why we cannot initialize all of it already in the constructor
        this._container.appendTo(domElement);

        this._resizeOnDrop();
        this._initializeEndpoints();
        this._makeInteractive();

        return this;
    }

    Node.prototype.deselect = function() {
        this._nodeImage.find('path').css('stroke', Config.Node.STROKE_NORMAL);
        return this;
    }

    Node.prototype.id = function() {
        return this._id;
    }

    Node.prototype.moveTo = function(x, y) {
        this._container.css({
            left: x || 0,
            top:  y || 0
        });

        return this;
    }

    Node.prototype.remove = function() {
        jsPlumb.deleteEndpoint(this._sourceEndpoint);
        jsPlumb.deleteEndpoint(this._targetEndpoint);
        this._container.remove();
    }

    Node.prototype.select = function() {
        this._nodeImage.find('path').css('stroke', Config.Node.STROKE_SELECTED);
        _.each(this._properties, function(property) {
            property.show();
        });
        return this;
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
        this._container = jQuery('<div>');
        this._nodeImage = jQuery('#' + Config.IDs.SHAPES_MENU + ' #' + this.type()).clone();

        this._container
            .attr('id', this._nodeImage.attr('id') + this._id)
            .addClass(Config.Classes.NODE)
            .css('position', 'absolute');

        this._nodeImage
            // cleanup the thumbnail's specific properties
            .removeClass('ui-draggable')
            .removeClass(Config.Classes.NODE_THUMBNAIL)
            .removeAttr('id')
            // add new stuff
            .addClass(Config.Classes.NODE_IMAGE)
            .appendTo(this._container);

        // give visual representation a back-link to this object
        this._container.data(Config.Keys.NODE, this);
    }

    Node.prototype._resizeOnDrop = function() {
        // find the nodes
        var image = this._nodeImage;
        var svg   = image.children('svg');
        var g     = svg.children('g');

        // calculate the scale factor
        var marginOffset = image.outerWidth(true) - image.width();
        var scaleFactor  = (Config.Grid.SIZE - marginOffset) / svg.height();

        // resize the svg and its elements
        svg.width(svg.width() * scaleFactor);
        svg.height(svg.height() * scaleFactor);
        g.attr('transform', 'scale(' + scaleFactor + ') ' + g.attr('transform'));
    }

    Node.prototype._initializeEndpoints = function() {
        var imageTopOffset = this._nodeImage.offset().top - this._container.offset().top;
        var imageBottomOffset = imageTopOffset + this._nodeImage.height();

        if (this._maxInConnections != 0) {
            this._sourceEndpoint = jsPlumb.addEndpoint(this._container, {
                anchor:   [ 0.5, 0, 0, 1, 0, imageBottomOffset],
                isSource: true,
                isTarget: false,
                maxConnections: this._maxInConnections
            });
        }

        if (this._maxOutConnections != 0) {
            this._targetEndpoint = jsPlumb.addEndpoint(this._container, {
                anchor:   [ 0.5, 0, 0, -1, 0, imageTopOffset],
                isSource: false,
                isTarget: true,
                maxConnections: this._maxOutConnections
            });
        }
    }

    Node.prototype._makeInteractive = function() {
        var _this = this;

        // make the node draggable
        jsPlumb.draggable(this._container, {
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
        this._container.hover(
            function() {
                if (!_this._editor.isSelected(_this)) {
                    _this._nodeImage.find('path').css('stroke', Config.Node.STROKE_HOVER);
                }
            },
            function() {
                if (!_this._editor.isSelected(_this)) {
                    _this._nodeImage.find('path').css('stroke', Config.Node.STROKE_NORMAL);
                }
            }
        );

        // clicking on a node
        this._container.click(
            function(eventObject) {
                eventObject.stopPropagation();
                _this._editor.selection(_this);
            }
        );
    }

    Node.prototype._initializeProperties = function() {
        this._properties = [];
    }

    /*
     *  Abstract Event Base Class
     */
    function Event() {
        if (this.constructor === Event) return;
        Event.Super.constructor.apply(this, arguments);

        this._maxOutConnections = -1;
        this._maxInConnections  =  1;
    }
    Event.Extends(Node);

    Event.prototype._initializeVisualRepresentation = function() {
        Event.Super._initializeVisualRepresentation.call(this);

        // add label for events
        jQuery('<span>Event</span>')
            .addClass(Config.Classes.NODE_LABEL)
            .appendTo(this._container);
    }

    Event.prototype._initializeProperties = function() {
        Event.Super._initializeProperties.call(this);

        this._properties = _.union(this._properties, [
            new Properties.Text(this, {
                name:  'Name',
                value: 'Event',
                label: true
            }),
            new Properties.Text(this, {
                name:  'Probability',
                value: '0' 
            }),
        ]);
    }

    /*
     *  Abstract Gate Base Class
     */
    function Gate() {
        if (this.constructor === Gate) return;
        Gate.Super.constructor.apply(this, arguments);

        this._maxOutConnections = 1;
        this._maxInConnections = -1;
    }
    Gate.Extends(Node);

    /*
     *  Basic Event
     */
    function BasicEvent() {
        BasicEvent.Super.constructor.apply(this, arguments);

        // no incoming connections allowed
        this._maxInConnections = 0;
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