def validate_attribute_values(chosen_attribute, product_inventory):
    inventory_attribute_values = product_inventory.attribute_values.all()
    if (chosen_attribute in inventory_attribute_values):
        return True
    else:
        return False
