script init:
print init.txt normal 0 0 .60 20 60
spawnmonster jorogumo jorogumo.egg 0 30 5 4 4 1.25 0.1
spawnproxtrigger scream 0 40 5 5 player player norunonce 100
spawnproxtrigger jorostartmove 0 30 5 10 player player runonce 0
spawnproxtrigger joroturn 30 25 5 5 jorogumo monster norunonce 100
spawnproxtrigger joroturn 35 50 5 5 jorogumo monster norunonce 100
spawnproxtrigger joroturn -30 55 5 5 jorogumo monster norunonce 100
spawnproxtrigger joroturn -35 30 5 5 jorogumo monster norunonce 100
spawnproxtrigger music1 0 -30 5 5 player player norunonce 100
spawnproxtrigger music2 0 40 5 5 player player norunonce 100
end init

script jorostartmove:
anim jorogumo Walk loop
walkforward jorogumo
end jorostartmove

script joroturn:
turn jorogumo 90 ccw
end joroturn1

script music1:
changemusic MountainsOfMadness.mp3 0.8
end music1

script music2:
changemusic CreaturesDark.mp3 0.8
end music2

script scream:
playsound FemaleScream5.mp3 0.7 0 noloop
end scream