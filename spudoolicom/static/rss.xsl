<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<!-- This causes the HTML doctype (<!doctype hmlt>) to be rendered. -->
	<xsl:output method="html" doctype-system="about:legacy-compat" indent="yes" />

	<!-- Start matching at the Channel node within the XML RSS feed. -->
	<xsl:template match="/rss/channel">

		<html lang="en">
		<head>
			<meta charset="utf-8" />
			<meta name="viewport" content="width=device-width, initial-scale=1" />

			<title>
				<xsl:value-of select="title" />
			</title>

		</head>
		<body>

			<h1 class="title">
				<xsl:value-of select="title" />
			</h1>

			<p class="description">
				<xsl:value-of select="description" />
			</p>

			<ul class="posts">
				<xsl:for-each select="./item">

					<li class="posts__post post">

						<h2 class="post__title">
							<a href="{ link }" class="post__link">
								<xsl:value-of select="title" />
							</a>
						</h2>

						<p class="post__preview">
							<xsl:value-of select="description" />

							<a href="{ link }" class="post__more">Read more</a>
						</p>

					</li>

				</xsl:for-each>
			</ul>

			<p class="cta">
				<a href="{ link }" class="cta__link">View all posts on <strong></strong></a>
			</p>

		</body>
		</html>

	</xsl:template>

</xsl:stylesheet>