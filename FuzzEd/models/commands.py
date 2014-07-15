from django.db import models

from FuzzEd.lib.jsonfield import JSONField
from edge import Edge
from graph import Graph
from node import Node
from project import Project
import notations


class Command(models.Model):
    """
    Class [abstract]: Command

    Abstract base class for any command in the system. Required for type correctness and contains meta data needed in
    every subtype.

    Fields:
     {bool}           undoable     - indicates if command can be undone (default: False)
     {const datetime} insert_date  - moment when the command was issued (default: now)
    """
    class Meta:
        app_label = 'FuzzEd'
        abstract  = True

    undoable    = models.BooleanField(default=False)
    insert_date = models.DateTimeField(auto_now_add=True, editable=False)

    def do(self):
        """
        Method [abstract]: do

        Stub for the command's do behaviour. Must be overwritten in sublasses.

        Returns:
         {None}
        """
        raise NotImplementedError('[Abstract Method] Implement in subclass')

    def undo(self):
        """
        Method [abstract]:
        
        Stub for the command's undo behaviour. Must be overwritten in sublcasses.

        Returns:
         {None}
        """
        raise NotImplementedError('[Abstract Method] Implement in subclass')
        
class AddProject(Command):
    """
    Class: AddProject
    
    Extends: Command
        
    Command that is issued when an a new project was created.
        
    """
    project = models.ForeignKey(Project, related_name='+')
    
    @classmethod
    def create_from(cls, name, owner):
        """
        Method [static]: create_from
        
        Convenience factory method for issuing an add project command from parameters as received from API calls.
        NOTE: A project object is created and saved when invoking this method.
         
        Parameters:
        {str}  name     - name of the project
        {User} owner    - the user that owns this project
        """
        project = Project(name=name, owner=owner, deleted=True)
        project.save()
         
        return cls(project=project)
   
    def do(self):
        self.project.deleted = False
        self.project.save()
        self.save()

    def undo(self):
        self.project.deleted = True
        self.project.save()
        self.save()
    
class AddEdge(Command):
    """
    Class: AddEdge
    
    Extends: Command

    Command that is issued when an edge was added to a graph.

    Fields:
     {<Edge>} edge  - the edge that was added
    """
    edge = models.ForeignKey(Edge, related_name='+')

    @classmethod
    def create_from(cls, graph_id, client_id, from_id, to_id):
        """
        Method [static]: create_from

        Convenience factory method for issuing an add edge command from parameters as received from API calls.
        NOTE: the edge object that is required for this command is created and saved when invoking this method.

        Parameters:
         {str} graph_id  - the id of the graph that will contain this edge
         {str} client_id - the id of the edge as set on the client
         {str} from_id   - the client id(!) of the node the edge origins
         {str} to_id     - the client id(!) of the node that terminates the edge

        Returns:
         {<AddEdge>} the add edge command instance
        """
        graph  = Graph.objects.get(pk=int(graph_id))
        source = Node.objects.get(client_id=int(from_id), graph=graph)
        target = Node.objects.get(client_id=int(to_id), graph=graph)
        edge   = Edge(client_id=int(client_id), graph=graph, source=source, target=target, deleted=True)
        edge.save()

        return cls(edge=edge)

    def do(self):
        """
        Method: do

        Adds the edge to the graph by removing the deleted flag from the instance. As the edge is by default marked as
        not deleted the invocation of this method is only mandatory when redoing this command.

        Returns:
         {None}
        """
        self.edge.deleted = False
        self.edge.save()
        self.save()

    def undo(self):
        """
        Method: undo
        
        Deletes the edge by setting its deletion flag.

        Returns:
         {None}
        """
        self.edge.deleted = True
        self.edge.save()
        self.save()

class AddGraph(Command):
    """
    Class: AddGraph

    Extends: Command
    
    Command that is issued when a graph was added.
    
    Fields:
     {<Graph>} graph  - the graph that was added
    """
    graph = models.ForeignKey(Graph, related_name='+')

    @classmethod
    def create_from(cls, kind, name, owner, project, add_default_nodes=True):
        """
        Method [static]: create_from
        
        Convenience factory method for issuing an add graph command from parameters as received from API calls.
        NOTE: the graph object that is required for this command is created and saved when invoking this method.
        
        Parameters:
         {str}  kind     - type identifier for the graph's notation
         {str}  name     - name of the graph
         {User} owner    - the user that owns this graph
        
        Returns:
         {<AddGraph>} the add graph command instance
        """
        graph = Graph(kind=kind, name=name, owner=owner, project=project, deleted=True)
        graph.save()
        if add_default_nodes:
            # pre-initialize the graph with default nodes
            notation = notations.by_kind[kind]
            if 'defaults' in notation:
                for index, node in enumerate(notation['defaults']['nodes']):
                    node.update({'properties': {}})

                    # use index as node ID
                    # this is unique since all other IDs are time stamps
                    command = AddNode.create_from(graph_id=graph.pk, node_id=index, **node)
                    command.undoable = False
                    command.do()
        return cls(graph=graph)

    def do(self):
        self.graph.deleted = False
        self.graph.save()
        self.save()

    def undo(self):
        self.graph.deleted = True
        self.graph.save()
        self.save()

class AddNode(Command):
    """
    Class: AddNode
    
    Extends: Command

    Command that is issued when a node was added to a graph.

    Fields:
     {<Node>} node  - the node that was added
    """
    node = models.ForeignKey(Node, related_name='+')

    @classmethod
    def create_from(cls, graph_id, node_id, kind, x, y, properties):
        """
        Method [static]: create_from

        Convenience factory method for issuing an add node command from parameters as received from API calls.
        NOTE: the node object that is required for this command is created and saved when invoking this method.

        Arguments:
         {str} graph_id  - the id of the graph the node is added to
         {str} node_id   - the client id(!) of the node as set on the client
         {str} kind      - the node's identification string
         {str} x         - x coordinate of the added node
         {str} y         - y coordinate of the added node
         dict(str, str) properties - dictionary with the initial node properties 
                      
        Returns:
         {<AddNode>} - the add node command instance
        """
        graph = Graph.objects.get(pk=int(graph_id))
        node  = Node(graph=graph, client_id=int(node_id), kind=kind, x=int(x), y=int(y), deleted=True)
        node.save()
        for k, v in properties.iteritems():
            node.set_attr(k, v['value'])
        
        return cls(node=node)

    def do(self):
        """
        Method: do
        
        Adds the node to the graph by removing the deleted flag from the instance. As the node is by default marked as
        not deleted the invocation of this method is only mandatory when redoing this command.
        
        Returns:
         {None}
        """
        self.node.deleted = False
        self.node.save()
        self.save()

    def undo(self):
        """
        Method: do
        
        Removes the node from the graph by setting its deletion flag.

        Returns:
         {None}
        """
        self.node.deleted = True
        self.node.save()
        self.save()

class ChangeNode(Command):
    """
    Class: ChangeNode
    
    Extends: Command

    Command that is issued when properties of a node change
    """
    node = models.ForeignKey(Node, related_name='+')

    @classmethod
    def create_from(cls, graph_id, node_id, updated_properties):
        assert(False)       # Command objects are deprecated.

    def do(self):
        """
        Method: do
        
        Apply the change to the node or it's corresponding property - i.e. set the new value

        Returns:
         {None}
        """
        for change in self.changes.all():
            self.node.set_attr(change.key, change.new_value)
        self.node.save()
        self.save()

    def undo(self):
        """
        Method: undo
        
        Reverts the changes to the node or it's corresponding property - i.e. set old value

        Returns:
         {None}
        """
        for change in self.changes:
            self.node.set_attr(change.key, change.old_value)
        self.node.save()
        self.save()

class ChangeEdge(Command):
    """
    Class: ChangeEdge

    Extends: Command

    Command that is issued when properties of an edge change
    """
    edge = models.ForeignKey(Edge, related_name='+')

    @classmethod
    def create_from(cls, graph_id, edge_id, updated_properties):
        assert(False)           # Command objects are deprecated

    def do(self):
        """
        Method: do

        Apply the change to the node or it's corresponding property - i.e. set the new value

        Returns:
         {None}
        """
        for change in self.changes.all():
            self.edge.set_attr(change.key, change.new_value)
        self.edge.save()
        self.save()

    def undo(self):
        """
        Method: undo

        Reverts the changes to the node or it's corresponding property - i.e. set old value

        Returns:
         {None}
        """
        for change in self.changes:
            self.edge.set_attr(change.key, change.old_value)
        self.edge.save()
        self.save()

class PropertyChange(models.Model):
    """
    Class: PropertyChange
    
    Extends: models.Model
    
    Small inline container class to model arbitrary number of property changes. 
    
    Attributes:
     {<ChangeNode>} command   - the command this property change belongs to
     {str}          old_value - the value of the property before the change
     {str}          new_value - the updated value
    """
    class Meta:
        app_label = 'FuzzEd'

    command   = models.ForeignKey(ChangeNode, related_name='changes')
    key       = models.CharField(max_length=255)
    old_value = JSONField()
    new_value = JSONField()

class EdgePropertyChange(models.Model):
    """
    Class: EdgePropertyChange

    Extends: models.Model

    Small inline container class to model arbitrary number of edge's property changes.

    Attributes:
     {<ChangeEdge>} command   - the command this property change belongs to
     {str}          old_value - the value of the property before the change
     {str}          new_value - the updated value
    """
    class Meta:
        app_label = 'FuzzEd'

    command   = models.ForeignKey(ChangeEdge, related_name='changes')
    key       = models.CharField(max_length=255)
    old_value = JSONField()
    new_value = JSONField()

class DeleteEdge(Command):
    """
    Class: DeleteEdge
    
    Extends: Command

    Command that is issued when an edge is deleted.

    Fields:
     {<Edge>} edge  - the edge that shall be deleted
    """
    edge = models.ForeignKey(Edge, related_name='+')

    @classmethod
    def create_from(cls, graph_id, edge_id):
        """
        Method [static]: create_from
        
        Convenience factory method for issuing a delete node command from parameters as received from API calls.

        Arguments:
         {str} graph_id  - the id of the graph that contains the edge to be deleted
         {str} edge_id   - the client id(!) of the edge to be deleted
        
        Returns:
         {<DeleteEdge>}  - the delete edge command instance
        """
        edge = Edge.objects.get(client_id=int(edge_id), graph__pk=int(graph_id))
        return cls(edge=edge)

    def do(self):
        """
        Method: do
        
        Deletes the edge from the graph by setting its deletion flag

        Returns:
         {None}
        """
        self.edge.deleted = True
        self.edge.save()
        self.save()

    def undo(self):
        """
        Method: undo
        
        Restores the edge by removing its deletion flag

        Returns:
         {None}
        """
        self.edge.deleted = False
        self.edge.save()

class DeleteGraph(Command):
    """
    Class: Delete Graph
    
    Extends: Command

    Command that is issued when a graph is deleted.

    Fields:
     {<Graph>} graph  - the graph that shall be deleted
    """
    graph = models.ForeignKey(Graph, related_name='+')

    @classmethod
    def create_from(cls, graph_id):
        """
        Method [static]: create_from
        
        Convenience factory method for issuing a delete graph command from parameters as received from API calls.

        Parameters:
         {str} graph_id  - the id of the graph to be deleted

        Returns:
         {<DeleteGraph>}  - the delete graph command instance
        """
        return cls(graph=Graph.objects.get(pk=int(graph_id)))

    def do(self):
        """
        Method: do
        
        Deletes the graph by setting its deletion flag

        Returns:
         {None}
        """
        self.graph.deleted = True
        self.graph.save()
        self.save()

    def undo(self):
        """
        Method: undo
        
        Restores the graph by removing its deletion flag

        Returns:
         {None}
        """
        self.graph.deleted = False
        self.graph.save()

class DeleteProject(Command):
    """
    Class: DeleteProject
    
    Extends: Command

    Command that is issued when a project is deleted.

    Fields:
     {<Project>} project  - the project that shall be deleted
    """
    project = models.ForeignKey(Project, related_name='+')

    @classmethod
    def create_from(cls, project_id):
        """
        Method [static]: create_from
        
        Convenience factory method for issuing a delete project command from parameters as received from API calls.

        Parameters:
         {str} project_id  - the id of the project to be deleted

        Returns:
         {<DeleteProject>}  - the delete project command instance
        """
        return cls(project=Project.objects.get(pk=int(project_id)))

    def do(self):
        """
        Method: do
        
        Deletes the project by setting its deletion flag

        Returns:
         {None}
        """
        self.project.deleted = True
        self.project.save()
        self.save()

    def undo(self):
        """
        Method: undo
        
        Restores the project by removing its deletion flag

        Returns:
         {None}
        """
        self.project.deleted = False
        self.project.save()

class DeleteNode(Command):
    """
    Class: DeleteNode
    
    Extends: Command

    Command that is issued when a node is deleted

    Fields:
     {<Node>} node  - the node that shall be deleted
    """
    node = models.ForeignKey(Node, related_name='+')

    @classmethod
    def create_from(cls, graph_id, node_id):
        """
        Method [static]: create_from
        
        Convenience factory method for issuing an add node command from parameters as received from API calls.

        Parameters:
         {str} graph_id  - the id of the graph that contains the node to be deleted
         {str} node_id   - the client id(!) of the node to be deleted

        Returns:
         {<DeleteNode>} the delete node command instance
        """
        return cls(node=Node.objects.get(client_id=int(node_id),graph__pk=int(graph_id)))

    def do(self):
        """
        Method: do
        
        Removes the node from the containing graph by setting its deletion flag

        Returns:
         {None}
        """
        self.node.deleted = True
        self.node.save()
        self.save()

    def undo(self):
        """
        Method: undo
        
        Restores the given node by removing its deletion flag

        Returns:
         {None}
        """
        self.node.deleted = False
        self.node.save()

class RenameGraph(Command):
    """
    Class: RenameGraph
    
    Extends: Command

    Command that is issued when a graph is renamed

    Fields:
     {<Node>} node  - the node that shall be deleted
    """
    graph    = models.ForeignKey(Graph, related_name='+')
    old_name = models.CharField(max_length=255)
    new_name = models.CharField(max_length=255)

    @classmethod
    def create_from(cls, graph_id, new_name):
        """
        Method [static]: create_from
        
        Convenience factory method for issuing an add node command from parameters as received from API calls.

        Parameters:
         {str} graph_id  - the id of the graph to be renamed
         {str} new_name  - the new name given to the graph

        Returns:
         {<RenameGraph>} the rename graph instance
        """
        graph = Graph.objects.get(pk=int(graph_id))

        return cls(graph=graph, old_name=graph.name, new_name=new_name)

    def do(self):
        """
        Method: do
        
        Assigns a new name for the graph

        Returns:
         {None}
        """
        self.graph.name = self.new_value
        self.graph.save()
        self.save()

    def undo(self):
        """
        Method: undo
        
        Restores the old name of the graph

        Returns:
         {None}
        """
        self.graph.name = self.old_value
        self.graph.save()
        self.save()
