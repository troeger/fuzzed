define(function() {
    Function.prototype.extend = function(parent) {
        if (parent.constructor != Function) {
            throw "Cannot inherit from " + parent;
        }

        this.prototype = new parent();
        this.prototype.constructor = this;
        this.prototype.parent = parent.prototype;
    } 

    return this;
});