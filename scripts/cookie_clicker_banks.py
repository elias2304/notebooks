""" 
Author: Elias Schweighuber
Date: 20.10.2026
Exercise:
"""

COMPANIES = ["CRL", "CHC", "BTR", "SUG", "NUT", "SLT", "VNL", "EGG", "CNM", "CRM"]
BANK_LEVEL = 1

# (10 x (id+1) + Bank level -1,
if __name__ == '__main__':
    threshold = []
    for i in range(len(COMPANIES)):
        result = 10 * (i+1) + BANK_LEVEL - 1
        threshold.append(COMPANIES[i] * BANK_LEVEL)
        print(COMPANIES[i],  ": ", result)
