define(['editor', 'canvas', 'faulttree/graph', 'menus', 'faulttree/config', 'alerts', 'highcharts', 'jquery-ui', 'slickgrid'],
function(Editor, Canvas, FaulttreeGraph, Menus, FaulttreeConfig, Alerts) {
    /**
     *  Package: Faulttree
     */

    /**
     *  Class: CutsetsMenu
     *∂DOW
     *  A menu for displaying a list of minimal cutsets calculated for the edited graph. The nodes that belong to a
     *  cutset become highlighted when hovering over the corresponding entry in the cutsets menu.
     *
     *  Extends: <Base::Menus::Menu>
     */
    var CutsetsMenu = Menus.Menu.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {Editor} _editor - <Faulttree::Editor> the editor that owns this menu.
         */
        _editor: undefined,

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Sets up the menu.
         *
         *  Parameters:
         *    {Editor} _editor - <Faulttree::Editor> the editor that owns this menu.
         */
        init: function(editor) {
            this._super();
            this._editor = editor;
        },

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
     *  Class: AnalysisResultMenu
     *    _Abstract_ base class for menus that display the results of a analysis performed by the backend.
     *    It contains a chart (currently implemented with Highcharts) and a table area (using SlickGrid).
     *    Subclasses are responsible for providing data formatters and data conversion functions.
     */
    var AnalysisResultMenu = Menus.Menu.extend({
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
         *    {Object}          _configNodeMap     - A dictionary mapping from configuration ID to a set of involved edges.
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
        _configEdgeMap:     {},
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

            job.successCallback  = this._evaluateResult.bind(this);
            job.updateCallback   = this._displayProgress.bind(this);
            job.errorCallback    = this._displayJobError.bind(this);
            job.notFoundCallback = this._displayJobError.bind(this);
            job.queryInterval    = 500;

            this._job = job;
            job.progressMessage = FaulttreeConfig.ProgressIndicator.CALCULATING_MESSAGE;
            job.start();

            this._super();
            return this;
        },

        /**
         *  Method: hide
         *    Hide the menu and clear all its content. Also stops querying for job results.
         *
         *  Returns:
         *    This menu instance for chaining.
         */
        hide: function() {
            this._super();
            // cancel query job
            this._job.cancel();
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
            // reset height in case it was set during grid creation
            this._gridContainer.css('height', '');
            this._chart = null; this._grid = null;
            this._configNodeMap = {};
            this._redundancyNodeMap = {};
        },

        /**
         *  Group: Setup
         */

        /**
         *  Method: _setupContainer
         *    _Abstract_, sets up the DOM container element for this menu and appends it to the DOM.
         *
         *  Returns:
         *    A jQuery object of the container.
         */
        _setupContainer: function() {
            throw new SubclassResponsibility();
        },

        _setupResizing: function() {
            this.container.resizable({
                minHeight: this.container.height(), // use current height as minimum
                maxHeight: this.container.height(),
                resize: function(event, ui) {
                    if (this._chart != null) {
                        // fit all available space with chart
                        this._chartContainer.height(this.container.height() - this._gridContainer.outerHeight());

                        this._chart.setSize(
                            this._chartContainer.width(),
                            this._chartContainer.height(),
                            false
                        );
                    }

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
         *    {string} data - Data returned from the backend containing the result of the calculation.
         */
        _evaluateResult: function(data) {
            data = jQuery.parseJSON(data);

            if (_.size(data.errors) > 0) {
                // errors is a dictionary with the node ID as key
                this._displayValidationErrors(data.errors);
            }

            if (_.size(data.warnings) > 0) {
                // warnings is a dictionary with the node ID as key
                this._displayValidationWarnings(data.warnings);
            }

            if (_.size(data.configurations) > 0) {
                var chartData = {};
                var tableData = [];
                var configID = '';

                _.each(data.configurations, function(config, index) {
                    configID = config['id'];

                    // remember the nodes and edges involved in this config for later highlighting
                    this._collectNodesAndEdgesForConfiguration(configID, config['choices']);

                    // remember the redundancy settings for this config for later highlighting
                    this._redundancyNodeMap[configID] = {};
                    _.each(config['choices'], function(choice, node) {
                        if (choice.type == 'RedundancyChoice') {
                            this._redundancyNodeMap[configID][node] = choice['n'];
                        }
                    }.bind(this));

                    // collect chart data if given
                    if (typeof config['points'] !== 'undefined') {
                        chartData[configID] = _.sortBy(config['points'], function(point){ return point[0] });
                    }

                    // collect table rows
                    // they are basically the configs without the points and choices
                    var tableEntry = config;
                    // delete keys we no longer need
                    tableEntry['points'] = undefined;
                    tableEntry['choices'] = undefined;
                    tableData.push(tableEntry);

                }.bind(this));

                // remove progress bar
                this._chartContainer.empty();
                // only display chart if points were given
                if (_.size(chartData) != 0) {
                    this._displayResultWithHighcharts(chartData, data['decompositionNumber']);
                }
                this._displayResultWithSlickGrid(tableData);

                this._setupResizing();
            } else {
                // close menu again if there are no results
                this.hide();
            }
        },

        /**
         *  Group: Accessors
         */

        /**
         *  Method: _getDataColumns
         *    _Abstract_, returns the format of columns that should be displayed with SlickGrid.
         *
         *  Returns:
         *    An array of column descriptions. See https://github.com/mleibman/SlickGrid/wiki/Column-Options.
         */
        _getDataColumns: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Method: _chartTooltipFormatter
         *    _Abstract_, function used to format the toolip that appears when hovering over a data point in the chart.
         *    The scope object ('this') contains the x and y value of the corresponding point.
         *
         *  Returns:
         *    A string that is displayed inside the tooltip. It may contain HTML tags.
         */
        _chartTooltipFormatter: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Method: _progressMessage
         *    _Abstract_, returns the message that should be displayed while the backend is calculating the result.
         *
         *  Returns:
         *    A string with the message. May contain HTML tags.
         */
        _progressMessage: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Group: Conversion
         */

        /**
         *  Method: _collectNodesAndEdgesForConfiguration
         *    Traverse the graph and collect all nodes and edges which are part of the configuration defined by the
         *    given set of choices. Remember those entities in the <_configNodeMap> and <_configEdgeMap> fields
         *    under the given configID.
         *
         *  Parameters:
         *    {String} configID - The name of the configuration that is used to store the nodes and edges in the maps.
         *    {Array}  choices  - A map from node IDs to choice objects (with 'type' and 'value') used to filter
         *                        the graph entities.
         *    {<Node>} topNode  - [optional] The top node of the graph. Used for recursion. Defaults to the top event.
         */
        _collectNodesAndEdgesForConfiguration: function(configID, choices, topNode) {
            // start from top event if not further
            if (typeof topNode === 'undefined') topNode = this._editor.graph.getNodeById(0);
            // get children filtered by choice
            var children = topNode.getChildren();
            var nodes = [topNode];
            var edges = topNode.incomingEdges;

            if (topNode.id in choices) {
                var choice = choices[topNode.id];

                switch (choice['type']) {
                    case 'InclusionChoice':
                        // if this node is not included (optional) ignore it and its children
                        if (!choice['included']) {
                            children = [];
                            nodes = [];
                            edges = [];
                        }
                        break;

                    case 'FeatureChoice':
                        // only pick the chosen child of a feature variation point
                        children = [_.find(children, function(node) {return node.id == choice['featureId']})];
                        break;

                    case 'RedundancyChoice':
                        // do not highlight this node and its children if no child was chosen
                        if (choice['n'] == 0) {
                            nodes = [];
                            children = [];
                            edges = [];
                        }
                        break;
                }
            }

            this._configNodeMap[configID] = nodes.concat(this._configNodeMap[configID] || []);
            this._configEdgeMap[configID] = edges.concat(this._configEdgeMap[configID] || []);

            // recursion
            _.each(children, function(child) {
                this._collectNodesAndEdgesForConfiguration(configID, choices, child);
            }.bind(this));
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
            if (this._chartContainer.find('.progress').length > 0) return;

            var progressBar = jQuery(
                '<div style="text-align: center;">' +
                    '<p>' + this._progressMessage() + '</p>' +
                    '<div class="progress progress-striped active">' +
                        '<div class="progress-bar" role="progressbar" style="width: 100%;"></div>' +
                    '</div>' +
                '</div>');

            this._chartContainer.empty().append(progressBar);
            this._gridContainer.empty();
        },

        /**
         *  Method: _displayResultWithHighcharts
         *    Display the job's result in the menu's body using Highcharts.
         *
         *  Parameters:
         *    {Array} data  - A set of one or more data series to display in the Highchart.
         *    {int}   yTick - [optional] The tick of the y-axis (number of lines).
         */
        _displayResultWithHighcharts: function(data, yTick) {
            if (data.length == 0) return;

            yTick = yTick || 5;

            var series = [];

            _.each(data, function(cutset, name) {
                series.push({
                    name: name,
                    data: cutset
                });
            });

            // clear container
            this._chartContainer.empty();

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
                    min: -0.05,
                    max:  1.05
                },
                yAxis: {
                    min: 0,
                    max: 1,
                    title: {
                        text: null
                    },
                    tickInterval: 1.0,
                    minorTickInterval: 1.0 / yTick
                },

                tooltip: {
                    formatter: this._chartTooltipFormatter
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
            var columns = this._getDataColumns();

            var options = {
                enableCellNavigation:       true,
                enableColumnReorder:        false,
                multiColumnSort:            true,
                autoHeight:                 true,
                forceFitColumns:            true
            };

            // little workaround for constraining the height of the grid
            var maxHeight = this._editor.getConfig().Menus.PROBABILITY_MENU_MAX_GRID_HEIGHT;
            if ((data.length + 1) * 25 > maxHeight) {
                options.autoHeight = false;
                this._gridContainer.height(maxHeight);
            }

            // clear container
            this._gridContainer.empty();

            // create new grid
            this._grid = new Slick.Grid(this._gridContainer, data, columns, options);

            // make rows selectable
            this._grid.setSelectionModel(new Slick.RowSelectionModel());

            // highlight the corresponding nodes if a row of the grid is selected
            this._grid.onSelectedRowsChanged.subscribe(function(e, args) {
                this._unhighlightConfiguration();

                // only highlight the configuration if only one config is selected
                if (args.rows.length == 1) {
                    var configID = args.grid.getDataItem(args.rows[0])['id'];
                    this._highlightConfiguration(configID);
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
         *  Method: _highlightConfiguration
         *    Highlight all nodes and edges that are part of the given configuration.
         *    Also display the N value on redundancy nodes.
         *
         *  Parameters:
         *    {String} configID - The ID of the configuration that should be highlighted.
         */
        _highlightConfiguration: function(configID) {
            // prevents that node edge anchors are being displayed
            Canvas.container.addClass(FaulttreeConfig.Classes.CANVAS_NOT_EDITABLE);

            // highlight nodes
            _.invoke(this._configNodeMap[configID], 'highlight');
            // highlight edges
            _.invoke(this._configEdgeMap[configID], 'setHover', true);
            // show redundancy values
            _.each(this._redundancyNodeMap[configID], function(value, nodeID) {
                var node = this._editor.graph.getNodeById(nodeID);
                node.showBadge('N=' + value, 'info');
            }.bind(this))
        },

        /**
         *  Method: _unhighlightConfiguration
         *    Remove all highlights from the graph.
         */
        _unhighlightConfiguration: function() {
            // make the anchors visible again
            Canvas.container.removeClass(FaulttreeConfig.Classes.CANVAS_NOT_EDITABLE);

            // unhighlight all nodes
            _.invoke(this._editor.graph.getNodes(), 'unhighlight');
            // unhighlight all edges
            _.invoke(this._editor.graph.getEdges(), 'setHover', false);
            // remove all badges
            _.invoke(this._editor.graph.getNodes(), 'hideBadge');
        },

        /**
         *  Method: _displayValidationErrors
         *    Display all errors that are thrown during graph validation.
         *
         *  Parameters:
         *    {Object} errors - A dictionary of error messages.
         */
        _displayValidationErrors: function(errors) {
            //TODO: This is a temporary solution. Errors should be displayed per node later.
            if (_.size(errors) == 1) {
                Alerts.showErrorAlert('Analysis error: ', errors[0]);
            } else {
                var errorList = '<ul>';
                _.each(errors, function(error) {
                    errorList += '<li>' + error + '</li>';
                });
                errorList += '</ul>'
                Alerts.showErrorAlert('Analysis errors: ', errorList);
            }
        },

        /**
         *  Method: _displayValidationWarnings
         *    Display all warnings that are thrown during graph validation.
         *
         *  Parameters:
         *    {Object} warnings - A dictionary of warning messages.
         */
        _displayValidationWarnings: function(warnings) {
            //TODO: This is a temporary solution. Warnings should be displayed per node later.
            if (_.size(warnings) == 1) {
                Alerts.showWarningAlert('Warning:', warnings[0]);
            } else {
                var warningList = '<ul>';
                _.each(warnings, function(warning) {
                    warningList += '<li>' + warning + '</li>';
                });
                warningList += '</ul>'
                Alerts.showWarningAlert('Multiple warnings returned from analysis:', warningList);
            }
        },

        /**
         *  Method: _displayJobError
         *    Display an error massage resulting from a job error.
         */
        _displayJobError: function(xhr) {
            Alerts.showErrorAlert('An error occurred!', xhr.responseText || 'Are you still connected to the internet? If so it\'s our fault and we are working on it.');
            this.hide();
        }
    });


    /**
     *  Class: AnalyticalProbabilityMenu
     *    The menu responsible for displaying the results of the 'analytical' analysis.
     */
    var AnalyticalProbabilityMenu = AnalysisResultMenu.extend({

        /**
         *  Method: _setupContainer
         *    Sets up the DOM container element for this menu and appends it to the DOM.
         *
         *  Returns:
         *    A jQuery object of the container.
         */
        _setupContainer: function() {
            return jQuery(
                '<div id="' + FaulttreeConfig.IDs.ANALYTICAL_PROBABILITY_MENU + '" class="menu" header="Analysis Results">\
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

        /**
         *  Method: _getDataColumns
         *    _Abstract_, returns the format of columns that should be displayed with SlickGrid.
         *
         *  Returns:
         *    An array of column descriptions. See https://github.com/mleibman/SlickGrid/wiki/Column-Options.
         */
        _getDataColumns: function() {
            function shorten(row, cell, value) {
                return Highcharts.numberFormat(value, 5);
            }

            return [
                { id: 'id',     name: 'Config',     field: 'id',     sortable: true },
                { id: 'min',    name: 'Min',        field: 'min',    sortable: true, formatter: shorten },
                { id: 'peak',   name: 'Peak',       field: 'peak',   sortable: true, formatter: shorten },
                { id: 'max',    name: 'Max',        field: 'max',    sortable: true, formatter: shorten },
                { id: 'costs',  name: 'Costs',      field: 'costs',  sortable: true },
                { id: 'ratio',  name: 'Risk',       field: 'ratio',  sortable: true, minWidth: 150}
            ];
        },

        /**
         *  Method: _chartTooltipFormatter
         *    Function used to format the toolip that appears when hovering over a data point in the chart.
         *    The scope object ('this') contains the x and y value of the corresponding point.
         *
         *  Returns:
         *    A string that is displayed inside the tooltip. It may contain HTML tags.
         */
        _chartTooltipFormatter: function() {
            return '<b>' + this.series.name + '</b><br/>' +
                   '<i>Probability:</i> <b>' + Highcharts.numberFormat(this.x, 5) + '</b><br/>' +
                   '<i>Membership Value:</i> <b>' + Highcharts.numberFormat(this.y, 2) + '</b>';
        },

        /**
         *  Method: _progressMessage
         *    Returns the message that should be displayed while the backend is calculating the result.
         *
         *  Returns:
         *    A string with the message.
         */
        _progressMessage: function() {
            return 'Running probability analysis...';
        }
    });


    /**
     *  Class: SimulatedProbabilityMenu
     *    The menu responsible for displaying the results of the 'analytical' analysis.
     */
    var SimulatedProbabilityMenu = AnalysisResultMenu.extend({

        /**
         *  Method: _setupContainer
         *    Sets up the DOM container element for this menu and appends it to the DOM.
         *
         *  Returns:
         *    A jQuery object of the container.
         */
        _setupContainer: function() {
            return jQuery(
                '<div id="' + FaulttreeConfig.IDs.SIMULATED_PROBABILITY_MENU + '" class="menu" header="Simulation Results">\
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

        /**
         *  Method: _getDataColumns
         *    _Abstract_, returns the format of columns that should be displayed with SlickGrid.
         *
         *  Returns:
         *    An array of column descriptions. See https://github.com/mleibman/SlickGrid/wiki/Column-Options.
         */
        _getDataColumns: function() {
            function shorten(row, cell, value) {
                return Highcharts.numberFormat(value, 5);
            }

            return [
                { id: 'id',          name: 'Config',      field: 'id',          sortable: true },
                { id: 'mttf',        name: 'MTTF',        field: 'mttf',        sortable: true },
                { id: 'reliability', name: 'Reliability', field: 'reliability', sortable: true },
                { id: 'rounds',      name: 'Rounds',      field: 'rounds',      sortable: true },
                { id: 'failures',    name: 'Failures',    field: 'failures',    sortable: true },
                { id: 'costs',       name: 'Costs',       field: 'costs',       sortable: true },
                { id: 'ratio',       name: 'Risk',        field: 'ratio',       sortable: true, minWidth: 150}
            ];
        },

        /**
         *  Method: _chartTooltipFormatter
         *    Function used to format the tooltip that appears when hovering over a data point in the chart.
         *    The scope object ('this') contains the x and y value of the corresponding point.
         *
         *  Returns:
         *    A string that is displayed inside the tooltip. It may contain HTML tags.
         */
        _chartTooltipFormatter: function() {
            //TODO: adapt to JSON format
            return '<b>' + this.series.name + '</b><br/>' +
                   '<i>Probability:</i> <b>' + Highcharts.numberFormat(this.x, 5) + '</b><br/>' +
                   '<i>Membership Value:</i> <b>' + Highcharts.numberFormat(this.y, 2) + '</b>';
        },

        /**
         *  Method: _progressMessage
         *    Returns the message that should be displayed while the backend is calculating the result.
         *
         *  Returns:
         *    A string with the message.
         */
        _progressMessage: function() {
            return 'Running simulation...';
        }
    });


    /**
     *  Class: FaulttreeEditor
     *
     *  Faulttree-specific <Base::Editor> class. The fault tree editor distinguishes from the 'normal' editor by their
     *  ability to calculate minimal cutsets for the displayed graph.
     *
     *  Extends: <Base::Editor>
     */
    return Editor.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {<CutsetsMenu>}               cutsetsMenu               - The <CutsetsMenu> instance used to display the
         *                                                              calculated minimal cutsets.
         *    {<AnalyticalProbabilityMenu>} analyticalProbabilityMenu - The <AnalyticalProbabilityMenu> instance used to
         *                                                              display the probability of the top event.
         *    {<SimulatedProbabilityMenu>} simulatedProbabilityMenu  - The <SimulatedProbabilityMenu> instance used to
         *                                                              display the probability of the top event.
         */
        cutsetsMenu:               undefined,
        analyticalProbabilityMenu: undefined,
        simulatedProbabilityMenu:  undefined,

        /**
         *  Group: Initialization
         */

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

        _loadGraphCompleted: function(readOnly) {
            //this.cutsetsMenu     = new CutsetsMenu(this);
            this.analyticalProbabilityMenu = new AnalyticalProbabilityMenu(this);
            this.simulatedProbabilityMenu  = new SimulatedProbabilityMenu(this);

            this._setupCutsetsAction()
                ._setupAnalyticalProbabilityAction()
                ._setupSimulatedProbabilityAction()
                ._setupExportPDFAction()
                ._setupExportEPSAction();

            return this._super(readOnly);
        },

        /**
         *  Method: _setupCutsetsAction
         *    Registers the click handler for the 'cut set analysis' menu entry.
         *
         *  Returns:
         *    This editor instance for chaining.
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
         *    Registers the click handler for the 'export PDF document' menu entry.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupExportPDFAction: function() {
            jQuery("#"+this.config.IDs.ACTION_EXPORT_PDF).click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_GRAPH_EXPORT_PDF,
                    function(url) {
                        this._downloadFileFromURL(url, 'pdf');
                    }.bind(this)
                )
            }.bind(this));

            return this;
        },

        /**
         *  Method: _setupExportEPSAction
         *    Registers the click handler for the 'export EPS document' menu entry.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupExportEPSAction: function() {
            jQuery("#"+this.config.IDs.ACTION_EXPORT_EPS).click(function() {
                jQuery(document).trigger(
                    this.config.Events.EDITOR_GRAPH_EXPORT_EPS,
                    function(url) {
                        this._downloadFileFromURL(url, 'eps');
                    }.bind(this)
                )
            }.bind(this));

            return this;
        },

        /**
         *  Method: _setupAnalyticalProbabilityAction
         *    Registers the click handler for the 'analytical analysis' menu entry. Clicking will
         *    issue an asynchronous backend call which returns a <Job> object that can be queried for the final result.
         *    The job object will be used to initialize the analytical probability menu.
         *
         *  Returns:
         *    This editor instance for chaining.
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
         *  Method: _setupSimulatedProbabilityAction
         *    Registers the click handler for the 'simulated analysis' menu entry. Clicking will
         *    issue an asynchronous backend call which returns a <Job> object that can be queried for the final result.
         *    The job object will be used to initialize the simulated probability menu.
         *
         *  Returns:
         *    This editor instance for chaining.
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
         *  Method: _downloadFileFromURL
         *    Triggers a download of the given resource. At the moment, it only opens it in the current window.
         *
         *  Parameters:
         *    {String} url - The URL to the file to be downloaded.
         */
        _downloadFileFromURL: function(url, format) {
            //TODO: maybe we can use more sophisticated methods here to get the file to download directly instead
            //      of opening in the same window
            window.location = url;
        },


        /**
         *      !! Temporarily copied code from dfd/editor.js !!
         *      Will be used until halos are implemented and take care of FaultTree NodeGroups.
         */

        _setupMenuActions: function() {
            this._super();

            jQuery('#' + this.config.IDs.ACTION_GROUP).click(function() {
                this._groupSelection();
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_UNGROUP).click(function() {
                this._ungroupSelection();
            }.bind(this));

            // set the shortcut hints from 'Ctrl+' to '⌘' when on Mac
            if (navigator.platform == 'MacIntel' || navigator.platform == 'MacPPC') {
                jQuery('#' + this.config.IDs.ACTION_GROUP + ' span').text('⌘G');
                jQuery('#' + this.config.IDs.ACTION_UNGROUP + ' span').text('⌘U');
            }


            return this;
        },

        _setupKeyBindings: function(readOnly) {
            this._super(readOnly)
            if (readOnly) return this;

            jQuery(document).keydown(function(event) {
                if (event.which === 'G'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._groupPressed(event);
                } else if (event.which === 'U'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._ungroupPressed(event);
                }
            }.bind(this));

            return this;
        },

        _groupPressed: function(event) {
            // prevent that node is being deleted when we edit an input field
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();

            this._groupSelection();

            return this;
        },

        _ungroupPressed: function(event) {
            // prevent that node is being deleted when we edit an input field
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();

            this._ungroupSelection();

            return this;
        }
    });
});
