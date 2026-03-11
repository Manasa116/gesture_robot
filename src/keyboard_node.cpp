#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <termios.h>
#include <unistd.h>
#include <iostream>

// Function to capture key presses without waiting for Enter
char getch() {
    struct termios oldt, newt;
    char ch;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    ch = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return ch;
}

class KeyboardDriver : public rclcpp::Node {
public:
    KeyboardDriver() : Node("keyboard_driver") {
        publisher_ = this->create_publisher<sensor_msgs::msg::JointState>("/joint_states", 10);

        joint1_pos = 0.0;
        joint2_pos = 0.0;

        RCLCPP_INFO(this->get_logger(), "Keyboard Control Started!");
        RCLCPP_INFO(this->get_logger(), "Use 'A'/'D' for Base, 'W'/'S' for Arm. 'Q' to Quit.");
    }

    void run_input_loop() {
        while (rclcpp::ok()) {
            char c = getch(); // Wait for keypress

            if (c == 'a') joint1_pos += 0.1;
            if (c == 'd') joint1_pos -= 0.1;
            if (c == 'w') joint2_pos += 0.1;
            if (c == 's') joint2_pos -= 0.1;
            if (c == 'q') break;

            publish_joints();
        }
    }

private:
    void publish_joints() {
        auto msg = sensor_msgs::msg::JointState();
        msg.header.stamp = this->now();
        msg.name = {"joint_1", "joint_2"};
        msg.position = {joint1_pos, joint2_pos};
        publisher_->publish(msg);

        // Print current status
        std::cout << "Joint 1: " << joint1_pos << " | Joint 2: " << joint2_pos << "\r" << std::flush;
    }

    rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr publisher_;
    double joint1_pos, joint2_pos;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<KeyboardDriver>();

    // Start the loop to listen for keys
    node->run_input_loop();

    rclcpp::shutdown();
    return 0;
}
