define(['require', 'require-config', 'require-nodes', 'require-backend', 
        'require-editor-menus', 'require-editor-selection', 'require-oop'],
    function(require, Config, Nodes, Backend, Menus, Selection, Class) {

    /*
     *  Class: Editor
     */
    var Editor = Class.extend({
        shapes:     undefined,
        properties: undefined,
        selection:  undefined,

        _canvas:     undefined,
        _background: undefined,

        init: function(graphId) {
            // locate predefined DOM elements and bind Editor instance to canvas
            this._canvas     = jQuery('#' + Config.IDs.CANVAS);
            this._background = this._canvas.svg().svg('get');
            this._canvas.data(Config.Keys.EDITOR, this);

            // create manager objects for the bars and the selection
            this.shapes     = new Menus.ShapeMenu();
            this.properties = new Menus.PropertiesMenu();
            this.selection  = new Selection();

            // run a few sub initializer
            this._setupCanvas();
            this._setupBackground();
            this._setupJsPlumb();
            this._setupKeyBindings();
            this._setupAjaxHandler();

            // fetch the content from the backend
            //TODO: init editor with a graph instance instead
            this._loadGraph(graphId);
        },

        /* Section: Accessors */

        graph: function(newGraph) {
            if (typeof newGraph === 'undefined') return this._graph;
            // TODO: on set full rendering of new graph required
            this._graph = newGraph;
            return this;
        },


        /* Section: Coordinate conversion */

        toGrid: function(first, second) {
            var x = Number.NaN;
            var y = Number.NaN;

            // if both parameter are numbers we can take them as they are
            if (_.isNumber(first) && _.isNumber(second)) {
                x = first;
                y = second;

                // however the first parameter could also be an object
                // of the form {x: NUMBER, y: NUMBER} (convenience reasons)
            } else if (_.isObject(first)) {
                x = first.x;
                y = first.y;
            }

            return {
                x: Math.round(x / Config.Grid.SIZE),
                y: Math.round(y / Config.Grid.SIZE)
            }
        },

        toPixel: function(first, second) {
            var x = Number.NaN;
            var y = Number.NaN;

            if (_.isNumber(first) && _.isNumber(second)) {
                x = first;
                y = second;

            } else if (_.isObject(first)) {
                x = first.x;
                y = first.y;
            }

            return {
                x: x * Config.Grid.SIZE,
                y: y * Config.Grid.SIZE
            }
        },


        /* Section: Internals */

        _drawGrid: function() {
            var height = this._canvas.height();
            var width  = this._canvas.width();

            // clear old background and resize svg container to current canvas size
            // important when window was resized in the mean time
            this._background.clear();
            this._background.configure({
                height: height,
                width:  width
            });

            // horizontal lines
            for (var y = Config.Grid.SIZE; y < height; y += Config.Grid.SIZE) {
                this._background.line(0, y, width, y, {
                    stroke:          Config.Grid.STROKE,
                    strokeWidth:     Config.Grid.STROKE_WIDTH,
                    strokeDashArray: Config.Grid.STROKE_STYLE
                });
            }

            // vertical lines
            for (var x = Config.Grid.SIZE; x < width; x += Config.Grid.SIZE) {
                this._background.line(x, 0, x, height, {
                    stroke:          Config.Grid.STROKE,
                    strokeWidth:     Config.Grid.STROKE_WIDTH,
                    strokeDashArray: Config.Grid.STROKE_STYLE
                });
            }
        },

        _edgeConnected: function(edge) {
            var connection = edge.connection;
            connection._fuzzedID = new Date().getTime();
            Backend.addEdge(connection._fuzzedID, edge.source.data(Config.Keys.NODE), edge.target.data(Config.Keys.NODE));
            this.graph().addEdge(edge.connection);
        },

        _edgeDetached: function(edge) {
            var connection = edge.connection;

            this.graph().deleteEdge(connection);
            Backend.deleteEdge(connection);
        },

        _loadGraph: function(graphId) {
            Backend.getGraph(graphId,
                this._loadGraphFromJson.bind(this),
                this._loadGraphError.bind(this)
            );
            return this;
        },

        _loadGraphCompleted: function() {
            this._setupPersistanceEvents();
            jQuery('#' + Config.IDs.SPLASH).fadeOut(Config.Splash.FADE_TIME);
        },

        _loadGraphError: function(graph, response, textStatus, errorThrown) {
            this.graph(graph);
            // TODO: this alert is weird. just do it or 404?
            alert('Could not find your graph in the database');
        },

        _loadGraphFromJson: function(json) {
            function constructGraph(Graph) {
                var graph = new Graph(json.id);
                this.graph(graph);

                //TODO: newFromJson for graph

                // parse the json nodes and convert them to node objects
                _.each(json.nodes, function(jsonNode) {
                    graph.addNode(Nodes.newNodeFromJson(jsonNode));
                });

                // draw the nodes on the canvas
                _.each(graph.getNodes(), function(node, index) {
                    node._editor = this;
                    node.appendTo(this._canvas)
                        .moveTo(node.x, node.y)
                }.bind(this));

                // connect the nodes again
                _.each(json.edges, function(jsonEdge) {
                    var edge = jsPlumb.connect({
                        source: graph.getNodeById(jsonEdge.source).container(),
                        target: graph.getNodeById(jsonEdge.target).container()
                    });
                    edge._fuzzedID = jsonEdge.id;
                    graph.addEdge(edge);
                }.bind(this));

                this._loadGraphCompleted();
            }

            // pick the right graph class depending on the type
            if (json.type == 'fuzztree') {
                require(['require-fuzztree'], constructGraph.bind(this));
            } else if (json.type == 'faulttree') {
                require(['require-faulttree'], constructGraph.bind(this));
            } else if (json.type == 'rbd') {
                require(['require-rbdg'], constructGraph.bind(this));
            } else {
                // TODO: maybe an "unknown graph type"-error here?
                require(['require-graph'], constructGraph.bind(this));
            }
        },

        _setupAjaxHandler: function() {
            jQuery('.fuzzed-ajax-loader').ajaxStart(function() {
                jQuery(this).css('visibility', 'visible');
            });

            jQuery('.fuzzed-ajax-loader').ajaxStop(function() {
                jQuery(this).css('visibility', 'hidden');
            });
        },

        _setupBackground: function() {
            this._drawGrid();
            // clicks on the canvas clear the selection
            this._canvas.click(this.selection.clear.bind(this.selection));
            // redraw the background grid when the window resizes
            jQuery(window).resize(this._drawGrid.bind(this));
        },

        _setupCanvas: function() {
            // make canvas droppable for shapes from the shape menu
            this._canvas.droppable({
                accept:    'svg',
                tolerance: 'fit',
                drop:      this._shapeDropped.bind(this)
            });
        },

        _setupJsPlumb: function() {
            jsPlumb.importDefaults({
                EndpointStyle: {
                    fillStyle:   Config.JSPlumb.ENDPOINT_FILL
                },
                Endpoint:        [Config.JSPlumb.ENDPOINT_STYLE, {
                    radius:      Config.JSPlumb.ENDPOINT_RADIUS,
                    cssClass:    Config.Classes.JSPLUMB_ENDPOINT,
                    hoverClass:  Config.Classes.JSPLUMB_ENDPOINT_HOVER
                }],
                PaintStyle: {
                    strokeStyle: Config.JSPlumb.STROKE,
                    lineWidth:   Config.JSPlumb.STROKE_WIDTH
                },
                HoverPaintStyle: {
                    strokeStyle: Config.JSPlumb.STROKE_HIGHLIGHTED
                },
                Connector:       [Config.JSPlumb.CONNECTOR_STYLE, {stub: Config.JSPlumb.CONNECTOR_STUB}],
                Anchors:         ['BottomMiddle', 'TopMiddle'],
                ConnectionsDetachable: false
            });

            var editor = this;
            // listen for clicks on connections for selections
            jsPlumb.bind('click', function(connection, event) {
                event.stopPropagation();
                editor.selection.ofConnections(connection);
            });
        },

        _setupKeyBindings: function() {
            jQuery(document).keydown(function(eventObject) {
                // hitting delete removes the current selection from the canvas
                if (eventObject.which === jQuery.ui.keyCode.DELETE) {
                    this.selection.remove();

                } else if (eventObject.which === jQuery.ui.keyCode.ESCAPE) {
                    this.selection.clear()
                }
            }.bind(this));
        },

        _setupPersistanceEvents: function() {
            jsPlumb.bind('jsPlumbConnection', this._edgeConnected.bind(this));
            jsPlumb.bind('jsPlumbConnectionDetached', this._edgeDetached.bind(this));
        },

        _shapeDropped: function(uiEvent, uiObject) {
            var node        = Nodes.newNodeOfKind(uiObject.draggable.attr('id'));
            var offset      = this._canvas.offset();
            var gridCoords  = this.toGrid(uiEvent.pageX - offset.left, uiEvent.pageY - offset.top);

            node._editor = this;
            node.appendTo(this._canvas)
                .moveTo(gridCoords.x, gridCoords.y)
            this.graph().addNode(node);
            this.selection.ofNodes(node);

            Backend.addNode(node);
        }
    });

    return Editor;
});