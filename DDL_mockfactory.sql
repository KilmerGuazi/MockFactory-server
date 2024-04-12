/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = data_source   */
/******************************************/
CREATE TABLE `data_source` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '数据源名称',
  `type` tinyint NOT NULL DEFAULT '1' COMMENT '数据集类型,1: MYSQL, 2:CLICKHOUSE,3:REDIS,4:KAFKA,5:MQ,6:INTERFACE',
  `project_id` int NOT NULL COMMENT '项目id',
  `ext_info` varchar(510) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '数据源拓展信息',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int DEFAULT '0' COMMENT '删除状态,0:未删除,1:已删除',
  `disabled` tinyint DEFAULT '0' COMMENT '禁用状态,0:未禁用,1:已禁用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='数据源'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = data_template   */
/******************************************/
CREATE TABLE `data_template` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '模板名称',
  `project_id` int NOT NULL COMMENT '项目id',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  `disabled` tinyint DEFAULT '0' COMMENT '禁用状态,0:未禁用,1:已禁用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_deleted` (`name`,`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COMMENT='数据模板'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = data_template_detail   */
/******************************************/
CREATE TABLE `data_template_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_template_id` int NOT NULL COMMENT '模板id',
  `comment` varchar(255) NOT NULL COMMENT '备注',
  `order` int NOT NULL COMMENT '顺序',
  `datasource_id` int NOT NULL COMMENT '数据源id',
  `db` varchar(255) NOT NULL COMMENT '数据库',
  `variables_id` int DEFAULT NULL COMMENT '变量id',
  `content` mediumtext NOT NULL COMMENT '内容',
  `context` mediumtext COMMENT '上下文',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_data_template_id_order_deleted` (`data_template_id`,`order`,`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb3 COMMENT='数据模板明细'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = launch_job   */
/******************************************/
CREATE TABLE `launch_job` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务名称',
  `productline_id` int NOT NULL COMMENT '生产线id',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '任务状态,0:未开始,1:进行中,2:成功,-1:异常',
  `start_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '任务开始时间',
  `end_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '任务结束时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='生产线运行任务'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = launch_job_detail   */
/******************************************/
CREATE TABLE `launch_job_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务明细名称',
  `job_id` int NOT NULL COMMENT '任务id',
  `worker_id` int NOT NULL COMMENT '工人id',
  `order` int NOT NULL COMMENT '顺序',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '任务状态,0:未开始,1:进行中,2:完成,-1:异常',
  `start_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '任务开始时间',
  `end_time` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '任务结束时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='生产线运行任务明细'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = msg_template   */
/******************************************/
CREATE TABLE `msg_template` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '消息模板名称',
  `type` tinyint NOT NULL DEFAULT '1' COMMENT '变量集类型,1: JSON',
  `template` mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '模板',
  `project_id` int NOT NULL COMMENT '项目id',
  `creator` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,null:未删除,!null:删除',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_deleted` (`name`,`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='记录消息模板'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = productline   */
/******************************************/
CREATE TABLE `productline` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '生产线名称',
  `project_id` int NOT NULL COMMENT '项目id',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  `disabled` tinyint DEFAULT '0' COMMENT '禁用状态,0:未禁用,1:已禁用',
  `favorite` int NOT NULL DEFAULT '0' COMMENT '收藏：0 : 否,1:是',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_deleted` (`name`,`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='生产线'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = productline_worker_relations   */
/******************************************/
CREATE TABLE `productline_worker_relations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `productline_id` int NOT NULL COMMENT '项目id',
  `worker_id` int NOT NULL COMMENT '工人id',
  `order` int NOT NULL COMMENT '工作顺序',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='生产线和工人的关联关系'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = project   */
/******************************************/
CREATE TABLE `project` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '项目名称',
  `creator` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '创建人',
  `disabled` tinyint DEFAULT '0' COMMENT '禁用状态,0:未禁用,1:已禁用',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,null:未删除,!null:删除',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_deleted` (`name`,`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='项目信息表'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = user   */
/******************************************/
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `uk_email_name` (`email`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='用户表存储用户信息相关数据'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = variables   */
/******************************************/
CREATE TABLE `variables` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '变量名称只能是英文且小写',
  `type` tinyint NOT NULL DEFAULT '1' COMMENT '变量集类型,1: JSON, 2:XML',
  `content` mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '变量内容',
  `project_id` int NOT NULL COMMENT '项目id',
  `creator` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,null:未删除,!null:删除',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_deleted` (`name`,`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='记录变量相关信息'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = worker   */
/******************************************/
CREATE TABLE `worker` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` tinyint NOT NULL COMMENT '工人类型,1：sql,2:rule,3:接口,4:混合',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '工人名称',
  `datasource_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '数据源Id',
  `project_id` int NOT NULL COMMENT '项目id',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  `disabled` tinyint DEFAULT '0' COMMENT '禁用状态,0:未禁用,1:已禁用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_deleted` (`name`,`deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='造数工人'
;

/******************************************/
/*   DatabaseName = mockfactory   */
/*   TableName = worker_content_message   */
/******************************************/
CREATE TABLE `worker_content_message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `worker_id` int NOT NULL COMMENT '工人id',
  `template_id` int NOT NULL COMMENT '消息模板id',
  `order` int NOT NULL COMMENT '消息顺序',
  `count` int NOT NULL COMMENT '发送次数',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `creator` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'unknown' COMMENT '创建人',
  `deleted` int NOT NULL DEFAULT '0' COMMENT '是否删除,0:未删除,>0:删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='消息类型工人的关联内容'
;
