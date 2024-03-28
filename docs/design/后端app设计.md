

# application & model & api
- django
  - model:
    - auth_user
    - auth_user_group
- common
  - model:
    - CustomUser 记录用户数据
    - Team 记录队伍数据
  - controller:
    - util.py 常用操作可以储存在这里
    - user.py 处理用户注册，登录，修改密码等针对user表的操作
    - team.py 处理用户创建、解散、加入、退出战队的行为

- rank
  - model:
    - first_kill 记录首杀数据
  - controller:
    - user.py 处理查询用户分数排名
    - team.py 处理查询队伍分数排名

- tasks
  - model:
    - task
    - answer_record
  - controller:
    - task.py 处理创建题目，删除题目操作
    - answer_record.py 处理用户答题操作
