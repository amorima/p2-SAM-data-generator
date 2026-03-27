const mongoose = require("mongoose");
const { ENUM } = require("sequelize");

// Regista notificações

const InteractionLogSchema = new mongoose.Schema({
 // Referencia a BD SQL (lead.id_lead)
 lead_sql_id: {
  type: Number,
  require: true,
  unique: true,
 },
 tipo: {
  type: String,
  require: true,
 },
 destinatario_hash: {
  type: String, // Dados "hashed" sao guardados como strings
  require: true,
 },
 data_envio: {
  type: Date,
  require: true,
 },
 estado_envio: {
  type: String,
  require: true,
 },
 tentativas: {
  type: Number,
  require: true,
 },
 motivo_erro: {
  type: String,
  require: true,
 },
});

module.exports = mongoose.model("notification", InteractionLogSchema);
