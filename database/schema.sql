DROP DATABASE IF EXISTS password_manager;
CREATE DATABASE IF NOT EXISTS password_manager;
CREATE USER 'password-manager'@'%' IDENTIFIED BY 'Humorous3-Boss-Residual';
GRANT SELECT, INSERT, DELETE, UPDATE ON `password_manager`.* TO 'password-manager'@'%';A
USE password_manager;


CREATE TABLE IF NOT EXISTS `password_manager`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `main_password_hash` VARCHAR(255) NOT NULL,
  `totp_secret` VARCHAR(255),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);


CREATE TABLE IF NOT EXISTS `password_manager`.`password` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `website` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password_hash` BLOB NOT NULL,
  `nonce` BLOB NOT NULL,
  `tag` BLOB NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_password_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_password_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `password_manager`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);