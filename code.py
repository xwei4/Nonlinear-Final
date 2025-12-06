import gurobipy as gp
from gurobipy import GRB
import pandas as pd

df = pd.read_csv("test.cvs")

foods = df["Food_Item"].tolist()

m = gp.Model("diet_opt")
x = m.addVars(foods, name="x", lb=0, vtype=GRB.CONTINUOUS)

m.setObjective(gp.quicksum(df.loc[i, "Estimated_Price (USD)"] * x[foods[i]] for i in range(len(foods))),GRB.MINIMIZE)

MAX_SUGARS   = 50    
MAX_CHOL     = 300  
MIN_FIBER    = 28   
MIN_PROTEIN  = 50   
MAX_FAT      = 78   
MIN_FAT      = 20    