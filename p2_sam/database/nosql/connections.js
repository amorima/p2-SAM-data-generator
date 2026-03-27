const mongoose = require("mongoose");

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
