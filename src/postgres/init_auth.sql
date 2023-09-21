CREATE SCHEMA auth;

CREATE TABLE auth.user
(
    id              bigserial,
    username        varchar(128),
    password        varchar(128),
    nickname        varchar(128),  -- 昵称
    phone           varchar(64),   -- 手机号通常11位，这里64位适应销号处理，13501174793_{userId}_removed
    removed         boolean,       -- 是否销号，true已销号，false正常
    email           varchar(128),
    avatar_url      varchar(1024), -- 头像地址
    platform        varchar(64),   -- 认证平台，如ma、admin
    source          varchar(64),   -- 用户来源，如book
    sharer_id       bigint,        -- 分享者userId
    client_platform varchar(128),  -- 设备平台，如ios，ios/android/windows/mac/devtools
    client_brand    varchar(128),  -- 设备品牌，如iPhone
    client_model    varchar(128),  -- 设备型号，如iPhone 11<iPhone12,1>，iPhone 6/7/8 Plus
    client_system   varchar(128),  -- 设备操作系统，如iOS 15.6.1，iOS 10.0.1
    unionid         varchar(128),  -- 微信用户union唯一id
    mp_openid       varchar(128),  -- 微信公众号用户openid
    ma_openid       varchar(128),  -- 微信小程序用户openid
    booksn          varchar(64),   -- 随书序列号
    description     varchar(4096),
    create_time     timestamp default now(),
    update_time     timestamp,
    motto           varchar(512),  -- 签名/座右铭
    height          int,           -- 身高，单位cm
    weight          float,         -- 体重，单位kg
    gender          int,           -- 性别，0男/1女
    birthday        timestamp,     -- 生日，年月日
    PRIMARY KEY (id),
    CONSTRAINT user_username_key UNIQUE (username),
    CONSTRAINT user_unionid_key UNIQUE (unionid)
);

CREATE TABLE auth.group
(
    id          bigserial,
    name        varchar,
    nickname    varchar,
    description varchar(4096),
    create_time timestamp,
    update_time timestamp,
    PRIMARY KEY (id),
    CONSTRAINT group_name_key UNIQUE (name)
);

CREATE TABLE auth.user_group
(
    user_id  bigint,
    group_id bigint,
    CONSTRAINT user_group_pkey PRIMARY KEY (user_id, group_id),
    CONSTRAINT fk_user_group_group_id FOREIGN KEY (group_id) REFERENCES auth.group (id),
    CONSTRAINT fk_user_group_user_id FOREIGN KEY (user_id) REFERENCES auth.user (id) on delete cascade -- 删除user时集联删除user.groups
);

-- ----------------------------
--  Table structure for menu
-- name 菜单名称，注意这里不作为显示在菜单栏的名称，显示在菜单栏的名称请看 meta_title
-- sort 前端显示顺序
-- redirect 当设置 noRedirect 的时候该路由在面包屑导航中不可被点击
-- component 当is_top_menu为true时，默认为Layout, 为false时，为菜单具体的组件路径
-- path 路径
-- meta_icon meta 中的图标名称 做为菜单栏显示图标的依据
-- meta_title meta 中的名称 做为菜单栏显示标题
-- meta_no_cache 如果设置为true，则不会被 <keep-alive> 缓存(默认 false)
-- meta_bread_crumb 如果设置为false，则不会在breadcrumb面包屑中显示
-- hidden 当设置 true 的时候该路由不会再侧边栏出现 如401，login等页面
-- always_show 当你一个路由下面的 children 声明的路由大于1个时，自动会变成嵌套的模式--如组件页面
--	只有一个时，会将那个子路由当做根路由显示在侧边栏--如引导页面
--	若你想不管路由下面的 children 声明的个数都显示你的根路由
--	你可以设置 alwaysShow: true，这样它就会忽略之前定义的规则，一直显示根路由
-- parent_id 菜单父节点
-- ----------------------------
CREATE TABLE auth.menu
(
    "id"                 bigserial,
    "name"               varchar(255),
    "sort"               integer,
    "redirect"           varchar(1024),
    "component"          varchar(1024),
    "path"               varchar(1024),
    "meta_icon"          varchar(1024),
    "meta_title"         varchar(1024),
    "meta_no_cache"      boolean default false,
    "meta_bread_crumb"   boolean default true,
    "hidden"             boolean default false,
    "always_show"        boolean default false,
    "parent_id"          int8,
    "udp_menu"           boolean default false,
    "description"        varchar(4096),
    "editable_udp_roles" varchar(1024),
    "create_date"        timestamp,
    PRIMARY KEY (id)
);

CREATE TABLE "auth"."group_menu"
(
    "group_id" int8 NOT NULL,
    "menu_id"  int8 NOT NULL,
    PRIMARY KEY (group_id, menu_id)
);

CREATE TABLE "auth"."user_domain"
(
    "user_id"   int8 NOT NULL,
    "domain_id" int8 NOT NULL,
    PRIMARY KEY (user_id, domain_id)
);

-- 查询user id对应的group name数组
CREATE or REPLACE FUNCTION group_names(integer) RETURNS varchar[] AS
$$
SELECT array_agg(g.name)
FROM auth.user_group ug
         LEFT JOIN auth.group g ON g.id = ug.group_id
WHERE ug.user_id = $1
$$ language sql;
-- select group_names(1);
