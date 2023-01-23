from generativepy.tween import Tween, set_frame_rate

# Set global frame rate to 4
set_frame_rate(4)

# Create a tween. Times are in seconds (1 sec = 4 frames)
tween = Tween(3.0).wait(2).to(12.0, 5).wait(6.5).set(7.0).wait(7)

# You can use len() to fund the length of the tween in frames
print('Length = ', len(tween))

# You can access the value for a particular frame using indexing []
# or the get() function.
print('tween[6] (1.5 seconds) = ', tween[6])
print('tween[12] (3 seconds) = ', tween.get(12))
print('tween[80] (20 seconds) = ', tween.get(80))

# The tween can be accessed as a sequence. Here we use a list
# comprehension to convert the values to strings that print the
# entire sequence
strings = [str(x) for x in tween]
print(', '.join(strings))

