import numpy as np
import pandas as pd
from os.path import join

RL_path = "/content/drive/MyDrive/RL"

class Candidate:
  '''
  Class to represent a candidate
  '''

  def __init__(self, row, df, encoding='utf8'):
    if isinstance(row, (dict, pd.DataFrame, pd.Series)):
      self.id = str(row['ID'])
    elif isinstance(row, int):
      if "ID" in df.columns:
        df.set_index("ID", inplace=True, verify_integrity=True)
      self.id = str(row)
    else:
      raise Exception("Either dict or int")

    self.path = join(join(RL_path, '20'+self.id[:2]), self.id)
    self.adviser_letter = False
    self.n_letters = 0
    self.letters = {1:dict(), 2:dict(), 3:dict(), 4:dict()}
    self.read_letters(encoding=encoding)

  def read_letters(self, encoding):
    for l in self.letters.keys():
      try:
        # Try short version first
        filename = f"RL_{l}s.txt"
        with open(join(self.path, filename), 'r', encoding=encoding, errors='ignore') as infile:
          if encoding != 'utf8':
            print(f"{encoding=}")
          self.letters[l]["text"] = infile.read()
        if l==1:
          self.adviser_letter = True
        self.n_letters += 1
      except FileNotFoundError as e:
        try:
          filename = f"RL_{l}.txt"
          with open(join(self.path, filename), 'r', encoding=encoding, errors='ignore') as infile:
            if encoding != 'utf8':
              print(f"{encoding=}")
            self.letters[l]["text"] = infile.read()
          if l==1:
            self.adviser_letter = True
          self.n_letters += 1
        except FileNotFoundError as e:
          self.letters[l]["text"] = ""
        except UnicodeError as e:
          self.letters[l]["text"] = ""

  def read_file(self, filename):
    if not filename.endswith('.txt'):
      filename += '.txt'
    try:
      with open(join(self.path, filename), 'r', encoding='utf8', errors='ignore') as infile:
        self.extra = infile.read()
    except FileNotFoundError as e:
      print("File not found")

  def __repr__(self):
    return f"Candidate #{self.id}"

  def __str__(self):
    text = f"""
    -------------------------------
    Candidate {self.id}
    Adviser's letter: {"Yes" if self.adviser_letter else "No"}
    Number of letters: {self.n_letters}
    -------------------------------
    """
    for k, letter in self.letters.items():
      if letter['text']:
        text += f"""
        Letter {k}: \"{letter["text"][:50]} ...\"
        """
    return text
    
  def save_letters(self, path=join(RL_path, "tfidf-processed"), mode='text'):
    for l,letter in self.letters.items():
      if letter['text']:
        filename = f'RL{l}_{self.id}.txt'
        text = letter.get(mode,"")
        if text:
          with open(join(path, filename), 'w') as f:
            f.write(text)

  def get_letters(self):
    letters = []
    for letter in self.letters.values():
      if letter['text']:
        letters.append(letter['text'])
    return letters

  def get_stats(self, stats):
    from copy import deepcopy
    s = {1:dict(), 2:dict(), 3:dict(), 4:dict()}
    for l in s.keys():
      s[l] = {stat: self.letters[l].get(stat, None) for stat in stats}
    return s

