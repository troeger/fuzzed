define(['faulttree/config'], function(FaulttreeConfig) {
    /**
     *  Package Fuzztree
     */

    /**
     *  Structure: FuzztreeConfig
     *    Fuzztree-specific config.
     *
     *  Extends: <Faulttree::FaulttreeConfig>
     */
    return jQuery.extend(true, FaulttreeConfig, {
        /**
         *  Group: Classes
         *    Names of certain CSS classes.
         *
         *  Constants:
         *    {String} NODE_OPTIONAL_INDICATOR - Class of the optional indicator above a node's image.
         */
        Classes: {
            NODE_OPTIONAL_INDICATOR: 'fuzzed-node-optional-indicator'
        },

        /**
         *  Group: Node
         *    Configuration of node (visual) properties.
         *
         *  Constants:
         *    {String} OPTIONAL_INDICATOR_FILL   - Fill color of optional indicators.
         *    {Number} OPTIONAL_INDICATOR_RADIUS - Circle radius of optional indicators.
         *    {Number} OPTIONAL_INDICATOR_STROKE - Stroke width of optional indicators.
         */
        Node: {
            OPTIONAL_INDICATOR_FILL:   '#FFF',
            OPTIONAL_INDICATOR_RADIUS: Math.round(FaulttreeConfig.Grid.SIZE / 10),
            OPTIONAL_INDICATOR_STROKE: 2
        }
    });
});
