script init:
print init.txt normal 0 0 .60 20 -1
spawnmonster jorogumo jorogumo.egg 0 30 5 4 4 1.25 0.1
spawnmonster kappa kappa.egg 0 10 5 5 1.5 1.25 0.1
anim kappa Idle loop
spawnitem cucumber cucumber.egg 10 10 5 1 1 1 false true true
spawnitem toilet toilet.egg 20 10 5 2 1.5 1.5 false false true
spawnitem the_book monster_book.egg -66 -17 .25 1 1 1 false false true
spawnitem page1 monster_book_page.egg -19 85 0.4 1 1 1 true false true
spawnitem page2 monster_book_page.egg 53 170 0.4 1 1 1 true false true
spawnitem page3 monster_book_page.egg 37 265 0.5 1 1 1 true false true
spawnitem page4 monster_book_page.egg -202 62 0.4 1 1 1 true false true
spawnitem page5 monster_book_page.egg 188 27 0.4 1 1 1 true false true
spawnitem page6 monster_book_page.egg 190 182 0.4 1 1 1 true false true
spawnproxtrigger scream 0 40 5 5 player player norunonce 100
spawnproxtrigger jorostartmove 0 30 5 10 player player runonce 0
spawnproxtrigger joroturn 30 25 5 5 jorogumo monster norunonce 100
spawnproxtrigger joroturn 35 50 5 5 jorogumo monster norunonce 100
spawnproxtrigger joroturn -30 55 5 5 jorogumo monster norunonce 100
spawnproxtrigger joroturn -35 30 5 5 jorogumo monster norunonce 100
spawnproxtrigger jorodelete 0 -40 5 5 player player runonce 100
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

script jorodelete:
despawn jorogumo
print why.txt normal 0 0 -.30 30 80
end jorodelete

script music1:
changemusic MountainsOfMadness.ogg 0.8
end music1

script music2:
changemusic CreaturesDark.ogg 0.8
end music2

script scream:
playsound FemaleScream5.ogg 0.7 0 noloop
end scream
