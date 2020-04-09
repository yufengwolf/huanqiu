#Spider Project
----

##部署与运行

* 从svn下载最新代码
* 切换到项目目录（main.py所在目录）
* 安装项目依赖
	pip3 install -r requirements.txt
* 直接运行项目
	python3 runner.py
	
* 我一般使用 screen 在不同的终端运行，也可以放在背景运行。


##修改數據庫
数据库配置写在 sina/util.py mysqlObj 初始化函数中，替换新数据库即可。

数据库表

CREATE TABLE `tb_article` (
  `article_id` char(32) CHARACTER SET utf8 NOT NULL COMMENT '文章编号',
  `medium_id` int(11) DEFAULT NULL COMMENT '媒体编号',
  `url` text CHARACTER SET utf8 COMMENT '文章地址',
  `author` varchar(48) DEFAULT NULL COMMENT '文章作者',
  `subject` varchar(255) DEFAULT NULL COMMENT '文章标题',
  `content` text COMMENT '文章内容',
  `read_count` int(11) DEFAULT NULL COMMENT '阅读数',
  `comment_count` int(11) DEFAULT NULL COMMENT '评论数',
  `forward_count` int(11) DEFAULT NULL COMMENT '转发数',
  `like_count` int(11) DEFAULT NULL COMMENT '点赞数',
  `issue_time` timestamp NULL DEFAULT NULL COMMENT '发布时间',
  `crawl_ip` varchar(15) CHARACTER SET utf8 DEFAULT NULL COMMENT '采集IP',
  `crawl_time` timestamp NULL DEFAULT NULL COMMENT '采集时间',
  `clean_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '清洗状态',
  `clean_time` timestamp NULL DEFAULT NULL COMMENT '清洗时间',
  `source` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '来源',
  PRIMARY KEY (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tb_request` (
  `id` char(32) NOT NULL,
  `url` text,
  `status` int(11) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
