# Quanzer

ROS2-workspace for styring og visualisering av Quanser Qube-systemet.
Prosjektet inneholder robotmodell, hardware-driver, regulatorer og launch-filer for simulering og testing.

## Prosjektbeskrivelse

Dette prosjektet implementerer styring, visualisering og kommunikasjon for Quanser Qube i ROS2. Systemet inkluderer drivere, robotmodell, launch-filer og regulatorer for simulering og testing.

## Innhold
### Pakker

Prosjektet består av flere ROS2-pakker:

- `qube_bringup` - launch-filer og oppstart av systemet
- `qube_controller` - regulering/styring av Qube
- `qube_description` - URDF/modellbeskrivelse
- `qube_driver` - kommunikasjon med fysisk system

  
### `qube_bringup`
Launch-filer for oppstart av hele systemet.

### `qube_controller`
Inneholder regulatorer og kontrollnoder.

### `qube_description`
Inneholder URDF/Xacro-modell og RViz-konfigurasjon.

### `qube_driver`
Håndterer kommunikasjon med fysisk Quanser Qube.


## Krav

- Ubuntu 24.04
- ROS2 Jazzy
- Python 3
- colcon

## Avhengigheter

- xacro
- rviz2
- robot_state_publisher
- joint_state_publisher_gui

## Bygge prosjektet

Kjør fra rotmappen:

```bash
source /opt/ros/jazzy/setup.bash
colcon build
```
## Kjøre prosjektet

### Terminal 1
```bash
source install/setup.bash
ros2 launch qube_bringup bringup.launch.py
```
### Terminal 2
```bash
source install/setup.bash
ros2 run qube_controller controller_node
```
