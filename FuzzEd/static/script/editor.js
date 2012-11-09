define(['class', 'editor-menus', 'editor-selection', 'config', 'backend'],
function(Class, Menus, Selection, Config, Backend) {

    /*
     *  Class: Editor
     */
    return Class.extend({
        canvas:     undefined,
        graph:      undefined,
        properties: undefined,
        selection:  undefined,
        shapes:     undefined,

        _background: undefined,
        _navbarActionsGroup: undefined,

        init: function(graphId) {
            if (typeof graphId !== 'number') throw 'You need a graph ID to initialize the editor.';

            // locate predefined DOM elements and bind Editor instance to canvas
            this.canvas = jQuery('#' + Config.IDs.CANVAS);
            this.canvas.data(Config.Keys.EDITOR, this);

            this._background         = this.canvas.svg().svg('get');
            this._navbarActionsGroup = jQuery('#' + Config.IDs.NAVBAR_ACTIONS);

            // create manager objects for the bars and the selection
            this.properties = new Menus.PropertiesMenu();
            this.shapes     = new Menus.ShapeMenu();
            this.selection  = new Selection();

            // run a few sub initializer
            this._setupBackground()
                ._setupCanvas()
                ._setupJsPlumb()
                ._setupKeyBindings();

            // fetch the content from the backend
            this._loadGraph(graphId);
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
            var height = this.canvas.height();
            var width  = this.canvas.width();

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

            return this;
        },

        _edgeConnected: function(edge) {
            var connection = edge.connection;
            connection._fuzzedID = new Date().getTime();
            Backend.addEdge(connection._fuzzedID, edge.source.data(Config.Keys.NODE), edge.target.data(Config.Keys.NODE));
            this.graph.addEdge(edge.connection);

            return this;
        },

        _edgeDetached: function(edge) {
            var connection = edge.connection;

            this.graph.deleteEdge(connection);
            Backend.deleteEdge(connection);

            return this;
        },

        _loadGraph: function(graphId) {
            Backend.getGraph(graphId,
                this._loadGraphFromJson.bind(this),
                this._loadGraphError.bind(this)
            );

            return this;
        },

        _loadGraphCompleted: function() {
            // setup JsPlumb events here, so that it does not save the edges from the graph loading
            this._setupJsPlumbEvents();
            // fade out the splash screen
            jQuery('#' + Config.IDs.SPLASH).fadeOut(Config.Splash.FADE_TIME);
        },

        _loadGraphError: function(graph, response, textStatus, errorThrown) {
            alert('Could not load graph, reason: ' + textStatus + ' ' + errorThrown);
            throw 'Could not load the graph from the backend';
        },

        _loadGraphFromJson: function(json) {
            this.graph = new Graph(json);
            this._loadGraphCompleted();
        },

        _setupBackground: function() {
            this._drawGrid();
            // clicks on the canvas clears the selection
            this.canvas.click(this.selection.clear.bind(this.selection));
            // redraw the background grid when the window resizes
            jQuery(window).resize(this._drawGrid.bind(this));
        },

        _setupCanvas: function() {
            // make canvas droppable for shapes from the shape menu
            this.canvas.droppable({
                accept:    'svg',
                tolerance: 'fit',
                drop:      this._shapeDropped.bind(this)
            });
        },

        _setupJsPlumb: function() {
            //TODO: check whether we need to move this to the specific notation files
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

        _setupJsPlumbEvents: function() {
            jsPlumb.bind('jsPlumbConnection', this._edgeConnected.bind(this));
            jsPlumb.bind('jsPlumbConnectionDetached', this._edgeDetached.bind(this));
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

        _shapeDropped: function(uiEvent, uiObject) {
            var node        = Nodes.newNodeOfKind(uiObject.draggable.attr('id'));
            var offset      = this.canvas.offset();
            var gridCoords  = this.toGrid(uiEvent.pageX - offset.left, uiEvent.pageY - offset.top);

            node._editor = this;
            node.appendTo(this.canvas)
                .moveTo(gridCoords.x, gridCoords.y)
            this.graph.addNode(node);
            this.selection.ofNodes(node);

            Backend.addNode(node);
        }
    });
});