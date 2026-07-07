# can_simulator
## 2. CAN 车速模拟器 (`can_simulator.py`)
*   **功能定位**：模拟实车 CAN 总线上报的轮速/车速信号，供 Pure Pursuit 等控制算法计算动态前视距离。
*   **输入**：直接读取 `vehicle_model` 内部计算出的 Ground Truth 实际车速（无需加噪声，因为真车此处也是直接反馈）。
*   **输出**：发布 `/localization/velocity` (`geometry_msgs/TwistStamped`)，`twist.linear.x = gt.speed`。
