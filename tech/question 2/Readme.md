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

### bus on

The bus On port is essentially an on/off switch for the contact force calculation inside the Box to Belt Force blocks.The reason we need this is because the contact force block is always present in the model and is always capable of computing forces. Without something to gate it, it would keep trying to calculate contact forces even when the belt is completely stopped, which would cause incorrect behavior where the box gets pushed by a belt that is not even moving. The bus On port prevents that by tying the force computation directly to whether the belt is actually active or not.



Grounding Everything to the World 
The World Frame block is the starting point of the entire physical world. Every mechanical component needs to trace back to it, otherwise MATLAB does not know where anything exists in 3D space.
The World Frame connects to the Config block so the physics solver knows the global reference it is working with.
The World Frame also connects to transform belt out. This gives the outgoing belt a fixed starting point in the real world to be positioned from.
The World Frame connects to transform belt in as well. Same idea, the incoming belt also needs to know its place in the world.
The World Frame connects to the Init Box 6-DOF Joint. This anchors the box into the world so it can exist physically and be free to move around.

Placing the Belts in the Right Position and Direction
transform belt out connects to the Belt Out subsystem. This connection is what actually places Belt Out at the correct spot in 3D space and makes it face the right direction. The 180 degree rotation we configured inside transform belt out is carried through this connection and without it, Belt Out would have no idea where to exist or which way to face.
transform belt in connects to the Belt In subsystem. Same logic applies. The minus 90 degree rotation we configured inside transform belt in is delivered to Belt In through this connection, aligning the incoming belt so the box arrives from the correct direction.

Placing the Box in the World and Letting It Move
The Init Box 6-DOF Joint connects to the Box block. This is the connection that actually puts the box into the simulation and gives it the freedom to slide, lift, swing, and land. The 6-DOF joint allows movement in all directions so the box is not stuck in place.

Connecting the Box to the Gripper Fingers
The Box has two frame ports, Fa and Fb, one for each finger of the gripper.
Fa on the Box connects to the Bfa port on the Damper Gripper Force block. This tells the force block exactly where Finger A is making contact with the box surface, so it can calculate the physical gripping force correctly.
Fb on the Box connects to the Fb port on the Damper Gripper Force block. This does the same thing for Finger B. Both connections together allow the Damper Gripper Force block to know the contact point of both fingers simultaneously and compute a realistic grip.
The output of the Damper Gripper Force block then connects into the Gripper subsystem. This delivers the calculated contact and damping force into the gripper so the grip is physically meaningful rather than just a number.

Connecting the Box to the Belt Contact Force Blocks
The Box to Belt Out Force block and Box to Belt In Force block are responsible for calculating the push that the belts apply to the box. For them to work, they need two things, the position of the belt surface and the position of the box itself.
The End frame port of Belt Out connects to the Box to Belt Out Force block. This tells the force block where the outgoing belt surface is sitting in 3D space.
The End frame port of Belt In connects to the Box to Belt In Force block. Same reason, the incoming belt surface position is passed to the force block so it knows the geometry of the contact.
The Out port of Box to Belt Out Force connects to the Goto block tagged as Out. The Out port of Box to Belt In Force connects to the Goto block tagged as In. These Goto blocks are just a cleaner way of routing these frame signals across the diagram without drawing wires all the way to the right side of the canvas.
On the right side, the From block tagged In connects to the B2 and Fn2 subsystem. The From block tagged Out connects to the B1 and Fn1 subsystem. These deliver the contact frame data to the force parameter blocks that need it.

Sending Commands to the Gripper
All four of these connections come from the Commands block and go into the Gripper subsystem. They are grouped together because they all exist for the same reason, to tell the gripper what to do and when to do it.
The xF signal from Commands goes into the Finger z port of the Gripper. This controls how much the fingers open or close.
The qF signal from Commands goes into the Gripper q port. This controls the rotation angle of the gripper head.
The zP signal from Commands goes into the Post z port. This raises and lowers the arm so the gripper can pick up and put down the box.
The qQ signal from Commands goes into the Post q port. This swings the arm sideways, carrying the box from above Belt In all the way over to above Belt Out.

Sending Speed Commands to the Belts
The Belt Out signal from Commands connects to the Spd port of Belt Out. This tells the outgoing belt how fast to spin its rollers.
The Belt In signal from Commands connects to the Spd port of Belt In. Same thing for the incoming belt.

Activating the Contact Forces Only When the Belt Is Running
The control output of Belt Out connects to the bus On port of Box to Belt Out Force. This connection acts like a switch where the contact force between the box and the outgoing belt is only active when the belt is actually moving. If the belt is stopped, this signal turns off the force calculation so the box is not pushed when it should not be.
The control output of Belt In connects to the bus On port of Box to Belt In Force for the exact same reason. The incoming belt contact force is only computed when Belt In is running













