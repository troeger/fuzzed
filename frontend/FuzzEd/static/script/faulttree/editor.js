define(['editor', 'factory', 'canvas', 'faulttree/graph', 'menus', 'faulttree/analytical_menus', 'faulttree/config', 'faulttree/node_group'],
function(Editor, Factory, Canvas, FaulttreeGraph, Menus, AnalyticalMenus, FaulttreeConfig) {
    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeEditor
     *      Faulttree-specific <Base::Editor> class. The fault tree editor distinguishes from the 'normal' editor by
     *      their ability to calculate minimal cutsets for the displayed graph.
     *
     * Extends: <Base::Editor>
     */
    return Editor.extend({
        /**
         * Group: Members
         *      {<CutsetsMenu>}               cutsetsMenu               - The <CutsetsMenu> instance used to display the
         *                                                                calculated minimal cutsets.
         *      {<AnalyticalProbabilityMenu>} analyticalProbabilityMenu - The <AnalyticalProbabilityMenu> instance used
         *                                                                to display the probability of the top event.
         *      {<SimulatedProbabilityMenu>}  simulatedProbabilityMenu  - The <SimulatedProbabilityMenu> instance used
         *                                                                to display the probability of the top event.
         */
        cutsetsMenu:               undefined,
        analyticalProbabilityMenu: undefined,
        simulatedProbabilityMenu:  undefined,

        /**
         * Group: Setup
         */
        _loadGraphCompleted: function(readOnly) {
            //this.cutsetsMenu     = new AnalyticalMenus.CutsetsMenu(this);
            this.analyticalProbabilityMenu = new AnalyticalMenus.AnalyticalProbabilityMenu(this);
            this.simulatedProbabilityMenu  = new AnalyticalMenus.SimulatedProbabilityMenu(this);

            this._setupCutsetsAction()
                ._setupAnalyticalProbabilityAction()
                ._setupSimulatedProbabilityAction()
                ._setupExportPDFAction()
                ._setupExportEPSAction();

            return this._super(readOnly);
        },

        /**
         * Method: _setupCutsetsAction
         *      Registers the click handler for the 'cut set analysis' menu entry.
         *
         * Returns:
         *      This {<FaulttreeEditor>} instance for chaining.
         */
        _setupCutsetsAction: function() {
            jQuery("#"+Factory.getModule('Config').IDs.ACTION_CUTSETS).click(function() {
                jQuery(document).trigger(
                    Factory.getModule('Config').Events.EDITOR_CALCULATE_CUTSETS,
                    this.cutsetsMenu.show.bind(this.cutsetsMenu)
                );
            }.bind(this));

            return this;
        },

        /**
         *  Method: _setupExportPDFAction
         *      Registers the click handler for the 'export PDF document' menu entry.
         *
         * Returns:
         *      This {<FaulttreeEditor>} instance for chaining.
         */
        _setupExportPDFAction: function() {
            jQuery("#"+Factory.getModule('Config').IDs.ACTION_EXPORT_PDF).click(function() {
                jQuery(document).trigger(
                    Factory.getModule('Config').Events.EDITOR_GRAPH_EXPORT_PDF,
                    function(issues, job_result_url) {
                        this._downloadFileFromURL(job_result_url, 'pdf');

                    }.bind(this)
                )
            }.bind(this));

            return this;
        },

        /**
         * Method: _setupExportEPSAction
         *      Registers the click handler for the 'export EPS document' menu entry.
         *
         * Returns:
         *      This {<FaulttreeEditor>} instance for chaining.
         */
        _setupExportEPSAction: function() {
            jQuery("#"+Factory.getModule('Config').IDs.ACTION_EXPORT_EPS).click(function() {
                jQuery(document).trigger(
                    Factory.getModule('Config').Events.EDITOR_GRAPH_EXPORT_EPS,
                    function(issues, job_result_url) {
                        this._downloadFileFromURL(job_result_url, 'eps');

                    }.bind(this)
                )
            }.bind(this));

            return this;
        },

        /**
         * Method: _setupAnalyticalProbabilityAction
         *      Registers the click handler for the 'analytical analysis' menu entry. Clicking will issue an
         *      asynchronous backend call which returns a <Job> object that can be queried for the final result. The
         *      job object will be used to initialize the analytical probability menu.
         *
         * Returns:
         *      This {<FaulttreeEditor>} instance for chaining.
         */
        _setupAnalyticalProbabilityAction: function() {
            jQuery("#"+Factory.getModule('Config').IDs.ACTION_ANALYTICAL).click(function() {
                jQuery(document).trigger(
                    Factory.getModule('Config').Events.EDITOR_CALCULATE_ANALYTICAL_PROBABILITY,
                    this.analyticalProbabilityMenu.show.bind(this.analyticalProbabilityMenu));
            }.bind(this));

            return this;
        },

        /**
         * Method: _setupSimulatedProbabilityAction
         *      Registers the click handler for the 'simulated analysis' menu entry. Clicking will issue an asynchronous
         *      backend call which returns a <Job> object that can be queried for the final result. The job object will
         *      be used to initialize the simulated probability menu.
         *
         * Returns:
         *      This {<FaulttreeEditor>} instance for chaining.
         */
        _setupSimulatedProbabilityAction: function() {
            jQuery("#"+Factory.getModule('Config').IDs.ACTION_SIMULATED).click(function() {
                jQuery(document).trigger(
                    Factory.getModule('Config').Events.EDITOR_CALCULATE_SIMULATED_PROBABILITY,
                    this.simulatedProbabilityMenu.show.bind(this.simulatedProbabilityMenu));
            }.bind(this));

            return this;
        },

        /**
         * Method: _downloadFileFromURL
         *      Triggers a download of the given resource.
         *
         * Parameters:
         *      {String} url - The URL to the file to be downloaded.
         *
         * Returns:
         *      This {<FaulttreeEditor>} instance for chaining.
         */
        _downloadFileFromURL: function(url, format) {
            //TODO: File is already downloaded in the _query method (job class), maybe first or second download should be prevented if possible.
            window.location = url;
        },

        _setupMenuActions: function() {
            this._super();

            jQuery('#' + Factory.getModule('Config').IDs.ACTION_MIRROR).click(function() {
                this._mirrorSelection();
            }.bind(this));

            return this;
        },

        _updateMenuActions: function() {
            this._super();

            var selectedNodes = this._selectedNodes();

            // mirror is only available when exactly one node is selected and this one is mirrorable
            if (selectedNodes.length == 1 && this._mirrorable(selectedNodes).length == 1) {
                jQuery('#' + Factory.getModule('Config').IDs.ACTION_MIRROR).parent().removeClass('disabled');
            } else {
                jQuery('#' + Factory.getModule('Config').IDs.ACTION_MIRROR).parent().addClass('disabled');
            }
        },

        /**
         * Method: _mirrorable
         *      Filters the given array of elements (Nodes, Edges, NodeGroups) for mirrorable ones.
         *
         * Returns:
         *      An array of elements that are mirrorable.
         */
        _mirrorable: function(elements) {
            return _.filter(elements, function(elem) { return elem.mirrorable });
        },

        _mirrorSelection: function(event) {
            var selected = jQuery('.' + Factory.getModule('Config').Classes.SELECTED + '.' + Factory.getModule('Config').Classes.NODE);

            // we will only mirror the selection, if a single node is selected
            if (selected.length === 1) {
                // temporarily hide the properties menu to avoid, that it shows the newly created node's individual
                //    properties, as it is supposed to show the common properties with it's original node (i.e. the
                //    NodeGroup's properties)
                this.properties.hide();

                var node  = this.graph.getNodeById(selected.data(Factory.getModule('Config').Keys.NODE).id);

                if (!node.mirrorable) return false;

                var mirroredNode = this.graph._mirror(node);

                if (mirroredNode) {
                    // highlight the newly generated node by selecting it
                    this._deselectAll();
                    mirroredNode.select();
                }

                // allow the properties menu to be shown again
                this.properties.show();
            }
            // otherwise do nothing
        }
    });
});
