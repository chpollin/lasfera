module.exports = function(eleventyConfig) {

  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/assets");

  // Add filter to get translation for a stanza
  eleventyConfig.addFilter("getTranslation", function(translations, lineCode) {
    return translations[lineCode] || null;
  });

  // Add filter to format line code (for display)
  eleventyConfig.addFilter("formatLineCode", function(lineCode) {
    return lineCode; // For now, just return as-is
  });

  return {
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["njk", "md", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
