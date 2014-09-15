define(['class'],
function(Class) {
    /**
     *  Package: Base
     */

    /**
     *  Class: Factory
     *
     *  TODO: documentation
     */
    var Factory = Class.extend({
        kind: undefined,

        // create's first argument is the name of the base class, we want to create an instance of
        //  all other arguments are passed directly into the class constructor
        create: function(baseCls) {
            // arguments is just an "array-like" object, not an actual array, so we have to convert it into an actual array
            var args = Array.prototype.slice.call(arguments);

            // if baseCls already is a constructor and not a string describing the desired class
            if (typeof baseCls === 'function') {
                //console.log('[-] Creating a ' + baseCls + ' directly from given constructor.')
                creation = this._construct(baseCls, args.slice(1));
            } else {
            // if baseCls is a string describing the desired class (most common case)
                var resolveObj = this._resolveClassName(baseCls);
                var path = resolveObj.path;
                var clsModule = require(path);

                var creation = undefined;

                // our first try is based on the assumption, that the class module only returns the class constructor
                if (typeof clsModule           !== 'undefined'
                 && typeof clsModule.prototype !== 'undefined') {
                    creation = this._construct(clsModule, args.slice(1));

                // our second try supposes that the constructor is a member of the return object and is called the same
                //  as the concrete class we are looking for (e.g. FaulttreeNodeGroup)
                } else if (typeof clsModule[resolveObj.fullClassName]           !== 'undefined'
                        && typeof clsModule[resolveObj.fullClassName].prototype !== 'undefined') {
                    creation = this._construct(clsModule[resolveObj.fullClassName], args.slice(1));

                // our third try is to find the wanted class inside the found package, but this time named as the
                //  baseCls (e.g. NodeGroup)
                } else if (typeof clsModule[resolveObj.cls]           !== 'undefined'
                        && typeof clsModule[resolveObj.cls].prototype !== 'undefined') {
                    creation = this._construct(clsModule[resolveObj.cls], args.slice(1));
                }
            }

            if (typeof creation !== 'undefined') {
                //console.log('Sucessfully created a ' + baseCls);
                return creation;
            } else {
                throw new ClassResolveError("Could not resolve class '" + baseCls + "' for kind '" + this.kind + "'");
            }
        },

        getModule: function(baseCls) {
            var resolveObj = this._resolveClassName(baseCls);
            //console.log('Successfully resolved class module for ' + baseCls + ' from ' + resolveObj.path);
            return require(resolveObj.path);
        },

        _construct: function(constructor, args) {
            function Creation() {
                return constructor.apply(this, args);
            }
            Creation.prototype = constructor.prototype;
            return new Creation();
        },

        _resolveClassName: function(cls, kind) {
            kind = kind || this.kind;

            // e.g. (NodeGroup, faulttree) becomes FaulttreeNodeGroup
            var fullClassName = kind[0].toUpperCase() + kind.slice(1) + cls[0].toUpperCase() + cls.slice(1);
            // e.g. (NodeGroup, faulttree) becomes faulttree/node
            var path = kind + '/' + this._fromClassToPath(cls);

            retObj = {
                cls: cls,
                kind: kind,
                path: path,
                fullClassName: fullClassName
            };

            // precondition: to subclass any class, one has to subclass an Editor (directly or indirectly) and require
            //  all classes in the XYEditor's module, that shall replace base classes in general.
            //  e.g. if I want to have an Editor Foo that only differs from Faulttrees in its Nodes, I have to subclass
            //  a FaulttreeEditor in 'foo/editor.js', beginning with
            //      define(['class'], ['editor'], ['foo/node'], function(Class, Editor, FooNode) { ...
            //  and off course I also have to implement
            //      getFactory: function() {
            //          return new Factory('foo');
            //      },

            if (require.defined(path)) {                                  // if a kind-specific class exists and is an
                return retObj;                                            // already loaded require-module, return its path
            } else if (this._baseKind(kind)) {                            // else if our kind inherits from a base kind
                return this._resolveClassName(cls, this._baseKind(kind)); // resolve the class name from that base
            } else {
                retObj.path = this._fromClassToPath(cls);                 // else use the default class, e.g. Node
                return retObj;
            }
        },

        _fromClassToPath: function(cls) {
            // convert every upper case letter into a '_' and a lowercase letter, so that NodeGroup becomes node_group
            var path = cls.replace(/[A-Z]/g, function(t){
                return t.slice(0, -1) + '_' + t.slice(-1).toLowerCase();
            }).slice(1);
            return path;
        },

        _baseKind: function(kind) {
            // this is the part where we hardcode any inheritances _not_ from the abstract editor.
            // we assume, that in most of the cases editors inherit directly from the abstract editor, so any other
            //  case has to be described here.

            if (kind === 'fuzztree') { // Fuzztrees inherit form Faulttrees
                return 'faulttree';
            } else {
                return false;
            }
        }
    });

    return new Factory();
});