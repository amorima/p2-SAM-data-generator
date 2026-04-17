const mongoose = require("mongoose");

// função para conectar ao MongoDB usando Mongoose. 
// Ela tenta estabelecer uma conexão com o banco de 
// dados usando as variáveis de ambiente para a URI 
// e o nome do banco de dados. Se a conexão for bem-sucedida, 

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
