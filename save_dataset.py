import pandas as pd
import io

data = """Transaction Id\tCustomer Id\tDay\tMonth\tYear\tPlace\tGender\tAge\tCategory\tSub Category\tBrand\tProduct Name\tVariant\tQuantity\tPrice Per Unit\tTotal Amount
1\tC001\t6\t10\t2024\tSalem\tFemale\t40\tHome\tFurniture\tIkea\tIkea Product\tRed\t2\t3478\t6956
2\tC002\t23\t6\t2024\tMadurai\tFemale\t58\tSports\tFitness\tDecathlon\tDecathlon Product\tBlue\t5\t207\t1035
3\tC003\t18\t11\t2024\tSalem\tMale\t41\tSports\tFitness\tDecathlon\tDecathlon Product\t256GB\t5\t4628\t23140
4\tC004\t21\t11\t2024\tSalem\tFemale\t48\tElectronics\tAccessories\tLogitech\tLogitech Product\t128GB\t1\t1531\t1531
5\tC005\t26\t3\t2024\tSalem\tMale\t34\tElectronics\tLaptop\tHP\tHP Product\tLarge\t2\t712\t1424
6\tC006\t18\t10\t2024\tTrichy\tMale\t36\tClothing\tMen\tNike\tNike Product\t256GB\t1\t4369\t4369
7\tC007\t18\t11\t2024\tCoimbatore\tFemale\t42\tHome\tFurniture\tHomeTown\tHomeTown Product\t256GB\t3\t4318\t12954
8\tC008\t23\t10\t2024\tMadurai\tMale\t46\tGrocery\tBeverages\tPepsi\tPepsi Product\t128GB\t1\t4034\t4034
9\tC009\t23\t5\t2024\tSalem\tFemale\t47\tHome\tKitchen\tPrestige\tPrestige Product\tLarge\t4\t2458\t9832
10\tC010\t12\t12\t2024\tCoimbatore\tMale\t23\tBeauty\tSkincare\tNivea\tNivea Product\tLarge\t2\t1554\t3108"""

# Write full dataset - using the pasted data
with open("dataset/retail_sales.csv", "w", encoding="utf-8") as f:
    f.write("Transaction Id,Customer Id,Day,Month,Year,Place,Gender,Age,Category,Sub Category,Brand,Product Name,Variant,Quantity,Price Per Unit,Total Amount\n")

print("Template created - please run save_dataset.py after pasting full data")
print("For now using tab-separated import...")

# Actually save as proper CSV from the tab data above
df = pd.read_csv(io.StringIO(data), sep='\t')
print(df.shape)
print(df.columns.tolist())
df.to_csv("dataset/retail_sales.csv", index=False)
print("Saved sample. Full dataset needs to be pasted.")
