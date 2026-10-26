import re
from bs4 import BeautifulSoup

# 1. Sample malformed XML input string (unclosed tags, trailing spaces, messiness)
bad_xml_data = """
<catalog>
    <product id="101">
        <name>   Wireless Keyboard   </name>
        <price currency="USD">29.99
        <description>High-quality mechanical switch keyboard.</descripton>
    </product>
    <product id="102">
        <name>Gaming Mouse</name>
        <price currency="USD">49.99</price>
    </product>
</catalog>
"""

def clean_and_edit_xml(raw_xml):
    # --- PHASE 1: CLEANING & CLOSING TAGS ---
    # BeautifulSoup automatically forces unclosed tags (like <price>) to close
    # and fixes structurally broken markup hierarchies.
    soup = BeautifulSoup(raw_xml, features="xml")
    
    # --- PHASE 2: EDITING MARKUPS & ATTRIBUTES ---
    # Find all product elements
    products = soup.find_all("product")
    
    for product in products:
        # A. Edit text: Strip extra whitespaces from the product name
        name_tag = product.find("name")
        if name_tag and name_tag.text:
            name_tag.string = name_tag.text.strip()
            
        # B. Edit attributes: Add a new attribute 'status="instock"' to every product
        product["status"] = "instock"
        
        # C. Conditional Edit: Increase the price of item 101 by $5.00
        if product.get("id") == "101":
            price_tag = product.find("price")
            if price_tag and price_tag.text:
                try:
                    new_price = float(price_tag.text.strip()) + 5.00
                    price_tag.string = f"{new_price:.2f}"
                except ValueError:
                    pass
                
        # D. Remove unwanted or broken tags (e.g., typos like <descripton>)
        typo_tag = product.find("description")
        if typo_tag:
            typo_tag.decompose() # Completely removes the element from the tree
            
    # --- PHASE 3: FINAL CLEANING (Whitespace & Formatting) ---
    # Convert back to string with beautiful tree indentation
    clean_xml_string = soup.prettify()
    
    # Optional: Strip out empty lines that prettify() sometimes leaves behind
    clean_xml_string = re.sub(r'\n\s*\n', '\n', clean_xml_string)
    
    return clean_xml_string

# Run the cleaning pipeline
final_xml = clean_and_edit_xml(bad_xml_data)
print(final_xml)

# Save the repaired XML to a file
with open("cleaned_output.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)
