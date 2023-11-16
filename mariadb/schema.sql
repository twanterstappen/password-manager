CREATE DATABASE password_manager;
USE password_manager;

CREATE TABLE IF NOT EXISTS `password_manager`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `main_password_hash` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);


CREATE TABLE IF NOT EXISTS `password_manager`.`password` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `website` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password_hash` BLOB NOT NULL,
  `nonce` BLOB NOT NULL,
  `tag` BLOB NOT NULL,
  `note` VARCHAR(255) NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_password_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_password_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `password_manager`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


INSERT INTO `password_manager`.`user` VALUES(
	NULL,
    'Twan Terstappen',
    'twanterstappen@gmail.com',
    '$2b$12$vlBDUMOJ1Lx3O6JaGhi31uGlaZoygvp6YgWmva/al/wUgW2X4Hu5C' # Welkom123!
);