# 本地节点延迟监控系统

## 简介
本项目用于本地到服务器的 Ping 延迟监控，助你检测本地真实的连接体验。

## 功能特点
- 多节点批量 Ping 监控，自动记录延迟数据
- 支持自定义节点列表（server.csv）
- 历史延迟数据可视化，支持 1小时/24小时/1周 多图展示

## Docker 部署
本项目已集成 GitHub Actions 自动构建并发布 Docker 镜像到 GitHub Container Registry（ghcr.io）。

### 配置服务器（从Nezha V1 获取）

```bash
docker pull ghcr.io/vpslog/local-monitor:latest
```


### 挂载数据库和 server.csv 并启动
```bash
docker run --rm \
  -v $(pwd)/local-monitor:/app/data \
  -e NEZHA_API_URL='XXXX' \
  -e NEZHA_USER='XXX' \
  -e NEZHA_PASSWORD='XXXX' \
  ghcr.io/vpslog/local-monitor:latest python3 nezha.py
```

> 说明：
> - `-v $(pwd)/local-monitor:/app/data` 挂载本地文件，数据持久化
> - `-e NEZHA_API_URL`、`-e NEZHA_USER`、`-e NEZHA_PASSWORD` 用于哪吒面板自动拉取服务器列表（如需自动生成 server.csv）。

### 运行容器

```bash
docker run -d \
  -v $(pwd)/local-monitor:/app/data \
  -p 6001:5000 \
  --name local-monitor \
  ghcr.io/vpslog/local-monitor:latest
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
