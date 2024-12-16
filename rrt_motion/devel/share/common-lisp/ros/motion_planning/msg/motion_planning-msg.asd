
(cl:in-package :asdf)

(defsystem "motion_planning-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "motion_planning" :depends-on ("_package_motion_planning"))
    (:file "_package_motion_planning" :depends-on ("_package"))
  ))