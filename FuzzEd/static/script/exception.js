/**
 * Package: Base
 */

/**
 * Section: Errors
 *      Exception type hierarchy for general purpose use - all error prototypes are exported on editor startup into the
 *      global namespace(!) and can be accessed from there. The exceptions are typed sub-prototypes of ECMAs builtin
 *      Error.
 *
 *      If you want to introduce another exception, follow the here laid out pattern. Create a new Error object in the
 *      constructor of the sub-prototype, set its message and stack value to your own object in order to get a
 *      meaningful stacktrace and overwrite the error name. It is NOT(!) possible to pass the name directly to the Error
 *      object's arguments since they are discarded for whatever reason.
 */


/**
 * Class: NetworkError
 *      Indicates a error in the network communication such as e.g. AJAX.
 */
function NetworkError(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'NetworkError';
    this.message = message || '';
    this.stack   = error.stack;
}
NetworkError.prototype = new Error();
NetworkError.prototype.constructor = NetworkError;

/**
 * Class: SubclassResponsibility
 *      Inspired by Smalltalk and Python's way of declaring sort of abstract classes. Throw a SubclassResponsibility
 *      error in methods that you want to be abstract respectively force to be overwritten.
 */
function SubclassResponsibility(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'SubclassResponsibility';
    this.message = message || '';
    this.stack   = error.stack;
}
SubclassResponsibility.prototype = new Error();
SubclassResponsibility.prototype.constructor = SubclassResponsibility;

/**
 * Class: TypeError
 *      Shadows the Builtin TypeError of ECMA script, though is fully compatible. Is used to indicate that value is not
 *      given or of wrong type.
 */
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

/**
 * Class: ValueError
 *      Indicated that the value if of proper type but not within other certain constraints such as e.g. array bounds,
 *      range, amount of values and so on.
 */
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

/**
 * Class: Warning
 *      JavaScript does not support any kind of warning mechanism. Therefore, we facilitate exceptions instead. This
 *      Warning sub-prototype can be extended at will and warning can be caught type safe.
 */
function Warning(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'Warning';
    this.message = message || '';
    this.stack   = error.stack;
}
Warning.prototype = new Error();
Warning.prototype.constructor = Warning;

function ClassResolveError(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'ClassResolveError';
    this.message = message || '';
    this.stack   = error.stack;
}
ClassResolveError.prototype = new Error();
ClassResolveError.prototype.constructor = ClassResolveError;

function ClassNotFound(message) {
    var error = Error.apply(this, arguments);

    this.name    = 'ClassNotFound';
    this.message = message || '';
    this.stack   = error.stack;
}
ClassNotFound.prototype = new Error();
ClassNotFound.prototype.constructor = ClassNotFound;