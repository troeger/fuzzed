define(['factory', 'canvas', 'menus', 'faulttree/config', 'alerts', 'datatables', 'datatables-api', 'faulttree/node_group', 'highcharts', 'jquery-ui'],
function(Factory, Canvas, Menus, FaulttreeConfig, Alerts, DataTables) {
    
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
                '<div id="' + Factory.getModule('Config').IDs.CUTSETS_MENU + '" class="menu" header="Cutsets">\
                    <div class="menu-controls">\
                       <i class="menu-minimize"></i>\
                       <i class="menu-close">   </i>\
                    </div>\
                    <ul class="nav-list unstyled"></ul>\
                </div>'
            ).appendTo(jQuery('#' + Factory.getModule('Config').IDs.CONTENT));
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
    
   /*
    * Abstract Class: AnalysisResultMenu
    *      Base class for menus that display the results of a analysis performed by the backend. It contains a chart
    *      (implemented with Highcharts) and a table area (using DataTables).
    *
    */
   var AnalysisResultMenu = Menus.Menu.extend({
       /**
        * Group: Members 
        *      {<Editor>}        _editor               - The <Editor> instance.
        *      {<Job>}           _job                  - <Job> instance of the backend job that is responsible for
        *                                                calculating the probability.
        *      {jQuery Selector} _graphIssuesContainer - Display
        *      {jQuery Selector} _chartContainer       - jQuery reference to the chart's container.
        *      {jQuery Selector} _tableContainer       - jQuery reference to the table's container.
        *      {Highchart}       _chart                - The Highchart instance displaying the result.
        *      {DataTables}      _table                - The DataTables instance displaying the result.
        *      {Object}          _configNodeMap        - A mapping of the configuration ID to its node set.
        *      {Object}          _configNodeMap        - A mapping of the configuration ID to its edge set.
        *      {Object}          _redundancyNodeMap    - A mapping of the configuration ID to the nodes' N-values
        *      {Object}          _configMetaDataCached - A dictionary indicating if choice meta data for a specific configuration is cached.

        */
       _editor:               undefined,
       _job:                  undefined,
       _graphIssuesContainer: undefined,
       _chartContainer:       undefined,
       _tableContainer:       undefined,
       _chart:                undefined,
       _table:                undefined,
       _configNodeMap:        {},
       _configEdgeMap:        {},
       _redundancyNodeMap:    {},
       _configMetaDataCached: {},
       

       /**
        * Group: Initialization
        */

       /**
        * Constructor: init
        *      Sets up the menu.
        */
       init: function(editor) {
           this._super();
           this._editor = editor;
           this._graphIssuesContainer = this.container.find('.graph_issues');
           this._chartContainer       = this.container.find('.chart');
           this._tableContainer       = this.container.find('.table_container');
       },

       /**
        * Group: Actions
        */

       /**
        * Method: show
        *      Display the given job status its results.
        *
        * Parameters:
        *      {<Job>} job - The backend job that calculates the probability of the top event.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} instance for chaining.
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
           job.progressMessage = Factory.getModule('Config').ProgressIndicator.CALCULATING_MESSAGE;
           job.start();

           this._super();
           return this;
       },

       /**
        * Method: hide
        *      Hide the menu and clear all its content. Also stops querying for job results.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} instance for chaining.
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
        * Method: _clear
        *      Clear the content of the menu and cancel any running jobs.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} instance for chaining.
        */
       _clear: function() {
           if (typeof this._job !== 'undefined') this._job.cancel();
           
           // reset height of the chart container (which is set after resizing event)
           this._chartContainer.height('');
           
           // reset height in case it was set during grid creation
           this._tableContainer.css('min-height', '');
           
           // reset container width (which is set after initalisation of DataTables)
           this.container.css('width','');
           
           this._graphIssuesContainer.empty();
           this._chartContainer.empty();
           this._tableContainer.empty();
           this._chart = null;
           this._table = null;
           this._configNodeMap        = {};
           this._redundancyNodeMap    = {};
           this._configEdgeMap        = {};
           this._configMetaDataCached = {};

           return this;
       },
       
       /**
        * Group: Accessors
        */
      
       /**
        *  Abstract Method: _progressMessage
        *      Should compute the message that is displayed while the backend calculation is pending.
        *
        *  Returns:
        *      A {String} with the message. May contain HTML.
        */
       _progressMessage: function() {
           throw new SubclassResponsibility();
       },
       
       /**
        *  Abstract Method: _menuHeader
        *      Computes the header of the menu.
        *
        *  Returns:
        *      A {String} which is the header of the menu.
        */
       _menuHeader: function() {
           throw new SubclassResponsibility();
       },
       
       /**
        * Method: _containerID
        *      Computes the HTML ID of the container.
        *
        * Returns:
        *      A {String} which is the ID of the Container.
        */
       _containerID: function() {
           throw new SubclassResponsibility();
       },

       /**
        *  Group: Setup
        */

       /**
        * Abstract Method: _setupContainer
        *      Sets up the DOM container element for this menu and appends it to the DOM.
        *
        * Returns:
        *      A jQuery object of the container.
        */
       _setupContainer: function() {
           return jQuery(
               '<div id="' + this._containerID()  + '" class="menu probabillity_menu" header="'+ this._menuHeader() +'">\
                   <div class="menu-controls">\
                       <i class="menu-minimize"></i>\
                       <i class="menu-close"></i>\
                   </div>\
                   <div class="graph_issues"></div>\
                   <div class="chart"></div>\
                   <div class="table_container content"></div>\
               </div>'
           ).appendTo(jQuery('#' + Factory.getModule('Config').IDs.CONTENT));
       },

       /**
        * Method: setupResizing
        *      Enables this menu to be resizable and therefore to enlarge or shrink the calculated analysis results.
        *      Any subclass has to ensure that its particular outcomes adhere to this behaviour.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _setupResizing: function() {
           this.container.resizable({
               minHeight: this.container.outerHeight(), // use current height as minimum
               minWidth : this.container.outerWidth(),
               resize: function(event, ui) {

                   if (this._chart != null) {
                       
                       // fit all available space with chart    
                       this._chartContainer.height(this.container.height() - this._graphIssuesContainer.height() - this._tableContainer.height());
                       
                       this._chart.setSize(
                           this._chartContainer.width(),
                           this._chartContainer.height(),
                           false
                       );
                   }   
               }.bind(this),
               stop: function(event, ui) {
                   // set container height to auto after resizing (because of collapsing elements)
                   this.container.css('height', 'auto');
                   
               }.bind(this)

           });
       },

       /**
        * Group: Evaluation
        */

       /**
        * Method: _evaluateResult
        *      Evaluates the job result. Either displays the analysis results or the returned error message.
        *
        * Parameters:
        *      {String} data           - Data returned from the backend containing global graph issues,
        *                                configuration data for Highcharts, as well as column definitions for DataTables.
        *
        *      {String} job_result_url - URL for accessing the job result (configuration data).
        *
        */
       _evaluateResult: function(data, job_result_url) {
           
           data   = jQuery.parseJSON(data);
           var issues = data.issues;
           
           if (issues){
               if (_.size(issues.errors) > 0 || _.size(issues.warnings) > 0){
                   this._displayGraphIssues(issues.errors, issues.warnings);
               }
           }
               
           // remove progress bar
           this._chartContainer.empty();
           var axisTitles = data.axis_titles;
           this._initializeHighcharts(axisTitles);
          
           
           // display results within a table
           var columns = data.columns;
           this._displayResultWithDataTables(columns, job_result_url);
           
           
       },

       /**
        * Method: _chartTooltipFormatter
        *      This function is used to format the tooltip that appears when hovering over a data point in the chart.
        *      The scope object ('this') contains the x and y value of the corresponding point.
        *
        *  Returns:
        *      A {String} that is displayed inside the tooltip. It may HTML.
        */
       _chartTooltipFormatter: function() {
           return '<b>' + this.series.name + '</b><br/>' +
                  '<i>Probability:</i> <b>' + Highcharts.numberFormat(this.x, 5) + '</b><br/>' +
                  '<i>Membership Value:</i> <b>' + Highcharts.numberFormat(this.y, 2) + '</b>';
       },

       /**
        * Group: Conversion
        */

       /**
        *  Method: _collectNodesAndEdgesForConfiguration
        *      Traverses the graph and collects all nodes and edges which are part of the configuration defined by the
        *      given set of choices. Remember those entities in the <_configNodeMap> and <_configEdgeMap> fields
        *      using the given configID.
        *
        * Parameters:
        *      {String}         configID - The id of the configuration that is used to store the nodes and edges.
        *      {Array[Object]}  choices  - A map from node IDs to choice objects (with 'type' and 'value') used to
        *                                  filter the graph entities.
        *      {<Node>}         topNode  - [optional] The top node of the graph. Used for recursion. Defaults to the
        *                                  top event.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
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

           return this;
       },

       /**
        * Group: Display
        */

       /**
        * Method: _displayProgress
        *      Display the job's progress in the menu's body.
        *
        * Parameters:
        *      {Object} data - Data returned from the backend with information about the job's progress.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _displayProgress: function(data) {
           if (this._chartContainer.find('.progress').length > 0) return this;

           var progressBar = jQuery(
               '<div style="text-align: center;">' +
                   '<p>' + this._progressMessage() + '</p>' +
                   '<div class="progress progress-striped active">' +
                       '<div class="progress-bar" role="progressbar" style="width: 100%;"></div>' +
                   '</div>' +
               '</div>');

           this._chartContainer.empty().append(progressBar);
           this._tableContainer.empty();

           return this;
       },
       
       /**
        * Method: _initializeHighcharts
        *      Intialize highcharts with Axis definitions.
        *
        * Parameters:
        *    {Array[Object]} axis_defititions  - A set of definitions used in Highcharts initialisation.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _initializeHighcharts: function(axis_definitions) { 
           var self = this;
                       
           this._chart = new Highcharts.Chart({
               chart: {
                   renderTo: this._chartContainer[0],
                   type:     'line',
                   height:   Factory.getModule('Config').AnalysisMenu.HIGHCHARTS_MIN_HEIGHT,

               },
               title: {
                   text: null
               },
               credits: {
                   style: {
                       fontSize: Factory.getModule('Config').AnalysisMenu.HIGHCHARTS_CREDIT_LABEL_SIZE
                   }
               },
               xAxis: axis_definitions.xAxis,
               yAxis: axis_definitions.yAxis,
               tooltip: {
                   formatter: this._chartTooltipFormatter
               },
               plotOptions: {
                   series: {
                       marker: {
                           radius: Factory.getModule('Config').AnalysisMenu.HIGHCHARTS_POINT_RADIUS
                       },
                       events: {
                           mouseOver : function () {
                               var config_id = this.name
                               var row = self._table.fnFindCellRowNodes(config_id, 0);
                               jQuery(row).addClass('tr_hover');
                           },
                           mouseOut  : function () {
                               var config_id = this.name
                               var row = self._table.fnFindCellRowNodes(config_id, 0);
                               jQuery(row).removeClass('tr_hover');
                           },
                       }
                   }
               },
               data: []
           });
           
           return this;
       },
       
       /**
        * Method: _displaySeriesWithHighcharts
        *      Draw series within the Highcharts diagram. 
        *
        * Parameters:
        *    {Array[Object]} defititions  - A set of one or more data series to display in the Highchart.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _displaySeriesWithHighcharts: function(data){
           // remove series from the last draw
           while(this._chart.series.length > 0){
               this._chart.series[0].remove(false);
           }
           
           var series = [];
           _.each(data, function(cutset, name) {
               series.push({
                   name: name,
                   data: cutset
               });
           });
           
           // draw series
           _.each(series, function(config){
               this._chart.addSeries(config, false, false)
           }.bind(this));
           
           this._chart.redraw();
           
           return this;
       },
             
       /**
        * Method: _displayResultWithDataTables
        *      Display the job's result with DataTables Plugin. Configuration Issues are printed inside the table as collapsed row. 
        *
        * Parameters:
        *     {Array[Object]}  columns        - A set of columns that shall be displayed within the table.
        *     {String}         job_result_url - URL under which the server delivers configurations for a specific analysis result (using ajax and pagingation)
        *    
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _displayResultWithDataTables: function(columns, job_result_url) {
           
           // clear container
           this._tableContainer.html('<table id="results_table" class="results_table table table-hover content"></table>');            
           
           var collapse_column = {
                                   "class":          'details-control',
                                   "orderable":      false,
                                   "data":           null,
                                   "defaultContent": '',
                                   "bSortable":      false
                                 };
                                 
           columns.push(collapse_column);
           
           //formating function for displaying configuration warnings/errors
           var format = function (issues) {
                   
                   var errors   = issues['errors'] || [];
                   var warnings = issues['warnings'] || [];
                   
                   return this._displayIsussuesList(errors, warnings);
           }.bind(this);
           
           this._table = jQuery('#results_table').dataTable({
                           "bProcessing":   true,
                           "bFilter":       false,
                           "bServerSide":   true,
                           "sAjaxSource":   job_result_url,
                           "aoColumns":     columns,
                           "bLengthChange": false,
                           "iDisplayLength": Factory.getModule('Config').AnalysisMenu.RESULTS_TABLE_MAX_ROWS,
                           "fnDrawCallback": function(oSettings) {
                               
                               var serverData = oSettings['json'];
                               var totalRecords = serverData['iTotalRecords'];
                              
                               if(totalRecords < 2){
                                    // unbind sorting events if there are less than 2 rows
                                   this._tableContainer.find('th').removeClass().unbind('click.DT');    
                               }
                               
                               if(totalRecords <= Factory.getModule('Config').AnalysisMenu.RESULTS_TABLE_MAX_ROWS){
                                    // remove pagination elements if only one page is displayed
                                    this._tableContainer.find('div.dataTables_paginate').css('display', 'none');
                                    this._tableContainer.find('div.dataTables_info').css('display', 'none');
                               }
                               
                               // display points with highchart after table was rendered
                               var configurations = serverData['aaData'];
                               var chartData = {}; 
                                _.each(configurations, function(config) {
                                    var configID = config['id'] || '';
                                    
                                    // collect chart data if given
                                    if (typeof config['points'] !== 'undefined') {
                                        chartData[configID] = _.sortBy(config['points'], function(point){ return point[0] });
                                    }
                                }.bind(this));
                                
                                if (_.size(chartData) != 0) {
                                    this._displaySeriesWithHighcharts(chartData);
                                }
                                else{
                                    this._chart.setSize (0, 0, false);
                                }     
                               }.bind(this),
                           "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull) {
                               
                               // Callback is executed for each row (each row is one configuration)
                                               
                               var current_config = aData;
                               var configID = current_config['id'];
                                                   
                               if ('choices' in current_config ){
                                   var choices  = aData['choices'];
                                   
                                   // check if config meta data is alredy cached 
                                   if (this._configMetaDataCached[configID] !== true){
                                       // remember the nodes and edges involved in this config for later highlighting
                                       this._collectNodesAndEdgesForConfiguration(configID, choices);
                                   
                                   
                                       // remember the redundancy settings for this config for later highlighting
                                       this._redundancyNodeMap[configID] = {};
                                       _.each(choices, function(choice, node) {
                                           if (choice.type == 'RedundancyChoice') {
                                               this._redundancyNodeMap[configID][node] = choice['n'];
                                           }
                                       }.bind(this));
                                       
                                       this._configMetaDataCached[configID] = true;
                                   }
                                   
                                   jQuery(nRow).on("mouseover", function(){    
                                           this._highlightConfiguration(configID);                                                
                                    }.bind(this));
                                    
                                    
                                    jQuery(nRow).on("mouseleave", function(){    
                                           this._unhighlightConfiguration();                                                
                                    }.bind(this));
                               }
                               
                               /* Sample Configuration issues
                               if (iDisplayIndex == 0){
                                   current_config["issues"] = { "errors": [{"message": "map::at", "issueId": 0, "elementId": ""}]};
                               } else if (iDisplayIndex == 1){
                                   current_config["issues"] = { "warnings": [{"message": "Ignoring invalid redundancy configuration with k=-2 N=0", "issueId": 0, "elementId": "3"}]};
                               } else if (iDisplayIndex == 2){
                                    current_config["issues"] = { "errors": [{"message": "map::at", "issueId": 0, "elementId": ""},{"message": "error error error", "issueId": 0, "elementId": ""}, {"message": "another error", "issueId": 0, "elementId": ""}], "warnings": [{"message": "Ignoring invalid redundancy configuration with k=-2 N=0", "issueId": 0, "elementId": "3"}, {"message": "another warning", "issueId": 0, "elementId": "3"}] };
                               }*/
                               
                               if ('issues' in current_config){
                                   var issues = current_config['issues'];
                                   
                                   jQuery(nRow).find('td.details-control').append('<i class="fa fa-exclamation-triangle"></i>');
                                   // Add event listener for opening and closing details
                                   jQuery(nRow).on('click', function () {
                                       var tr  = jQuery(nRow);
                                       var row = this._table.api().row(tr);

                                       if ( row.child.isShown() ) {
                                           // This row is already open - close it
                                           row.child.hide();
                                       }
                                       else {
                                           // Open this row
                                           row.child(format(issues)).show();
                                       }
                                   }.bind(this));
                                   
                                   if ('errors' in issues){
                                       jQuery(nRow).addClass('danger');
                                   }
                                   else if ('warnings' in issues){
                                       jQuery(nRow).addClass('warning');
                                   }
                               }
                               else{
                                   // if row is not collapsable show default pointer
                                   jQuery(nRow).css('cursor', 'default');
                               } 
                           }.bind(this),
                                            
                           "fnInitComplete": function(oSettings, json) {  
                                   this._setupResizing();
                                   // set minumum height of grid as the height of the first draw of the grid
                                   this._tableContainer.css('min-height', this._tableContainer.height());
                                   // keep container width when switching the page (-> otherwise jumping width when switching)
                                   this.container.css('width', this.container.width());
                                   
                               }.bind(this)    
                           });
            
           return this;
       },
       
       /**
        *  Method: _highlightConfiguration
        *      Highlights all nodes, edges and n-values that are part of the given configuration on hover.
        *
        *  Parameters:
        *      {String} configID - The ID of the configuration that should be highlighted.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _highlightConfiguration: function(configID) {
           // prevents that node edge anchors are being displayed
           Canvas.container.addClass(Factory.getModule('Config').Classes.CANVAS_NOT_EDITABLE);

           // highlight nodes
           _.invoke(this._configNodeMap[configID], 'highlight');
           // highlight edges
           _.invoke(this._configEdgeMap[configID], 'highlight');
           // show redundancy values
           _.each(this._redundancyNodeMap[configID], function(value, nodeID) {
               var node = this._editor.graph.getNodeById(nodeID);
               node.showBadge('N=' + value, 'info');
           }.bind(this));

           return this;
       },

       /**
        *  Method: _unhighlightConfiguration
        *      Remove all hover highlights handler currently attached.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _unhighlightConfiguration: function() {
           // make the anchors visible again
           Canvas.container.removeClass(Factory.getModule('Config').Classes.CANVAS_NOT_EDITABLE);

           // unhighlight all nodes
           _.invoke(this._editor.graph.getNodes(), 'unhighlight');
           // unhighlight all edges
           _.invoke(this._editor.graph.getEdges(), 'unhighlight');
           // remove all badges
           _.invoke(this._editor.graph.getNodes(), 'hideBadge');

           return this;
       },
       
       /**
        * Method: _displayGraphIssues
        *      Display all warnings/errors that are thrown during graph validation.
        *
        * Parameters:
        *      {Object} warnings - An array of warning objects.
        *      {Object} errors   - An array of error objects.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _displayGraphIssues: function(errors, warnings) {

           var num_errors   = _.size(errors);
           var num_warnings = _.size(warnings);
           
           var alert_container = jQuery('<div class="alert"><i class="fa fa-exclamation-triangle"></i></div>')
           
           if (num_errors > 0){
               alert_container.addClass('alert-error');                
           } else if(num_warnings >0){
               alert_container.addClass('alert-warning');  
           } else{
               alert_container.addClass('alert-success');  
           }
           
           var issues_heading   = jQuery('<a class="alert-link">\
                                           Errors: ' + num_errors + '&nbsp;&nbsp;&nbsp;\
                                           Warnings: ' + num_warnings +
                                         '</a>');
                                           
           var issues_details   = jQuery('<div class="collapse">' + this._displayIsussuesList(errors, warnings) + '</div>');
           
           alert_container.append(issues_heading).append(issues_details);
           
           // collapse error/warning messages details after clicking on the heading
           issues_heading.click(function(){
               issues_details.collapse('toggle');
           });
           
          this._graphIssuesContainer.append(alert_container);

          return this;
       },
       
       
       /**
        * Method: _displayIsussuesList
        *      Display all errors/warnings in a HTML unordered list.
        *
        * Parameters:
        *      {Object} warnings - An array of warning objects.
        *      {Object} errors   - An array of error objects.
        *
        * Returns:
        *     {String} contains HTML with error/warning messages.
        */
       _displayIsussuesList: function(errors, warnings){
           var html_errors   = '';
           var html_warnings = '';
                  
           
           if(_.size(errors) > 0){
               _.each(errors, function(error){
                   html_errors += '<li>' + error['message'] + '</li>';
               });
               html_errors = '<li><strong>Errors:</strong></li><ul>' + html_errors + '</ul>';  
           }
           
            if(_.size(warnings) > 0){        
               _.each(warnings, function(warning){
                   html_warnings += '<li>' + warning['message'] + '</li>';
               });
               html_warnings = '<li><strong>Warnings:</strong></li><ul>' + html_warnings + '</ul>';
           }
                           
           return '<ul>' + 
                       html_errors + 
                       html_warnings + 
                  '</ul>';
                     
       },
       
       /**
        * Method: _displayJobError
        *      Display an error massage resulting from a job error.
        *
        * Returns:
        *      This {<AnalysisResultMenu>} for chaining.
        */
       _displayJobError: function(xhr) {
           Alerts.showErrorAlert(
               'An error occurred!', xhr.responseText ||
               'We were trying to trigger a computational job, but this crashed on our side. A retry may help. The developers are already informed, sorry for the inconvinience.');
           this.hide();
       }
   });


   /**
    *  Class: AnalyticalProbabilityMenu
    *      The menu responsible for displaying analysis results.
    *
    *  Extends: {<AnalyticalResultMenu>}
    */
   var AnalyticalProbabilityMenu = AnalysisResultMenu.extend({
       /**
        * Method: _containerID
        *      Override of the abstract base class method.
        */
       _containerID: function() {
           return Factory.getModule('Config').IDs.ANALYTICAL_PROBABILITY_MENU;
       },
       
       /**
        * Method: _progressMessage
        *      Override of the abstract base class method.
        */
       _progressMessage: function() {
           return 'Running probability analysis...';
       },
       
       /**
        * Method: _menuHeader
        *      Override of the abstract base class method.
        */
       _menuHeader: function() { 
           return 'Analysis Results';
       }
   });


   /**
    * Class: SimulatedProbabilityMenu
    *      The menu responsible for displaying simulation results.
    *
    * Extends: AnalysisResultMenu
    */
   var SimulatedProbabilityMenu = AnalysisResultMenu.extend({      
       /**
        * Method: _containerID
        *      Override of the abstract base class method.
        */
       _containerID: function() {
           return Factory.getModule('Config').IDs.SIMULATED_PROBABILITY_MENU;
       },
       
       /**
        * Method: _progressMessage
        *      Override of the abstract base method.
        */
       _progressMessage: function() {
           return 'Running simulation...';
       },
       
       /**
        * Method: _menuHeader
        *      Override of the abstract base class method.
        */
       _menuHeader: function() { 
           return 'Simulation Results';
       }
   });
    
    return{
        AnalyticalProbabilityMenu : AnalyticalProbabilityMenu,
        SimulatedProbabilityMenu  : SimulatedProbabilityMenu,
        CutsetsMenu               : CutsetsMenu
    } 
});
