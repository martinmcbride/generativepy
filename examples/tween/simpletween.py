from generativepy.tween import Tween

# Create a tween
tween = Tween(3.0).wait(4).to(13.0, 5).wait(2).set(7.0, 4)

# You can use len() to fund the length of the tween in frames
print('Length = ', len(tween))

# You can access the vale#ue for a particular frame using indexing []
# or the get() function.
print('tween[7] = ', tween[5])
print('tween[8] = ', tween.get(7))

# The tween can be accessed as a sequence. Here we use a list
# comprehension to convert the values to strings that print the
# entire sequence
strings = [str(x) for x in tween]
print(', '.join(strings))

