-- 创建数据库
CREATE database if not exists cm DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
-- 添加超级用户
INSERT INTO user(username, pwd, create_time,is_delete) VALUES ('coco', 'e10adc3949ba59abbe56e057f20f883e', now(),0);

-- 添加超级管理员
INSERT INTO role(rolename) VALUES ('超级管理员');
INSERT INTO role(rolename) VALUES ('管理员');

-- 为用户1添加角色
INSERT INTO user_roles(user_id, role_id) VALUES (1,1);

-- 添加一辆车
INSERT INTO car(VIN) VALUES ('LDP53A962KC095022');

-- 权限添加
insert into permission(url, title) VALUES ('/CAN/show/', 'CAN数据展示页面');
insert into permission(url, title) VALUES ('/CAN/can_search/', 'CAN数据搜索');
insert into permission(url, title) VALUES ('/CAN/analysis_data/', 'CAN数据解析');
insert into permission(url, title) VALUES ('/CAN/test/', 'CAN数据json');
insert into permission(url, title) VALUES ('/car/manage/', '车辆管理页面');
insert into permission(url, title) VALUES ('/car/car_add/', '车辆添加功能');
insert into permission(url, title) VALUES ('/car/car_edit/', '车辆编辑功能');
insert into permission(url, title) VALUES ('/car/car_del/', '车辆删除功能');
insert into permission(url, title) VALUES ('/car/car_search/', '车辆查询功能');
insert into permission(url, title) VALUES ('/car/car_upload/', '车辆上传功能');
insert into permission(url, title) VALUES ('/car/car_download/', '车辆模板下载功能');
insert into permission(url, title) VALUES ('/car/car_index/', '车辆监控页面');
insert into permission(url, title) VALUES ('/car/car_monitor/', '车辆监控功能');
insert into permission(url, title) VALUES ('/doctor/doctor/', '医疗设备监控页面');
insert into permission(url, title) VALUES ('/doctor/drug_socket/', '医疗设备监控功能');
insert into permission(url, title) VALUES ('/doctor/analysis_doctor/', '医疗设备解析功能');
insert into permission(url, title) VALUES ('/doctor/doctor_download/', '医疗设备数据下载页面');
insert into permission(url, title) VALUES ('/fence/index/', '电子围栏页面');
insert into permission(url, title) VALUES ('/index/index/', '主页显示');
insert into permission(url, title) VALUES ('/index/map/', '地图页面显示');
insert into permission(url, title) VALUES ('/index/search/', '搜索车辆位置');
insert into permission(url, title) VALUES ('/index/chat/', '动态返回数据');
insert into permission(url, title) VALUES ('/lock/lock/', '解锁车页面显示');
insert into permission(url, title) VALUES ('/lock/llock/', '锁车功能');
insert into permission(url, title) VALUES ('/lock/unlock/', '解锁功能');
insert into permission(url, title) VALUES ('/lock/check_status/', '查询车辆状态');
insert into permission(url, title) VALUES ('/lock/search/', '查询车辆');
insert into permission(url, title) VALUES ('/machine/index/', '设备页面显示');
insert into permission(url, title) VALUES ('/machine/get_machine/', '设备列表');
insert into permission(url, title) VALUES ('/machine/machine_edit/', '设备编辑功能');
insert into permission(url, title) VALUES ('/machine/machine_del/', '设备删除功能');
insert into permission(url, title) VALUES ('/machine/machine_add/', '添加设备功能');
insert into permission(url, title) VALUES ('/machine/machine_download/', '设备下载功能');
insert into permission(url, title) VALUES ('/machine/machine_upload/', '设备上传功能');
insert into permission(url, title) VALUES ('/playback/back_video/', '轨迹回放页面显示');
insert into permission(url, title) VALUES ('/playback/search/', '车辆轨迹搜索');
insert into permission(url, title) VALUES ('/updt/up/', '车辆升级页面显示和编辑升级功能');
insert into permission(url, title) VALUES ('/updt/get_users/', '车辆升级列表');
insert into permission(url, title) VALUES ('/user/login/', '用户登录页面和登录功能');
insert into permission(url, title) VALUES ('/user/logout/', '注销功能');
insert into permission(url, title) VALUES ('/user/manage/', '用户管理');
insert into permission(url, title) VALUES ('/user/member_add/', '用户添加功能');
insert into permission(url, title) VALUES ('/user/edit/', '用户编辑功能');
insert into permission(url, title) VALUES ('/user/member_del/', '删除用户功能');
insert into permission(url, title) VALUES ('/user/member_search/', '查找用户功能');

-- 插入角色权限
insert into role_permissions(role_id, permission_id) VALUES
(1,1),
(1,2),
(1,3),
(1,4),
(1,5),
(1,6),
(1,7),
(1,8),
(1,9),
(1,10),
(1,11),
(1,12),
(1,13),
(1,14),
(1,15),
(1,16),
(1,17),
(1,18),
(1,19),
(1,20),
(1,21),
(1,22),
(1,23),
(1,24),
(1,25),
(1,26),
(1,27),
(1,28),
(1,29),
(1,30),
(1,31),
(1,32),
(1,33),
(1,34),
(1,35),
(1,36),
(1,37),
(1,38),
(1,39),
(1,40),
(1,41),
(1,42),
(1,43),
(1,44),
(1,45);

-- 医疗管理员权限
insert into role_permissions(role_id, permission_id) VALUES
(2,1),
(2,2),
(2,3),
(2,4),
(2,14),
(2,15),
(2,16),
(2,17),
(2,19),
(2,20),
(2,21),
(2,22),
(2,39),
(2,40);