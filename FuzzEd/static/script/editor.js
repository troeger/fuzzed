define(['class', 'canvas', 'menus', 'selection', 'config', 'backend'],
function(Class, Canvas, Menus, Selection, Config, Backend) {

    /*
     *  Class: Editor
     */
    return Class.extend({
        graph:      undefined,
        properties: undefined,
        selection:  undefined,
        shapes:     undefined,

        _backend:            undefined,
        _navbarActionsGroup: undefined,

        init: function(graphId) {
            if (typeof graphId !== 'number') throw 'You need a graph ID to initialize the editor.';

            this._backend = new Backend(graphId);
            this._navbarActionsGroup = jQuery('#' + Config.IDs.NAVBAR_ACTIONS);

            // create manager objects for the bars and the selection
            this.properties = new Menus.PropertiesMenu();
            this.shapes     = new Menus.ShapeMenu();
            this.selection  = new Selection(this);

            // run a few sub initializer
            this._setupJsPlumb()
                ._setupKeyBindings();

            // fetch the content from the backend
            this._loadGraph(graphId);
        },

        /* Section: Internals */

        _graphClass: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        _loadGraph: function(graphId) {
            Backend.getGraph(
                this._loadGraphFromJson.bind(this),
                this._loadGraphError.bind(this)
            );

            return this;
        },

        _loadGraphCompleted: function() {
            // fade out the splash screen
            jQuery('#' + Config.IDs.SPLASH).fadeOut(Config.Splash.FADE_TIME);
            // activate the backend AFTER the graph is fully loaded to prevent backend calls during graph construction
            this._backend.activate();
        },

        _loadGraphError: function(response, textStatus, errorThrown) {
            alert('Could not load graph, reason: ' + textStatus + ' ' + errorThrown);
            throw 'Could not load the graph from the backend';
        },

        _loadGraphFromJson: function(json) {
            this.graph = new (this._graphClass())(json);
            this._loadGraphCompleted();
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

            // listen for clicks on connections for selections
            //TODO: move to selection
            jsPlumb.bind('click', function(connection, event) {
                event.stopPropagation();
                this.selection.ofConnections(connection);
            }.bind(this));
        },

        //TODO move to selection
        _setupKeyBindings: function() {
            jQuery(document).keydown(function(eventObject) {
                // hitting delete removes the current selection from the canvas
                if (eventObject.which === jQuery.ui.keyCode.DELETE) {
                    this.selection.remove();

                } else if (eventObject.which === jQuery.ui.keyCode.ESCAPE) {
                    this.selection.clear()
                }
            }.bind(this));
        }
    });
});