# django-project-lite 
*** 
## 开发
- 复制 `setting_production.py` 为 `setting.py`, 并配置对应内容
- python manage.py startapp xxx 创建应用
- 将xxx文件夹移动到apps文件夹下
- 配置urls.py
- 将app添加到`setting.py`中的`INSTALLED_APPS`

## 部署
- 服务器上安装 docker 和 docker-compose
- 将 `.env.example` 复制到 `.env` 中，填写对应配置内容
- 执行 `docker-compose up -d --build` 构建并启动项目
- 首次启动后,执行 `docker-compose exec web bash` 进入 web 容器
   - 若需要收集静态文件 `python manage.py collectstatic --no-input`
   - 迁移数据库 `python manage.py makemigrations`
   - 迁移数据库 `python manage.py migrate` 
