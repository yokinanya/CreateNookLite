# 版本记录

## 1.1.0

### 新增

| 模组 | 侧 | 说明 |
|---|---|---|
| **Xaero's Minimap** | 客户端 | 小地图，显示地形和实体 |
| **Xaero's World Map** | 客户端 | 世界地图，与小地图共享路径点 |
| **LetMeClickAndSend** | 客户端 | 修复 1.19.1+ 的点击事件限制 |
| **LetMeClickAndSendForServer** | 服务端 | 同上，服务端版让玩家不必装客户端模组 |
| **GJEB** | 客户端 | 亮度滑块上限从 100% 提到 1000% |

**关于点击事件**：Minecraft 1.19.1 起，`run_command` 点击事件只接受以 `/`
开头的命令。MCDR 的插件提示发的是 `!!MCDR ...`，原版客户端会直接忽略，
表现为「点击没反应」。装了这两个模组即可恢复。

### 性能优化

关闭了 Forge 的全局版本检查（`config/fml.toml` 的 `versionCheck = false`）。

原来每次启动会发 28 条外部请求（14 个模组 × 2），国内网络下大量超时，
显著拖慢启动。关掉后不再有 `Failed to process update information` 刷屏。

> 部分模组（Supplementaries、Quark 等）自带独立检查，无法通过配置关闭，
> 仍会尝试访问外网。这类请求是异步的，不影响启动。

### 模组数

118 个：92 双端 + 25 客户端 + 1 服务端。

---

## 1.0.0

首个版本。

### 内容

| 模块 | 内容 |
|---|---|
| 机械动力 | Create 6.0.8 + 20 个扩展 |
| 烹饪 | Farmer's Delight + 15 个 Delight 扩展 + Vinery / Candlelight / Brewin' |
| 枪械 | TaCZ 1.1.8-hotfix2 |
| 探索 | Terralith / Structory / Explorify / Towns and Towers / Dungeons and Taverns |
| 性能 | Embeddium / Oculus / Colorwheel / ModernFix / FerriteCore / Entity Culling |
| 生活质量 | Sophisticated Backpacks / Waystones / JEI / Jade / Quark / Supplementaries |

共 113 个模组，服务端加载 92 个。

### 验证

服务端完整启动通过：

```
Loading 92 mods
Done (21.101s)! For help, type "help"
```

- 世界生成正常
- 25565 端口正常监听
- RCON 25575 端口正常，`list` / `whitelist list` / `seed` 命令实测可用
- 无 FATAL 错误
- 113 个模组文件 SHA 校验通过

### 已知问题

**日志里的无害警告**

- `Couldn't parse data file` 4 条，来自 `culturaldelights` 的空占位配方文件
  （`minecraft:recipes/` 下的 mushroom_stew、beetroot_soup 等）。
  不影响游戏，这几条原版炖菜配方保持原样。
- `Couldn't load tag` 若干条，来自 `createutilities` 和 `vintagedelight`
  引用了不存在的 tag 成员，属于模组自身的可选兼容项。

**删 world 后首次启动偶发崩溃**

```
NullPointerException: Registry entry not present: create:chocolate_bucket
```

Create 的 `AllAdvancements` 在静态初始化时引用流体注册表的竞态。
只在删掉 `world/` 后第一次生成时可能出现，正常重启不会触发。
重跑一次即可，不需要改配置。

### 排除的模组

以下几类内容经过权衡后**没有**纳入本包：

| 模组 | 排除原因 |
|---|---|
| Iron's Spells、Tetra、Apotheosis | 魔法系统体量大，与 Create 玩法重叠少 |
| Alex's Mobs、Alex's Caves、Ice and Fire、Cataclysm | 内容量巨大，主要拖累性能 |
| AE2、MEGA Cells、ExtendedAE | 与 Create 物流功能重复 |
| FTB Quests + KubeJS 魔改 | 轻量包不需要任务线 |
| Tectonic | 地形放大，与 Terralith 功能重叠，且区块生成更慢 |
| Create: Structures | 仅少量 Create 风格建筑，内容价值低 |
| YUNG's Better Mineshafts / Dungeons / Strongholds | 结构数据量较大，收益不匹配 |
| Incendium、Nullscape | 下界与末地改造，非核心体验 |
| Create: Bigger Storage | 基于 Create 5 API 编译，与 Create 6 冲突，会导致服务端崩溃 |
| ImmediatelyFast | 只认 Iris 旧包名 `net.coderbot`，与 Oculus 的 `net.irisshaders` 不兼容，启动即崩 |
| Ecliptic Seasons、SeasonHud | 季节系统非核心体验 |
