# front/FuzzEd/models/xml_fuzztree.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:4e577dc0c998265d17f355c47a293bafde28b966
# Generated 2018-03-16 08:24:57.477008 by PyXB version 1.2.6 using Python 3.5.2.final.0
# Namespace net.fuzztree

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:82da2a40-28f3-11e8-adbc-0242ac110002')

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
Namespace = pyxb.namespace.NamespaceForURI('net.fuzztree', create_if_missing=True)
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


# Complex type {net.fuzztree}Annotation with content type EMPTY
class Annotation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}Annotation with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Annotation')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 5, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Annotation = Annotation
Namespace.addCategoryObject('typeBinding', 'Annotation', Annotation)


# Complex type {net.fuzztree}Probability with content type EMPTY
class Probability (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}Probability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Probability')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 6, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Probability = Probability
Namespace.addCategoryObject('typeBinding', 'Probability', Probability)


# Complex type {net.fuzztree}AnnotatedElement with content type ELEMENT_ONLY
class AnnotatedElement (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}AnnotatedElement with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnnotatedElement')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 8, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element annotations uses Python identifier annotations
    __annotations = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'annotations'), 'annotations', '__net_fuzztree_AnnotatedElement_annotations', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12), )

    
    annotations = property(__annotations.value, __annotations.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__net_fuzztree_AnnotatedElement_id', pyxb.binding.datatypes.string, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 12, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 12, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__net_fuzztree_AnnotatedElement_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 13, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 13, 8)
    
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


# Complex type {net.fuzztree}DoubleToIntervalMap with content type ELEMENT_ONLY
class DoubleToIntervalMap_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}DoubleToIntervalMap with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DoubleToIntervalMap')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 236, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element value uses Python identifier value_
    __value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__net_fuzztree_DoubleToIntervalMap__value', False, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 238, 12), )

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute key uses Python identifier key
    __key = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'key'), 'key', '__net_fuzztree_DoubleToIntervalMap__key', pyxb.binding.datatypes.double, required=True)
    __key._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 240, 8)
    __key._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 240, 8)
    
    key = property(__key.value, __key.set, None, None)

    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap.update({
        __key.name() : __key
    })
_module_typeBindings.DoubleToIntervalMap_ = DoubleToIntervalMap_
Namespace.addCategoryObject('typeBinding', 'DoubleToIntervalMap', DoubleToIntervalMap_)


# Complex type {net.fuzztree}Interval with content type EMPTY
class Interval_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}Interval with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Interval')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 244, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute lowerBound uses Python identifier lowerBound
    __lowerBound = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lowerBound'), 'lowerBound', '__net_fuzztree_Interval__lowerBound', pyxb.binding.datatypes.double, required=True)
    __lowerBound._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 245, 8)
    __lowerBound._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 245, 8)
    
    lowerBound = property(__lowerBound.value, __lowerBound.set, None, None)

    
    # Attribute upperBound uses Python identifier upperBound
    __upperBound = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'upperBound'), 'upperBound', '__net_fuzztree_Interval__upperBound', pyxb.binding.datatypes.double, required=True)
    __upperBound._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 246, 8)
    __upperBound._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 246, 8)
    
    upperBound = property(__upperBound.value, __upperBound.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lowerBound.name() : __lowerBound,
        __upperBound.name() : __upperBound
    })
_module_typeBindings.Interval_ = Interval_
Namespace.addCategoryObject('typeBinding', 'Interval', Interval_)


# Complex type {net.fuzztree}Model with content type ELEMENT_ONLY
class Model (AnnotatedElement):
    """Complex type {net.fuzztree}Model with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Model')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 16, 4)
    _ElementMap = AnnotatedElement._ElementMap.copy()
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    # Base type is AnnotatedElement
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Model = Model
Namespace.addCategoryObject('typeBinding', 'Model', Model)


# Complex type {net.fuzztree}Node with content type ELEMENT_ONLY
class Node (AnnotatedElement):
    """Complex type {net.fuzztree}Node with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Node')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 23, 4)
    _ElementMap = AnnotatedElement._ElementMap.copy()
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    # Base type is AnnotatedElement
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children uses Python identifier children
    __children = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'children'), 'children', '__net_fuzztree_Node_children', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20), )

    
    children = property(__children.value, __children.set, None, None)

    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x uses Python identifier x
    __x = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'x'), 'x', '__net_fuzztree_Node_x', pyxb.binding.datatypes.int)
    __x._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 29, 16)
    __x._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 29, 16)
    
    x = property(__x.value, __x.set, None, None)

    
    # Attribute y uses Python identifier y
    __y = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'y'), 'y', '__net_fuzztree_Node_y', pyxb.binding.datatypes.int)
    __y._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 30, 16)
    __y._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 30, 16)
    
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


# Complex type {net.fuzztree}CrispProbability with content type EMPTY
class CrispProbability (Probability):
    """Complex type {net.fuzztree}CrispProbability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CrispProbability')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 63, 4)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__net_fuzztree_CrispProbability_value', pyxb.binding.datatypes.double, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 66, 16)
    __value._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 66, 16)
    
    value_ = property(__value.value, __value.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __value.name() : __value
    })
_module_typeBindings.CrispProbability = CrispProbability
Namespace.addCategoryObject('typeBinding', 'CrispProbability', CrispProbability)


# Complex type {net.fuzztree}FailureRate with content type EMPTY
class FailureRate_ (Probability):
    """Complex type {net.fuzztree}FailureRate with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FailureRate')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 72, 4)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__net_fuzztree_FailureRate__value', pyxb.binding.datatypes.double, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 75, 16)
    __value._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 75, 16)
    
    value_ = property(__value.value, __value.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __value.name() : __value
    })
_module_typeBindings.FailureRate_ = FailureRate_
Namespace.addCategoryObject('typeBinding', 'FailureRate', FailureRate_)


# Complex type {net.fuzztree}TriangularFuzzyInterval with content type EMPTY
class TriangularFuzzyInterval_ (Probability):
    """Complex type {net.fuzztree}TriangularFuzzyInterval with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TriangularFuzzyInterval')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 204, 4)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Attribute a uses Python identifier a
    __a = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'a'), 'a', '__net_fuzztree_TriangularFuzzyInterval__a', pyxb.binding.datatypes.double, required=True)
    __a._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 207, 16)
    __a._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 207, 16)
    
    a = property(__a.value, __a.set, None, None)

    
    # Attribute b1 uses Python identifier b1
    __b1 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'b1'), 'b1', '__net_fuzztree_TriangularFuzzyInterval__b1', pyxb.binding.datatypes.double, required=True)
    __b1._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 208, 16)
    __b1._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 208, 16)
    
    b1 = property(__b1.value, __b1.set, None, None)

    
    # Attribute b2 uses Python identifier b2
    __b2 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'b2'), 'b2', '__net_fuzztree_TriangularFuzzyInterval__b2', pyxb.binding.datatypes.double, required=True)
    __b2._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 209, 16)
    __b2._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 209, 16)
    
    b2 = property(__b2.value, __b2.set, None, None)

    
    # Attribute c uses Python identifier c
    __c = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'c'), 'c', '__net_fuzztree_TriangularFuzzyInterval__c', pyxb.binding.datatypes.double, required=True)
    __c._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 210, 16)
    __c._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 210, 16)
    
    c = property(__c.value, __c.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __a.name() : __a,
        __b1.name() : __b1,
        __b2.name() : __b2,
        __c.name() : __c
    })
_module_typeBindings.TriangularFuzzyInterval_ = TriangularFuzzyInterval_
Namespace.addCategoryObject('typeBinding', 'TriangularFuzzyInterval', TriangularFuzzyInterval_)


# Complex type {net.fuzztree}DecomposedFuzzyProbability with content type ELEMENT_ONLY
class DecomposedFuzzyProbability_ (Probability):
    """Complex type {net.fuzztree}DecomposedFuzzyProbability with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DecomposedFuzzyProbability')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 225, 4)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Element alphaCuts uses Python identifier alphaCuts
    __alphaCuts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'alphaCuts'), 'alphaCuts', '__net_fuzztree_DecomposedFuzzyProbability__alphaCuts', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 229, 20), )

    
    alphaCuts = property(__alphaCuts.value, __alphaCuts.set, None, None)

    _ElementMap.update({
        __alphaCuts.name() : __alphaCuts
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DecomposedFuzzyProbability_ = DecomposedFuzzyProbability_
Namespace.addCategoryObject('typeBinding', 'DecomposedFuzzyProbability', DecomposedFuzzyProbability_)


# Complex type {net.fuzztree}ChildNode with content type ELEMENT_ONLY
class ChildNode (Node):
    """Complex type {net.fuzztree}ChildNode with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChildNode')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 35, 4)
    _ElementMap = Node._ElementMap.copy()
    _AttributeMap = Node._AttributeMap.copy()
    # Base type is Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ChildNode = ChildNode
Namespace.addCategoryObject('typeBinding', 'ChildNode', ChildNode)


# Complex type {net.fuzztree}FuzzTree with content type ELEMENT_ONLY
class FuzzTree_ (Model):
    """Complex type {net.fuzztree}FuzzTree with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FuzzTree')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 42, 4)
    _ElementMap = Model._ElementMap.copy()
    _AttributeMap = Model._AttributeMap.copy()
    # Base type is Model
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element topEvent uses Python identifier topEvent
    __topEvent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'topEvent'), 'topEvent', '__net_fuzztree_FuzzTree__topEvent', False, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 46, 20), )

    
    topEvent = property(__topEvent.value, __topEvent.set, None, None)

    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    _ElementMap.update({
        __topEvent.name() : __topEvent
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.FuzzTree_ = FuzzTree_
Namespace.addCategoryObject('typeBinding', 'FuzzTree', FuzzTree_)


# Complex type {net.fuzztree}TopEvent with content type ELEMENT_ONLY
class TopEvent_ (Node):
    """Complex type {net.fuzztree}TopEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TopEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 53, 4)
    _ElementMap = Node._ElementMap.copy()
    _AttributeMap = Node._AttributeMap.copy()
    # Base type is Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute missionTime uses Python identifier missionTime
    __missionTime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'missionTime'), 'missionTime', '__net_fuzztree_TopEvent__missionTime', pyxb.binding.datatypes.int)
    __missionTime._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 56, 16)
    __missionTime._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 56, 16)
    
    missionTime = property(__missionTime.value, __missionTime.set, None, None)

    
    # Attribute decompositionNumber uses Python identifier decompositionNumber
    __decompositionNumber = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'decompositionNumber'), 'decompositionNumber', '__net_fuzztree_TopEvent__decompositionNumber', pyxb.binding.datatypes.int)
    __decompositionNumber._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 57, 16)
    __decompositionNumber._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 57, 16)
    
    decompositionNumber = property(__decompositionNumber.value, __decompositionNumber.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __missionTime.name() : __missionTime,
        __decompositionNumber.name() : __decompositionNumber
    })
_module_typeBindings.TopEvent_ = TopEvent_
Namespace.addCategoryObject('typeBinding', 'TopEvent', TopEvent_)


# Complex type {net.fuzztree}Gate with content type ELEMENT_ONLY
class Gate (ChildNode):
    """Complex type {net.fuzztree}Gate with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Gate')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 82, 4)
    _ElementMap = ChildNode._ElementMap.copy()
    _AttributeMap = ChildNode._AttributeMap.copy()
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Gate = Gate
Namespace.addCategoryObject('typeBinding', 'Gate', Gate)


# Complex type {net.fuzztree}VariationPoint with content type ELEMENT_ONLY
class VariationPoint (ChildNode):
    """Complex type {net.fuzztree}VariationPoint with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VariationPoint')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 198, 4)
    _ElementMap = ChildNode._ElementMap.copy()
    _AttributeMap = ChildNode._AttributeMap.copy()
    # Base type is ChildNode
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.VariationPoint = VariationPoint
Namespace.addCategoryObject('typeBinding', 'VariationPoint', VariationPoint)


# Complex type {net.fuzztree}And with content type ELEMENT_ONLY
class And_ (Gate):
    """Complex type {net.fuzztree}And with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'And')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 88, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.And_ = And_
Namespace.addCategoryObject('typeBinding', 'And', And_)


# Complex type {net.fuzztree}Or with content type ELEMENT_ONLY
class Or_ (Gate):
    """Complex type {net.fuzztree}Or with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Or')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 95, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Or_ = Or_
Namespace.addCategoryObject('typeBinding', 'Or', Or_)


# Complex type {net.fuzztree}Xor with content type ELEMENT_ONLY
class Xor_ (Gate):
    """Complex type {net.fuzztree}Xor with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Xor')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 102, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Xor_ = Xor_
Namespace.addCategoryObject('typeBinding', 'Xor', Xor_)


# Complex type {net.fuzztree}VotingOr with content type ELEMENT_ONLY
class VotingOr_ (Gate):
    """Complex type {net.fuzztree}VotingOr with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VotingOr')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 109, 4)
    _ElementMap = Gate._ElementMap.copy()
    _AttributeMap = Gate._AttributeMap.copy()
    # Base type is Gate
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute k uses Python identifier k
    __k = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'k'), 'k', '__net_fuzztree_VotingOr__k', pyxb.binding.datatypes.int, required=True)
    __k._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 112, 16)
    __k._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 112, 16)
    
    k = property(__k.value, __k.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __k.name() : __k
    })
_module_typeBindings.VotingOr_ = VotingOr_
Namespace.addCategoryObject('typeBinding', 'VotingOr', VotingOr_)


# Complex type {net.fuzztree}TransferIn with content type ELEMENT_ONLY
class TransferIn_ (VariationPoint):
    """Complex type {net.fuzztree}TransferIn with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TransferIn')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 119, 4)
    _ElementMap = VariationPoint._ElementMap.copy()
    _AttributeMap = VariationPoint._AttributeMap.copy()
    # Base type is VariationPoint
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute fromModelId uses Python identifier fromModelId
    __fromModelId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'fromModelId'), 'fromModelId', '__net_fuzztree_TransferIn__fromModelId', pyxb.binding.datatypes.int, required=True)
    __fromModelId._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 122, 16)
    __fromModelId._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 122, 16)
    
    fromModelId = property(__fromModelId.value, __fromModelId.set, None, None)

    
    # Attribute maxCosts uses Python identifier maxCosts
    __maxCosts = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'maxCosts'), 'maxCosts', '__net_fuzztree_TransferIn__maxCosts', pyxb.binding.datatypes.int, unicode_default='0')
    __maxCosts._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 123, 16)
    __maxCosts._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 123, 16)
    
    maxCosts = property(__maxCosts.value, __maxCosts.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __fromModelId.name() : __fromModelId,
        __maxCosts.name() : __maxCosts
    })
_module_typeBindings.TransferIn_ = TransferIn_
Namespace.addCategoryObject('typeBinding', 'TransferIn', TransferIn_)


# Complex type {net.fuzztree}FeatureVariationPoint with content type ELEMENT_ONLY
class FeatureVariationPoint_ (VariationPoint):
    """Complex type {net.fuzztree}FeatureVariationPoint with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FeatureVariationPoint')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 181, 4)
    _ElementMap = VariationPoint._ElementMap.copy()
    _AttributeMap = VariationPoint._AttributeMap.copy()
    # Base type is VariationPoint
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.FeatureVariationPoint_ = FeatureVariationPoint_
Namespace.addCategoryObject('typeBinding', 'FeatureVariationPoint', FeatureVariationPoint_)


# Complex type {net.fuzztree}RedundancyVariationPoint with content type ELEMENT_ONLY
class RedundancyVariationPoint_ (VariationPoint):
    """Complex type {net.fuzztree}RedundancyVariationPoint with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RedundancyVariationPoint')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 187, 4)
    _ElementMap = VariationPoint._ElementMap.copy()
    _AttributeMap = VariationPoint._AttributeMap.copy()
    # Base type is VariationPoint
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'start'), 'start', '__net_fuzztree_RedundancyVariationPoint__start', pyxb.binding.datatypes.int, required=True)
    __start._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 190, 16)
    __start._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 190, 16)
    
    start = property(__start.value, __start.set, None, None)

    
    # Attribute end uses Python identifier end
    __end = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'end'), 'end', '__net_fuzztree_RedundancyVariationPoint__end', pyxb.binding.datatypes.int, required=True)
    __end._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 191, 16)
    __end._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 191, 16)
    
    end = property(__end.value, __end.set, None, None)

    
    # Attribute formula uses Python identifier formula
    __formula = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formula'), 'formula', '__net_fuzztree_RedundancyVariationPoint__formula', pyxb.binding.datatypes.string, required=True)
    __formula._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 192, 16)
    __formula._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 192, 16)
    
    formula = property(__formula.value, __formula.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __start.name() : __start,
        __end.name() : __end,
        __formula.name() : __formula
    })
_module_typeBindings.RedundancyVariationPoint_ = RedundancyVariationPoint_
Namespace.addCategoryObject('typeBinding', 'RedundancyVariationPoint', RedundancyVariationPoint_)


# Complex type {net.fuzztree}InclusionVariationPoint with content type ELEMENT_ONLY
class InclusionVariationPoint (VariationPoint):
    """Complex type {net.fuzztree}InclusionVariationPoint with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'InclusionVariationPoint')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 216, 4)
    _ElementMap = VariationPoint._ElementMap.copy()
    _AttributeMap = VariationPoint._AttributeMap.copy()
    # Base type is VariationPoint
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute optional uses Python identifier optional
    __optional = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'optional'), 'optional', '__net_fuzztree_InclusionVariationPoint_optional', pyxb.binding.datatypes.boolean, unicode_default='false')
    __optional._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 219, 16)
    __optional._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 219, 16)
    
    optional = property(__optional.value, __optional.set, None, None)

    
    # Attribute costs uses Python identifier costs
    __costs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'costs'), 'costs', '__net_fuzztree_InclusionVariationPoint_costs', pyxb.binding.datatypes.int)
    __costs._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 220, 16)
    __costs._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 220, 16)
    
    costs = property(__costs.value, __costs.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __optional.name() : __optional,
        __costs.name() : __costs
    })
_module_typeBindings.InclusionVariationPoint = InclusionVariationPoint
Namespace.addCategoryObject('typeBinding', 'InclusionVariationPoint', InclusionVariationPoint)


# Complex type {net.fuzztree}UndevelopedEvent with content type ELEMENT_ONLY
class UndevelopedEvent_ (InclusionVariationPoint):
    """Complex type {net.fuzztree}UndevelopedEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UndevelopedEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 129, 4)
    _ElementMap = InclusionVariationPoint._ElementMap.copy()
    _AttributeMap = InclusionVariationPoint._AttributeMap.copy()
    # Base type is InclusionVariationPoint
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute optional inherited from {net.fuzztree}InclusionVariationPoint
    
    # Attribute costs inherited from {net.fuzztree}InclusionVariationPoint
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.UndevelopedEvent_ = UndevelopedEvent_
Namespace.addCategoryObject('typeBinding', 'UndevelopedEvent', UndevelopedEvent_)


# Complex type {net.fuzztree}BasicEvent with content type ELEMENT_ONLY
class BasicEvent_ (InclusionVariationPoint):
    """Complex type {net.fuzztree}BasicEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BasicEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 143, 4)
    _ElementMap = InclusionVariationPoint._ElementMap.copy()
    _AttributeMap = InclusionVariationPoint._AttributeMap.copy()
    # Base type is InclusionVariationPoint
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element probability uses Python identifier probability
    __probability = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'probability'), 'probability', '__net_fuzztree_BasicEvent__probability', False, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 147, 20), )

    
    probability = property(__probability.value, __probability.set, None, None)

    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute optional inherited from {net.fuzztree}InclusionVariationPoint
    
    # Attribute costs inherited from {net.fuzztree}InclusionVariationPoint
    _ElementMap.update({
        __probability.name() : __probability
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.BasicEvent_ = BasicEvent_
Namespace.addCategoryObject('typeBinding', 'BasicEvent', BasicEvent_)


# Complex type {net.fuzztree}IntermediateEvent with content type ELEMENT_ONLY
class IntermediateEvent_ (InclusionVariationPoint):
    """Complex type {net.fuzztree}IntermediateEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IntermediateEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 154, 4)
    _ElementMap = InclusionVariationPoint._ElementMap.copy()
    _AttributeMap = InclusionVariationPoint._AttributeMap.copy()
    # Base type is InclusionVariationPoint
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute optional inherited from {net.fuzztree}InclusionVariationPoint
    
    # Attribute costs inherited from {net.fuzztree}InclusionVariationPoint
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.IntermediateEvent_ = IntermediateEvent_
Namespace.addCategoryObject('typeBinding', 'IntermediateEvent', IntermediateEvent_)


# Complex type {net.fuzztree}HouseEvent with content type ELEMENT_ONLY
class HouseEvent_ (BasicEvent_):
    """Complex type {net.fuzztree}HouseEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HouseEvent')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 136, 4)
    _ElementMap = BasicEvent_._ElementMap.copy()
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    # Base type is BasicEvent_
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element probability (probability) inherited from {net.fuzztree}BasicEvent
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute optional inherited from {net.fuzztree}InclusionVariationPoint
    
    # Attribute costs inherited from {net.fuzztree}InclusionVariationPoint
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.HouseEvent_ = HouseEvent_
Namespace.addCategoryObject('typeBinding', 'HouseEvent', HouseEvent_)


# Complex type {net.fuzztree}BasicEventSet with content type ELEMENT_ONLY
class BasicEventSet_ (BasicEvent_):
    """Complex type {net.fuzztree}BasicEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BasicEventSet')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 161, 4)
    _ElementMap = BasicEvent_._ElementMap.copy()
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    # Base type is BasicEvent_
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element probability (probability) inherited from {net.fuzztree}BasicEvent
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'quantity'), 'quantity', '__net_fuzztree_BasicEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 164, 16)
    __quantity._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 164, 16)
    
    quantity = property(__quantity.value, __quantity.set, None, None)

    
    # Attribute optional inherited from {net.fuzztree}InclusionVariationPoint
    
    # Attribute costs inherited from {net.fuzztree}InclusionVariationPoint
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
_module_typeBindings.BasicEventSet_ = BasicEventSet_
Namespace.addCategoryObject('typeBinding', 'BasicEventSet', BasicEventSet_)


# Complex type {net.fuzztree}IntermediateEventSet with content type ELEMENT_ONLY
class IntermediateEventSet_ (IntermediateEvent_):
    """Complex type {net.fuzztree}IntermediateEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IntermediateEventSet')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 170, 4)
    _ElementMap = IntermediateEvent_._ElementMap.copy()
    _AttributeMap = IntermediateEvent_._AttributeMap.copy()
    # Base type is IntermediateEvent_
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute x inherited from {net.fuzztree}Node
    
    # Attribute y inherited from {net.fuzztree}Node
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'quantity'), 'quantity', '__net_fuzztree_IntermediateEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 173, 16)
    __quantity._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 173, 16)
    
    quantity = property(__quantity.value, __quantity.set, None, None)

    
    # Attribute optional inherited from {net.fuzztree}InclusionVariationPoint
    
    # Attribute costs inherited from {net.fuzztree}InclusionVariationPoint
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
_module_typeBindings.IntermediateEventSet_ = IntermediateEventSet_
Namespace.addCategoryObject('typeBinding', 'IntermediateEventSet', IntermediateEventSet_)


DoubleToIntervalMap = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DoubleToIntervalMap'), DoubleToIntervalMap_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 242, 4))
Namespace.addCategoryObject('elementBinding', DoubleToIntervalMap.name().localName(), DoubleToIntervalMap)

Interval = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Interval'), Interval_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 248, 4))
Namespace.addCategoryObject('elementBinding', Interval.name().localName(), Interval)

FailureRate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FailureRate'), FailureRate_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 79, 4))
Namespace.addCategoryObject('elementBinding', FailureRate.name().localName(), FailureRate)

TriangularFuzzyInterval = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TriangularFuzzyInterval'), TriangularFuzzyInterval_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 214, 4))
Namespace.addCategoryObject('elementBinding', TriangularFuzzyInterval.name().localName(), TriangularFuzzyInterval)

DecomposedFuzzyProbability = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DecomposedFuzzyProbability'), DecomposedFuzzyProbability_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 234, 4))
Namespace.addCategoryObject('elementBinding', DecomposedFuzzyProbability.name().localName(), DecomposedFuzzyProbability)

FuzzTree = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FuzzTree'), FuzzTree_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 51, 4))
Namespace.addCategoryObject('elementBinding', FuzzTree.name().localName(), FuzzTree)

TopEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TopEvent'), TopEvent_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 61, 4))
Namespace.addCategoryObject('elementBinding', TopEvent.name().localName(), TopEvent)

And = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'And'), And_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 93, 4))
Namespace.addCategoryObject('elementBinding', And.name().localName(), And)

Or = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Or'), Or_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 100, 4))
Namespace.addCategoryObject('elementBinding', Or.name().localName(), Or)

Xor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Xor'), Xor_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 107, 4))
Namespace.addCategoryObject('elementBinding', Xor.name().localName(), Xor)

VotingOr = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VotingOr'), VotingOr_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 116, 4))
Namespace.addCategoryObject('elementBinding', VotingOr.name().localName(), VotingOr)

TransferIn = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransferIn'), TransferIn_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 127, 4))
Namespace.addCategoryObject('elementBinding', TransferIn.name().localName(), TransferIn)

FeatureVariationPoint = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FeatureVariationPoint'), FeatureVariationPoint_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 186, 4))
Namespace.addCategoryObject('elementBinding', FeatureVariationPoint.name().localName(), FeatureVariationPoint)

RedundancyVariationPoint = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RedundancyVariationPoint'), RedundancyVariationPoint_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 196, 4))
Namespace.addCategoryObject('elementBinding', RedundancyVariationPoint.name().localName(), RedundancyVariationPoint)

UndevelopedEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UndevelopedEvent'), UndevelopedEvent_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 134, 4))
Namespace.addCategoryObject('elementBinding', UndevelopedEvent.name().localName(), UndevelopedEvent)

BasicEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BasicEvent'), BasicEvent_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 152, 4))
Namespace.addCategoryObject('elementBinding', BasicEvent.name().localName(), BasicEvent)

IntermediateEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediateEvent'), IntermediateEvent_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 159, 4))
Namespace.addCategoryObject('elementBinding', IntermediateEvent.name().localName(), IntermediateEvent)

HouseEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HouseEvent'), HouseEvent_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 141, 4))
Namespace.addCategoryObject('elementBinding', HouseEvent.name().localName(), HouseEvent)

BasicEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BasicEventSet'), BasicEventSet_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 168, 4))
Namespace.addCategoryObject('elementBinding', BasicEventSet.name().localName(), BasicEventSet)

IntermediateEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntermediateEventSet'), IntermediateEventSet_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 177, 4))
Namespace.addCategoryObject('elementBinding', IntermediateEventSet.name().localName(), IntermediateEventSet)



AnnotatedElement._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'annotations'), Annotation, scope=AnnotatedElement, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AnnotatedElement._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AnnotatedElement._Automaton = _BuildAutomaton()




DoubleToIntervalMap_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'value'), Interval_, scope=DoubleToIntervalMap_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 238, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DoubleToIntervalMap_._UseForTag(pyxb.namespace.ExpandedName(None, 'value')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 238, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DoubleToIntervalMap_._Automaton = _BuildAutomaton_()




def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Model._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Model._Automaton = _BuildAutomaton_2()




Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'children'), ChildNode, scope=Node, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
Node._Automaton = _BuildAutomaton_3()




DecomposedFuzzyProbability_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'alphaCuts'), DoubleToIntervalMap_, scope=DecomposedFuzzyProbability_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 229, 20)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 229, 20))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DecomposedFuzzyProbability_._UseForTag(pyxb.namespace.ExpandedName(None, 'alphaCuts')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 229, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DecomposedFuzzyProbability_._Automaton = _BuildAutomaton_4()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
ChildNode._Automaton = _BuildAutomaton_5()




FuzzTree_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'topEvent'), TopEvent_, scope=FuzzTree_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 46, 20)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FuzzTree_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FuzzTree_._UseForTag(pyxb.namespace.ExpandedName(None, 'topEvent')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 46, 20))
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
FuzzTree_._Automaton = _BuildAutomaton_6()




def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
TopEvent_._Automaton = _BuildAutomaton_7()




def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
Gate._Automaton = _BuildAutomaton_8()




def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VariationPoint._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(VariationPoint._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
VariationPoint._Automaton = _BuildAutomaton_9()




def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
And_._Automaton = _BuildAutomaton_10()




def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
Or_._Automaton = _BuildAutomaton_11()




def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
Xor_._Automaton = _BuildAutomaton_12()




def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
VotingOr_._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
TransferIn_._Automaton = _BuildAutomaton_14()




def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FeatureVariationPoint_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(FeatureVariationPoint_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
FeatureVariationPoint_._Automaton = _BuildAutomaton_15()




def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(RedundancyVariationPoint_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(RedundancyVariationPoint_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
RedundancyVariationPoint_._Automaton = _BuildAutomaton_16()




def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(InclusionVariationPoint._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(InclusionVariationPoint._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
InclusionVariationPoint._Automaton = _BuildAutomaton_17()




def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
UndevelopedEvent_._Automaton = _BuildAutomaton_18()




BasicEvent_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'probability'), Probability, scope=BasicEvent_, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 147, 20)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'probability')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 147, 20))
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
BasicEvent_._Automaton = _BuildAutomaton_19()




def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
IntermediateEvent_._Automaton = _BuildAutomaton_20()




def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, 'probability')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 147, 20))
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
HouseEvent_._Automaton = _BuildAutomaton_21()




def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'probability')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 147, 20))
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
BasicEventSet_._Automaton = _BuildAutomaton_22()




def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'annotations')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 10, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, 'children')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/fuzztree.xsd', 27, 20))
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
IntermediateEventSet_._Automaton = _BuildAutomaton_23()

