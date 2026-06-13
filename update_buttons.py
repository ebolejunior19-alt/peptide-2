import re
from pathlib import Path

file_path = Path(r'c:\Users\pc\Desktop\peptide 2\index.html')
content = file_path.read_text(encoding='utf-8', errors='replace')

# Map of product names to their default prices and dosages
products = {
    'GHK-Cu': ('80.00', '50mg'),
    'Retatrutide': ('125.00', '5mg'),
    'BPC157': ('75.00', '5mg'),
    'BPC157 + TB500': ('110.00', '10mg'),
    'TB-500 (Thymosin Beta-4)': ('55.00', '5mg'),
    'Selank': ('55.00', '5mg'),
    'Semax': ('55.00', '5mg'),
    'Glow Blend 70 mg': ('160.00', '70mg'),
    'BAC Water 3ML': ('10.00', '3ML'),
    'BAC Water 10ML': ('15.00', '10ML'),
    'Cagrilintide': ('125.00', '5mg'),
    'Cagrilintide + Semaglutide': ('155.00', '5mg'),
    'Tirzepatide 10 mg': ('145.00', '10mg'),
    'MOTS-C': ('155.00', '10mg'),
    'Tesamorelin': ('145.00', '5mg'),
    'AOD9604 5mg': ('95.00', '5mg'),
    'Tesamorelin + CJC1295 + Ipamorelin Blend': ('195.00', 'Blend'),
    'Tesamorelin + Ipamorelin Blend': ('150.00', 'Blend'),
    'Ipamorelin': ('65.00', '5mg'),
    'GHRP6': ('70.00', '5mg'),
    'CJC1295 Without DAC': ('80.00', '5mg'),
    'Hexarelin': ('55.00', '2mg'),
    'IGF-1 LR3 1 mg': ('100.00', '1mg'),
    'GHRP2 5 mg': ('75.00', '5mg'),
    'Follistatin 315 1 mg': ('320.00', '1mg'),
    'Follistatin 344 1 mg': ('340.00', '1mg'),
    'CJC1295 + Ipamorelin 10 mg': ('120.00', '10mg'),
    'MGF 2 mg': ('165.00', '2mg'),
    'LL37 5 mg': ('165.00', '5mg'),
    'ARA-290 10 mg': ('85.00', '10mg'),
    'Melanotan 2 10 mg': ('75.00', '10mg'),
    'KPV': ('95.00', '5mg'),
    'NAD+': ('65.00', '500mg'),
    'SS-31': ('95.00', '10mg'),
    'Thymosin Alpha-1': ('85.00', '5mg'),
    'Epithalon 10 mg': ('90.00', '10mg'),
    'Glutathione 1500 mg': ('95.00', '1500mg'),
    'FOXO4-DRI 10 mg': ('385.00', '10mg'),
    'N-Acetyl Epitalon 5 mg': ('85.00', '5mg'),
    'NeuroPinealon': ('85.00', '5mg'),
    'VIP': ('95.00', '5mg'),
    'DSIP 5 mg': ('90.00', '5mg'),
    'Oxytocin 2mg': ('65.00', '2mg'),
    'P21 10 mg': ('190.00', '10mg'),
    'Gonadorelin 2 mg': ('55.00', '2mg'),
    'PT-141 10 mg': ('105.00', '10mg'),
}

# Replace each product's button with a link
for product_name, (price, dosage) in products.items():
    # URL encode the product name
    encoded_product = product_name.replace(' ', '%20').replace('+', '%2B').replace('(', '%28').replace(')', '%29')
    payment_url = f"payment.html?product={encoded_product}&price={price}&dosage={dosage}"
    
    # Find the button that follows the product name
    # Use a regex pattern that finds h4 with product name, followed by any content, then the button
    pattern = f"(<h4>{re.escape(product_name)}</h4>.*?)<button class=\"btn btn-primary\">Add to Cart</button>"
    replacement = f"$1<a href='{payment_url}' class='btn btn-primary'>Add to Cart</a>"
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    print(f"Updated: {product_name}")

# Write back
file_path.write_text(content, encoding='utf-8')
print(f"\nAll {len(products)} products updated successfully!")
print(f"Total file size: {len(content)} bytes")
