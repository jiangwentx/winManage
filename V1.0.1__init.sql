
CREATE TABLE `ips` (
                       `id` int NOT NULL,
                       `ip` varchar(255) DEFAULT NULL,
                       `port` varchar(255) DEFAULT NULL,
                       `mport` varchar(255) DEFAULT NULL COMMENT '管理端口',
                       `username` varchar(255) DEFAULT NULL,
                       `passwd` varchar(255) DEFAULT NULL,
                       `status` varchar(255) DEFAULT NULL COMMENT '状态',
                       `resettime` datetime DEFAULT NULL COMMENT '重置时间',
                       `lastusetime` datetime DEFAULT NULL COMMENT '用户最后使用时间',
                       `sysid` int DEFAULT NULL COMMENT '系统ID',
                       `sysname` varchar(255) DEFAULT NULL COMMENT '系统名称',
                       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




INSERT INTO `winmanage`.`ips`(`id`, `ip`, `port`, `mport`, `username`, `passwd`, `status`, `resettime`, `lastusetime`, `sysid`, `sysname`) VALUES (4, '192.168.11.130', '3389', '5985', 'sqwa', 'd84c61f393ae90dfcba5b062f138757c', 'error', '2025-01-24 10:49:18', NULL, 1, NULL);
INSERT INTO `winmanage`.`ips`(`id`, `ip`, `port`, `mport`, `username`, `passwd`, `status`, `resettime`, `lastusetime`, `sysid`, `sysname`) VALUES (5, '192.168.11.123', '3389', '5985', 'sqwa', '', 'free', NULL, NULL, 2, NULL);


