define(['class', 'config', 'job', 'alerts', 'progress_indicator', 'jquery', 'jquery-ajaxq', 'jquery-cookie'],
function (Class, Config, Job, Alerts, Progress) {
    /**
     * Package: Base
     */

    /**
     * Class: Backend
     *      This small helper class is responsible for handling the communication with the Backend and so synchronize
     *      changes in the graph. The implementation is event driven. This means this helper will listen on custom
     *      events triggered by other entities and make according AJAX requests. Direct invocation of synchronization
     *      calls is highly discouraged in all cases. There should be always only Backend instance at the same time in
     *      existence to avoid data duplication in the backend.
     */
    var Backend = Class.extend({
        /**
         * Group: Members
         *
         * Properties:
         *      {Number} _graphId - The ID of the graph the Backend will synchronize changes for.
         */
        _graphId: undefined,

        /**
         * Constructor: init
         *      Creates a new Backend instance and will capture the passed graphId.
         *
         * Parameters:
         *      {Number} graphId - The ID of the graph the Backend will synchronize changes for.
         */
        init: function(graphId) {
            this._graphId = graphId;
        },

        /**
         * Section: State
         */

        /**
         * Method: activate
         *      Tells a <Backend> instance to start synchronizing changes. There MUST be one invocation off this method
         *      as data synchronization is turned off by default. Registers AJAX synchronization calls for all custom
         *      events listed below.
         *
         * On:
         *      <Config::Events::NODE_PROPERTY_CHANGED>
         *      <Config::Events::NODE_ADDED>
         *      <Config::Events::NODE_DELETED>
         *      <Config::Events::EDGE_ADDED>
         *      <Config::Events::EDGE_DELETED>
         *      <Config::Events::EDITOR_GRAPH_EXPORT_PDF>
         *      <Config::Events::EDITOR_GRAPH_EXPORT_EPS>
         *      <Config::Events::EDITOR_CALCULATE_CUTSETS>
         *      <Config::Events::EDITOR_CALCULATE_ANALYTICAL_PROBABILITY>
         *      <Config::Events::EDITOR_CALCULATE_SIMULATED_PROBABILITY>
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        activate: function() {
            jQuery(document)
                .on(Config.Events.NODE_PROPERTY_CHANGED,                   this.nodePropertyChanged.bind(this))
                .on(Config.Events.EDGE_PROPERTY_CHANGED,                   this.edgePropertyChanged.bind(this))
                .on(Config.Events.NODEGROUP_PROPERTY_CHANGED,              this.nodeGroupPropertyChanged.bind(this))
                .on(Config.Events.NODE_ADDED,                              this.nodeAdded.bind(this))
                .on(Config.Events.NODE_DELETED,                            this.nodeDeleted.bind(this))
                .on(Config.Events.EDGE_ADDED,                              this.edgeAdded.bind(this))
                .on(Config.Events.EDGE_DELETED,                            this.edgeDeleted.bind(this))
                .on(Config.Events.NODEGROUP_ADDED,                         this.nodeGroupAdded.bind(this))
                .on(Config.Events.NODEGROUP_DELETED,                       this.nodeGroupDeleted.bind(this))
                .on(Config.Events.EDITOR_GRAPH_EXPORT_PDF,                 this.graphExport.bind(this))
                .on(Config.Events.EDITOR_GRAPH_EXPORT_EPS,                 this.graphExport.bind(this))
                .on(Config.Events.EDITOR_CALCULATE_CUTSETS,                this.calculateCutsets.bind(this))
                .on(Config.Events.EDITOR_CALCULATE_ANALYTICAL_PROBABILITY, this.calculateAnalyticalProbability.bind(this))
                .on(Config.Events.EDITOR_CALCULATE_SIMULATED_PROBABILITY,  this.calculateSimulatedProbability.bind(this));
            return this;
        },

        /**
         * Method: deactivate
         *      An invocation of this method will turn off all data synchronization with the Backend. Therefore
         *      deregisters all handlers for custom synchronization events.
         *
         * Off:
         *      <Config::Events::NODE_PROPERTY_CHANGED>
         *      <Config::Events::NODE_ADDED>
         *      <Config::Events::NODE_DELETED>
         *      <Config::Events::EDGE_ADDED>
         *      <Config::Events::EDGE_DELETED>
         *      <Config::Events::EDITOR_GRAPH_EXPORT_PDF>
         *      <Config::Events::EDITOR_GRAPH_EXPORT_EPS>
         *      <Config::Events::EDITOR_CALCULATE_CUTSETS>
         *      <Config::Events::EDITOR_CALCULATE_ANALYTICAL_PROBABILITY>
         *      <Config::Events::EDITOR_CALCULATE_SIMULATED_PROBABILITY>
         *
         * Returns:
         *      This {<Backend>} instance for chaining.
         */
        deactivate: function() {
            jQuery(document)
                .off(Config.Events.NODE_PROPERTY_CHANGED)
                .off(Config.Events.NODE_ADDED)
                .off(Config.Events.NODE_DELETED)
                .off(Config.Events.EDGE_ADDED)
                .off(Config.Events.EDGE_DELETED)
                .off(Config.Events.EDITOR_GRAPH_EXPORT_PDF)   
                .off(Config.Events.EDITOR_GRAPH_EXPORT_EPS)                
                .off(Config.Events.EDITOR_CALCULATE_CUTSETS)
                .off(Config.Events.EDITOR_CALCULATE_ANALYTICAL_PROBABILITY)
                .off(Config.Events.EDITOR_CALCULATE_SIMULATED_PROBABILITY);
            return this;
        },

        /**
         * Section: Handlers
         */

        /**
         * Method: showProgress
         *      Default function for indicating progress on standard backend communication methods. Should be passed to
         *      the 'beforeSend' argument of an ajaxq request. This method will also set the CSRF token
         *
         * Parameters:
         *      {XMLHTTPRequest} xhr - standard browser XHR object.
         */
        showProgress: function(xhr) {
            // set messages for progress indicator
            xhr.progressMessage        = 'Saving…';
            xhr.progressSuccessMessage = 'Saved';
            xhr.progressErrorMessage   = 'Not saved!';
            // set CSRF cookie
            xhr.setRequestHeader('X-CSRFToken', jQuery.cookie('csrftoken'));
        },

        /**
         * Method: errorCallback
         *      Creates a standard error callback
         *
         * Parameters:
         *      {String}   alert - The message to be displayed on error.
         *      {Function} error - [optional] an optional user passed error callback.
         *
         * Returns:
         *      The error callback {Function}.
         */
        errorCallback: function(alert, error) {
            return function(jqXHR, errorStatus, errorThrown) {
                var message = errorThrown || 'Could not connect to backend.';
                Alerts.showErrorAlert(alert, message, Config.Alerts.TIMEOUT);
                (error || jQuery.noop).apply(arguments);
            }
        },

        /**
         * Method: edgeAdded
         *      Adds a new edge from a given source node to a given target node.
         *
         * Parameters:
         *      {Event}    event        - jQuery event object of the custom trigger.
         *      {Number}   edgeId       - ID of the edge.
         *      {Number}   sourceNodeId - Source node of the new edge.
         *      {Number}   targetNodeId - Target node of the new edge.
         *      {Object}   properties   - The new edges properties
         *      {Function} success      - [optional] Will be called when the request was successful. Provides e.g. the
         *                                ID of the new edge.
         *      {Function} error        - [optional] Callback that gets called in case of an ajax-error.
         *      {Function} complete     - [optional] Callback that is invoked in both cases - a successful or an
         *                                erroneous AJAX request.
         */
        edgeAdded: function(event, edgeId, sourceNodeId, targetNodeId, properties, success, error, complete) {
            var data = {
                client_id:  edgeId,
                source:     sourceNodeId,
                target:     targetNodeId,
                properties: properties
            };

            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForEdges(),
                type:        'POST',
                contentType: 'application/json; charset=utf-8',
                data:        JSON.stringify(data),

                beforeSend:  this.showProgress,
                success:     success  || jQuery.noop,
                complete:    complete || jQuery.noop,
                error:       this.errorCallback('Edge could not be saved:', error)
            });

            return this;
        },

        /**
         * Method: nodeAdded
         *      Adds a new node to the backend of this graph.
         *
         * Parameters:
         *      {Event}    event      - jQuery event object of the custom trigger.
         *      {Number}   nodeId     - The node ID.
         *      {String}   kind       - The node kind.
         *      {Number}   x          - The grid x coordinate where the node was added.
         *      {Number}   y          - The grid y coordinate where the node was added.
         *      {Object}   properties - The new node's properties
         *      {Function} success    - [optional] Will be called on successful node creation transmission to server.
         *      {Function} error      - [optional] Callback that gets called in case of an ajax-error.
         *      {Function} complete   - [optional] Callback that is invoked when the ajax request completes successful
         *                              or erroneous.
         */
        nodeAdded: function(event, nodeId, kind, x, y, properties, success, error, complete) {
            var data = {
                client_id:  nodeId,
                kind:       kind,
                x:          x,
                y:          y,
                properties: properties
            };

            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForNodes(),
                type:        'POST',
                contentType: 'application/json; charset=utf-8',
                data:        JSON.stringify(data),

                beforeSend:  this.showProgress,
                success:     success  || jQuery.noop,
                complete:    complete || jQuery.noop,
                error:       this.errorCallback('Node could not be created:', error)
            });

            return this;
        },

        /**
         * Method: nodeGroupAdded
         *      Adds a new node group to the backend of this graph.
         *
         * Parameters:
         *      {Event}    event       - jQuery event object of the custom trigger.
         *      {Number}   nodeGroupId - The nodeGroup ID.
         *      {String}   nodeIds     - The member nodes' ids.
         *      {Object}   properties  - The new nodeGroup's properties
         *      {Function} success     - [optional] Will be called on successful node creation transmission to server.
         *      {Function} error       - [optional] Callback that gets called in case of an ajax-error.
         *      {Function} complete    - [optional] Callback that is invoked when the ajax request completes successful
         *                               or erroneous.
         */
        nodeGroupAdded: function(event, nodeGroupId, nodeIds, properties, success, error, complete) {
            var data = {
                client_id:  nodeGroupId,
                nodeIds:    nodeIds,
                properties: properties
            };

            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForNodeGroups(),
                type:        'POST',
                contentType: 'application/json; charset=utf-8',
                data:        JSON.stringify(data),

                beforeSend:  this.showProgress,
                success:     success  || jQuery.noop,
                complete:    complete || jQuery.noop,
                error:       this.errorCallback('Node group could not be created:', error)
            });

            return this;
        },

        /**
         * Method: edgeDeleted
         *      Deletes a given edge in the backend.
         *
         * Parameters:
         *      {Event}    event    - jQuery event object of the custom trigger.
         *      {Number}   edgeId   - The ID of the edge that should be deleted.
         *      {Function} success  - [optional] Function that is invoked when the AJAX request was successful.
         *      {Function} error    - [optional] Callback that gets called in case of an AJAX error.
         *      {Function} complete - [optional] Callback that gets invoked in both cases - a successful and an
         *                            erroneous AJAX call.
         */
        edgeDeleted: function(event, edgeId, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:        this._fullUrlForEdge(edgeId),
                type:       'DELETE',

                beforeSend: this.showProgress,
                success:    success  || jQuery.noop,
                complete:   complete || jQuery.noop,
                error:      this.errorCallback('Edge could not be deleted:', error)
            });

            return this;
        },

        /**
         * Method: nodeDeleted
         *      Deletes a given node in the backend.
         *
         * Parameters:
         *      {Event}    event    - jQuery event object of the custom trigger.
         *      {Number}   nodeId   - The ID of the node that should be deleted.
         *      {Function} success  - [optional] Callback that is being called on successful deletion on backend.
         *      {Function} error    - [optional] Callback that gets called in case of an ajax-error.
         *      {Function} complete - [optional] Callback that is invoked for successful and erroneous AJAX requests.
         */
        nodeDeleted: function(event, nodeId, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:        this._fullUrlForNode(nodeId),
                type:       'DELETE',

                beforeSend: this.showProgress,
                success:    success  || jQuery.noop,
                complete:   complete || jQuery.noop,
                error:      this.errorCallback('Node could not be deleted:', error)
            });

            return this;
        },

        /**
         * Method: nodeGroupDeleted
         *      Deletes a given node group in the backend.
         *
         * Parameters:
         *      {Event}    event         - jQuery event object of the custom trigger.
         *      {Number}   nodeGroupId   - The ID of the node that should be deleted.
         *      {Function} success       - [optional] Callback that is being called on successful deletion on backend.
         *      {Function} error         - [optional] Callback that gets called in case of an ajax-error.
         *      {Function} complete      - [optional] Callback that is invoked for successful and erroneous requests.
         */
        nodeGroupDeleted: function(event, nodeGroupId, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:        this._fullUrlForNodeGroup(nodeGroupId),
                type:       'DELETE',

                beforeSend: this.showProgress,
                success:    success  || jQuery.noop,
                complete:   complete || jQuery.noop,
                error:      this.errorCallback('Node could not be deleted:', error)
            });

            return this;
        },

        /**
         * Method: nodePropertyChanged
         *      Changes the properties of a given node.
         *
         * Parameters:
         *      {Event}    event      - jQuery event object of the custom trigger.
         *      {Number}   nodeId     - The node that shall be moved.
         *      {Object}   properties - The node's properties that should be changed. Keys stand for property names and
         *                              their assigned values is the new state.
         *      {Function} success    - [optional] Callback that is called when the move was successfully saved.
         *      {Function} error      - [optional] Callback that gets called in case of an AJAX error.
         *      {Function} complete   - [optional] Callback that is always invoked no matter if AJAX request was
         *                              successful or erroneous.
         */
        nodePropertyChanged: function(event, nodeId, properties, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForNode(nodeId),
                type:        'PATCH',
                contentType: 'application/json; charset=utf-8',
                data:        JSON.stringify({'properties': properties}),

                beforeSend:  this.showProgress,
                success:     success  || jQuery.noop,
                complete:    complete || jQuery.noop,
                error:       this.errorCallback('Node property could not be changed:', error)
            });

            return this;
        },

        /**
         * Method: edgePropertyChanged
         *      Changes the properties of a given edge.
         *
         * Parameters:
         *      {Event}    event      - jQuery event object of the custom trigger.
         *      {Number}   edgeId     - The edge that shall be moved.
         *      {Object}   properties - The edge's properties that should be changed. Keys stand for property names and
         *                              their assigned values is the new state.
         *      {Function} success    - [optional] Callback that is called when the move was successfully saved.
         *      {Function} error      - [optional] Callback that gets called in case of an AJAX error.
         *      {Function} complete   - [optional] Callback that is always invoked no matter if AJAX request was
         *                              successful or erroneous.
         */
        edgePropertyChanged: function(event, edgeId, properties, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForEdge(edgeId),
                type:        'PATCH',
                contentType: 'application/json; charset=utf-8',
                data:        JSON.stringify({properties: properties}),

                beforeSend:  this.showProgress,
                success:     success  || jQuery.noop,
                complete:    complete || jQuery.noop,
                error:       this.errorCallback('Edge property could not be changed:', error)
            });

            return this;
        },

        /**
         * Method: nodeGroupPropertyChanged
         *      Changes the properties of a given node group.
         *
         * Parameters:
         *      {Event}    event       - jQuery event object of the custom trigger.
         *      {Number}   nodeGroupId - The edge that shall be moved.
         *      {Object}   properties  - The node group's properties that should be changed. Keys stand for property
         *                               names and their assigned values is the new state.
         *      {Function} success     - [optional] Callback that is called when the move was successfully saved.
         *      {Function} error       - [optional] Callback that gets called in case of an AJAX error.
         *      {Function} complete    - [optional] Callback that is always invoked no matter if AJAX request was
         *                               successful or erroneous.
         */
        nodeGroupPropertyChanged: function(event, nodeGroupId, properties, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForNodeGroup(nodeGroupId),
                type:        'PATCH',
                contentType: 'application/json; charset=utf-8',
                data:        JSON.stringify({properties: properties}),

                beforeSend:  this.showProgress,
                success:     success  || jQuery.noop,
                complete:    complete || jQuery.noop,
                error:       this.errorCallback('Node group property could not be changed:', error)
            });

            return this;
        },

        /**
         * Method: getGraph
         *      Fetch a graph JSON object from the backend.
         *
         * Parameters:
         *      {Function} success  - [optional] Callback function for a successful asynchronous request for JSON
         *                            representing a graph with given id.
         *      {Function} error    - [optional] Callback that gets called in case of an unsuccessful retrieval of the
         *                            graph from the database. Will create a new graph in the backend anyway.
         *      {Function} complete - [optional] Callback that gets invoked in either a successful or erroneous request.
         */
        getGraph: function(success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:      this._fullUrlForGraph(),
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /**
         * Method: calculateCutsets
         *      Asks the backend to calculate the minimal cutsets for the given graph.
         *
         * Parameters:
         *      {Event}    event    - jQuery event object of the custom trigger.
         *      {Function} success  - [optional] Callback that is called when the calculation was successful.
         *      {Function} error    - [optional] Callback that gets called in case of an AJAX error.
         *      {Function} complete - [optional] Callback that gets invoked in both; successful or erroneous request.
         */
        calculateCutsets: function(event, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:      this._fullUrlForCutsets(),
                dataType: 'json',

                success:  success  || jQuery.noop,
                complete: complete || jQuery.noop,
                error:    this.errorCallback('Failed to calculate cutsets:', error)
            });

            return this;
        },

        /**
         * Method: calculateAnalyticalProbability
         *      Tell the backend to calculate the analytical probability of the top event. This is an asynchronous
         *      request, i.e. the success callback will get a <Job> object it can use to receive the final result.
         *
         * Parameters:
         *      {Function} success  - [optional] Callback function that will receive the <Job> object if the job
         *                            submission was successful.
         *      {Function} error    - [optional] Callback that gets called in case of an error.
         *      {Function} complete - [optional] Callback that gets invoked in either a successful or erroneous request.
         */
        calculateAnalyticalProbability: function(event, success, error, complete) {
            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForJobTasks(),
                type:        'POST',
                contentType: 'application/json',
                data:        JSON.stringify({kind : Config.Backend.ANALYSIS_JOB}),

                beforeSend:  function(xhr) { xhr.setRequestHeader('X-CSRFToken', jQuery.cookie('csrftoken')); },
                statusCode:  {
                    201: function(data, status, req) {
                        success ? success(req.getResponseHeader('location')) : jQuery.noop();
                    }
                },
                complete: complete || jQuery.noop,
                error:    this.errorCallback('Could not analyze probability:', error)
            });
        },

        /**
         * Method: calculateSimulatedProbability
         *      Tell the backend to calculate the simulated probability of the top event. This is an asynchronous
         *      request, i.e. the success callback will get a <Job> object it can use to receive the final result.
         *
         * Parameters:
         *      {Function} success  - [optional] Callback function that will receive the <Job> object if the job
         *                            submission was successful.
         *      {Function} error    - [optional] Callback that gets called in case of an error.
         *      {Function} complete - [optional] Callback that gets invoked in either a successful or erroneous request.
         */
        calculateSimulatedProbability: function(event, success, error, complete) {

            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForJobTasks(),
                type:        'POST',
                contentType: 'application/json',
                data:        JSON.stringify({kind : Config.Backend.SIMULATION_JOB}),

                beforeSend:  function(xhr) { xhr.setRequestHeader('X-CSRFToken', jQuery.cookie('csrftoken')); },
                statusCode:  {
                    201: function(data, status, req) {
                        success ? success(req.getResponseHeader('location')) : jQuery.noop();
                    }
                },
                complete: complete || jQuery.noop,
                error:    this.errorCallback('Could not simulate probability:', error)
            });
        },

        /**
         * Method: graphExport
         *      Starts a <Job> for exporting and eventually downloading the graph in the specified file format. The file
         *      format depends on the type of the triggering event. This method will spawn a <Job> that frequently
         *      queries the backend for the exported file and returns the URL to the file if successful. The progress
         *      indicator will reflect the file generation progress.
         *
         *  Parameters:
         *      {Function} success - Callback function that receives the URL to the generated file.
         *      {Function} error   - [optional] Callback function that gets called in case of an error (either during
         *                           job creation or an error in the job itself).
         */
        graphExport: function(event, success, error) {
            var progressID = _.uniqueId('export_');
            var kind       = undefined;

                 if (event.type === Config.Events.EDITOR_GRAPH_EXPORT_PDF) kind = Config.Backend.PDF_JOB;
            else if (event.type === Config.Events.EDITOR_GRAPH_EXPORT_EPS) kind = Config.Backend.EPS_JOB;
            else    throw new ValueError('Unknown export type ' + event.type);

            var pendingMessage = Config.ProgressIndicator.EXPORT_PROGRESS_MESSAGE + kind.toUpperCase();
            var errorMessage   = Config.ProgressIndicator.EXPORT_ERROR_MESSAGE    + kind.toUpperCase();
            var successMessage = Config.ProgressIndicator.EXPORT_SUCCESS_MESSAGE;

            jQuery.ajaxq(Config.Backend.AJAX_QUEUE, {
                url:         this._fullUrlForJobTasks(),
                type:        'POST',
                contentType: 'application/json',
                data:        JSON.stringify({kind : kind}),

                beforeSend: function(xhr) {
                    //Progress.showProgress(progressID, progressMessage);
                    xhr.setRequestHeader('X-CSRFToken', jQuery.cookie('csrftoken'));
                },
                statusCode: {
                    201: function(data, status, req) {
                        var job = new Job(req.getResponseHeader('location'));
                        job.progressID             = progressID;
                        job.progressMessage        = pendingMessage;
                        job.progressSuccessMessage = successMessage;
                        job.progressErrorMessage   = errorMessage;
                        job.successCallback        = success || jQuery.noop;
                        job.errorCallback          = error || jQuery.noop;

                        job.start();
                    }
                },
                error: function(jqXHR, errorStatus, errorThrown) {
                    var message = jqXHR.responseText || errorThrown || 'Export failed! Could not connect to backend.';

                    Progress.flashErrorMessage(errorMessage);
                    Alerts.showErrorAlert('Error:\n', message, Config.Alerts.TIMEOUT);
                    (error || jQuery.noop).apply(arguments);
                }
            });
        },

        /**
         * Section: URL Helper
         */

        /**
         * Method: _fullUrlForGraph
         *      Calculates the AJAX backend URL for this graph (see: <Backend::_graphId>).
         *
         * Returns:
         *      The graph URL as {String}.
         */
        _fullUrlForGraph: function() {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/' + this._graphId;
        },

        /**
         * Method: _fullUrlForNodes
         *      Calculates the AJAX backend URL for the graph's nodes. Allows to fetch a list of all graphs (GET) or to
         *      create a new one (POST).
         *
         * Returns:
         *      The graph's nodes URL as {String}.
         */
        _fullUrlForNodes: function() {
            return this._fullUrlForGraph() + Config.Backend.NODES_URL + '/';
        },

        /**
         * Method: _fullUrlForNode
         *      Calculates the AJAX backend URL for one particular node of the graph. Allows to fetch (GET), modify
         *      (POST) or delete (DELETE) it.
         *
         * Parameters:
         *      {Number} nodeId - The id of the node.
         *
         * Returns:
         *      The node's URL as {String}.
         */
        _fullUrlForNode: function(nodeId) {
            return this._fullUrlForNodes() + nodeId;
        },

        /**
         * Method: _fullUrlForEdges
         *      Calculates the AJAX backend URL for the graph's edges. Allows to fetch a list of all of them (GET) or to
         *      create (POST) a new one.
         *
         * Returns:
         *      The graph's edges URL as {String}.
         */
        _fullUrlForEdges: function() {
            return this._fullUrlForGraph() + Config.Backend.EDGES_URL + '/';
        },

        /**
         * Method: _fullUrlForEdge
         *      Calculates the AJAX backend URL for a particular edge of the graph. Allows to fetch (GET), modify (PUT)
         *      or delete (DELETE) it.
         *
         * Parameters:
         *      {Number} edgeId - The id of the edge.
         *
         * Returns:
         *      The edge's URL as {String}.
         */
        _fullUrlForEdge: function(edgeId) {
            return this._fullUrlForEdges() + edgeId;
        },

        /**
         * Method: _fullUrlForNodeGroups
         *      Calculates the AJAX backend URL for the graph's node groups. Allows to fetch all of them (GET) or to
         *      create a new one (POST).
         *
         * Returns:
         *      The graph's node groups URL as {String}.
         */
        _fullUrlForNodeGroups: function() {
            return this._fullUrlForGraph() + Config.Backend.NODEGROUPS_URL + '/';
        },

        /**
         * Method: _fullUrlForNodeGroup
         *      Calculates the AJAX backend URL for one particular node group of the graph. Allows to fetch (GET),
         *      modify (PUT) or delete (DELETE) it.
         *
         * Parameters:
         *      {Number} nodeGroupId - The id of the node group.
         *
         * Returns:
         *      The node group's URL as {String}.
         */
        _fullUrlForNodeGroup: function(nodeGroupId) {
            return this._fullUrlForNodeGroups() + nodeGroupId;
        },

        /**
         * Method: _fullUrlForJobTasks
         *   Calculates the AJAX backend URL used by multiple Job Tasks.
         *   Specific tasks of a Job are PDF and EPS export, as well as Topevent and Simulation analysis.
         */
        _fullUrlForJobTasks: function() {
            return this._fullUrlForGraph() + Config.Backend.JOBS_URL + '/';
        }
        
    });

    // Variable that holds the Backend singletons
    var registeredBackends = {};

    return {
        /**
         * Function: establish
         *      Get or creates a Backend singleton for the given graph id.
         *
         * Parameters:
         *      {Number} graphId - the backend's graph id
         *
         * Returns:
         *      A {Backend} singleton
         */
        establish: function(graphId) {
            if (typeof registeredBackends[graphId] === 'undefined') {
                registeredBackends[graphId] = new Backend(graphId);
            }
            return registeredBackends[graphId];
        }
    }
});
