const mongoose = require("mongoose");

// Regista vouchers emitidos

const InteractionLogSchema = new mongoose.Schema({
 montante: {
  type: Number,
  require: true,
 },
 data_emissao: {
  type: Date,
  require: true,
 },
 estado: {
  type: String,
  require: true,
 },
 validade: {
  type: Date,
  require: true,
 },
 entidade_disponivel_levantamento: {
  type: String,
  require: true,
 },
 data_uso: {
  type: Date,
  require: true,
 },
});

module.exports = mongoose.model("vouchers", InteractionLogSchema);
