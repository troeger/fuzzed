# front/FuzzEd/models/xml_backend.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:05ee920a1d4f1202361106450bf13e4b20aed253
# Generated 2018-03-13 20:23:23.647052 by PyXB version 1.2.6 using Python 3.5.2.final.0
# Namespace http://www.fuzzed.org/backendResults

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:60e52fd2-26fc-11e8-8df3-0242ac110002')

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
from . import xml_common as _ImportedBinding_xml_common
from . import xml_configurations as _ImportedBinding_xml_configurations

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.fuzzed.org/backendResults', create_if_missing=True)
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


# Complex type {http://www.fuzzed.org/backendResults}Result with content type ELEMENT_ONLY
class Result (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.fuzzed.org/backendResults}Result with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Result')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 15, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element issue uses Python identifier issue
    __issue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'issue'), 'issue', '__httpwww_fuzzed_orgbackendResults_Result_issue', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6), )

    
    issue = property(__issue.value, __issue.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpwww_fuzzed_orgbackendResults_Result_id', pyxb.binding.datatypes.string)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 19, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 19, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute modelId uses Python identifier modelId
    __modelId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'modelId'), 'modelId', '__httpwww_fuzzed_orgbackendResults_Result_modelId', pyxb.binding.datatypes.string, required=True)
    __modelId._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 20, 4)
    __modelId._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 20, 4)
    
    modelId = property(__modelId.value, __modelId.set, None, None)

    
    # Attribute configId uses Python identifier configId
    __configId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'configId'), 'configId', '__httpwww_fuzzed_orgbackendResults_Result_configId', pyxb.binding.datatypes.string, required=True)
    __configId._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 21, 4)
    __configId._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 21, 4)
    
    configId = property(__configId.value, __configId.set, None, None)

    
    # Attribute timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timestamp'), 'timestamp', '__httpwww_fuzzed_orgbackendResults_Result_timestamp', pyxb.binding.datatypes.string, required=True)
    __timestamp._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 22, 4)
    __timestamp._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 22, 4)
    
    timestamp = property(__timestamp.value, __timestamp.set, None, None)

    
    # Attribute validResult uses Python identifier validResult
    __validResult = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'validResult'), 'validResult', '__httpwww_fuzzed_orgbackendResults_Result_validResult', pyxb.binding.datatypes.boolean, required=True)
    __validResult._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 23, 4)
    __validResult._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 23, 4)
    
    validResult = property(__validResult.value, __validResult.set, None, None)

    _ElementMap.update({
        __issue.name() : __issue
    })
    _AttributeMap.update({
        __id.name() : __id,
        __modelId.name() : __modelId,
        __configId.name() : __configId,
        __timestamp.name() : __timestamp,
        __validResult.name() : __validResult
    })
_module_typeBindings.Result = Result
Namespace.addCategoryObject('typeBinding', 'Result', Result)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 61, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element configuration uses Python identifier configuration
    __configuration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'configuration'), 'configuration', '__httpwww_fuzzed_orgbackendResults_CTD_ANON_configuration', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 63, 10), )

    
    configuration = property(__configuration.value, __configuration.set, None, None)

    
    # Element result uses Python identifier result
    __result = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'result'), 'result', '__httpwww_fuzzed_orgbackendResults_CTD_ANON_result', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 64, 10), )

    
    result = property(__result.value, __result.set, None, None)

    
    # Element issue uses Python identifier issue
    __issue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'issue'), 'issue', '__httpwww_fuzzed_orgbackendResults_CTD_ANON_issue', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 65, 10), )

    
    issue = property(__issue.value, __issue.set, None, None)

    _ElementMap.update({
        __configuration.name() : __configuration,
        __result.name() : __result,
        __issue.name() : __issue
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.fuzzed.org/backendResults}MincutResult with content type ELEMENT_ONLY
class MincutResult (Result):
    """Complex type {http://www.fuzzed.org/backendResults}MincutResult with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MincutResult')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 26, 2)
    _ElementMap = Result._ElementMap.copy()
    _AttributeMap = Result._AttributeMap.copy()
    # Base type is Result
    
    # Element issue (issue) inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Element nodeid uses Python identifier nodeid
    __nodeid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'nodeid'), 'nodeid', '__httpwww_fuzzed_orgbackendResults_MincutResult_nodeid', True, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 30, 10), )

    
    nodeid = property(__nodeid.value, __nodeid.set, None, None)

    
    # Attribute id inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute modelId inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute configId inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute timestamp inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute validResult inherited from {http://www.fuzzed.org/backendResults}Result
    _ElementMap.update({
        __nodeid.name() : __nodeid
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MincutResult = MincutResult
Namespace.addCategoryObject('typeBinding', 'MincutResult', MincutResult)


# Complex type {http://www.fuzzed.org/backendResults}SimulationResult with content type ELEMENT_ONLY
class SimulationResult (Result):
    """Complex type {http://www.fuzzed.org/backendResults}SimulationResult with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SimulationResult')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 36, 2)
    _ElementMap = Result._ElementMap.copy()
    _AttributeMap = Result._AttributeMap.copy()
    # Base type is Result
    
    # Element issue (issue) inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute id inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute modelId inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute configId inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute timestamp inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute validResult inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute reliability uses Python identifier reliability
    __reliability = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'reliability'), 'reliability', '__httpwww_fuzzed_orgbackendResults_SimulationResult_reliability', pyxb.binding.datatypes.double, required=True)
    __reliability._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 39, 8)
    __reliability._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 39, 8)
    
    reliability = property(__reliability.value, __reliability.set, None, None)

    
    # Attribute nFailures uses Python identifier nFailures
    __nFailures = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'nFailures'), 'nFailures', '__httpwww_fuzzed_orgbackendResults_SimulationResult_nFailures', pyxb.binding.datatypes.int, required=True)
    __nFailures._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 40, 8)
    __nFailures._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 40, 8)
    
    nFailures = property(__nFailures.value, __nFailures.set, None, None)

    
    # Attribute nSimulatedRounds uses Python identifier nSimulatedRounds
    __nSimulatedRounds = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'nSimulatedRounds'), 'nSimulatedRounds', '__httpwww_fuzzed_orgbackendResults_SimulationResult_nSimulatedRounds', pyxb.binding.datatypes.int, required=True)
    __nSimulatedRounds._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 41, 8)
    __nSimulatedRounds._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 41, 8)
    
    nSimulatedRounds = property(__nSimulatedRounds.value, __nSimulatedRounds.set, None, None)

    
    # Attribute availability uses Python identifier availability
    __availability = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'availability'), 'availability', '__httpwww_fuzzed_orgbackendResults_SimulationResult_availability', pyxb.binding.datatypes.double)
    __availability._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 42, 8)
    __availability._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 42, 8)
    
    availability = property(__availability.value, __availability.set, None, None)

    
    # Attribute duration uses Python identifier duration
    __duration = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'duration'), 'duration', '__httpwww_fuzzed_orgbackendResults_SimulationResult_duration', pyxb.binding.datatypes.double)
    __duration._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 43, 8)
    __duration._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 43, 8)
    
    duration = property(__duration.value, __duration.set, None, None)

    
    # Attribute mttf uses Python identifier mttf
    __mttf = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mttf'), 'mttf', '__httpwww_fuzzed_orgbackendResults_SimulationResult_mttf', pyxb.binding.datatypes.double)
    __mttf._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 44, 8)
    __mttf._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 44, 8)
    
    mttf = property(__mttf.value, __mttf.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __reliability.name() : __reliability,
        __nFailures.name() : __nFailures,
        __nSimulatedRounds.name() : __nSimulatedRounds,
        __availability.name() : __availability,
        __duration.name() : __duration,
        __mttf.name() : __mttf
    })
_module_typeBindings.SimulationResult = SimulationResult
Namespace.addCategoryObject('typeBinding', 'SimulationResult', SimulationResult)


# Complex type {http://www.fuzzed.org/backendResults}AnalysisResult with content type ELEMENT_ONLY
class AnalysisResult (Result):
    """Complex type {http://www.fuzzed.org/backendResults}AnalysisResult with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnalysisResult')
    _XSDLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 49, 2)
    _ElementMap = Result._ElementMap.copy()
    _AttributeMap = Result._AttributeMap.copy()
    # Base type is Result
    
    # Element issue (issue) inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Element probability uses Python identifier probability
    __probability = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'probability'), 'probability', '__httpwww_fuzzed_orgbackendResults_AnalysisResult_probability', False, pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 53, 10), )

    
    probability = property(__probability.value, __probability.set, None, None)

    
    # Attribute id inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute modelId inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute configId inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute timestamp inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute validResult inherited from {http://www.fuzzed.org/backendResults}Result
    
    # Attribute decompositionNumber uses Python identifier decompositionNumber
    __decompositionNumber = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'decompositionNumber'), 'decompositionNumber', '__httpwww_fuzzed_orgbackendResults_AnalysisResult_decompositionNumber', pyxb.binding.datatypes.int, required=True)
    __decompositionNumber._DeclarationLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 55, 8)
    __decompositionNumber._UseLocation = pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 55, 8)
    
    decompositionNumber = property(__decompositionNumber.value, __decompositionNumber.set, None, None)

    _ElementMap.update({
        __probability.name() : __probability
    })
    _AttributeMap.update({
        __decompositionNumber.name() : __decompositionNumber
    })
_module_typeBindings.AnalysisResult = AnalysisResult
Namespace.addCategoryObject('typeBinding', 'AnalysisResult', AnalysisResult)


backendResults = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'backendResults'), CTD_ANON, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 60, 2))
Namespace.addCategoryObject('elementBinding', backendResults.name().localName(), backendResults)



Result._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'issue'), _ImportedBinding_xml_common.Issue, scope=Result, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Result._UseForTag(pyxb.namespace.ExpandedName(None, 'issue')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Result._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'configuration'), _ImportedBinding_xml_configurations.Configuration, scope=CTD_ANON, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 63, 10)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'result'), Result, scope=CTD_ANON, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 64, 10)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'issue'), _ImportedBinding_xml_common.Issue, scope=CTD_ANON, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 65, 10)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 63, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 64, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 65, 10))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'configuration')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 63, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'result')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 64, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'issue')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 65, 10))
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
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




MincutResult._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'nodeid'), pyxb.binding.datatypes.string, scope=MincutResult, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 30, 10)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 30, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MincutResult._UseForTag(pyxb.namespace.ExpandedName(None, 'issue')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MincutResult._UseForTag(pyxb.namespace.ExpandedName(None, 'nodeid')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 30, 10))
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
MincutResult._Automaton = _BuildAutomaton_2()




def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SimulationResult._UseForTag(pyxb.namespace.ExpandedName(None, 'issue')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SimulationResult._Automaton = _BuildAutomaton_3()




AnalysisResult._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'probability'), _ImportedBinding_xml_common.Probability, scope=AnalysisResult, location=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 53, 10)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 53, 10))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AnalysisResult._UseForTag(pyxb.namespace.ExpandedName(None, 'issue')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 17, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(AnalysisResult._UseForTag(pyxb.namespace.ExpandedName(None, 'probability')), pyxb.utils.utility.Location('/ore/front/FuzzEd/static/xsd/backendResult.xsd', 53, 10))
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
AnalysisResult._Automaton = _BuildAutomaton_4()

