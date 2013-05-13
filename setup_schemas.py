commonXsd='''
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xsd:schema xmlns:ft="{0}" xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="{0}">
  
  <!--Abstract Types-->
  <xsd:complexType abstract="true" name="Annotation"/>
  <xsd:complexType abstract="true" name="Probability"/>

  <xsd:complexType abstract="true" name="AnnotatedElement">
    <xsd:sequence>
      <xsd:element maxOccurs="unbounded" minOccurs="0" name="annotations" type="ft:Annotation"/>
    </xsd:sequence>
    <xsd:attribute name="id" type="xsd:int" use="required"/>
    <xsd:attribute name="name" type="xsd:string"/>
  </xsd:complexType>

  <xsd:complexType abstract="true" name="Model">
    <xsd:complexContent>
      <xsd:extension base="ft:AnnotatedElement"/>
    </xsd:complexContent>
  </xsd:complexType>

  <!--Abstract Tree Nodes-->
  <xsd:complexType abstract="true" name="Node">
    <xsd:complexContent>
      <xsd:extension base="ft:AnnotatedElement">
        <xsd:sequence>
          <xsd:element maxOccurs="unbounded" minOccurs="0" name="children" type="ft:ChildNode"/>
        </xsd:sequence>
        <xsd:attribute name="x" type="xsd:int"/>
        <xsd:attribute name="y" type="xsd:int"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:complexType abstract="true" name="ChildNode">
    <xsd:complexContent>
      <xsd:extension base="ft:Node"/>
    </xsd:complexContent>
  </xsd:complexType>

  <!--Tree-->
  <xsd:complexType name="{1}">
    <xsd:complexContent>
      <xsd:extension base="ft:Model">
        <xsd:sequence>
          <xsd:element maxOccurs="1" minOccurs="1" name="topEvent" type="ft:TopEvent"/>
        </xsd:sequence>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="{1}" type="ft:{1}"/>

  <xsd:complexType name="TopEvent">
    <xsd:complexContent>
      <xsd:extension base="ft:Node"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="TopEvent" type="ft:TopEvent"/>

  <xsd:complexType name="CrispProbability">
    <xsd:complexContent>
      <xsd:extension base="ft:Probability">
        <xsd:attribute name="value" type="xsd:double" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>

  <!--Static Tree Gates-->
  <xsd:complexType abstract="true" name="Gate">
    <xsd:complexContent>
      <xsd:extension base="ft:ChildNode"/>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:complexType name="And">
    <xsd:complexContent>
      <xsd:extension base="ft:Gate"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="And" type="ft:And"/>

  <xsd:complexType name="Or">
    <xsd:complexContent>
      <xsd:extension base="ft:Gate"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="Or" type="ft:Or"/>

  <xsd:complexType name="Xor">
    <xsd:complexContent>
      <xsd:extension base="ft:Gate"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="Xor" type="ft:Xor"/>

  <xsd:complexType name="VotingOr">
    <xsd:complexContent>
      <xsd:extension base="ft:Gate">
        <xsd:attribute name="k" type="xsd:int" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="VotingOr" type="ft:VotingOr"/>

  <!--Tree Leaf Nodes-->
  <xsd:complexType name="TransferIn">
    <xsd:complexContent>
      <xsd:extension base="{2}">
        <xsd:attribute name="fromModelId" type="xsd:int" use="required"/>
        <xsd:attribute default="0" name="maxCosts" type="xsd:int"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="TransferIn" type="ft:TransferIn"/>

  <xsd:complexType name="UndevelopedEvent">
    <xsd:complexContent>
      <xsd:extension base="ft:ChildNode"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="UndevelopedEvent" type="ft:UndevelopedEvent"/>

  <xsd:complexType name="HouseEvent">
    <xsd:complexContent>
      <xsd:extension base="ft:BasicEvent"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="HouseEvent" type="ft:HouseEvent"/>

  <xsd:complexType name="BasicEvent">
    <xsd:complexContent>
      <xsd:extension base="{2}">
        <xsd:sequence>
          <xsd:element maxOccurs="1" minOccurs="1" name="probability" type="ft:Probability"/>
        </xsd:sequence>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="BasicEvent" type="ft:BasicEvent"/>
'''

faultTreeXsd = '''
  <!--Dynamic Fault Tree Gates-->
  <xsd:complexType abstract="true" name="DynamicGate">
    <xsd:complexContent>
      <xsd:extension base="ft:Gate"/>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:simpleType name="idlist">
    <xsd:list itemType="xsd:int"/>
  </xsd:simpleType>

  <xsd:complexType name="ColdSpare">
    <xsd:complexContent>
      <xsd:extension base="ft:DynamicGate">
        <xsd:attribute name="spareIds" type="ft:idlist" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="ColdSpare" type="ft:ColdSpare"/>

  <xsd:complexType name="PriorityAnd">
    <xsd:complexContent>
      <xsd:extension base="ft:DynamicGate">
        <xsd:attribute name="priorityIds" type="ft:idlist" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="PriorityAnd" type="ft:PriorityAnd"/>

  <xsd:complexType name="Sequence">
    <xsd:complexContent>
      <xsd:extension base="ft:DynamicGate">
        <xsd:attribute name="eventSequence" type="ft:idlist" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="Sequence" type="ft:Sequence"/>

  <xsd:complexType name="FDEP">
    <xsd:complexContent>
      <xsd:extension base="ft:DynamicGate">
        <xsd:attribute name="triggeredEvents" type="ft:idlist" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="FDEP" type="ft:FDEP"/>
'''

fuzzTreeXsd = '''
  <!--FuzzTree Variation Points-->

  <xsd:complexType name="FeatureVariationPoint">
    <xsd:complexContent>
      <xsd:extension base="ft:VariationPoint"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="FeatureVariationPoint" type="ft:FeatureVariationPoint"/>
  <xsd:complexType name="RedundancyVariationPoint">
    <xsd:complexContent>
      <xsd:extension base="ft:VariationPoint">
        <xsd:attribute name="start" type="xsd:int" use="required"/>
        <xsd:attribute name="end" type="xsd:int" use="required"/>
        <xsd:attribute name="formula" type="xsd:string" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="RedundancyVariationPoint" type="ft:RedundancyVariationPoint"/>

  <xsd:complexType abstract="true" name="VariationPoint">
    <xsd:complexContent>
      <xsd:extension base="ft:ChildNode"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="CrispProbability" type="ft:CrispProbability"/>

  <xsd:complexType name="TriangularFuzzyInterval">
    <xsd:complexContent>
      <xsd:extension base="ft:Probability">
        <xsd:attribute name="a" type="xsd:double" use="required"/>
        <xsd:attribute name="b1" type="xsd:double" use="required"/>
        <xsd:attribute name="b2" type="xsd:double" use="required"/>
        <xsd:attribute name="c" type="xsd:double" use="required"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="TriangularFuzzyInterval" type="ft:TriangularFuzzyInterval"/>

  <xsd:complexType name="IntermediateEvent">
    <xsd:complexContent>
      <xsd:extension base="ft:InclusionVariationPoint"/>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="IntermediateEvent" type="ft:IntermediateEvent"/>

  <xsd:complexType name="BasicEventSet">
    <xsd:complexContent>
      <xsd:extension base="ft:BasicEvent">
        <xsd:attribute name="quantity" type="xsd:int"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="BasicEventSet" type="ft:BasicEventSet"/>

  <xsd:complexType name="IntermediateEventSet">
    <xsd:complexContent>
      <xsd:extension base="ft:IntermediateEvent">
        <xsd:attribute name="quantity" type="xsd:int"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="IntermediateEventSet" type="ft:IntermediateEventSet"/>

  <xsd:complexType abstract="true" name="EventSet">
    <xsd:complexContent>
      <xsd:extension base="ft:InclusionVariationPoint">
        <xsd:attribute name="quantity" type="xsd:int"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:complexType abstract="true" name="InclusionVariationPoint">
    <xsd:complexContent>
      <xsd:extension base="ft:VariationPoint">
        <xsd:attribute default="false" name="optional" type="xsd:boolean"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:complexType name="DecomposedFuzzyProbability">
    <xsd:complexContent>
      <xsd:extension base="ft:Probability">
        <xsd:sequence>
          <xsd:element maxOccurs="unbounded" minOccurs="0" name="alphaCuts" type="ft:DoubleToIntervalMap"/>
        </xsd:sequence>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="DecomposedFuzzyProbability" type="ft:DecomposedFuzzyProbability"/>
   
  <xsd:complexType name="DoubleToIntervalMap">
    <xsd:sequence>
      <xsd:element maxOccurs="1" minOccurs="1" name="value" type="ft:Interval"/>
    </xsd:sequence>
    <xsd:attribute name="key" type="xsd:double" use="required"/>
  </xsd:complexType>
  <xsd:element name="DoubleToIntervalMap" type="ft:DoubleToIntervalMap"/>

  <xsd:complexType name="Interval">
    <xsd:attribute name="lowerBound" type="xsd:double" use="required"/>
    <xsd:attribute name="upperBound" type="xsd:double" use="required"/>
  </xsd:complexType>
  <xsd:element name="Interval" type="ft:Interval"/>
'''

def createFaultTreeSchema(fname):
	xsd = commonXsd.format('net.faulttree', 'FaultTree', 'ft:ChildNode') + faultTreeXsd + '</xsd:schema>'
	print "Writing new XSD file to "+fname
	f=open(fname,'w')
	f.write(xsd)
	f.close()

def createFuzzTreeSchema(fname):
	xsd = commonXsd.format('net.fuzztree', 'FuzzTree', 'ft:VariationPoint') + fuzzTreeXsd + '</xsd:schema>'
	print "Writing new XSD file to "+fname
	f=open(fname,'w')
	f.write(xsd)
	f.close()


