# What I Built

- I collected the model predictions for each example in the dataset using the
Humanloop API and stored the enriched data in a SQL DB. This is done in
`create_enriched_db.py` which doesn't need to be run as I have provided the
DB in the zip file.
- I created a command-line app that has two modes: one for viewing and updating
potential mistakes in the annotated data and the other one for using predicted
labels for confusing examples to quickly add to the annotated set.

# Info About the Modes

- For the first mode, the app goes through all the examples where the predicted
label and the existing annotation disagree. It starts with the example where
the model is most confident and goes in descending order of confidence. This
is where the annotation mistakes most likely lie.
- For the second mode, the app goes through unannotated examples where the
model is at least 50% confident. It starts with the example where the confusion
is the highest and goes in descending order of confusion. The idea here is to
quickly add to the annotated set with examples that can potentially provide the
model with information it lacks.

# Instructions to Run

- Extract the contents of the zip file in the same location as `run_app.py`.
- Run the app: `python3 run_app.py`, use `0, 1, 2` to select what you want to
do.
- The code is pretty light on dependencies: it only uses the packages `json`,
`pandas` and `sqlite3`.

# Other Ideas

- I tried to get a UI going using PySimpleGUI, but I was facing [this issue](
https://stackoverflow.com/questions/25905540/importerror-no-module-named-tkinter)
which I tried to resolve but it didn't go away even after 15 minutes which is
when I gave up.
- Add additional heuristic modes where you try to collect data based on class
information. For example, push additional annotation for classes that have
relatively few annotated examples or classes where the test accuracy is
relatively low.
