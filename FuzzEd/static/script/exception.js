/**
 * Package: Base
 */

function NetworkError(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'NetworkError';
    this.message = message || '';
    this.stack   = error.stack;
}
NetworkError.prototype = new Error();
NetworkError.prototype.constructor = NetworkError;

function SubclassResponsibility(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'SubclassResponsibility';
    this.message = message || '';
    this.stack   = error.stack;
}
SubclassResponsibility.prototype = new Error();
SubclassResponsibility.prototype.constructor = SubclassResponsibility;

var BuiltinTypeError = TypeError;
function CustomTypeError(expectedOrMessage, got) {
    var error = BuiltinTypeError.apply(this, arguments);

    this.name = 'TypeError';
    if (typeof got !== 'undefined') {
        this.message =  'got "' + expectedOrMessage + '", expected "' + got + '"';
    } else {
        this.message = expectedOrMessage || '';
    }
    this.stack = error.stack;
}
CustomTypeError.prototype = new BuiltinTypeError();
CustomTypeError.prototype.constructor = CustomTypeError;
TypeError = CustomTypeError;

function ValueError(expectedOrMessage, got) {
    var error = Error.apply(this, arguments);

    this.name = 'ValueError';
    if (typeof got !== 'undefined')
        this.message = 'got "' + expectedOrMessage + '", expected "' + got + '"';
    else
        this.message = expectedOrMessage || message;
    this.stack = error.stack;
}
ValueError.prototype = new Error();
ValueError.prototype.constructor = ValueError;

function Warning(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'Warning';
    this.message = message || '';
    this.stack   = error.stack;
}
Warning.prototype = new Error();
Warning.prototype.constructor = Warning;
