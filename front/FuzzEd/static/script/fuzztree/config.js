define(['factory', 'faulttree/config', 'jquery'], function(Factory, FaulttreeConfig) {
    /**
     * Package Fuzztree
     */

    /**
     * Structure: FuzztreeConfig
     *      Fuzztree-specific Factory.getModule('Config').
     *
     * Extends: <Faulttree::FaulttreeConfig>
     */
    return jQuery.extend(true, FaulttreeConfig, {
        /**
         * Group: Classes
         *      Names of certain CSS classes.
         *
         * Constants:
         *      {String} OPTIONAL                - Class assigned to optional nodes.
         *      {String} NODE_OPTIONAL_INDICATOR - Class of the optional indicator above a node's image.
         */
        Classes: {
            OPTIONAL:                'optional',
            NODE_OPTIONAL_INDICATOR: 'fuzzed-node-optional-indicator'
        },

        /**
         * Group: Node
         *      Configuration of node (visual) properties.
         *
         * Constants:
         *      {String} OPTIONAL_STROKE-STYLE - SVG dash-array value that optional nodes receive
         */
        Node: {
            OPTIONAL_STROKE_STYLE: '4.8 2' // svg dash-array value
        }
    });
});
