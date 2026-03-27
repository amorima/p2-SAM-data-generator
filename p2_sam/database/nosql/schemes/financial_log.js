const mongoose = require("mongoose");

// Armazena registos técnicos de comunicação com gateways de pagamento

const FinancialAuditSchema = new mongoose.Schema(
 {
  // Referência à PK da tabela doacao no MySQL
  transacao_sql_id: {
   type: Number,
   required: true,
  },
  metodo: {
   type: String,
   enum: ["MBWAY", "MULTIBANCO", "TRANSFERENCIA", "CHEQUE", "NUMERARIO"],
   required: true,
  },
  data_hora: {
   type: Date,
   required: true,
  },
  status_gateway: {
   type: String,
   enum: ["SUCESSO", "FALHA", "PENDENTE"],
   required: true,
  },
  // Mixed porque a estrutura varia consoante o método de pagamento
  // MBWay tem telemovel_hash, Multibanco tem referencia (...)
  gateway_response: {
   type: mongoose.Schema.Types.Mixed,
   required: true,
  },
 },
 {
  collection: "financial_audit",
  timestamps: false,
 }
);

// Índice para a query de auditoria de falhas do documento
FinancialAuditSchema.index({ transacao_sql_id: 1 });
FinancialAuditSchema.index({ status_gateway: 1 });
FinancialAuditSchema.index({ data_hora: -1 }); // -1 = descendente, mais recente primeiro

module.exports = mongoose.model("FinancialAudit", FinancialAuditSchema);
