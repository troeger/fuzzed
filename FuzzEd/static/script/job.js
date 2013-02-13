define(["class"], function(Class) {

    /**
     *  Class: Job
     *    Wrapper that simplifies continuous querying of a backend job.
     */
    return Class.extend({

        /**
         *  Group: Members
         *
         *  Properties:
         *    {String}      _url                - The query URL of this job.
         *    {Function}    _successCallback    - Function that is called as soon as the job is finished.
         *    {Function}    _updateCallback     - Function that is called each time the job progress is queried and
         *                                        the job progress is reported back as 'not finished'.
         *    {Function}    _errorCallback      - Function that is called if the job results in an error.
         *    {int}         _queryInterval      - The interval (in ms) between job queries.
         *    {Timeout)     _timeout            - A reference to the current job query timeout.
         */
        _url:             undefined,
        _successCallback: jQuery.noop(),
        _updateCallback:  jQuery.noop(),
        _errorCallback:   jQuery.noop(),
        _queryInterval:   0,
        _timeout:         undefined,

        /**
         *  Constructor: init
         *    Constructor for this Job instance.
         *
         *  Parameters:
         *    {String}      url                - The query URL of this job.
         *    {int}         queryInterval      - The interval (in ms) between job queries.
         *    {Function}    successCallback    - [optional] Function that is called as soon as the job is finished.
         *    {Function}    updateCallback     - [optional] Function that is called each time the job progress is
         *                                       queried and the job progress is reported back as 'not finished'.
         *    {Function}    errorCallback      - [optional] Function that is called if the job results in an error.
         *    {boolean}     startImmediately   - [optional] Start querying this Job after init. Default is 'true'.
         *
         */
        init: function(url, queryInterval, successCallback, updateCallback, errorCallback, startImmediately) {
            if (typeof startImmediately === 'undefined') startImmediately = true;

            this._url             = url;
            this._successCallback = successCallback || jQuery.noop();
            this._updateCallback  = updateCallback  || jQuery.noop();
            this._errorCallback   = errorCallback   || jQuery.noop();
            this._queryInterval   = queryInterval;

            if (startImmediately) this.start();
        },

        /**
         *  Method: start
         *    Start querying this Job.
         */
        start: function() {
            this._query();
        },

        /**
         *  Method: cancel
         *    Tell the backend to cancel this job. This will result in the error callback getting called the next
         *    time this Job is queried.
         */
        cancel: function() {
            //TODO: call backend as soon as the call is available
        },

        /**
         *  Method: _query
         *    Fetch the Job's status from the backend using AJAX and call the callback corresponding to the result.
         *    In case the Job is not finished, set a timeout for the next query.
         */
        _query: function() {
            jQuery.ajax({
                url: this._url,
                statusCode: {
                    200: function(data) { // success
                        this._successCallback(data);
                    }.bind(this),

                    202: function(data) { // not finished
                        this._updateCallback(data);
                        // query again later
                        this._timeout = setTimeout(this._query, this._queryInterval);
                    }.bind(this),

                    404: function() { // not found / canceled
                        this._errorCallback();
                    }.bind(this)
                }
            });
        }

    });
});
