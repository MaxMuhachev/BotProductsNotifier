-- MySQL dump 10.13  Distrib 8.0.19, for macos10.15 (x86_64)
--
-- Host: localhost    Database: millioner
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;
/*!40103 SET TIME_ZONE = '+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;
/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;

--
-- Table structure for table `answers`
--
CREATE DATABASE product_notifier;
USE product_notifier;

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products`
(
    `id`                    int NOT NULL AUTO_INCREMENT,
    `name`                  varchar(255) DEFAULT NULL,
    `price_last_citilink`   int(20)          DEFAULT NULL,
    `price_last_technopark` int(20)          DEFAULT NULL,
    `price_last_biggeek`    int(20)          DEFAULT NULL,
    `price_last_notik`      int(20)          DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_name` (`name`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 26
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `user_track`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_track`
(
    `chat_id`                   int      NOT NULL,
    `product_id`                int      NOT NULL,
    `date_updated`              DATETIME NOT NULL DEFAULT (now()) ON UPDATE now(),
    `last_notification`         DATETIME          DEFAULT NULL,
    `every_hour`                int               DEFAULT NULL,
    `notification_price_change` tinyint(1)        DEFAULT '0',
    `price_low`                 int               DEFAULT NULL,
    KEY `questionId` (`chat_id`, `product_id`),
    UNIQUE KEY `uq_chat_priduct` (`chat_id`, `product_id`),
    CONSTRAINT `fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--


