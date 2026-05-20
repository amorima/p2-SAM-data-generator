const mongoose = require("mongoose");
const fs = require("fs");
const path = require("path");

// função para conectar ao MongoDB com Mongoose.
// Ela tenta conectar à base de dados com
// as variáveis de ambiente para a URI
// e o nome da base de dados com resultados

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

const connectMongoDB = async () => {
 try {
  await mongoose.connect(process.env.MONGODB_URI, {
   user: process.env.MONGODB_USER,
   pass: process.env.MONGODB_PASSWORD,
   authSource: process.env.MONGODB_AUTH_SOURCE,
   dbName: process.env.MONGODB_DB_NAME,
  });
  console.log("MongoDB conectado com sucesso");
 } catch (error) {
  console.error("Erro ao conectar ao MongoDB:", error);
  process.exit(1);
 }
};

module.exports = connectMongoDB;
