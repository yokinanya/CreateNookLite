# Create Nook Lite — 模组清单

Minecraft 1.20.1 / Forge 47.4.16

**总计 113 个模组**：92 个双端通用 + 21 个客户端专用（服务端不加载）。

---

## 机械动力（21）

Create 6.0.8（本体）· Create Crafts & Additions · Create: Steam 'n' Rails ·
Create: Connected · Create: Copycats+ · Create Deco · Create: Enchantment Industry ·
Create: Central Kitchen · Create Slice & Dice · Create: Garnished ·
Create Confectionery · Create Ore Excavation · Create Utilities · Create: New Age ·
Create: Diesel Generators · Create: Solar Powered · Create Jetpack ·
Create: Factory Controller · Create: FluidLogistics ·
Create Stuff 'N Additions · Create: Dragons Plus

## 烹饪（18）

Farmer's Delight（本体）· Farmer's Respite · Cultural Delights · Corn Delight ·
Nether's Delight · End's Delight · Oceanic Delight · Cuisine Delight ·
Miner's Delight · Neapolitan · Festival Delicacies · Vintage Delight ·
Brewin' And Chewin' · Crate Delight · Chef's Delight ·
[Let's Do] Vinery · [Let's Do] Candlelight · [Let's Do] API

## 枪械（1）

TaCZ — Timeless and Classics Zero 1.1.8-hotfix2

## 探索与世界生成（9）

Terralith · Structory · Explorify · Dungeons and Taverns · Towns and Towers ·
Nature's Compass · Explorer's Compass · YUNG's API

## 性能与光影（11）

Embeddium · Entity Culling · ModernFix · FerriteCore ·
Memory Leak Fix · Packet Fixer · Neruina（实体崩溃修复）· Crash Assistant ·
Oculus（光影加载器）· Colorwheel（Create × 光影兼容）· Colorwheel Patcher

## 生活质量与界面（34）

**背包与存储**：Sophisticated Backpacks · Sophisticated Core · Functional Storage

**导航与信息**：Waystones · Jade · JEI · Just Enough Breeding · JEED · AppleSkin

**操作手感**：Mouse Tweaks · Controlling · Searchables · Clumps ·
Toast Control · Crafting Tweaks · Comforts · Carry On

**内容扩展**：Quark · Supplementaries · No Chat Reports

**界面美化**：FancyMenu · Drippy Loading Screen · Prism · Iceberg · Konkrete ·
Better Advancements · Advancement Plaques · Item Borders · Traveler's Titles ·
Shoulder Surfing Reloaded · CustomSkinLoader · Sound Physics Remastered ·
[EMF] Entity Model Features · [ETF] Entity Texture Features

## 前置库（19）

Architectury API · Balm · Blueprint · Bookshelf · Cloth Config API ·
Cristel Lib · Curios API · Geckolib · Kotlin for Forge · Melody ·
MezzConfig · Moonlight Lib · Mysterious Mountain Lib · Placebo · Puzzles Lib ·
Resourceful Lib · Resourceful Config · Titanium · YetAnotherConfigLib · Zeta

---

## 客户端专用（21 个，服务端不加载）

[EMF] Entity Model Features · [ETF] Entity Texture Features ·
Advancement Plaques · Better Advancements · Colorwheel · Colorwheel Patcher ·
Controlling · Crash Assistant · CustomSkinLoader · Drippy Loading Screen ·
Embeddium · Entity Culling · ImmediatelyFast · Item Borders ·
Just Enough Effect Descriptions · Mouse Tweaks · Oculus · Prism ·
Searchables · Shoulder Surfing Reloaded · Toast Control · Traveler's Titles

> 服务端部署时**不要**把这些放进 `server/mods/`。它们引用了客户端专用的
> Minecraft 类，在服务端加载会直接抛 `invalid dist DEDICATED_SERVER` 导致启动崩溃。

---

## 性能实测

在 i5-1235U（2P+8E / 15.7GB）+ Debian 13 环境下的实测数据：

| 指标 | 数值 |
|---|---|
| 服务端模组数 | 92 |
| 启动耗时 | 21.1s |
| 堆使用 | 2.1 GB / 4 GB |
| 存活对象 | 594 MB |
| FATAL 错误 | 0 |

### 堆占用构成

用 `jmap -histo:live` 抓的存活对象分布：

| 类别 | 占用 | 说明 |
|---|---|---|
| `[B` byte 数组 | 194 MB | 主要是资源文件与网络缓冲 |
| BlockState | 41.8 MB | 47 万个方块状态，内容量的必然代价 |
| zip 索引 | 14.8 MB | 113 个模组 jar 的文件索引 |
| 结构模板 | 14.3 MB | 世界生成结构缓存 |
| datafixer | 5.5 MB | Mojang 数据修复器（原版开销） |

**一个反直觉的结论**：模组 jar 的体积和内存占用几乎无关。

- Create 的 jar 19MB，实际堆占用只有 0.8MB
- TaCZ 的 jar 55MB，堆占用 0.1MB
- JEI 的 jar 4.6MB，堆占用 0.03MB

jar 大是因为里面装的是贴图、模型、音效等资源文件，加载时只是引用，不占堆。
真正吃内存的是**方块状态总量**和**模组数量本身带来的 jar 索引**。

所以想进一步降内存，方向是砍内容量，而不是找某个「吃内存的模组」。
