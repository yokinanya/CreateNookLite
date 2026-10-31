轻量版机械动力 + 农夫乐事整合包。

参考 [Create-Delight-Remake](https://github.com/Jasons-impart/Create-Delight-Remake) 的思路，
把体量从 397 个模组收敛到 113 个。

## 版本信息

| | |
|---|---|
| Minecraft | 1.20.1 |
| Forge | 47.4.16 |
| 模组数 | 113（服务端加载 91） |
| 客户端内存 | 建议 4-6 GB |

## 怎么装

下载下面的 `CreateNookLite.mrpack`，导入启动器即可：

- **PCL2** → 版本管理 → 导入整合包
- **Prism Launcher** → Add Instance → Import from zip
- **HMCL** → 安装整合包

启动器会自动下载 Forge 和全部模组，不用手动装任何东西。

服务端部署见 [server/README.md](server/README.md)。

## 内容

- **机械动力**：Create 6.0.8 + 20 个扩展（铁路、附魔工业、厨房、物流、能源）
- **烹饪**：Farmer's Delight + 15 个 Delight 扩展 + Vinery / Candlelight / Brewin'
- **枪械**：TaCZ
- **探索**：Terralith / Structory / Explorify / Towns and Towers / Dungeons and Taverns
- **性能**：Embeddium / Oculus / Colorwheel / ModernFix / FerriteCore / ImmediatelyFast
- **生活质量**：Sophisticated Backpacks / Waystones / JEI / Jade / Quark / Supplementaries

完整清单见 [MODLIST.md](MODLIST.md)。

## 验证结果

服务端完整启动通过：

```
Loading 91 mods
Done (21.101s)! For help, type "help"
```

- 世界生成正常
- RCON 25575 端口实测可用
- 无 FATAL 错误
- 113 个模组 SHA 校验通过

## 已知问题

日志里有 4 条 `Couldn't parse data file`，来自 `culturaldelights` 的空占位配方，
不影响游戏。详见 [CHANGELOG.md](CHANGELOG.md)。
