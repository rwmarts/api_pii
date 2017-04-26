-- MySQL dump 10.13  Distrib 5.7.9, for Win32 (AMD64)
--
-- Host: 127.0.0.1    Database: pii_db
-- ------------------------------------------------------
-- Server version	5.7.12-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `client_domains`
--

DROP TABLE IF EXISTS `client_domains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_domains` (
  `client_domains_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_domain` varchar(45) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`client_domains_id`),
  UNIQUE KEY `client_id_UNIQUE` (`client_domains_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `frequencies`
--

DROP TABLE IF EXISTS `frequencies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `frequencies` (
  `frequencies_id` int(11) NOT NULL AUTO_INCREMENT,
  `frequency` varchar(45) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`frequencies_id`),
  UNIQUE KEY `frequency_id_UNIQUE` (`frequencies_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metrics`
--

DROP TABLE IF EXISTS `metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metrics` (
  `metrics_id` int(11) NOT NULL AUTO_INCREMENT,
  `providers_id` int(11) NOT NULL,
  `metric` varchar(45) NOT NULL,
  `validation_type` varchar(45) NOT NULL,
  `must_hash` tinyint(1) NOT NULL,
  PRIMARY KEY (`metrics_id`),
  UNIQUE KEY `metric_id_UNIQUE` (`metrics_id`),
  KEY `fk_metric_provider_idx` (`providers_id`),
  CONSTRAINT `fk_metric_provider` FOREIGN KEY (`providers_id`) REFERENCES `providers` (`providers_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `provider_clients`
--

DROP TABLE IF EXISTS `provider_clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `provider_clients` (
  `provider_clients_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_domains_id` int(11) NOT NULL,
  `providers_id` int(11) NOT NULL,
  `clients_api_id` varchar(45) NOT NULL,
  `clients_api_name` varchar(45) NOT NULL,
  PRIMARY KEY (`provider_clients_id`),
  UNIQUE KEY `provider_clients_id_UNIQUE` (`provider_clients_id`),
  KEY `fk_provider_clients_client_domains_idx` (`client_domains_id`),
  KEY `fk_provider_clients_providers_id_idx` (`providers_id`),
  CONSTRAINT `fk_provider_clients_client_domains` FOREIGN KEY (`client_domains_id`) REFERENCES `client_domains` (`client_domains_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_provider_clients_providers_id` FOREIGN KEY (`providers_id`) REFERENCES `providers` (`providers_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `providers`
--

DROP TABLE IF EXISTS `providers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `providers` (
  `providers_id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(45) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `auth_json` blob,
  PRIMARY KEY (`providers_id`),
  UNIQUE KEY `provider_id_UNIQUE` (`providers_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schedules`
--

DROP TABLE IF EXISTS `schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedules` (
  `schedules_id` int(11) NOT NULL AUTO_INCREMENT,
  `providers_id` int(11) NOT NULL,
  `frequencies_id` int(11) NOT NULL,
  `hash` varchar(100) NOT NULL,
  `expires` datetime NOT NULL,
  `active` tinyint(1) NOT NULL,
  `client_domain_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`schedules_id`),
  UNIQUE KEY `schedule_id_UNIQUE` (`schedules_id`),
  KEY `fk_schedule_provider_idx` (`providers_id`),
  KEY `fk_schedule_frequency_idx` (`frequencies_id`),
  CONSTRAINT `fk_schedule_frequency` FOREIGN KEY (`frequencies_id`) REFERENCES `frequencies` (`frequencies_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_schedule_provider` FOREIGN KEY (`providers_id`) REFERENCES `providers` (`providers_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schedules_metrics`
--

DROP TABLE IF EXISTS `schedules_metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedules_metrics` (
  `schedules_id` int(11) NOT NULL,
  `metrics_id` int(11) NOT NULL,
  KEY `fk_schedules_metrics_schedules_idx` (`schedules_id`),
  KEY `fk_schedules_metrics_metrics_idx` (`metrics_id`),
  CONSTRAINT `fk_schedules_metrics_metrics` FOREIGN KEY (`metrics_id`) REFERENCES `metrics` (`metrics_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_schedules_metrics_schedules` FOREIGN KEY (`schedules_id`) REFERENCES `schedules` (`schedules_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_types`
--

DROP TABLE IF EXISTS `user_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_types` (
  `user_types_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_type` varchar(45) NOT NULL,
  PRIMARY KEY (`user_types_id`),
  UNIQUE KEY `user_types_id_UNIQUE` (`user_types_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `users_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(45) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `date_added` datetime DEFAULT NULL,
  `access_token` varchar(100) DEFAULT NULL,
  `pii_token` varchar(100) DEFAULT NULL,
  `pii_token_expires` datetime DEFAULT NULL,
  `oauth_token` varchar(100) DEFAULT NULL,
  `user_types_id` int(11) NOT NULL,
  `approved` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`users_id`),
  UNIQUE KEY `id_UNIQUE` (`users_id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `fk_users_user_types_idx` (`user_types_id`),
  CONSTRAINT `fk_users_user_types` FOREIGN KEY (`user_types_id`) REFERENCES `user_types` (`user_types_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_client_domains`
--

DROP TABLE IF EXISTS `users_client_domains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_client_domains` (
  `users_id` int(11) NOT NULL,
  `client_domains_id` int(11) NOT NULL,
  KEY `fk_users_client_domains_users_idx` (`users_id`),
  KEY `fk_users_client_domains_client_domains_idx` (`client_domains_id`),
  CONSTRAINT `fk_users_client_domains_client_domains` FOREIGN KEY (`client_domains_id`) REFERENCES `client_domains` (`client_domains_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_client_domains_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`users_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_schedules`
--

DROP TABLE IF EXISTS `users_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_schedules` (
  `users_id` int(11) NOT NULL,
  `schedules_id` int(11) NOT NULL,
  KEY `fk_users_schedules_users_idx` (`users_id`),
  KEY `fk_users_schedules_schedules_idx` (`schedules_id`),
  CONSTRAINT `fk_users_schedules_schedules` FOREIGN KEY (`schedules_id`) REFERENCES `schedules` (`schedules_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_schedules_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`users_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-26  9:25:01
