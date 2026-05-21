"use strict";
const { sequelize } = require("./models");
(async () => {
 for (const t of ["pedido_bens_e_servicos", "leads"]) {
  console.log(`\n=== ${t} ===`);
  const [rows] = await sequelize.query(`SHOW COLUMNS FROM ${t}`);
  rows.forEach((r) => console.log(`  ${r.Field}: ${r.Type} null=${r.Null} default=${r.Default} key=${r.Key} extra=${r.Extra}`));
 }
 const [fks] = await sequelize.query(`
   SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
   FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
   WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'leads' AND REFERENCED_TABLE_NAME IS NOT NULL
 `);
 console.log("\n=== leads FKs ===");
 fks.forEach((r) => console.log(`  ${r.COLUMN_NAME} -> ${r.REFERENCED_TABLE_NAME}.${r.REFERENCED_COLUMN_NAME} (${r.CONSTRAINT_NAME})`));
 await sequelize.close();
})();
