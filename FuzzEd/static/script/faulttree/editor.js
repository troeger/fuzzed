define(['editor', 'factory', 'canvas', 'faulttree/graph', 'menus', 'faulttree/analytical_menus', 'faulttree/config', 'faulttree/node_group'],
function(Editor, Factory, Canvas, FaulttreeGraph, Menus, AnalyticalMenus, FaulttreeConfig) {
    /**
     * Package: Faulttree
     */

    /**
     * Class: CutsetsMenu
     *      A menu for displaying a list of minimal cutsets calculated for the edited graph. The nodes that belong to a
     *      cutset become highlighted when hovering over the corresponding entry in the cutsets menu.
     *
     * Extends: <Base::Menus::Menu>
     */
    var CutsetsMenu = Menus.Menu.extend({
        /**
         * Group: Members
         *      {Editor} _editor - <Faulttree::Editor> the editor that owns this menu.
         */
        _editor: undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *      Sets up the menu.
         *
         * Parameters:
         *      {Editor} _editor - <Faulttree::Editor> the editor that owns this menu.
         */
        init: function(editor) {
            this._super();
            this._editor = editor;
        },

        /**
         * Method: _setupContainer
         *      Sets up the DOM container element for this menu and appends it to the DOM.
         *
         * Returns:
         *      A {jQuery} set holding the container.
         */
        _setupContainer: function() {
            return jQuery(
                '<div id="' + FaulttreeConfig.IDs.CUTSETS_MENU + '" class="menu" header="Cutsets">\
                    <div class="menu-controls">\
                       <i class="menu-minimize"></i>\
                       <i class="menu-close">   </i>\
                    </div>\
                    <ul class="nav-list unstyled"></ul>\
                </div>'
            ).appendTo(jQuery('#' + FaulttreeConfig.IDs.CONTENT));
        },

        /**
         * Group: Actions
         */

        /**
         * Method: show
         *      Display the given cutsets in the menu and make the menu visible.
         *
         * Parameters:
         *      {Array[Object]} cutsets - A list of cutsets calculated by the backend.
         *
         *  Returns:
         *      This{<Menu>} instance for chaining.
         */
        show: function(cutsets) {
            if (typeof cutsets === 'undefined') {
                this.container.show();
                return this;
            }

            var listElement = this.container.find('ul').empty();

            _.each(cutsets, function(cutset) {
                var nodeIDs = cutset['nodes'];
                var nodes = _.map(nodeIDs, function(id) {
                    return this._editor.graph.getNodeById(id);
                }.bind(this));
                var nodeNames = _.map(nodes, function(node) {
                    return node.name;
                });

                // create list entry for the menu
                var entry = jQuery('<li><a href="#">' + nodeNames.join(', ') + '</a></li>');

                // highlight the corresponding nodes on hover
                entry.hover(
                    // in
                    function() {
                        var disable = _.difference(this._editor.graph.getNodes(), nodes);
                        _.invoke(disable, 'disable');
                        _.invoke(nodes, 'highlight');
                    }.bind(this),

                    // out
                    function() {
                        var enable = _.difference(this._editor.graph.getNodes(), nodes);
                        _.invoke(enable, 'enable');
                        _.invoke(nodes, 'unhighlight');
                    }.bind(this)
                );

                listElement.append(entry);
            }.bind(this));

            this._super();
            return this;
        }
    });

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
            //this.cutsetsMenu     = new CutsetsMenu(this);
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
            jQuery("#"+this.config.IDs.ACTION_CUTSETS).click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_CALCULATE_CUTSETS,
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
            jQuery("#"+this.config.IDs.ACTION_EXPORT_PDF).click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_GRAPH_EXPORT_PDF,
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
            jQuery("#"+this.config.IDs.ACTION_EXPORT_EPS).click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_GRAPH_EXPORT_EPS,
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
            jQuery("#"+this.config.IDs.ACTION_ANALYTICAL).click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_CALCULATE_ANALYTICAL_PROBABILITY,
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
            jQuery("#"+this.config.IDs.ACTION_SIMULATED).click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_CALCULATE_SIMULATED_PROBABILITY,
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

            jQuery('#' + this.config.IDs.ACTION_CLONE).click(function() {
                this._cloneSelection();
            }.bind(this));

            return this;
        },

        _cloneSelection: function(event) {
            var selected = jQuery('.' + this.config.Classes.SELECTED + '.' + this.config.Classes.NODE);

            // we will only clone the selection, if a single node is selected
            if (selected.length === 1) {
                // temporarily hide the properties menu to avoid, that it shows the newly created node's individual
                //    properties, as it is supposed to show the common properties with it's original node (i.e. the
                //    NodeGroup's properties)
                this.properties.hide();

                var node  = this.graph.getNodeById(selected.data(this.config.Keys.NODE).id);

                if (!node.cloneable) return false;

                var clone = this.graph._clone(node);

                if (clone) {
                    // highlight the newly generated node by selecting it
                    this._deselectAll();
                    clone.select();
                }

                // allow the properties menu to be shown again
                this.properties.show();
            }
            // otherwise do nothing
        }
    });
});
