define(['factory', 'fuzztree/config', 'faulttree/node'], function(Factory, Config, FaulttreeNode) {
    /**
     * Package: Fuzztree
     */

    /**
     * Class: FuzztreeNode
     *      Fuzztree-specific node implementation.
     *
     * Extends: <Faulttree::FaulttreeNode>.
     *
     */
    return FaulttreeNode.extend({
        /**
         * Group: Initialization
         */

        /**
         * Method: _setupProperties
         *      For a general description of this method refer to <Base::Node::_setupProperties>. Fuzztree nodes must
         *      additionally observe changes of the optional property in order to render the node accordingly.
         *
         * Parameters:
         *      {Array[str]} - The order in which to display the properties if present.
         *
         * Returns:
         *      This {<FuzztreeNode>} instance for chaining.
         */
        _setupProperties: function(propertiesDisplayOrder) {
            this._super(propertiesDisplayOrder);
            var optionalProperty = this.properties.optional;

            if (optionalProperty) {
                this.setOptional(optionalProperty.value);
                jQuery(optionalProperty).on(Config.Events.NODE_PROPERTY_CHANGED, function(event, newValue) {
                    this.setOptional(newValue);
                }.bind(this));
            }

            return this;
        },

        /**
         * Group: Accessors
         */

        /**
         * Method: setOptional
         *      Sets the node to be optional in the Fuzztree.
         *
         * Parameters:
         *      {Boolean} optional - optional flag
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        setOptional: function(optional) {
            // mark node optional (or remove mark)
            if (optional) {
                this.container.addClass(this.config.Classes.OPTIONAL);
            } else {
                this.container.removeClass(this.config.Classes.OPTIONAL);
            }

            return this;
        },

        getConfig: function() {
            return Config;
        }
    });
});
