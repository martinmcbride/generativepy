from generativepy.bitmap import Scaler

scaler = Scaler(300, 200, width=3, height=2, startx=-1.5, starty=-1)

print(scaler.user_to_device(1, .5))
print(scaler.device_to_user(20, 50))
