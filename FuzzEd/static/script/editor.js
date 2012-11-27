define(['class', 'menus', 'canvas', 'config', 'backend', 'canvas'],
function(Class, Menus, Canvas, Config, Backend) {

    /*
     *  Class: Editor
     */
    return Class.extend({
        graph:      undefined,
        properties: undefined,
        shapes:     undefined,

        _backend:            undefined,
        _navbarActionsGroup: undefined,

        init: function(graphId) {
            if (typeof graphId !== 'number') throw 'You need a graph ID to initialize the editor.';

            this._backend = new Backend(graphId);
            this._navbarActionsGroup = jQuery('#' + Config.IDs.NAVBAR_ACTIONS);

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
            this._backend.getGraph(
                this._loadGraphFromJson.bind(this),
                this._loadGraphError.bind(this)
            );

            return this;
        },

        _loadGraphCompleted: function() {
            // create manager objects for the bars
            this.properties = new Menus.PropertiesMenu(this.graph.getNotation().propertyMenuDisplayOrder);
            this.shapes     = new Menus.ShapeMenu();

            // fade out the splash screen
            jQuery('#' + Config.IDs.SPLASH).fadeOut(Config.Splash.FADE_TIME, function() {
                jQuery(this).remove();
            });
            // activate the backend AFTER the graph is fully loaded to prevent backend calls during graph construction
            this._backend.activate();

            return this;
        },

        _loadGraphError: function(response, textStatus, errorThrown) {
            alert('Could not load graph, reason: ' + textStatus + ' ' + errorThrown);
            throw 'Could not load the graph from the backend';
        },

        _loadGraphFromJson: function(json) {
            this.graph = new (this._graphClass())(json);
            this._loadGraphCompleted();

            return this;
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

            return this;
        },

        _setupKeyBindings: function() {
            jQuery(document).keydown(function(event) {

                if (event.which == jQuery.ui.keyCode.ESCAPE) {
                    event.preventDefault();
                    //XXX: deselect everything
                    // This uses the jQuery.ui.selectable internal functions.
                    // We need to trigger them manually in order to simulate a click on the canvas.
                    Canvas.container.data('selectable')._mouseStart(event);
                    Canvas.container.data('selectable')._mouseStop(event);
                } else if (event.which == jQuery.ui.keyCode.DELETE) {
                    event.preventDefault();
                    jQuery('.ui-selected, ' + Config.Classes.NODE).each(function(index, element) {
                        this.graph.deleteNode(jQuery(element).data(Config.Keys.NODE).id);
                    }.bind(this));
                }
            }.bind(this));
        }
    });
});