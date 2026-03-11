#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import sys, select, termios, tty

# Settings to allow key detection
settings = termios.tcgetattr(sys.stdin)

def get_key():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
        # Arrow keys send a sequence of 3 bytes: \x1b, [, A/B/C/D
        if key == '\x1b':
            sys.stdin.read(1) # Skip the '['
            arrow = sys.stdin.read(1) # Read the letter (A, B, C, or D)
            return arrow
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class ArrowKeyDriver(Node):
    def __init__(self):
        super().__init__('keyboard_driver')
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        # Initial Positions
        self.joint1 = 0.0 # Base Rotation
        self.joint2 = 0.0 # Arm Lift

        # Create a timer to keep the robot visible (20Hz)
        self.timer = self.create_timer(0.05, self.publish_joints)

        print("\n=====================================")
        print(" ARROW KEY ROBOT CONTROLLER")
        print("=====================================")
        print("  [UP]    : Lift Arm")
        print("  [DOWN]  : Lower Arm")
        print("  [LEFT]  : Rotate Left")
        print("  [RIGHT] : Rotate Right")
        print("  [Q]     : Quit")
        print("=====================================\n")

    def publish_joints(self):
        # 1. Read Key
        key = get_key()
        move_speed = 0.1

        # 2. Logic for Arrow Keys
        if key == 'A':  # UP Arrow
            self.joint2 -= move_speed
            print(f"UP: Lifting...      [{self.joint2:.2f}]")
        elif key == 'B': # DOWN Arrow
            self.joint2 += move_speed
            print(f"DOWN: Lowering...   [{self.joint2:.2f}]")
        elif key == 'D': # LEFT Arrow
            self.joint1 += move_speed
            print(f"LEFT: Turning...    [{self.joint1:.2f}]")
        elif key == 'C': # RIGHT Arrow
            self.joint1 -= move_speed
            print(f"RIGHT: Turning...   [{self.joint1:.2f}]")
        elif key == 'q':
            print("Quitting...")
            sys.exit(0)

        # 3. Publish to RViz
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint_1', 'joint_2']
        msg.position = [self.joint1, self.joint2]
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ArrowKeyDriver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
