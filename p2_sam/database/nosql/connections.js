const mongoose = require("mongoose");

// função para conectar ao MongoDB com Mongoose.
// Ela tenta conectar à base de dados com
// as variáveis de ambiente para a URI
// e o nome da base de dados com resultados

const connectMongoDB = async () => {
 try {
  await mongoose.connect(process.env.MONGODB_URI, {
   dbName: process.env.MONGODB_DB_NAME,
  });
  console.log("MongoDB conectado com sucesso");
 } catch (error) {
  console.error("Erro ao conectar ao MongoDB:", error);
  process.exit(1);
 }
};

module.exports = connectMongoDB;
