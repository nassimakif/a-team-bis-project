import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

df = pd.read_csv('test.csv')
df.head()
df.info
df["solde"].value_counts(normalize=True).plot(kind='pie')