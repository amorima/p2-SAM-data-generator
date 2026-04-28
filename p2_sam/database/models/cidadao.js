const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Cidadao = sequelize.define(
  "Cidadao",
  {
   nome: {
    type: DataTypes.STRING(50),
    primaryKey: true,
   },
   contacto: {
    type: DataTypes.STRING(13),
    allowNull: false,
   },
   rgpd: {
    type: DataTypes.TINYINT,
    allowNull: false,
   },
  },
  {
   tableName: "Contacto",
   timestamps: false,
  },
 );

 Cidadao.associate = (models) => {
  // Cidadao pertence a entidade
  Cidadao.belongsTo(models.Leads, {
   foreignKey: "entidade_nif_nipc",
   as: "entidade",
  });
 };

 return Cidadao;
};
