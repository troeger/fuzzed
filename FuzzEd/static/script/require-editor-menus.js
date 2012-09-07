define(['require-config', 'require-oop', 'json!config/fuzztree.json'], 
        function(Config, Class, FuzztreeConfig) {

    /**
     * Class: Menu
     */
    var Menu = Class.extend({
        _container: undefined,

        init: function() {
            this._container = this._setupContainer();
            this._setupDragging();
        },

        _setupContainer: function() {
            throw '[ABSTRACT] Override in subclass';
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

    return {
        ShapeMenu:      ShapeMenu,
        PropertiesMenu: PropertiesMenu
    }
});