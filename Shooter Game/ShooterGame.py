from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

counter = 0
app = Ursina()

platform = Entity(model="plane", scale=(100,1,100), color=color.white, texture="white_cube", texture_scale=(100, 100), collider="box")

player = FirstPersonController(model="cube", y=0, origin_y=0.5, speed=20)

wall1 = Entity(model="cube", texture="brick",scale=(24,12, 1), color=color.gray, collider='box', x=0, z=-6)
wall2 = Entity(model="cube", texture="brick",scale=(24,12, 1), color=color.red, collider='box', x=0, z=22)

wall3 = Entity(model="cube", texture="brick",scale=(28,12, 1), color=color.blue, collider='box', x=-12, z=8, rotation_y=90)
wall4 = Entity(model="cube", texture="brick",scale=(28,12, 1), color=color.green, collider='box', x=12, z=8, rotation_y=90)

targets = []
bullets= []
for _ in range(11):
    x = random.randrange(-9, 9, 2)
    y = random.randrange(1, 6, 1)
    z = random.randrange(3, 21, 2)
    target = Entity(model="cube", color=color.white, texture="Devil-Emoji.png", scale=(1,1,0.1), dx=0.05, position=(x,y,z), collider="box")
    target.collider = BoxCollider(target, size=(3,3,3))
    targets.append(target)

gun = Entity(parent=camera, model='blast/3D/gun.obj', origin_y=-0.5, scale=(0.1,0.1,0.1), position = (2,-1,3), collider='box', rotation=(0,-90,0))
player.gun = gun

def input(key):
    global bullets,counter
    if key == "left mouse down" and player.gun:
        bullet = Entity(parent=gun, model='cube', scale=(1, 1, 1), position=(0.8, 2.5,0), speed=5, color=color.black, collider='box', rotation_y=90)
        bullets.append(bullet)
        gun.blink(color.white)
        bullet.world_parent = scene
        counter +=1
        if counter >= 25:
            message = Text(text="You used all your bullet!", scale = 1.5, origin=(0,0), background=True, color=color.blue)
            application.pause()
def update():
    if held_keys["escape"]:
        application.quit()

    for target in targets:
        target.x += target.dx
        if target.x >9:
            target.x = 9
            target.dx *= -1
        if target.x <-9:
            target.x = -9
            target.dx *= -1

    global bullets
    if len(bullets) > 0:
        for bullet in bullets:
            bullet.position += bullet.forward * 8

            hit_info = bullet.intersects()
            if hit_info.hit:
                if hit_info.entity in  targets:
                    targets.remove(hit_info.entity)
                    destroy(hit_info.entity)
                    destroy(bullet)
                    bullets.remove(bullet)
                    if len(targets) == 0:
                        message = Text(text="You Won!", scale = 1.5, origin=(0,0), background=True, color=color.blue)
                    


if __name__ == "__main__":
    app.run()