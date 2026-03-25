#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>

class PIDController
{
public:
  PIDController(double kp, double ki, double kd)
  : kp_(kp), ki_(ki), kd_(kd), integral_(0.0), prev_error_(0.0) {}

  double compute(double error, double dt)
  {
    if (dt <= 0.0) return 0.0;
    integral_ += error * dt;
    double derivative = (error - prev_error_) / dt;
    prev_error_ = error;
    return kp_ * error + ki_ * integral_ + kd_ * derivative;
  }

private:
  double kp_, ki_, kd_;
  double integral_, prev_error_;
};

class QubeControllerNode : public rclcpp::Node
{
public:
  QubeControllerNode() : Node("qube_controller")
  {
    this->declare_parameter("kp", 5.0);
    this->declare_parameter("ki", 0.1);
    this->declare_parameter("kd", 0.5);
    this->declare_parameter("reference_angle", 0.0);

    double kp = this->get_parameter("kp").as_double();
    double ki = this->get_parameter("ki").as_double();
    double kd = this->get_parameter("kd").as_double();
    reference_ = this->get_parameter("reference_angle").as_double();

    pid_ = std::make_unique<PIDController>(kp, ki, kd);

    param_callback_handle_ = this->add_on_set_parameters_callback(
  [this](const std::vector<rclcpp::Parameter> & params) {
    for (const auto & param : params) {
      if (param.get_name() == "reference_angle") {
        reference_ = param.as_double();
        RCLCPP_INFO(this->get_logger(), "Reference angle updated to: %f", reference_);
      }
    }
    rcl_interfaces::msg::SetParametersResult result;
    result.successful = true;
    return result;
  });

    subscription_ = this->create_subscription<sensor_msgs::msg::JointState>(
      "/joint_states", 10,
      std::bind(&QubeControllerNode::joint_states_callback, this, std::placeholders::_1));

    publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(
      "/velocity_controller/commands", 10);

    RCLCPP_INFO(this->get_logger(), "QubeControllerNode started");
  }

private:
  void joint_states_callback(const sensor_msgs::msg::JointState::SharedPtr msg)
  {
    // Find motor_joint in the message
    auto it = std::find(msg->name.begin(), msg->name.end(), "motor_joint");
    if (it == msg->name.end()) return;

    int idx = std::distance(msg->name.begin(), it);
    double position = msg->position[idx];

    rclcpp::Time now = this->get_clock()->now();
    if (!last_time_.has_value()) {
      last_time_ = now;
      return;
    }

    double dt = (now - last_time_.value()).seconds();
    last_time_ = now;

    double error = reference_ - position;
    double command = pid_->compute(error, dt);

    // Float64MultiArray: data må være en liste
    std_msgs::msg::Float64MultiArray out_msg;
    out_msg.data = {command};
    publisher_->publish(out_msg);
  }

  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr subscription_;
  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
  std::unique_ptr<PIDController> pid_;
  std::optional<rclcpp::Time> last_time_;
  double reference_;
  rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr param_callback_handle_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<QubeControllerNode>());
  rclcpp::shutdown();
  return 0;
}