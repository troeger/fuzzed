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
         *    {Function}    successCallback    - Function that is called as soon as the job is finished.
         *    {Function}    updateCallback     - Function that is called each time the job progress is queried and
         *                                       the job progress is reported back as 'not finished'.
         *    {Function}    errorCallback      - Function that is called if the resource was not found.
         *    {Function}    errorCallback      - Function that is called if the job results in an error.
         *    {int}         queryInterval      - The interval (in ms) between job queries.
         *    {String}      _url               - The query URL of this job.
         *    {Timeout)     _timeout           - A reference to the current job query timeout.
         */
        successCallback:  jQuery.noop(),
        updateCallback:   jQuery.noop(),
        notFoundCallback: jQuery.noop(),
        errorCallback:    jQuery.noop(),
        queryInterval:    1000,

        _url:            undefined,
        _timeout:        undefined,

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Constructor for this Job instance.
         *
         *  Parameters:
         *    {String}      url                - The query URL of this job.
         */
        init: function(url) {
            this._url             = url;
        },

        /**
         *  Group: Actions
         */

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
         *  Group: Internal
         */

        /**
         *  Method: _query
         *    Fetch the Job's status from the backend using AJAX and call the callback corresponding to the result.
         *    In case the Job is not finished, set a timeout for the next query.
         */
        _query: function() {
            jQuery.ajax({
                url: this._url,
                dataType: 'json',
                statusCode: {
                    200: function(data) { // success
                        this.successCallback(data);
                    }.bind(this),

                    202: function(data) { // not finished
                        this.updateCallback(data);
                        // query again later
                        this._timeout = setTimeout(this._query.bind(this), this.queryInterval);
                    }.bind(this),

                    404: function() { // not found / canceled
                        this.notFoundCallback();
                    }.bind(this)
                },
                error: this.errorCallback
            });
        }

    });
});
