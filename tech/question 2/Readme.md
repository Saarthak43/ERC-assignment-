## QUESTION 2

2.You've seen robotic arms on factory floors — seamlessly grabbing, moving, and placing
objects with surgical precision. Now it's your turn to build one. Model a pick-and-place
robotic arm with a functioning conveyor belt and gripper in MATLAB Simscape
Multibody. The arm must pick an object off the belt, move it, and place it — all
simulated in 3D. The catch? You're getting a broken, unconnected Simscape model as
your starting point. Blocks are there. Wires aren't. Parameters are wrong. Rotations are
missing. You'll need to understand the kinematics, fix the connections, and get the
whole thing running.

## ANSWER 2

To understand the wiring and connections, we first have to understand the blocks and ports, their functions, and how the subsystems inside those blocks are connected within. Each block in this model represents either a physical component in the real world — like a conveyor belt, a gripper arm, or a rigid body — or a computational element that governs how those physical components behave, such as a force calculator or a signal router. Before any wire is drawn, every block must be understood on its own terms: what it receives, what it produces, and what role it plays in the broader system.

### Config

This is the physics engine settings block. It tells MATLAB how to solve the physical equations.Every Simscape network needs exactly one of these. It has no physical frame ports , it connectes to the world frame to govern the entire system . Any MATLAB system requires exactly one of these.

### World Frame 

This is the absolute ground reference for the entire 3D world - the absolute origin . Without this block MATLAM simscape enviornment doesn't know where anything exists in space , connecting every physical block to this world frame is necessary or else "Floating in space" error occurs. 

### Init Box 6-DOF Joint

A 6 Degrees-of-Freedom joint connecting the World Frame to the Box. It allows the Box to move freely in all 6 directions -3 translational (X, Y, Z) and 3 rotational (roll, pitch, yaw). its a joint which connects the box with worldframe , the contact forces from the belt works on the box because of this , without this joint the box will be rigidly fixed in the 3d space , we want a free floating rigid body.

### Box (blue block)
The rigid body representing the physical box being picked and placed. It has two frame ports:

Fa (top face) — used by the gripper to grab the box from above
Fb (bottom face) — used by the belt contact force blocks to push the box along


### Damper Gripper Force
This block computes the contact and damping forces between the gripper fingers and the box surface. It uses physical frame data (the box top face Bfa) plus an energy/effort signal (E) and the second box frame (Fb) to calculate how hard the gripper is pressing. Its output goes into the Gripper block to simulate the grip physically.


### Gripper
The gripper arm subsystem — contains the post, rod, and two fingers (A and B) driven by prismatic joints. It has 4 input ports driven entirely by signal commands:
PortSignalMeaningb (Finger z)xFHow far the fingers open/closeE (Gripper q)qFRotation angle of the gripper heada (Post z)zPVertical height of the postP (Post q)qQRotation of the post (swinging arm)
Internally, a gain of −1 inverts the signal to Finger B so both fingers move symmetrically inward to grip and outward to release.

### Commands (Box Test)

The master signal source — a pre-programmed sequence of timed motion commands that drives the entire pick-and-place operation. It outputs 6 signals:

### Box to Belt Out Force and Box to Belt In Force

These blocks compute the contact forces between the box's bottom face and each belt surface. They model what happens physically when a solid object sits on a moving conveyor — the belt pushes it forward via friction. Ports:

PlaB — the physical frame of the belt plane (so it knows the belt's position and orientation)

FacF — the contact face force parameters (stiffness, damping, friction)

bus On — enable/disable signal to activate the force computation

Out — outputs the resulting physical frame data (used by the Goto blocks)

### Belt Out and Belt In
The conveyor belt subsystems, each containing 5 rollers driven by revolute joints. Ports:

Spd — speed input signal (from Commands)

Ctr — control/enable signal

End — the end frame port (physical frame output of the belt structure)

Internally, a gain + integrator converts the speed signal into a roller rotation angle over time. Belt In was already connected in the starter file and served as the reference to figure out Belt Out.

### transform belt out and belt in

A Rigid Transform block that defines where Belt Out sits in 3D space and which way it faces, relative to the World Frame. You configured it with a 180° rotation about the +Z axis because the outgoing belt faces the opposite direction to the incoming belt — they carry the box in opposite directions. This is a pure frame positioning block; it has no signal ports, only frame ports.

### GOTO blocks 

Signal routing blocks that let you pass a frame/signal across the canvas without drawing a long messy wire. A Goto block tags a signal with a name; a From block anywhere in the model picks it up using the same tag.













