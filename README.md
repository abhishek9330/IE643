#data_modification folder contains all the scripts that were used to extract the labels, filter the classes, and apply motion blur.

#interface folder contains all code files used for the interface including the flask backend, templates, etc.

#model folder contains all the models obtained/used during the project.

#training_notebook.ipynb is the saved notebook from kaggle that we used for the training. Please follow through the code to see the following commands in action

#Command to train the model:-

yolo task=detect mode=train model=<model path> data=<data.yaml> epochs=<number of epochs> lr=0.000833 optimizer=AdamW
data.yaml content looks like following:

yaml_content = """
train: /kaggle/input/finalt/T/T9/images/train
val: /kaggle/input/finalt/T/T9/images/train

 Number of classes
nc: 8

names:
  0: person
  1: bicycle
  2: car
  3: motorcycle
  4: airplane
  5: bus
  6: train
  7: truck
"""


#Command to infer:-
yolo task=detect mode=predict model=<model path> source=<inference data path>

#To run the interface, run the command:
pip install Flask werkzeug
python main.py

Note: set the paths according to the code in your repo while running the scripts, especially the data related ones







