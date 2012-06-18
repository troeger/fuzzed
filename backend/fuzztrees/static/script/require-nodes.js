define(['require-config', 'require-properties', 'require-oop'], function(Config, Properties) {

    /*
     *  Abstract Node Base Class
     */
    function Node(id) {
        // pass here on inheritance calls
        if (this.constructor === Node) return;

        // endpoints (default configuration)
        this._maxInConnections  = typeof this._maxInConnections  === 'undefined' ? -1 : this._maxInConnections; // infinite
        this._maxOutConnections = typeof this._maxOutConnections === 'undefined' ?  1 : this._maxOutConnections;
        // connector (default configuration)
        this._connectorStyle = typeof this._connectorStyle === 'undefined' ? {} : this._connectorStyle;
        jsPlumb.extend(this._connectorStyle, jsPlumb.Defaults.PaintStyle);

        // logic
        this._editor     = undefined; // will be set when appending
        this._graph      = undefined; // will be set when adding to a Graph
        this._id         = id;

        // state
        this._disabled    = false;
        this._highlighted = false;
        this._selected    = false;

        // visuals
        var visuals            = this._setupVisualRepresentation();
        this._container        = visuals.container;
        this._nodeImage        = visuals.nodeImage;
        this._connectionHandle = visuals.connectionHandle;

        // properties
        this._properties       = this._defineProperties();
    }

    Node.prototype.allowsConnectionsTo = function(otherNode) {
        // no connections to same node
        if (this == otherNode) return false;

        // there is already a connection between these nodes
        var connections = jsPlumb.getConnections({
            //XXX: the selector should suffice, but due to a bug in jsPlumb we need the IDs here
            source: this._container.attr('id'),
            target: otherNode._container.attr('id')
        });
        if (connections.length != 0) return false;

        // no connection if endpoint is full
        var endpoints = jsPlumb.getEndpoints(otherNode._container);
        if (endpoints) {
            //XXX: find a better way to determine endpoint
            var targetEndpoint = _.find(endpoints, function(endpoint){
                return endpoint.isTarget || endpoint._makeTargetCreator
            });
            if (targetEndpoint && targetEndpoint.isFull()) return false;
        }

        return true;
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
        this._selected = false;

        if (this._highlighted) {
            this._nodeImage.find('path').css('stroke', Config.Node.STROKE_HIGHLIGHTED);
        } else {
            this._nodeImage.find('path').css('stroke', Config.Node.STROKE_NORMAL);
        }

        return this;
    }

    Node.prototype.disable = function() {
        this._disabled = true;
        this._container.find('path').css('stroke', Config.Node.STROKE_DISABLED);

        return this;
    }

    Node.prototype.enable = function() {
        this._disabled = false;

        if (this._selected) {
            this._container.find('path').css('stroke', Config.Node.STROKE_SELECTED);
        } else if (this._highlighted) {
            this._container.find('path').css('stroke', Config.Node.STROKE_HIGHLIGHTED);
        } else {
            this._container.find('path').css('stroke', Config.Node.STROKE_NORMAL);
        }

        return this;
    }

    Node.prototype.highlight = function(highlight) {
        this._highlighted = typeof highlight === 'undefined' ? true : highlight;
        // don't highlight selected or disabled nodes (visually)
        if (this._selected || this._disabled) return this;

        if (this._highlighted) {
            this._container.find('path').css('stroke', Config.Node.STROKE_HIGHLIGHTED);
        } else {
            this._container.find('path').css('stroke', Config.Node.STROKE_NORMAL);
        }

        return this;
    }

    Node.prototype.id = function(newId) {
        if (typeof newId === 'undefined') return this._id;

        this._id = newId;
        return this;
    }

    Node.prototype.moveTo = function(x, y) {
        this._container.css({
            left: x || 0,
            top:  y || 0
        });

        return this;
    }

    Node.prototype.name = function() {
        throw 'Abstract Method - override name (human readable) in subclass';
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
        // don't allow selection of disabled nodes
        if (this._disabled) return this;

        this._selected = true;
        this._nodeImage.find('path').css('stroke', Config.Node.STROKE_SELECTED);
        
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
                _this._editor.selection.ofNodes(_this);
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
                maxConnections: this._maxInConnections,
                connectorStyle: this._connectorStyle,
                dragOptions: {
                    drag: function() {
                        // disable all nodes that can not be targeted
                        var nodesToDisable = jQuery('.' + Config.Classes.NODE + ':not(.'+ Config.Classes.NODE_DROP_ACTIVE + ')');
                        nodesToDisable.each(function(index, node){
                            jQuery(node).data('node').disable();
                        });
                    },
                    stop: function() {
                        // re-enable disabled nodes
                        var nodesToEnable = jQuery('.' + Config.Classes.NODE + ':not(.'+ Config.Classes.NODE_DROP_ACTIVE + ')');
                        nodesToEnable.each(function(index, node){
                            jQuery(node).data('node').enable();
                        });
                    }
                }
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

                        return sourceNode.allowsConnectionsTo(targetNode);
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
                _this._editor.selection.ofNodes(_this);
            }
        );

        // hovering over a node
        this._container.hover(
            function() {
                _this.highlight();
            },
            function() {
                _this.highlight(false);
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

    Event.prototype.allowsConnectionsTo = function(otherNode) {
        // no connections between Event nodes
        if (otherNode instanceof Event) return false;
        return Event.Super.allowsConnectionsTo.call(this, otherNode);
    }

    Event.prototype._defineProperties = function() {
        return [
            new Properties.Text({
                name:   'Name',
                value:  this.name(),
                mirror: this._container
            }, this),

            new Properties.SingleChoice({
                name:        'Probability',
                mirror:       this._container,
                mirrorPrefix: 'p=',
                mirrorClass:  Config.Classes.PROPERTY_LABEL_PROBABILITY,

                choices: [{
                    name:     'Exact',
                    selected:  true,
                    input: new Properties.Text({
                                type:  'number',
                                min:   0,
                                max:   1,
                                step:  0.01,
                                value: 0,
                        }, this),
                }, {
                    name: 'Fuzzy',
                    input: new Properties.Select({
                        options: [
                                    'very unlikely',
                                    'unlikely',
                                    'likely',
                                    'very likely',
                                    'unknown'
                                ],
                        value:  'unknown',
                    }, this)
                }]
            }),

            new Properties.Text({
                name:  'Cost',
                type:  'number',
                value: 1
            }, this)
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

    Gate.prototype.allowsConnectionsTo = function(otherNode) {
        // no connections between Event nodes
        if (otherNode instanceof Gate) return false;
        return Gate.Super.allowsConnectionsTo.call(this, otherNode);
    }

    /*
     *  Basic Event
     */
    function BasicEvent() {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

        BasicEvent.Super.constructor.apply(this, arguments);
    }
    BasicEvent.Extends(Event);

    BasicEvent.prototype.name = function() {
        return Config.Node.Names.BASIC_EVENT;
    }

    BasicEvent.prototype.type = function() {
        return Config.Node.Types.BASIC_EVENT;
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

    MultiEvent.prototype.name = function() {
        return Config.Node.Names.MULTI_EVENT;
    }

    MultiEvent.prototype.type = function() {
        return Config.Node.Types.MULTI_EVENT;
    }

    MultiEvent.prototype._defineProperties = function() {
        var properties = MultiEvent.Super._defineProperties.call(this);
        properties.splice(1, 0, new Properties.Text({
            name:  'Cardinality',
            type:  'number',
            value: 1,
            min:   1,
            step:  1
        }, this));

        return properties;
    }

    /*
     *  Fault Event
     */
    function FaultEvent() {
        FaultEvent.Super.constructor.apply(this, arguments);
    }
    FaultEvent.Extends(Event);

    FaultEvent.prototype.name = function() {
        return Config.Node.Names.FAULT_EVENT;
    }

    FaultEvent.prototype.type = function() {
       return Config.Node.Types.FAULT_EVENT;
    }

    /*
     *  Fault Event
     */
    function MultiFaultEvent() {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

        MultiEvent.Super.constructor.apply(this, arguments);
    }
    MultiFaultEvent.Extends(Event);

    MultiFaultEvent.prototype.name = function() {
        return Config.Node.Names.MULTI_FAULT_EVENT;
    }

    MultiFaultEvent.prototype.type = function() {
       return Config.Node.Types.MULTI_FAULT_EVENT;
    }

    MultiFaultEvent.prototype._defineProperties = function() {
        var properties = MultiFaultEvent.Super._defineProperties.call(this);
        properties.splice(1, 0, new Properties.Text({
            name:  'Cardinality',
            type:  'number',
            value: 1,
            min:   1,
            step:  1
        }, this));

        return properties;
    }

    /*
     *  AndGate
     */
    function AndGate() {
        AndGate.Super.constructor.apply(this, arguments);
    } 
    AndGate.Extends(Gate);

    AndGate.prototype.name = function() {
        return Config.Node.Names.AND_GATE;
    }

    AndGate.prototype.type = function() {
       return Config.Node.Types.AND_GATE;
    }

    /*
     *  OrGate
     */
    function OrGate() {
        OrGate.Super.constructor.apply(this, arguments);
    } 
    OrGate.Extends(Gate);

    OrGate.prototype.name = function() {
        return Config.Node.Names.OR_GATE;
    }

    OrGate.prototype.type = function() {
        return Config.Node.Types.OR_GATE;
    }

    /*
     *  XorGate
     */
    function XorGate() {
        XorGate.Super.constructor.apply(this, arguments);
    } 
    XorGate.Extends(Gate);

    XorGate.prototype.name = function() {
        return Config.Node.Names.XOR_GATE;
    }

    XorGate.prototype.type = function() {
        return Config.Node.Types.XOR_GATE;
    }

    /*
     *  PriorityAndGate
     */
    function PriorityAndGate() {
        PriorityAndGate.Super.constructor.apply(this, arguments);
    } 
    PriorityAndGate.Extends(Gate);

    PriorityAndGate.prototype.name = function() {
        return Config.Node.Names.PRIORITY_AND_GATE;
    }

    PriorityAndGate.prototype.type = function() {
        return Config.Node.Types.PRIORITY_AND_GATE;
    }

    /*
     *  VotingOrGate
     */
    function VotingOrGate() {
        VotingOrGate.Super.constructor.apply(this, arguments);
    } 
    VotingOrGate.Extends(Gate);

    VotingOrGate.prototype.name = function() {
        return Config.Node.Names.VOTING_OR_GATE;
    }

    VotingOrGate.prototype.type = function() {
        return Config.Node.Types.VOTING_OR_GATE;
    }

    VotingOrGate.prototype._defineProperties = function() {
        return [
            new Properties.Text({
                name:         'Count',
                type:         'number',
                value:        1,
                min:          0,
                mirror:       this._container,
                mirrorPrefix: 'k=',
                mirrorClass:  Config.Classes.PROPERTY_LABEL_PROBABILITY
            }, this)
        ];
    }

    /*
     *  InhibitGate
     */
    function InhibitGate() {
        InhibitGate.Super.constructor.apply(this, arguments);
    } 
    InhibitGate.Extends(Gate);

    InhibitGate.prototype.name = function() {
        return Config.Node.Names.INHIBIT_GATE;
    }

    InhibitGate.prototype.type = function() {
        return Config.Node.Types.INHIBIT_GATE;
    }

    /*
     *  ChoiceEvent
     */
    function ChoiceEvent() {
        // outgoing connections are dashed
        this._connectorStyle = typeof this._connectorStyle === 'undefined' ? {} : this._connectorStyle;
        this._connectorStyle = jsPlumb.extend({ dashstyle: "4 2"}, this._connectorStyle);

        ChoiceEvent.Super.constructor.apply(this, arguments);
    } 
    ChoiceEvent.Extends(Event);

    ChoiceEvent.prototype.name = function() {
        return Config.Node.Names.CHOICE_EVENT;
    }

    ChoiceEvent.prototype.type = function() {
        return Config.Node.Types.CHOICE_EVENT;
    }

    ChoiceEvent.prototype.allowsConnectionsTo = function(otherNode) {
        // no connections to gates
        if (otherNode instanceof Gate) return false;

        // allow connections to other events, but also check basic conditions
        return otherNode instanceof Event && Node.prototype.allowsConnectionsTo.call(this, otherNode);
    }

    ChoiceEvent.prototype._defineProperties = function() {
        var properties = ChoiceEvent.Super._defineProperties.call(this);
        properties.splice(1, 0, new Properties.Text({
            name:  'Cardinality',
            type:  'number',
            value: 1,
            min:   1,
            step:  1
        }, this));

        return properties;
    }

    /*
     *  RedundancyEvent
     */
    function RedundancyEvent() {
        // outgoing connections are dashed
        this._connectorStyle = typeof this._connectorStyle === 'undefined' ? {} : this._connectorStyle;
        this._connectorStyle = jsPlumb.extend({ dashstyle: "4 2"}, this._connectorStyle);

        RedundancyEvent.Super.constructor.apply(this, arguments);
    } 
    RedundancyEvent.Extends(Event);

    RedundancyEvent.prototype.name = function() {
        return Config.Node.Names.REDUNDANCY_EVENT;
    }

    RedundancyEvent.prototype.type = function() {
        return Config.Node.Types.REDUNDANCY_EVENT;
    }

    RedundancyEvent.prototype.allowsConnectionsTo = function(otherNode) {
        // no connections to gates
        if (otherNode instanceof Gate) return false;

        // allow connections to other events, but also check basic conditions
        return otherNode instanceof Event && Node.prototype.allowsConnectionsTo.call(this, otherNode);
    }

    RedundancyEvent.prototype._defineProperties = function() {
        var properties = RedundancyEvent.Super._defineProperties.call(this);
        properties.splice(1, 0, new Properties.Text({
            name:  'Cardinality',
            type:  'number',
            value: 1,
            min:   1,
            step:  1
        }, this));

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

    UndevelopedEvent.prototype.name = function() {
        return Config.Node.Names.UNDEVELOPED_EVENT;
    }

    UndevelopedEvent.prototype.type = function() {
       return Config.Node.Types.UNDEVELOPED_EVENT;
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

    HouseEvent.prototype.name = function() {
        return Config.Node.Names.HOUSE_EVENT;
    }

    HouseEvent.prototype.type = function() {
       return Config.Node.Types.HOUSE_EVENT;
    }

    /*
        Function: newNodeWithType
            Factory method. Returns a new Node of the given type.

        Parameter:
            type - String specifying the type of the new Node. See Config.Node.Types.

        Returns:
            A new Node of the given type
     */
    function newNodeForType(type, id) {
        switch(type) {
            case Config.Node.Types.BASIC_EVENT:
                return new BasicEvent(id);
            case Config.Node.Types.MULTI_EVENT:
                return new MultiEvent(id);
            case Config.Node.Types.FAULT_EVENT:
                return new FaultEvent(id);
            case Config.Node.Types.MULTI_FAULT_EVENT:
                return new MultiFaultEvent(id);
            case Config.Node.Types.AND_GATE:
                return new AndGate(id);
            case Config.Node.Types.PRIORITY_AND_GATE:
                return new PriorityAndGate(id);
            case Config.Node.Types.OR_GATE:
                return new OrGate(id);
            case Config.Node.Types.XOR_GATE:
                return new XorGate(id);
            case Config.Node.Types.VOTING_OR_GATE:
                return new VotingOrGate(id);
            case Config.Node.Types.INHIBIT_GATE:
                return new InhibitGate(id);
            case Config.Node.Types.CHOICE_EVENT:
                return new ChoiceEvent(id);
            case Config.Node.Types.REDUNDANCY_EVENT:
                return new RedundancyEvent(id);
            case Config.Node.Types.UNDEVELOPED_EVENT:
                return new UndevelopedEvent(id);
            case Config.Node.Types.HOUSE_EVENT:
                return new HouseEvent(id);
        }
    }

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
        HouseEvent:       HouseEvent,
        newNodeForType:   newNodeForType
    };
})