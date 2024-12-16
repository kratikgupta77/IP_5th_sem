;; Auto-generated. Do not edit!


(when (boundp 'motion_planning::motion_planning)
  (if (not (find-package "MOTION_PLANNING"))
    (make-package "MOTION_PLANNING"))
  (shadow 'motion_planning (find-package "MOTION_PLANNING")))
(unless (find-package "MOTION_PLANNING::MOTION_PLANNING")
  (make-package "MOTION_PLANNING::MOTION_PLANNING"))

(in-package "ROS")
;;//! \htmlinclude motion_planning.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass motion_planning::motion_planning
  :super ros::object
  :slots (_turtlebot_twist _orientation _path ))

(defmethod motion_planning::motion_planning
  (:init
   (&key
    ((:turtlebot_twist __turtlebot_twist) ())
    ((:orientation __orientation) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:path __path) ())
    )
   (send-super :init)
   (setq _turtlebot_twist __turtlebot_twist)
   (setq _orientation __orientation)
   (setq _path __path)
   self)
  (:turtlebot_twist
   (&rest __turtlebot_twist)
   (if (keywordp (car __turtlebot_twist))
       (send* _turtlebot_twist __turtlebot_twist)
     (progn
       (if __turtlebot_twist (setq _turtlebot_twist (car __turtlebot_twist)))
       _turtlebot_twist)))
  (:orientation
   (&optional __orientation)
   (if __orientation (setq _orientation __orientation)) _orientation)
  (:path
   (&rest __path)
   (if (keywordp (car __path))
       (send* _path __path)
     (progn
       (if __path (setq _path (car __path)))
       _path)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Twist[] _turtlebot_twist
    (apply #'+ (send-all _turtlebot_twist :serialization-length)) 4
    ;; float64[] _orientation
    (* 8    (length _orientation)) 4
    ;; geometry_msgs/Point[] _path
    (apply #'+ (send-all _path :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Twist[] _turtlebot_twist
     (write-long (length _turtlebot_twist) s)
     (dolist (elem _turtlebot_twist)
       (send elem :serialize s)
       )
     ;; float64[] _orientation
     (write-long (length _orientation) s)
     (dotimes (i (length _orientation))
       (sys::poke (elt _orientation i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; geometry_msgs/Point[] _path
     (write-long (length _path) s)
     (dolist (elem _path)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Twist[] _turtlebot_twist
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _turtlebot_twist (let (r) (dotimes (i n) (push (instance geometry_msgs::Twist :init) r)) r))
     (dolist (elem- _turtlebot_twist)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; float64[] _orientation
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _orientation (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _orientation i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; geometry_msgs/Point[] _path
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _path (let (r) (dotimes (i n) (push (instance geometry_msgs::Point :init) r)) r))
     (dolist (elem- _path)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get motion_planning::motion_planning :md5sum-) "0247c14c3a73b7bc94615f398d116434")
(setf (get motion_planning::motion_planning :datatype-) "motion_planning/motion_planning")
(setf (get motion_planning::motion_planning :definition-)
      "geometry_msgs/Twist[] turtlebot_twist
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

")



(provide :motion_planning/motion_planning "0247c14c3a73b7bc94615f398d116434")


