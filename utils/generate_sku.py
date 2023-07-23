import random
import string


def generate_sku(pk):
    print('---====PKL', pk)
    suffix = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits, k=6
        )
    )
    sku = f"{suffix}-{pk}"
    return sku
