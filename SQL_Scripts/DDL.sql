use N01518034F21;

-- MySQL Script generated by MySQL Workbench
-- Tue Nov 23 16:39:10 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customers_pr` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `user_name` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `email_address` VARCHAR(45) NULL,
  PRIMARY KEY (`customer_id`));



-- -----------------------------------------------------
-- Table `departments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `departments_pr` (
  `department_id` INT NOT NULL AUTO_INCREMENT,
  `department_name` VARCHAR(45) NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`department_id`));
  


-- -----------------------------------------------------
-- Table `products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `products_pr` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(45) NULL,
  `price` DECIMAL(10,2) NULL,
  `description` TEXT NULL,
  `department_id` INT NOT NULL,
  PRIMARY KEY (`product_id`),
   INDEX `fk_products_departments_idx` (`department_id` ASC),
  CONSTRAINT `fk_products_departments`
    FOREIGN KEY (`department_id`)
    REFERENCES `departments_pr` (`department_id`));
    



-- -----------------------------------------------------
-- Table `orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `orders_pr` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `order_price` DECIMAL(10,2) NOT NULL,
  `order_date` DATETIME NULL,
  `tax_amount` DECIMAL(10,2) NOT NULL,
  `customer_id` INT NOT NULL,
  PRIMARY KEY (`order_id`),
    CONSTRAINT `fk_orders_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `customers_pr` (`customer_id`));
   

-- -----------------------------------------------------
-- Table `items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `items_pr` (
  `item_id` INT NOT NULL AUTO_INCREMENT,
  `quantity` INT NULL,
  `item_price` DECIMAL(10,2) NULL,
  `product_id` INT NOT NULL,
  `order_id` INT NOT NULL,
  PRIMARY KEY (`item_id`),
    CONSTRAINT `fk_items_products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `products_pr` (`product_id`),
  CONSTRAINT `fk_items_orders1`
    FOREIGN KEY (`order_id`)
    REFERENCES `orders_pr` (`order_id`));
   


-- -----------------------------------------------------
-- Table `addresses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `addresses_pr` (
  `address_id` INT NOT NULL AUTO_INCREMENT,
  `line1` VARCHAR(60) NULL,
  `line2` VARCHAR(60) NULL,
  `state` VARCHAR(2) NULL,
  `zip_code` VARCHAR(10) NULL,
  `customer_id` INT NOT NULL,
  PRIMARY KEY (`address_id`),
    CONSTRAINT `fk_addresses_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `customers_pr` (`customer_id`));
    


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;