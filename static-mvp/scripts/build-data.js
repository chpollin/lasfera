const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

/**
 * Build all data files from YAML to JSON
 */

function loadYamlFiles(dir) {
  const files = fs.readdirSync(dir);
  const data = {};

  for (const file of files) {
    if (!file.endsWith('.yaml')) continue;

    const filePath = path.join(dir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const parsed = yaml.load(content);

    // Use filename without extension as key
    const key = file.replace('.yaml', '');
    data[key] = parsed;
  }

  return data;
}

function buildManuscripts() {
  const manuscriptsDir = path.join(__dirname, '../data/manuscripts');
  const outputFile = path.join(__dirname, '../src/_data/manuscripts.json');

  const manuscripts = loadYamlFiles(manuscriptsDir);

  // Convert to array for easier iteration in templates
  const manuscriptsArray = Object.values(manuscripts);

  fs.writeFileSync(
    outputFile,
    JSON.stringify(manuscriptsArray, null, 2),
    'utf8'
  );

  console.log(`✓ Built ${manuscriptsArray.length} manuscripts`);
  return manuscriptsArray;
}

function buildStanzas() {
  const stanzasDir = path.join(__dirname, '../data/stanzas');
  const outputFile = path.join(__dirname, '../src/_data/stanzas.json');

  const stanzas = loadYamlFiles(stanzasDir);

  // Convert to array sorted by line_code
  const stanzasArray = Object.values(stanzas).sort((a, b) =>
    a.line_code.localeCompare(b.line_code)
  );

  fs.writeFileSync(
    outputFile,
    JSON.stringify(stanzasArray, null, 2),
    'utf8'
  );

  console.log(`✓ Built ${stanzasArray.length} stanzas`);
  return stanzasArray;
}

function buildTranslations() {
  const translationsDir = path.join(__dirname, '../data/translations');
  const outputFile = path.join(__dirname, '../src/_data/translations.json');

  const translations = loadYamlFiles(translationsDir);

  // Group by line_code for easy lookup
  const translationsObj = {};
  for (const [key, value] of Object.entries(translations)) {
    translationsObj[value.line_code] = value;
  }

  fs.writeFileSync(
    outputFile,
    JSON.stringify(translationsObj, null, 2),
    'utf8'
  );

  console.log(`✓ Built ${Object.keys(translationsObj).length} translations`);
  return translationsObj;
}

function buildLocations() {
  const locationsDir = path.join(__dirname, '../data/locations');
  const outputFile = path.join(__dirname, '../src/_data/locations.json');

  const locations = loadYamlFiles(locationsDir);
  const locationsArray = Object.values(locations);

  fs.writeFileSync(
    outputFile,
    JSON.stringify(locationsArray, null, 2),
    'utf8'
  );

  console.log(`✓ Built ${locationsArray.length} locations`);
  return locationsArray;
}

// Run all build steps
console.log('Building La Sfera static data files...\n');

// Ensure output directory exists
const dataDir = path.join(__dirname, '../src/_data');
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

buildManuscripts();
buildStanzas();
buildTranslations();
buildLocations();

console.log('\n✅ Build complete!');
