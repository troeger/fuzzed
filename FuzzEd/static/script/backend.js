define(['class', 'config', 'job', 'alerts', 'progressIndicator', 'jquery'], function (Class, Config, Job, Alerts, Progress) {

    /**
     * Class: Backend
     *
     * This small helper class is responsible for handling the communication with the Backend and so synchronize changes
     * in the graph. The implementation is event driven. This means this helper will listen on custom events triggered
     * by other entities and make according AJAX requests. Direct invocation of synchronization calls is highly
     * discouraged in all cases. There should be always only Backend instance at the same time in existence to avoid
     * data duplication in the backend.
     */
    return Class.extend({
        /**
         * Group: Members
         *
         * Properties:
         *   {Number} _graphId - The ID of the graph the Backend will synchronize changes for.
         */
        _graphId: undefined,

        /**
         * Constructor: init
         *
         * Creates a new Backend instance and will capture the passed graphId.
         *
         * Parameters:
         *   {Number} graphId - The ID of the graph the Backend will synchronize changes for.
         */
        init: function(graphId) {
            this._graphId = graphId;
        },

        /**
         * Section: State
         */

        /**
         * Method: activate
         *
         * Tells a <Backend> instance to start synchronizing changes. There MUST be one invocation off this method as
         * data synchronization is turned off by default. Registers AJAX synchronization calls for all custom events
         * listed below.
         *
         * On:
         *   <Config::Events::PROPERTY_CHANGED>
         *   <Config::Events::GRAPH_NODE_ADDED>
         *   <Config::Events::GRAPH_NODE_DELETED>
         *   <Config::Events::GRAPH_EDGE_DELETED>
         *   <Config::Events::EDITOR_CALCULATE_CUTSETS>
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        activate: function() {
            jQuery(document)
                .on(Config.Events.PROPERTY_CHANGED,    this.nodePropertyChanged.bind(this))
                .on(Config.Events.GRAPH_NODE_ADDED,         this.graphNodeAdded.bind(this))
                .on(Config.Events.GRAPH_NODE_DELETED,       this.graphNodeDeleted.bind(this))
                .on(Config.Events.GRAPH_EDGE_ADDED,         this.graphEdgeAdded.bind(this))
                .on(Config.Events.GRAPH_EDGE_DELETED,       this.graphEdgeDeleted.bind(this))
                .on(Config.Events.EDITOR_GRAPH_EXPORT_PDF,  this.graphExport.bind(this))
                .on(Config.Events.EDITOR_GRAPH_EXPORT_EPS,  this.graphExport.bind(this))
                .on(Config.Events.EDITOR_CALCULATE_CUTSETS, this.calculateCutsets.bind(this))
                .on(Config.Events.EDITOR_CALCULATE_TOP_EVENT_PROBABILITY, this.calculateTopEventProbability.bind(this));
            return this;
        },

        /**
         * Method: deactivate
         *
         * An invocation of this method will turn off all data synchronization with the Backend. Therefore un-registers
         * all handlers for custom synchronization events.
         *
         * Off:
         *   <Config::Events::PROPERTY_CHANGED>
         *   <Config::Events::GRAPH_NODE_ADDED>
         *   <Config::Events::GRAPH_NODE_DELETED>
         *   <Config::Events::GRAPH_EDGE_DELETED>
         *   <Config::Events::EDITOR_CALCULATE_CUTSETS>
         *
         * Returns:
         *   This {<Backend>} instance for chaining.
         */
        deactivate: function() {
            jQuery(document)
                .off(Config.Events.PROPERTY_CHANGED)
                .off(Config.Events.GRAPH_NODE_ADDED)
                .off(Config.Events.GRAPH_NODE_DELETED)
                .off(Config.Events.GRAPH_EDGE_ADDED)
                .off(Config.Events.GRAPH_EDGE_DELETED)
                .off(Config.Events.EDITOR_GRAPH_EXPORT_PDF)   
                .off(Config.Events.EDITOR_GRAPH_EXPORT_EPS)                
                .off(Config.Events.EDITOR_CALCULATE_CUTSETS)
                .off(Config.Events.EDITOR_CALCULATE_TOP_EVENT_PROBABILITY);
            return this;
        },

        /**
         * Section: Handlers
         */

        /**
         * Method: graphEdgeAdded
         *
         * Adds a new edge from a given source node to a given target node.
         *
         * Parameters:
         *   {Event}    event        - jQuery event object of the custom trigger.
         *   {Number}   edgeId       - ID of the edge.
         *   {Number}   sourceNodeId - Source node of the new edge.
         *   {Number}   targetNodeId - Target node of the new edge.
         *   {function} success      - [optional] Will be called when the request was successful. Provides e.g. the ID
         *                             of the new edge.
         *   {function} error        - [optional] Callback that gets called in case of an ajax-error.
         *   {function} complete     - [optional] Callback that is invoked in both cases - a successful or an erroneous
         *                             AJAX request.
         */
        graphEdgeAdded: function(event, edgeId, sourceNodeId, targetNodeId, success, error, complete) {
            var data = {
                id:          edgeId,
                source:      sourceNodeId,
                destination: targetNodeId
            };

            var xhr = jQuery.ajax({
                url:      this._fullUrlForEdges(),
                type:     'POST',
                dataType: 'json',

                data:     data,
                success:  success  || jQuery.noop,
                error:    function(jqXHR, errorStatus, errorThrown) {
                    var message = errorThrown || 'Could not connect to backend.';
                    Alerts.showErrorAlert('Edge could not be saved:', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                },
                complete: complete || jQuery.noop,

                beforeSend: function(xhr) {
                    // set messages for progress indicator
                    xhr.progressMessage        = 'Saving…';
                    xhr.progressSuccessMessage = 'Saved';
                    xhr.progressErrorMessage   = 'Not saved!';
                }
            });

            return this;
        },

        /**
         * Method: graphNodeAdded
         *
         * Adds a new node to the backend of this graph.
         *
         * Parameters:
         *   {Event}    event    - jQuery event object of the custom trigger.
         *   {Number}   nodeId   - The node ID.
         *   {String}   kind     - The node kind.
         *   {Number}   x        - The grid x coordinate where the node was added.
         *   {Number}   y        - The grid y coordinate where the node was added.
         *   {function} success  - [optional] Will be called on successful node creation transmission to server.
         *   {function} error    - [optional] Callback that gets called in case of an ajax-error.
         *   {function} complete - [optional] Callback that is invoked when the ajax request completes successful or
         *                         erroneous.
         */
        graphNodeAdded: function(event, nodeId, kind, x, y, success, error, complete) {
            var data = {
                id:   nodeId,
                kind: kind,
                x:    x,
                y:    y
            };

            var xhr = jQuery.ajax({
                url:      this._fullUrlForNodes(),
                type:     'POST',
                dataType: 'json',

                data:     data,
                success:  success  || jQuery.noop,
                error:    function(jqXHR, errorStatus, errorThrown) {
                    var message = errorThrown || 'Could not connect to backend.';
                    Alerts.showErrorAlert('Node could not be created:', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                },
                complete: complete || jQuery.noop,

                beforeSend: function(xhr) {
                    // set messages for progress indicator
                    xhr.progressMessage        = 'Saving…';
                    xhr.progressSuccessMessage = 'Saved';
                    xhr.progressErrorMessage   = 'Not saved!';
                }
            });

            return this;
        },

        /**
         * Method: graphEdgeDeleted
         *   Deletes a given edge in the backend.
         *
         * Parameters:
         *   {Event}    event    - jQuery event object of the custom trigger.
         *   {Number}   edgeId   - The ID of the edge that should be deleted.
         *   {function} success  - [optional] Function that is invoked when the AJAX request was successful.
         *   {function} error    - [optional] Callback that gets called in case of an AJAX error.
         *   {function} complete - [optional] Callback that gets invoked in both cases - a successful and an errornous
         *                         AJAX call.
         */
        graphEdgeDeleted: function(event, edgeId, success, error, complete) {
            var xhr = jQuery.ajax({
                url:      this._fullUrlForEdge(edgeId),
                type:     'DELETE',
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    function(jqXHR, errorStatus, errorThrown) {
                    var message = jqXHR.responseText || errorThrown || 'Could not connect to backend.';
                    Alerts.showErrorAlert('Edge could not be deleted:', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                },
                complete: complete || jQuery.noop,

                beforeSend: function(xhr) {
                    // set messages for progress indicator
                    xhr.progressMessage        = 'Saving…';
                    xhr.progressSuccessMessage = 'Saved';
                    xhr.progressErrorMessage   = 'Not saved!';
                }
            });

            return this;
        },

        /**
         * Method: graphNodeDeleted
         *
         * Deletes a given node in the backend.
         *
         * Parameters:
         *   {Event}    event    - jQuery event object of the custom trigger.
         *   {Number}   nodeId   - The ID of the node that should be deleted.
         *   {function} succes   - [optional] Callback that is being called on successful deletion on backend.
         *   {function} error    - [optional] Callback that gets called in case of an ajax-error.
         *   {function} complete - [optional] Callback that is invoked in both cases, successful and errornous requests.
         */
        graphNodeDeleted: function(event, nodeId, success, error, complete) {
            var xhr = jQuery.ajax({
                url:      this._fullUrlForNode(nodeId),
                type:     'DELETE',
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    function(jqXHR, errorStatus, errorThrown) {
                    var message = jqXHR.responseText || errorThrown || 'Could not connect to backend.';
                    Alerts.showErrorAlert('Node could not be deleted:', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                },
                complete: complete || jQuery.noop,

                beforeSend: function(xhr) {
                    // set messages for progress indicator
                    xhr.progressMessage        = 'Saving…';
                    xhr.progressSuccessMessage = 'Saved';
                    xhr.progressErrorMessage   = 'Not saved!';
                }
            });

            return this;
        },

        /**
         * Method: nodePropertyChanged
         *
         * Changes the properties of a given node.
         *
         * Parameters:
         *   {Event}    event      - jQuery event object of the custom trigger.
         *   {Number}   nodeId     - The node that shall be moved.
         *   {Object}   properties - The node's properties that should be changed. Keys stand for property names and
         *                           their assigned values is the new state.
         *   {function} success    - [optional] Callback that is called when the move was successfully saved.
         *   {function} error      - [optional] Callback that gets called in case of an AJAX error.
         *   {function} complete   - [optional] Callback that is always invoked no matter if AJAX request was successful
         *                           or erroneous.
         */
        nodePropertyChanged: function(event, nodeId, properties, success, error, complete) {
            var xhr = jQuery.ajax({
                url:      this._fullUrlForNode(nodeId),
                type:     'POST',
                data:{
                    properties: JSON.stringify(properties)
                },
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    function(jqXHR, errorStatus, errorThrown) {
                    var message = jqXHR.responseText || errorThrown || 'Could not connect to backend.';
                    Alerts.showErrorAlert('Node could not be changed:', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                },
                complete: complete || jQuery.noop,

                beforeSend: function(xhr) {
                    // set messages for progress indicator
                    xhr.progressMessage        = 'Saving…';
                    xhr.progressSuccessMessage = 'Saved';
                    xhr.progressErrorMessage   = 'Not saved!';
                }
            });

            return this;
        },

        /**
         * Method: getGraph
         *
         * Fetch a graph JSON object from the backend.
         *
         * Parameters:
         *   {function} success  - [optional] Callback function for a successful asynchronous request for JSON
         *                         representing a graph with given id.
         *   {function} error    - [optional] Callback that gets called in case of an unsuccessful retrieval of the
         *                         graph from the database. Will create a new graph in the backend anyway.
         *   {function} complete - [optional] Callback that gets invoked in either a successful or erroneous request.
         */
        getGraph: function(success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForGraph(),
                dataType: 'json',
                // don't show progress
                global:   false,

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /**
         * Method: calculateCutsets
         *
         * Ask the backend to calculate the minimal cutsets.
         *
         * Parameters:
         *   {Event}    event    - jQuery event object of the custom trigger.
         *   {function} success  - [optional] Callback that is called when the calculation was successful.
         *   {function} error    - [optional] Callback that gets called in case of an AJAX error.
         *   {function} complete - [optional] Callback that gets invoked in both; successful or erroneous request.
         */
        calculateCutsets: function(event, success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForCutsets(),
                dataType: 'json',
                // don't show progress
                global:   false,

                success:  success  || jQuery.noop,
                error:    function(jqXHR, errorStatus, errorThrown) {
                    var message = jqXHR.responseText || errorThrown || 'Could not connect to backend.';
                    Alerts.showErrorAlert('Failed to calculate cutsets:', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                },
                complete: complete || jQuery.noop
            });

            return this;
        },

        /**
         *  Method: calculateTopEventProbability
         *    Tell the backend to calculate the probability of the top event. This is an asynchronous request, i.e. the
         *    success callback will get a <Job> object it can use to receive the final result.
         *
         *  Parameters:
         *    {Function} success  - [optional] Callback function that will receive the <Job> object if the job submission
         *                          was successful.
         *    {Function} error    - [optional] Callback that gets called in case of an error.
         *    {Function} complete - [optional] Callback that gets invoked in either a successful or erroneous request.
         */
        calculateTopEventProbability: function(event, success, error, complete) {
            jQuery.ajax({
                url:    this._fullUrlForTopEventProbability(),
                // don't show progress
                global: false,

                statusCode: {
                    201: function(data, status, req) {
                        var jobUrl = req.getResponseHeader('location');
                        if (typeof success !== 'undefined') {
                            success(new Job(jobUrl));
                        }
                    }
                },

                error: function(jqXHR, errorStatus, errorThrown) {
                    var message = jqXHR.responseText || errorThrown || 'Could not connect to backend.';
                    Alerts.showErrorAlert('Error:\n', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                },
                complete: complete || jQuery.noop
            });
        },

        /**
         *  Method: graphExport
         *    Starts a <Job> for exporting and eventually downloading the graph in the specified file format.
         *    The file format depends on the type of the triggering event.
         *    This method will spawn a <Job> that frequently queries the backend for the exported file and returns
         *    the URL to the file if successful. The progress indicator will reflect the file generation progress.
         *
         *  Parameters:
         *    {Function} success - Callback function that receives the URL to the generated file.
         *    {Function} error   - [optional] Callback function that gets called in case of an error (either during
         *                         job creation or an error in the job itself).
         */
        graphExport: function(event, success, error) {
            var progressID = _.uniqueId('export_');
            var fileType;
            if (event.type == Config.Events.EDITOR_GRAPH_EXPORT_PDF) fileType = 'PDF';
            if (event.type == Config.Events.EDITOR_GRAPH_EXPORT_EPS) fileType = 'EPS';
            var progressMessage = Config.ProgressIndicator.EXPORT_PROGRESS_MESSAGE + fileType;
            var progressSuccessMessage = Config.ProgressIndicator.EXPORT_SUCCESS_MESSAGE;
            var progressErrorMessage = Config.ProgressIndicator.EXPORT_ERROR_MESSAGE + fileType;

            jQuery.ajax({
                url:    this._fullUrlForExport(event),
                // don't show progress
                global: false,
                beforeSend: function() {
                    Progress.showProgress(progressID, progressMessage);
                },
                statusCode: {
                    201: function(data, status, req) {
                        var jobUrl = req.getResponseHeader('location');
                        var job = new Job(jobUrl);
                        job.progressID = progressID;
                        job.progressMessage = progressMessage;
                        job.progressSuccessMessage = progressSuccessMessage;
                        job.progressErrorMessage = progressErrorMessage;
                        job.successCallback = success || jQuery.noop;
                        job.errorCallback = error || jQuery.noop;

                        job.start();
                    }
                },

                error: function(jqXHR, errorStatus, errorThrown) {
                    Progress.flashErrorMessage(progressErrorMessage);

                    var message = jqXHR.responseText || errorThrown || 'Sorry, export failed, could not connect to backend.';
                    Alerts.showErrorAlert('Error:\n', message, Config.Alerts.TIMEOUT);

                    (error || jQuery.noop).apply(arguments);
                }
            });
        },

        /**
         * Section: URL Helper
         */

        /**
         * Method: _fullUrlForAnalysis
         *   Calculates the AJAX backend URL for this analysis resources for this graph (see: <Backend::_graphId>).
         *
         * Returns:
         *   The analysis URL as {String}.
         */
        _fullUrlForAnalysis: function() {
            return this._fullUrlForGraph() + Config.Backend.ANALYSIS_URL;
        },

        /**
         * Method: _fullUrlForGraph
         *   Calculates the AJAX backend URL for this graph (see: <Backend::_graphId>).
         *
         * Returns:
         *   The graph URL as {String}.
         */
        _fullUrlForGraph: function() {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/' + this._graphId;
        },

        /**
         * Method: _fullUrlForNodes
         *   Calculates the AJAX backend URL for the graph's nodes. Allows to fetch all of them or to create a new one.
         *
         * Returns:
         *   The graph's nodes URL as {String}.
         */
        _fullUrlForNodes: function() {
            return this._fullUrlForGraph() + Config.Backend.NODES_URL;
        },

        /**
         * Method: _fullUrlForNode
         *   Calculates the AJAX backend URL for on particular node of the graph. Allows to fetch, modify or delete it.
         *
         * Parameters:
         *   {Number} nodeId - The id of the node.
         *
         * Returns:
         *   The node's URL as {String}.
         */
        _fullUrlForNode: function(nodeId) {
            return this._fullUrlForNodes() + '/' + nodeId;
        },

        /**
         * Method: _fullUrlForEdges
         *   Calculates the AJAX backend URL for the graph's edges. Allows to fetch all of them or to create a new one.
         *
         * Returns:
         *   The graph's edges URL as {String}.
         */
        _fullUrlForEdges: function() {
            return this._fullUrlForGraph() + Config.Backend.EDGES_URL;
        },

        /**
         * Method: _fullUrlForEdge
         *   Calculates the AJAX backend URL for a particular edge of the graph. Allows to fetch, modify or delete it.
         *
         * Parameters:
         *   {Number} edgeId - The id of the edge.
         *
         * Returns:
         *   The edge's URL as {String}.
         */
        _fullUrlForEdge: function(edgeId) {
            return this._fullUrlForEdges() + '/' + edgeId;
        },

        /**
         * Method: _fullUrlForCutsets
         *   Calculates the AJAX backend URL calculating the cutsets of a graph. Cutsets are only available in Fault- and
         * Fuzztrees.
         *
         * Returns:
         *   The cutset URL as {String}.
         */
        _fullUrlForCutsets: function() {
            return this._fullUrlForAnalysis() + Config.Backend.CUTSETS_URL;
        },

        _fullUrlForTopEventProbability: function() {
            return this._fullUrlForAnalysis() + Config.Backend.TOP_EVENT_PROBABILITY_URL;
        },

        /**
         * Method: _fullUrlForExport
         *   Calculates the AJAX backend URL for graph export.
         *
         * Returns:
         *   The export URL as {String}.
         */
        _fullUrlForExport: function(event) {
            if (event.type == Config.Events.EDITOR_GRAPH_EXPORT_PDF) {
                exportType = 'pdf';
            }
            else if (event.type == Config.Events.EDITOR_GRAPH_EXPORT_EPS) {
                exportType = 'eps';
            }
            else {
                //TODO: Raise a meaningful exception here
                exportType = 'invalid';
            }
            return this._fullUrlForGraph() + Config.Backend.GRAPH_EXPORT_URL + '/'+exportType;
        }
    });
});
