const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Bens_E_Servicos_Negocio = sequelize.define(
  "bens_e_servicos_negocio",
  {
   id_oferta: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
   },
   negocio_nif_nipc: {
    type: DataTypes.STRING(20),
    allowNull: false,
   },
   tipo_bem_servico: {
    type: DataTypes.STRING(100),
    allowNull: false,
   },
   descricao: {
    type: DataTypes.STRING(255),
    allowNull: false,
   },
   valor_total: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false,
   },
   desconto: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false,
   },
  },
  {
   tableName: "bens_e_servicos_negocio",
   timestamps: false,
  }
 );

 Bens_E_Servicos_Negocio.associate = (models) => {
  //
  Bens_E_Servicos_Negocio.belongsTo(models.Bens_E_Servico, {
   foreignKey: "tipo_bem_servico",
   as: "bens_e_servico",
  });
  Bens_E_Servicos_Negocio.belongsTo(models.Negocio, {
   foreignKey: "negocio_nif_nipc",
   as: "negocio",
  });
 };

 return Bens_E_Servicos_Negocio;
};
