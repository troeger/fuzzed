define(['factory', 'config', 'class', 'jquery', 'jquery-ui'], function (Factory, Config, Class) {
    /**
     * Package: Base
     */

    /**
     * Abstract Class: Menu
     *      Abstract base class that implements base functionality of editor menus (sometimes referred to as fly
     *      windows). Offers functionality for showing/hiding the menu, to maximize and minimize it to the editor's
     *      toolbar and to drag it around on the canvas.
     */
    var Menu = Class.extend({
        /**
         * Group: Members
         *      {jQuerySelector} container     - The DOM element that holds all other visual elements of the menu.
         *
         *      {jQuerySelector} _controls     - jQuery selector referencing the menu title buttons (close, ...)
         *      {Boolean}        _disabled     - Flag indicating whether the menu is disabled and therefore hidden.
         *      {jQuerySelector} _navbar       - jQuery selector referencing the editor's toolbar.
         *      {jQuerySelector} _navbarButton - jQuery selector referencing the button to the minimized menu.
         */
        container:     undefined,
        _controls:     undefined,
        _disabled:     undefined,
        _navbar:       undefined,
        _navbarButton: undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         */
        init: function() {
            this.container = this._setupContainer();
            this._controls = this._setupControls();
            this._disabled = false;
            this._navbar = this._setupNavbar();

            jQuery(this.container).data(Factory.getModule('Config').Keys.MENU, this);

            this._setupDragging();
        },

        /**
         * Abstract Method: _setupContainer
         *      Locate or create the menu's container here and return it as a jQuery selector. Must be overwritten by
         *      subclasses. Usual approach would be to locate a previously created div in the Django templates by their
         *      id.
         */
        _setupContainer: function() {
            throw new SubclassResponsibility();
        },

        /**
         * Method: _setupControls
         *      Locates menu controls container inside the menu's container and its contained minimize and close
         *      buttons. Both of them are optional, but, if present, will be get their minimize or respectively close
         *      callback bound.
         *
         * Returns:
         *      The {<Menu>} controls container as jQuery selector.
         */
        _setupControls: function() {
            var controls = this.container.find('.' + Factory.getModule('Config').Classes.MENU_CONTROLS);

            controls.find('.' + Factory.getModule('Config').Classes.MENU_MINIMIZE)
                .addClass('fa fa-minus-circle')
                .click(this.minimize.bind(this));

            controls.find('.' + Factory.getModule('Config').Classes.MENU_CLOSE)
                .addClass('fa fa-times-circle')
                .click(this.hide.bind(this));

            return controls;
        },

        /**
         * Method: _setupDragging
         *      Enables the menu container to be dragged around on the canvas. Menus are always above other elements on
         *      the canvas and may not leave the canvas. When close to the edges of the canvas, menus snap to its inner
         *      edges.
         *
         * Returns:
         *      This {<Menu>} instance for chaining.
         */
        _setupDragging: function() {
            this.container.draggable({
                containment:   'body',
                stack:         'svg',
                cursor:        Factory.getModule('Config').Dragging.CURSOR,
                scroll:        false,
                snap:          'body',
                snapMode:      'inner',
                snapTolerance: Factory.getModule('Config').Dragging.SNAP_TOLERANCE
            });

            return this;
        },

        /**
         * Method: _setupNavbar
         *      Locates and returns the editor's navbar.
         *
         * Returns:
         *      The navbar's jQuery selector.
         */
        _setupNavbar: function() {
            return jQuery('ul.nav.pull-right');
        },

        /**
         * Group: Accessors
         */

        /**
         * Method: _isMinimized
         *      Returns a boolean flag indicating whether the menu is minimized.
         *
         * Returns:
         *      True if the menu is minimized, false otherwise.
         */
        _isMinimized: function() {
            return typeof this._navbarButton !== 'undefined';
        },

        /**
         * Group: Visibility
         */

        /**
         * Method: disable
         *      Disables the menu, meaning it is being hidden and cannot be shown until enabled again.
         *
         * Returns:
         *      This {<Menu>} instance for chaining.
         */
        disable: function() {
            this._disabled = true;
            this.hide();

            return this;
        },

        /**
         * Method: enable
         *      Enables the menu again. An implicit show is not performed.
         *
         * Returns:
         *      This {<Menu>} instance for chaining.
         */
        enable: function() {
            this._disabled = false;

            return this;
        },

        /**
         * Method: show
         *      Shows the menu's container unless it the menu is minimized or disabled.
         *
         * Returns:
         *      This {<Menu?} instance for chaining.
         */
        show: function() {
            // prevent that the menu is shown again as long it is minimized
            if (this._isMinimized() || this._disabled) return this;
            this.container.show();

            return this;
        },

        /**
         * Method: hide
         *      Hides the menu.
         *
         * Returns:
         *      This {<Menu>} instance for chaining.
         */
        hide: function() {
            this.container.hide();
            return this;
        },

        /**
         * Method: maximize
         *      Maximizes the menu on clicking its minimized representation in the navigation bar. Will calculate the
         *      position where the menu will be maximized to first (including a 20 pixel offset of the canvas borders)
         *      and then animate it moving there. This method will also remove the button from the bar.
         *
         * Returns:
         *      This {<Menu>} instance for chaining.
         */
        maximize: function(eventObject) {
            this._navbarButton.remove();
            this._navbarButton = undefined;

            var destinationTransformation = eventObject.data;
            this.container.show();

            // ensure that maximized menus will be visible (in case the window has been resized)
            destinationTransformation.left = Math.min(
                destinationTransformation.left,
                jQuery(window).width() - this.container.outerWidth() - Factory.getModule('Config').Menus.MENU_OFFSET
            );
            destinationTransformation.top = Math.min(
                destinationTransformation.top,
                jQuery(window).height() - this.container.outerHeight() - Factory.getModule('Config').Menus.MENU_OFFSET
            );

            this.container.animate(destinationTransformation, { duration: Factory.getModule('Config').Menus.ANIMATION_DURATION });

            return this;
        },

        /**
         * Method: minimize
         *      Minimizes the menu from its current position to the navigation bar. A button will appear in the menu bar
         *      instead. The minimization is animated in width and height over the period of about half a second. A
         *      minimized menu will not reappear until maximized again by clicking on the navigation bar button.
         *
         * Returns:
         *      This {<Menu>} instance for chaining.
         */
        minimize: function() {
            if (this._isMinimized()) return this;

            // create a button in the toolbar
            this._navbarButton = jQuery('<li><a href="#">' + this.container
                .attr(Factory.getModule('Config').Attributes.HEADER) + '</a></li>')
                .css('visibility', 'hidden')
                .prependTo(this._navbar)
                // .offset() here will closure the position where the window was minimized
                .click(this.container.offset(), this.maximize.bind(this));

            // animate the window minimizing towards the navigation button
            var navButtonPosition = this._navbarButton.offset();
            this.container.animate({
                top: navButtonPosition.top,
                left: navButtonPosition.left,
                width: 0,
                height: 0
            }, {
                duration: Factory.getModule('Config').Menus.ANIMATION_DURATION,
                complete: function () {
                    this._navbarButton.css('visibility', '');
                    this.container.hide();
                    // width and height have to be remove here so that the css will fall back to auto
                    // so that changes to the bounding box of the menu will be reflected when maximizing
                    this.container.css('width', '');
                    this.container.css('height', '');
                }.bind(this)
            });

            return this;
        }
    });

    /**
     * Class: ShapeMenu
     *      Concrete implementation of a menu. This menu class manages the shapes menu and is instantiated in the
     *      editor. A shapes menu represents the repository of shapes that a user can create on its own. The thumbnail
     *      of a shape can be dragged from the menu and released on the canvas in order to create a new node.
     *
     * Extends: <Base::Menu>
     */
    var ShapeMenu = Menu.extend({
        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *      Overrides the default implementation of menu in order to also locate the shape thumbnails.
         */
        init: function () {
            this._super();
            this._setupThumbnails();
        },

        /**
         * Method: _setupContainer
         *      Implements the abstract _setupContainer method of {<Menu>}. Locates the shapes menu container that is
         *      pre-created in the Django template and returns it.
         *
         * Returns:
         *      jQuery set including the shapes menu's container.
         */
        _setupContainer: function() {
            return jQuery('#' + Factory.getModule('Config').IDs.SHAPES_MENU);
        },

        /**
         * Method: _setupThumbnails
         *      Locates the thumbnails (pre-rendered in the Django template) and makes them draggable.
         *
         * Returns:
         *      This {<ShapesMenu>} instance for chaining.
         */
        _setupThumbnails: function() {
			var thumbnails = this.container.find('.' + Factory.getModule('Config').Classes.DRAGGABLE_WRAP_DIV).children();

            // make shapes in the menu draggable
            thumbnails.draggable({
                helper: 'clone',
                opacity: Factory.getModule('Config').Dragging.OPACITY,
                cursor: Factory.getModule('Config').Dragging.CURSOR,
                appendTo: 'body',
                revert: 'invalid',
                zIndex: 200
            });

            return this;
		}
    });

    /**
     * Class: PropertiesMenu
     *      Concrete implementation of the abstract menu class. Models the properties menu that displays the modifiable
     *      or user-readable properties of a node. Will only display the properties of exactly one node. Multi-selected
     *      nodes are hidden.
     *
     * Extends: {<Menu>}
     */
    var PropertiesMenu = Menu.extend({
        /**
         * Group: Members
         *      {Array[String]} _displayOrder - Array containing the names of displayable properties ordered by
         *                                      appearance in the menu.
         *      {DOMElement}    _form         - The form containing all the visual form inputs of the
         *                                      {PropertyMenuEntries::Entries}.
         *      {Node}          _selectee     - The node instance which properties are being currently displayed.
         */
        _displayOrder: undefined,
        _form:         undefined,
        _selectee:     undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *      Overrides menu's constructor. Saves the display order attributed and locates the pre-rendered form. Sets
         *      up the selection event handlers also.
         */
        init: function(displayOrder) {
            this._super();

            this._displayOrder = displayOrder;
            this._form         = this.container.find('.form-horizontal');

            this._setupSelection();
        },

        /**
         * Method: _setupContainer
         *      Concrete implementation of the abstract base method. Locates and returns the property menu container
         *      that is pre-rendered into the editors template.
         *
         * Returns:
         *      jQuery set containing the property menu container.
         */
        _setupContainer: function() {
            return jQuery('#' + Factory.getModule('Config').IDs.PROPERTIES_MENU);
        },

        /**
         * Method: _setupSelection
         *      Registers on the selection stop event in order to display the selected node's properties.
         *
         * On:
         *      <Config::Events::CANVAS_SELECTION_STOPPED>
         *
         * Returns:
         *      This {<PropertyMenu>} instance for chaining.
         */
        _setupSelection: function() {
            jQuery(document).on(Factory.getModule('Config').Events.CANVAS_SELECTION_STOPPED, this.show.bind(this));

            return this;
        },

        /**
         * Group: Visibility
         */

        /**
         * Method: hide
         *      Overrides the base hide method of <Base::Menu>. Additionally, removes the visual representations of the
         *      properties from the form and resets the current node.
         *
         * Returns:
         *      This {<PropertyMenu>} for chaining.
         */
        hide: function() {
            this._removeEntries();
            this._selectee = undefined;
            return this._super();
        },

        /**
         * Method: _removeEntries
         *      If exactly one node is selected, this method will issue all visual representation of the properties to
         *      remove themselves.
         *
         * Returns:
         *      This {<PropertyMenu>} instance for chaining.
         */
        _removeEntries: function() {
            if (!this._selectee) return this;

            _.each(this._selectee.properties, function(property) {
                property.menuEntry.remove();
            }.bind(this));

            return this;
        },

        /**
         * Method: maximize
         *      Overrides the base implementation of maximize. Triggers the show method again in order to recalculate
         *      the current selection and consequently the property menu's visibility.
         *
         * Returns:
         *      This {<PropertyMenu>} instance for chaining.
         */
        maximize: function(eventObject) {
            this._super(eventObject);
            this.show();

            return this;
        },

        /**
         * Method: show
         *      Overrides the base implementation of <Menu>. First, removes all currently displayed entries (even
         *      when being the same). Then, calculates the current node selection. If and only if, the is exactly one
         *      node in the the selection and the menu is not minimized, the node's properties are displayed using
         *      _show. Otherwise, the property menu is hidden.
         *
         * Returns:
         *      This {<PropertyMenu>} instance for chaining.
         */
        show: function() {
            var selected = jQuery('.' + Factory.getModule('Config').Classes.SELECTED);
            this._removeEntries();

            // display the properties menu only if there is exactly one node selected
            // and the menu is not minimized; otherwise hide the menu
            if (selected.length === 1 && !this._isMinimized() && !this._disabled) {
                return this._show(selected);
            }

            return this.hide();
        },

        /**
         * Method: _show
         *      Internal implementation of the property menu's show mechanism. Grabs the selected node instance first.
         *      Determines whether there are properties to be displayed - i.e. properties present and not hidden - and
         *      then issues the properties to display themselves on the form and to change their visibility to show.
         *
         * Returns:
         *      This {<PropertyMenu>} instance for chaining.
         */
        _show: function (selected) {
            if (selected.hasClass(Factory.getModule('Config').Classes.NODE)) {
                this._selectee = selected.data(Factory.getModule('Config').Keys.NODE);
            } else if (selected.hasClass(Factory.getModule('Config').Classes.JSPLUMB_CONNECTOR)) {
                this._selectee = selected.data(Factory.getModule('Config').Keys.EDGE);
            } else { // if (selected.hasClass(Factory.getModule('Config').Keys.NODEGROUP
                //TODO: do this right (which is handling all
                this._selectee = selected.parent().parent().data(Factory.getModule('Config').Keys.NODEGROUP);
            }

            // this node does not have any properties to display, go home!
            if (_.isEmpty(this._selectee.properties)) {
                this.hide();
                return this;
            }

            _.each(this._displayOrder, function (propertyName) {
                var property = this._selectee.properties[propertyName];
                // has the node such a property? display it!
                if (typeof property !== 'undefined' && property !== null) {
                    property.menuEntry.appendTo(this._form);

                    jQuery(property).on(Factory.getModule('Config').Events.PROPERTY_HIDDEN_CHANGED, function (event, hidden) {
                        this.container.toggle(!this._allHidden());
                    }.bind(this));
                }
            }.bind(this));

            // fix the left offset (jQueryUI bug with draggable menus and CSS right property)
            if (this.container.css('left') === 'auto') {
                var offset =  - this.container.outerWidth(true) - Factory.getModule('Config').Menus.MENU_OFFSET;
                this.container.css('left', jQuery('body').outerWidth(true) + offset);
            }
            this.container.toggle(!_.all(this._selectee.properties, function(property) {
                return property.hidden;
            }));

            return this;
        },

        /**
         * Method: _allHidden
         *      Determines if all properties of the node are hidden preventing the menu to be displayed.
         *
         * Returns:
         *      {Boolean} indicating hidden state of the properties.
         */
        _allHidden: function() {
            return !this._selectee || _.all(this._selectee.properties, function(property) { return property.hidden; });
        }
    });

    /**
     * Class: LayoutMenu
     *      Small prompt window after hitting the layout button that asks whether you want to keep the changes or not.
     *      Any editor interaction while the prompt is open will auto-accept the layout and commit it to the backend.
     */
    var LayoutMenu = Menu.extend({
        /**
         * Group: Members
         *      {jQuerySelector} _keep - jQuery selector referencing the keep layout button.
         *      {jQuerySelector} _undo - jQuery selector referencing the undo layout button.
         */
        _keep: undefined,
        _undo: undefined,

        /**
         * Constructor: init
         *      Overrides the default construct so that the layout request can be captured and the undo button located.
         *      Initially, the layout menu is also set to hidden.
         */
        init: function () {
            this._super();
            this._setupButtons()
                ._setupLayoutRequested()
                .hide();
        },

        /**
         * Method: keep
         *      Is called by the {<Editor>} in order to obtain a promise from the layout window. The promise will be kept
         *      if the user clicks on 'Keep' in the layout window or continues modelling (including new requests to
         *      auto layout, ...). On hitting undo in the layout menu the promise is broken and the editor is reverting
         *      the nodes to their initial positions before the auto-layout.
         *
         * Returns:
         *      A {jQuery::Promise} that is watched by the {<Editor>} for reverting the nodes' positions.
         */
        keep: function () {
            var deferred = jQuery.Deferred();

            // User has accepted to keep the layout by explicitly clicking the button
            this._keep.click(function () {
                deferred.resolve();
            }.bind(this));

            // User has accepted implicitly by continuing to edit the graph
            jQuery(document).one([
                Factory.getModule('Config').Events.CANVAS_SHAPE_DROPPED,
                Factory.getModule('Config').Events.NODE_ADDED,
                Factory.getModule('Config').Events.NODE_DELETED,
                Factory.getModule('Config').Events.EDGE_ADDED,
                Factory.getModule('Config').Events.EDGE_DELETED,
                Factory.getModule('Config').Events.NODEGROUP_ADDED,
                Factory.getModule('Config').Events.NODEGROUP_DELETED,
                Factory.getModule('Config').Events.GRAPH_LAYOUT,
                Factory.getModule('Config').Events.NODE_PROPERTY_CHANGED
            ].join(' '), function () {
                deferred.resolve();
            }.bind(this));

            // User requested an undo
            this._undo.click(function () {
                deferred.reject();
            }.bind(this));

            return deferred.promise();
        },

        /**
         * Method: show
         *      Override of the basic show method. Center the layout menu dialog on the canvas.
         *
         * Returns:
         *      This {<LayoutMenu>} instance for chaining.
         */
        show: function () {
            var viewport = jQuery(window);

            this.container.css({
                top: viewport.height() / 2 - this.container.height() / 2,
                left: viewport.width() / 2 - this.container.width() / 2
            });

            return this._super();
        },

        /**
         * Method: _setupButtons
         *      Locates the keep and undo layout buttons.
         *
         * Returns:
         *      This {<LayoutMenu>} instance for chaining.
         */
        _setupButtons: function () {
            this._keep = this.container.find('button.btn-primary').add(this._controls.find('.menu-close'));
            this._undo = this.container.find('button.btn-danger');

            return this;
        },

        /**
         * Method: _setupLayoutRequested
         *      Sets up two global event listeners that listens to graph layout requests and performed layouts. Shows
         *      or respectively hides the menu.
         *
         * Returns:
         *      This {<LayoutMenu>} instance for chaining.
         */
        _setupLayoutRequested: function () {
            jQuery(document).on(Factory.getModule('Config').Events.GRAPH_LAYOUT,   this.show.bind(this));
            jQuery(document).on(Factory.getModule('Config').Events.GRAPH_LAYOUTED, this.hide.bind(this));

            return this;
        },

        /**
         * Method: _setupContainer
         *      Implements the abstract base method. Locates the template-prerendered layout menu div.
         *
         * Returns:
         *      The jQuery selector referencing the layout menu.
         */
        _setupContainer: function () {
            return jQuery('#' + Factory.getModule('Config').IDs.LAYOUT_MENU);
        }
    });

    return {
        Menu:           Menu,
        LayoutMenu:     LayoutMenu,
        ShapeMenu:      ShapeMenu,
        PropertiesMenu: PropertiesMenu
    }
});
