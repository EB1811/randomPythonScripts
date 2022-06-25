import operator
import math
import random
import sys
import numpy  as np
from matplotlib import pyplot

def taxCalc(taxBands, income):
    taxPayed = 0
    for i, band in enumerate(taxBands):
        taxable = (band["pay"] if income > band["pay"] else income) - (taxBands[i - 1]["pay"] if i > 0 else 0)
        if taxable > 0:
            taxPayed += taxable * band["rate"]

    return round(taxPayed)
        

# Config
expenses = 0
basicTaxBands = [
    {"pay": 12570, "rate": 0, "rollingCutoff": 100000},
    {"pay": 50271, "rate": 0.2},
    {"pay": 150000, "rate": 0.4},
    {"pay": sys.maxsize, "rate": 0.45}
]
niTaxBands = [
    {"pay": 9569, "rate": 0},
    {"pay": 50270, "rate": 0.12},
    {"pay": sys.maxsize, "rate": 0.02},
]
sLoanTaxBands = [
    {"pay": 27288, "rate": 0},
    {"pay": sys.maxsize, "rate": 0.09},
]

income = int(input("Enter Income:"))

taxPayed = taxCalc(basicTaxBands, income)
nInsurancePayed = taxCalc(niTaxBands, income)
sLoanPayed = taxCalc(sLoanTaxBands, income)
postTaxIncome = income - taxPayed - nInsurancePayed - sLoanPayed

print("\nTax Payed:", taxPayed)
print("National Insurance Payed:", nInsurancePayed)
print("Student Loans Payed:", sLoanPayed)
print("----------------")
print("Post Tax Income:", postTaxIncome)
