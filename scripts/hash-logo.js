// Prints the SHA-256 hash for the logo file.
// Usage: node scripts/hash-logo.js [path/to/file]
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function hashFile(file) {
  const bytes = fs.readFileSync(file);
  return "0x" + crypto.createHash("sha256").update(bytes).digest("hex");
}

if (require.main === module) {
  const file = process.argv[2] || path.join(__dirname, "..", "alu-logo.jpg");
  console.log("File  :", file);
  console.log("SHA-256:", hashFile(file));
}

module.exports = { hashFile };
