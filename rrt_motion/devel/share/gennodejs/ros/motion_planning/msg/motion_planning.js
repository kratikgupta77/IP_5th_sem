// Auto-generated. Do not edit!

// (in-package motion_planning.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class motion_planning {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.turtlebot_twist = null;
      this.orientation = null;
      this.path = null;
    }
    else {
      if (initObj.hasOwnProperty('turtlebot_twist')) {
        this.turtlebot_twist = initObj.turtlebot_twist
      }
      else {
        this.turtlebot_twist = [];
      }
      if (initObj.hasOwnProperty('orientation')) {
        this.orientation = initObj.orientation
      }
      else {
        this.orientation = [];
      }
      if (initObj.hasOwnProperty('path')) {
        this.path = initObj.path
      }
      else {
        this.path = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type motion_planning
    // Serialize message field [turtlebot_twist]
    // Serialize the length for message field [turtlebot_twist]
    bufferOffset = _serializer.uint32(obj.turtlebot_twist.length, buffer, bufferOffset);
    obj.turtlebot_twist.forEach((val) => {
      bufferOffset = geometry_msgs.msg.Twist.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [orientation]
    bufferOffset = _arraySerializer.float64(obj.orientation, buffer, bufferOffset, null);
    // Serialize message field [path]
    // Serialize the length for message field [path]
    bufferOffset = _serializer.uint32(obj.path.length, buffer, bufferOffset);
    obj.path.forEach((val) => {
      bufferOffset = geometry_msgs.msg.Point.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type motion_planning
    let len;
    let data = new motion_planning(null);
    // Deserialize message field [turtlebot_twist]
    // Deserialize array length for message field [turtlebot_twist]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.turtlebot_twist = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.turtlebot_twist[i] = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [orientation]
    data.orientation = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [path]
    // Deserialize array length for message field [path]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.path = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.path[i] = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 48 * object.turtlebot_twist.length;
    length += 8 * object.orientation.length;
    length += 24 * object.path.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'motion_planning/motion_planning';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0247c14c3a73b7bc94615f398d116434';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    geometry_msgs/Twist[] turtlebot_twist
    float64[] orientation
    geometry_msgs/Point[] path
    
    ================================================================================
    MSG: geometry_msgs/Twist
    # This expresses velocity in free space broken into its linear and angular parts.
    Vector3  linear
    Vector3  angular
    
    ================================================================================
    MSG: geometry_msgs/Vector3
    # This represents a vector in free space. 
    # It is only meant to represent a direction. Therefore, it does not
    # make sense to apply a translation to it (e.g., when applying a 
    # generic rigid transformation to a Vector3, tf2 will only apply the
    # rotation). If you want your data to be translatable too, use the
    # geometry_msgs/Point message instead.
    
    float64 x
    float64 y
    float64 z
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new motion_planning(null);
    if (msg.turtlebot_twist !== undefined) {
      resolved.turtlebot_twist = new Array(msg.turtlebot_twist.length);
      for (let i = 0; i < resolved.turtlebot_twist.length; ++i) {
        resolved.turtlebot_twist[i] = geometry_msgs.msg.Twist.Resolve(msg.turtlebot_twist[i]);
      }
    }
    else {
      resolved.turtlebot_twist = []
    }

    if (msg.orientation !== undefined) {
      resolved.orientation = msg.orientation;
    }
    else {
      resolved.orientation = []
    }

    if (msg.path !== undefined) {
      resolved.path = new Array(msg.path.length);
      for (let i = 0; i < resolved.path.length; ++i) {
        resolved.path[i] = geometry_msgs.msg.Point.Resolve(msg.path[i]);
      }
    }
    else {
      resolved.path = []
    }

    return resolved;
    }
};

module.exports = motion_planning;
