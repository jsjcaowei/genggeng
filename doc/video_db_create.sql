# --用户表
create table if not exists user
(
    user_id VARCHAR(64) not null DEFAULT '' comment '用户',
    phone   VARCHAR(64) not null DEFAULT '' comment '用户手机号',
    type    int  not null DEFAULT 0 comment '用户等级，类型',
    name    VARCHAR (512) not null DEFAULT '' comment '用户姓名',
    nick_name VARCHAR(512) not null DEFAULT '' comment '用户昵称',
    head_img varchar(1024) NOT NULL DEFAULT '' COMMENT '用户头像',
    status  int not null DEFAULT 1 comment '1有效用户，0失效用户',
    create_time timestamp not null default current_timestamp comment '创建时间',
    update_time timestamp not null default current_timestamp on update current_timestamp comment '最近修改时间',
    primary key (user_id),
    KEY (phone)
)engine=innodb default charset=utf8mb4 comment '用户表';



# 用户信息表
create table if not exists user_info
(
    user_id VARCHAR(64) not null DEFAULT '' comment '用户',
    email   VARCHAR(128) not null DEFAULT '' comment '邮箱',
    industry VARCHAR(128) not null DEFAULT '' comment '行业',
    position varchar(128) NOT NULL DEFAULT '' COMMENT '职位',
    company varchar(128) NOT NULL DEFAULT '' COMMENT '公司',
    weixin   varchar(64) NOT NULL DEFAULT '' COMMENT '微信号',
    prov_name varchar(64) NOT NULL DEFAULT '' COMMENT '所在省份',
    city_name varchar(64) NOT NULL DEFAULT '' COMMENT '所在城市',
    town_name varchar(64) NOT NULL DEFAULT '' COMMENT '所在乡镇',
    status  int not null DEFAULT 1 comment '1有效，0失效',
    create_time timestamp not null default current_timestamp comment '创建时间',
    update_time timestamp not null default current_timestamp on update current_timestamp comment '最近修改时间',
    primary key (user_id),
)engine=innodb default charset=utf8mb4 comment '用户信息表';



# video 视频表
create table if not exists user_info
(
    video_id int not null AUTO_INCREMENT  comment '视频id',
    ali_video_id   VARCHAR(128) not null DEFAULT '' comment '对应的阿里云视频id',
    size     float not null DEFAULT 1.0  comment '视频大小，以k为单位，',
    clarity  int not null DEFAULT 0 comment '清晰度，0高清，1标清',
    video_url    VARCHAR(256) not null DEFAULT '' comment '视频播放路径,使用播放凭时,可以不用赋值',
    play_info varchar(1024) NOT NULL DEFAULT '' COMMENT '对应阿里云的视频播放信息',
    status  int not null DEFAULT 1 comment '1有效，0失效',
    create_time timestamp not null default current_timestamp comment '创建时间',
    update_time timestamp not null default current_timestamp on update current_timestamp comment '最近修改时间',
    primary key (video_id)
)engine=innodb default charset=utf8mb4 comment '用户信息表';












