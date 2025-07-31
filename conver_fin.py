import base64

# Path to your .tif fingerprint image
image_path = "D:\\Chantal\\Biometric_Login_auth-main\\Biometric_Login_auth-main\\012_3_1.tif"
output_path = "fingerprint_base64.txt"

with open(image_path, "rb") as image_file:
    base64_str = base64.b64encode(image_file.read()).decode("utf-8")

with open(output_path, "w") as out_file:
    out_file.write(base64_str)

print("Base64 conversion complete. Output saved to fingerprint_base64.txt.")