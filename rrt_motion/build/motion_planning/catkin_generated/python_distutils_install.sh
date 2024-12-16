#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/shashank/rrt_motion/src/motion_planning"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/shashank/rrt_motion/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/shashank/rrt_motion/install/lib/python3/dist-packages:/home/shashank/rrt_motion/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/shashank/rrt_motion/build" \
    "/usr/bin/python3" \
    "/home/shashank/rrt_motion/src/motion_planning/setup.py" \
     \
    build --build-base "/home/shashank/rrt_motion/build/motion_planning" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/shashank/rrt_motion/install" --install-scripts="/home/shashank/rrt_motion/install/bin"
