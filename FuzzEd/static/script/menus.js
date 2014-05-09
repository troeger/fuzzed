define(['config', 'class', 'jquery', 'jquery-ui'], function(Config, Class) {

    /**
     * Class: Menu
     */
    var Menu = Class.extend({
        container:    undefined,

        _controls:     undefined,
        _disabled:     undefined,
        _navbar:       undefined,
        _navbarButton: undefined,

        init: function() {
            this.container = this._setupContainer();
            this._controls = this._setupControls();
            this._disabled = false;
            this._navbar   = this._setupNavbar();

            this._setupDragging();
        },

        /* Section: Visibility */
        disable: function() {
            this._disabled = true;
            this.hide();
        },

        enable: function() {
            this._disabled = false;
        },

        hide: function() {
            this.container.hide();
            return this;
        },

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
        },

        maximize: function(eventObject) {
            this._navbarButton.remove();
            this._navbarButton = undefined;

            var destinationTransformation = eventObject.data;

            this.container.show();

            // ensure that maximized menus will be visible (in case the window has been resized)
            destinationTransformation.left =
                Math.min(destinationTransformation.left, jQuery(window).width()  - this.container.outerWidth()  - 10);
            destinationTransformation.top  =
                Math.min(destinationTransformation.top,  jQuery(window).height() - this.container.outerHeight() - 10);

            this.container.animate(destinationTransformation, {
                duration: Config.Menus.ANIMATION_DURATION
            });
            return this;
        },

        show: function() {
            // prevent that the menu is shown again as long it is minimized
            if (this._isMinimized() || this._disabled) return this;

            this.container.show();
            return this;
        },

        /* Section: Internal */
        _isMinimized: function() {
            return typeof this._navbarButton !== 'undefined';
        },

        _setupContainer: function() {
            throw new SubclassResponsibility();
        },

        _setupControls: function() {
            var controls = this.container.find('.' + Config.Classes.MENU_CONTROLS);

            controls.find('.' + Config.Classes.MENU_MINIMIZE)
                .addClass('fa fa-minus-circle')
                .click(this.minimize.bind(this));

            controls.find('.' + Config.Classes.MENU_CLOSE)
                .addClass('fa fa-times-circle')
                .click(this.hide.bind(this));

            return controls;
        },

        _setupDragging: function() {
            this.container.draggable({
                containment:   'document',
                stack:         'svg',
                cursor:        Config.Dragging.CURSOR,
                scroll:        false,
                snap:          'body',
                snapMode:      'inner',
                snapTolerance: Config.Dragging.SNAP_TOLERANCE
            });
        },

        _setupNavbar: function() {
            return jQuery('ul.nav.pull-right');
        }
    });

    /**
     * Class: ShapeMenu
     */
    var ShapeMenu = new (Menu.extend({
        init: function() {
            this._super();
            this._setupThumbnails();
        },

        /* Section: Internal */
        _setupContainer: function() {
            return jQuery('#' + Config.IDs.SHAPES_MENU);
        },

        _setupThumbnails: function() {
			var thumbnails = this.container.find('.' + Config.Classes.DRAGGABLE_WRAP_DIV).children();

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

    }));

    /**
     * Class: PropertiesMenu
     */
    var PropertiesMenu = new (Menu.extend({
        _displayOrder: undefined,
        _form:         undefined,
        _selectee:     undefined,

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

        displayOrder: function(newOrder) {
            if (typeof newOrder === 'undefined') return this._displayOrder;

            this._displayOrder = newOrder;
            return this;
        },

        /* Section: Visibility */
        hide: function() {
            this._removeEntries();
            this._selectee = undefined;
            return this._super();
        },

        show: function() {
            var selected = jQuery('.' + Config.Classes.SELECTED);
            this._removeEntries();

            // display the properties menu only if there is exactly one node selected
            // and the menu is not minimized; otherwise hide the menu
            if (selected.length === 1 && !this._isMinimized() && !this._disabled) {
                return this._show(selected);
            }

            return this.hide();
        },

        _removeEntries: function() {
            if (!this._selectee) return this;

            _.each(this._selectee.properties, function(property) {
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
            if (selected.hasClass(Config.Classes.NODE)) {
                this._selectee = selected.data(Config.Keys.NODE);
            } else if (selected.hasClass(Config.Classes.JSPLUMB_CONNECTOR)) {
                this._selectee = selected.data(Config.Keys.EDGE);
            } else { // if (selected.hasClass(Config.Keys.NODEGROUP
                //TODO: do this right
                this._selectee = selected.parent().parent().data(Config.Keys.NODEGROUP);
            }

            // this node does not have any properties to display, go home!
            if (_.isEmpty(this._selectee.properties)) {
                this.hide();
                return this;
            }

            _.each(this._displayOrder, function(propertyName) {
                var property = this._selectee.properties[propertyName];
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
                var offset =  - this.container.outerWidth(true) - Config.Menus.PROPERTIES_MENU_OFFSET;
                this.container.css('left', jQuery('body').outerWidth(true) + offset);
            }
            this.container.toggle(!_.all(this._selectee.properties, function(property) { return property.hidden; }));

            return this;
        },

        _allHidden: function() {
            return !this._selectee || _.all(this._selectee.properties, function(property) { return property.hidden; });
        }
    }));

    var LayoutMenu = new (Menu.extend({
        _keep: undefined,
        _undo: undefined,

        init: function() {
            this._super();
            this._setupButtons()
                ._setupLayoutRequested()
                .hide();
        },

        keep: function() {
            var deferred = jQuery.Deferred();

            // User has accepted to keep the layout by explicitly clicking the button
            this._keep.click(function() {
                deferred.resolve();
            }.bind(this));

            // User has accepted implicitly by continuing to edit the graph
            jQuery(document).one([
                Config.Events.CANVAS_SHAPE_DROPPED,
                Config.Events.NODE_ADDED,
                Config.Events.NODE_DELETED,
                Config.Events.EDGE_ADDED,
                Config.Events.EDGE_DELETED,
                Config.Events.GRAPH_LAYOUT,
                Config.Events.NODE_PROPERTY_CHANGED
            ].join(' '), function() {
                deferred.resolve();
            }.bind(this));

            // User requested an undo
            this._undo.click(function() {
                deferred.reject();
            }.bind(this));

            return deferred.promise();
        },

        show: function() {
            var viewport = jQuery(window);
            this.container.css({
                top: viewport.height() / 2 - this.container.height() / 2,
                left: viewport.width() / 2 - this.container.width() / 2
            });
            return this._super();
        },

        _setupButtons: function() {
            this._keep = this.container.find('button.btn-primary').add(this._controls.find('.menu-close'));
            this._undo = this.container.find('button.btn-danger');

            return this;
        },

        _setupLayoutRequested: function() {
            jQuery(document).on(Config.Events.GRAPH_LAYOUT, this.show.bind(this));
            jQuery(document).on(Config.Events.GRAPH_LAYOUTED, this.hide.bind(this));
            return this;
        },

        _setupContainer: function() {
            return jQuery('#' + Config.IDs.LAYOUT_MENU);
        }
    }));

    return {
        Menu:           Menu,
        LayoutMenu:     LayoutMenu,
        ShapeMenu:      ShapeMenu,
        PropertiesMenu: PropertiesMenu
    }
});