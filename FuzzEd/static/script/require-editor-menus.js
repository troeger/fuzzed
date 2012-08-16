define(['require-config', 'require-oop'], function(Config, Class) {

    /**
     * Class: Menu
     */
    var Menu = Class.extend({

        _container: undefined,

        init: function() {
            this._setupDragging();
        },

        _setupDragging: function() {
            this._container.draggable({
                containment:   '#' + Config.IDs.CONTENT,
                stack:         '.' + Config.Classes.NODE,
                cursor:        Config.Dragging.CURSOR,
                scroll:        false,
                snap:          '#' + Config.IDs.CONTENT,
                snapMode:      'inner',
                snapTolerance: Config.Dragging.SNAP_TOLERANCE
            });
        }
    });


    /**
     * Class: ShapeMenu
     */
    var ShapeMenu = Menu.extend({

        _shapes: undefined,

        init: function() {
            this._container = jQuery('#' + Config.IDs.SHAPES_MENU);
            this._shapes = jQuery('#' + Config.IDs.SHAPES_MENU);

            this._setupThumbnails();

            this._super();
        },

        /* Section: Internal */

        _setupThumbnails: function() {
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

    });

    /**
     * Class: PropertiesMenu
     */
    var PropertiesMenu = Menu.extend({

        _list: undefined,

        init: function() {
            this._container = jQuery('#' + Config.IDs.PROPERTIES_MENU);
            this._list = this._container.find('.ui-listview');

            this._setupDragging();

            this._super();
        },

        /* Section: Visibility */

        hide: function() {
            this._container.hide();

            _.each(this._nodes, function(node, index) {
                _.each(node.properties(), function(property) {
                    property.hide();
                })
            });
            this._list.children(':not(:eq(0))').remove();

            delete this._nodes;
        },

        show: function(nodes, force) {
            if (!_.isArray(nodes)) this._nodes = [nodes];
            else                   this._nodes =  nodes;

            if (force || typeof(this._nodes) === 'undefined' || _.any(this._nodes, function(node) { return node.properties().length > 0})) {
                this._container.show();

                _.each(this._nodes, function(node) {
                    var frame = this._makePropertyFrame(node)
                    this._list.append(frame);

                    _.each(node.properties(), function(property) {
                        property.show(frame.children('form'));
                    }.bind(this));
                }.bind(this));

                this._list.listview('refresh');
            }

            return this;
        },

        /* Section: Internals */

        _makePropertyFrame: function(node) {
            var li    = jQuery('<li>');

            var title = jQuery('<h3>')
                .html(node.name())
                .appendTo(li);

            var form  = jQuery('<form>')
                .attr('action', '#')
                .attr('method', 'get')
                .addClass(Config.Classes.PROPERTIES)
                .appendTo(li)
                .keydown(function(eventObject) {
                    if (eventObject.which === jQuery.ui.keyCode.ENTER) {
                        eventObject.preventDefault();
                        return false;
                    }
                });

            return li;
        }
    });

    return {
        ShapeMenu: ShapeMenu,
        PropertiesMenu: PropertiesMenu
    }
});