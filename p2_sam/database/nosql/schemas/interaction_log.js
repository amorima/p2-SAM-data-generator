const mongoose = require("mongoose");

// Regista o comportamento do cidadão nos Painéis Digitais

const InteractionLogSchema = new mongoose.Schema(
 {
  sessao_id: {
   type: Number,
   required: true,
   unique: true,
  },
  // Referência ao id do painel na BD SQL
  painel_id: {
   type: Number,
   required: true,
  },
  inicio_sessao: {
   type: Date,
   required: true,
  },
  duracao_segundos: {
   type: Number,
   required: true,
  },
  // Array com o caminho percorrido pelo cidadão no ecrã
  // ["Home", "Mapa", "Ver_Necessidade", "Doar", "Inserir_MBWAY"]
  fluxo_navegacao: {
   type: [String],
   required: true,
  },
  concluiu_doacao: {
   type: Boolean,
   required: true,
   default: false,
  },
 },
 {
  collection: "interaction_logs",
  timestamps: false,
 }
);

// Índices para as queries de análise de funil e abandono do documento
InteractionLogSchema.index({ painel_id: 1 });
InteractionLogSchema.index({ concluiu_doacao: 1 });
InteractionLogSchema.index({ inicio_sessao: -1 }); // -1 = descendente, mais recente primeiro

module.exports = mongoose.model("InteractionLog", InteractionLogSchema);
