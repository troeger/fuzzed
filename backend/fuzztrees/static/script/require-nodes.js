define(['require-config', 'require-properties', 'require-backend', 'require-oop'], function(Config, Properties, Backend) {

    /*
     *  Abstract Node Base Class
     */
    function Node(properties) {
        // pass here on inheritance calls
        if (this.constructor === Node) return;
        properties = jQuery.extend({}, properties);

        // endpoints (default configuration)
        this._maxInConnections  = typeof this._maxInConnections  === 'undefined' ? -1 : this._maxInConnections; // infinite
        this._maxOutConnections = typeof this._maxOutConnections === 'undefined' ?  1 : this._maxOutConnections;
        // connector (default configuration)
        this._connectorStyle = typeof this._connectorStyle === 'undefined' ? {} : this._connectorStyle;
        jsPlumb.extend(this._connectorStyle, jsPlumb.Defaults.PaintStyle);

        // logic
        this._editor     = undefined; // will be set when appending
        this._graph      = undefined; // will be set as soon as it get added to a concrete graph
        this._id         = properties.id || new Date().getTime();
        this._optional   = properties.Optional === 'yes' ? true : false;

        // state
        this._disabled    = false;
        this._highlighted = false;
        this._selected    = false;

        // visuals
        var visuals             = this._setupVisualRepresentation();
        this._container         = visuals.container;
        this._nodeImage         = visuals.nodeImage;
        this._connectionHandle  = visuals.connectionHandle;
        this._optionalIndicator = visuals.optionalIndicator;

        // properties
        this._properties = this._defineProperties(properties);
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

    Node.prototype.container = function() {
        return this._container;
    }

    Node.prototype.deselect = function() {
        this._selected = false;

        if (this._highlighted) {
            this._nodeImage.find('path').css('stroke', Config.Node.STROKE_HIGHLIGHTED);
            this._optionalIndicator.attr('stroke', Config.Node.STROKE_HIGHLIGHTED);
            if (!this._optional) {
                this._optionalIndicator.attr('fill', Config.Node.STROKE_HIGHLIGHTED);
            }
        } else {
            this._nodeImage.find('path').css('stroke', Config.Node.STROKE_NORMAL);
            this._optionalIndicator.attr('stroke', Config.Node.STROKE_NORMAL);
            if (!this._optional) {
                this._optionalIndicator.attr('fill', Config.Node.STROKE_NORMAL);
            }
        }

        return this;
    }

    Node.prototype.disable = function() {
        this._disabled = true;
        this._container.find('path').css('stroke', Config.Node.STROKE_DISABLED);
        this._optionalIndicator.attr('stroke', Config.Node.STROKE_DISABLED);
        if (!this._optional) {
            this._optionalIndicator.attr('fill', Config.Node.STROKE_DISABLED);
        }

        return this;
    }

    Node.prototype.enable = function() {
        this._disabled = false;

        if (this._selected) {
            this._container.find('path').css('stroke', Config.Node.STROKE_SELECTED);
            this._optionalIndicator.attr('stroke', Config.Node.STROKE_SELECTED);
            if (!this._optional) {
                this._optionalIndicator.attr('fill', Config.Node.STROKE_SELECTED);
            }
        } else if (this._highlighted) {
            this._container.find('path').css('stroke', Config.Node.STROKE_HIGHLIGHTED);
            this._optionalIndicator.attr('stroke', Config.Node.STROKE_HIGHLIGHTED);
            if (!this._optional) {
                this._optionalIndicator.attr('fill', Config.Node.STROKE_HIGHLIGHTED);
            }
        } else {
            this._container.find('path').css('stroke', Config.Node.STROKE_NORMAL);
            this._optionalIndicator.attr('stroke', Config.Node.STROKE_NORMAL);
            if (!this._optional) {
                this._optionalIndicator.attr('fill', Config.Node.STROKE_NORMAL);
            }
        }

        return this;
    }

    Node.prototype.graph = function(newGraph) {
        if (typeof newGraph === 'undefined') return this._graph;

        this._graph = newGraph;
        return this;
    }

    Node.prototype.highlight = function(highlight) {
        this._highlighted = typeof highlight === 'undefined' ? true : highlight;
        // don't highlight selected or disabled nodes (visually)
        if (this._selected || this._disabled) return this;

        if (this._highlighted) {
            this._container.find('path').css('stroke', Config.Node.STROKE_HIGHLIGHTED);
            this._optionalIndicator.attr('stroke', Config.Node.STROKE_HIGHLIGHTED);
            if (!this._optional) {
                this._optionalIndicator.attr('fill', Config.Node.STROKE_HIGHLIGHTED);
            }
        } else {
            this._container.find('path').css('stroke', Config.Node.STROKE_NORMAL);
            this._optionalIndicator.attr('stroke', Config.Node.STROKE_NORMAL);
            if (!this._optional) {
                this._optionalIndicator.attr('fill', Config.Node.STROKE_NORMAL);
            }
        }

        return this;
    }

    Node.prototype.id = function(newId) {
        if (typeof newId === 'undefined') return this._id;

        this._id = newId;
        return this;
    }

    Node.prototype.moveTo = function(x, y) {
        var image = this._nodeImage;
        var offsetX = image.position().left + image.outerWidth(true) / 2;
        var offsetY = image.position().top  + image.outerHeight(true) / 2;

        this._container.css({
            left: x - offsetX || 0,
            top:  y - offsetY || 0
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
        this._optionalIndicator.attr('stroke', Config.Node.STROKE_SELECTED);
        if (!this._optional) {
            this._optionalIndicator.attr('fill', Config.Node.STROKE_SELECTED);
        }

        return this;
    }

    Node.prototype.setOptional = function(optional) {
        this._optional = optional;

        if (optional) {
            this._optionalIndicator.attr('fill', Config.Node.OPTIONAL_INDICATOR_FILL);
        } else if (this._highlighted) {
            this._optionalIndicator.attr('fill', Config.Node.STROKE_HIGHLIGHTED);
        } else {
            this._optionalIndicator.attr('fill', Config.Node.STROKE_NORMAL);
        }
    }

    Node.prototype.type = function() {
        throw 'Abstract Method - override type in subclass';
    }

    Node.prototype._defineProperties = function(properties) {
        // the basic node does not have any properties therefore the empty array
        // overwrite in subclasses in order to set any
        return [];
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
        jsPlumb.draggable(this._container, {
            containment: 'parent',
            opacity:     Config.Dragging.OPACITY,
            cursor:      Config.Dragging.CURSOR,
            grid:        [Config.Grid.SIZE, Config.Grid.SIZE],
            stack:       '.' + Config.Classes.NODE,

            // start dragging callback
            start:       function() {
                this._editor.selection.ofNodes(this);
            }.bind(this),

            // stop dragging callback
            stop:        function(eventObject, uiHelpers) {
                var editorOffset = this._editor._canvas.offset();
                var coordinates = this._editor.toGrid({
                    //XXX: find a better way (give node position function...)
                    x: this._nodeImage.offset().left - editorOffset.left,
                    y: this._nodeImage.offset().top - editorOffset.top
                });
                Backend.moveNode(this, coordinates);
            }.bind(this)
        });
    }

    Node.prototype._setupEndpoints = function() {
        // get upper and lower image offsets
        var optionalIndicatorWrapper = jQuery(this._optionalIndicator._container);
        var imageTopOffset    = optionalIndicatorWrapper.offset().top - this._container.offset().top;
        var imageBottomOffset = this._nodeImage.offset().top - this._container.offset().top + this._nodeImage.height();

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
        // click on the node
        this._container.click(function(eventObject) {
                eventObject.stopPropagation();
                this._editor.selection.ofNodes(this);
        }.bind(this));

        // hovering over a node
        this._container.hover(
            // mouse in
            function() {
                this.highlight();
            }.bind(this),

            // mouse out
            function() {
                this.highlight(false);
            }.bind(this)
        );
    }

    Node.prototype._setupVisualRepresentation = function() {
        // get the thumbnail, clone it and wrap it with a container (for labels)
        var container = jQuery('<div>');
        var nodeImage = jQuery('#' + Config.IDs.SHAPES_MENU + ' #' + this.type()).clone();
        var optionalIndicatorWrapper = jQuery('<div>').svg();
        var optionalIndicator = optionalIndicatorWrapper.svg('get');

        container
            .attr('id', nodeImage.attr('id') + this._id)
            .addClass(Config.Classes.NODE)
            .css('position', 'absolute')
            .data(Config.Keys.NODE, this);

        //TODO: config
        var radius = Config.Node.OPTIONAL_INDICATOR_RADIUS;
        var optionalIndicatorCircle = optionalIndicator.circle(null, radius+1, radius+1, radius, {
            strokeWidth: 2,
            fill: this._optional ? Config.Node.OPTIONAL_INDICATOR_FILL : Config.Node.STROKE_NORMAL,
            stroke: Config.Node.STROKE_NORMAL
        });

        // external method for changing attributes of the circle later
        optionalIndicator.attr = function(attr, value) {
            var setting = {}
            setting[attr] = value;
            optionalIndicator.change(optionalIndicatorCircle, setting);
        };

        optionalIndicatorWrapper
            .addClass(Config.Classes.NODE_OPTIONAL_INDICATOR)
            .appendTo(container);

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
            container:         container,
            nodeImage:         nodeImage,
            connectionHandle:  connectionHandle,
            optionalIndicator: optionalIndicator
        };
    }

    /*
     *  Abstract Event Base Class
     */
    function Event(properties) {
        if (this.constructor === Event) return;
        this._maxInConnections  = this._maxInConnections  == undefined ?  1 : this._maxInConnections;
        this._maxOutConnections = this._maxOutConnections == undefined ? -1 : this._maxOutConnections;

        Event.Super.constructor.call(this, properties);
    }
    Event.Extends(Node);

    Event.prototype.allowsConnectionsTo = function(otherNode) {
        // no connections between Event nodes
        if (otherNode instanceof Event) return false;
        return Event.Super.allowsConnectionsTo.call(this, otherNode);
    }

    Event.prototype._defineProperties = function(properties) {
        return [
            new Properties.Text({
                name:   'Name',
                value:  properties.Name || this.name(),
                mirror: this._container
            }, this),

            new Properties.Text({
                name:     'Cost',
                value:    properties.Cost || 1,
                disabled: true
            }, this),

            new Properties.Text({
                name:         'Probability',
                mirror:       this._container,
                mirrorPrefix: 'p=',
                mirrorClass:  Config.Classes.PROPERTY_LABEL_PROBABILITY,
                value:        properties.Probability || 0,
                disabled:     true
            }, this),

            new Properties.Radio({
                name:     'Optional',
                options:  [
                    'no',
                    'yes'
                ],
                value:    properties.Optional || 'no',
                change:   function() {
                    this.setOptional(!this._optional);
                }.bind(this)
            }, this)
        ];
    }

    /*
     *  Abstract Gate Base Class
     */
    function Gate(properties) {
        if (this.constructor === Gate) return;

        this._maxInConnections  = this._maxInConnections  == undefined ? -1 : this._maxInConnections;
        this._maxOutConnections = this._maxOutConnections == undefined ?  1 : this._maxOutConnections;

        Gate.Super.constructor.call(this, properties);
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
    function BasicEvent(properties) {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;
        BasicEvent.Super.constructor.call(this, properties);
    }
    BasicEvent.Extends(Event);

    BasicEvent.prototype.name = function() {
        return Config.Node.Names.BASIC_EVENT;
    }

    BasicEvent.prototype.type = function() {
        return Config.Node.Types.BASIC_EVENT;
    }

    BasicEvent.prototype._defineProperties = function(properties) {
        var probability   = parseFloat(properties.Probability);
        var exactSelected = typeof properties.Probability === 'undefined' || !isNaN(probability);

        return [
            new Properties.Text({
                name:   'Name',
                value:  properties.Name || this.name(),
                mirror: this._container
            }, this),

            new Properties.Text({
                name:  'Cost',
                type:  'number',
                value: properties.Cost || 1
            }, this),

            new Properties.SingleChoice({
                name:        'Probability',
                mirror:       this._container,
                mirrorPrefix: 'p=',
                mirrorClass:  Config.Classes.PROPERTY_LABEL_PROBABILITY,

                choices: [{
                    name:     'Exact',
                    selected:  exactSelected,
                    input: new Properties.Text({
                        type:  'number',
                        min:   0,
                        max:   1,
                        step:  0.01,
                        value: exactSelected ? probability : 0
                    }, this)
                }, {
                    name:     'Fuzzy',
                    selected: !exactSelected,
                    input: new Properties.Select({
                        options: [
                            'very',
                            'more or less',
                            'slightly',
                            'very likely',
                            'highly'
                        ],
                        value: !exactSelected ? properties.Probability : 'very'
                    }, this)
                }]
            }, this),

            new Properties.Radio({
                name:     'Optional',
                options:  [
                    'no',
                    'yes'
                ],
                value:    properties.Optional || 'no',
                change:   function() {
                    this.setOptional(!this._optional);
                }.bind(this)
            }, this)
        ];
    }

    /*
     *  Basic Event Set
     */
    function BasicEventSet(properties) {
        BasicEventSet.Super.constructor.call(this, properties);
    }
    BasicEventSet.Extends(BasicEvent);

    BasicEventSet.prototype.name = function() {
        return Config.Node.Names.BASIC_EVENT_SET;
    }

    BasicEventSet.prototype.type = function() {
        return Config.Node.Types.BASIC_EVENT_SET;
    }

    BasicEventSet.prototype._defineProperties = function(properties) {
        var parentProperties = BasicEventSet.Super._defineProperties.call(this, properties);

        parentProperties.splice(-2, 0,
            new Properties.Text({
                name:         'Cardinality',
                type:         'number',
                value:        properties.Cardinality || 1,
                min:          1,
                step:         1,
                mirror:       this._container,
                mirrorPrefix: '#',
                mirrorClass:  Config.Classes.PROPERTY_LABEL_PROBABILITY
            }, this)
        );

        return parentProperties;
    }

    /*
     *  Intermediate Event
     */
    function IntermediateEvent(properties) {
        IntermediateEvent.Super.constructor.call(this, properties);
    }
    IntermediateEvent.Extends(Event);

    IntermediateEvent.prototype.name = function() {
        return Config.Node.Names.INTERMEDIATE_EVENT;
    }

    IntermediateEvent.prototype.type = function() {
       return Config.Node.Types.INTERMEDIATE_EVENT;
    }

    /*
     *  Intermediate Event Set
     */
    function IntermediateEventSet(properties) {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

        IntermediateEventSet.Super.constructor.call(this, properties);
    }
    IntermediateEventSet.Extends(IntermediateEvent);

    IntermediateEventSet.prototype.name = function() {
        return Config.Node.Names.INTERMEDIATE_EVENT_SET;
    }

    IntermediateEventSet.prototype.type = function() {
       return Config.Node.Types.INTERMEDIATE_EVENT_SET;
    }

    IntermediateEventSet.prototype._defineProperties = function(properties) {
        var parentProperties = IntermediateEventSet.Super._defineProperties.call(this, properties);

        parentProperties.push(new Properties.Text({
            name:         'Cardinality',
            type:         'number',
            value:        properties.Cardinality || 1,
            min:          1,
            step:         1,
            mirror:       this._container,
            mirrorPrefix: '#',
            mirrorClass:  Config.Classes.PROPERTY_LABEL_PROBABILITY
        }, this));

        return parentProperties;
    }

    /*
     *  AndGate
     */
    function AndGate(properties) {
        AndGate.Super.constructor.call(this, properties);
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
    function OrGate(properties) {
        OrGate.Super.constructor.call(this, properties);
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
    function XorGate(properties) {
        XorGate.Super.constructor.call(this, properties);
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
    function PriorityAndGate(properties) {
        PriorityAndGate.Super.constructor.call(this, properties);
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
    function VotingOrGate(properties) {
        VotingOrGate.Super.constructor.call(this, properties);
    } 
    VotingOrGate.Extends(Gate);

    VotingOrGate.prototype.name = function() {
        return Config.Node.Names.VOTING_OR_GATE;
    }

    VotingOrGate.prototype.type = function() {
        return Config.Node.Types.VOTING_OR_GATE;
    }

    VotingOrGate.prototype._defineProperties = function(properties) {
        return [
            new Properties.Text({
                name:         'Count',
                type:         'number',
                value:        properties.Count || 1,
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
    function InhibitGate(properties) {
        InhibitGate.Super.constructor.call(this, properties);
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
    function ChoiceEvent(properties) {
        // outgoing connections are dashed
        this._connectorStyle = typeof this._connectorStyle === 'undefined' ? {} : this._connectorStyle;
        this._connectorStyle = jsPlumb.extend({ dashstyle: "4 2"}, this._connectorStyle);

        ChoiceEvent.Super.constructor.call(this, properties);
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

    /*
     *  RedundancyEvent
     */
    function RedundancyEvent(properties) {
        // outgoing connections are dashed
        this._connectorStyle = typeof this._connectorStyle === 'undefined' ? {} : this._connectorStyle;
        this._connectorStyle = jsPlumb.extend({ dashstyle: "4 2"}, this._connectorStyle);

        RedundancyEvent.Super.constructor.call(this, properties);
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

    RedundancyEvent.prototype._defineProperties = function(properties) {
        var parentProperties = RedundancyEvent.Super._defineProperties.call(this, properties);

        parentProperties.push(new Properties.Text({
            name:         'Cardinality',
            type:         'number',
            value:        parseInt(properties.Cardinality) || 1,
            min:          1,
            step:         1,
            mirror:       this._container,
            mirrorPrefix: 'k=',
            mirrorClass:  Config.Classes.PROPERTY_LABEL_PROBABILITY
        }, this));

        return parentProperties;
    }

    /*
     *  Undeveloped Event
     */
    function UndevelopedEvent(properties) {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

        UndevelopedEvent.Super.constructor.call(this, properties);
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
    function HouseEvent(properties) {
        // no incoming connections allowed
        this._maxInConnections = this._maxInConnections == undefined ? 0 : this._maxInConnections;

        HouseEvent.Super.constructor.call(this, properties);
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
    function newNodeForType(type, properties) {
        switch(type) {
            case Config.Node.Types.BASIC_EVENT:
                return new BasicEvent(properties);
            case Config.Node.Types.BASIC_EVENT_SET:
                return new BasicEventSet(properties);
            case Config.Node.Types.INTERMEDIATE_EVENT:
                return new IntermediateEvent(properties);
            case Config.Node.Types.INTERMEDIATE_EVENT_SET:
                return new IntermediateEventSet(properties);
            case Config.Node.Types.AND_GATE:
                return new AndGate(properties);
            case Config.Node.Types.PRIORITY_AND_GATE:
                return new PriorityAndGate(properties);
            case Config.Node.Types.OR_GATE:
                return new OrGate(properties);
            case Config.Node.Types.XOR_GATE:
                return new XorGate(properties);
            case Config.Node.Types.VOTING_OR_GATE:
                return new VotingOrGate(properties);
            case Config.Node.Types.INHIBIT_GATE:
                return new InhibitGate(properties);
            case Config.Node.Types.CHOICE_EVENT:
                return new ChoiceEvent(properties);
            case Config.Node.Types.REDUNDANCY_EVENT:
                return new RedundancyEvent(properties);
            case Config.Node.Types.UNDEVELOPED_EVENT:
                return new UndevelopedEvent(properties);
            case Config.Node.Types.HOUSE_EVENT:
                return new HouseEvent(properties);
        }
    }

    /*
     *  Return the collection of all nodes for require
     */
    return {
        // classes
        BasicEvent:       BasicEvent,
        BasicEventSet:    BasicEventSet,
        UndevelopedEvent: UndevelopedEvent,
        IntermediateEvent:IntermediateEvent,
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