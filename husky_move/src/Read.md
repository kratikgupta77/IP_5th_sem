

# **Husky Robot Square Path Simulation**

This project simulates the movement of a Husky robot in a Gazebo environment using ROS Noetic. The robot follows a square path and returns to its starting position, all controlled by a Python script.

---

## **How to Run**

Follow these steps to set up and execute the simulation:

### **Step 1: Download the Project**
- Clone or download this repository into your ROS workspace (`husky_move`).
  ```bash
  git clone <repository-link>
  ```
  Replace `<repository-link>` with the URL of this repository.

### **Step 2: Move to Workspace**
- Navigate to the root of your workspace:
  ```bash
  cd ~/husky_move
  ```

### **Step 3: Build the Workspace**
- Build the workspace using `catkin_make`:
  ```bash
  catkin_make
  ```

### **Step 4: Source the Workspace**
- Source the workspace to set up environment variables:
  ```bash
  source devel/setup.bash
  ```

### **Step 5: Launch Gazebo with Husky Robot**
- Launch the Gazebo simulation with a single Husky robot:
  ```bash
  roslaunch husky_gazebo empty_world.launch
  ```
  This opens the Gazebo simulator with the Husky robot in an empty world.

### **Step 6: Run the Python Script**
1. Open a new terminal.
2. Source the workspace:
   ```bash
   source ~/husky_move/devel/setup.bash
   ```
3. Run the Python script to move the Husky robot in a square path:
   ```bash
   rosrun husky_square_move move_in_square.py
   ```

---

## **Expected Behavior**
- The Husky robot will move in a square path with each side of a specified length.
- After completing the square, the robot will return to its starting position.
- The visited points in the path will be logged to the console.

---

## **Dependencies**
Make sure the following dependencies are installed:

1. **ROS Noetic**:
   - Install using:
     ```bash
     sudo apt install ros-noetic-desktop-full
     ```

2. **Husky Simulation Packages**:
   - Install using:
     ```bash
     sudo apt install ros-noetic-husky-simulator
     ```

3. **Python Dependencies**:
   - Ensure Python 3 is installed with the following ROS packages:
     - `rospy`
     - `geometry_msgs`
     - `nav_msgs`

---

## **Files and Directory Structure**

```
husky_move/
├── src/
│   ├── husky/  # Husky robot simulation packages
│   ├── husky_square_move/  # Custom package for square path movement
│   │   ├── CMakeLists.txt
│   │   ├── package.xml
│   │   ├── scripts/
│   │   │   └── move_in_square.py  # Python script for square path movement
```

---

## **Credits**
This project uses Clearpath Robotics' Husky robot simulation packages.

For further information or issues, feel free to contact [Your Name/Email].

