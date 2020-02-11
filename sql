-- ----------------------------
-- Table structure for users_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile`;
CREATE TABLE `users_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `openid` varchar(200) NOT NULL,
  `avatarUrl` varchar(500) NOT NULL,
  `country` varchar(100) NOT NULL,
  `user_bh` varchar(50) NOT NULL,
  `province` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `language` varchar(100) NOT NULL,
  `background` varchar(100),
  `nickName` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `birthay` date NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `thesignature` longtext NOT NULL,
  `agreement` tinyint(1) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `user_bh` (`user_bh`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- -----
