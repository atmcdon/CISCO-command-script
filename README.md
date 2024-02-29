# CISCO-command-script

This Program is designed for CISCO routers and switchs, when connected to a
router or switch via a console cable.

USE CASE: This was intended to pull infomation from the routers and switches as well,
set up for inital config. While recording the results.

WHAT THE PROGRAM DOES:
This program INPUTS/reads "commands.txt" and runs and excecutes the commands.
  The first command is the routers host name.
  terminal length 0 is used to be able to read the whole command at once.

Then OUTPUTS the results of the commands to a txt file.

EXAMPLE: Commands.txt file.
NOTE: the space in between the router is intentional and will act
as if the user presses <enter>
R1

en
terminal length 0
show version
show inventory
show interfaces
show ipv6 interface brief
show sdm prefer
