# FuzzEd/models/xml_fuzztree.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:4e577dc0c998265d17f355c47a293bafde28b966
# Generated 2013-03-08 22:35:07.611505 by PyXB version 1.2.1
# Namespace net.fuzztree [xmlns:ft]

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:0bf039e3-8838-11e2-9f02-58b035ff3a58')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'net.fuzztree', create_if_missing=True)
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


# Complex type {net.fuzztree}AnnotatedElement with content type ELEMENT_ONLY
class AnnotatedElement (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}AnnotatedElement with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnnotatedElement')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 27, 2)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element annotations uses Python identifier annotations
    __annotations = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'annotations'), 'annotations', '__net_fuzztree_AnnotatedElement_annotations', True, pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6), )

    
    annotations = property(__annotations.value, __annotations.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__net_fuzztree_AnnotatedElement_id', pyxb.binding.datatypes.int, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 31, 4)
    __id._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 31, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__net_fuzztree_AnnotatedElement_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 32, 4)
    __name._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 32, 4)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __annotations.name() : __annotations
    }
    _AttributeMap = {
        __id.name() : __id,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'AnnotatedElement', AnnotatedElement)


# Complex type {net.fuzztree}Annotation with content type EMPTY
class Annotation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}Annotation with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Annotation')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 108, 2)
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Annotation', Annotation)


# Complex type {net.fuzztree}Probability with content type EMPTY
class Probability (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {net.fuzztree}Probability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Probability')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 109, 2)
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Probability', Probability)


# Complex type {net.fuzztree}Node with content type ELEMENT_ONLY
class Node (AnnotatedElement):
    """Complex type {net.fuzztree}Node with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 13, 2)
    # Base type is AnnotatedElement
    
    # Element children uses Python identifier children
    __children = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'children'), 'children', '__net_fuzztree_Node_children', True, pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10), )

    
    children = property(__children.value, __children.set, None, None)

    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = AnnotatedElement._ElementMap.copy()
    _ElementMap.update({
        __children.name() : __children
    })
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Node', Node)


# Complex type {net.fuzztree}Model with content type ELEMENT_ONLY
class Model (AnnotatedElement):
    """Complex type {net.fuzztree}Model with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Model')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 22, 2)
    # Base type is AnnotatedElement
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = AnnotatedElement._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AnnotatedElement._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Model', Model)


# Complex type {net.fuzztree}CrispProbability with content type EMPTY
class CrispProbability_ (Probability):
    """Complex type {net.fuzztree}CrispProbability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CrispProbability')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 130, 2)
    # Base type is Probability
    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'value'), 'value_', '__net_fuzztree_CrispProbability__value', pyxb.binding.datatypes.double, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 133, 8)
    __value._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 133, 8)
    
    value_ = property(__value.value, __value.set, None, None)


    _ElementMap = Probability._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Probability._AttributeMap.copy()
    _AttributeMap.update({
        __value.name() : __value
    })
Namespace.addCategoryObject('typeBinding', u'CrispProbability', CrispProbability_)


# Complex type {net.fuzztree}TriangularFuzzyInterval with content type EMPTY
class TriangularFuzzyInterval_ (Probability):
    """Complex type {net.fuzztree}TriangularFuzzyInterval with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TriangularFuzzyInterval')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 138, 2)
    # Base type is Probability
    
    # Attribute a uses Python identifier a
    __a = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'a'), 'a', '__net_fuzztree_TriangularFuzzyInterval__a', pyxb.binding.datatypes.double, required=True)
    __a._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 141, 8)
    __a._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 141, 8)
    
    a = property(__a.value, __a.set, None, None)

    
    # Attribute b1 uses Python identifier b1
    __b1 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'b1'), 'b1', '__net_fuzztree_TriangularFuzzyInterval__b1', pyxb.binding.datatypes.double, required=True)
    __b1._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 142, 8)
    __b1._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 142, 8)
    
    b1 = property(__b1.value, __b1.set, None, None)

    
    # Attribute b2 uses Python identifier b2
    __b2 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'b2'), 'b2', '__net_fuzztree_TriangularFuzzyInterval__b2', pyxb.binding.datatypes.double, required=True)
    __b2._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 143, 8)
    __b2._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 143, 8)
    
    b2 = property(__b2.value, __b2.set, None, None)

    
    # Attribute c uses Python identifier c
    __c = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'c'), 'c', '__net_fuzztree_TriangularFuzzyInterval__c', pyxb.binding.datatypes.double, required=True)
    __c._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 144, 8)
    __c._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 144, 8)
    
    c = property(__c.value, __c.set, None, None)


    _ElementMap = Probability._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Probability._AttributeMap.copy()
    _AttributeMap.update({
        __a.name() : __a,
        __b1.name() : __b1,
        __b2.name() : __b2,
        __c.name() : __c
    })
Namespace.addCategoryObject('typeBinding', u'TriangularFuzzyInterval', TriangularFuzzyInterval_)


# Complex type {net.fuzztree}FuzzTree with content type ELEMENT_ONLY
class FuzzTree_ (Model):
    """Complex type {net.fuzztree}FuzzTree with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FuzzTree')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 3, 2)
    # Base type is Model
    
    # Element topEvent uses Python identifier topEvent
    __topEvent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'topEvent'), 'topEvent', '__net_fuzztree_FuzzTree__topEvent', False, pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 7, 10), )

    
    topEvent = property(__topEvent.value, __topEvent.set, None, None)

    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = Model._ElementMap.copy()
    _ElementMap.update({
        __topEvent.name() : __topEvent
    })
    _AttributeMap = Model._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'FuzzTree', FuzzTree_)


# Complex type {net.fuzztree}SinkNode with content type ELEMENT_ONLY
class SinkNode (Node):
    """Complex type {net.fuzztree}SinkNode with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SinkNode')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 115, 2)
    # Base type is Node
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = Node._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Node._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'SinkNode', SinkNode)


# Complex type {net.fuzztree}ChildNode with content type ELEMENT_ONLY
class ChildNode (Node):
    """Complex type {net.fuzztree}ChildNode with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChildNode')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 120, 2)
    # Base type is Node
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = Node._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Node._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ChildNode', ChildNode)


# Complex type {net.fuzztree}Gate with content type ELEMENT_ONLY
class Gate (ChildNode):
    """Complex type {net.fuzztree}Gate with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Gate')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 34, 2)
    # Base type is ChildNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Gate', Gate)


# Complex type {net.fuzztree}TopEvent with content type ELEMENT_ONLY
class TopEvent_ (SinkNode):
    """Complex type {net.fuzztree}TopEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TopEvent')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 51, 2)
    # Base type is SinkNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = SinkNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = SinkNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TopEvent', TopEvent_)


# Complex type {net.fuzztree}SourceNode with content type ELEMENT_ONLY
class SourceNode (ChildNode):
    """Complex type {net.fuzztree}SourceNode with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SourceNode')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 110, 2)
    # Base type is ChildNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'SourceNode', SourceNode)


# Complex type {net.fuzztree}ConfigurableNode with content type ELEMENT_ONLY
class ConfigurableNode (ChildNode):
    """Complex type {net.fuzztree}ConfigurableNode with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ConfigurableNode')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 125, 2)
    # Base type is ChildNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ConfigurableNode', ConfigurableNode)


# Complex type {net.fuzztree}IntermediateEvent with content type ELEMENT_ONLY
class IntermediateEvent_ (ChildNode):
    """Complex type {net.fuzztree}IntermediateEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IntermediateEvent')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 155, 2)
    # Base type is ChildNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute costs uses Python identifier costs
    __costs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'costs'), 'costs', '__net_fuzztree_IntermediateEvent__costs', pyxb.binding.datatypes.int)
    __costs._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 158, 8)
    __costs._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 158, 8)
    
    costs = property(__costs.value, __costs.set, None, None)

    
    # Attribute optional uses Python identifier optional
    __optional = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'optional'), 'optional', '__net_fuzztree_IntermediateEvent__optional', pyxb.binding.datatypes.boolean)
    __optional._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 159, 8)
    __optional._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 159, 8)
    
    optional = property(__optional.value, __optional.set, None, None)


    _ElementMap = ChildNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ChildNode._AttributeMap.copy()
    _AttributeMap.update({
        __costs.name() : __costs,
        __optional.name() : __optional
    })
Namespace.addCategoryObject('typeBinding', u'IntermediateEvent', IntermediateEvent_)


# Complex type {net.fuzztree}BasicEvent with content type ELEMENT_ONLY
class BasicEvent_ (SourceNode):
    """Complex type {net.fuzztree}BasicEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BasicEvent')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 39, 2)
    # Base type is SourceNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element probability uses Python identifier probability
    __probability = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'probability'), 'probability', '__net_fuzztree_BasicEvent__probability', False, pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 43, 10), )

    
    probability = property(__probability.value, __probability.set, None, None)

    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute optional uses Python identifier optional
    __optional = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'optional'), 'optional', '__net_fuzztree_BasicEvent__optional', pyxb.binding.datatypes.boolean, unicode_default=u'false')
    __optional._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 45, 8)
    __optional._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 45, 8)
    
    optional = property(__optional.value, __optional.set, None, None)

    
    # Attribute costs uses Python identifier costs
    __costs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'costs'), 'costs', '__net_fuzztree_BasicEvent__costs', pyxb.binding.datatypes.int)
    __costs._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 46, 8)
    __costs._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 46, 8)
    
    costs = property(__costs.value, __costs.set, None, None)


    _ElementMap = SourceNode._ElementMap.copy()
    _ElementMap.update({
        __probability.name() : __probability
    })
    _AttributeMap = SourceNode._AttributeMap.copy()
    _AttributeMap.update({
        __optional.name() : __optional,
        __costs.name() : __costs
    })
Namespace.addCategoryObject('typeBinding', u'BasicEvent', BasicEvent_)


# Complex type {net.fuzztree}And with content type ELEMENT_ONLY
class And_ (Gate):
    """Complex type {net.fuzztree}And with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'And')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 57, 2)
    # Base type is Gate
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'And', And_)


# Complex type {net.fuzztree}Or with content type ELEMENT_ONLY
class Or_ (Gate):
    """Complex type {net.fuzztree}Or with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Or')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 63, 2)
    # Base type is Gate
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Or', Or_)


# Complex type {net.fuzztree}Xor with content type ELEMENT_ONLY
class Xor_ (Gate):
    """Complex type {net.fuzztree}Xor with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Xor')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 69, 2)
    # Base type is Gate
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Xor', Xor_)


# Complex type {net.fuzztree}VotingOr with content type ELEMENT_ONLY
class VotingOr_ (Gate):
    """Complex type {net.fuzztree}VotingOr with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VotingOr')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 75, 2)
    # Base type is Gate
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute k uses Python identifier k
    __k = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'k'), 'k', '__net_fuzztree_VotingOr__k', pyxb.binding.datatypes.int, required=True)
    __k._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 78, 8)
    __k._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 78, 8)
    
    k = property(__k.value, __k.set, None, None)


    _ElementMap = Gate._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = Gate._AttributeMap.copy()
    _AttributeMap.update({
        __k.name() : __k
    })
Namespace.addCategoryObject('typeBinding', u'VotingOr', VotingOr_)


# Complex type {net.fuzztree}ChoiceEvent with content type ELEMENT_ONLY
class ChoiceEvent_ (ConfigurableNode):
    """Complex type {net.fuzztree}ChoiceEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChoiceEvent')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 83, 2)
    # Base type is ConfigurableNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = ConfigurableNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ConfigurableNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ChoiceEvent', ChoiceEvent_)


# Complex type {net.fuzztree}RedundancyGate with content type ELEMENT_ONLY
class RedundancyGate_ (ConfigurableNode):
    """Complex type {net.fuzztree}RedundancyGate with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RedundancyGate')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 89, 2)
    # Base type is ConfigurableNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'start'), 'start', '__net_fuzztree_RedundancyGate__start', pyxb.binding.datatypes.int, required=True)
    __start._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 92, 8)
    __start._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 92, 8)
    
    start = property(__start.value, __start.set, None, None)

    
    # Attribute end uses Python identifier end
    __end = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'end'), 'end', '__net_fuzztree_RedundancyGate__end', pyxb.binding.datatypes.int, required=True)
    __end._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 93, 8)
    __end._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 93, 8)
    
    end = property(__end.value, __end.set, None, None)

    
    # Attribute formula uses Python identifier formula
    __formula = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'formula'), 'formula', '__net_fuzztree_RedundancyGate__formula', pyxb.binding.datatypes.string, required=True)
    __formula._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 94, 8)
    __formula._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 94, 8)
    
    formula = property(__formula.value, __formula.set, None, None)

    
    # Attribute costFormula uses Python identifier costFormula
    __costFormula = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'costFormula'), 'costFormula', '__net_fuzztree_RedundancyGate__costFormula', pyxb.binding.datatypes.string)
    __costFormula._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 95, 8)
    __costFormula._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 95, 8)
    
    costFormula = property(__costFormula.value, __costFormula.set, None, None)


    _ElementMap = ConfigurableNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ConfigurableNode._AttributeMap.copy()
    _AttributeMap.update({
        __start.name() : __start,
        __end.name() : __end,
        __formula.name() : __formula,
        __costFormula.name() : __costFormula
    })
Namespace.addCategoryObject('typeBinding', u'RedundancyGate', RedundancyGate_)


# Complex type {net.fuzztree}TransferIn with content type ELEMENT_ONLY
class TransferIn_ (SourceNode):
    """Complex type {net.fuzztree}TransferIn with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TransferIn')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 100, 2)
    # Base type is SourceNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute fromModelId uses Python identifier fromModelId
    __fromModelId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'fromModelId'), 'fromModelId', '__net_fuzztree_TransferIn__fromModelId', pyxb.binding.datatypes.int, required=True)
    __fromModelId._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 103, 8)
    __fromModelId._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 103, 8)
    
    fromModelId = property(__fromModelId.value, __fromModelId.set, None, None)


    _ElementMap = SourceNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = SourceNode._AttributeMap.copy()
    _AttributeMap.update({
        __fromModelId.name() : __fromModelId
    })
Namespace.addCategoryObject('typeBinding', u'TransferIn', TransferIn_)


# Complex type {net.fuzztree}UndevelopedEvent with content type ELEMENT_ONLY
class UndevelopedEvent_ (SourceNode):
    """Complex type {net.fuzztree}UndevelopedEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UndevelopedEvent')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 149, 2)
    # Base type is SourceNode
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement

    _ElementMap = SourceNode._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = SourceNode._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'UndevelopedEvent', UndevelopedEvent_)


# Complex type {net.fuzztree}IntermediateEventSet with content type ELEMENT_ONLY
class IntermediateEventSet_ (IntermediateEvent_):
    """Complex type {net.fuzztree}IntermediateEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IntermediateEventSet')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 178, 2)
    # Base type is IntermediateEvent_
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute costs inherited from {net.fuzztree}IntermediateEvent
    
    # Attribute optional inherited from {net.fuzztree}IntermediateEvent
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quantity'), 'quantity', '__net_fuzztree_IntermediateEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 181, 8)
    __quantity._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 181, 8)
    
    quantity = property(__quantity.value, __quantity.set, None, None)


    _ElementMap = IntermediateEvent_._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = IntermediateEvent_._AttributeMap.copy()
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
Namespace.addCategoryObject('typeBinding', u'IntermediateEventSet', IntermediateEventSet_)


# Complex type {net.fuzztree}BasicEventSet with content type ELEMENT_ONLY
class BasicEventSet_ (BasicEvent_):
    """Complex type {net.fuzztree}BasicEventSet with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BasicEventSet')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 164, 2)
    # Base type is BasicEvent_
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element probability (probability) inherited from {net.fuzztree}BasicEvent
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute optional inherited from {net.fuzztree}BasicEvent
    
    # Attribute costs inherited from {net.fuzztree}BasicEvent
    
    # Attribute quantity uses Python identifier quantity
    __quantity = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quantity'), 'quantity', '__net_fuzztree_BasicEventSet__quantity', pyxb.binding.datatypes.int)
    __quantity._DeclarationLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 167, 8)
    __quantity._UseLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 167, 8)
    
    quantity = property(__quantity.value, __quantity.set, None, None)


    _ElementMap = BasicEvent_._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    _AttributeMap.update({
        __quantity.name() : __quantity
    })
Namespace.addCategoryObject('typeBinding', u'BasicEventSet', BasicEventSet_)


# Complex type {net.fuzztree}HouseEvent with content type ELEMENT_ONLY
class HouseEvent_ (BasicEvent_):
    """Complex type {net.fuzztree}HouseEvent with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HouseEvent')
    _XSDLocation = pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 172, 2)
    # Base type is BasicEvent_
    
    # Element children (children) inherited from {net.fuzztree}Node
    
    # Element annotations (annotations) inherited from {net.fuzztree}AnnotatedElement
    
    # Element probability (probability) inherited from {net.fuzztree}BasicEvent
    
    # Attribute id inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute name inherited from {net.fuzztree}AnnotatedElement
    
    # Attribute optional inherited from {net.fuzztree}BasicEvent
    
    # Attribute costs inherited from {net.fuzztree}BasicEvent

    _ElementMap = BasicEvent_._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BasicEvent_._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'HouseEvent', HouseEvent_)


CrispProbability = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CrispProbability'), CrispProbability_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 137, 2))
Namespace.addCategoryObject('elementBinding', CrispProbability.name().localName(), CrispProbability)

TriangularFuzzyInterval = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TriangularFuzzyInterval'), TriangularFuzzyInterval_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 148, 2))
Namespace.addCategoryObject('elementBinding', TriangularFuzzyInterval.name().localName(), TriangularFuzzyInterval)

FuzzTree = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FuzzTree'), FuzzTree_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 12, 2))
Namespace.addCategoryObject('elementBinding', FuzzTree.name().localName(), FuzzTree)

TopEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TopEvent'), TopEvent_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 56, 2))
Namespace.addCategoryObject('elementBinding', TopEvent.name().localName(), TopEvent)

IntermediateEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IntermediateEvent'), IntermediateEvent_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 163, 2))
Namespace.addCategoryObject('elementBinding', IntermediateEvent.name().localName(), IntermediateEvent)

BasicEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BasicEvent'), BasicEvent_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 50, 2))
Namespace.addCategoryObject('elementBinding', BasicEvent.name().localName(), BasicEvent)

And = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'And'), And_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 62, 2))
Namespace.addCategoryObject('elementBinding', And.name().localName(), And)

Or = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Or'), Or_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 68, 2))
Namespace.addCategoryObject('elementBinding', Or.name().localName(), Or)

Xor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Xor'), Xor_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 74, 2))
Namespace.addCategoryObject('elementBinding', Xor.name().localName(), Xor)

VotingOr = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'VotingOr'), VotingOr_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 82, 2))
Namespace.addCategoryObject('elementBinding', VotingOr.name().localName(), VotingOr)

ChoiceEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ChoiceEvent'), ChoiceEvent_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 88, 2))
Namespace.addCategoryObject('elementBinding', ChoiceEvent.name().localName(), ChoiceEvent)

RedundancyGate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RedundancyGate'), RedundancyGate_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 99, 2))
Namespace.addCategoryObject('elementBinding', RedundancyGate.name().localName(), RedundancyGate)

TransferIn = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TransferIn'), TransferIn_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 107, 2))
Namespace.addCategoryObject('elementBinding', TransferIn.name().localName(), TransferIn)

UndevelopedEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'UndevelopedEvent'), UndevelopedEvent_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 154, 2))
Namespace.addCategoryObject('elementBinding', UndevelopedEvent.name().localName(), UndevelopedEvent)

IntermediateEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IntermediateEventSet'), IntermediateEventSet_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 185, 2))
Namespace.addCategoryObject('elementBinding', IntermediateEventSet.name().localName(), IntermediateEventSet)

BasicEventSet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BasicEventSet'), BasicEventSet_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 171, 2))
Namespace.addCategoryObject('elementBinding', BasicEventSet.name().localName(), BasicEventSet)

HouseEvent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'HouseEvent'), HouseEvent_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 177, 2))
Namespace.addCategoryObject('elementBinding', HouseEvent.name().localName(), HouseEvent)



AnnotatedElement._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'annotations'), Annotation, scope=AnnotatedElement, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AnnotatedElement._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AnnotatedElement._Automaton = _BuildAutomaton()




Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'children'), ChildNode, scope=Node, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Node._Automaton = _BuildAutomaton_()




def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Model._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Model._Automaton = _BuildAutomaton_2()




FuzzTree_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'topEvent'), TopEvent_, scope=FuzzTree_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 7, 10)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FuzzTree_._UseForTag(pyxb.namespace.ExpandedName(None, u'topEvent')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 7, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FuzzTree_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FuzzTree_._Automaton = _BuildAutomaton_3()




def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SinkNode._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(SinkNode._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SinkNode._Automaton = _BuildAutomaton_4()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ChildNode._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ChildNode._Automaton = _BuildAutomaton_5()




def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Gate._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
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
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TopEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
TopEvent_._Automaton = _BuildAutomaton_7()




def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SourceNode._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(SourceNode._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SourceNode._Automaton = _BuildAutomaton_8()




def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ConfigurableNode._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ConfigurableNode._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ConfigurableNode._Automaton = _BuildAutomaton_9()




def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
IntermediateEvent_._Automaton = _BuildAutomaton_10()




BasicEvent_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'probability'), Probability, scope=BasicEvent_, location=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 43, 10)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'probability')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 43, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BasicEvent_._Automaton = _BuildAutomaton_11()




def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(And_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
And_._Automaton = _BuildAutomaton_12()




def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Or_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Or_._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Xor_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Xor_._Automaton = _BuildAutomaton_14()




def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(VotingOr_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
VotingOr_._Automaton = _BuildAutomaton_15()




def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ChoiceEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ChoiceEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ChoiceEvent_._Automaton = _BuildAutomaton_16()




def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(RedundancyGate_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(RedundancyGate_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
RedundancyGate_._Automaton = _BuildAutomaton_17()




def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TransferIn_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
TransferIn_._Automaton = _BuildAutomaton_18()




def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(UndevelopedEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
UndevelopedEvent_._Automaton = _BuildAutomaton_19()




def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(IntermediateEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
IntermediateEventSet_._Automaton = _BuildAutomaton_20()




def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicEventSet_._UseForTag(pyxb.namespace.ExpandedName(None, u'probability')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 43, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BasicEventSet_._Automaton = _BuildAutomaton_21()




def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'children')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 17, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'annotations')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 29, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(HouseEvent_._UseForTag(pyxb.namespace.ExpandedName(None, u'probability')), pyxb.utils.utility.Location(u'/Users/troeger/svn/fuzztrees/FuzzEd/static/xsd/fuzztree.xsd', 43, 10))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
HouseEvent_._Automaton = _BuildAutomaton_22()

