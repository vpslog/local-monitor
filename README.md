# 本地节点延迟监控系统

## 简介
本项目用于本地到服务器的 Ping 延迟监控，助你检测本地真实的连接体验。

## 功能特点
- 多节点批量 Ping 监控，自动记录延迟数据
- 支持自定义节点列表（server.csv）
- 历史延迟数据可视化，支持 1小时/24小时/1周 多图展示

## 快速开始
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 配置节点列表：
   编辑 `server.csv`，格式如下：
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

## 主要文件说明
- `run.py`：主程序，负责数据采集和 Web 服务
- `db.py`：数据库操作，延迟数据存储与查询
- `nezha.py`: 哪吒面板交互
- `template.html`：前端页面，数据展示与交互
- `server.csv`：节点列表配置
- `requirements.txt`：依赖包列表


