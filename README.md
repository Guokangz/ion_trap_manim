# Ion Trap Manim Animation

一个本地 Manim Community Edition 项目，用于中文三分钟展示 Paul ion trap
的基本囚禁图像：任意瞬间的四极势是马鞍形，而快速振荡可以产生时间平均的
有效赝势囚禁。

## 环境要求

- Manim Community Edition
- Python with `numpy`
- 中文字体：`Noto Sans CJK SC`

动画只使用 Manim 图形对象和 `Text`，不使用外部图片资源，也不依赖 MathTex/LaTeX。

## 渲染建议

普通预览建议用中等质量 `-qm`：

```bash
bash scripts/render_preview.sh SceneName
```

普通高清 MP4 可用 Manim 的 `-qh`：

```bash
bash scripts/render_mp4.sh SceneName
```

PPT 正式插入建议使用高质量 H.264 转码版本：

```bash
bash scripts/render_ppt_hq.sh SceneName
```

批量导出正式 PPT 四段的高质量版本：

```bash
bash scripts/render_all_ppt_hq.sh
```

导出正式四段并合成为一个完整高质量 MP4：

```bash
bash scripts/render_full_video.sh
```

GIF 只适合快速预览，不建议作为正式 PPT 素材：

```bash
bash scripts/render_gif.sh RodToRadialPotential
```

开发检查时，可以批量渲染较完整的分镜列表：

```bash
bash scripts/render_all.sh
```

`render_all.sh` 默认使用 `-qh`，偏开发检查用途，列表可以包含备用分镜。当前默认包含：`RodToRadialPotential`、`PotentialToSaddle`、`StaticSaddleEscape`、`DrivenSaddleComparison`、`PseudopotentialConfinement`。

`render_all_ppt_hq.sh` 默认只导出正式 PPT 四段：`RodToRadialPotential`、`PotentialToSaddle`、`DrivenSaddleComparison`、`PseudopotentialConfinement`。

PPT 高质量脚本会先用 Manim 输出 1080p、30 fps MP4，再转码为 `output/ppt_hq/*_PPT_HQ.mp4`。这些文件使用高质量 H.264，文件大小会比普通预览大，但通常仍适合插入 PPT。

分段 MP4 适合 PPT 分页控制节奏；完整 MP4 适合备用播放或单文件展示，输出为 `output/ppt_hq/IonTrap_FullTalk_PPT_HQ.mp4`。每个正式分镜的第一帧已设计为可用的 PPT 封面帧，避免插入 PowerPoint 后默认显示黑色播放块。

## Cleaning render outputs

Manim 渲染文件默认不会纳入 git。如需清理旧的预览、高清输出和 Python 缓存，可以运行：

```bash
bash scripts/clean_outputs.sh
```

## 独立分镜

每个 Scene 都可以独立渲染：

```bash
manim -qm --format mp4 scenes/ion_trap_intro.py RodTrap3D
manim -qm --format mp4 scenes/ion_trap_intro.py RodToRadialPotential
manim -qm --format mp4 scenes/ion_trap_intro.py PotentialToSaddle
manim -qm --format mp4 scenes/ion_trap_intro.py StaticSaddleEscape
manim -qm --format mp4 scenes/ion_trap_intro.py DrivenSaddleComparison
manim -qm --format mp4 scenes/ion_trap_intro.py PseudopotentialConfinement
manim -qm --format mp4 scenes/ion_trap_intro.py IonTrapDemo
```

## 分镜功能

`IonTrapDemo` 是简短合集预览，不作为正式 PPT 默认输出。正式 PPT 默认输出当前控制为四段：

1. `RodToRadialPotential`：从四极杆结构过渡到 xy 横截面，并淡入 `Φ(x,y) ∝ x² - y²` 的双曲线等势线。
2. `PotentialToSaddle`：从同一个二维四极势桥接帧开始，解释性过渡到三维马鞍势。
3. `DrivenSaddleComparison`：顺序展示低频翻转仍会逃逸，以及高频翻转下中心附近的有效约束趋势。
4. `PseudopotentialConfinement`：先短暂显示快速翻转马鞍势，再过渡到 `U_eff ∝ x² + y²` 的时间平均碗形赝势。

`RodTrap3D` 仍可单独渲染，用作备用的纯三维结构展示；默认正式批量渲染不包含它，以避免开头信息重复。
`StaticSaddleEscape` 是备用/可选分镜，代码保留；如果需要单独展示静止逃逸，可手动运行 `bash scripts/render_ppt_hq.sh StaticSaddleEscape`。

## 版式原则

每个分镜尽量保持固定结构：顶部标题、中间主图、底部一句核心说明。

如果发现文字重叠，应优先减少同屏文字或分阶段出现，而不是继续缩小字号。
中文说明尽量控制在一行或两行以内，PPT 正式版优先使用 `-qh` MP4。

## 物理说明

- 线性 Paul 阱的四根杆形成径向 RF 四极场。
- 相对的一对杆同相，另一对杆反相；不是“两根静电杆 + 两根 RF 杆”。
- 任意瞬间的四极势是马鞍形：一个方向聚焦，另一个方向发散。
- 高频驱动后可以得到时间平均意义下的有效束缚，即赝势。
- 真实系统的轴向 z 囚禁通常由端电极或分段 DC 电极提供。

为直观展示做的简化：

- 这不是 Mathieu 方程的数值仿真。
- 离子轨迹只是稳定束缚的示意，没有显式区分 micromotion 和 secular motion。
- 四根圆形杆电极是横截面示意，不是精确工程几何。
