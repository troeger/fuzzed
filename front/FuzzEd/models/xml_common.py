# FuzzEd/models/xml_common.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:048f94face6649912cf7a695fb6b859022492725
# Generated 2018-03-07 21:34:38.162952 by PyXB version 1.2.6 using Python 2.7.12.final.0
# Namespace http://www.fuzzed.org/commonTypes [xmlns:common]


import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:56401044-224f-11e8-a35e-0242ac110002')

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
Namespace = pyxb.namespace.NamespaceForURI('http://www.fuzzed.org/commonTypes', create_if_missing=True)
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


# List simple type: {http://www.fuzzed.org/commonTypes}idList
# superclasses pyxb.binding.datatypes.anySimpleType
class idList (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.string."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'idList')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 26, 2)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.string
idList._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'idList', idList)
_module_typeBindings.idList = idList

# Complex type {http://www.fuzzed.org/commonTypes}Model with content type EMPTY
class Model (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/commonTypes}Model with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Model')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 11, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpwww_fuzzed_orgcommonTypes_Model_id', pyxb.binding.datatypes.string)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 13, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 13, 4)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.Model = Model
Namespace.addCategoryObject('typeBinding', 'Model', Model)


# Complex type {http://www.fuzzed.org/commonTypes}GraphNode with content type EMPTY
class GraphNode (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/commonTypes}GraphNode with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GraphNode')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 17, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute x uses Python identifier x
    __x = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'x'), 'x', '__httpwww_fuzzed_orgcommonTypes_GraphNode_x', pyxb.binding.datatypes.int)
    __x._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 19, 4)
    __x._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 19, 4)
    
    x = property(__x.value, __x.set, None, None)

    
    # Attribute y uses Python identifier y
    __y = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'y'), 'y', '__httpwww_fuzzed_orgcommonTypes_GraphNode_y', pyxb.binding.datatypes.int)
    __y._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 20, 4)
    __y._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 20, 4)
    
    y = property(__y.value, __y.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpwww_fuzzed_orgcommonTypes_GraphNode_id', pyxb.binding.datatypes.string)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 22, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 22, 4)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __x.name() : __x,
        __y.name() : __y,
        __id.name() : __id
    })
_module_typeBindings.GraphNode = GraphNode
Namespace.addCategoryObject('typeBinding', 'GraphNode', GraphNode)


# Complex type {http://www.fuzzed.org/commonTypes}DoubleToIntervalMap with content type ELEMENT_ONLY
class DoubleToIntervalMap (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/commonTypes}DoubleToIntervalMap with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DoubleToIntervalMap')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 31, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element value uses Python identifier value_
    __value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__httpwww_fuzzed_orgcommonTypes_DoubleToIntervalMap_value', False, pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 33, 6), )

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute key uses Python identifier key
    __key = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'key'), 'key', '__httpwww_fuzzed_orgcommonTypes_DoubleToIntervalMap_key', pyxb.binding.datatypes.double, required=True)
    __key._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 35, 4)
    __key._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 35, 4)
    
    key = property(__key.value, __key.set, None, None)

    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap.update({
        __key.name() : __key
    })
_module_typeBindings.DoubleToIntervalMap = DoubleToIntervalMap
Namespace.addCategoryObject('typeBinding', 'DoubleToIntervalMap', DoubleToIntervalMap)


# Complex type {http://www.fuzzed.org/commonTypes}Interval with content type EMPTY
class Interval (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/commonTypes}Interval with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Interval')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 38, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute lowerBound uses Python identifier lowerBound
    __lowerBound = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lowerBound'), 'lowerBound', '__httpwww_fuzzed_orgcommonTypes_Interval_lowerBound', pyxb.binding.datatypes.double, required=True)
    __lowerBound._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 39, 4)
    __lowerBound._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 39, 4)
    
    lowerBound = property(__lowerBound.value, __lowerBound.set, None, None)

    
    # Attribute upperBound uses Python identifier upperBound
    __upperBound = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'upperBound'), 'upperBound', '__httpwww_fuzzed_orgcommonTypes_Interval_upperBound', pyxb.binding.datatypes.double, required=True)
    __upperBound._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 40, 4)
    __upperBound._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 40, 4)
    
    upperBound = property(__upperBound.value, __upperBound.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lowerBound.name() : __lowerBound,
        __upperBound.name() : __upperBound
    })
_module_typeBindings.Interval = Interval
Namespace.addCategoryObject('typeBinding', 'Interval', Interval)


# Complex type {http://www.fuzzed.org/commonTypes}Issue with content type EMPTY
class Issue (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/commonTypes}Issue with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Issue')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 43, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute issueId uses Python identifier issueId
    __issueId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'issueId'), 'issueId', '__httpwww_fuzzed_orgcommonTypes_Issue_issueId', pyxb.binding.datatypes.int)
    __issueId._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 44, 6)
    __issueId._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 44, 6)
    
    issueId = property(__issueId.value, __issueId.set, None, None)

    
    # Attribute elementId uses Python identifier elementId
    __elementId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'elementId'), 'elementId', '__httpwww_fuzzed_orgcommonTypes_Issue_elementId', pyxb.binding.datatypes.string)
    __elementId._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 45, 6)
    __elementId._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 45, 6)
    
    elementId = property(__elementId.value, __elementId.set, None, None)

    
    # Attribute message uses Python identifier message
    __message = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'message'), 'message', '__httpwww_fuzzed_orgcommonTypes_Issue_message', pyxb.binding.datatypes.string)
    __message._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 46, 6)
    __message._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 46, 6)
    
    message = property(__message.value, __message.set, None, None)

    
    # Attribute isFatal uses Python identifier isFatal
    __isFatal = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isFatal'), 'isFatal', '__httpwww_fuzzed_orgcommonTypes_Issue_isFatal', pyxb.binding.datatypes.boolean)
    __isFatal._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 47, 6)
    __isFatal._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 47, 6)
    
    isFatal = property(__isFatal.value, __isFatal.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __issueId.name() : __issueId,
        __elementId.name() : __elementId,
        __message.name() : __message,
        __isFatal.name() : __isFatal
    })
_module_typeBindings.Issue = Issue
Namespace.addCategoryObject('typeBinding', 'Issue', Issue)


# Complex type {http://www.fuzzed.org/commonTypes}Probability with content type EMPTY
class Probability (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/commonTypes}Probability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Probability')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 51, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Probability = Probability
Namespace.addCategoryObject('typeBinding', 'Probability', Probability)


# Complex type {http://www.fuzzed.org/commonTypes}CrispProbability with content type EMPTY
class CrispProbability (Probability):
    """Complex type {http://www.fuzzed.org/commonTypes}CrispProbability with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CrispProbability')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 53, 2)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Attribute val uses Python identifier val
    __val = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'val'), 'val', '__httpwww_fuzzed_orgcommonTypes_CrispProbability_val', pyxb.binding.datatypes.double, required=True)
    __val._DeclarationLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 56, 8)
    __val._UseLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 56, 8)
    
    val = property(__val.value, __val.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __val.name() : __val
    })
_module_typeBindings.CrispProbability = CrispProbability
Namespace.addCategoryObject('typeBinding', 'CrispProbability', CrispProbability)


# Complex type {http://www.fuzzed.org/commonTypes}DecomposedFuzzyProbability with content type ELEMENT_ONLY
class DecomposedFuzzyProbability (Probability):
    """Complex type {http://www.fuzzed.org/commonTypes}DecomposedFuzzyProbability with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DecomposedFuzzyProbability')
    _XSDLocation = pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 61, 2)
    _ElementMap = Probability._ElementMap.copy()
    _AttributeMap = Probability._AttributeMap.copy()
    # Base type is Probability
    
    # Element alphaCuts uses Python identifier alphaCuts
    __alphaCuts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'alphaCuts'), 'alphaCuts', '__httpwww_fuzzed_orgcommonTypes_DecomposedFuzzyProbability_alphaCuts', True, pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 65, 10), )

    
    alphaCuts = property(__alphaCuts.value, __alphaCuts.set, None, None)

    _ElementMap.update({
        __alphaCuts.name() : __alphaCuts
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DecomposedFuzzyProbability = DecomposedFuzzyProbability
Namespace.addCategoryObject('typeBinding', 'DecomposedFuzzyProbability', DecomposedFuzzyProbability)




DoubleToIntervalMap._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'value'), Interval, scope=DoubleToIntervalMap, location=pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 33, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DoubleToIntervalMap._UseForTag(pyxb.namespace.ExpandedName(None, 'value')), pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 33, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DoubleToIntervalMap._Automaton = _BuildAutomaton()




DecomposedFuzzyProbability._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'alphaCuts'), DoubleToIntervalMap, scope=DecomposedFuzzyProbability, location=pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 65, 10)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 65, 10))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DecomposedFuzzyProbability._UseForTag(pyxb.namespace.ExpandedName(None, 'alphaCuts')), pyxb.utils.utility.Location('/FuzzEd/FuzzEd/static/xsd/commonTypes.xsd', 65, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DecomposedFuzzyProbability._Automaton = _BuildAutomaton_()

