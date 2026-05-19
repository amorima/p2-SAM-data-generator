const fs = require("fs");
const path = require("path");

function loadRootEnv() {
 const envPath = path.resolve(__dirname, "../../../.env");

 if (!fs.existsSync(envPath)) {
  return;
 }

 const lines = fs.readFileSync(envPath, "utf8").split(/\r?\n/);

 for (const line of lines) {
  const trimmed = line.trim();

  if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) {
   continue;
  }

  const [key, ...valueParts] = trimmed.split("=");
  const value = valueParts.join("=").trim().replace(/^["']|["']$/g, "");

  if (!process.env[key]) {
   process.env[key] = value;
  }
 }
}

loadRootEnv();

const config = {
 username: process.env.DB_USER || "root",
 password: process.env.DB_PASSWORD || process.env.DB_PASS || null,
 database: process.env.DB_NAME || "database_development",
 host: process.env.DB_HOST || "127.0.0.1",
 port: Number(process.env.DB_PORT || 3306),
 dialect: process.env.DB_DIALECT || "mysql",
};

module.exports = {
 development: config,
 test: config,
 production: config,
 ...config,
};
