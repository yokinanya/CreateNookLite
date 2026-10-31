# 服务端部署

面向 Linux 的部署说明。已在 **Debian 13 / i5-1235U / 15.7GB** 上实测：
`Loading 91 mods` → `Done (21.1s)`，FATAL 0 条。

---

## 前置条件

| 组件 | 版本 | 说明 |
|---|---|---|
| Minecraft | 1.20.1 | |
| Forge | 47.4.16 | |
| Java | **17** | 必须是 17，Java 21 跑不了 Forge 1.20.1 |
| Python | 3.10+ | 运行 MCDReforged |
| MCDReforged | 2.16.2+ | 可选，不需要壳可以跳过 |

Java 17 安装（Debian，Zulu 源）：

```bash
sudo apt install -y zulu17-jdk-headless
```

或从 [Adoptium](https://adoptium.net/temurin/releases/?version=17) 下载解压。

---

## 目录结构

推荐布局（MCDR 根目录直接放服务端旁边）：

```
CreateNookLite/
├── start.sh              # 启动入口
├── config.yml            # MCDR 配置
├── .venv/                # MCDR 的 Python 环境
├── plugins/
└── server/               # Forge 服务端
    ├── mods/             # 91 个服务端模组
    ├── libraries/
    ├── server.properties
    ├── eula.txt
    └── world/
```

**关键**：`server.properties` 必须放在 `server/` 下。
MCDR 的 `working_directory` 指向 `server/`，放错位置 Forge 会生成一份默认配置覆盖你的调优。

---

## 部署步骤

### 1. 装 Forge

```bash
cd /path/to/CreateNookLite
curl -LO https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.16/forge-1.20.1-47.4.16-installer.jar
java -jar forge-1.20.1-47.4.16-installer.jar --installServer
echo "eula=true" > eula.txt
```

### 2. 放模组

**推荐**：用 Packwiz Installer，它会自动跳过客户端专用模组。

```bash
cd /path/to/CreateNookLite
curl -LO https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar

# -s server 表示只装服务端需要的
java -jar packwiz-installer-bootstrap.jar \
  -s server \
  https://raw.githubusercontent.com/yokinanya/CreateNookLite/main/pack.toml
```

这会把 91 个服务端模组下到 `mods/`，客户端专用的 22 个自动跳过。

**手动方式**：从 [Modrinth](https://modrinth.com/mods) 按
[MODLIST.md](../MODLIST.md) 逐个下载，注意跳过末尾那 22 个客户端专用模组。

**关键**：只放服务端需要的。`MODLIST.md` 末尾列了 22 个客户端专用模组
（Oculus、Embeddium、Colorwheel 等），**不要**放进去 —— 它们引用了客户端专用的
Minecraft 类，服务端加载会抛 `invalid dist DEDICATED_SERVER` 直接崩溃。

装完确认数量：

```bash
ls mods/*.jar | wc -l    # 应该是 91
```

### 3. 装 MCDReforged（可选）

```bash
cd CreateNookLite
python3 -m venv .venv
./.venv/bin/pip install mcdreforged
./.venv/bin/python -m mcdreforged init
```

然后编辑 `config.yml`：

```yaml
working_directory: /path/to/CreateNookLite/server
start_command: taskset -c 0-3 /usr/lib/jvm/zulu17/bin/java -Xms4G -Xmx4G \
  -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \
  @libraries/net/minecraftforge/forge/1.20.1-47.4.16/unix_args.txt nogui
handler: forge_handler
disable_console_thread: true
```

三个必改项：

| 项 | 值 | 原因 |
|---|---|---|
| `working_directory` | `.../server` | MCDR 要在这里找服务端 |
| `handler` | `forge_handler` | 解析 Forge 的日志格式 |
| `disable_console_thread` | `true` | 否则会和 MCSManager 抢 stdin |

### 4. 启动

```bash
./start.sh
```

`start.sh` 内容：

```bash
#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
export PATH=/usr/lib/jvm/zulu17/bin:$PATH
exec ./.venv/bin/python -m mcdreforged start
```

---

## 资源分配

### 内存

```
-Xms4G -Xmx4G
```

实测堆只用了 2.1GB，存活对象 594MB。4G 对 91 模组足够，
`-Xms` = `-Xmx` 避免堆动态扩张卡顿。实际 RSS 约 3-4GB。

### CPU

```bash
taskset -c 0-3 java ...
```

**这一步对混合架构 CPU 很重要。**

i5-1235U 是 2P+8E 架构：2 个性能核（4.4GHz）+ 8 个能效核（3.3GHz）。
Minecraft 主线程是单线程的，被调度到能效核上 TPS 会明显下降。
绑到 CPU 0-3（两个 P 核 + 超线程）能稳定吃到睿频。

在普通服务器（非大小核）上可以不加 `taskset`。

---

## server.properties 调优

关键项（针对低功耗 CPU + 模组服）：

```properties
# 性能 —— 视距是 TPS 头号杀手
view-distance=7
simulation-distance=5
entity-broadcast-range-percentage=70
sync-chunk-writes=false
max-tick-time=-1
use-native-transport=true

# 游戏性
difficulty=normal
max-players=10
spawn-protection=0
allow-flight=true

# 正版与白名单
online-mode=true
enforce-secure-profile=true
white-list=true
enforce-whitelist=true
```

**几个容易踩坑的项**

- `allow-flight=true` 必须开。包里带 Create Jetpack 和悬浮背包，
  玩家飞行时服务器会判定为「非法飞行」并踢人。
- `max-tick-time=-1` 必须设。默认 60000 意味着单次卡顿超过 60 秒直接崩服，
  模组服在区块生成时很容易触发。
- `online-mode` 和 `enforce-secure-profile` 要一起开或一起关。
  正版服开着，离线服关掉，混搭会导致聊天签名异常。

---

## 白名单与 OP

`whitelist.json`：

```json
[
  { "uuid": "玩家的正版UUID", "name": "玩家名" }
]
```

`ops.json`：

```json
[
  {
    "uuid": "玩家的正版UUID",
    "name": "玩家名",
    "level": 4,
    "bypassesPlayerLimit": true
  }
]
```

UUID 必须是正版 32 位无横线格式。可以用 Mojang API 校验：

```bash
curl "https://api.mojang.com/users/profiles/minecraft/玩家名"
```

或者在服务器开好后执行 `whitelist add 玩家名` 让它自己解析。

---

## RCON

```properties
enable-rcon=true
rcon.port=25575
rcon.password=随机密码
```

RCON 只监听本机回环。测试：

```bash
# 装 mcrcon 或任意 RCON 客户端
mcrcon -H 127.0.0.1 -P 25575 -p 密码 "list"
```

---

## MCSManager

如果用 MCSManager 管理，在实例配置里加：

```json
{
  "startCommand": "./start.sh",
  "stopCommand": "^c",
  "cwd": "/path/to/CreateNookLite",
  "runAs": "运行用户"
}
```

**停止命令必须用 `^c`，不能用 `stop`。**

原因：MCDR 用管道接管了 Forge 的 stdin，MCSManager 输入的 `stop`
到不了 Forge。而 MCDR 在 `disable_console_thread: true` 下不读 stdin，
只响应 SIGINT。`^c` 发的就是 SIGINT，MCDR 会转成 `stop` 发给服务端，
能正常保存世界后退出。

**`runAs` 建议填上**。不填的话 MCSManager 以 root 启动，
服务端生成的 `world/`、`logs/` 全是 root 属主，之后普通账号改配置会被拒。
注意 MCSManager 只降权启动，**不会帮你 chown**，所以改完要手动确认属主：

```bash
sudo chown -R 用户名:用户名 /path/to/CreateNookLite
```

---

## 已知问题

**删 world 后首次启动偶发崩溃**

```
NullPointerException: Registry entry not present: create:chocolate_bucket
```

这是 Create 的 `AllAdvancements` 在静态初始化时引用流体注册表的竞态。
只在删掉 `world/` 后第一次生成时可能出现，正常重启不会触发。
重跑一次即可，不需要改任何配置。

**模组下载慢**

服务器直连 Modrinth/CDN 可能只有十几 KB/s，走代理能快两个数量级：

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```
