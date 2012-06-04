define(['require-config', 'require-properties', 'require-oop'], function(Config, Properties) {

    /*
     *  Abstract Node Base Class
     */
    function Node() {
        // pass here on inheritance calls
        if (this.constructor === Node) return;

        // endpoints (default configuration)
        this._maxInConnections  = this._maxInConnections  == undefined ? -1 : this._maxInConnections; // infinite
        this._maxOutConnections = this._maxOutConnections == undefined ?  1 : this._maxOutConnections;

        // logic
        this._editor     = jQuery('#' + Config.IDs.CANVAS).data(Config.Keys.EDITOR);
        this._id         = this._generateId();

        // visuals
        var visuals            = this._setupVisualRepresentation();
        this._container        = visuals.container;
        this._nodeImage        = visuals.nodeImage;
        this._connectionHandle = visuals.connectionHandle;

        // properties
        this._properties       = this._defineProperties();
    }

    Node.prototype.addLabel = function(element) {
        element
            .addClass(Config.Classes.NODE_LABEL)
            .width(Config.Grid.SIZE)
            .appendTo(this._container);
    }

    Node.prototype.appendTo = function(domElement) {
        // some visual stuff, interaction and endpoints need to go here since they require the elements to be
        // already in the DOM. This is why we cannot initialize all of it already in the constructor
        this._container.appendTo(domElement);

        this._resize();
        this._setupEndpoints();
        this._setupDragging();
        this._setupMouse();

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

    Node.prototype.properties = function() {
        return this._properties;
    }

    Node.prototype.remove = function() {
        _.each(jsPlumb.getEndpoints(this._container), function(endpoint) {
            jsPlumb.deleteEndpoint(endpoint);
        })
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
        var image = this._container.children('.' + Config.Classes.NODE_IMAGE);
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

        jsPlumb.draggable(this._container, {
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
        // get upper and lower image offsets
        var imageTopOffset    = this._nodeImage.offset().top - this._container.offset().top;
        var imageBottomOffset = imageTopOffset + this._nodeImage.height();

        // make node source
        if (this._maxInConnections != 0) {
            //TODO: we can use an halo icon instead later
            jsPlumb.makeSource(this._connectionHandle, {
                parent: this._container,
                anchor:   [ 0.5, 0, 0, 1, 0, imageBottomOffset],
                maxConnections: this._maxInConnections
            });
        }

        // make node target
        var targetNode = this;
        if (this._maxOutConnections != 0) {
            jsPlumb.makeTarget(this._container, {
                anchor:         [ 0.5, 0, 0, -1, 0, imageTopOffset],
                maxConnections: this._maxOutConnections,
                dropOptions: {
                    accept: function(draggable) {
                        var elid = draggable.attr('elid');
                        if (typeof elid === 'undefined') return false;

                        // this is not a connection-dragging-scenario
                        var sourceNode = jQuery('.' + Config.Classes.NODE + ':has(#' + elid + ')').data('node');
                        if (typeof sourceNode === 'undefined') return false;

                        // no connections to same node
                        if (targetNode == sourceNode) return false;

                        if (targetNode instanceof Gate && sourceNode instanceof Gate) return false;
                        if (targetNode instanceof Event && sourceNode instanceof Event) return false;

                        // there is already a connection between these nodes
                        var connections = jsPlumb.getConnections({
                            //XXX: the selector should suffice, but due to a bug in jsPlumb we need the IDs here
                            source: sourceNode._container.attr('id'),
                            target: targetNode._container.attr('id')
                        });
                        if (connections.length != 0) return false;

                        // no connection if endpoint is full
                        var endpoints = jsPlumb.getEndpoints(targetNode._container);
                        if (endpoints) {
                            //XXX: find a better way to determine endpoint
                            var targetEndpoint = _.find(endpoints, function(endpoint){
                                return endpoint.isTarget || endpoint._makeTargetCreator
                            });
                            if (targetEndpoint && targetEndpoint.isFull()) return false;
                        }

                        //TODO: type-dependent checks

                        return true;
                    },
                    activeClass: Config.Classes.NODE_DROP_ACTIVE
                }
            });
        }
    }

    Node.prototype._setupMouse = function() {
        var _this = this;

        // click on the node
        this._container.click(
            function(eventObject) {
                eventObject.stopPropagation();
                _this._editor.selection.of(_this);
            }
        );

        // hovering over a node
        this._container.hover(
            function() {
                if (!_this._editor.selection.contains(_this)) {
                    _this._container.find('path').css('stroke', Config.Node.STROKE_HOVER);
                }
            },
            function() {
                if (!_this._editor.selection.contains(_this)) {
                    _this._container.find('path').css('stroke', Config.Node.STROKE_NORMAL);
                }
            }
        );
    }

    Node.prototype._setupVisualRepresentation = function() {
        // get the thumbnail, clone it and wrap it with a container (for labels)
        var container = jQuery('<div>');
        var nodeImage = jQuery('#' + Config.IDs.SHAPES_MENU + ' #' + this.type()).clone();

        container
            .attr('id', nodeImage.attr('id') + this._id)
            .addClass(Config.Classes.NODE)
            .css('position', 'absolute')
            .data(Config.Keys.NODE, this);

        nodeImage
            // cleanup the thumbnail's specific properties
            .removeClass('ui-draggable')
            .removeClass(Config.Classes.NODE_THUMBNAIL)
            .removeAttr('id')
            // add new classes for the actual node
            .addClass(Config.Classes.NODE_IMAGE)
            .appendTo(container);

        if (this._maxInConnections != 0) {
            var connectionHandle = jQuery('<span></span>')
                .addClass(Config.Classes.NODE_HALO_CONNECT)
                .appendTo(container);
        }

        return {
            container:        container,
            nodeImage:        nodeImage,
            connectionHandle: connectionHandle
        };
    }

    /*
     *  Abstract Event Base Class
     */
    function Event() {
        if (this.constructor === Event) return;
        this._maxInConnections  = this._maxInConnections  == undefined ?  1 : this._maxInConnections;
        this._maxOutConnections = this._maxOutConnections == undefined ? -1 : this._maxOutConnections;

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
                type:  'number',
                min:   0,
                max:   1,
                step:  0.01,
                value: 0
            }),
            new Properties.Text(this, {
                name:  'Cost',
                type:  'number',
                value: 1
            }),
        ];
    }

    /*
     *  Abstract Gate Base Class
     */
    function Gate() {
        if (this.constructor === Gate) return;

        this._maxInConnections  = this._maxInConnections  == undefined ? -1 : this._maxInConnections;
        this._maxOutConnections = this._maxOutConnections == undefined ?  1 : this._maxOutConnections;

        Gate.Super.constructor.apply(this, arguments);
    }
    Gate.Extends(Node);

    /*
     *  Basic Event
     */
    function BasicEvent() {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

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
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

        MultiEvent.Super.constructor.apply(this, arguments);
    }
    MultiEvent.Extends(Event);

    MultiEvent.prototype.type = function() {
        return Config.Types.MULTI_EVENT;
    }

    MultiEvent.prototype._defineProperties = function() {
        var properties = MultiEvent.Super._defineProperties.call(this);
        properties.splice(1, 0, new Properties.Text(this, {
            name:  'Cardinality',
            type:  'number',
            value: 1,
            min:   1,
            step:  1
        }));

        return properties;
    }

    /*
     *  Undeveloped Event
     */
    function UndevelopedEvent() {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

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

    ChoiceEvent.prototype._defineProperties = function() {
        var properties = ChoiceEvent.Super._defineProperties.call(this);
        properties.splice(1, 0, new Properties.Text(this, {
            name:  'Cardinality',
            type:  'number',
            value: 1,
            min:   1,
            step:  1
        }));

        return properties;
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

    RedundancyEvent.prototype._defineProperties = function() {
        var properties = RedundancyEvent.Super._defineProperties.call(this);
        properties.splice(1, 0, new Properties.Text(this, {
            name:  'Cardinality',
            type:  'number',
            value: 1,
            min:   1,
            step:  1
        }));

        return properties;
    }

    /*
     *  House Event
     */
    function HouseEvent() {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

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