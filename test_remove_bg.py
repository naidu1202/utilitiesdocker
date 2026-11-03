from rembg import remove

with open("input.jpg", "rb") as i:
    input_data = i.read()

output_data = remove(input_data)

with open("output.png", "wb") as o:
    o.write(output_data)

print("Background removed successfully")
