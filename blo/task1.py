from pygame import*

W,H = 800,500
win = display.set_mode((W,H))
display.set_caption("Blockada")

game= True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
    display.update()