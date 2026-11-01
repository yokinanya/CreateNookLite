<img src="icon.png" width="140" align="right" alt="Create Nook Lite">

# Create Nook Lite

轻量版机械动力 + 农夫乐事整合包。参考
[Create-Delight-Remake](https://github.com/Jasons-impart/Create-Delight-Remake)
的思路，但把体量收敛到 117 个模组。

![Minecraft](https://img.shields.io/badge/Minecraft-1.20.1-62b47a)
![Forge](https://img.shields.io/badge/Forge-47.4.16-d8a657)
![Mods](https://img.shields.io/badge/Mods-117-5aa9c9)
![License](https://img.shields.io/badge/License-MIT-blue)

<br clear="right">


## 这个包是什么

一个「Create 自动化 + 烹饪 + 轻度冒险」的中等体量整合包。
目标：**进得去、跑得动、玩得爽**。不是那种开局要看三小时攻略的深度魔改包。

适合这样的你：

- 想玩 Create 的产线自动化，但不想被 AE2、FTB 任务线、魔法系统淹没
- 想和朋友开个小服，10 人以内，普通电脑就能带
- 喜欢农夫乐事的烹饪系统，想有个完整的厨房玩法
- 偶尔想拿枪打点东西（TaCZ），但不需要一整套军械库

**实测环境**：服务端 93 个模组，`Done (21.1s)`，存活对象 594MB，
低功耗 CPU（i5-1235U）上稳定运行。

| | |
|---|---|
| Minecraft | **1.20.1** |
| Forge | **47.4.16** |
| 模组数 | **117**（服务端加载 93） |
| 客户端内存 | 建议 4-6 GB |

---

## 怎么装

### 客户端（推荐：直接用 mrpack）

从 [Releases](https://github.com/yokinanya/CreateNookLite/releases/latest) 页面
下载 `CreateNookLite.mrpack`，然后：

1. 导入启动器：
   - **PCL2** → 版本管理 → 导入整合包
   - **Prism Launcher** → Add Instance → Import from zip
   - **HMCL** → 安装整合包
2. 内存分配 **4-6 GB**
3. 启动

启动器会自动下载 Forge 47.4.16 和全部 117 个模组，不用手动装任何东西。

### 客户端（进阶：packwiz-installer，可自动更新）

适合想跟着包更新的场景。

1. 下载 [packwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar)
2. 放进 `.minecraft` 目录
3. 启动器 JVM 参数加：

```
-Dpackwiz.updateURL=https://raw.githubusercontent.com/yokinanya/CreateNookLite/master/pack.toml
```

完整启动参数：

```
-javaagent:packwiz-installer-bootstrap.jar
-Dpackwiz.bootstrapsMainClass=link.infra.packwiz.installer.Main
-Dpackwiz.updateURL=https://raw.githubusercontent.com/yokinanya/CreateNookLite/master/pack.toml
```

这样每次启动都会拉取最新的 `pack.toml`，自动同步模组增删。

### 服务端

服务端是 Linux 部署，完整步骤见 **[server/README.md](server/README.md)**，
包含 Forge 安装、MCDReforged 配置、MCSManager 接入、性能调优和已知问题。

快速开始：

```bash
# 1. 下载并安装 Forge
curl -LO https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.16/forge-1.20.1-47.4.16-installer.jar
java -jar forge-1.20.1-47.4.16-installer.jar --installServer
echo "eula=true" > eula.txt

# 2. 把 .mrpack 里的模组解压到 mods/，注意排除客户端专用模组

# 3. 启动
java -Xms4G -Xmx4G -XX:+UseG1GC \
  @libraries/net/minecraftforge/forge/1.20.1-47.4.16/unix_args.txt nogui
```

`server/server.properties` 是调好的配置模板，复制到服务端根目录即可。
里面 `allow-flight=true` 和 `max-tick-time=-1` 别改 ——
前者防止喷气背包被反作弊踢，后者防止卡顿直接崩服。

---

## 运行时要注意

### Java
需要 **Java 17**。启动器一般会自动处理；手动指定的话去
[Adoptium](https://adoptium.net/temurin/releases/?version=17) 下个 JDK 17。

### 内存建议

| 场景 | 内存 |
|---|---|
| 只玩原版内容 + Create | 4 GB |
| 开光影 | 5-6 GB |
| 多人联机 | 6 GB |

### 光影

包里带了 **Oculus**（光影加载器）和 **Colorwheel**（Create 与光影兼容）。
把光影包丢进 `shaderpacks/` 就能用。

Create 的机械结构在光影下需要 Colorwheel 才能正常渲染，已经装好了。

---

## 内容清单

### 机械动力（核心）

Create 本体 6.0.8，加 20 个扩展：

- **交通**：Steam 'n' Rails（铁路）、Jetpack（喷气背包）
- **工业**：Crafts & Additions（电力）、New Age（新能源）、
  Diesel Generators（柴油）、Solar Powered（太阳能）
- **物流**：Factory Controller（工厂控制）、FluidLogistics（流体）、
  Ore Excavation（矿脉开采）、Utilities（实用工具）
- **厨房**：Central Kitchen、Slice & Dice、Garnished、Confectionery
- **建筑**：Deco、Copycats+、Connected（连接件）
- **进阶**：Enchantment Industry（附魔工业）、Stuff 'N Additions、Dragons Plus

### 烹饪（农夫乐事系）

Farmer's Delight 本体，加 Nether / End / Oceanic / Miner's / Corn /
Cultural / Cuisine Delight，再加 Vinery、Candlelight、Brewin' And Chewin'、
Neapolitan、Crate Delight 等生活向扩展。

### 枪械

TaCZ（Timeless and Classics Zero）本体。不带额外枪包，保持轻量。

### 探索

- **地形**：Terralith（主世界地形重制）
- **建筑**：Structory、Explorify、Towns and Towers（村庄扩展）
- **冒险**：Dungeons and Taverns（地牢与酒馆）
- **辅助**：Nature's Compass、Explorer's Compass（定位工具）

### 生活质量

Sophisticated Backpacks（背包）、Waystones（传送石）、Jade（方块信息）、
JEI（配方查询）、AppleSkin（饱食度）、Mouse Tweaks、Controlling（按键搜索）、
Crafting Tweaks、Clumps（经验合并）、Toast Control、Comforts（睡袋）、
Carry On（搬箱子）、Quark（内容扩展）、Supplementaries、
Better Advancements、Traveler's Titles、Shoulder Surfing、Sound Physics。

### 性能

Embeddium + Oculus + Colorwheel（光影三件套）、Entity Culling、
ModernFix、FerriteCore、ImmediatelyFast、Memory Leak Fix、Packet Fixer、
Neruina（实体崩溃修复）、Crash Assistant（崩溃诊断）。

---

## 设计取舍

这个包刻意没有装下面这些内容：

| 类别 | 常见选择 | 为什么不要 |
|---|---|---|
| 魔法 | Iron's Spells、Tetra、Apotheosis | 体量大，和 Create 玩法重叠少 |
| 大型生物 | Alex's Mobs、Ice and Fire、Cataclysm | 内容量巨大，主要拖累性能 |
| 科技线 | AE2、MEGA Cells | 和 Create 物流功能重复 |
| 任务线 | FTB Quests + KubeJS 深度魔改 | 轻量包不需要 |
| 季节系统 | Ecliptic Seasons | 非核心体验 |
| 地形放大 | Tectonic | 与 Terralith 功能重叠，且区块生成更慢 |

思路是：**同类玩法只保留一个最好的实现**，而不是把能装的全装上。

---

## 项目结构

```
CreateNookLite/
├── mods/              # 117 个 .pw.toml（packwiz 元数据，不含 jar）
├── server/            # 服务端部署说明与配置模板
├── dist/              # 导出的 .mrpack（可直接导入启动器）
├── pack.toml          # packwiz 主配置
├── index.toml         # packwiz 文件索引
├── MODLIST.md         # 完整模组清单
├── CHANGELOG.md       # 版本记录
└── LICENSE
```

## 二次开发

用 [packwiz](https://packwiz.infra.link/) 管理模组：

```bash
# 加模组
packwiz modrinth add <slug>

# 更新全部模组
packwiz update --all

# 改完文件后刷新索引
packwiz refresh

# 重新导出 mrpack
packwiz modrinth export -o dist/CreateNookLite-1.0.0.mrpack
```

国内网络建议先设代理，否则从 Modrinth 拉包会非常慢：

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```