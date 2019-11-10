-- MySQL dump 10.13  Distrib 8.0.17, for macos10.14 (x86_64)
--
-- Host: localhost    Database: project_hh
-- ------------------------------------------------------
-- Server version	8.0.17

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
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (1,'Python',5260),(2,'Java',1912),(3,'PHP',708),(4,'Pascal',23),(5,'Ruby',435),(6,'ABAP',22),(7,'JavaScript',826),(8,'C++',781),(9,'SQL',3119),(10,'Delphi',55),(11,'TypeScript',146),(12,'.NET',201),(13,'Kotlin',142),(14,'Scala',325),(15,'MySQL',727),(16,'PostgreSQL',1131),(17,'Redis',428),(18,'Cassandra',141),(19,'Prometheus',217),(20,'InfluxDB',42),(21,'MongoDB',364),(22,'MariaDB',45),(23,'CouchDB',5),(24,'ClickHouse',199),(25,'Django',482),(26,'Flask',236),(27,'AIOHTTP',81),(28,'Falcon',29),(29,'Spark',306),(30,'TCP/IP',352),(31,'TCP',438),(32,'WebSocket',60),(33,'Elasticsearch',261),(34,'Solr',35),(35,'Sphinx',30),(36,'Tornado',92),(37,'Apache',362),(38,'Nginx',471),(39,'RabbitMQ',365),(40,'Kafka',307),(41,'Amazon SQS',0),(42,'Windows',571),(43,'Linux',2007),(44,'Debian',182),(45,'Git',1902),(46,'Bitbucket',136),(47,'Github',164),(48,'Mercurial',70),(49,'Docker',1137),(50,'VMware',233),(51,'PowerShell',194),(52,'Ansible',648),(53,'Jenkins',627),(54,'TeamCity',224),(55,'Sqlalchemy',52),(56,'Mongoengine',1),(57,'Hibernate',36),(58,'Redmine',78),(59,'Confluence',258),(60,'Scrum',307),(61,'Kanban',99),(62,'Agile',523),(63,'Zabbix',406);
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-08 20:55:52
