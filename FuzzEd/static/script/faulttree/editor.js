define(['editor', 'faulttree/graph', 'menus', 'faulttree/config', 'highcharts', 'jquery.ui/jquery.ui.resizable', 'slickgrid'],
function(Editor, FaulttreeGraph, Menus, FaulttreeConfig) {
    /**
     *  Package: Faulttree
     */

    /**
     *  Class: CutsetsMenu
     *    A menu for displaying a list of minimal cutsets calculated for the edited graph. The nodes that belong to
     *    a cutset become highlighted when hovering over the corresponding entry in the cutsets menu.
     *
     *  Extends: <Base::Menus::Menu>
     */
    var CutsetsMenu = Menus.Menu.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {Graph} _graph - <Base::Graph> instance for which the cutsets are calculated.
         */
        _graph: undefined,

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Sets up the menu.
         *
         *  Parameters:
         *    {Graph} graph - The <Base::Graph> instance for which the cutsets are calculated.
         */
        init: function(graph) {
            this._super();
            this._graph = graph;
        },

        /**
         *  Group: Actions
         */

        /**
         *  Method: show
         *    Display the given cutsets in the menu and make the menu visible.
         *
         *  Parameters:
         *    {Array} cutsets - A list of cutsets calculated by the backend.
         *
         *  Returns:
         *    This menu instance for chaining.
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
                    return this._graph.getNodeById(id);
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
                        var allNodes = this._graph.getNodes();
                        _.invoke(allNodes, 'disable');
                        _.invoke(nodes, 'highlight');
                    }.bind(this),

                    // out
                    function() {
                        var allNodes = this._graph.getNodes();
                        _.invoke(allNodes, 'enable');
                        _.invoke(nodes, 'unhighlight');
                    }.bind(this)
                );

                listElement.append(entry);
            }.bind(this));

            this._super();
            return this;
        },

        /**
         *  Group: Setup
         */

        /**
         *  Method: _setupContainer
         *    Sets up the DOM container element for this menu and appends it to the DOM.
         *
         *  Returns:
         *    A jQuery object of the container.
         */
        _setupContainer: function() {
            return jQuery(
                '<div id="' + FaulttreeConfig.IDs.CUTSETS_MENU + '" class="menu" header="Cutsets">\
                    <div class="menu-controls">\
                        <span class="menu-minimize"></span>\
                        <span class="menu-close"></span>\
                    </div>\
                    <ul class="nav-list unstyled"></ul>\
                </div>'
            ).appendTo(jQuery('#' + FaulttreeConfig.IDs.CONTENT));
        }
    });

    var ProbabilityMenu = Menus.Menu.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {<Editor>}        _editor            - The <Editor> instance.
         *    {<Job>}           _job               - <Job> instance of the backend job that is responsible for
         *                                           calculating the probability.
         *    {jQuery Selector} _chartContainer    - jQuery reference to the div inside the container containing the chart.
         *    {jQuery Selector} _gridContainer     - jQuery reference to the div inside the container containing the table.
         *    {Highchart}       _chart             - The Highchart instance displaying the result.
         *    {SlickGrid}       _grid              - The SlickGrid instance displaying the result.
         *    {Object}          _configNodeMap     - A dictionary mapping from configuration ID to a set of involved nodes.
         *    {Object}          _redundancyNodeMap - A dictionary mapping from configuration ID to a map of
         *                                           node IDs to N values.
         */
        _editor:            undefined,
        _job:               undefined,
        _chartContainer:    undefined,
        _gridContainer:     undefined,
        _chart:             undefined,
        _grid:              undefined,
        _configNodeMap:     {},
        _redundancyNodeMap: {},

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Sets up the menu.
         */
        init: function(editor) {
            this._super();
            this._editor = editor;
            this._chartContainer = this.container.find('.chart');
            this._gridContainer  = this.container.find('.grid');
        },

        /**
         *  Group: Actions
         */

        /**
         *  Method: show
         *    Display the given job status (and finally its result).
         *
         *  Parameters:
         *    {<Job>} job - The backend job that calculates the probability of the top event.
         *
         *  Returns:
         *    This menu instance for chaining.
         */
        show: function(job) {
            // clear the content
            this._clear();

            job.successCallback = this._evaluateResult.bind(this);
            job.updateCallback  = this._displayProgress.bind(this);
            job.errorCallback   = this._displayNetworkError.bind(this);
            job.queryInterval   = 500;

            this._job = job;
            job.start();

            this._super();
            return this;
        },

        /**
         *  Method: hide
         *    Hide the menu and clear all its content.
         *
         *  Returns:
         *    This menu instance for chaining.
         */
        hide: function() {
            this._super();
            // clear content
            this._clear();

            return this;
        },

        /**
         *  Method: _clear
         *    Clear the content of the menu and cancel any running jobs.
         *
         *  Returns:
         *    This menu instance for chaining.
         */
        _clear: function() {
            if (typeof this._job !== 'undefined') this._job.cancel();
            this._chartContainer.empty();
            this._gridContainer.empty();
            this._chart = null; this._grid = null;
            this._configNodeMap = {};
            this._redundancyNodeMap = {};
        },

        /**
         *  Group: Setup
         */

        /**
         *  Method: _setupContainer
         *    Sets up the DOM container element for this menu and appends it to the DOM.
         *
         *  Returns:
         *    A jQuery object of the container.
         */
        _setupContainer: function() {
            return jQuery(
                '<div id="' + FaulttreeConfig.IDs.PROBABILITY_MENU + '" class="menu" header="Probability of Top Event">\
                    <div class="menu-controls">\
                        <span class="menu-minimize"></span>\
                        <span class="menu-close"></span>\
                    </div>\
                    <div class="chart"></div>\
                    <div class="grid" style="width: 450px; padding-top: 5px;"></div>\
                </div>'
            )
            .appendTo(jQuery('#' + FaulttreeConfig.IDs.CONTENT));
        },

        _setupResizing: function() {
            this.container.resizable({
                minHeight: this.container.height(), // use current height as minimum
                resize: function(event, ui) {
                    // fit all available space with chart
                    this._chartContainer.height(this.container.height() - this._gridContainer.outerHeight());

                    this._chart.setSize(
                        this._chartContainer.width(),
                        this._chartContainer.height(),
                        false
                    );

                    this._gridContainer.width(this._chartContainer.width());
                    this._grid.resizeCanvas();
                }.bind(this)
            });
        },

        /**
         *  Group: Evaluation
         */

        /**
         *  Method: _evaluateResult
         *    Evaluates the job result. Either displays the analysis results or the returned error message.
         *
         *  Parameters:
         *    {JSON} data - Data returned from the backend containing the result of the calculation.
         */
        _evaluateResult: function(data) {
            if (typeof data.errors !== 'undefined' && _.size(data.errors) != 0) {
                // errors is a dictionary with the node ID as key
                //TODO: display validation result at the node
                this._displayValidationErrors(_.values(data.errors));
            } else {
                var chartData = {};
                var tableData = [];
                var configID = "";

                _.each(data['configurations'], function(config, index) {
                    //TODO: better naming?
                    configID = 'Configuration ' + (index + 1);
                    var displayData = this._convertToDisplayFormat(config['alphacuts']);

                    // remember the nodes involved in this config for later highlighting
                    this._configNodeMap[configID] = this._getNodeSetForChoices(config['choices']);

                    // remember the redundancy settings for this config for later highlighting
                    this._redundancyNodeMap[configID] = {};
                    _.each(config['choices'], function(choice, node) {
                        if (choice.type == 'RedundancyChoice') {
                            this._redundancyNodeMap[configID][node] = choice.value;
                        }
                    }.bind(this));

                    chartData[configID] = displayData['series'];
                    // add the name to the statistics for displaying it in a table cell later
                    displayData['statistics']['id'] = configID;
                    tableData.push(displayData['statistics']);
                }.bind(this));

                this._displayResultWithHighcharts(chartData, data['decompositionNumber']);
                this._displayResultWithSlickGrid(tableData);

                this._setupResizing();
            }
        },

        /**
         *  Group: Conversion
         */

        /**
         *  Methods: _convertToDisplayFormat
         *    Converts a data series of a configuration from API JSON to the Highcharts format incl. statistics.
         *
         *  Parameters:
         *    {JSON} configuration - The data series in JSON format (e.g. "{"0.0": [0.2, 0.5], "1.0": [0.4, 0.4]}").
         *
         *  Returns:
         *    An object containing an array-of-arrays representation of the input that can be used by Highcharts to
         *    plot the data ('series'), and the 'min', 'max' and 'peak' probabilities in a 'statistics' field.
         */
        _convertToDisplayFormat: function(configuration) {
            var dataPoints = [];
            var max = 0.0; var min = 1.0; var peak = 0.0; var peakY = 0.0;
            _.each(configuration, function(values, key) {
                var y = parseFloat(key);
                _.each(values, function(x) {
                    dataPoints.push([x, y]);
                    // track statistics
                    if (x < min) min = x;
                    if (x > max) max = x;
                    if (peakY < y) {peakY = y; peak = x}
                });
            });

            var series = _.sortBy(dataPoints, function(point) {
                return point[0];
            });

            return {
                series: series,
                statistics: {
                    min:    min,
                    max:    max,
                    peak:   peak
                }
            }
        },

        _getNodeSetForChoices: function(choices, topNode) {
            // start from top event if not further
            if (typeof topNode === 'undefined') topNode = this._editor.graph.getNodeById(0);
            // get children filtered by choice
            var children = topNode.getChildren();
            var nodes = [topNode];

            if (topNode.id in choices) {
                var choice = choices[topNode.id];

                switch (choice.type) {
                    case 'InclusionChoice':
                        // if this node is not included (optional) ignore it and its children
                        if (!choice.value) {
                            children = [];
                            nodes = [];
                        }
                        break;

                    case 'FeatureChoice':
                        // only pick the chosen child of a feature variation point
                        children = [_.find(children, function(node) {return node.id == choice.value})];
                        break;

                    case 'RedundancyChoice':
                        // do not highlight this node and its children if no child was chosen
                        if (choice.value == 0) {
                            nodes = [];
                            children = [];
                        }
                        break;
                }
            }

            _.each(children, function(child) {
                nodes = nodes.concat(this._getNodeSetForChoices(choices, child));
            }.bind(this));

            return nodes;
        },

        /**
         *  Group: Display
         */

        /**
         *  Method: _displayProgress
         *    Display the job's progress in the menu's body.
         *
         *  Parameters:
         *    {JSON} data - Data returned from the backend with information about the job's progress.
         */
        _displayProgress: function(data) {
            //TODO
            this._chartContainer.text(JSON.stringify(data));
            this._gridContainer.empty();
        },

        /**
         *  Method: _displayResultWithHighcharts
         *    Display the job's result in the menu's body using Highcharts.
         *
         *  Parameters:
         *    {Array} data                - A set of one or more data series to display in the Highchart.
         *    {int}   decompositionNumber - [optional] Number of decompositions of the result. Used for calculating
         *                                  the tick of the y-axis.
         */
        _displayResultWithHighcharts: function(data, decompositionNumber) {
            if (data.length == 0) return;

            decompositionNumber = decompositionNumber || 5;

            var series = [];

            _.each(data, function(cutset, name) {
                series.push({
                    name: name,
                    data: cutset
                });
            });

            var self = this;

            //TODO: This is all pretty hard-coded. Put it into config instead.
            this._chart = new Highcharts.Chart({
                chart: {
                    renderTo: this._chartContainer[0],
                    type:     'line',
                    height:   180
                },

                title: {
                    text: null
                },

                credits: {
                    style: {
                        fontSize: '8px'
                    }
                },

                xAxis: {
                    min: 0,
                    max: 1
                },
                yAxis: {
                    min: 0,
                    max: 1,
                    title: {
                        text: null
                    },
                    tickInterval: 1.0,
                    minorTickInterval: 1.0 / decompositionNumber
                },

                tooltip: {
                    formatter: function() {
                        return '<b>' + this.series.name + '</b><br/>' +
                               '<i>Probability:</i> <b>' + Highcharts.numberFormat(this.x, 5) + '</b><br/>' +
                               '<i>Membership Value:</i> <b>' + Highcharts.numberFormat(this.y, 2) + '</b>';
                    }
                },

                plotOptions: {
                    series: {
                        marker: {
                            radius: 1
                        },
                        events: {
                            // select the corresponding grid row of the hovered series
                            // this will also highlight the corresponding nodes
                            mouseOver: function() {
                                var configID = this.name;
                                _.each(self._grid.getData(), function(dataItem, index) {
                                    if (dataItem.id == configID) {
                                        self._grid.setSelectedRows([index]);
                                    }
                                });
                            },
                            // unselect all grid cells
                            mouseOut: function() {
                                self._grid.setSelectedRows([]);
                            }
                        }
                    }
                },

                series: series
            });
        },

        /**
         *  Method: _displayResultWithSlickGrid
         *    Display the job's result in the menu's body using SlickGrid.
         *
         *  Parameters:
         *    {JSON} data - A set of one or more data series to display in the SlickGrid.
         */
        _displayResultWithSlickGrid: function(data) {
            function shorten(row, cell, value) {
                return Highcharts.numberFormat(value, 5);
            }

            var columns = [
                { id: 'id',   name: 'ID',      field: 'id',   sortable: true },
                { id: 'min',  name: 'Minimum', field: 'min',  sortable: true, formatter: shorten },
                { id: 'peak', name: 'Peak',    field: 'peak', sortable: true, formatter: shorten },
                { id: 'max',  name: 'Maximum', field: 'max',  sortable: true, formatter: shorten }
            ];

            var options = {
                enableCellNavigation:       true,
                enableColumnReorder:        false,
                multiColumnSort:            true,
                autoHeight:                 true,
                forceFitColumns:            true
            }

            this._grid = new Slick.Grid(this._gridContainer, data, columns, options);

            this._grid.setSelectionModel(new Slick.RowSelectionModel());

            // highlight the corresponding nodes if a row of the grid is selected
            this._grid.onSelectedRowsChanged.subscribe(function(e, args) {
                // unhighlight all nodes
                _.invoke(this._editor.graph.getNodes(), 'unhighlight');
                // remove all badges
                _.invoke(this._editor.graph.getNodes(), 'hideBadge');

                // only highlight nodes if one config is selected
                if (args.rows.length == 1) {
                    var configID = args.grid.getDataItem(args.rows[0])['id'];
                    // highlight nodes
                    _.each(this._configNodeMap[configID], function(node) {
                        node.highlight();
                    });
                    // show redundancy values
                    _.each(this._redundancyNodeMap[configID], function(value, nodeID) {
                        var node = this._editor.graph.getNodeById(nodeID);
                        node.showBadge('N=' + value, 'info');
                    }.bind(this))
                }
            }.bind(this));

            // highlight rows on mouse over
            this._grid.onMouseEnter.subscribe(function(e, args) {
                var row = args.grid.getCellFromEvent(e)['row'];
                args.grid.setSelectedRows([row]);
            });
            // unhighlight cells on mouse out
            this._grid.onMouseLeave.subscribe(function(e, args) {
                args.grid.setSelectedRows([]);
            });

            // enable sorting of the grid
            this._grid.onSort.subscribe(function(e, args) {
                var cols = args.sortCols;

                data.sort(function (dataRow1, dataRow2) {
                    for (var i = 0, l = cols.length; i < l; i++) {
                        var field = cols[i].sortCol.field;
                        var sign = cols[i].sortAsc ? 1 : -1;
                        var value1 = dataRow1[field], value2 = dataRow2[field];
                        var result = (value1 == value2 ? 0 : (value1 > value2 ? 1 : -1)) * sign;
                        if (result != 0) {
                            return result;
                        }
                    }
                    return 0;
                });

                this._grid.invalidate();
            }.bind(this));
        },

        /**
         *  Method: _displayValidationErrors
         *    Display all errors that are thrown during graph validation.
         *
         *  Parameters:
         *    {Array} errors - A list of error messages.
         */
        _displayValidationErrors: function(errors) {
            //TODO: This is a temporary solution. Should be replaced by error messages later.

            var list = jQuery('<ul></ul>');
            _.each(errors, function(error) {
                jQuery('<li></li>').text(error).appendTo(list);
            });
            this._chartContainer.html(list);
        },

        /**
         *  Method: _displayNetworkError
         *    Display an error massage resulting from a network error (e.g. 404) in the menu's body.
         */
        _displayNetworkError: function() {
            //TODO: This is a temporary solution. Should be replaced by error messages later.
            this._chartContainer.text("Not found");
        }


    });

    /**
     *  Class: FaultTreeEditor
     *    Faulttree-specific <Base::Editor> class. The fault tree editor distinguishes from the 'normal' editor by
     *    their ability to calculate minimal cutsets for the displayed graph.
     *
     *  Extends: <Base::Editor>
     */
    return Editor.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {<CutsetsMenu>}     cutsetsMenu     - The <CutsetsMenu> instance used to display the calculated minimal cutsets.
         *    {<ProbabilityMenu>} probabilityMenu - The <ProbabilityMenu> instance used to display the probability of the top event.
         */
        cutsetsMenu: undefined,
        probabilityMenu: undefined,

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Sets up the cutset and probability menus in addition to <Base::Editor::init>.
         *
         *  Parameters:
         *    {int} graphId - The ID of the graph that is going to be edited by this editor.
         */
        init: function(graphId) {
            this._super(graphId);

            this.cutsetsMenu = new CutsetsMenu();
            this.probabilityMenu = new ProbabilityMenu(this);

            this._setupCutsetsActionEntry()
                ._setupTobEventProbabilityActionEntry();
        },

        /**
         *  Group: Accessors
         */

        /**
         *  Method: getConfig
         *
         *  Returns:
         *    The <FaulttreeConfig> object.
         *
         *  See also:
         *    <Base::Editor::getConfig>
         */
        getConfig: function() {
            return FaulttreeConfig;
        },

        /**
         *  Method: getGraphClass
         *
         *  Returns:
         *    The <FaulttreeGraph> class.
         *
         *  See also:
         *    <Base::Editor::getGraphClass>
         */
        getGraphClass: function() {
            return FaulttreeGraph;
        },

        /**
         *  Group: Setup
         */

        /**
         *  Method: _setupCutsetsActionEntry
         *    Adds an entry to the actions navbar group for calculating the minimal cutsets for the edited graph.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupCutsetsActionEntry: function() {
            var navbarActionsEntry = jQuery(
                '<li>' +
                    '<a id="' + this.config.IDs.NAVBAR_ACTION_CUTSETS + '" href="#">Calculate cutsets</a>' +
                '</li>');
            this._navbarActionsGroup.append(navbarActionsEntry);

            // register for clicks on the corresponding nav action
            navbarActionsEntry.click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_CALCULATE_CUTSETS,
                    this.cutsetsMenu.show.bind(this.cutsetsMenu)
                );
            }.bind(this));

            return this;
        },

        /**
         *  Method: _setupTobEventProbabilityActionEntry
         *    Adds an entry to the actions navbar group for calculating the probability of the top event.
         *    Clicking will issue an asynchronous backend call which returns a <Job> object that can be queried for
         *    the final result. The job object will be used to initialize the probability menu.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupTobEventProbabilityActionEntry: function() {
            var navbarActionsEntry = jQuery(
                '<li>' +
                    '<a href="#">Calculate top event probability</a>' +
                '</li>');
            this._navbarActionsGroup.append(navbarActionsEntry);

            // register for clicks on the corresponding nav action
            navbarActionsEntry.click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_CALCULATE_TOPEVENT_PROBABILITY,
                    this.probabilityMenu.show.bind(this.probabilityMenu)
                );
            }.bind(this));

            return this;
        }
    });
});
