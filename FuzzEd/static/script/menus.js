define(['config', 'class', 'jquery'], function(Config, Class) {
    /**
     * Package: Base
     */

    /**
     * Class: {Abstract} Menu
     *
     * Abstract base class that implements base functionality of editor menus (sometimes referred to as fly windows).
     * Offers functionality for showing/hiding the menu, to maximize and minimize it to the editor's toolbar and to
     * drag it around on the canvas.
     *
     * A concrete implementation of the menu must define the location/construct the menu's container.
     */
    var Menu = Class.extend({
        /**
         * Group: Members
         *
         * Properties:
         *  {DOMElement} container     - The DOM element that holds all other visual elements of the menu.
         *
         *  {DOMElement} _controls     -
         *  {boolean}    _disabled     -
         *  {DOMElement} _navbar       -
         *  {DOMElement  _navbarButton -
         */
        container:    undefined,

        _controls:     undefined,
        _disabled:     undefined,
        _navbar:       undefined,
        _navbarButton: undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *
         * Abstract constructor that will create menu instances in non abstract subclasses (see _setupContainer).
         * Interaction is fully enabled.
         *
         * Returns:
         *   This {Menu} instance.
         */
        init: function() {
            this.container = this._setupContainer();
            this._controls = this._setupControls();
            this._disabled = false;
            this._navbar   = this._setupNavbar();

            this._setupDragging();
        },

        /**
         * Method: _setupContainer
         *
         * Locate or create the menu's container here and return it as a jQuery selector. Must be overwritten by sub-
         * classes. Usual approach would be to locate a previously created div in the Django templates by their id.
         *
         * Throws:
         *   SubclassResponsibility
         */
        _setupContainer: function() {
            throw new SubclassResponsibility();
        },

        /**
         * Method: _setupControls
         *
         * Locates menu controls container inside the menu's container and its contained minimize and close buttons.
         * Both of them are optional, but, if present, will be get their minimize or respectively close callback bound.
         *
         * Returns:
         *   The menu controls container as jQuery selector.
         */
        _setupControls: function() {
            var controls = this.container.find('.' + Config.Classes.MENU_CONTROLS);

            controls.find('.' + Config.Classes.MENU_MINIMIZE)
                .addClass('icon-white icon-minus-sign')
                .click(this.minimize.bind(this));

            controls.find('.' + Config.Classes.MENU_CLOSE)
                .addClass('icon-white icon-remove-sign')
                .click(this.hide.bind(this));

            return controls;
        },

        /**
         * Method: _setupDragging
         *
         * Enables the menu container to be dragged around on the canvas. Menus are always above other elements on the
         * canvas and may not leave the canvas. When close to the edges of the canvas, menus snap to its inner edges.
         *
         * Returns:
         *   This {Menu} instance for chaining.
         */
        _setupDragging: function() {
            this.container.draggable({
                containment:   'body',
                stack:         'svg',
                cursor:        Config.Dragging.CURSOR,
                scroll:        false,
                snap:          'body',
                snapMode:      'inner',
                snapTolerance: Config.Dragging.SNAP_TOLERANCE
            });

            return this;
        },

        /**
         * Method: _setupNavbar
         *
         * Locates and returns the editor's navbar.
         *
         * Returns:
         *   The navbar's jQuery selector.
         */
        _setupNavbar: function() {
            return jQuery('ul.nav.pull-right');
        },

        /**
         * Group: Accessors
         */

        /**
         * Method: _isMinimized
         *
         * Returns a boolean flag indicating whether the menu is minimized.
         *
         * Returns:
         *   True if the menu is minimized, false otherwise.
         */
        _isMinimized: function() {
            return typeof this._navbarButton !== 'undefined';
        },

        /**
         * Group: Visibility
         */

        /**
         * Method: disable
         *
         * Disables the menu, meaning it is being hidden and cannot be shown until enabled again.
         *
         * Returns:
         *   This {Menu} instance for chaining.
         */
        disable: function() {
            this._disabled = true;
            this.hide();

            return this;
        },

        /**
         * Method: enable
         *
         * Enables the menu again. It is no implicitly shown again.
         *
         * Returns:
         *   This {Menu} instance for chaining.
         */
        enable: function() {
            this._disabled = false;

            return this;
        },

        /**
         * Method: show
         *
         * Shows the menu's container unless it the menu is minimized or disabled.
         *
         * Returns:
         *   This {Menu} instance for chaining.
         */
        show: function() {
            // prevent that the menu is shown again as long it is minimized
            if (this._isMinimized() || this._disabled) return this;

            this.container.show();
            return this;
        },

        /**
         * Method: hide
         *
         * Hides the menu.
         *
         * Returns:
         *   This {Menu} instance for chaining.
         */
        hide: function() {
            this.container.hide();
            return this;
        },

        /**
         * Method: maximize
         *
         * Maximized the menu on clicking its minimized representation in the navigation bar. Will calculate the
         * position where the menu will be maximized to first (including a 20 pixel offset of the canvas borders) and
         * then animate it over parts of a seconds moving there. This method will also remove the button from the bar.
         *
         * Returns:
         *   This {Menu} instance for chaining.
         */
        maximize: function(eventObject) {
            this._navbarButton.remove();
            this._navbarButton = undefined;

            var destinationTransformation = eventObject.data;
            this.container.show();

            // ensure that maximized menus will be visible (in case the window has been resized)
            destinationTransformation.left = Math.min(
                destinationTransformation.left,
                jQuery(window).width() - this.container.outerWidth() - Config.Menus.MENU_OFFSET
            );
            destinationTransformation.top = Math.min(
                destinationTransformation.top,
                jQuery(window).height() - this.container.outerHeight() - Config.Menus.MENU_OFFSET
            );

            this.container.animate(destinationTransformation, { duration: Config.Menus.ANIMATION_DURATION });

            return this;
        },

        /**
         * 
         * @returns {Menu}
         */
        minimize: function() {
            if (this._isMinimized()) return this;

            // create a button in the toolbar
            this._navbarButton = jQuery('<li><a href="#">' + this.container.attr(Config.Attributes.HEADER) + '</a></li>')
                .css('visibility', 'hidden')
                .prependTo(this._navbar)
                // .offset() here will closure the position where the window was minimized
                .click(this.container.offset(), this.maximize.bind(this));

            // animate the window minimizing towards the navigation button
            var navButtonPosition = this._navbarButton.offset();
            this.container.animate({
                top:    navButtonPosition.top,
                left:   navButtonPosition.left,
                width:  0,
                height: 0
            }, {
                duration: Config.Menus.ANIMATION_DURATION,
                complete: function() {
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
     */
    var ShapeMenu = Menu.extend({
        init: function() {
            this._super();
            this._setupThumbnails();
        },

        /* Section: Internal */
        _setupContainer: function() {
            return jQuery('#' + Config.IDs.SHAPES_MENU);
        },

        _setupThumbnails: function() {
            var svgs = this.container.find('svg');

            // make shapes in the menu draggable
            svgs.draggable({
                helper:   'clone',
                opacity:  Config.Dragging.OPACITY,
                cursor:   Config.Dragging.CURSOR,
                appendTo: 'body',
                revert:   'invalid',
                zIndex:   200
            });
        }

    });

    /**
     * Class: PropertiesMenu
     */
    var PropertiesMenu = Menu.extend({
        _displayOrder: undefined,
        _form:         undefined,
        _node:         undefined,

        init: function(displayOrder) {
            this._super();
            this._displayOrder = displayOrder;
            this._form = this.container.find('.form-horizontal');

            this._setupSelection();
        },

        maximize: function(eventObject) {
            this._super(eventObject);
            this.show();
            return this;
        },

        /* Section: Visibility */
        hide: function() {
            this._node = undefined;
            return this._super();
        },

        show: function() {
            var selected = jQuery('.' + Config.Classes.SELECTED + '.' + Config.Classes.NODE);
            this._removeEntries();

            // display the properties menu only if there is exactly one node selected
            // and the menu is not minimized; otherwise hide the menu
            if (selected.length === 1 && !this._isMinimized() && !this._disabled) {
                return this._show(selected);
            }

            return this.hide();
        },

        _removeEntries: function() {
            if (!this._node) return this;

            _.each(this._node.properties, function(property) {
                property.menuEntry.remove();
            }.bind(this));

            return this;
        },

        _setupContainer: function() {
            return jQuery('#' + Config.IDs.PROPERTIES_MENU);
        },

        _setupSelection: function() {
            jQuery(document).on(Config.Events.CANVAS_SELECTION_STOPPED, this.show.bind(this));

            return this;
        },

        _show: function(selected) {
            this._node = selected.data(Config.Keys.NODE);

            // this node does not have any properties to display, go home!
            if (_.isEmpty(this._node.properties)) {
                this.hide();
                return this;
            }

            _.each(this._displayOrder, function(propertyName) {
                var property = this._node.properties[propertyName];
                // has the node such a property? display it!
                if (typeof property !== 'undefined' && property !== null) {
                    property.menuEntry.appendTo(this._form);

                    jQuery(property).on(Config.Events.PROPERTY_HIDDEN_CHANGED, function(event, hidden) {
                        this.container.toggle(!this._allHidden());
                    }.bind(this));
                }
            }.bind(this));

            // fix the left offset (jQueryUI bug with draggable menus and CSS right property)
            if (this.container.css('left') === 'auto') {
                var offset =  - this.container.outerWidth(true) - Config.Menus.MENU_OFFSET;
                this.container.css('left', jQuery('body').outerWidth(true) + offset);
            }
            this.container.toggle(!_.all(this._node.properties, function(property) { return property.hidden; }));

            return this;
        },

        _allHidden: function() {
            return !this._node || _.all(this._node.properties, function(property) { return property.hidden; });
        }
    });

    return {
        Menu:           Menu,
        ShapeMenu:      ShapeMenu,
        PropertiesMenu: PropertiesMenu
    }
});
