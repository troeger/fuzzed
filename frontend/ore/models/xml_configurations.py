# ore/models/xml_configurations.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:380e5bfe768ca2a493a558a9fe7b1795196a7c97
# Generated 2019-01-09 14:06:28.482992 by PyXB version 1.2.6 using Python 2.7.15.candidate.1
# Namespace http://www.fuzzed.org/configurations [xmlns:configurations]

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
Namespace = pyxb.namespace.NamespaceForURI('http://www.fuzzed.org/configurations', create_if_missing=True)
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


# Complex type {http://www.fuzzed.org/configurations}Choice with content type EMPTY
class Choice (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/configurations}Choice with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Choice')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 7, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Choice = Choice
Namespace.addCategoryObject('typeBinding', 'Choice', Choice)


# Complex type {http://www.fuzzed.org/configurations}IntegerToChoiceMap with content type ELEMENT_ONLY
class IntegerToChoiceMap (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/configurations}IntegerToChoiceMap with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IntegerToChoiceMap')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 9, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element value uses Python identifier value_
    __value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__httpwww_fuzzed_orgconfigurations_IntegerToChoiceMap_value', False, pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 11, 6), )

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute key uses Python identifier key
    __key = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'key'), 'key', '__httpwww_fuzzed_orgconfigurations_IntegerToChoiceMap_key', pyxb.binding.datatypes.string, required=True)
    __key._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 13, 4)
    __key._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 13, 4)
    
    key = property(__key.value, __key.set, None, None)

    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap.update({
        __key.name() : __key
    })
_module_typeBindings.IntegerToChoiceMap = IntegerToChoiceMap
Namespace.addCategoryObject('typeBinding', 'IntegerToChoiceMap', IntegerToChoiceMap)


# Complex type {http://www.fuzzed.org/configurations}Configuration with content type ELEMENT_ONLY
class Configuration (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/configurations}Configuration with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Configuration')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 16, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element choice uses Python identifier choice
    __choice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'choice'), 'choice', '__httpwww_fuzzed_orgconfigurations_Configuration_choice', True, pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 18, 6), )

    
    choice = property(__choice.value, __choice.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpwww_fuzzed_orgconfigurations_Configuration_id', pyxb.binding.datatypes.string, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 20, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 20, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute costs uses Python identifier costs
    __costs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'costs'), 'costs', '__httpwww_fuzzed_orgconfigurations_Configuration_costs', pyxb.binding.datatypes.int, required=True)
    __costs._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 21, 4)
    __costs._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 21, 4)
    
    costs = property(__costs.value, __costs.set, None, None)

    _ElementMap.update({
        __choice.name() : __choice
    })
    _AttributeMap.update({
        __id.name() : __id,
        __costs.name() : __costs
    })
_module_typeBindings.Configuration = Configuration
Namespace.addCategoryObject('typeBinding', 'Configuration', Configuration)


# Complex type {http://www.fuzzed.org/configurations}InclusionChoice with content type EMPTY
class InclusionChoice (Choice):
    """Complex type {http://www.fuzzed.org/configurations}InclusionChoice with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'InclusionChoice')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 24, 2)
    _ElementMap = Choice._ElementMap.copy()
    _AttributeMap = Choice._AttributeMap.copy()
    # Base type is Choice
    
    # Attribute included uses Python identifier included
    __included = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'included'), 'included', '__httpwww_fuzzed_orgconfigurations_InclusionChoice_included', pyxb.binding.datatypes.boolean, required=True)
    __included._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 27, 8)
    __included._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 27, 8)
    
    included = property(__included.value, __included.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __included.name() : __included
    })
_module_typeBindings.InclusionChoice = InclusionChoice
Namespace.addCategoryObject('typeBinding', 'InclusionChoice', InclusionChoice)


# Complex type {http://www.fuzzed.org/configurations}RedundancyChoice with content type EMPTY
class RedundancyChoice (Choice):
    """Complex type {http://www.fuzzed.org/configurations}RedundancyChoice with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RedundancyChoice')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 32, 2)
    _ElementMap = Choice._ElementMap.copy()
    _AttributeMap = Choice._AttributeMap.copy()
    # Base type is Choice
    
    # Attribute n uses Python identifier n
    __n = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'n'), 'n', '__httpwww_fuzzed_orgconfigurations_RedundancyChoice_n', pyxb.binding.datatypes.int, required=True)
    __n._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 35, 8)
    __n._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 35, 8)
    
    n = property(__n.value, __n.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __n.name() : __n
    })
_module_typeBindings.RedundancyChoice = RedundancyChoice
Namespace.addCategoryObject('typeBinding', 'RedundancyChoice', RedundancyChoice)


# Complex type {http://www.fuzzed.org/configurations}FeatureChoice with content type EMPTY
class FeatureChoice (Choice):
    """Complex type {http://www.fuzzed.org/configurations}FeatureChoice with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FeatureChoice')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 40, 2)
    _ElementMap = Choice._ElementMap.copy()
    _AttributeMap = Choice._AttributeMap.copy()
    # Base type is Choice
    
    # Attribute featureId uses Python identifier featureId
    __featureId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'featureId'), 'featureId', '__httpwww_fuzzed_orgconfigurations_FeatureChoice_featureId', pyxb.binding.datatypes.string, required=True)
    __featureId._DeclarationLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 43, 8)
    __featureId._UseLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 43, 8)
    
    featureId = property(__featureId.value, __featureId.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __featureId.name() : __featureId
    })
_module_typeBindings.FeatureChoice = FeatureChoice
Namespace.addCategoryObject('typeBinding', 'FeatureChoice', FeatureChoice)


# Complex type {http://www.fuzzed.org/configurations}TransferInChoice with content type ELEMENT_ONLY
class TransferInChoice (Choice):
    """Complex type {http://www.fuzzed.org/configurations}TransferInChoice with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TransferInChoice')
    _XSDLocation = pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 48, 2)
    _ElementMap = Choice._ElementMap.copy()
    _AttributeMap = Choice._AttributeMap.copy()
    # Base type is Choice
    
    # Element chosenConfiguration uses Python identifier chosenConfiguration
    __chosenConfiguration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'chosenConfiguration'), 'chosenConfiguration', '__httpwww_fuzzed_orgconfigurations_TransferInChoice_chosenConfiguration', False, pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 52, 10), )

    
    chosenConfiguration = property(__chosenConfiguration.value, __chosenConfiguration.set, None, None)

    _ElementMap.update({
        __chosenConfiguration.name() : __chosenConfiguration
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TransferInChoice = TransferInChoice
Namespace.addCategoryObject('typeBinding', 'TransferInChoice', TransferInChoice)




IntegerToChoiceMap._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'value'), Choice, scope=IntegerToChoiceMap, location=pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 11, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(IntegerToChoiceMap._UseForTag(pyxb.namespace.ExpandedName(None, 'value')), pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 11, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IntegerToChoiceMap._Automaton = _BuildAutomaton()




Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'choice'), IntegerToChoiceMap, scope=Configuration, location=pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 18, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 18, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'choice')), pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 18, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Configuration._Automaton = _BuildAutomaton_()




TransferInChoice._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'chosenConfiguration'), Configuration, scope=TransferInChoice, location=pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 52, 10)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TransferInChoice._UseForTag(pyxb.namespace.ExpandedName(None, 'chosenConfiguration')), pyxb.utils.utility.Location('/ore-common/xsd/configurations.xsd', 52, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TransferInChoice._Automaton = _BuildAutomaton_2()

