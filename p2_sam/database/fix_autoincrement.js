"use strict";

// Applies AUTO_INCREMENT to PK columns that were created without it.
// Run this once via the SSH tunnel (see .env for tunnel instructions):
//   node fix_autoincrement.js

const { sequelize } = require("./models");

const fixes = [
  "ALTER TABLE `doacao` MODIFY `id_doacao` INT NOT NULL AUTO_INCREMENT",
  "ALTER TABLE `leads` MODIFY `id_lead` INT NOT NULL AUTO_INCREMENT",
  "ALTER TABLE `pedido` MODIFY `id_pedido` INT NOT NULL AUTO_INCREMENT",
];

async function main() {
  await sequelize.authenticate();
  console.log("Ligado à base de dados.");

  for (const sql of fixes) {
    try {
      await sequelize.query(sql);
      console.log(`OK: ${sql}`);
    } catch (e) {
      console.warn(`SKIP (${e.message.split("\n")[0]}): ${sql}`);
    }
  }

  await sequelize.close();
  console.log("Concluído.");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
