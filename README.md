# Quanzer

ROS2-prosjekt for Quanser/Qube-systemet.

## Prosjektbeskrivelse

Dette prosjektet implementerer styring, visualisering og kommunikasjon for Quanser Qube i ROS2. Systemet inkluderer drivere, robotmodell, launch-filer og regulatorer for simulering og testing.

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
