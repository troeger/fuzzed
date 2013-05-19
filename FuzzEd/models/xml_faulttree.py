# FuzzEd/models/xml_faulttree.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:0c3643272b4de760c38b0556be1c2c4346c7368c
# Generated 2013-05-13 20:55:56.312129 by PyXB version 1.2.1
# Namespace net.faulttree

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:be24c6bd-bbfe-11e2-b66d-58b035ff3a58')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'net.faulttree', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.
    
    @kw default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# List simple type: {net.faulttree}idlist
# superclasses pyxb.binding.datatypes.anySimpleType
class idlist (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.int."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'idlist')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 174, 2)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.int
idlist._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'idlist', idlist)

# Complex type {net.faulttree}Annotation with content type EMPTY
class Annotation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.faulttree}Annotation with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Annotation')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 5, 2)
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Annotation', Annotation)


# Complex type {net.faulttree}Probability with content type EMPTY
class Probability (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.faulttree}Probability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Probability')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 6, 2)
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Probability', Probability)


# Complex type {net.faulttree}AnnotatedElement with content type ELEMENT_ONLY
class AnnotatedElement (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.faulttree}AnnotatedElement with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnnotatedElement')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 8, 2)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element annotations uses Python identifier annotations
    __annotations = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'annotations'), 'annotations', '__net_faulttree_AnnotatedElement_annotations', True, pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6), )

    
    annotations = property(__annotations.value, __annotations.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__net_faulttree_AnnotatedElement_id', pyxb.binding.datatypes.int, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 12, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 12, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__net_faulttree_AnnotatedElement_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 13, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 13, 4)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __annotations.name() : __annotations
    }
    _AttributeMap = {
        __id.name() : __id,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'AnnotatedElement', AnnotatedElement)


# Complex type {net.faulttree}Model with content type ELEMENT_ONLY
class Model (AnnotatedElement):
    """Complex type {net.faulttree}Model with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Model')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 16, 2)
    # Base type is AnnotatedElement
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement

    _ElementMap = AnnotatedElement._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Model', Model)


# Complex type {net.faulttree}Node with content type ELEMENT_ONLY
class Node (AnnotatedElement):
    """Complex type {net.faulttree}Node with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 23, 2)
    # Base type is AnnotatedElement
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children uses Python identifier children
    __children = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'children'), 'children', '__net_faulttree_Node_children', True, pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10), )

    
    children = property(__children.value, __children.set, None, None)

    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x uses Python identifier x
    __x = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'x'), 'x', '__net_faulttree_Node_x', pyxb.binding.datatypes.int)
    __x._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 29, 8)
    __x._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 29, 8)
    
    x = property(__x.value, __x.set, None, None)

    
    # Attribute y uses Python identifier y
    __y = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'y'), 'y', '__net_faulttree_Node_y', pyxb.binding.datatypes.int)
    __y._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 30, 8)
    __y._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 30, 8)
    
    y = property(__y.value, __y.set, None, None)


    _ElementMap = AnnotatedElement._ElementMap.copy()
    _ElementMap.update({
        __children.name() : __children
    })
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    _AttributeMap.update({
        __x.name() : __x,
        __y.name() : __y
    })
Namespace.addCategoryObject('typeBinding', u'Node', Node)


# Complex type {net.faulttree}CrispProbability with content type EMPTY
class CrispProbability (Probability):
    """Complex type {net.faulttree}CrispProbability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CrispProbability')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 60, 2)
    # Base type is Probability
    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'value'), 'value_', '__net_faulttree_CrispProbability_value', pyxb.binding.datatypes.double, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 63, 8)
    __value._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 63, 8)
    
    value_ = property(__value.value, __value.set, None, None)


    _ElementMap = Probability._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Probability._AttributeMap.copy()
    _AttributeMap.update({
        __value.name() : __value
    })
Namespace.addCategoryObject('typeBinding', u'CrispProbability', CrispProbability)


# Complex type {net.faulttree}ChildNode with content type ELEMENT_ONLY
class ChildNode (Node):
    """Complex type {net.faulttree}ChildNode with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChildNode')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 35, 2)
    # Base type is Node
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = Node._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Node._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ChildNode', ChildNode)


# Complex type {net.faulttree}FaultTree with content type ELEMENT_ONLY
class FaultTree_ (Model):
    """Complex type {net.faulttree}FaultTree with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FaultTree')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 42, 2)
    # Base type is Model
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element topEvent uses Python identifier topEvent
    __topEvent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'topEvent'), 'topEvent', '__net_faulttree_FaultTree__topEvent', False, pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 46, 10), )

    
    topEvent = property(__topEvent.value, __topEvent.set, None, None)

    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement

    _ElementMap = Model._ElementMap.copy()
    _ElementMap.update({
        __topEvent.name() : __topEvent
    })
    _AttributeMap = Model._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'FaultTree', FaultTree_)


# Complex type {net.faulttree}TopEvent with content type ELEMENT_ONLY
class TopEvent_ (Node):
    """Complex type {net.faulttree}TopEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TopEvent')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 53, 2)
    # Base type is Node
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = Node._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Node._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TopEvent', TopEvent_)


# Complex type {net.faulttree}Gate with content type ELEMENT_ONLY
class Gate (ChildNode):
    """Complex type {net.faulttree}Gate with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Gate')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 69, 2)
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Gate', Gate)


# Complex type {net.faulttree}TransferIn with content type ELEMENT_ONLY
class TransferIn_ (ChildNode):
    """Complex type {net.faulttree}TransferIn with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TransferIn')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 106, 2)
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute fromModelId uses Python identifier fromModelId
    __fromModelId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'fromModelId'), 'fromModelId', '__net_faulttree_TransferIn__fromModelId', pyxb.binding.datatypes.int, required=True)
    __fromModelId._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 109, 8)
    __fromModelId._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 109, 8)
    
    fromModelId = property(__fromModelId.value, __fromModelId.set, None, None)

    
    # Attribute maxCosts uses Python identifier maxCosts
    __maxCosts = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'maxCosts'), 'maxCosts', '__net_faulttree_TransferIn__maxCosts', pyxb.binding.datatypes.int, unicode_default=u'0')
    __maxCosts._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 110, 8)
    __maxCosts._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 110, 8)
    
    maxCosts = property(__maxCosts.value, __maxCosts.set, None, None)


    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        __fromModelId.name() : __fromModelId,
        __maxCosts.name() : __maxCosts
    })
Namespace.addCategoryObject('typeBinding', u'TransferIn', TransferIn_)


# Complex type {net.faulttree}UndevelopedEvent with content type ELEMENT_ONLY
class UndevelopedEvent_ (ChildNode):
    """Complex type {net.faulttree}UndevelopedEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UndevelopedEvent')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 116, 2)
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'UndevelopedEvent', UndevelopedEvent_)


# Complex type {net.faulttree}BasicEvent with content type ELEMENT_ONLY
class BasicEvent_ (ChildNode):
    """Complex type {net.faulttree}BasicEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BasicEvent')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 130, 2)
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Element probability uses Python identifier probability
    __probability = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'probability'), 'probability', '__net_faulttree_BasicEvent__probability', False, pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 134, 10), )

    
    probability = property(__probability.value, __probability.set, None, None)

    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        __probability.name() : __probability
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'BasicEvent', BasicEvent_)


# Complex type {net.faulttree}IntermediateEvent with content type ELEMENT_ONLY
class IntermediateEvent_ (ChildNode):
    """Complex type {net.faulttree}IntermediateEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IntermediateEvent')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 142, 2)
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'IntermediateEvent', IntermediateEvent_)


# Complex type {net.faulttree}And with content type ELEMENT_ONLY
class And_ (Gate):
    """Complex type {net.faulttree}And with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'And')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 75, 2)
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'And', And_)


# Complex type {net.faulttree}Or with content type ELEMENT_ONLY
class Or_ (Gate):
    """Complex type {net.faulttree}Or with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Or')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 82, 2)
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Or', Or_)


# Complex type {net.faulttree}Xor with content type ELEMENT_ONLY
class Xor_ (Gate):
    """Complex type {net.faulttree}Xor with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Xor')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 89, 2)
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Xor', Xor_)


# Complex type {net.faulttree}VotingOr with content type ELEMENT_ONLY
class VotingOr_ (Gate):
    """Complex type {net.faulttree}VotingOr with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VotingOr')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 96, 2)
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute k uses Python identifier k
    __k = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'k'), 'k', '__net_faulttree_VotingOr__k', pyxb.binding.datatypes.int, required=True)
    __k._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 99, 8)
    __k._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 99, 8)
    
    k = property(__k.value, __k.set, None, None)


    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        __k.name() : __k
    })
Namespace.addCategoryObject('typeBinding', u'VotingOr', VotingOr_)


# Complex type {net.faulttree}HouseEvent with content type ELEMENT_ONLY
class HouseEvent_ (BasicEvent_):
    """Complex type {net.faulttree}HouseEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HouseEvent')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 123, 2)
    # Base type is BasicEvent_
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Element probability (probability) inherited from {net.faulttree}BasicEvent
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = BasicEvent_._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'HouseEvent', HouseEvent_)


# Complex type {net.faulttree}BasicEventSet with content type ELEMENT_ONLY
class BasicEventSet_ (BasicEvent_):
    """Complex type {net.faulttree}BasicEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BasicEventSet')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 149, 2)
    # Base type is BasicEvent_
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Element probability (probability) inherited from {net.faulttree}BasicEvent
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quantity'), 'quantity', '__net_faulttree_BasicEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 152, 8)
    __quantity._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 152, 8)
    
    quantity = property(__quantity.value, __quantity.set, None, None)


    _ElementMap = BasicEvent_._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
Namespace.addCategoryObject('typeBinding', u'BasicEventSet', BasicEventSet_)


# Complex type {net.faulttree}IntermediateEventSet with content type ELEMENT_ONLY
class IntermediateEventSet_ (IntermediateEvent_):
    """Complex type {net.faulttree}IntermediateEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IntermediateEventSet')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 158, 2)
    # Base type is IntermediateEvent_
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quantity'), 'quantity', '__net_faulttree_IntermediateEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 161, 8)
    __quantity._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 161, 8)
    
    quantity = property(__quantity.value, __quantity.set, None, None)


    _ElementMap = IntermediateEvent_._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = IntermediateEvent_._AttributeMap.copy()
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
Namespace.addCategoryObject('typeBinding', u'IntermediateEventSet', IntermediateEventSet_)


# Complex type {net.faulttree}DynamicGate with content type ELEMENT_ONLY
class DynamicGate (Gate):
    """Complex type {net.faulttree}DynamicGate with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DynamicGate')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 168, 2)
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node

    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'DynamicGate', DynamicGate)


# Complex type {net.faulttree}ColdSpare with content type ELEMENT_ONLY
class ColdSpare_ (DynamicGate):
    """Complex type {net.faulttree}ColdSpare with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ColdSpare')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 178, 2)
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute spareIds uses Python identifier spareIds
    __spareIds = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'spareIds'), 'spareIds', '__net_faulttree_ColdSpare__spareIds', idlist, required=True)
    __spareIds._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 181, 8)
    __spareIds._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 181, 8)
    
    spareIds = property(__spareIds.value, __spareIds.set, None, None)


    _ElementMap = DynamicGate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = DynamicGate._AttributeMap.copy()
    _AttributeMap.update({
        __spareIds.name() : __spareIds
    })
Namespace.addCategoryObject('typeBinding', u'ColdSpare', ColdSpare_)


# Complex type {net.faulttree}PriorityAnd with content type ELEMENT_ONLY
class PriorityAnd_ (DynamicGate):
    """Complex type {net.faulttree}PriorityAnd with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PriorityAnd')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 187, 2)
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute priorityIds uses Python identifier priorityIds
    __priorityIds = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'priorityIds'), 'priorityIds', '__net_faulttree_PriorityAnd__priorityIds', idlist, required=True)
    __priorityIds._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 190, 8)
    __priorityIds._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 190, 8)
    
    priorityIds = property(__priorityIds.value, __priorityIds.set, None, None)


    _ElementMap = DynamicGate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = DynamicGate._AttributeMap.copy()
    _AttributeMap.update({
        __priorityIds.name() : __priorityIds
    })
Namespace.addCategoryObject('typeBinding', u'PriorityAnd', PriorityAnd_)


# Complex type {net.faulttree}Sequence with content type ELEMENT_ONLY
class Sequence_ (DynamicGate):
    """Complex type {net.faulttree}Sequence with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Sequence')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 196, 2)
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute eventSequence uses Python identifier eventSequence
    __eventSequence = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'eventSequence'), 'eventSequence', '__net_faulttree_Sequence__eventSequence', idlist, required=True)
    __eventSequence._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 199, 8)
    __eventSequence._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 199, 8)
    
    eventSequence = property(__eventSequence.value, __eventSequence.set, None, None)


    _ElementMap = DynamicGate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = DynamicGate._AttributeMap.copy()
    _AttributeMap.update({
        __eventSequence.name() : __eventSequence
    })
Namespace.addCategoryObject('typeBinding', u'Sequence', Sequence_)


# Complex type {net.faulttree}FDEP with content type ELEMENT_ONLY
class FDEP_ (DynamicGate):
    """Complex type {net.faulttree}FDEP with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FDEP')
    _XSDLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 205, 2)
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute triggeredEvents uses Python identifier triggeredEvents
    __triggeredEvents = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'triggeredEvents'), 'triggeredEvents', '__net_faulttree_FDEP__triggeredEvents', idlist, required=True)
    __triggeredEvents._DeclarationLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 208, 8)
    __triggeredEvents._UseLocation = pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 208, 8)
    
    triggeredEvents = property(__triggeredEvents.value, __triggeredEvents.set, None, None)


    _ElementMap = DynamicGate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = DynamicGate._AttributeMap.copy()
    _AttributeMap.update({
        __triggeredEvents.name() : __triggeredEvents
    })
Namespace.addCategoryObject('typeBinding', u'FDEP', FDEP_)


FaultTree = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FaultTree'), FaultTree_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 51, 2))
Namespace.addCategoryObject('elementBinding', FaultTree.name().localName(), FaultTree)

TopEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TopEvent'), TopEvent_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 58, 2))
Namespace.addCategoryObject('elementBinding', TopEvent.name().localName(), TopEvent)

TransferIn = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TransferIn'), TransferIn_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 114, 2))
Namespace.addCategoryObject('elementBinding', TransferIn.name().localName(), TransferIn)

UndevelopedEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'UndevelopedEvent'), UndevelopedEvent_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 121, 2))
Namespace.addCategoryObject('elementBinding', UndevelopedEvent.name().localName(), UndevelopedEvent)

BasicEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BasicEvent'), BasicEvent_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 140, 2))
Namespace.addCategoryObject('elementBinding', BasicEvent.name().localName(), BasicEvent)

IntermediateEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IntermediateEvent'), IntermediateEvent_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 147, 2))
Namespace.addCategoryObject('elementBinding', IntermediateEvent.name().localName(), IntermediateEvent)

And = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'And'), And_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 80, 2))
Namespace.addCategoryObject('elementBinding', And.name().localName(), And)

Or = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Or'), Or_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 87, 2))
Namespace.addCategoryObject('elementBinding', Or.name().localName(), Or)

Xor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Xor'), Xor_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 94, 2))
Namespace.addCategoryObject('elementBinding', Xor.name().localName(), Xor)

VotingOr = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'VotingOr'), VotingOr_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 103, 2))
Namespace.addCategoryObject('elementBinding', VotingOr.name().localName(), VotingOr)

HouseEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'HouseEvent'), HouseEvent_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 128, 2))
Namespace.addCategoryObject('elementBinding', HouseEvent.name().localName(), HouseEvent)

BasicEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BasicEventSet'), BasicEventSet_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 156, 2))
Namespace.addCategoryObject('elementBinding', BasicEventSet.name().localName(), BasicEventSet)

IntermediateEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IntermediateEventSet'), IntermediateEventSet_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 165, 2))
Namespace.addCategoryObject('elementBinding', IntermediateEventSet.name().localName(), IntermediateEventSet)

ColdSpare = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ColdSpare'), ColdSpare_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 185, 2))
Namespace.addCategoryObject('elementBinding', ColdSpare.name().localName(), ColdSpare)

PriorityAnd = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PriorityAnd'), PriorityAnd_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 194, 2))
Namespace.addCategoryObject('elementBinding', PriorityAnd.name().localName(), PriorityAnd)

Sequence = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Sequence'), Sequence_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 203, 2))
Namespace.addCategoryObject('elementBinding', Sequence.name().localName(), Sequence)

FDEP = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FDEP'), FDEP_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 212, 2))
Namespace.addCategoryObject('elementBinding', FDEP.name().localName(), FDEP)



AnnotatedElement._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'annotations'), Annotation, scope=AnnotatedElement, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AnnotatedElement._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AnnotatedElement._Automaton = _BuildAutomaton()




def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Model._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Model._Automaton = _BuildAutomaton_()




Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'children'), ChildNode, scope=Node, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Node._Automaton = _BuildAutomaton_2()




def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ChildNode._Automaton = _BuildAutomaton_3()




FaultTree_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'topEvent'), TopEvent_, scope=FaultTree_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 46, 10)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FaultTree_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FaultTree_._UseForTag(pyxb.namespace.ExpandedName(None, u'topEvent')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 46, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FaultTree_._Automaton = _BuildAutomaton_4()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
TopEvent_._Automaton = _BuildAutomaton_5()




def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Gate._Automaton = _BuildAutomaton_6()




def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
TransferIn_._Automaton = _BuildAutomaton_7()




def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
UndevelopedEvent_._Automaton = _BuildAutomaton_8()




BasicEvent_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'probability'), Probability, scope=BasicEvent_, location=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 134, 10)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'probability')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 134, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BasicEvent_._Automaton = _BuildAutomaton_9()




def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
IntermediateEvent_._Automaton = _BuildAutomaton_10()




def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
And_._Automaton = _BuildAutomaton_11()




def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Or_._Automaton = _BuildAutomaton_12()




def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Xor_._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
VotingOr_._Automaton = _BuildAutomaton_14()




def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'probability')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 134, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
HouseEvent_._Automaton = _BuildAutomaton_15()




def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'probability')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 134, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BasicEventSet_._Automaton = _BuildAutomaton_16()




def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
IntermediateEventSet_._Automaton = _BuildAutomaton_17()




def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DynamicGate._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DynamicGate._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DynamicGate._Automaton = _BuildAutomaton_18()




def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ColdSpare_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ColdSpare_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ColdSpare_._Automaton = _BuildAutomaton_19()




def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PriorityAnd_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(PriorityAnd_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
PriorityAnd_._Automaton = _BuildAutomaton_20()




def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Sequence_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Sequence_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Sequence_._Automaton = _BuildAutomaton_21()




def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FDEP_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 10, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(FDEP_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location('/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/faulttree.xsd', 27, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
FDEP_._Automaton = _BuildAutomaton_22()

