script jumostartmove:
walkforward jumogoro
end jumostartmove

script jumoturn1:
turn jumogoro 90 ccw
end jumoturn1

script initprint:
print init.txt normal 0 0 .60 20 60
end initprint

script music1:
changemusic MountainsOfMadness.mp3 0.4
end music1

script music2:
changemusic CreaturesDark.mp3 0.4
end music2

script scream:
playsound FemaleScream5.mp3 0.7 0 noloop
end scream