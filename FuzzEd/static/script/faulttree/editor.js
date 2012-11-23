define(['editor', 'faulttree/graph', 'menus', 'faulttree/config'],
function(Editor, FaulttreeGraph, Menus, Config) {
    /**
     * Class: CutsetsMenu
     */
    var CutsetsMenu = Menus.Menu.extend({
        _graph: undefined,

        init: function(graph) {
            this._super();
            this._graph = graph;
        },

        show: function(cutsets) {
            if (typeof cutsets === 'undefined') {
                this.container.show();
                return this;
            }

            var listElement = this.container.find('ul').empty();

            _.each(cutsets, function(cutset) {
                var nodeIDs = cutset['nodes'];
                var nodes = _.map(nodeIDs, function(id) {
                    return this._graph.getNodeById(id);
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
                        var allNodes = this._graph.getNodes();
                        _.invoke(allNodes, 'disable');
                        _.invoke(nodes, 'highlight');
                    }.bind(this),

                    // out
                    function() {
                        var allNodes = this._graph.getNodes();
                        _.invoke(allNodes, 'enable');
                        _.invoke(nodes, 'unhighlight');
                    }.bind(this)
                );

                listElement.append(entry);
            }.bind(this));

            this._super();
        },

        _setupContainer: function() {
            return jQuery(
                '<div id="' + Config.IDs.CUTSETS_MENU + '" class="menu" header="Cutsets">\
                    <div class="menu-controls">\
                        <span class="menu-minimize"></span>\
                        <span class="menu-close"></span>\
                    </div>\
                    <ul class="nav-list unstyled"></ul>\
                </div>'
            ).appendTo(jQuery('#' + Config.IDs.CONTENT));
        }
    });

    /**
     * Class: FaultTreeEditor
     */
    return Editor.extend({
        cutsets: undefined,

        init: function(graphId) {
            this._super(graphId);

            this.cutsets = new CutsetsMenu();
            this._setupCutsetsActionEntry();
        },

        _graphClass: function() {
            return FaulttreeGraph;
        },

        _setupCutsetsActionEntry: function() {
            var navbarActionsEntry = jQuery(
                '<li>' +
                    '<a id="' + Config.IDs.NAVBAR_ACTION_CUTSETS + '" href="#">Calculate cutsets</a>' +
                '</li>');
            this._navbarActionsGroup.append(navbarActionsEntry);

            // register for clicks on the corresponding nav action
            navbarActionsEntry.click(function() {
                jQuery(document).trigger(Config.Events.EDITOR_CALCULATE_CUTSETS, this.cutsets.show.bind(this.cutsets));
            }.bind(this));

            return this;
        }
    });
});
