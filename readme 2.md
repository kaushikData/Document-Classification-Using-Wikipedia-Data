Data Collection

1. Run GTA V in an 800x600 window and place it on the top left corner on the screen.

2. Execute collect_data.py and start playing the game. This will grab all the frames and associate them with the input key used at that point. 

We have collected over 10 hours of data for this project.

Training and Balancing Data

1. Execute train.py, which will use "training_data.npy" that was created as part of data collection.

2. Execute preprocess_labels.py to ensure all key captures are balanced by down-sampling.

Test Data

1. Run GTA V in a 800x600 window and place it on the top-left corner of the screen.

2. Execute test.py and ensure the GTA V screen has focus.

3. The code will start playing the game.