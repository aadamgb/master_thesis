from manim import *
import numpy as np


class DroneRacing(ThreeDScene):
    """
    A 3D animation explaining drone racing:
      - Gates are drawn as concentric squares standing upright in 3D space.
      - The drone is a quadrotor: an 'X' frame with a sphere at each arm tip.
      - The drone flies along a smooth path through the sequence of gates.
    """

    def construct(self):
        # ---------------------------------------------------------------
        # 1. Camera: tilt down (phi) and rotate around (theta) for a 3D look
        # ---------------------------------------------------------------
        self.set_camera_orientation(phi=70 * DEGREES, theta=110 * DEGREES)

        # ---------------------------------------------------------------
        # 2. Faint 3D axes so the viewer has a spatial reference
        # ---------------------------------------------------------------
        axes = ThreeDAxes(
            x_range=[-1, 12, 2],
            y_range=[-4, 4, 2],
            z_range=[-3, 3, 2],
            x_length=13, y_length=8, z_length=6,
        ).set_opacity(0.25)

        # ---------------------------------------------------------------
        # 2b. Ground grid
        # ---------------------------------------------------------------
        ground = NumberPlane(
            x_range=[-8, 12, 2],
            y_range=[-20, 10, 2],
            background_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 1,
            }
        )
        # ground.rotate(90 * DEGREES, axis=RIGHT)  # rotate to be horizontal
        ground.set_opacity(0.4)

        # ---------------------------------------------------------------
        # 3. Gate positions along the course (x = forward, y = left/right, z = up)
        # ---------------------------------------------------------------
        gate_positions = [
            np.array([-3.0,  0.0,  0.0]),
            np.array([3.0,  -4.0,  -4.0]),
            np.array([8.0,  -8.0,  0.0]),
            # np.array([4.5,  1.5,  1.0]),
            # np.array([7.0, -1.5, -0.5]),
            # np.array([9.5,  0.5,  1.5]),
        ]
        gate_colors = [BLUE, BLUE, BLUE]

        gates = VGroup()
        for pos, col in zip(gate_positions, gate_colors):
            gate = self.make_gate(color=col)
            gate.move_to(pos)
            gates.add(gate)

        # ---------------------------------------------------------------
        # 4. The quadrotor drone
        # ---------------------------------------------------------------
        drone = self.make_drone()
        start_point = np.array([-6.0, 0.0, 0.0])
        drone.move_to(start_point)
        

        # ---------------------------------------------------------------
        # 5. Smooth flight path through every gate centre
        # ---------------------------------------------------------------
        path = VMobject()
        path_points = [start_point] + gate_positions + [np.array([11.5, 0.0, 0.0])]
        path.set_points_smoothly(path_points)
        path.set_stroke(YELLOW, width=5)

        # ---------------------------------------------------------------
        # 6. Title (fixed to the screen, not the 3D world)
        # ---------------------------------------------------------------
        # title = Text("Drone Racing", font_size=30, weight=BOLD)
        # self.add_fixed_in_frame_mobjects(title)
        # title.to_edge(UP)

        # ---------------------------------------------------------------
        # 7. Animate everything
        # ---------------------------------------------------------------
        self.add(ground)  # add ground grid to scene
        
        self.play(FadeIn(drone, scale=0.4))
        self.wait(0.8)
        
        # self.wait(0.1)

        # gates appear one after another
        for gate in gates:
            self.add(gate)
            self.wait(0.5) 
        
        drone.rotate(20 * DEGREES, axis=Y_AXIS)

        self.play(MoveAlongPath(drone, path), run_time=6, rate_func=smooth)

        # drone.remove_updater(spin_rotors)
        self.wait(0.5)

    # ===================================================================
    # Helper builders
    # ===================================================================
    def make_drone(self):
        """Quadrotor: an X of 4 arms, each ending in a sphere."""
        arm_length = 0.55
        rotor_radius = 0.1
 
        arms = VGroup()
        rotors = VGroup()
 
        for angle in [45, 135, 225, 315]:
            rad = angle * DEGREES
            tip = arm_length * np.array([np.cos(rad), np.sin(rad), 0.0])
 
            # the arm
            arms.add(Line(ORIGIN, tip, color=WHITE, stroke_width=5))
 
            # sphere at the tip
            sphere = Dot3D(radius=rotor_radius, color=GREEN)
            sphere.move_to(tip)
            rotors.add(sphere)
 
        # body = Dot3D(point=ORIGIN, radius=0.13, color=RED)
 
        drone = VGroup(arms, rotors)
        # drone.rotor_groups = rotors  # keep a handle for the spin updater
        return drone

    def make_gate(self, color=YELLOW):
        """A racing gate: a solid square frame (open centre) standing upright.
 
        The frame is the outer square minus the inner square, so the band
        between them is filled solid while the middle stays open for the
        drone to fly THROUGH.
        """
        outer = Square(side_length=2.5)
        inner = Square(side_length=1.5)
        frame = Difference(
            outer, inner,
            color=color,
            fill_opacity=1.0,      # solid fill, same opacity as the outline
            stroke_color=color,
            stroke_width=2,
        )
        gate = VGroup(frame)
        # rotate from the xy-plane into the yz-plane so the drone flies THROUGH it
        gate.rotate(90 * DEGREES, axis=UP)
        return gate