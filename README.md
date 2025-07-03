# 实时地震观测器 (Real-time Earthquake Viewer)

> [!IMPORTANT]
> **重要**
> 自 v1.6 起，开始使用自建的云变量服务器。伴随此变更，我们制定了服务条款和隐私政策。请查阅 [服务条款与隐私政策](terms.md)。
> 在 [Scratch 版本](https://scratch.mit.edu/projects/636244032) 和 [TurboWarp 版本](https://turbowarp.org/636244032) 中，将分别适用 [Scratch 的隐私政策](https://scratch.mit.edu/privacy_policy) 和 [TurboWarp 的隐私政策](https://turbowarp.org/privacy.html)。

> [!NOTE]
> **说明**
> 此应用程序是使用 [Turbowarp Packager](https://packager.turbowarp.org/#636244032) 将 Scratch 上创建的 [实时地震观测器](https://scratch.mit.edu/projects/636244032) 打包而成的。
> 由于该项目在 Scratch 上共享，位于 [/assets](https://github.com/kotoho7/scratch-realtime-earthquake-viewer-page/tree/main/assets) 目录下的图像和音频资源遵循 [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/deed.ja) 许可协议。

## 概述

可以实时浏览地震和海啸信息。
基本无需操作，能够全自动显示实时接收到的信息。

通过应用程序内的不同标签页，可以查看以下信息：

*   **地震信息**
    显示地震发生后数分钟内由气象厅发布的 **震度速报**、**震源信息**、**地震信息** 和 **长周期地震动信息**，并进行实时更新。这些地震信息与电视或气象厅官网上可查看的地震信息相同。
    除最新地震外，还可以查看过去9次的地震记录。

*   **实时信息 (紧急地震速报)**
    显示地震发生后，由气象厅立即发布的 **紧急地震速报（预报）** 以及基于防灾科学技术研究所强震监测数据的 **实时震度**。
    这些信息 **实时性极高**，但请注意它们包含预测值或等效值，因此 **仅供参考**。

*   **海啸预报·海啸观测信息**
    显示伴随地震等事件由气象厅发布的 **大海啸警报**、**海啸警报**、**海啸注意报**、**海啸预报**，以及实际观测到海啸时的 **海啸观测相关信息**，并进行实时更新。
    可以查看各地的海啸预测高度、预计到达时间以及观测到的海啸高度。

此应用程序使用的气象厅实时电文数据，主要从 [Project DM-D.S.S (dmdata.jp)](https://dmdata.jp/) 接收。
通过 WebSocket 与服务器保持常时连接，能够即时接收气象厅发布的信息。

## 使用方法·安装方法

作为 Web 应用程序，只需访问 [网站](https://kotoho7.github.io/scratch-realtime-earthquake-viewer-page/) 即可使用。

此外，它支持 PWA（渐进式 Web 应用），因此可以像原生应用一样安装到设备上。
（并非所有设备和浏览器都支持此功能）

*   **桌面版 Chrome 浏览器**
    地址栏中的安装按钮 或 菜单 → 保存与共享 → 安装

*   **iOS 设备**
    共享 → 添加到主屏幕

*   **Android 设备**
    安装横幅 或 菜单 → 添加到主屏幕

## 其他

### 关于在直播或视频中使用

在直播或视频等中使用此应用程序显示的画面时，无需特别获取单独许可。

> [!WARNING]
> **警告**
> 但是，无法保证其运行的稳定性和可靠性，请用户自行承担使用风险。

### 联系咨询

有关此项目的咨询，可以通过以下渠道进行：

*   [创作者 X (原 Twitter)](https://twitter.com/kotoho76)
*   [Scratch 项目页面](https://scratch.mit.edu/projects/636244032)
*   [YouTube 社区帖子](https://www.youtube.com/post/UgkxGV7Jutqt9kMEByTHdihpdSBVYzcl0_Ue)

## 关于紧急地震速报的注意事项

在此项目中，会显示面向高级用户的 **紧急地震速报（预报）**。请基于以下特点活用信息：

*   信息在地震发生后数秒内生成，因此可能出现误报。
*   地震检测后的最初信息，其震源、震级和预测震度的精度可能较低。
*   通常情况下，预估震度也存在约1个震度等级的误差。
*   对于深度超过150公里的地震，不会发布预测最大震度（※ 有时会根据实际摇晃情况发布）。

## 应用程序内使用信息的来源

*   气象厅 紧急地震速报 (已获得再分发许可) & 地震信息 & 海啸信息
    [Project DM(Disaster Mitigation)-Data Send Service](https://dmdata.jp/docs/telegrams/)

*   地震信息更新 (至2天前)
    [气象厅 震度数据库检索](https://www.data.jma.go.jp/svd/eqdb/data/shindo/)

*   (实时震度)
    [防灾科学技术研究所 长周期地震动监测](https://www.lmoni.bosai.go.jp/monitor/)

*   (海底地震计)
    [海洋状况显示系统(海しる) 强震动信息](https://www.msil.go.jp/)

## 鸣谢 (Credits)

### 制作过程中参考的文章

*   [使用多项式插值从强震监测图像中确定数值数据](https://qiita.com/NoneType1/items/a4d2cf932e20b56ca444)

### 日本地图

*   [气象厅 预报区等 GIS 数据](https://www.data.jma.go.jp/developer/gis.html)
*   [国土交通省 国土数值信息 湖泊数据](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-W09-v2_2.html)

### 世界地图

*   [Natural Earth 1:10m Cultural Vectors (Japan POV)](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/)
*   [NOAA ETOPO](https://www.ngdc.noaa.gov/mgg/global/)

### 字体

*   [Akshar](https://fonts.google.com/specimen/Akshar)
*   [BIZ UDPGothic](https://fonts.google.com/specimen/BIZ+UDPGothic)
    ※ 两者均遵循 SIL Open Font License

### 音效

*   [OtoLogic 新闻 提示音](https://otologic.jp/free/se/news-accent01.html)

※ 音效的选择参考了 [BSC24 地震警戒放送２４时](https://ch.nicovideo.jp/bousai-share)。
※ 摇晃检测音效参考了 [JQuake](https://jquake.net/) 的音效制作。
