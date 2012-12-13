define(['class', 'menus', 'canvas', 'backend', 'canvas'],
function(Class, Menus, Canvas, Backend) {

    /*
     *  Class: Editor
     */
    return Class.extend({
        config:     undefined,
        graph:      undefined,
        properties: undefined,
        shapes:     undefined,

        _backend:            undefined,
        _navbarActionsGroup: undefined,

        init: function(graphId) {
            if (typeof graphId !== 'number') throw 'You need a graph ID to initialize the editor.';

            this.config = this.getConfig();
            this._backend = new Backend(graphId);
            this._navbarActionsGroup = jQuery('#' + this.config.IDs.NAVBAR_ACTIONS);

            // run a few sub initializer
            this._setupJsPlumb()
                ._setupKeyBindings();

            // fetch the content from the backend
            this._loadGraph(graphId);
        },

        /* Section: Internals */

        getConfig: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        getGraphClass: function() {
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
            this.properties = new Menus.PropertiesMenu(this.graph.getNotation().propertiesDisplayOrder);
            this.shapes     = new Menus.ShapeMenu();

            // fade out the splash screen
            jQuery('#' + this.config.IDs.SPLASH).fadeOut(this.config.Splash.FADE_TIME, function() {
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
            this.graph = new (this.getGraphClass())(json);
            this._loadGraphCompleted();

            return this;
        },

        _setupJsPlumb: function() {
            jsPlumb.importDefaults({
                EndpointStyle: {
                    fillStyle:   this.config.JSPlumb.ENDPOINT_FILL
                },
                Endpoint:        [this.config.JSPlumb.ENDPOINT_STYLE, {
                    radius:      this.config.JSPlumb.ENDPOINT_RADIUS,
                    cssClass:    this.config.Classes.JSPLUMB_ENDPOINT,
                    hoverClass:  this.config.Classes.JSPLUMB_ENDPOINT_HOVER
                }],
                PaintStyle: {
                    strokeStyle: this.config.JSPlumb.STROKE_COLOR,
                    lineWidth:   this.config.JSPlumb.STROKE_WIDTH
                },
                HoverPaintStyle: {
                    strokeStyle: this.config.JSPlumb.STROKE_COLOR_HIGHLIGHTED
                },
                HoverClass:      this.config.Classes.JSPLUMB_CONNECTOR_HOVER,
                Connector:       [this.config.JSPlumb.CONNECTOR_STYLE, this.config.JSPlumb.CONNECTOR_OPTIONS],
                ConnectionsDetachable: false
            });

            jsPlumb.connectorClass = this.config.Classes.JSPLUMB_CONNECTOR;

            return this;
        },

        _setupKeyBindings: function() {
            jQuery(document).keydown(function(event) {

                if (event.which == jQuery.ui.keyCode.ESCAPE) {
                    event.preventDefault();
                    //XXX: deselect everything
                    // This uses the jQuery.ui.selectable internal functions.
                    // We need to trigger them manually in order to simulate a click on the canvas.
                    Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(event);
                    Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(event);
                } else if (event.which == jQuery.ui.keyCode.DELETE) {
                    event.preventDefault();

                    // delete selected nodes
                    jQuery('.' + this.config.Classes.JQUERY_UI_SELECTED + '.' + this.config.Classes.NODE).each(function(index, element) {
                        this.graph.deleteNode(jQuery(element).data(this.config.Keys.NODE).id);
                    }.bind(this));

                    this.properties.hide();

                    // delete selected edges
                    jQuery('.' + this.config.Classes.JQUERY_UI_SELECTED + '.' + this.config.Classes.JSPLUMB_CONNECTOR).each(function(index, element) {
                        var edge = this.graph.getEdgeById(jQuery(element).attr(this.config.Keys.CONNECTION_ID));
                        jsPlumb.detach(edge);
                        this.graph.deleteEdge(edge);
                    }.bind(this));
                }
            }.bind(this));

            return this;
        }
    });
});
