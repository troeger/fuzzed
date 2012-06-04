define(['require-config', 'require-nodes'], function(Config, Nodes) {

    /*
     *  ShapeMenu
     */
    function ShapeMenu() {
        this._shapes = jQuery('#' + Config.IDs.SHAPES_MENU);

        this._setupDragging();
        this._setupThumbnails();
    }

    ShapeMenu.prototype._setupDragging = function() {
        jQuery('#' + Config.IDs.SHAPES_MENU).draggable({
            containment:   '#' + Config.IDs.CONTENT,
            stack:         '.' + Config.Classes.NODE,
            cursor:        Config.Dragging.CURSOR,
            scroll:        false,
            snap:          '#' + Config.IDs.CONTENT,
            snapMode:      'inner',
            snapTolerance: Config.Dragging.SNAP_TOLERANCE
        });
    }

    ShapeMenu.prototype._setupThumbnails = function() {  
        var thumbnails = this._shapes.find('.' + Config.Classes.NODE_THUMBNAIL);
        var svgs       = thumbnails.children('svg');

        // scale the icons down
        svgs.width (svgs.width()  * Config.ShapeMenu.THUMBNAIL_SCALE_FACTOR);
        svgs.height(svgs.height() * Config.ShapeMenu.THUMBNAIL_SCALE_FACTOR);
        svgs.each(function() {
            var g = jQuery(this).children('g');
            g.attr('transform', 'scale(' + Config.ShapeMenu.THUMBNAIL_SCALE_FACTOR + ') ' + g.attr('transform'));
        });

        // make shapes in the menu draggable
        thumbnails.draggable({
            helper:   'clone',
            opacity:  Config.Dragging.OPACITY,
            cursor:   Config.Dragging.CURSOR,
            appendTo: 'body',
            revert:   'invalid',
            zIndex:   200
        });
    }

    /*
     *  PropertiesMenu
     */
    function PropertiesMenu() {
        // menu is the container and properties the actual element where properties will bea added
        this._menu       = jQuery('#' + Config.IDs.PROPERTIES_MENU);
        this._properties = this._menu.find('.' + Config.Classes.PROPERTIES);

        this._setupDragging();
    }

    PropertiesMenu.prototype.hide = function() {
        this._menu.hide();
    }

    PropertiesMenu.prototype.show = function(nodes, force) {
        if (!_.isArray(nodes)) nodes = [nodes];

        if (force || typeof(nodes) === 'undefined' || _.any(nodes, function(node) { return node.properties().length > 0})) {
            this._properties.empty();
            this._menu.show();

            _.each(nodes, function(node) {
                _.each(node.properties(), function(property) {
                    property.show(this._properties);
                }.bind(this));
            }.bind(this));
        }
    }

    PropertiesMenu.prototype._setupDragging = function() {
        this._properties.draggable({
            containment:   '#' + Config.IDs.CONTENT,
            stack:         '.' + Config.Classes.NODE,
            cursor:        Config.Dragging.CURSOR,
            scroll:        false,
            snap:          '#' + Config.IDs.CONTENT,
            snapMode:      'inner',
            snapTolerance: Config.Dragging.SNAP_TOLERANCE
        });
    }

    /*
     *  Selection
     */
    function Selection() {
        this._nodes  = []; // node objects; not DOM elements
        this._editor = jQuery('#' + Config.IDs.CANVAS).data(Config.Keys.EDITOR);
    }

    // clear the selection, leaving the nodes on the canvas
    Selection.prototype.clear = function() {
        _.each(this._nodes, function(node) {
            node.deselect()
        });
        this._empty();
        this._editor.properties.hide();

        return this;
    }

    Selection.prototype.contains = function(node) {
        return _.indexOf(this._nodes, node) >= 0;
    }

    // make a new selection of the given node(s)
    Selection.prototype.of = function(nodes) {
        this.clear();

        if (_.isArray(nodes)) {
            this._nodes = nodes;
        } else {
            this._nodes.push(nodes);
        }

        _.each(this._nodes, function(node) {
            node.select();
        });
        this._editor.properties.show(nodes);

        return this;
    }

    // remove the current contained nodes from the canvas and clear the selection
    Selection.prototype.remove = function() {
        _.each(this._nodes, function(node) {
            node.remove();
        })
        this._empty();
        this._editor.properties.hide();

        return this;
    }

    // helper function to empty the selected nodes
    Selection.prototype._empty = function() {
        this._nodes = [];
        return this;
    }

    /*
     *  Editor
     */
    function Editor(_id_) {
        this._graphId = _id_;

        // locate own DOM elements and bind Editor instance to canvas
        this._canvas     = jQuery('#' + Config.IDs.CANVAS);
        this._background = this._canvas.svg().svg('get');
        this._canvas.data(Config.Keys.EDITOR, this);

        // create manager objects for the bars and the selection
        this.shapes     = new ShapeMenu();
        this.properties = new PropertiesMenu();
        this.selection  = new Selection();

        // run a few sub initializer
        this._setupBackground();
        this._setupCanvas();
        this._setupJsPlumb();
        this._setupKeyBindings();
    }

    Editor.prototype.graphId = function() {
        return this._graphId;
    }

    Editor.prototype.toGrid = function(first, second) {
        var x = Number.NaN;
        var y = Number.NaN;

        // if both parameter are numbers we can take them as they are
        if (_.isNumber(first) && _.isNumber(second)) {
            x = first;
            y = second;

        // however the first parameter could also be an object
        // of the form {x: NUMBER, y: NUMBER} (convenience reasons)
        } else if (typeof first === 'object') {
            x = first.x;
            y = first.y;
        }

        return {
            x: Math.round((first  - Config.Grid.HALF_SIZE) / Config.Grid.SIZE),
            y: Math.round((second - Config.Grid.HALF_SIZE) / Config.Grid.SIZE)
        }
    }

    Editor.prototype._drawGrid = function() {
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
        for (var y = Config.Grid.HALF_SIZE; y < height; y += Config.Grid.SIZE) {
            this._background.line(0, y, width, y, {
                stroke:          Config.Grid.STROKE,
                strokeWidth:     Config.Grid.STROKE_WIDTH,
                strokeDashArray: Config.Grid.STROKE_STYLE
            });
        }

        // vertical lines
        for (var x = Config.Grid.HALF_SIZE; x < width; x += Config.Grid.SIZE) {
            this._background.line(x, 0, x, height, {
                stroke:          Config.Grid.STROKE,
                strokeWidth:     Config.Grid.STROKE_WIDTH,
                strokeDashArray: Config.Grid.STROKE_STYLE
            });
        }
    }

    Editor.prototype._setupBackground = function() {
        this._drawGrid();

        // clicks on the canvas clear the selection
        this._canvas.click(this.selection.clear.bind(this.selection));
        // redraw the background grid when the window resizes
        jQuery(window).resize(this._drawGrid.bind(this));
    }

    Editor.prototype._setupCanvas = function() {
        // make canvas droppable for shapes from the shape menu
        this._canvas.droppable({
            accept:    '.' + Config.Classes.NODE_THUMBNAIL,
            tolerance: 'fit',
            drop:      this._shapeDropped.bind(this)
        });
    }

    Editor.prototype._setupJsPlumb = function() {
        jsPlumb.importDefaults({
            EndpointStyle: {
                fillStyle:   Config.JSPlumb.ENDPOINT_FILL
            },
            Endpoint:        [Config.JSPlumb.ENDPOINT_STYLE, 
                {
                    radius:     Config.JSPlumb.ENDPOINT_RADIUS,
                    cssClass:   Config.Classes.JSPLUMB_ENDPOINT,
                    hoverClass: Config.Classes.JSPLUMB_ENDPOINT_HOVER
                }],
            PaintStyle: {
                strokeStyle: Config.JSPlumb.STROKE,
                lineWidth:   Config.JSPlumb.STROKE_WIDTH
            },
            HoverPaintStyle: {
                strokeStyle: Config.JSPlumb.STROKE_HOVER
            },
            Connector:       Config.JSPlumb.STROKE_STYLE,
            Anchors:         ['BottomMiddle', 'TopMiddle']
        });
    }

    Editor.prototype._setupKeyBindings = function() {
        jQuery(document).keydown(function(eventObject) {
            // hitting delete removes the current selection from the canvas
            if (eventObject.which === jQuery.ui.keyCode.DELETE) {
                this.selection.remove();
            }
        }.bind(this));
    }

    Editor.prototype._shapeDropped = function(uiEvent, uiObject) {
        var node        = new (uiObject.draggable.data(Config.Keys.CONSTRUCTOR))();
        var offset      = this._canvas.offset();
        var coordinates = this.toGrid(uiEvent.pageX - offset.left, uiEvent.pageY - offset.top);

        node
            .moveTo(coordinates.x * Config.Grid.SIZE, coordinates.y * Config.Grid.SIZE)
            .appendTo(this._canvas);
        this.selection.of(node);
    }

    return Editor;
});