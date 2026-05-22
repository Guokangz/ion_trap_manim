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
DEFAULT_CONTOUR_LEVELS = (0.28, 0.68)
SADDLE_BRIDGE_CONTOUR_LEVELS = (0.22, 0.48, 0.78)


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


def make_corner_coordinate_reference(scene):
    axis_origin = np.array(
        [config.frame_width / 2 - 1.65, -config.frame_height / 2 + 1.02, 0.0]
    )
    panel_center = axis_origin + np.array([0.40, 0.34, 0.0])
    axis_length = 0.60
    axis_specs = (
        ("x", np.array([1.0, 0.0, 0.0]), RED_A),
        ("y", np.array([0.0, 1.0, 0.0]), GREEN_A),
        ("z", np.array([0.0, 0.0, 1.0]), BLUE_A),
    )

    def get_camera_angle(name, fallback):
        getter = getattr(scene.camera, f"get_{name}", None)
        if getter is not None:
            return getter()
        tracker = getattr(scene.camera, f"{name}_tracker", None)
        return tracker.get_value() if tracker is not None else fallback

    def draw_reference():
        phi = get_camera_angle("phi", 0.0)
        theta = get_camera_angle("theta", -90 * DEGREES)
        right_vec = np.array([-np.sin(theta), np.cos(theta), 0.0])
        view_vec = np.array(
            [np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)]
        )
        up_vec = np.cross(view_vec, right_vec)

        panel = RoundedRectangle(
            width=1.88,
            height=1.54,
            corner_radius=0.08,
            stroke_color="#334155",
            stroke_width=1.0,
            fill_color="#111827",
            fill_opacity=0.42,
        ).move_to(panel_center)
        axes = VGroup(panel)

        for axis_name, world_vec, color in axis_specs:
            projected = np.array(
                [np.dot(world_vec, right_vec), np.dot(world_vec, up_vec), 0.0]
            )
            projected_norm = np.linalg.norm(projected[:2])
            if projected_norm < 0.08:
                dot = Dot(axis_origin, radius=0.043, color=color)
                dot.set_stroke(WHITE, width=0.9, opacity=0.75)
                label = cn_text(axis_name, font_size=16, color=color).move_to(
                    axis_origin + np.array([0.17, 0.17, 0.0])
                )
                axes.add(dot, label)
                continue

            current_axis_length = axis_length * (1.08 if axis_name == "z" else 1.0)
            axis_end = axis_origin + current_axis_length * projected
            direction = projected / projected_norm
            shaft_end = axis_end - 0.045 * direction
            arrow_shaft = Line(
                axis_origin,
                shaft_end,
                stroke_width=3.5,
                color=color,
            )
            tip_size = 0.064 if axis_name == "z" else 0.058
            tip_angle = np.arctan2(direction[1], direction[0])
            arrow_tip = Triangle(
                fill_color=color,
                fill_opacity=1.0,
                stroke_color=color,
                stroke_width=0,
            )
            arrow_tip.scale(tip_size).rotate(tip_angle - PI / 2).move_to(axis_end)
            label = cn_text(axis_name, font_size=16, color=color).move_to(
                axis_end + (0.16 if axis_name == "z" else 0.13) * direction
            )
            axes.add(arrow_shaft, arrow_tip, label)

        axes.set_z_index(20)
        return axes

    return always_redraw(draw_reference)


def make_coordinate_inset(mode="3d"):
    panel = RoundedRectangle(
        width=1.88,
        height=1.54,
        corner_radius=0.08,
        stroke_color="#334155",
        stroke_width=1.0,
        fill_color="#111827",
        fill_opacity=0.42,
    )
    origin = LEFT * 0.44 + DOWN * 0.34

    if mode == "2d":
        axis_data = (
            ("x", origin + RIGHT * 0.72, RED_A, RIGHT * 0.10 + DOWN * 0.02, 1.0),
            ("y", origin + UP * 0.64, GREEN_A, UP * 0.10, 1.0),
            ("z", origin + LEFT * 0.15 + DOWN * 0.10, BLUE_A, LEFT * 0.08, 0.72),
        )
    else:
        axis_data = (
            ("x", origin + RIGHT * 0.72 + DOWN * 0.17, RED_A, RIGHT * 0.10 + DOWN * 0.02, 1.0),
            ("y", origin + RIGHT * 0.62 + UP * 0.48, GREEN_A, RIGHT * 0.08 + UP * 0.08, 1.0),
            ("z", origin + UP * 0.68, BLUE_A, LEFT * 0.02 + UP * 0.11, 1.0),
        )

    inset = VGroup(panel)
    for label_text, axis_end, color, label_offset, opacity in axis_data:
        vector = axis_end - origin
        norm = np.linalg.norm(vector[:2])
        direction = vector / norm
        shaft_end = axis_end - 0.055 * direction
        shaft = Line(origin, shaft_end, stroke_width=3.4, color=color)
        tip = Triangle(
            fill_color=color,
            fill_opacity=1.0,
            stroke_color=color,
            stroke_width=0,
        )
        tip.scale(0.056).rotate(np.arctan2(direction[1], direction[0]) - PI / 2)
        tip.move_to(axis_end)
        axis_label = cn_text(label_text, font_size=15, color=color).move_to(
            axis_end + label_offset
        )
        axis_group = VGroup(shaft, tip, axis_label).set_opacity(opacity)
        inset.add(axis_group)

    inset.to_corner(DR, buff=0.45)
    inset.set_z_index(20)
    return inset


def make_rf_drive_inset():
    panel = RoundedRectangle(
        width=3.70,
        height=1.72,
        corner_radius=0.08,
        stroke_color="#334155",
        stroke_width=1.0,
        fill_color="#111827",
        fill_opacity=0.50,
    )
    header = cn_text("RF 反相驱动", font_size=20, color=TEAL_A).move_to(UP * 0.63)
    plus_baseline = Line(LEFT * 1.46 + UP * 0.20, RIGHT * 0.38 + UP * 0.20)
    minus_baseline = Line(LEFT * 1.46 + DOWN * 0.20, RIGHT * 0.38 + DOWN * 0.20)
    baselines = VGroup(plus_baseline, minus_baseline).set_stroke(
        GREY_B, width=1.0, opacity=0.48
    )

    def wave_point(t, sign):
        x = -1.46 + 1.84 * (t + PI) / TAU
        y = sign * 0.20 + sign * 0.14 * np.cos(t)
        return np.array([x, y, 0.0])

    plus_wave = ParametricFunction(
        lambda t: wave_point(t, 1.0),
        t_range=[-PI, PI, 0.04],
        color=RED_A,
        stroke_width=2.8,
    )
    minus_wave = ParametricFunction(
        lambda t: wave_point(t, -1.0),
        t_range=[-PI, PI, 0.04],
        color=BLUE_A,
        stroke_width=2.8,
    )
    plus_label = cn_text("+V_RF cos(Ωt)", font_size=14, color=RED_A).move_to(
        RIGHT * 1.18 + UP * 0.31
    )
    minus_label = cn_text("-V_RF cos(Ωt)", font_size=14, color=BLUE_A).move_to(
        RIGHT * 1.18 + DOWN * 0.17
    )
    pair_plus = cn_text("左右同相", font_size=14, color=RED_A).move_to(
        LEFT * 0.62 + DOWN * 0.64
    )
    pair_minus = cn_text("上下反相", font_size=14, color=BLUE_A).move_to(
        RIGHT * 0.78 + DOWN * 0.64
    )

    inset = VGroup(
        panel,
        header,
        baselines,
        plus_wave,
        minus_wave,
        plus_label,
        minus_label,
        pair_plus,
        pair_minus,
    )
    inset.to_corner(UR, buff=0.42).shift(DOWN * 0.68)
    inset.set_z_index(18)
    return inset


def make_dynamic_rf_drive_inset(
    phase_tracker,
    cycles_tracker=None,
    omega_text="Ω 较小",
    omega_color=RED_A,
):
    if cycles_tracker is None:
        cycles_tracker = ValueTracker(1.15)

    panel = RoundedRectangle(
        width=3.70,
        height=1.72,
        corner_radius=0.08,
        stroke_color="#334155",
        stroke_width=1.0,
        fill_color="#111827",
        fill_opacity=0.50,
    )
    panel.to_corner(UR, buff=0.42).shift(DOWN * 0.68)
    center = panel.get_center()

    def at(x, y):
        return center + np.array([x, y, 0.0])

    header = cn_text("RF 反相驱动", font_size=20, color=TEAL_A).move_to(at(0.0, 0.63))
    omega_badge = cn_text(omega_text, font_size=15, color=omega_color).move_to(
        at(1.30, 0.62)
    )

    scope_x_min = -1.46
    scope_x_max = 0.50
    scope_y_min = -0.48
    scope_y_max = 0.46
    scope_width = scope_x_max - scope_x_min
    plus_base = 0.18
    minus_base = -0.18
    amplitude = 0.13

    scope_frame = Rectangle(
        width=scope_width,
        height=scope_y_max - scope_y_min,
        stroke_color="#334155",
        stroke_width=0.8,
        fill_opacity=0.0,
    ).move_to(at((scope_x_min + scope_x_max) / 2, (scope_y_min + scope_y_max) / 2))
    grid = VGroup()
    for x in np.linspace(scope_x_min, scope_x_max, 6):
        grid.add(Line(at(x, scope_y_min), at(x, scope_y_max)))
    for y in np.linspace(scope_y_min, scope_y_max, 5):
        grid.add(Line(at(scope_x_min, y), at(scope_x_max, y)))
    grid.set_stroke("#475569", width=0.7, opacity=0.24)

    plus_baseline = Line(at(scope_x_min, plus_base), at(scope_x_max, plus_base))
    minus_baseline = Line(at(scope_x_min, minus_base), at(scope_x_max, minus_base))
    baselines = VGroup(plus_baseline, minus_baseline).set_stroke(
        GREY_B, width=1.0, opacity=0.42
    )

    def visible_cycles():
        return max(0.3, cycles_tracker.get_value())

    def wave_value(s):
        return np.cos(TAU * visible_cycles() * s - phase_tracker.get_value())

    def wave_point(s, sign):
        base = plus_base if sign > 0 else minus_base
        x = scope_x_min + scope_width * s
        y = base + sign * amplitude * wave_value(s)
        return at(x, y)

    plus_wave = always_redraw(
        lambda: ParametricFunction(
            lambda s: wave_point(s, 1.0),
            t_range=[0, 1, 0.01],
            color=RED_A,
            stroke_width=2.7,
        ).set_z_index(19)
    )
    minus_wave = always_redraw(
        lambda: ParametricFunction(
            lambda s: wave_point(s, -1.0),
            t_range=[0, 1, 0.01],
            color=BLUE_A,
            stroke_width=2.7,
        ).set_z_index(19)
    )
    now_pointer = Line(
        at(scope_x_max, scope_y_min),
        at(scope_x_max, scope_y_max),
        color=TEAL_A,
        stroke_width=2.1,
    ).set_opacity(0.70)
    plus_dot = always_redraw(
        lambda: Dot(wave_point(1.0, 1.0), radius=0.043, color=RED_A)
        .set_stroke(WHITE, width=0.7, opacity=0.7)
        .set_z_index(20)
    )
    minus_dot = always_redraw(
        lambda: Dot(wave_point(1.0, -1.0), radius=0.043, color=BLUE_A)
        .set_stroke(WHITE, width=0.7, opacity=0.7)
        .set_z_index(20)
    )
    voltage_label = cn_text("V(t)", font_size=12, color=MUTED_TEXT).move_to(
        at(scope_x_min - 0.13, scope_y_max - 0.03)
    )
    time_label = cn_text("t", font_size=13, color=MUTED_TEXT).move_to(
        at(scope_x_max + 0.12, scope_y_min - 0.02)
    )
    plus_label = cn_text("+V_RF cos(Ωt)", font_size=14, color=RED_A).move_to(
        at(1.18, 0.31)
    )
    minus_label = cn_text("-V_RF cos(Ωt)", font_size=14, color=BLUE_A).move_to(
        at(1.18, -0.17)
    )
    pair_plus = cn_text("左右同相", font_size=14, color=RED_A).move_to(
        at(-0.62, -0.64)
    )
    pair_minus = cn_text("上下反相", font_size=14, color=BLUE_A).move_to(
        at(0.78, -0.64)
    )

    inset = VGroup(
        panel,
        header,
        omega_badge,
        scope_frame,
        grid,
        baselines,
        plus_wave,
        minus_wave,
        now_pointer,
        plus_dot,
        minus_dot,
        voltage_label,
        time_label,
        plus_label,
        minus_label,
        pair_plus,
        pair_minus,
    )
    inset.set_z_index(18)
    return inset, omega_badge


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


def make_electrode_phase_tags(electrodes):
    return VGroup(
        cn_text("+RF", font_size=24, color=WHITE).move_to(electrodes[0]),
        cn_text("+RF", font_size=24, color=WHITE).move_to(electrodes[1]),
        cn_text("-RF", font_size=24, color=WHITE).move_to(electrodes[2]),
        cn_text("-RF", font_size=24, color=WHITE).move_to(electrodes[3]),
    ).set_opacity(0.88)


def make_hyperbola_parts(scale=1.0, levels=DEFAULT_CONTOUR_LEVELS):
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


def make_radial_potential_bridge_frame(
    scale=1.12, show_curve_labels=False, levels=DEFAULT_CONTOUR_LEVELS
):
    electrodes, _labels, _guides, ion_group = make_cross_section_parts(scale=scale)
    for electrode in electrodes:
        electrode.set_style(fill_opacity=0.08, stroke_opacity=0.5, stroke_width=2.5)

    (
        axes,
        x_label,
        y_label,
        positive_curves,
        negative_curves,
        positive_label,
        negative_label,
        _center_ion,
    ) = make_hyperbola_parts(scale=scale, levels=levels)

    axes_and_labels = VGroup(axes)
    curve_labels = (
        VGroup(positive_label, negative_label) if show_curve_labels else VGroup()
    )
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


def make_saddle_surface(
    axes, sign=1.0, opacity=0.72, resolution=(16, 16), height_scale=1.0
):
    colors = [RED_E, RED_D] if sign >= 0 else [BLUE_E, BLUE_D]

    def saddle_point(u, v):
        return axes.c2p(u, v, 0.22 * sign * height_scale * (u * u - v * v))

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


def make_saddle_contour_parts(
    axes, sign=1.0, height_scale=1.0, levels=DEFAULT_CONTOUR_LEVELS
):
    positive_curves = VGroup()
    negative_curves = VGroup()
    t_min, t_max = -1.68, 1.68

    for c in levels:
        positive_z = 0.22 * sign * height_scale * c
        negative_z = -0.22 * sign * height_scale * c
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
    scene.set_camera_orientation(phi=58 * DEGREES, theta=-42 * DEGREES, zoom=0.88)

    title = scene_title("线性 Paul 阱的四杆电极与径向四极场")
    coord_ref = make_corner_coordinate_reference(scene)
    rf_inset = make_rf_drive_inset()
    prepare_fixed_frame(scene, title, coord_ref, rf_inset)

    rods_3d, ion_glow_3d, ion_3d, _z_axis = make_rod_3d_parts(
        rod_offset=1.42,
        rod_radius=0.16,
        rod_length=6.0,
    )
    add_opening_keyframe(
        scene,
        title,
        coord_ref,
        rods_3d,
        ion_glow_3d,
        ion_3d,
        pause=0.2,
    )
    scene.wait(0.15 if short else 0.28)
    scene.move_camera(
        phi=0 * DEGREES,
        theta=-90 * DEGREES,
        zoom=1.22,
        run_time=1.75 if short else 2.9,
        rate_func=smooth,
    )
    scene.wait(0.18 if short else 0.36)

    rods, _labels, guides, ion_group = make_cross_section_parts(scale=1.12)
    phase_tags = make_electrode_phase_tags(rods)
    cross_section = VGroup(rods, guides, ion_group, phase_tags)
    prepare_fixed_frame(scene, cross_section)
    scene.play(
        FadeOut(rods_3d, scale=1.02),
        FadeOut(ion_glow_3d, scale=1.02),
        FadeOut(ion_3d, scale=1.02),
        FadeIn(rods, scale=0.94),
        FadeIn(ion_group, scale=0.94),
        run_time=1.05 if short else 1.25,
        rate_func=smooth,
    )
    scene.play(
        FadeIn(guides),
        FadeIn(phase_tags),
        run_time=0.45 if short else 0.6,
        rate_func=smooth,
    )
    scene.play(
        FadeIn(rf_inset, shift=0.08 * DOWN),
        run_time=0.6 if short else 0.82,
        rate_func=smooth,
    )
    scene.wait(0.08 if short else 0.2)

    bridge = make_radial_potential_bridge_frame(scale=1.12)
    prepare_fixed_frame(scene, bridge["frame"])
    scene.play(
        ReplacementTransform(rods, bridge["electrodes"]),
        ReplacementTransform(ion_group, bridge["ion"]),
        FadeOut(guides),
        FadeOut(phase_tags),
        FadeIn(bridge["axes"]),
        run_time=0.72 if short else 0.98,
        rate_func=smooth,
    )
    scene.play(
        Create(bridge["positive_curves"]),
        Create(bridge["negative_curves"]),
        FadeIn(bridge["curve_labels"]),
        run_time=1.1 if short else 1.55,
        rate_func=smooth,
    )
    scene.wait(0.75 if short else 1.5)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            bridge["frame"],
            title,
            coord_ref,
            rf_inset,
            fixed_mobjects=(
                title,
                coord_ref,
                rf_inset,
                cross_section,
                bridge["frame"],
            ),
        )


def play_potential_to_saddle(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.16)

    title = scene_title("四极电势的二维图像与三维马鞍面")
    coord_ref = make_coordinate_inset(mode="2d")
    rf_inset = make_rf_drive_inset()
    prepare_fixed_frame(scene, title, coord_ref, rf_inset)

    contour_levels = SADDLE_BRIDGE_CONTOUR_LEVELS
    bridge = make_radial_potential_bridge_frame(scale=1.12, levels=contour_levels)
    prepare_fixed_frame(scene, bridge["frame"])

    add_opening_keyframe(
        scene, title, bridge["frame"], rf_inset, coord_ref, pause=0.25
    )

    axes = ThreeDAxes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 2.2, 1],
        z_range=[-1.35, 1.35, 0.7],
        x_length=4.85,
        y_length=4.85,
        z_length=2.4,
        tips=False,
    )
    axes.set_stroke(opacity=0.0, width=0)
    lift = ValueTracker(0.0)

    def lifted_amount():
        return smooth(lift.get_value())

    saddle = always_redraw(
        lambda: make_saddle_surface(
            axes,
            sign=1.0,
            opacity=0.10 + 0.48 * lifted_amount(),
            resolution=(18, 18),
            height_scale=lifted_amount(),
        )
    )
    saddle_contours = make_saddle_contour_parts(
        axes,
        sign=1.0,
        height_scale=0.0,
        levels=contour_levels,
    )

    def update_saddle_contours(mob):
        mob.become(
            make_saddle_contour_parts(
                axes,
                sign=1.0,
                height_scale=lifted_amount(),
                levels=contour_levels,
            )
        )

    scene.play(
        FadeOut(bridge["electrodes"]),
        FadeOut(bridge["ion"]),
        FadeOut(bridge["axes"]),
        run_time=0.75 if short else 1.05,
        rate_func=smooth,
    )
    scene.play(
        FadeIn(saddle),
        FadeOut(bridge["curve_labels"]),
        ReplacementTransform(bridge["curves"], saddle_contours),
        run_time=0.8 if short else 1.05,
        rate_func=smooth,
    )
    release_fixed_frame(scene, bridge["frame"])
    saddle_contours.add_updater(update_saddle_contours)
    scene.wait(0.18 if short else 0.28)

    scene.play(
        lift.animate.set_value(1.0),
        run_time=1.0 if short else 1.35,
        rate_func=smooth,
    )
    scene.move_camera(
        phi=14 * DEGREES,
        theta=-78 * DEGREES,
        zoom=1.14,
        run_time=0.85 if short else 1.15,
        rate_func=smooth,
        added_anims=[Transform(coord_ref, make_coordinate_inset(mode="3d"))],
    )
    scene.move_camera(
        phi=48 * DEGREES,
        theta=-54 * DEGREES,
        zoom=1.04,
        run_time=1.15 if short else 1.85,
        rate_func=smooth,
    )
    scene.wait(0.55 if short else 1.05)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            saddle,
            saddle_contours,
            title,
            rf_inset,
            coord_ref,
            fixed_mobjects=(title, rf_inset, coord_ref),
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
    scene.set_camera_orientation(phi=48 * DEGREES, theta=-54 * DEGREES, zoom=1.04)

    title = scene_title("RF 翻转频率与动态稳定")
    coord_ref = make_coordinate_inset(mode="3d")
    drive_phase = ValueTracker(0.0)
    scope_cycles = ValueTracker(1.15)
    rf_inset, omega_badge = make_dynamic_rf_drive_inset(
        drive_phase,
        cycles_tracker=scope_cycles,
        omega_text="Ω 较小",
        omega_color=RED_A,
    )
    status = cn_text("情形二：Ω 较小", font_size=22, color=RED_A).to_corner(
        UL, buff=0.62
    )
    status.shift(DOWN * 0.86)
    outcome = cn_text("低频：仍会逃逸", font_size=20, color=TEXT_COLOR).next_to(
        status, DOWN, buff=0.14, aligned_edge=LEFT
    )
    prepare_fixed_frame(scene, title, coord_ref, rf_inset, status, outcome)

    axes = ThreeDAxes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 2.2, 1],
        z_range=[-1.35, 1.35, 0.7],
        x_length=5.15,
        y_length=5.15,
        z_length=2.55,
        tips=False,
    )
    axes.set_stroke(opacity=0.0, width=0)

    saddle = always_redraw(
        lambda: make_saddle_surface(
            axes,
            sign=np.cos(drive_phase.get_value()),
            opacity=0.66,
            resolution=(12, 12),
        )
    )
    slow_progress = ValueTracker(0.0)

    def slow_point_at(t):
        y = 0.08 + 1.86 * smooth(t)
        x = 0.08 + 0.05 * np.sin(4 * PI * t)
        z = 0.10 - 0.74 * smooth(t)
        return axes.c2p(x, y, z)

    def slow_ion_point():
        return slow_point_at(slow_progress.get_value())

    slow_ion = always_redraw(
        lambda: Sphere(radius=0.1, color=ION_COLOR, resolution=(14, 7)).move_to(
            slow_ion_point()
        )
    )
    slow_path = ParametricFunction(
        slow_point_at,
        t_range=[0, 1, 0.02],
        color=YELLOW_A,
        stroke_width=2.1,
    )
    slow_path.set_stroke(YELLOW_A, width=2.1, opacity=0.84)
    slow_path.set_fill(opacity=0.0)

    add_opening_keyframe(
        scene,
        saddle,
        title,
        rf_inset,
        coord_ref,
        status,
        outcome,
        slow_ion,
        pause=0.28 if not short else 0.18,
    )
    slow_run_time = 2.8 if short else 4.4
    scene.play(
        Create(slow_path),
        drive_phase.animate.set_value(2 * TAU),
        slow_progress.animate.set_value(1.0),
        run_time=slow_run_time,
        rate_func=linear,
    )
    scene.wait(0.2 if short else 0.45)

    fast_status = cn_text("情形三：Ω 较大", font_size=22, color=BLUE_A).move_to(status)
    fast_outcome = cn_text("高频：形成有效约束", font_size=20, color=TEXT_COLOR).move_to(
        outcome
    )
    fast_badge = cn_text("Ω 较大", font_size=15, color=BLUE_A).move_to(omega_badge)
    prepare_fixed_frame(scene, fast_status, fast_outcome, fast_badge)
    scene.play(
        FadeOut(slow_ion),
        FadeOut(slow_path),
        FadeOut(status, shift=0.04 * UP),
        FadeOut(outcome, shift=0.04 * UP),
        FadeOut(omega_badge),
        FadeIn(fast_status, shift=0.04 * UP),
        FadeIn(fast_outcome, shift=0.04 * UP),
        FadeIn(fast_badge),
        drive_phase.animate.set_value(2 * TAU + 0.35),
        scope_cycles.animate.set_value(2.85),
        run_time=0.65 if short else 0.85,
        rate_func=smooth,
    )
    status = fast_status
    outcome = fast_outcome
    omega_badge = fast_badge

    fast_progress = ValueTracker(0.0)

    def fast_point_at(t):
        x = 0.23 * np.cos(5.2 * PI * t) + 0.035 * np.sin(13 * PI * t)
        y = 0.16 * np.sin(5.2 * PI * t)
        z = 0.08 + 0.035 * np.sin(10.4 * PI * t)
        return axes.c2p(x, y, z)

    def fast_ion_point():
        return fast_point_at(fast_progress.get_value())

    fast_ion = always_redraw(
        lambda: Sphere(radius=0.1, color=ION_COLOR, resolution=(14, 7)).move_to(
            fast_ion_point()
        )
    )
    fast_path = ParametricFunction(
        fast_point_at,
        t_range=[0, 1, 0.015],
        color=YELLOW_A,
        stroke_width=1.8,
    )
    fast_path.set_stroke(YELLOW_A, width=1.8, opacity=0.86)
    fast_path.set_fill(opacity=0.0)

    scene.play(
        FadeIn(fast_ion),
        run_time=0.35,
    )
    fast_run_time = 2.0 if short else 3.2
    scene.play(
        Create(fast_path),
        drive_phase.animate.set_value(8 * TAU),
        fast_progress.animate.set_value(1.0),
        run_time=fast_run_time,
        rate_func=linear,
    )
    scene.wait(0.35 if short else 0.8)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            saddle,
            fast_ion,
            fast_path,
            title,
            rf_inset,
            coord_ref,
            status,
            outcome,
            omega_badge,
            fixed_mobjects=(
                title,
                rf_inset,
                coord_ref,
                status,
                outcome,
                omega_badge,
            ),
        )


def play_pseudopotential_confinement(scene, short=False, clear_at_end=False):
    scene.set_camera_orientation(phi=48 * DEGREES, theta=-54 * DEGREES, zoom=1.04)

    title = scene_title("高频平均下的赝势囚禁")
    coord_ref = make_coordinate_inset(mode="3d")
    drive_phase = ValueTracker(0.0)
    scope_cycles = ValueTracker(2.85)
    rf_inset, _omega_badge = make_dynamic_rf_drive_inset(
        drive_phase,
        cycles_tracker=scope_cycles,
        omega_text="Ω 较大",
        omega_color=BLUE_A,
    )
    status = cn_text("高频驱动：Ω 较大", font_size=22, color=BLUE_A).to_corner(
        UL, buff=0.62
    )
    status.shift(DOWN * 0.86)
    outcome = cn_text("瞬时势快速交替", font_size=20, color=TEXT_COLOR).next_to(
        status, DOWN, buff=0.14, aligned_edge=LEFT
    )
    pseudo_formula = cn_text("U_eff ∝ x² + y²", font_size=17, color=TEAL_A)
    pseudo_formula.move_to(np.array([4.82, 1.05, 0.0])).set_opacity(0.84)
    prepare_fixed_frame(scene, title, coord_ref, rf_inset, status, outcome, pseudo_formula)

    axes = ThreeDAxes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 2.2, 1],
        z_range=[-1.2, 1.2, 0.5],
        x_length=5.15,
        y_length=5.15,
        z_length=2.55,
        tips=False,
    )
    axes.set_stroke(opacity=0.0, width=0)

    surface = make_saddle_surface(
        axes,
        sign=1.0,
        opacity=0.52,
        resolution=(14, 14),
    )
    bowl = make_bowl_surface(axes)

    pseudo_progress = ValueTracker(0.0)

    def pseudo_point_at(t):
        x = 0.32 * np.cos(t)
        y = 0.22 * np.sin(t)
        z = -0.65 + 0.16 * (x * x + y * y) + 0.08
        return axes.c2p(x, y, z)

    def ion_point():
        return pseudo_point_at(pseudo_progress.get_value())

    ion = always_redraw(
        lambda: Sphere(radius=0.1, color=ION_COLOR, resolution=(14, 7)).move_to(
            ion_point()
        )
    )
    pseudo_trace = ParametricFunction(
        pseudo_point_at,
        t_range=[0, 0.92 * TAU, 0.03],
        color=YELLOW_A,
        stroke_width=2.0,
    )
    pseudo_trace.set_stroke(YELLOW_A, width=2.0, opacity=0.88)
    pseudo_trace.set_fill(opacity=0.0)

    add_opening_keyframe(
        scene,
        surface,
        title,
        rf_inset,
        coord_ref,
        status,
        outcome,
        pause=0.2 if not short else 0.12,
    )

    phase_target = drive_phase.get_value()
    flip_run_time = 0.16 if short else 0.24
    for sign in [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0]:
        phase_target += PI
        scene.play(
            Transform(
                surface,
                make_saddle_surface(
                    axes,
                    sign=sign,
                    opacity=0.52,
                    resolution=(14, 14),
                ),
            ),
            drive_phase.animate.set_value(phase_target),
            run_time=flip_run_time,
            rate_func=linear,
        )

    avg_status = cn_text("时间平均图像", font_size=22, color=TEAL_A).move_to(status)
    avg_outcome = cn_text("高频平均 → 有效势阱", font_size=20, color=TEXT_COLOR).move_to(
        outcome
    )
    prepare_fixed_frame(scene, avg_status, avg_outcome)
    scene.play(
        FadeOut(status, shift=0.04 * UP),
        FadeOut(outcome, shift=0.04 * UP),
        FadeIn(avg_status, shift=0.04 * UP),
        FadeIn(avg_outcome, shift=0.04 * UP),
        run_time=0.45 if short else 0.6,
        rate_func=smooth,
    )

    scene.play(
        Transform(surface, bowl),
        FadeIn(pseudo_formula, shift=0.04 * DOWN),
        drive_phase.animate.set_value(phase_target + TAU),
        run_time=0.85 if short else 1.25,
        rate_func=smooth,
    )

    final_status = cn_text("赝势阱：稳定囚禁", font_size=22, color=TEAL_A).move_to(
        avg_status
    )
    final_outcome = cn_text("阱底附近小振荡", font_size=20, color=TEXT_COLOR).move_to(
        avg_outcome
    )
    prepare_fixed_frame(scene, final_status, final_outcome)
    scene.move_camera(
        phi=54 * DEGREES,
        theta=-43 * DEGREES,
        zoom=0.92,
        run_time=0.45 if short else 0.6,
        rate_func=smooth,
        added_anims=[
            FadeOut(avg_status, shift=0.04 * UP),
            FadeOut(avg_outcome, shift=0.04 * UP),
            FadeIn(final_status, shift=0.04 * UP),
            FadeIn(final_outcome, shift=0.04 * UP),
        ],
    )
    scene.play(
        FadeIn(ion),
        Create(pseudo_trace),
        pseudo_progress.animate.set_value(0.92 * TAU),
        drive_phase.animate.set_value(phase_target + 5 * TAU),
        run_time=1.75 if short else 2.8,
        rate_func=linear,
    )
    scene.wait(0.45 if short else 1.0)

    if clear_at_end:
        fade_out_and_clear(
            scene,
            surface,
            ion,
            pseudo_trace,
            title,
            rf_inset,
            coord_ref,
            final_status,
            final_outcome,
            pseudo_formula,
            fixed_mobjects=(
                title,
                rf_inset,
                coord_ref,
                pseudo_formula,
                status,
                outcome,
                avg_status,
                avg_outcome,
                final_status,
                final_outcome,
            ),
        )


class RodTrap3D(ThreeDScene):
    """线性 Paul 阱四根杆电极的三维结构。"""

    def construct(self):
        set_dark_background(self)
        play_rod_trap_3d(self)


class RodToRadialPotential(ThreeDScene):
    """线性 Paul 阱四杆电极到径向横截面四极场。"""

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
