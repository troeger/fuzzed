define(['config', 'canvas', 'class'], function(Config, Canvas, Class) {
    /**
     * Package: Base
     */

    /**
     * Class: Mirror
     *
     * Mirrors are the small text boxes above or below the image of a node. They are used to display the value of a
     * node's property directly next to its image without the need to look it up in the properties menu. Mirror's sole
     * purpose is visualization, meaning that they do not allow edit operations.
     */
    return Class.extend({
        /**
         * Group: Members
         *
         * Properties:
         *   {DOMElement} container    - This is the mirror's container element that holds the actual content.
         *   {String}     prefix       - A constant string that is always prepended to the show content (default: '').
         *   {String}     suffix       - A constant string that is always appended to the show content (default: '').
         *
         *   {DOMElement} _containment - The DOM element that the mirror is attached to - i.e. <Node::container>.
         */
        container:    undefined,
        prefix:       undefined,
        suffix:       undefined,

        _containment: undefined,

        /**
         * Constructor: init
         *
         * This method constructs a new mirror object. It embeds its visualization in the passed containment DOM
         * element. Additionally, the mirror may also be configured using the properties parameter. The following
         * options are read: {String} prefix, {String} suffix, {String} position (possible values: 'top', 'bottom'),
         * {Array[String]} style (possible values in array: 'bold', 'italic', 'large').
         *
         * Parameters:
         *   {DOMElement} containment - The DOM element that will contain the mirror's DOM elements.
         *   {Objects}    properties  - Object with mirror configuration options. See description above for details.
         */
        init: function(containment, properties) {
            this._containment = containment;
            this.container    = jQuery('<span>').addClass(Config.Classes.MIRROR)
                // The label is double the grid/node's width to allow for large textual content. Since the mirror is
                // already partially centered (see CSS), we only need to offset the container by a quarter of its size.
                // In order to not cover the grid lines behind the mirror box, we need to down size the box by the
                // grid's stroke.
                .css('width', Canvas.gridSize * 2 - Config.Grid.STROKE_WIDTH * 4)
                .css('margin-left', -(Canvas.gridSize / 2) + Config.Grid.STROKE_WIDTH);

            this.prefix = properties.prefix || '';
            this.suffix = properties.suffix || '';

            // style the mirror's visualization - i.e. bold, italic or larger text
            _.each(properties.style, function(style) {
                if (style === 'italic') this.container.addClass(Config.Classes.MIRROR_ITALIC);
                if (style === 'bold')   this.container.addClass(Config.Classes.MIRROR_BOLD);
                if (style === 'large')  this.container.addClass(Config.Classes.MIRROR_LARGE);
            }.bind(this));

            // add the mirror to the containment at specified position (bottom [default] or top)
            if (typeof properties.position === 'undefined' || properties.position === 'bottom')
                this._containment.append(this.container);
            else if (properties.position === 'top')
                this._containment.prepend(this.container);
            else
                throw '[VALUE ERROR] unknown mirror position: ' + properties.position;
        },

        /**
         * Method: show
         *
         * This method allows to change the text of the mirror to the one specified in the method's only parameter. If
         * the mirror was configured to add a prefix/suffix, this will be done here automatically. If the text
         * parameter is a falsy value, the mirror will be hidden, until the show method is called again with a truthy
         * value.
         *
         * Parameters:
         *   {String} text - The text to show in the mirror (without prefix/suffix)
         *
         * Returns:
         *   This {Mirror} instance for chaining.
         */
        show: function(text) {
            if (typeof text === 'undefined' || text === null) {
                this.container.css('display', 'none');
            } else {
                // remove 'display: none' from element to show it again
                // '.show()' won't work because this sets display to 'inline', but we need 'block'
                this.container.css('display', '');
                this.container.html(this.prefix + text + this.suffix);
            }

            return this;
        }
    });
});
