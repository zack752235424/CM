-- 添加超级用户
INSERT INTO user(username, pwd, create_time) VALUES ('coco', 'e10adc3949ba59abbe56e057f20f883e', now());

-- 添加超级管理员
INSERT INTO role(rolename) VALUES ('超级管理员');
INSERT INTO role(rolename) VALUES ('管理员');

-- 为用户1添加角色
INSERT INTO user_roles(user_id, role_id) VALUES (1,1);

-- 添加一辆车
INSERT INTO car(VIN) VALUES ('LDP53A962KC095022');