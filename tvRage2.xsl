<?xml version="1.0" encoding="ISO-8859-1" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">

<html>
<body>
Test
<xsl:for-each select="guide/time">
<h2><xsl:value-of select="header" /></h2>
<xsl:for-each select="show">
<ul>
<li><b><xsl:value-of select="network" /></b> - <xsl:value-of select="@name" />: <xsl:value-of select="title"/></li>
</ul>
</xsl:for-each>
</xsl:for-each>
</body>
</html>

</xsl:template>
</xsl:stylesheet>