# Quanzer

ROS2-prosjekt for Quanser/Qube-systemet.

## Innhold

Prosjektet består av flere ROS2-pakker:

- `qube_bringup` - launch-filer og oppstart av systemet
- `qube_controller` - regulering/styring av Qube
- `qube_description` - URDF/modellbeskrivelse
- `qube_driver` - kommunikasjon med fysisk system

## Krav

- ROS2 Jazzy
- colcon
- Python 3
- C++

## Bygge prosjektet

Kjør fra rotmappen:

```bash
source /opt/ros/jazzy/setup.bash
colcon build