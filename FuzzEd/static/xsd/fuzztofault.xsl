<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
	xmlns:ft="net.fuzztree">
 <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="xsd:complexType[@name='DecomposedFuzzyProbability']"/>
  <xsl:template match="xsd:element[@name='DecomposedFuzzyProbability']"/>
  <xsl:template match="xsd:complexType[@name='InclusionVariationPoint']"/>
  <xsl:template match="xsd:element[@name='RedundancyVariationPoint']"/>
  <xsl:template match="xsd:complexType[@name='RedundancyVariationPoint']"/>
  <xsl:template match="xsd:element[@name='TriangularFuzzyInterval']"/>
  <xsl:template match="xsd:complexType[@name='TriangularFuzzyInterval']"/>
  <xsl:template match="xsd:element[@name='FeatureVariationPoint']"/>
  <xsl:template match="xsd:extension[@base='ft:InclusionVariationPoint']"/>
  <xsl:template match="xsd:complexType[@name='FuzzTree']">
  	<xsl:copy>
		<xsl:attribute name="name">
  		  <xsl:value-of select="'FaultTree'"/>
		</xsl:attribute>
	</xsl:copy>
  </xsl:template>
</xsl:stylesheet>




