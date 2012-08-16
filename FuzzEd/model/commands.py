from django.db import models

from edge import Edge
from graph import Graph
from node import Node
from properties import Property

class Command(models.Model)
    """
    [ABSTRACT] Command class

    Abstract base class for any command in the system. Required for type correctness
    and contains meta data needed in every subtype.

    Attributes:
    undoable    -- flag indicating whether this command can be undone (boolean, required, default: False)
    insert_date -- timestamp of the moment the command was issued (datetime, constant, default: now)
    """
    class Meta:
        app_label = 'FuzzEd'
        abstract  = True

    undoable    = models.BooleanField(default=False)
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)

    def do(self):
        """
        [ABSTRACT] Method stub for application behaviour of commands.
        Needs to be overwritten in subtypes.

        Returns:
        None
        """
        raise NotImplementedError('[Abstract Method] Implement do in subclass')

    def undo(self):
        """
        [ABSTRACT] Method stub for revert behaviour of commands.
        Needs to be overwritten in subtypes.

        Returns:
        None
        """
        raise NotImplementedError('[Abstract Method] Implement undo in subclass')

class AddEdge(Command):
    """
    AddEdge class

    Models the command of adding an edge.

    Attributes:
    edge - the edge that was added (Edge, required)
    """
    edge = models.ForeignKey(Edge, related_name='+')

    @staticmethod
    def create_of(graph_id, from_node_id, to_node_id, client_id):
        """
        Convience method for issueing an add edge command. Note: the edge required 
        for this command is CREATED AND SAVED when invoking this method.

        Arguments:
        graph_id     -- the graph that will contain this edge (string/integer, required)
        from_node_id -- the id of the starting node of the edge (string/integer, required)
        to_node_id   -- the id of the endpoint node of the edge (string/integer, required)
        client_id    -- this is the id of the edge as assigned by the user (string/integer, required)

        Returns:
        AddEdge
        """
        source = Node.objects.get(client_id=int(from_node_id), graph__pk=int(graph_id))
        target = Node.objects.get(client_id=int(to_node_id), graph__pk=int(graph_id))
        edge   = Edge(client_id=int(client_id), source=source, target=target)

        edge.save()
        return AddEdge(edge=edge)

    def do(self):
        """
        Marks the edge as not deleted. This makes only sense when this command is
        reapplied/redone.

        Returns:
        None
        """
        self.edge.deleted = False
        self.edge.save()

    def undo(self):
        """
        Deletes the edge again by marking its deletion flag

        Returns:
        None
        """
        self.edge.deleted = True
        self.edge.save()

class AddGraph(Command):
    pass

class AddNode(Command):
    node = models.ForeignKey(Node, related_name='+')

    @staticmethod
    def create_of(graph_id, node_id, kind, x, y):
        """
        Convenience factory method for issueing an add node command. Note: this method
        will CREATE AND SAVE the node object required for the command.

        Arguments:
        graph_id -- the id of the graph that shall contain the node (string/integer, required)
        node_id  -- the client id(!) of the node as received from the client (string/integer, required)
        kind     -- a string identifying the node's kind (string/integer, required)
        x        -- x coordinate of the created node (string/integer, required)
        y        -- y coordinate of the created node (string/integer, required)
        """
        graph = Graph.objects.get(pk=int(graph_id))
        node  = Node(graph=graph, client_id=int(node_id), kind=kind, x=int(x), y=int(y))
        node.save()
        
        return AddNode(node=node)

    def do(self):
        """
        Add the node to the graph by removing its deletion flag. Is only necessary to be executed when 
        the reapplying/redoing this commmand.

        Returns:
        None
        """
        self.node.deleted = False
        self.node.save()

    def undo(self):
        """
        Removes the node from the graph by setting its deletion flag.

        Returns:
        None
        """
        self.node.deleted = True
        self.node.save()

class DeleteEdge(Command):
    """
    DeleteEdge class

    Command that is issued when an edge is deleted.

    Attributes:
    edge -- the edge that was deleted (Edge, required)
    """
    edge = models.ForeignKey(Edge, related_name='+')

    @staticmethod
    def of(graph_id, edge_id):
        """
        Convenience factory method for issueing a edge deletion command from unparsed user
        request values.

        Arguments:
        graph_id -- the id of the graph the edge is in (string/integer, required)
        edge_id  -- the client id(!) of the edge to be deleted (string/integer, required)
        """
        return DeleteEdge(Edge.objects.get(client_id=int(edge_id), node__graph__pk=int(graph_id)))

    def do(self):
        """
        Marks the edge as deleted by setting the flag

        Returns:
        None
        """
        self.edge.deleted = True
        self.edge.save()

    def undo(self):
        """
        Restores the edge by removing the deletion flag

        Returns:
        None
        """
        self.edge.deleted = False
        self.edge.save()

class DeleteGraph(Command):
    """
    DeleteGraph class

    Command that is issued when a graph is deleted.

    Attributes:
    graph -- the graph that is deleted (Graph, required)
    """
    graph = models.ForeignKey(Graph, related_name='+')

    @staticmethod
    def of(graph_id):
        """
        Convenience factory method for the creation of a delete graph command. Accepts
        the graph identification values as for instance received from user requests.

        Arguments:
        graph_id -- the id of the graph to be deleted (string/integer, required)

        Returns:
        DeleteGraph
        """
        return DeleteGraph(graph=Graph.objects.get(pk=int(graph_id)))

    def do(self):
        """
        Applies the deletion by setting the deletion flag of the graph

        Returns:
        None
        """
        self.graph.deleted = True
        self.graph.save()

    def undo(self):
        """
        Restores the graph by removing the deletion flag of the graph

        Returns:
        None
        """
        self.graph.deleted = False
        self.graph.save()

class DeleteNode(Command):
    """
    DeleteNode class

    This class models the deletion command for a node. Its do method will
    actually remove the node whereas undo restores it.

    Attributes:
    node -- the node that was deleted (Node, required)
    """
    node = modelsForeignKey(Node, related_name='+')

    @staticmethod
    def of(graph_id, node_id):
        """
        Convenience factory method for creating node deletion commands from values as e.g. received from
        client side requests

        Arguments:
        graph_id -- the id of the graph that contains the node to be deleted (string/integer, required)
        node_id  -- the client id(!) of the node to be deleted (string/integer, required)

        Returns:
        DeleteNode
        """
        return DeleteNode(node=Node.objects.get(client_id=int(node_id),graph__pk=int(graph_id)))

    def do(self):
        """
        Removes the given node from its graph by setting its deletion flag

        Returns:
        None
        """
        self.node.deleted = True
        self.node.save()

    def undo(self):
        """
        Restores the given node by removing the deletion flag

        Returns:
        None
        """
        self.node.deleted = False
        self.node.save()

class MoveNode(Command):
    node  = models.ForeignKey(Node, related_name='+')
    old_x = models.IntegerField()
    old_y = models.IntegerField()
    new_x = models.IntegerField()
    new_y = models.IntegerField()

    @staticmethod
    def of(graph_id, node_id, new_x, new_y):
        node = Node.objects.get(client_id=int(node_id), graph__pk=int(graph_id))

        return MoveNode(node=node, old_x=node.x, old_y=node.y, new_x=new_x, new_y=new_y)

    def do(self):
        self.node.x = self.new_x
        self.node.y = self.new_y
        self.node.save()

    def undo(self):
        self.node.x = self.old_x
        self.node.y = self.old_y
        self.node.save()

class PropertyChanged(Command):
    """
    PropertyChanged class

    This command models the value change of a node's property. Its do method will
    apply the value change, whereas the undo method will set the property back to
    its previous state.

    Attributes:
    property  -- the property whichs value changed (Property, required)
    old_value -- the value of the property before the change (string, required)
    new_value -- updated value of the property (string, required)
    """
    property  = models.ForeignKey(Property, related_name='+')
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)

    @staticmethod
    def create_of(graph_id, node_id, key, new_value):
        """
        Convenience factory method for issueing a property changed command from values as e.g. received from
        client side requests. If the property does not yet exist it is being CREATED AND SAVED.

        Arguments:
        graph_id  -- the id of the graph that contains the node thats property changed (string/integer, required)
        node_id   -- the client id(!) of the node thats property changed (string/integer, required)
        key       -- this is the name of the property that changed (string, required)
        new_value -- is the new value of the property (string, required)

        Returns:
        PropertyChanged
        """
        node_property, created = Property.objects.get_or_create(key=key, node__client_id=int(node_id), node__graph__pk=int(graph_id))
        if created:
            node_property.save()

        return PropertyChanged(property=node_property, old_value=node_property.value, new_value=new_value)

    def do(self):
        """
        Apply the change to the property - i.e. set new_value

        Returns:
        None
        """
        self.property.value = self.new_value
        self.property.save()

    def undo(self):
        """
        Reverts the change -- i.e. set old_value

        Returns:
        None
        """
        self.property.value = self.old_value
        self.property.save()