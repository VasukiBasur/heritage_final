import os

filepath = 'd:/dbmss/templates/shop_products.html'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Using a raw string to perfectly control the output.
# We want the file to literally contain:
#                     <button class="wishlist-btn absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors cursor-pointer" onclick="event.preventDefault(); event.stopPropagation(); window.toggleWishlistProduct(this, '${product.title.replace(/\'/g, \\"\\\\\'\\")}', ${product.price}, '/static/${product.img}');">
replacement = r"""                    <button class="wishlist-btn absolute top-3 right-3 z-20 p-2 bg-black/50 backdrop-blur rounded-full text-gray-300 hover:text-red-500 transition-colors cursor-pointer" onclick="event.preventDefault(); event.stopPropagation(); window.toggleWishlistProduct(this, '${product.title.replace(/'/g, "\\\\'")}', ${product.price}, '/static/${product.img}');">""" + "\n"

lines[776] = replacement

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed line 777")
