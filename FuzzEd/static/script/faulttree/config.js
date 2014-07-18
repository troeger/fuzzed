define(['config', 'jquery'], function(Config) {
    /**
     * Package Faulttree
     */

    /**
     * Structure: FaulttreeConfig
     *      Faulttree-specific config.
     *
     * Extends: <Base::Config>
     */
    return jQuery.extend(true, Config, {
        Classes: {
            AFFECTED:                'affected'
        },
        /**
         * Group: Events
         *      Name of global events triggered on the document with jQuery.trigger().
         *
         *  Constants:
         *      {String} EDITOR_CALCULATE_CUTSETS                - Event triggered when he 'calculate cutsets' action
         *                                                         has been chosen.
         *      {String} EDITOR_CALCULATE_ANALYTICAL_PROBABILITY - Event triggered when the 'analytical probability'
         *                                                         action has been chosen.
         *      {String} EDITOR_CALCULATE_SIMULATED_PROBABILITY  - Event triggered when the 'simulated probability'
         *                                                         action has been chosen.
         *      {String} EDITOR_GRAPH_EXPORT_PDF                 - Event triggered when the 'export as PDF' action has
         *                                                         been chosen.
         *      {String} EDITOR_GRAPH_EXPORT_EPS                 - Event triggered when the 'export as EPS' action has
         *                                                         been chosen.
         */
        Events: {
            EDITOR_CALCULATE_CUTSETS:                'editor-calculate-cutsets',
            EDITOR_CALCULATE_ANALYTICAL_PROBABILITY: 'editor-calculate-analytical-probability',
            EDITOR_CALCULATE_SIMULATED_PROBABILITY:  'editor-calculate-simulated-probability',
            EDITOR_GRAPH_EXPORT_PDF:                 'editor-export-pdf',
            EDITOR_GRAPH_EXPORT_EPS:                 'editor-export-eps'
        },

        /**
         * Group: IDs
         *      IDs of certain DOM-elements.
         *
         * Constants:
         *      {String} CUTSETS_MENU                - The container element of the cutsets menu.
         *      {String} ACTION_CUTSETS              - The list element that contains the cut set analysis menu entry.
         *      {String} ACTION_ANALYTICAL           - The list element that contains the analytical analysis menu entry
         *      {String} ACTION_SIMULATED            - The list element that contains the simulated analysis menu entry.
         *      {String} ANALYTICAL_PROBABILITY_MENU - The container element of the analytical probability menu.
         *      {String} SIMULATED_PROBABILITY_MENU  - The container element of the simulated probability menu.
         */
        IDs: {
            CUTSETS_MENU:                'FuzzEdCutsetsMenu',
            ACTION_CUTSETS:              'FuzzEdActionCutsets',
            ACTION_ANALYTICAL:           'FuzzEdActionAnalytical',
            ACTION_SIMULATED:            'FuzzEdActionSimulated',
            ACTION_CLONE:                'FuzzEdActionClone',
            ANALYTICAL_PROBABILITY_MENU: 'FuzzEdAnalyticalProbabilityMenu',
            SIMULATED_PROBABILITY_MENU:  'FuzzEdSimulatedProbabilityMenu'
        },

        /**
         * Group: AnlysisMenu
         *      Configurations for results table, as well as highcharts diagram within the analysis results menu. 
         *
         * Constants:
         *      {Number} RESULTS_TABLE_MAX_ROWS       - Max. number of configurations that can be dispayed within one page in the analysis results table.
         *
         *      {Number} HIGHCHARTS_MIN_HEIGHT        - Min. height of the highcharts container.
         *      {Number} HIGHCHARTS_X_MIN             - Min. value on the X axis.
         *      {Number} HIGHCHARTS_X_MAX             - Max. value on the X axis.
         *      {Number} HIGHCHARTS_Y_MIN             - Min value on the Y axis.
         *      {Number} HIGHCHARTS_Y_MAX             - Max value on the Y axis.
         *      {Number} HIGHCHARTS_Y_TICK_INTERVAL   - Interval in which values are labeled on the Y axis.
         *      {Number} HIGHCHARTS_POINT_RADIUS      - Radius of probabillity points drawn in the coordinate system.
         *      {String} HIGHCHARTS_CREDIT_LABEL_SIZE - Font size of the highcharts credit label.
         *
         *
         */
        AnalysisMenu: {
            RESULTS_TABLE_MAX_ROWS: 10,
            
            HIGHCHARTS_MIN_HEIGHT: 140,
            HIGHCHARTS_X_MIN:-0.05,
            HIGHCHARTS_X_MAX:1.05,
            HIGHCHARTS_Y_MIN:0, 
            HIGHCHARTS_Y_MAX:1.0,
            HIGHCHARTS_Y_TICK_INTERVAL:1.0,
            HIGHCHARTS_POINT_RADIUS:1,
            HIGHCHARTS_CREDIT_LABEL_SIZE:'8px'
        }
    });
});
