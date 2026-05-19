const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Doacao = sequelize.define(
  "Doacao",
  {
   id_doacao: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
   },
   mecena_nif_nipc: {
    type: DataTypes.STRING(9),
    allowNull: false,
   },
   data: {
    type: DataTypes.DATE,
    allowNull: false,
   },
   valor_transacao: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false,
   },
   tipo_donativo: {
    type: DataTypes.ENUM("REFERENCIA", "NUMERARIO", "CHEQUE", "TRANFERENCIA"), // caso se adicione um novo metodo de pagamento, adicionar aqui
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
    type: DataTypes.ENUM("ACEITE", "REJEITADO", "PENDENTE"),
    allowNull: false,
   },
  },
  {
   tableName: "doacao",
   timestamps: false,
  },
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
