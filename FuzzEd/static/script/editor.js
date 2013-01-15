define(['class', 'menus', 'canvas', 'backend', 'canvas'],
function(Class, Menus, Canvas, Backend) {
    /**
     *  Package: Base
     */

    /**
     *  Class: Editor
     *
     *  This is the _abstract_ base class for all graph-kind-specific editors. It manages the visual components
     *  like menus and the graph itself. It is also responsible for global keybindings.
     */
    return Class.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {Object}         config               - Graph-specific <Config> object.
         *    {Graph}          graph                - <Graph> instance to be edited.
         *    {PropertiesMenu} properties           - The <Menu::PropertiesMenu> instance used by this editor for
         *                                            changing the properties of nodes of the edited graph.
         *    {ShapesMenu}     shapes               - The <Menu::ShapeMenu> instance use by this editor to show the
         *                                            available shapes for the kind of the edited graph.
         *    {Backend}        _backend             - The instance of the <Backend> that is used to communicate graph
         *                                            changes to the server.
         *    {jQuery Selector} _navbarActionsGroup - Navbar dropdown menu that contains the available actions.
         */
        config:              undefined,
        graph:               undefined,
        properties:          undefined,
        shapes:              undefined,

        _backend:            undefined,
        _navbarActionsGroup: undefined,

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Sets up the editor interface and necessary callbacks and loads the graph with the given ID
         *    from the backend.
         *
         *  Parameters:
         *    {int} graphId - The ID of the graph that is going to be edited by this editor.
         */
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

        /**
         *  Group: Accessors
         */

        /**
         *  Method: getConfig
         *    _Abstract_, needs to be overridden in specific editor classes.
         *
         *  Returns:
         *    The <Config> object that corresponds to the loaded graph's kind.
         */
        getConfig: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        /**
         *  Method: getGraphClass
         *    _Abstract_, needs to be overridden in specific editor classes.
         *
         *  Returns:
         *    The specific <Graph> class that should be used to instantiate the editor's graph with information
         *    loaded from the backend.
         */
        getGraphClass: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        /**
         *  Group: Graph Loading
         */

        /**
         *  Method: _loadGraph
         *    Asynchronously loads the graph with the given ID from the backend.
         *    <_loadGraphFromJson> will be called when done.
         *
         *  Parameters:
         *    {int} graphId - ID of the graph that should be loaded.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _loadGraph: function(graphId) {
            this._backend.getGraph(
                this._loadGraphFromJson.bind(this),
                this._loadGraphError.bind(this)
            );

            return this;
        },

        /**
         *  Method: _loadGraphCompleted
         *    Callback that gets fired when the graph is loaded completely.
         *    We need to perform certain actions afterwards, like initialization of menus and activation of
         *    backend observers to prevent calls to the backend while the graph is initially constructed.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
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

        /**
         *  Method: _loadGraphError
         *    Callback that gets called in case <_loadGraph> results in an error.
         */
        _loadGraphError: function(response, textStatus, errorThrown) {
            alert('Could not load graph, reason: ' + textStatus + ' ' + errorThrown);
            throw 'Could not load the graph from the backend';
        },

        /**
         *  Method: _loadGraphFromJson
         *    Callback triggered by the backend, passing the loaded JSON representation of the graph.
         *    It will initialize the editor's graph instance using the <Graph> class returned in <getGraphClass>.
         *
         *  Parameters:
         *    {JSON} json - JSON representation of the graph, loaded from the backend.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _loadGraphFromJson: function(json) {
            this.graph = new (this.getGraphClass())(json);
            this._loadGraphCompleted();

            return this;
        },

        /**
         *  Group: Setup
         */

        /**
         *  Method: _setupJsPlumb
         *    Sets all jsPlumb defaults used by this editor.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
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

        /**
         *  Method: _setupKeyBindings
         *    Setup the global key bindings
         *
         *  Keys:
         *    ESCAPE - Clear selection.
         *    DELETE - Delete all selected elements (nodes/edges).
         *
         *  Returns:
         *    This editor instance for chaining.
         */
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
                        var edge = this.graph.getEdgeById(jQuery(element).attr(this.config.Attributes.CONNECTION_ID));
                        jsPlumb.detach(edge);
                        this.graph.deleteEdge(edge);
                    }.bind(this));
                }
            }.bind(this));

            return this;
        }
    });
});
