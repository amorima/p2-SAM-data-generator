const mongoose = require("mongoose");

// Armazena eventos técnicos e heartbeats dos Painéis e Lockers

const IotTelemetrySchema = new mongoose.Schema(
 {
  timestamp: {
   type: Date,
   required: true,
  },
  evento: {
   type: String,
   enum: ["HEARTBEAT", "OVERHEAT", "ERRO"],
   required: true,
  },
  // Referência ao id do dispositivo na BD SQL (painel.id_painel ou locker.id_locker)
  dispositivo_id: {
   type: Number,
   required: true,
  },
  tipo: {
   type: String,
   enum: ["LOCKER", "PAINEL"],
   required: true,
  },
  localizacao: {
   geo_latitude: { type: Number },
   geo_longitude: { type: Number },
  },
  telemetria: {
   bateria_voltagem: { type: Number },
   cpu_temp: { type: Number },
   sinal_dbm: { type: Number },
   aviso: {
    type: String,
    enum: ["NENHUM", "BATERIA_CRITICA", "TEMPERATURA_ALTA"],
    default: "NENHUM",
   },
  },
 },
 {
  collection: "iot_telemetry",
  timestamps: false,
 }
);

// Índices para acelerar as queries de manutenção preventiva do documento
IotTelemetrySchema.index({ dispositivo_id: 1 });
IotTelemetrySchema.index({ "telemetria.cpu_temp": 1 });
IotTelemetrySchema.index({ "telemetria.bateria_voltagem": 1 });

module.exports = mongoose.model("IotTelemetry", IotTelemetrySchema);
