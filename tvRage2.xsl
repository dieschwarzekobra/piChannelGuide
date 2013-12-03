<?xml version="1.0" encoding="ISO-8859-1" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">

<html>
<head>
<title>piChannelGuide</title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<div class="header">
<h1>piChannelGuide</h1>
</div>
<div class="comingUp">
<xsl:for-each select="guide/time">
<h2><xsl:value-of select="header" /></h2>

<ul>
<xsl:for-each select="show">
<li><b><xsl:value-of select="network" /></b> - <xsl:value-of select="@name" />: <xsl:value-of select="title"/></li>
</xsl:for-each>
</ul>

</xsl:for-each>
</div>

<div class="channels">
<ul>
<xsl:for-each select="guide/channel">
<li><xsl:value-of select="." /></li>
</xsl:for-each>
</ul>
</div>
</body>
</html>

</xsl:template>
</xsl:stylesheet>