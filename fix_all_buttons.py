#!/usr/bin/env python3
"""
Replace all Add to Cart buttons with payment page links
"""
import re
from pathlib import Path

file_path = Path(r'c:\Users\pc\Desktop\peptide 2\index.html')
content = file_path.read_text(encoding='utf-8', errors='replace')

# List of all products with their details
products = [
    ('GHK-Cu', '80.00', '50mg'),
    ('Retatrutide', '125.00', '5mg'),
    ('Cagrilintide', '125.00', '5mg'),
    ('Cagrilintide + Semaglutide', '155.00', '5mg'),
    ('Tirzepatide 10 mg', '145.00', '10mg'),
    ('MOTS-C', '155.00', '10mg'),
    ('Tesamorelin', '145.00', '5mg'),
    ('AOD9604 5mg', '95.00', '5mg'),
    ('Tesamorelin + CJC1295 + Ipamorelin Blend', '195.00', 'Blend'),
    ('Tesamorelin + Ipamorelin Blend', '150.00', 'Blend'),
    ('Ipamorelin', '65.00', '5mg'),
    ('GHRP6', '70.00', '5mg'),
    ('CJC1295 Without DAC', '80.00', '5mg'),
    ('Hexarelin', '55.00', '2mg'),
    ('IGF-1 LR3 1 mg', '100.00', '1mg'),
    ('GHRP2 5 mg', '75.00', '5mg'),
    ('Follistatin 315 1 mg', '320.00', '1mg'),
    ('Follistatin 344 1 mg', '340.00', '1mg'),
    ('CJC1295 + Ipamorelin 10 mg', '120.00', '10mg'),
    ('MGF 2 mg', '165.00', '2mg'),
    ('LL37 5 mg', '165.00', '5mg'),
    ('ARA-290 10 mg', '85.00', '10mg'),
    ('Melanotan 2 10 mg', '75.00', '10mg'),
    ('KPV', '95.00', '5mg'),
    ('NAD+', '65.00', '500mg'),
    ('SS-31', '95.00', '10mg'),
    ('Thymosin Alpha-1', '85.00', '5mg'),
    ('Epithalon 10 mg', '90.00', '10mg'),
    ('Glutathione 1500 mg', '95.00', '1500mg'),
    ('FOXO4-DRI 10 mg', '385.00', '10mg'),
    ('N-Acetyl Epitalon 5 mg', '85.00', '5mg'),
    ('NeuroPinealon', '85.00', '5mg'),
    ('VIP', '95.00', '5mg'),
    ('DSIP 5 mg', '90.00', '5mg'),
    ('Oxytocin 2mg', '65.00', '2mg'),
    ('P21 10 mg', '190.00', '10mg'),
    ('Gonadorelin 2 mg', '55.00', '2mg'),
    ('PT-141 10 mg', '105.00', '10mg'),
]

# Replace buttons for each product
for product_name, price, dosage in products:
    # URL encode product name
    encoded = product_name.replace(' ', '%20').replace('+', '%2B').replace('(', '%28').replace(')', '%29').replace('/', '%2F')
    url = f"payment.html?product={encoded}&price={price}&dosage={dosage}"
    
    # Find pattern: h4 with product name, any content, then the button
    # Using non-greedy match to stop at first button
    pattern = f"(<h4>{re.escape(product_name)}</h4>(?:.*?)<div class=\"price\">.*?</div>(?:.*?))<button class=\"btn btn-primary\">Add to Cart</button>"
    replacement = f'$1<a href="{url}" class="btn btn-primary">Add to Cart</a>'
    
    # Count matches before
    matches_before = len(re.findall(pattern, content, re.DOTALL))
    
    # Replace
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        content = new_content
        print(f"✓ Updated: {product_name} ({matches_before} instance(s))")
    else:
        print(f"⚠ No changes for: {product_name}")

# Save the file
file_path.write_text(content, encoding='utf-8')

# Verify
remaining_buttons = len(re.findall(r'<button class="btn btn-primary">Add to Cart</button>', content))
payment_links = len(re.findall(r'href="payment\.html', content))

print(f"\n{'='*50}")
print(f"Payment links added: {payment_links}")
print(f"Remaining buttons: {remaining_buttons}")
print(f"File saved successfully!")
