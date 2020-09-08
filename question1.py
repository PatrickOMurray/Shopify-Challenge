import pandas as pd
import sys

# This will give a full list for outliers later
pd.set_option('display.max_rows', None)

# Opening the selected file
file = input("\nInput csv file: ")
try:
    df = pd.read_csv(file)
except:
    print("\nInvalid input.")
    input("")
    sys.exit(1)

# This give a general view of the data
# Hopefully at a glance it will give an idea of the issue
print(df.describe())

# order_amount is to be selected, but total_items can also be used for insights
clm = input("\nSelect column from above for analysis (order_amount is suggested)\n>> ")




# This will indicate if the data has a skew in its distribution
# The number should range between -1 and 1
try:
    sk = round(df[clm].skew(),2)
    print(f"\n{clm} skew = {sk}\n")
except:
    print("\nInvalid input.")
    input("")
    sys.exit(1)


if sk > 1.5: # Using 1.5 to give some leeway
    print(f"The skew for the distribution of {clm} is too large. There are outliers that must be addressed")
    input("\n>>")

    # This is used to find the Interquartile range
    # This number will be used to select the outliers
    Q1 = df[clm].quantile(.25)
    Q3 = df[clm].quantile(.75)
    IQR = Q3 - Q1
    print(Q1)
    print(IQR)
    # Displaying the outliers, the lower quartile can be ignored since they shouldnt go below zero and the skew should be over 1.5 rather than negative
    outdf = df[df.loc[:,clm] > (Q3 + 1.5*IQR)]
    print(outdf.sort_values(by=clm))
    print("\n\nThe above list is skewing the data to much and should not be included in evaluating the stores.")
    input("\n>>")

    print("\nAn average can still be used if the outliers are excluded from the dataset.")

    # Separate useful data from outliers to calculate mean
    evaldf = df[df.loc[:,clm] < (Q3 + 1.5*IQR)]
    # print(round(evaldf[clm].skew(),2)) calculating the new skew if needed
    print("\nAverage without outliers: ", round(evaldf[clm].mean(),2))
    # Old mean for compare
    print("\nAverage with outliers: ", round(df[clm].mean(),2))
    input("\n>>")

else:
    print(f"\nThe skew for the {clm} is with in reason.\nA regular AOV could work for an evaluation")
    input("\n>>")
