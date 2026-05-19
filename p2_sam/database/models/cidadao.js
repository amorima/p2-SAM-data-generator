const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Cidadao = sequelize.define(
  "cidadao",
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
   blocked: {
    type: DataTypes.TINYINT,
    allowNull: false,
    defaultValue: 0,
   },
   role: {
    type: DataTypes.STRING(255),
    allowNull: false,
    defaultValue: null,
   },
   reason: {
    type: DataTypes.STRING(255),
    allowNull: true,
    defaultValue: null,
   },
  },
  {
   tableName: "cidadao",
   timestamps: false,
   validate: {
    reasonMatchesBlocked() {
     if (this.blocked === 1 && !this.reason) {
      throw new Error("reason é obrigatório quando blocked é 1");
     }

     if (this.blocked !== 1 && this.reason) {
      throw new Error("reason só deve existir quando blocked é 1");
     }
    },
   },
  },
 );

 Cidadao.associate = (models) => {
  Cidadao.hasMany(models.Lead, {
   foreignKey: "nome_cidadao",
   sourceKey: "nome",
   as: "leads",
  });
 };

 return Cidadao;
};
