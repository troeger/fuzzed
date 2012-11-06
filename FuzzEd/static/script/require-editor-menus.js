define(['require-config', 'require-oop', 'json!notations/fuzztree.json'],
        function(Config, Class, FuzztreeConfig) {

    /**
     * Class: Menu
     */
    var Menu = Class.extend({
        _container:    undefined,
        _controls:     undefined,
        _navbar:       undefined,
        _navbarButton: undefined,

        init: function() {
            this._container = this._setupContainer();
            this._controls  = this._setupControls();
            this._navbar    = this._setupNavbar();

            this._setupDragging();
        },

        /* Section: Visibility */
        hide: function() {
            this._container.hide();
            return this;
        },

        minimize: function() {
            if (this._isMinimized()) return this;

            // create a button in the toolbar
            this._navbarButton = jQuery('<li><a href="#">' + this._container.attr(Config.Attributes.HEADER) + '</a></li>')
                .css('visibility', 'hidden')
                .prependTo(this._navbar)
                // .offset() here will closure the position where the window was minimized
                .click(this._container.offset(), this.maximize.bind(this));

            // animate the window minimizing towards the navigation button
            var navButtonPosition = this._navbarButton.offset();
            this._container.animate({
                top:    navButtonPosition.top,
                left:   navButtonPosition.left,
                width:  0,
                height: 0
            }, {
                duration: Config.Menus.ANIMATION_DURATION,
                complete: function() {
                    this._navbarButton.css('visibility', '');
                    this._container.hide();
                    // width and height have to be remove here so that the css will fall back to auto
                    // so that changes to the bounding box of the menu will be reflected when maximizing
                    this._container.css('width', '');
                    this._container.css('height', '');
                }.bind(this)
            });
            return this;
        },

        maximize: function(eventObject) {
            this._navbarButton.remove();
            this._navbarButton = undefined;

            var destinationTransformation = _.extend({
                // those lines might seem weird but they are very necessary
                // if the window changed its bounding box while being minimized (e.g. properties menu)
                // we need to capture this change here first...
                width:  this._container.width(),
                height: this._container.height()
            }, eventObject.data);

            // ... then we resize the window to zero...
            this._container.width(0);
            this._container.height(0);
            this._container.show();

            // ... so that this animation can finally resize it back to the captured value :O
            this._container.animate(destinationTransformation, {
                duration: Config.Menus.ANIMATION_DURATION
            });
            return this;
        },

        show: function() {
            // prevent that the menu is shown again as long it is minimized
            if (this._isMinimized()) return this;

            this._container.show();
            return this;
        },

        /* Section: Internal */
        _isMinimized: function() {
            return typeof this._navbarButton !== 'undefined';
        },

        _setupContainer: function() {
            throw '[ABSTRACT] Override in subclass';
        },

        _setupControls: function() {
            var controls = this._container.find('.' + Config.Classes.MENU_CONTROLS);

            controls.find('.' + Config.Classes.MENU_MINIMIZE)
                .addClass('icon-white icon-minus-sign')
                .click(this.minimize.bind(this));

            controls.find('.' + Config.Classes.MENU_CLOSE)
                .addClass('icon-white icon-remove-sign')
                .click(this.hide.bind(this));

            return controls;
        },

        _setupDragging: function() {
            this._container.draggable({
                containment:   'body',
                stack:         'svg',
                cursor:        Config.Dragging.CURSOR,
                scroll:        false,
                snap:          'body',
                snapMode:      'inner',
                snapTolerance: Config.Dragging.SNAP_TOLERANCE
            });
        },

        _setupNavbar: function() {
            return jQuery('ul.nav');
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
            var svgs = this._container.find('svg');

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
        _form:      undefined,

        init: function() {
            this._super();
            this._form = this._container.find('form');
        },

        maximize: function(eventObject) {
            this._navbarButton.remove();
            this._navbarButton = undefined;

            this.show(this._nodes);
            this._container.animate(eventObject.data, {
                duration: Config.Menus.ANIMATION_DURATION
            });
            return this;
        },

        /* Section: Visibility */
        hide: function() {
            this._container.hide();

            _.each(this._nodes, function(node) {
                _.each(node.propertyMenuEntries, function(menuEntry) {
                    // TODO: remove me, here fordev purposes (the if)
                    if (typeof menuEntry === 'undefined') return;
                    menuEntry.hide();
                })
            });
            delete this._nodes;

            return this;
        },

        show: function(nodes, force) {

            if (!_.isArray(nodes)) this._nodes = [nodes];
            else                   this._nodes =  nodes;

            if (this._haveEntries(this._nodes) || force) {
                _.each(this._nodes, function(node) {
                    _.each(FuzztreeConfig.propertiesDisplayOrder, function(property) {
                        var menuEntry = node.propertyMenuEntries[property];

                        if (typeof menuEntry !== 'undefined') {
                            menuEntry.show(this._form);
                        }
                    }.bind(this));
                }.bind(this));

                if (this._isMinimized()) return this;

                // fix the left offset (jQueryUI bug with draggable and right)
                if (this._container.css('left') === 'auto') {
                    var offset =  - this._container.outerWidth(true) - Config.Menus.PROPERTIES_MENU_OFFSET;
                    this._container.css('left', jQuery('body').outerWidth(true) + offset);
                }

                this._container.show();
            }

            return this;
        },

        _haveEntries: function(nodes) {
            return _.any(nodes, function(node) {
                return !(_.isEmpty(node.propertyMenuEntries));
            })
        },

        _setupContainer: function() {
            return jQuery('#' + Config.IDs.PROPERTIES_MENU);
        }
    });

    /**
     * Class: CutsetsMenu
     */
    var CutsetsMenu = Menu.extend({
        init: function(editor) {
            this._super();
            this._editor = editor;
        },

        displayCutsets: function(cutsets) {
            var listElement = this._container.find('ul');
            listElement.empty();

            _.each(cutsets, function(cutset) {
                var nodeIDs = cutset['nodes'];
                var nodes = _.map(nodeIDs, function(id) {
                    return this._editor.graph().getNodeById(id);
                }.bind(this));
                var nodeNames = _.map(nodes, function(node) {
                    return node.name;
                })

                // create list entry for the menu
                var entry = jQuery('<li><a href="#">' + nodeNames.join(', ') + '</a></li>');

                // highlight the corresponding nodes on hover
                entry.hover(
                    // in
                    function() {
                        var allNodes = this._editor._nodes;
                        _.invoke(allNodes, 'disable');
                        _.invoke(nodes, 'highlight');
                    }.bind(this),

                    // out
                    function() {
                        var allNodes = this._editor._nodes;
                        _.invoke(allNodes, 'enable');
                        _.invoke(nodes, 'highlight', false);
                    }.bind(this)
                );

                listElement.append(entry);
            }.bind(this));
        },

        /* Section: Internal */
        _setupContainer: function() {
            return jQuery('#' + Config.IDs.CUTSETS_MENU);
        }
    });

    return {
        ShapeMenu:      ShapeMenu,
        PropertiesMenu: PropertiesMenu,
        CutsetsMenu:    CutsetsMenu
    }
});