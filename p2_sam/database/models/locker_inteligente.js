const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Locker_Inteligente = sequelize.define(
  "locker_inteligente",
  {
   id_locker: {
    type: DataTypes.STRING(45),
    primaryKey: true,
    autoIncrement: true,
   },
   estado: {
    type: DataTypes.ENUM("DISPONIVEL", "INDISPONIVEL", "OCUPADO", "MANUTENCAO"),
    allowNull: false,
   },
   codigo_mestre: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   geo_latitude: {
    type: DataTypes.DECIMAL(10, 8),
    allowNull: false,
   },
   geo_longitude: {
    type: DataTypes.DECIMAL(11, 8),
    allowNull: false,
   },
   codigo_mestre: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
  },
  {
   tableName: "locker_inteligente",
   timestamps: false,
  },
 );

 Locker_Inteligente.associate = (models) => {
  //
  Locker_Inteligente.hasMany(models.Lead, {
   foreignKey: "id_locker",
   as: "locker",
  });
 };

 return Locker_Inteligente;
};
