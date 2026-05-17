from manim import *
import numpy as np


BACKGROUND = "#0f172a"
TEXT_COLOR = "#f1f5f9"
MUTED_TEXT = "#94a3b8"
ION_COLOR = YELLOW
PLUS_COLOR = RED_C
MINUS_COLOR = BLUE_C
CJK_FONT = "Noto Sans CJK SC"

TITLE_WIDTH = 11.6
CAPTION_WIDTH = 12.2


def cn_text(content, font_size=30, color=WHITE, **kwargs):
    return Text(content, font=CJK_FONT, font_size=font_size, color=color, **kwargs)


def fit_width(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def scene_title(content):
    title = cn_text(content, font_size=32, color=TEXT_COLOR)
    fit_width(title, TITLE_WIDTH)
    return title.to_edge(UP, buff=0.46)


def bottom_caption(content):
    caption = cn_text(content, font_size=24, color=MUTED_TEXT)
    fit_width(caption, CAPTION_WIDTH)
    return caption.to_edge(DOWN, buff=0.50)


def prepare_fixed_frame(scene, *mobjects):
    if hasattr(scene.camera, "add_fixed_in_frame_mobjects"):
        scene.camera.add_fixed_in_frame_mobjects(*mobjects)


def release_fixed_frame(scene, *mobjects):
    if hasattr(scene.camera, "remove_fixed_in_frame_mobjects"):
        scene.camera.remove_fixed_in_frame_mobjects(*mobjects)


def set_dark_background(scene):
    scene.camera.background_color = BACKGROUND


def add_opening_keyframe(scene, *mobjects, pause=0.2):
    visible = [mob for mob in mobjects if mob is not None]
    if visible:
        scene.add(*visible)
    scene.wait(pause)


def fade_out_and_clear(scene, *mobjects, fixed_mobjects=()):
    visible = [mob for mob in mobjects if mob is not None]
    if visible:
        scene.play(*[FadeOut(mob) for mob in visible], run_time=0.5)
    if fixed_mobjects:
        release_fixed_frame(scene, *fixed_mobjects)
    scene.clear()


def make_rod_3d_parts(rod_offset=1.3, rod_radius=0.14, rod_length=6.2):
    def make_rod(position, color):
        rod = Cylinder(
            radius=rod_radius,
            height=rod_length,
            direction=OUT,
            resolution=(24, 12),
            fill_color=color,
            fill_opacity=0.78,
            stroke_width=0,
        )
        rod.move_to(position)
        return rod

    rods = VGroup(
        make_rod(np.array([-rod_offset, 0.0, 0.0]), PLUS_COLOR),
        make_rod(np.array([rod_offset, 0.0, 0.0]), PLUS_COLOR),
        make_rod(np.array([0.0, rod_offset, 0.0]), MINUS_COLOR),
        make_rod(np.array([0.0, -rod_offset, 0.0]), MINUS_COLOR),
    )
    ion = Sphere(radius=0.14, color=ION_COLOR, resolution=(16, 8)).move_to(ORIGIN)
    ion_glow = Sphere(radius=0.24, color=YELLOW_A, resolution=(12, 6)).move_to(ORIGIN)
    ion_glow.set_opacity(0.22)
    z_axis = Arrow3D(
        start=np.array([0.0, 0.0, -3.35]),
        end=np.array([0.0, 0.0, 3.35]),
        color=GREY_B,
        thickness=0.012,
        height=0.16,
        base_radius=0.055,
    )
    return rods, ion_glow, ion, z_axis


def make_cross_section_parts(scale=1.0):
    rod_radius = 0.55 * scale
    x_offset = 2.45 * scale
    y_offset = 1.6 * scale
    left = Circle(
        radius=rod_radius,
        stroke_color=RED_A,
        stroke_width=5,
        fill_color=PLUS_COLOR,
        fill_opacity=0.82,
    ).move_to(LEFT * x_offset)
    right = left.copy().move_to(RIGHT * x_offset)
    top = Circle(
        radius=rod_radius,
        stroke_color=BLUE_A,
        stroke_width=5,
        fill_color=MINUS_COLOR,
        fill_opacity=0.82,
    ).move_to(UP * y_offset)
    bottom = top.copy().move_to(DOWN * y_offset)

    plus_label = "+V_RF cos(Ωt)"
    minus_label = "-V_RF cos(Ωt)"
    labels = VGroup(
        fit_width(cn_text(plus_label, font_size=19, color=RED_A), 2.05).next_to(
            left, LEFT, buff=0.26
        ),
        fit_width(cn_text(plus_label, font_size=19, color=RED_A), 2.05).next_to(
            right, RIGHT, buff=0.26
        ),
        fit_width(cn_text(minus_label, font_size=19, color=BLUE_A), 2.15).next_to(
            top, UP, buff=0.2
        ),
        fit_width(cn_text(minus_label, font_size=19, color=BLUE_A), 2.15).next_to(
            bottom, DOWN, buff=0.2
        ),
    )

    guides = VGroup(
        DashedLine(LEFT * 1.75 * scale, RIGHT * 1.75 * scale, dash_length=0.08),
        DashedLine(DOWN * 1.05 * scale, UP * 1.05 * scale, dash_length=0.08),
    ).set_stroke(GREY_B, width=1, opacity=0.32)

    ion = Dot(radius=0.19 * scale, color=ION_COLOR)
    ion_ring = Circle(
        radius=0.38 * scale, color=YELLOW_A, stroke_width=2.5
    ).set_opacity(0.8)

    return VGroup(left, right, top, bottom), labels, guides, VGroup(ion_ring, ion)


def make_hyperbola_parts(scale=1.0):
    axes = VGroup(
        DashedLine(LEFT * 2.35 * scale, RIGHT * 2.35 * scale, dash_length=0.08),
        DashedLine(DOWN * 1.85 * scale, UP * 1.85 * scale, dash_length=0.08),
    ).set_stroke(GREY_B, width=1, opacity=0.45)
    x_label = cn_text("x", font_size=21, color=MUTED_TEXT).next_to(
        axes[0], RIGHT, buff=0.08
    )
    y_label = cn_text("y", font_size=21, color=MUTED_TEXT).next_to(
        axes[1], UP, buff=0.08
    )

    positive_curves = VGroup()
    negative_curves = VGroup()
    levels = [0.28, 0.68]
    t_min, t_max = -1.68, 1.68

    for c in levels:
        positive_curves.add(
            ParametricFunction(
                lambda t, c=c: scale * np.array([np.sqrt(t * t + c), t, 0]),
                t_range=[t_min, t_max],
                color=RED_A,
                stroke_width=3.2,
            ),
            ParametricFunction(
                lambda t, c=c: scale * np.array([-np.sqrt(t * t + c), t, 0]),
                t_range=[t_min, t_max],
                color=RED_A,
                stroke_width=3.2,
            ),
        )
        negative_curves.add(
            ParametricFunction(
                lambda t, c=c: scale * np.array([t, np.sqrt(t * t + c), 0]),
                t_range=[t_min, t_max],
                color=BLUE_A,
                stroke_width=3.2,
            ),
            ParametricFunction(
                lambda t, c=c: scale * np.array([t, -np.sqrt(t * t + c), 0]),
                t_range=[t_min, t_max],
                color=BLUE_A,
                stroke_width=3.2,
            ),
        )

    positive_label = cn_text("x²-y² = +c", font_size=20, color=RED_A).move_to(
        RIGHT * 3.05 * scale + UP * 0.95 * scale
    )
    negative_label = cn_text("x²-y² = -c", font_size=20, color=BLUE_A).move_to(
        LEFT * 3.05 * scale + DOWN * 0.95 * scale
    )
    ion = Dot(radius=0.15 * scale, color=ION_COLOR)
    ion_ring = Circle(radius=0.3 * scale, color=YELLOW_A, stroke_width=2).set_opacity(0.72)

    return (
        axes,
        x_label,
        y_label,
        positive_curves,
        negative_curves,
        positive_label,
        negative_label,
        VGroup(ion_ring, ion),
    )


def make_radial_potential_bridge_frame(scale=1.06):
    electrodes, _labels, _guides, ion_group = make_cross_section_parts(scale=scale)
    for electrode in electrodes:
        electrode.set_style(fill_opacity=0.0, stroke_opacity=0.32, stroke_width=2.3)

    (
        axes,
        x_label,
        y_label,
        positive_curves,
        negative_curves,
        positive_label,
        negative_label,
        _center_ion,
    ) = make_hyperbola_parts(scale=scale)

    axes_and_labels = VGroup(axes)
    curve_labels = VGroup(positive_label, negative_label)
    curves = VGroup(positive_curves, negative_curves)
    frame = VGroup(electrodes, axes_and_labels, curves, curve_labels, ion_group)

    return {
        "frame": frame,
        "electrodes": electrodes,
        "axes": axes_and_labels,
        "curves": curves,
        "positive_curves": positive_curves,
        "negative_curves": negative_curves,
        "curve_labels": curve_labels,
        "ion": ion_group,
    }


def make_saddle_surface(axes, sign=1.0, opacity=0.72, resolution=(16, 16)):
    colors = [RED_E, RED_D] if sign >= 0 else [BLUE_E, BLUE_D]

    def saddle_point(u, v):
        return axes.c2p(u, v, 0.22 * sign * (u * u - v * v))

    return Surface(
        saddle_point,
        u_range=[-2.0, 2.0],
        v_range=[-2.0, 2.0],
        resolution=resolution,
        checkerboard_colors=colors,
        fill_opacity=opacity,
        stroke_color=GREY_C,
        stroke_width=0.25,
    )


def make_saddle_contour_parts(axes, sign=1.0):
    positive_curves = VGroup()
    negative_curves = VGroup()
    levels = [0.28, 0.68]
    t_min, t_max = -1.68, 1.68

    for c in levels:
        positive_z = 0.22 * sign * c
        negative_z = -0.22 * sign * c
        positive_curves.add(
            ParametricFunction(
                lambda t, c=c, z=positive_z: axes.c2p(np.sqrt(t * t + c), t, z),
                t_range=[t_min, t_max],
                color=RED_A,
                stroke_width=3.0,
            ),
            ParametricFunction(
                lambda t, c=c, z=positive_z: axes.c2p(-np.sqrt(t * t + c), t, z),
                t_range=[t_min, t_max],
                color=RED_A,
                stroke_width=3.0,
            ),
        )
        negative_curves.add(
            ParametricFunction(
                lambda t, c=c, z=negative_z: axes.c2p(t, np.sqrt(t * t + c), z),
                t_range=[t_min, t_max],
                color=BLUE_A,
                stroke_width=3.0,
            ),
            ParametricFunction(
                lambda t, c=c, z=negative_z: axes.c2p(t, -np.sqrt(t * t + c), z),
                t_range=[t_min, t_max],
                color=BLUE_A,
                stroke_width=3.0,
            ),
        )

    return VGroup(positive_curves, negative_curves)


def make_bowl_surface(axes, opacity=0.68):
    def bowl_point(u, v):
        z = -0.65 + 0.16 * (u * u + v * v)
        return axes.c2p(u, v, z)

    return Surface(
        bowl_point,
        u_range=[-2.0, 2.0],
        v_range=[-2.0, 2.0],
        resolution=(22, 22),
        checkerboard_colors=[TEAL_E, GREEN_E],
        fill_opacity=opacity,
        stroke_color=GREY_B,
        stroke_width=0.25,
    )


def play_opening(scene, short=False):
    title = cn_text("振荡电场如何囚禁一个离子？", font_size=42, color=TEXT_COLOR)
    fit_width(title, 11.4)
    subtitle = cn_text("Paul 离子阱的三分钟物理图像", font_size=27, color=MUTED_TEXT)
    subtitle.next_to(title, DOWN, buff=0.35)
    accent = Line(LEFT * 2.6, RIGHT * 2.6, color=TEAL_A).next_to(
        subtitle, DOWN, buff=0.35
    )

    scene.play(Write(title), FadeIn(subtitle, shift=0.2 * DOWN), Create(accent))
    scene.wait(0.5 if short else 1.0)
    scene.play(FadeOut(title), FadeOut(subtitle), FadeOut(accent), run_time=0.45)
    scene.clear()


def play_rod_trap_3d(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=63 * DEGREES, theta=-42 * DEGREES, zoom=0.78)

    title = scene_title("线性 Paul 阱的四极杆结构")
    caption = bottom_caption("四根杆沿 z 方向延伸，在径向形成 RF 四极场。")
    prepare_fixed_frame(scene, title, caption)

    rods, ion_glow, ion, z_axis = make_rod_3d_parts()

    scene.play(FadeIn(title, shift=0.15 * DOWN))
    scene.play(
        LaggedStart(*[GrowFromCenter(rod) for rod in rods], lag_ratio=0.08),
        FadeIn(z_axis),
        run_time=1.1 if short else 1.6,
    )
    scene.play(FadeIn(ion_glow), FadeIn(ion), FadeIn(caption, shift=0.12 * UP))
    scene.wait(0.25 if short else 0.65)
    scene.move_camera(
        phi=0 * DEGREES,
        theta=-90 * DEGREES,
        zoom=1.03,
        run_time=1.45 if short else 2.6,
        rate_func=smooth,
    )
    scene.wait(0.3 if short else 0.75)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            rods,
            ion_glow,
            ion,
            z_axis,
            title,
            caption,
            fixed_mobjects=(title, caption),
        )


def play_rod_to_radial_potential(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=58 * DEGREES, theta=-42 * DEGREES, zoom=0.86)

    title = scene_title("从四极杆到径向四极势")
    caption_rods = bottom_caption("四根杆电极先给出三维结构。")
    caption_cross = bottom_caption("垂直 z 轴看过去，就是 xy 横截面的两对反相电极。")
    caption_potential = bottom_caption("中心附近：Φ(x,y) ∝ x² - y²")
    prepare_fixed_frame(scene, title, caption_rods, caption_cross, caption_potential)

    rods_3d, ion_glow_3d, ion_3d, z_axis = make_rod_3d_parts()
    add_opening_keyframe(
        scene,
        title,
        caption_rods,
        rods_3d,
        z_axis,
        ion_glow_3d,
        ion_3d,
        pause=0.2,
    )
    scene.move_camera(
        phi=0 * DEGREES,
        theta=-90 * DEGREES,
        zoom=1.16,
        run_time=1.3 if short else 2.2,
        rate_func=smooth,
    )
    scene.wait(0.15 if short else 0.4)

    rods, labels, guides, ion_group = make_cross_section_parts(scale=1.08)
    cross_section = VGroup(rods, labels, guides, ion_group)
    prepare_fixed_frame(scene, cross_section)
    scene.play(
        FadeOut(rods_3d),
        FadeOut(ion_glow_3d),
        FadeOut(ion_3d),
        FadeOut(z_axis),
        FadeOut(caption_rods),
        FadeIn(guides),
        LaggedStart(*[GrowFromCenter(rod) for rod in rods], lag_ratio=0.05),
        FadeIn(ion_group),
        FadeIn(caption_cross, shift=0.12 * UP),
        run_time=0.9 if short else 1.25,
    )
    scene.play(LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.08))

    bridge = make_radial_potential_bridge_frame(scale=1.06)
    prepare_fixed_frame(scene, bridge["frame"])
    scene.play(
        FadeOut(labels),
        FadeOut(caption_cross),
        FadeOut(rods),
        FadeOut(guides),
        FadeOut(ion_group),
        FadeIn(bridge["electrodes"]),
        FadeIn(bridge["axes"]),
        FadeIn(bridge["ion"]),
        run_time=0.55 if short else 0.75,
    )
    scene.play(
        Create(bridge["positive_curves"]),
        Create(bridge["negative_curves"]),
        FadeIn(bridge["curve_labels"]),
        FadeIn(caption_potential, shift=0.12 * UP),
        run_time=1.1 if short else 1.7,
    )
    scene.wait(0.55 if short else 1.25)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            bridge["frame"],
            title,
            caption_potential,
            fixed_mobjects=(
                title,
                caption_rods,
                caption_cross,
                caption_potential,
                cross_section,
                bridge["frame"],
            ),
        )


def play_potential_to_saddle(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.16)

    title = scene_title("二维四极势到三维马鞍面")
    caption_bridge = bottom_caption("中心附近：Φ(x,y) ∝ x² - y²")
    caption_lift = bottom_caption("把二维势图像解释为沿 z 方向的势能高度。")
    caption_saddle = bottom_caption("同一个函数在三维中呈现为马鞍面。")
    prepare_fixed_frame(scene, title, caption_bridge, caption_lift, caption_saddle)

    bridge = make_radial_potential_bridge_frame(scale=1.06)
    prepare_fixed_frame(scene, bridge["frame"])

    add_opening_keyframe(scene, title, bridge["frame"], caption_bridge, pause=0.2)

    axes = ThreeDAxes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 2.2, 1],
        z_range=[-1.35, 1.35, 0.7],
        x_length=5.3,
        y_length=5.3,
        z_length=2.6,
        tips=False,
    )
    axes.set_stroke(opacity=0.42, width=1)
    saddle = make_saddle_surface(axes, sign=1.0, opacity=0.58, resolution=(16, 16))
    saddle_contours = make_saddle_contour_parts(axes)

    scene.play(
        FadeOut(bridge["electrodes"]),
        FadeOut(bridge["ion"]),
        FadeOut(caption_bridge),
        FadeIn(caption_lift, shift=0.12 * UP),
        run_time=0.65 if short else 0.9,
    )
    scene.play(
        FadeOut(bridge["axes"]),
        FadeOut(bridge["curve_labels"]),
        FadeOut(bridge["curves"]),
        FadeIn(axes),
        FadeIn(saddle_contours),
        run_time=0.7 if short else 1.0,
    )
    release_fixed_frame(scene, bridge["frame"])

    scene.play(
        FadeOut(caption_lift),
        FadeIn(saddle),
        FadeIn(caption_saddle, shift=0.12 * UP),
        run_time=0.7 if short else 1.0,
    )
    scene.add(saddle_contours)
    scene.move_camera(
        phi=62 * DEGREES,
        theta=-42 * DEGREES,
        zoom=0.97,
        run_time=1.35 if short else 2.3,
        rate_func=smooth,
    )
    scene.wait(0.45 if short else 0.95)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            axes,
            saddle,
            saddle_contours,
            title,
            caption_saddle,
            fixed_mobjects=(title, caption_bridge, caption_lift, caption_saddle),
        )


def play_static_saddle_escape(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=62 * DEGREES, theta=-42 * DEGREES, zoom=0.97)

    title = scene_title("静止四极势：不是稳定势阱")
    formula = cn_text("Φ(x,y) ∝ x² - y²", font_size=22, color=MUTED_TEXT)
    formula.to_corner(UR, buff=0.52)
    status = cn_text("情形一：Ω = 0", font_size=20, color=TEAL_A).next_to(
        formula, DOWN, buff=0.16
    )
    caption = bottom_caption("一个方向聚焦，另一个方向发散。")
    prepare_fixed_frame(scene, title, formula, status, caption)

    axes = ThreeDAxes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 2.2, 1],
        z_range=[-1.35, 1.35, 0.7],
        x_length=5.3,
        y_length=5.3,
        z_length=2.6,
        tips=False,
    )
    axes.set_stroke(opacity=0.42, width=1)
    saddle = make_saddle_surface(axes, sign=1.0)

    def escape_point(t):
        y = 0.1 + 2.0 * smooth(t)
        x = 0.12 + 0.04 * np.sin(PI * t)
        z = 0.22 * (x * x - y * y) + 0.09
        return axes.c2p(x, y, z)

    ion = Sphere(radius=0.11, color=ION_COLOR, resolution=(16, 8)).move_to(escape_point(0))
    escape_path = ParametricFunction(escape_point, t_range=[0, 1], color=YELLOW_A)
    escape_path.set_opacity(0)
    trace = TracedPath(ion.get_center, stroke_color=YELLOW_A, stroke_width=2.2)

    scene.play(FadeIn(axes), FadeIn(saddle), FadeIn(title, shift=0.15 * DOWN))
    scene.add(trace)
    scene.play(
        FadeIn(ion),
        FadeIn(formula),
        FadeIn(status),
        FadeIn(caption, shift=0.12 * UP),
    )
    scene.play(
        MoveAlongPath(ion, escape_path),
        run_time=2.0 if short else 3.2,
        rate_func=linear,
    )
    scene.wait(0.35 if short else 0.8)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            axes,
            saddle,
            ion,
            trace,
            title,
            formula,
            status,
            caption,
            fixed_mobjects=(title, formula, status, caption),
        )


def play_driven_saddle_comparison(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=62 * DEGREES, theta=-42 * DEGREES, zoom=0.97)

    slow_title = scene_title("低频翻转：仍会逃逸")
    fast_title = scene_title("高频翻转：形成有效约束")
    formula = cn_text("Φ(x,y,t) ∝ cos(Ωt)(x² - y²)", font_size=21, color=MUTED_TEXT)
    formula.to_corner(UR, buff=0.52)
    slow_status = cn_text("情形二：Ω 较小", font_size=21, color=RED_A).next_to(
        formula, DOWN, buff=0.16
    )
    fast_status = cn_text("情形三：Ω 较大", font_size=21, color=BLUE_A).next_to(
        formula, DOWN, buff=0.16
    )
    caption_slow = bottom_caption("翻转较慢时，离子轨迹会被扰动，但最终仍离开中心。")
    caption_fast = bottom_caption("快速交替的聚焦作用可限制离子逃逸。")
    prepare_fixed_frame(
        scene,
        slow_title,
        fast_title,
        formula,
        slow_status,
        fast_status,
        caption_slow,
        caption_fast,
    )

    axes = ThreeDAxes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 2.2, 1],
        z_range=[-1.35, 1.35, 0.7],
        x_length=5.3,
        y_length=5.3,
        z_length=2.6,
        tips=False,
    )
    axes.set_stroke(opacity=0.42, width=1)

    saddle = make_saddle_surface(axes, sign=1.0, opacity=0.68, resolution=(12, 12))
    slow_progress = ValueTracker(0.0)

    def slow_ion_point():
        t = slow_progress.get_value()
        y = 0.12 + 1.9 * smooth(t)
        x = 0.1 + 0.04 * np.sin(4 * PI * t)
        z = 0.1 - 0.8 * smooth(t)
        return axes.c2p(x, y, z)

    slow_ion = always_redraw(
        lambda: Sphere(radius=0.1, color=ION_COLOR, resolution=(14, 7)).move_to(
            slow_ion_point()
        )
    )
    slow_trace = TracedPath(slow_ion.get_center, stroke_color=YELLOW_A, stroke_width=2)

    add_opening_keyframe(
        scene,
        axes,
        saddle,
        slow_title,
        formula,
        slow_status,
        caption_slow,
        slow_ion,
        pause=0.2,
    )
    scene.add(slow_trace)
    slow_signs = [-1.0, 1.0, -1.0, 1.0]
    slow_step_time = 0.55 if short else 0.9
    for index, sign in enumerate(slow_signs, start=1):
        scene.play(
            Transform(
                saddle,
                make_saddle_surface(
                    axes, sign=sign, opacity=0.68, resolution=(12, 12)
                ),
            ),
            slow_progress.animate.set_value(index / len(slow_signs)),
            run_time=slow_step_time,
            rate_func=linear,
        )
    scene.wait(0.2 if short else 0.45)
    scene.play(
        FadeOut(slow_ion),
        FadeOut(slow_trace),
        FadeOut(slow_title),
        FadeOut(slow_status),
        FadeOut(caption_slow),
        run_time=0.45,
    )

    fast_progress = ValueTracker(0.0)

    def fast_ion_point():
        t = fast_progress.get_value()
        x = 0.23 * np.cos(10 * PI * t) + 0.06 * np.sin(34 * PI * t)
        y = 0.2 * np.sin(10 * PI * t)
        z = 0.08 + 0.04 * np.sin(20 * PI * t)
        return axes.c2p(x, y, z)

    fast_ion = always_redraw(
        lambda: Sphere(radius=0.1, color=ION_COLOR, resolution=(14, 7)).move_to(
            fast_ion_point()
        )
    )
    fast_trace = TracedPath(fast_ion.get_center, stroke_color=YELLOW_A, stroke_width=2)

    scene.add(fast_trace)
    scene.play(
        FadeIn(fast_title, shift=0.15 * DOWN),
        FadeIn(fast_ion),
        FadeIn(fast_status),
        FadeIn(caption_fast, shift=0.12 * UP),
    )
    fast_signs = [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0]
    fast_step_time = 0.18 if short else 0.28
    for index, sign in enumerate(fast_signs, start=1):
        scene.play(
            Transform(
                saddle,
                make_saddle_surface(
                    axes, sign=sign, opacity=0.68, resolution=(12, 12)
                ),
            ),
            fast_progress.animate.set_value(index / len(fast_signs)),
            run_time=fast_step_time,
            rate_func=linear,
        )
    scene.wait(0.35 if short else 0.8)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            axes,
            saddle,
            fast_ion,
            fast_trace,
            fast_title,
            formula,
            fast_status,
            caption_fast,
            fixed_mobjects=(
                slow_title,
                fast_title,
                formula,
                slow_status,
                fast_status,
                caption_slow,
                caption_fast,
            ),
        )


def play_pseudopotential_confinement(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=62 * DEGREES, theta=-42 * DEGREES, zoom=1.01)

    title = scene_title("时间平均的赝势阱")
    caption_flip = bottom_caption("快速翻转的马鞍势，可以用时间平均图像理解。")
    caption_bowl = bottom_caption("平均效果近似为平滑碗形势，离子保持在中心附近。")
    closing = bottom_caption("动态不稳定 + 高频驱动 → 稳定囚禁")
    pseudo_formula = cn_text("时间平均：U_eff ∝ x² + y²", font_size=22, color=MUTED_TEXT)
    pseudo_formula.to_corner(UR, buff=0.52)
    prepare_fixed_frame(scene, title, caption_flip, caption_bowl, closing, pseudo_formula)

    axes = ThreeDAxes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 2.2, 1],
        z_range=[-1.0, 1.2, 0.5],
        x_length=5.4,
        y_length=5.4,
        z_length=2.7,
        tips=False,
    )
    axes.set_stroke(opacity=0.34, width=1)

    surface = make_saddle_surface(axes, sign=1.0, opacity=0.52, resolution=(14, 14))
    add_opening_keyframe(scene, axes, surface, title, caption_flip, pause=0.2)
    for sign in [-1.0, 1.0, -1.0, 1.0]:
        scene.play(
            Transform(
                surface,
                make_saddle_surface(axes, sign=sign, opacity=0.52, resolution=(14, 14)),
            ),
            run_time=0.22 if short else 0.32,
        )

    bowl = make_bowl_surface(axes)
    scene.play(
        FadeOut(caption_flip),
        Transform(surface, bowl),
        FadeIn(pseudo_formula),
        FadeIn(caption_bowl, shift=0.12 * UP),
        run_time=0.85 if short else 1.25,
    )

    def ion_point(t):
        x = 0.35 * np.cos(t)
        y = 0.24 * np.sin(t)
        z = -0.65 + 0.16 * (x * x + y * y) + 0.07
        return axes.c2p(x, y, z)

    ion = Sphere(radius=0.11, color=ION_COLOR, resolution=(16, 8)).move_to(ion_point(0))
    secular_path = ParametricFunction(ion_point, t_range=[0, TAU], color=ION_COLOR)
    secular_path.set_opacity(0)
    trace = TracedPath(ion.get_center, stroke_color=YELLOW_A, stroke_width=2.2)

    scene.add(trace)
    scene.play(FadeIn(ion))
    scene.play(
        MoveAlongPath(ion, secular_path),
        run_time=2.0 if short else 3.3,
        rate_func=linear,
    )
    scene.play(FadeOut(caption_bowl), FadeIn(closing, shift=0.12 * UP), run_time=0.5)
    scene.wait(0.45 if short else 1.0)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            axes,
            surface,
            ion,
            trace,
            title,
            pseudo_formula,
            closing,
            fixed_mobjects=(title, caption_flip, caption_bowl, closing, pseudo_formula),
        )


class RodTrap3D(ThreeDScene):
    """线性 Paul 阱四根杆电极的三维结构。"""

    def construct(self):
        set_dark_background(self)
        play_rod_trap_3d(self)


class RodToRadialPotential(ThreeDScene):
    """从四极杆结构过渡到 xy 横截面上的四极电势。"""

    def construct(self):
        set_dark_background(self)
        play_rod_to_radial_potential(self)


class PotentialToSaddle(ThreeDScene):
    """从二维四极势示意过渡到三维马鞍势。"""

    def construct(self):
        set_dark_background(self)
        play_potential_to_saddle(self)


class StaticSaddleEscape(ThreeDScene):
    """静止马鞍面上的定性逃逸图像。"""

    def construct(self):
        set_dark_background(self)
        play_static_saddle_escape(self)


class DrivenSaddleComparison(ThreeDScene):
    """慢翻转逃逸与快翻转受限的定性对比。"""

    def construct(self):
        set_dark_background(self)
        play_driven_saddle_comparison(self)


class PseudopotentialConfinement(ThreeDScene):
    """高频驱动下的有效赝势束缚。"""

    def construct(self):
        set_dark_background(self)
        play_pseudopotential_confinement(self)


class IonTrapDemo(ThreeDScene):
    """PPT 展示用的合集入口，短版串联新叙事结构。"""

    def construct(self):
        set_dark_background(self)
        play_opening(self, short=True)
        play_rod_to_radial_potential(self, short=True, clear_at_end=True)
        play_potential_to_saddle(self, short=True, clear_at_end=True)
        play_static_saddle_escape(self, short=True, clear_at_end=True)
        play_driven_saddle_comparison(self, short=True, clear_at_end=True)
        play_pseudopotential_confinement(self, short=True, clear_at_end=True)


class RodCrossSection(ThreeDScene):
    """兼容旧名称：渲染新的结构到径向势连续分镜。"""

    def construct(self):
        set_dark_background(self)
        play_rod_to_radial_potential(self)


class EquipotentialToSaddle(ThreeDScene):
    """兼容旧名称：渲染二维四极势到三维马鞍势过渡。"""

    def construct(self):
        set_dark_background(self)
        play_potential_to_saddle(self)


class OscillatingSaddle(ThreeDScene):
    """兼容旧名称：渲染慢翻转与快翻转对比分镜。"""

    def construct(self):
        set_dark_background(self)
        play_driven_saddle_comparison(self)
