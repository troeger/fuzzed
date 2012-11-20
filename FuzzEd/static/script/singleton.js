define(['class'], function(Class) {
    var Singleton = function(){};

    Singleton.extend = function(prop) {
        var instance = new Class.extend(prop);

        function Singleton() {
            return instance;
        }

        // Populate our constructed prototype object
        Singleton.prototype = prototype;

        // Enforce the constructor to be what we expect
        Singleton.prototype.constructor = Singleton;

        // And make this class extendable
        Singleton.extend = arguments.callee;

        return Singleton;
    };

    return Singleton;
});
