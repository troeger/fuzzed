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
         *    {String} EDITOR_CALCULATE_CUTSETS              - Event triggered when he 'calculate cutsets' action
         *                                                     has been chosen.
         *    {String} EDITOR_CALCULATE_TOPEVENT_PROBABILITY - Event triggered when he 'calculate top event probability'
         *                                                     action has been chosen.
         */
        Events: {
            EDITOR_CALCULATE_CUTSETS:               'editor-calculate-cutsets',
            EDITOR_CALCULATE_TOPEVENT_PROBABILITY:  'editor-calculate-topevent-probability'
        },

        /**
         *  Group: IDs
         *    IDs of certain DOM-elements.
         *
         *  Constants:
         *    {String} CUTSETS_MENU          - The container element of the cutsets menu.
         *    {String} PROBABILITY_MENU      - The container element of the probability menu.
         *    {String} NAVBAR_ACTION_CUTSETS - The navbar actions button for cutsets calculation.
         */
        IDs: {
            CUTSETS_MENU:          'FuzzEdCutsetsMenu',
            PROBABILITY_MENU:      'FuzzEdProbabilityMenu',
            NAVBAR_ACTION_CUTSETS: 'FuzzEdNavbarActionCutsets'
        }
    });
});
