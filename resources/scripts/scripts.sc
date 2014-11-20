script init:
print init.txt normal 0 0 .60 20 60
spawnproxtrigger scream 0 40 5 5 player player norunonce 100
spawnproxtrigger jumostartmove 0 30 5 10 player player runonce 0
spawnproxtrigger jumoturn 30 25 5 5 jumogoro monster norunonce 100
spawnproxtrigger jumoturn 35 50 5 5 jumogoro monster norunonce 100
spawnproxtrigger jumoturn -30 55 5 5 jumogoro monster norunonce 100
spawnproxtrigger jumoturn -35 30 5 5 jumogoro monster norunonce 100
spawnproxtrigger music1 0 -30 5 5 player player norunonce 100
spawnproxtrigger music2 0 40 5 5 player player norunonce 100
end init

script jumostartmove:
walkforward jumogoro
end jumostartmove

script jumoturn:
turn jumogoro 90 ccw
end jumoturn1

script music1:
changemusic MountainsOfMadness.mp3 0.8
end music1

script music2:
changemusic CreaturesDark.mp3 0.8
end music2

script scream:
playsound FemaleScream5.mp3 0.7 0 noloop
end scream