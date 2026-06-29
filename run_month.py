import os

print("=" * 50)
print("MONTHLY KASSENBUCH AUTOMATION")
print("=" * 50)

print("\n[1/5] Exporting POS...")
os.system("python Parsers/export_pos_csv.py")

print("\n[2/5] Exporting NEXI...")
os.system("python Parsers/export_nexi_csv.py")

print("\n[3/5] Exporting Lieferando...")
os.system("python Parsers/export_lieferando_csv.py")

print("\n[4/5] Exporting Uber...")
os.system("python Parsers/export_uber_csv.py")

print("\n[5/5] Generating Kassenbuch...")
os.system("python Parsers/generate_full_kassenbuch.py")

print("\nDONE!")