# ore/models/xml_faulttree.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:0c3643272b4de760c38b0556be1c2c4346c7368c
# Generated 2019-01-09 14:06:28.478291 by PyXB version 1.2.6 using Python 2.7.15.candidate.1
# Namespace net.faulttree

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c1f84e9a-1417-11e9-9981-0242c0a83004')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('net.faulttree', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
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
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
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

    """Simple type that is a list of pyxb.binding.datatypes.string."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'idlist')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 186, 4)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.string
idlist._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'idlist', idlist)
_module_typeBindings.idlist = idlist

# Complex type {net.faulttree}Annotation with content type EMPTY
class Annotation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.faulttree}Annotation with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Annotation')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 5, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Annotation = Annotation
Namespace.addCategoryObject('typeBinding', 'Annotation', Annotation)


# Complex type {net.faulttree}Probability with content type EMPTY
class Probability (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.faulttree}Probability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Probability')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 6, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Probability = Probability
Namespace.addCategoryObject('typeBinding', 'Probability', Probability)


# Complex type {net.faulttree}AnnotatedElement with content type ELEMENT_ONLY
class AnnotatedElement (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.faulttree}AnnotatedElement with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnnotatedElement')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 8, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element annotations uses Python identifier annotations
    __annotations = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'annotations'), 'annotations', '__net_faulttree_AnnotatedElement_annotations', True, pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12), )

    
    annotations = property(__annotations.value, __annotations.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__net_faulttree_AnnotatedElement_id', pyxb.binding.datatypes.string, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 12, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 12, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__net_faulttree_AnnotatedElement_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 13, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 13, 8)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __annotations.name() : __annotations
    })
    _AttributeMap.update({
        __id.name() : __id,
        __name.name() : __name
    })
_module_typeBindings.AnnotatedElement = AnnotatedElement
Namespace.addCategoryObject('typeBinding', 'AnnotatedElement', AnnotatedElement)


# Complex type {net.faulttree}Model with content type ELEMENT_ONLY
class Model (AnnotatedElement):
    """Complex type {net.faulttree}Model with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Model')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 16, 4)
    _ElementMap = AnnotatedElement._ElementMap.copy()
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    # Base type is AnnotatedElement
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Model = Model
Namespace.addCategoryObject('typeBinding', 'Model', Model)


# Complex type {net.faulttree}Node with content type ELEMENT_ONLY
class Node (AnnotatedElement):
    """Complex type {net.faulttree}Node with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Node')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 23, 4)
    _ElementMap = AnnotatedElement._ElementMap.copy()
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    # Base type is AnnotatedElement
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children uses Python identifier children
    __children = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'children'), 'children', '__net_faulttree_Node_children', True, pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20), )

    
    children = property(__children.value, __children.set, None, None)

    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x uses Python identifier x
    __x = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'x'), 'x', '__net_faulttree_Node_x', pyxb.binding.datatypes.int)
    __x._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 29, 16)
    __x._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 29, 16)
    
    x = property(__x.value, __x.set, None, None)

    
    # Attribute y uses Python identifier y
    __y = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'y'), 'y', '__net_faulttree_Node_y', pyxb.binding.datatypes.int)
    __y._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 30, 16)
    __y._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 30, 16)
    
    y = property(__y.value, __y.set, None, None)

    _ElementMap.update({
        __children.name() : __children
    })
    _AttributeMap.update({
        __x.name() : __x,
        __y.name() : __y
    })
_module_typeBindings.Node = Node
Namespace.addCategoryObject('typeBinding', 'Node', Node)


# Complex type {net.faulttree}CrispProbability with content type EMPTY
class CrispProbability (Probability):
    """Complex type {net.faulttree}CrispProbability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CrispProbability')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 63, 4)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__net_faulttree_CrispProbability_value', pyxb.binding.datatypes.double, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 66, 16)
    __value._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 66, 16)
    
    value_ = property(__value.value, __value.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __value.name() : __value
    })
_module_typeBindings.CrispProbability = CrispProbability
Namespace.addCategoryObject('typeBinding', 'CrispProbability', CrispProbability)


# Complex type {net.faulttree}FailureRate with content type EMPTY
class FailureRate_ (Probability):
    """Complex type {net.faulttree}FailureRate with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FailureRate')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 72, 4)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__net_faulttree_FailureRate__value', pyxb.binding.datatypes.double, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 75, 16)
    __value._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 75, 16)
    
    value_ = property(__value.value, __value.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __value.name() : __value
    })
_module_typeBindings.FailureRate_ = FailureRate_
Namespace.addCategoryObject('typeBinding', 'FailureRate', FailureRate_)


# Complex type {net.faulttree}ChildNode with content type ELEMENT_ONLY
class ChildNode (Node):
    """Complex type {net.faulttree}ChildNode with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChildNode')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 35, 4)
    _ElementMap = Node._ElementMap.copy()
    _AttributeMap = Node._AttributeMap.copy()
    # Base type is Node
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ChildNode = ChildNode
Namespace.addCategoryObject('typeBinding', 'ChildNode', ChildNode)


# Complex type {net.faulttree}FaultTree with content type ELEMENT_ONLY
class FaultTree_ (Model):
    """Complex type {net.faulttree}FaultTree with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FaultTree')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 42, 4)
    _ElementMap = Model._ElementMap.copy()
    _AttributeMap = Model._AttributeMap.copy()
    # Base type is Model
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element topEvent uses Python identifier topEvent
    __topEvent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'topEvent'), 'topEvent', '__net_faulttree_FaultTree__topEvent', False, pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 46, 20), )

    
    topEvent = property(__topEvent.value, __topEvent.set, None, None)

    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    _ElementMap.update({
        __topEvent.name() : __topEvent
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.FaultTree_ = FaultTree_
Namespace.addCategoryObject('typeBinding', 'FaultTree', FaultTree_)


# Complex type {net.faulttree}TopEvent with content type ELEMENT_ONLY
class TopEvent_ (Node):
    """Complex type {net.faulttree}TopEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TopEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 53, 4)
    _ElementMap = Node._ElementMap.copy()
    _AttributeMap = Node._AttributeMap.copy()
    # Base type is Node
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute missionTime uses Python identifier missionTime
    __missionTime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'missionTime'), 'missionTime', '__net_faulttree_TopEvent__missionTime', pyxb.binding.datatypes.int)
    __missionTime._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 56, 16)
    __missionTime._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 56, 16)
    
    missionTime = property(__missionTime.value, __missionTime.set, None, None)

    
    # Attribute decompositionNumber uses Python identifier decompositionNumber
    __decompositionNumber = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'decompositionNumber'), 'decompositionNumber', '__net_faulttree_TopEvent__decompositionNumber', pyxb.binding.datatypes.int)
    __decompositionNumber._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 57, 16)
    __decompositionNumber._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 57, 16)
    
    decompositionNumber = property(__decompositionNumber.value, __decompositionNumber.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __missionTime.name() : __missionTime,
        __decompositionNumber.name() : __decompositionNumber
    })
_module_typeBindings.TopEvent_ = TopEvent_
Namespace.addCategoryObject('typeBinding', 'TopEvent', TopEvent_)


# Complex type {net.faulttree}Gate with content type ELEMENT_ONLY
class Gate (ChildNode):
    """Complex type {net.faulttree}Gate with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Gate')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 82, 4)
    _ElementMap = ChildNode._ElementMap.copy()
    _AttributeMap = ChildNode._AttributeMap.copy()
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Gate = Gate
Namespace.addCategoryObject('typeBinding', 'Gate', Gate)


# Complex type {net.faulttree}TransferIn with content type ELEMENT_ONLY
class TransferIn_ (ChildNode):
    """Complex type {net.faulttree}TransferIn with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TransferIn')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 119, 4)
    _ElementMap = ChildNode._ElementMap.copy()
    _AttributeMap = ChildNode._AttributeMap.copy()
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute fromModelId uses Python identifier fromModelId
    __fromModelId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'fromModelId'), 'fromModelId', '__net_faulttree_TransferIn__fromModelId', pyxb.binding.datatypes.int, required=True)
    __fromModelId._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 122, 16)
    __fromModelId._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 122, 16)
    
    fromModelId = property(__fromModelId.value, __fromModelId.set, None, None)

    
    # Attribute maxCosts uses Python identifier maxCosts
    __maxCosts = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'maxCosts'), 'maxCosts', '__net_faulttree_TransferIn__maxCosts', pyxb.binding.datatypes.int, unicode_default='0')
    __maxCosts._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 123, 16)
    __maxCosts._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 123, 16)
    
    maxCosts = property(__maxCosts.value, __maxCosts.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __fromModelId.name() : __fromModelId,
        __maxCosts.name() : __maxCosts
    })
_module_typeBindings.TransferIn_ = TransferIn_
Namespace.addCategoryObject('typeBinding', 'TransferIn', TransferIn_)


# Complex type {net.faulttree}UndevelopedEvent with content type ELEMENT_ONLY
class UndevelopedEvent_ (ChildNode):
    """Complex type {net.faulttree}UndevelopedEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UndevelopedEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 129, 4)
    _ElementMap = ChildNode._ElementMap.copy()
    _AttributeMap = ChildNode._AttributeMap.copy()
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.UndevelopedEvent_ = UndevelopedEvent_
Namespace.addCategoryObject('typeBinding', 'UndevelopedEvent', UndevelopedEvent_)


# Complex type {net.faulttree}BasicEvent with content type ELEMENT_ONLY
class BasicEvent_ (ChildNode):
    """Complex type {net.faulttree}BasicEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BasicEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 143, 4)
    _ElementMap = ChildNode._ElementMap.copy()
    _AttributeMap = ChildNode._AttributeMap.copy()
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Element probability uses Python identifier probability
    __probability = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'probability'), 'probability', '__net_faulttree_BasicEvent__probability', False, pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 147, 20), )

    
    probability = property(__probability.value, __probability.set, None, None)

    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        __probability.name() : __probability
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BasicEvent_ = BasicEvent_
Namespace.addCategoryObject('typeBinding', 'BasicEvent', BasicEvent_)


# Complex type {net.faulttree}IntermediateEvent with content type ELEMENT_ONLY
class IntermediateEvent_ (ChildNode):
    """Complex type {net.faulttree}IntermediateEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IntermediateEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 154, 4)
    _ElementMap = ChildNode._ElementMap.copy()
    _AttributeMap = ChildNode._AttributeMap.copy()
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.IntermediateEvent_ = IntermediateEvent_
Namespace.addCategoryObject('typeBinding', 'IntermediateEvent', IntermediateEvent_)


# Complex type {net.faulttree}And with content type ELEMENT_ONLY
class And_ (Gate):
    """Complex type {net.faulttree}And with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'And')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 88, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.And_ = And_
Namespace.addCategoryObject('typeBinding', 'And', And_)


# Complex type {net.faulttree}Or with content type ELEMENT_ONLY
class Or_ (Gate):
    """Complex type {net.faulttree}Or with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Or')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 95, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Or_ = Or_
Namespace.addCategoryObject('typeBinding', 'Or', Or_)


# Complex type {net.faulttree}Xor with content type ELEMENT_ONLY
class Xor_ (Gate):
    """Complex type {net.faulttree}Xor with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Xor')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 102, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Xor_ = Xor_
Namespace.addCategoryObject('typeBinding', 'Xor', Xor_)


# Complex type {net.faulttree}VotingOr with content type ELEMENT_ONLY
class VotingOr_ (Gate):
    """Complex type {net.faulttree}VotingOr with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VotingOr')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 109, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute k uses Python identifier k
    __k = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'k'), 'k', '__net_faulttree_VotingOr__k', pyxb.binding.datatypes.int, required=True)
    __k._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 112, 16)
    __k._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 112, 16)
    
    k = property(__k.value, __k.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __k.name() : __k
    })
_module_typeBindings.VotingOr_ = VotingOr_
Namespace.addCategoryObject('typeBinding', 'VotingOr', VotingOr_)


# Complex type {net.faulttree}HouseEvent with content type ELEMENT_ONLY
class HouseEvent_ (BasicEvent_):
    """Complex type {net.faulttree}HouseEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HouseEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 136, 4)
    _ElementMap = BasicEvent_._ElementMap.copy()
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    # Base type is BasicEvent_
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Element probability (probability) inherited from {net.faulttree}BasicEvent
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.HouseEvent_ = HouseEvent_
Namespace.addCategoryObject('typeBinding', 'HouseEvent', HouseEvent_)


# Complex type {net.faulttree}BasicEventSet with content type ELEMENT_ONLY
class BasicEventSet_ (BasicEvent_):
    """Complex type {net.faulttree}BasicEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BasicEventSet')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 161, 4)
    _ElementMap = BasicEvent_._ElementMap.copy()
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    # Base type is BasicEvent_
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Element probability (probability) inherited from {net.faulttree}BasicEvent
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'quantity'), 'quantity', '__net_faulttree_BasicEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 164, 16)
    __quantity._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 164, 16)
    
    quantity = property(__quantity.value, __quantity.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
_module_typeBindings.BasicEventSet_ = BasicEventSet_
Namespace.addCategoryObject('typeBinding', 'BasicEventSet', BasicEventSet_)


# Complex type {net.faulttree}IntermediateEventSet with content type ELEMENT_ONLY
class IntermediateEventSet_ (IntermediateEvent_):
    """Complex type {net.faulttree}IntermediateEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IntermediateEventSet')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 170, 4)
    _ElementMap = IntermediateEvent_._ElementMap.copy()
    _AttributeMap = IntermediateEvent_._AttributeMap.copy()
    # Base type is IntermediateEvent_
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'quantity'), 'quantity', '__net_faulttree_IntermediateEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 173, 16)
    __quantity._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 173, 16)
    
    quantity = property(__quantity.value, __quantity.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
_module_typeBindings.IntermediateEventSet_ = IntermediateEventSet_
Namespace.addCategoryObject('typeBinding', 'IntermediateEventSet', IntermediateEventSet_)


# Complex type {net.faulttree}DynamicGate with content type ELEMENT_ONLY
class DynamicGate (Gate):
    """Complex type {net.faulttree}DynamicGate with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DynamicGate')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 180, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DynamicGate = DynamicGate
Namespace.addCategoryObject('typeBinding', 'DynamicGate', DynamicGate)


# Complex type {net.faulttree}Spare with content type ELEMENT_ONLY
class Spare_ (DynamicGate):
    """Complex type {net.faulttree}Spare with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Spare')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 190, 4)
    _ElementMap = DynamicGate._ElementMap.copy()
    _AttributeMap = DynamicGate._AttributeMap.copy()
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute primaryID uses Python identifier primaryID
    __primaryID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primaryID'), 'primaryID', '__net_faulttree_Spare__primaryID', pyxb.binding.datatypes.string, required=True)
    __primaryID._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 193, 16)
    __primaryID._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 193, 16)
    
    primaryID = property(__primaryID.value, __primaryID.set, None, None)

    
    # Attribute dormancyFactor uses Python identifier dormancyFactor
    __dormancyFactor = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dormancyFactor'), 'dormancyFactor', '__net_faulttree_Spare__dormancyFactor', pyxb.binding.datatypes.double, required=True)
    __dormancyFactor._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 194, 16)
    __dormancyFactor._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 194, 16)
    
    dormancyFactor = property(__dormancyFactor.value, __dormancyFactor.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primaryID.name() : __primaryID,
        __dormancyFactor.name() : __dormancyFactor
    })
_module_typeBindings.Spare_ = Spare_
Namespace.addCategoryObject('typeBinding', 'Spare', Spare_)


# Complex type {net.faulttree}PriorityAnd with content type ELEMENT_ONLY
class PriorityAnd_ (DynamicGate):
    """Complex type {net.faulttree}PriorityAnd with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PriorityAnd')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 200, 4)
    _ElementMap = DynamicGate._ElementMap.copy()
    _AttributeMap = DynamicGate._AttributeMap.copy()
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute eventSequence uses Python identifier eventSequence
    __eventSequence = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'eventSequence'), 'eventSequence', '__net_faulttree_PriorityAnd__eventSequence', _module_typeBindings.idlist, required=True)
    __eventSequence._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 203, 16)
    __eventSequence._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 203, 16)
    
    eventSequence = property(__eventSequence.value, __eventSequence.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __eventSequence.name() : __eventSequence
    })
_module_typeBindings.PriorityAnd_ = PriorityAnd_
Namespace.addCategoryObject('typeBinding', 'PriorityAnd', PriorityAnd_)


# Complex type {net.faulttree}Sequence with content type ELEMENT_ONLY
class Sequence_ (DynamicGate):
    """Complex type {net.faulttree}Sequence with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Sequence')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 209, 4)
    _ElementMap = DynamicGate._ElementMap.copy()
    _AttributeMap = DynamicGate._AttributeMap.copy()
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute eventSequence uses Python identifier eventSequence
    __eventSequence = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'eventSequence'), 'eventSequence', '__net_faulttree_Sequence__eventSequence', _module_typeBindings.idlist, required=True)
    __eventSequence._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 212, 16)
    __eventSequence._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 212, 16)
    
    eventSequence = property(__eventSequence.value, __eventSequence.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __eventSequence.name() : __eventSequence
    })
_module_typeBindings.Sequence_ = Sequence_
Namespace.addCategoryObject('typeBinding', 'Sequence', Sequence_)


# Complex type {net.faulttree}FDEP with content type ELEMENT_ONLY
class FDEP_ (DynamicGate):
    """Complex type {net.faulttree}FDEP with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FDEP')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 218, 4)
    _ElementMap = DynamicGate._ElementMap.copy()
    _AttributeMap = DynamicGate._AttributeMap.copy()
    # Base type is DynamicGate
    
    # Element annotations (annotations) inherited from {net.faulttree}AnnotatedElement
    
    # Element children (children) inherited from {net.faulttree}Node
    
    # Attribute id inherited from {net.faulttree}AnnotatedElement
    
    # Attribute name inherited from {net.faulttree}AnnotatedElement
    
    # Attribute x inherited from {net.faulttree}Node
    
    # Attribute y inherited from {net.faulttree}Node
    
    # Attribute trigger uses Python identifier trigger
    __trigger = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'trigger'), 'trigger', '__net_faulttree_FDEP__trigger', pyxb.binding.datatypes.string, required=True)
    __trigger._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 221, 16)
    __trigger._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 221, 16)
    
    trigger = property(__trigger.value, __trigger.set, None, None)

    
    # Attribute triggeredEvents uses Python identifier triggeredEvents
    __triggeredEvents = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'triggeredEvents'), 'triggeredEvents', '__net_faulttree_FDEP__triggeredEvents', _module_typeBindings.idlist, required=True)
    __triggeredEvents._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 222, 16)
    __triggeredEvents._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 222, 16)
    
    triggeredEvents = property(__triggeredEvents.value, __triggeredEvents.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __trigger.name() : __trigger,
        __triggeredEvents.name() : __triggeredEvents
    })
_module_typeBindings.FDEP_ = FDEP_
Namespace.addCategoryObject('typeBinding', 'FDEP', FDEP_)


FailureRate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FailureRate'), FailureRate_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 79, 4))
Namespace.addCategoryObject('elementBinding', FailureRate.name().localName(), FailureRate)

FaultTree = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FaultTree'), FaultTree_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 51, 4))
Namespace.addCategoryObject('elementBinding', FaultTree.name().localName(), FaultTree)

TopEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TopEvent'), TopEvent_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 61, 4))
Namespace.addCategoryObject('elementBinding', TopEvent.name().localName(), TopEvent)

TransferIn = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransferIn'), TransferIn_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 127, 4))
Namespace.addCategoryObject('elementBinding', TransferIn.name().localName(), TransferIn)

UndevelopedEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UndevelopedEvent'), UndevelopedEvent_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 134, 4))
Namespace.addCategoryObject('elementBinding', UndevelopedEvent.name().localName(), UndevelopedEvent)

BasicEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BasicEvent'), BasicEvent_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 152, 4))
Namespace.addCategoryObject('elementBinding', BasicEvent.name().localName(), BasicEvent)

IntermediateEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediateEvent'), IntermediateEvent_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 159, 4))
Namespace.addCategoryObject('elementBinding', IntermediateEvent.name().localName(), IntermediateEvent)

And = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'And'), And_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 93, 4))
Namespace.addCategoryObject('elementBinding', And.name().localName(), And)

Or = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Or'), Or_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 100, 4))
Namespace.addCategoryObject('elementBinding', Or.name().localName(), Or)

Xor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Xor'), Xor_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 107, 4))
Namespace.addCategoryObject('elementBinding', Xor.name().localName(), Xor)

VotingOr = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VotingOr'), VotingOr_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 116, 4))
Namespace.addCategoryObject('elementBinding', VotingOr.name().localName(), VotingOr)

HouseEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HouseEvent'), HouseEvent_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 141, 4))
Namespace.addCategoryObject('elementBinding', HouseEvent.name().localName(), HouseEvent)

BasicEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BasicEventSet'), BasicEventSet_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 168, 4))
Namespace.addCategoryObject('elementBinding', BasicEventSet.name().localName(), BasicEventSet)

IntermediateEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediateEventSet'), IntermediateEventSet_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 177, 4))
Namespace.addCategoryObject('elementBinding', IntermediateEventSet.name().localName(), IntermediateEventSet)

Spare = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Spare'), Spare_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 198, 4))
Namespace.addCategoryObject('elementBinding', Spare.name().localName(), Spare)

PriorityAnd = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriorityAnd'), PriorityAnd_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 207, 4))
Namespace.addCategoryObject('elementBinding', PriorityAnd.name().localName(), PriorityAnd)

Sequence = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Sequence'), Sequence_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 216, 4))
Namespace.addCategoryObject('elementBinding', Sequence.name().localName(), Sequence)

FDEP = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FDEP'), FDEP_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 226, 4))
Namespace.addCategoryObject('elementBinding', FDEP.name().localName(), FDEP)



AnnotatedElement._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'annotations'), Annotation, scope=AnnotatedElement, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AnnotatedElement._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AnnotatedElement._Automaton = _BuildAutomaton()




def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Model._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Model._Automaton = _BuildAutomaton_()




Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'children'), ChildNode, scope=Node, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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




FaultTree_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'topEvent'), TopEvent_, scope=FaultTree_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 46, 20)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FaultTree_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FaultTree_._UseForTag(pyxb.namespace.ExpandedName(None, 'topEvent')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 46, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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




BasicEvent_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'probability'), Probability, scope=BasicEvent_, location=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 147, 20)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'probability')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 147, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'probability')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 147, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'probability')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 147, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DynamicGate._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DynamicGate._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Spare_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Spare_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
Spare_._Automaton = _BuildAutomaton_19()




def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PriorityAnd_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(PriorityAnd_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Sequence_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Sequence_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FDEP_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(FDEP_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore-common/xsd/faulttree.xsd', 27, 20))
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

