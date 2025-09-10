# 本地节点延迟监控系统

## 简介
本项目用于本地到服务器的 Ping 延迟监控，助你检测本地真实的连接体验。

## 功能特点
- 多节点批量 Ping 监控，自动记录延迟数据
- 支持自定义节点列表（server.csv）
- 历史延迟数据可视化，支持 1小时/24小时/1周 多图展示

## Docker 部署
本项目已集成 GitHub Actions 自动构建并发布 Docker 镜像到 GitHub Container Registry（ghcr.io）。

### 拉取镜像
```bash
docker pull ghcr.io/vpslog/local-monitor:latest
```


### 挂载数据库和 server.csv 并启动
```bash
docker run -d --name local-monitor \
   -v $(pwd)/local-monitor:/app/data \
   -e PING_INTERVAL=60 \
   -e NEZHA_API_URL=https://xxxx \
   -e NEZHA_USER=xxxx \
   -e NEZHA_PASSWORD=xxxxx \
   -p 5000:5000 \
   ghcr.io/<你的用户名>/local-monitor:latest
```
> 说明：
> - `-v $(pwd)/database.sqlite3:/app/database.sqlite3` 挂载本地数据库文件，数据持久化。
> - `-v $(pwd)/server.csv:/app/server.csv` 挂载节点列表配置。
> - `-e DATABASE_URL` 指定数据库路径。
> - `-e PING_INTERVAL` 设置 ping 间隔秒数。
> - `-e NEZHA_API_URL`、`-e NEZHA_USER`、`-e NEZHA_PASSWORD` 用于哪吒面板自动拉取服务器列表（如需自动生成 server.csv）。

### 生成/更新 server.csv（首次部署或节点变更时）
```bash
docker exec local-monitor python3 nezha.py
```
生成后可重启容器：
```bash
   如需本地开发，可在 data 目录添加 `data/.env` 文件，内容如下：
```


## 环境变量说明
- `DATABASE_URL`：sqlite3 数据库路径（建议挂载到本机）
- `PING_INTERVAL`：ping 间隔秒数
- `NEZHA_API_URL`：哪吒面板 API 地址（如 https://nezha.xxx.com）
- `NEZHA_USER`：哪吒面板用户名
- `NEZHA_PASSWORD`：哪吒面板密码（如有特殊字符建议加引号）

## 快速开始
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 配置节点列表：
   编辑 `data/server.csv`，格式如下：
   ```csv
   ip,name,desc
   1.2.3.4,节点A,描述A
   5.6.7.8,节点B,描述B
   ...
   ```
   或配置 `.env`后直接使用`python nezha.py`从 哪吒面板拉取服务器数据

3. 启动服务：
   ```bash
   python run.py
   ```

4. 浏览器访问 `http://localhost:5000` 查看监控界面。
