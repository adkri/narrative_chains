# Narrative Event Chains in Python


Basic implementation of narrative chain events in python.

## Required 
- Python 3.7+
- spacy
- neuralcoref
- tqdm 
- pandas


## Installation
- You can install most of the libraries using pip.
  ```sh
  python3 -m pip install spacy tqdm pandas
  ```
- After installing spacy, run the command
  ```sh
  python3 -m spacy download en_core_web_lg
  ```
- Neuralcoref must be built locally:
  ```sh
  git clone https://github.com/huggingface/neuralcoref.git
  cd neuralcoref/
  pip install -r requirements.txt
  pip intall -e .
  ```

## Run the script
- First run the script with the "--build" flag to create the model. (this takes over an hour on my machine)
  ```sh
  python3 run.py --build
  ```
  This saves the model as "all.json".
- Subsequent execution of run.py will use this model. Run as:
  ```sh
  python3 run.py
  ```
  This will build a answer.txt file with storyid, and predicted story ending number.
  
- If you want to run it on validation model, inside "run.py" change "test.csv" to "val.csv" and change validation to True.

