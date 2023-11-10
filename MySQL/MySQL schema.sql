CREATE DATABASE  IF NOT EXISTS `binance` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `binance`;
-- MySQL dump 10.13  Distrib 8.0.25, for macos11 (x86_64)
--
-- Host: 95.165.15.68    Database: binance
-- ------------------------------------------------------
-- Server version	8.0.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `book_ticker_busdrub`
--

DROP TABLE IF EXISTS `book_ticker_busdrub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_ticker_busdrub` (
  `u` bigint DEFAULT NULL,
  `bid_price` decimal(15,8) DEFAULT NULL,
  `bid_qty` decimal(15,8) DEFAULT NULL,
  `ask_price` decimal(15,8) DEFAULT NULL,
  `ask_qty` decimal(15,8) DEFAULT NULL,
  `datetime` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `buf_trades`
--

DROP TABLE IF EXISTS `buf_trades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buf_trades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(45) DEFAULT NULL,
  `tradeid` bigint DEFAULT NULL,
  `orderId` bigint DEFAULT NULL,
  `orderlistId` int DEFAULT NULL,
  `price` varchar(45) DEFAULT NULL,
  `qty` varchar(45) DEFAULT NULL,
  `quoteqty` varchar(45) DEFAULT NULL,
  `commission` varchar(45) DEFAULT NULL,
  `commissionasset` varchar(10) DEFAULT NULL,
  `time` bigint DEFAULT NULL,
  `isBuyer` tinyint DEFAULT NULL,
  `isMaker` tinyint DEFAULT NULL,
  `isBestMatch` tinyint DEFAULT NULL,
  `isLoaded` tinyint(1) DEFAULT '0',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `IX_tradeid_isloaded` (`tradeid`,`isLoaded`),
  KEY `IX_time` (`time` DESC)
) ENGINE=InnoDB AUTO_INCREMENT=637 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fund`
--

DROP TABLE IF EXISTS `fund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fund` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brief` varchar(45) NOT NULL,
  `name` varchar(100) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `brief_UNIQUE` (`brief`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brief` varchar(45) DEFAULT NULL,
  `image` blob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kvitrelation`
--

DROP TABLE IF EXISTS `kvitrelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kvitrelation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kv_datetime` datetime DEFAULT NULL,
  `security` varchar(45) DEFAULT NULL,
  `buy_id` int DEFAULT NULL,
  `sell_id` int DEFAULT NULL,
  `qty` decimal(15,8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index4` (`security`,`kv_datetime`,`buy_id`),
  KEY `index_buy_id` (`buy_id`),
  KEY `index_sell_id` (`sell_id`)
) ENGINE=InnoDB AUTO_INCREMENT=718 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `log_level` int DEFAULT NULL,
  `log_levelname` varchar(45) DEFAULT NULL,
  `log` varchar(2048) DEFAULT NULL,
  `created_by` varchar(150) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3136 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partial_book_depth_busdrub`
--

DROP TABLE IF EXISTS `partial_book_depth_busdrub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partial_book_depth_busdrub` (
  `type` varchar(3) DEFAULT NULL,
  `price` decimal(15,8) DEFAULT NULL,
  `qty` decimal(15,8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `quik_prices_view`
--

DROP TABLE IF EXISTS `quik_prices_view`;
/*!50001 DROP VIEW IF EXISTS `quik_prices_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `quik_prices_view` AS SELECT 
 1 AS `security`,
 1 AS `ask`,
 1 AS `ask_qty`,
 1 AS `ask_datetime`,
 1 AS `bid`,
 1 AS `bid_qty`,
 1 AS `bid_datetime`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `quik_quotes`
--

DROP TABLE IF EXISTS `quik_quotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quik_quotes` (
  `security` varchar(150) DEFAULT NULL,
  `price` decimal(15,6) DEFAULT NULL,
  `buy` decimal(15,6) DEFAULT NULL,
  `sell` decimal(15,6) DEFAULT NULL,
  `datetime` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `security`
--

DROP TABLE IF EXISTS `security`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `security` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brief` varchar(45) NOT NULL,
  `name` varchar(100) DEFAULT '',
  `fund1` varchar(45) DEFAULT NULL,
  `fund2` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `brief_UNIQUE` (`brief`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `xml` text,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=107010 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `telegram_subscribes`
--

DROP TABLE IF EXISTS `telegram_subscribes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telegram_subscribes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `unsubscribe` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `threads`
--

DROP TABLE IF EXISTS `threads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `threads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brief` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `timestamp` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_brief` (`brief`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trade`
--

DROP TABLE IF EXISTS `trade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade` (
  `id` int NOT NULL AUTO_INCREMENT,
  `security` varchar(45) NOT NULL,
  `trade_date` date DEFAULT NULL,
  `trade_num` bigint DEFAULT NULL,
  `order_num` bigint DEFAULT NULL,
  `side` tinyint(1) NOT NULL,
  `price` decimal(15,8) DEFAULT NULL,
  `qty` decimal(15,8) DEFAULT NULL,
  `quoteqty` decimal(15,8) DEFAULT NULL,
  `commission` decimal(15,8) DEFAULT NULL,
  `commission_asset` varchar(45) DEFAULT NULL,
  `is_maker` tinyint(1) DEFAULT NULL,
  `is_best_match` tinyint(1) DEFAULT NULL,
  `timestamp` bigint DEFAULT NULL,
  `trade_datetime` datetime DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=681 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `quik_prices_view`
--

/*!50001 DROP VIEW IF EXISTS `quik_prices_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `quik_prices_view` AS select `b`.`security` AS `security`,`b`.`price` AS `ask`,`b`.`buy` AS `ask_qty`,`b`.`datetime` AS `ask_datetime`,`s`.`price` AS `bid`,`s`.`sell` AS `bid_qty`,`s`.`datetime` AS `bid_datetime` from (((select `quik_quotes`.`security` AS `security`,max((case when (`quik_quotes`.`buy` <> 0) then `quik_quotes`.`price` else 0 end)) AS `ask`,min((case when (`quik_quotes`.`sell` <> 0) then `quik_quotes`.`price` else 1000000000 end)) AS `bid` from `quik_quotes` group by `quik_quotes`.`security`) `best` join (select `q`.`security` AS `security`,`q`.`price` AS `price`,`q`.`buy` AS `buy`,`q`.`sell` AS `sell`,`q`.`datetime` AS `datetime` from `quik_quotes` `q`) `b`) join (select `q`.`security` AS `security`,`q`.`price` AS `price`,`q`.`buy` AS `buy`,`q`.`sell` AS `sell`,`q`.`datetime` AS `datetime` from `quik_quotes` `q`) `s`) where ((`b`.`security` = `best`.`security`) and (`b`.`price` = `best`.`ask`) and (`s`.`security` = `best`.`security`) and (`s`.`price` = `best`.`bid`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-10 12:59:14
