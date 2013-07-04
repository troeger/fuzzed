define(['config'], function(Config) {
    /**
     *  Package Faulttree
     */

    /**
     *  Structure: FaulttreeConfig
     *    Faulttree-specific config.
     *
     *  Extends: <Base::Config>
     */
    return jQuery.extend(true, Config, {
        /**
         *  Group: Events
         *    Name of global events triggered on the document with jQuery.trigger().
         *
         *  Constants:
         *    {String} EDITOR_CALCULATE_CUTSETS               - Event triggered when he 'calculate cutsets' action
         *                                                      has been chosen.
         *    {String} EDITOR_CALCULATE_TOP_EVENT_PROBABILITY - Event triggered when the 'calculate top event
         *                                                      probability' action has been chosen.
         */
        Events: {
            EDITOR_CALCULATE_CUTSETS:               'editor-calculate-cutsets',
            EDITOR_CALCULATE_TOP_EVENT_PROBABILITY: 'editor-calculate-topevent-probability'
        },

        /**
         *  Group: IDs
         *    IDs of certain DOM-elements.
         *
         *  Constants:
         *    {String} CUTSETS_MENU          - The container element of the cutsets menu.
         *    {String} PROBABILITY_MENU      - The container element of the probability menu.
         */
        IDs: {
            CUTSETS_MENU:          'FuzzEdCutsetsMenu',
            PROBABILITY_MENU:      'FuzzEdProbabilityMenu'
        },

        /**
         *  Group: Menus
         *    Menu configurations.
         *
         *  Constants:
         *    {Number} PROBABILITY_MENU_MAX_GRID_HEIGHT - Max. height of the grid that displays the configurations.
         */
        Menus: {
            PROBABILITY_MENU_MAX_GRID_HEIGHT: 500
        }
    });
});
