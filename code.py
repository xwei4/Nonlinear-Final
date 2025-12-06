import gurobipy as gp
from gurobipy import GRB
import pandas as pd

df = pd.read_csv("test.txt")

foods = df["Food_Item"].tolist()

m = gp.Model("diet_opt")
x = m.addVars(foods, name="x", lb=0, vtype=GRB.CONTINUOUS)

m.setObjective(gp.quicksum(df.loc[i, "Estimated_Price (USD)"] * x[foods[i]] for i in range(len(foods))),GRB.MINIMIZE)

MAX_SUGARS = 50    
MAX_CHOL = 300  
MIN_FIBER = 28   
MIN_PROTEIN = 50   
MAX_FAT = 78   
MIN_FAT = 20 
MAX_SODIUM = 2300
MAX_CARBS = 275

m.addConstr(gp.quicksum(df.loc[i, "Sugars (g)"] * x[foods[i]] for i in range(len(foods)))<= MAX_SUGARS,"max_sugars")
m.addConstr(gp.quicksum(df.loc[i, "Cholesterol (mg)"] * x[foods[i]] for i in range(len(foods)))<= MAX_CHOL,"max_cholesterol")
m.addConstr(gp.quicksum(df.loc[i, "Fiber (g)"] * x[foods[i]] for i in range(len(foods)))>= MIN_FIBER,"min_fiber")
m.addConstr(gp.quicksum(df.loc[i, "Protein (g)"] * x[foods[i]] for i in range(len(foods)))>= MIN_PROTEIN,"min_protein")
m.addConstr(gp.quicksum(df.loc[i, "Fat (g)"] * x[foods[i]] for i in range(len(foods)))<= MAX_FAT,"max_fat")
m.addConstr(gp.quicksum(df.loc[i, "Fat (g)"] * x[foods[i]] for i in range(len(foods)))>= MIN_FAT,"min_fat")
m.addConstr(gp.quicksum(df.loc[i, "Sodium (mg)"] * x[foods[i]] for i in range(len(foods)))<= MAX_SODIUM,"max_sodium")
m.addConstr(gp.quicksum(df.loc[i, "Carbohydrates (g)"] * x[foods[i]] for i in range(len(foods)))<= MAX_CARBS,"max_carbohydrates")

m.optimize()

print("\nOptimal food quantities:")
for f in foods:
    if x[f].X > 1e-6:
        print(f"{f:30s} : {x[f].X:.3f} units")
print("\nTotal cost = $", m.ObjVal)
