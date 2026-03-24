const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Doacao = sequelize.define(
  "Doacao",
  {
   id_doacao: {
    type: DataTypes.INTEGER,
    primarykey: true,
    autoIncrement: true,
   },
   mecena_nif_nipc: {
    type: DataTypes.INTEGER(9),
    allowNull: false,
   },
   data: {
    type: DataTypes.DATE,
    allowNull: false,
   },
   valor_transacao: {
    type: DataTypes.DECIMAL(10, 8),
    allowNull: false,
   },
   tipo_donativo: {
    type: DataTypes.ENUM(
     "numerário",
     "cheque",
     "transferência",
     "multibanco",
     "mbway"
    ), // caso se adicione um novo metodo de pagamento, adicionar aqui
    allowNull: false,
   },
   anonimo: {
    type: DataTypes.BOOLEAN,
    allowNull: false,
   },
   url_comprovativo: {
    type: DataTypes.TEXT,
    allowNull: false,
   },
   estado: {
    type: DataTypes.ENUM("pendente", "finalizado", "rejeitado"),
    allowNull: false,
   },
  },
  {
   tableName: "doacao",
   timestamps: false,
  }
 );

 Doacao.associate = (models) => {
  // Cada doação pertence a um mecenas
  Doacao.belongsTo(models.Mecena, {
   foreignKey: "mecena_nif_nipc",
   as: "mecena",
  });
 };

 return Doacao;
};
