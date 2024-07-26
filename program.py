# Description: A program to enter and calculate new insurance policy information
# Author: Jacob Crummey
# Date(s): 2024 - 07 - 24
 
 
# Define required libraries.
import datetime
import sys
import time
 
# Define program constants.
f = open('Const.dat', 'r')
NEXT_POLICY_NUM = int(f.readline())
BASIC_PREMIUM_RATE = float(f.readline())
CAR_DISCOUNT_RATE = float(f.readline())
LIABILITY_RATE = float(f.readline())
GLASS_RATE = float(f.readline())
LOAN_RATE = float(f.readline())
HST_RATE = float(f.readline())
PROCESSING_RATE = float(f.readline())
f.close()

# Define program functions.
def calcExtraCosts(extraLiability, optionalGlass, optionalLoanerCar, LIABILITY_RATE, GLASS_RATE, LOAN_RATE, carNum):
    extraCosts = 0
    if extraLiability == 'Y':
        extraCosts += LIABILITY_RATE
    if optionalGlass == 'Y':
        extraCosts += GLASS_RATE
    if optionalLoanerCar == 'Y':
        extraCosts += LOAN_RATE
    extraCosts = extraCosts * carNum
    return extraCosts
 
def calcInsuranceCost(carNum, BASIC_PREMIUM_RATE, CAR_DISCOUNT_RATE):
    if carNum == 1:
        return BASIC_PREMIUM_RATE
    if carNum == 0:
        return 0
    else:
        return ((BASIC_PREMIUM_RATE * (carNum - 1)) * (1 - CAR_DISCOUNT_RATE)) + BASIC_PREMIUM_RATE
        
def calTotalInsurancePremium(insuranceCost, extraCosts):
    return insuranceCost + extraCosts

def calcHST(totalInsurancePremium, HST_RATE):
    return totalInsurancePremium * HST_RATE

def calcTotalCost(totalInsurancePremium, hst):
    return totalInsurancePremium + hst

def calcMonthlyPayment(payRate, downPayment, calcTotalCost, PROCESSING_RATE):
    if payRate == 'M':
        return (calcTotalCost(totalInsurancePremium, hst) + PROCESSING_RATE) / 8
    elif payRate == 'F':
        return calcTotalCost(totalInsurancePremium, hst)
    else:
        return ((calcTotalCost(totalInsurancePremium, hst) + PROCESSING_RATE) - downPayment) / 8
    
def ProgressBar(iteration, total, prefix='', suffix='', length=30, fill='█'):
 
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    
def incrementPolicyNumber():
    f = open('Const.dat', 'r+')
    lines = f.readlines()
    lines[0] = str(NEXT_POLICY_NUM + 1) + '\n'
    f.seek(0)
    f.writelines(lines)
    f.close()
    


# Main program starts here.
print("Welcome to the insurance policy program.")
print("Please enter the following information for the new policy.")
print("-----------------------------------------------")
print()

while True:
    # Gather user inputs
    custName = input("Enter customer name: ").title()
    custAddress = input("Enter customer address: ").title()
    custCity = input("Enter customer city: ").title()
    validProvinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
    custProvince = input("Enter customer province: ").upper()
    while custProvince not in validProvinces:
        custProvince = input("Invalid province. Please enter a valid province: ").upper()
    custPostal = input("Enter customer postal code: ").upper()
    custPhone = input("Enter customer phone number: ")
    carNum = int(input("Enter number of cars to be insured: "))
    extraLiability = input("Do you want extra liability insurance for up to $1,000,000? (Y/N): ").upper()
    optionalGlass = input("Do you want optional glass coverage? (Y/N): ").upper()
    optionalLoanerCar = input("Do you want optional loaner car coverage? (Y/N): ").upper()
    payOptions = ['M', 'F', 'D']
    payRate = input("Do you want to pay monthly or full, or make a down payment? (M/F/D): ").upper()
    while payRate not in payOptions:
        payRate = input("Invalid payment option. Please enter a valid option: ").upper()
    if payRate == 'D':
        downPayment = int(input("Enter down payment amount: "))
    else:
        downPayment = 0
    claimNumber = input("Enter the claim Number: ")
    claimDate = input("Enter the claim date: ")
    claimAmount = int(input("Enter the claim amount of all previous claims: "))
    
    # Calculate the results
    
    extraCosts = calcExtraCosts(extraLiability, optionalGlass, optionalLoanerCar, LIABILITY_RATE, GLASS_RATE, LOAN_RATE)
    insuranceCost = calcInsuranceCost(carNum, BASIC_PREMIUM_RATE, CAR_DISCOUNT_RATE)
    totalInsurancePremium = calTotalInsurancePremium(insuranceCost, extraCosts)
    hst = calcHST(totalInsurancePremium, HST_RATE)
    totalCost = calcTotalCost(totalInsurancePremium, hst)
    monthlyPayment = calcMonthlyPayment(payRate, downPayment, calcTotalCost, PROCESSING_RATE)
    
    # Display the results in a receipt format
    print()
    print("Insurance Policy Receipt")
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    print(f"Policy Number: {NEXT_POLICY_NUM} Claim Number: {claimNumber} Claim Date: {claimDate} Claim Amount: ${claimAmount:.2f}")
    print()
    print(f"Customer Name: {custName} Customer Phone: {custPhone}")
    print()
    print(f"Customer Address: {custAddress} {custCity} {custProvince} {custPostal}")
    print()
    print(f"Number of Cars: {carNum} Extra Liability: {extraLiability} Optional Glass: {optionalGlass} Optional Loaner Car: {optionalLoanerCar}")
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"Insurance Cost: ${insuranceCost:.2f} Extra Costs: ${extraCosts:.2f}")
    print()
    print(f"Total Insurance Premium: ${totalInsurancePremium:.2f} HST: ${hst:.2f}")
    print()
    print(f"Total Cost: ${totalCost:.2f}")
    print()
    print(f"Monthly Payment: ${monthlyPayment:.2f}")
    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    
    # Save the results to a file each line a complete record
    
    
    
    
    f = open('Claims.dat', 'a')
    
    f.write(f"{NEXT_POLICY_NUM}, ")
    f.write(f"{custName}, ")
    f.write(f"{custAddress}, ")
    f.write(f"{custCity}, ")
    f.write(f"{custProvince}, ")
    f.write(f"{custPostal}, ")
    f.write(f"{custPhone}, ")
    f.write(f"{str(carNum)}, ")
    f.write(f"{extraLiability}, ")
    f.write(f"{optionalGlass}, ")
    f.write(f"{optionalLoanerCar}, ")
    f.write(f"{payRate}, ")
    f.write(f"{str(downPayment)}, ")
    f.write(f"{claimNumber}, ")
    f.write(f"{claimDate}, ")
    f.write(f"{str(claimAmount)}, ")
    f.write(f"{str(extraCosts)}, ")
    f.write(f"{str(insuranceCost)}, ")
    f.write(f"{str(totalInsurancePremium)}, ")
    f.write(f"{str(hst)}, ")
    f.write(f"{str(totalCost)}\n")
    
    f.close()
    
    # Show a progress bar
    print()
 
    TotalIterations = 30 # The more iterations, the more time is takes.
    Message = "Saving Data ..."
 
    for i in range(TotalIterations + 1):
        time.sleep(0.1)  # Simulate some work
        ProgressBar(i, TotalIterations, prefix=Message, suffix='Complete', length=50)
 
    print()
 
 
    print()
    print("Claim information has been successfully saved to Claims.dat ...")
    print()
    
    # Ask user if they want to enter another customer
    Continue = input("Do you want to enter another customer? (Y/N): ").upper()
    if Continue == 'N':
        break
    
    
# Read the data file and display the summary data.
print()
print("Summary Data")
print("Claim #   Claim Date       Amount")
print("---------------------------------")
print()

f = open('Claims.dat', 'r')
for records in f:
    recordLst = records.split(", ")
    print(f"{recordLst[13]}          {recordLst[14]}     ${recordLst[15]}")
    
f.close()

        


 
# Increase the policy number for the next customer.
incrementPolicyNumber()
