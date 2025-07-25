# Multipart ETag calculation
from hashlib import md5, sha256

import awscrt.checksums
import base64

# read content of all file have prefix 'part-' in directory
def read_split_files(prefix='part-'):
    import os
    parts = []
    part_files = sorted([f for f in os.listdir('.') if f.startswith(prefix)])
    
    for part_file in part_files:
        with open(part_file, 'rb') as f:
            parts.append(f.read())
    
    return parts

parts = read_split_files('part-')
part1_content=parts[0]
part2_content=parts[1]
part3_content=parts[2]
part4_content=parts[3]

part1_md5 = md5(part1_content).digest()  # Binary, not hex
part2_md5 = md5(part2_content).digest()  # Binary, not hex
part3_md5 = md5(part3_content).digest()  # Binary, not hex
part4_md5 = md5(part4_content).digest()  # Binary, not hex

# print 
print(f"part1_md5: {part1_md5}\n")
print(f"part2_md5: {part2_md5}\n")
print(f"part3_md5: {part3_md5}\n")
print(f"part4_md5: {part4_md5}\n")

# Concatenate binary hashes
combined_hash = part1_md5 + part2_md5 + part3_md5 + part4_md5

# Final ETag
etag = md5(combined_hash).hexdigest() + "-4"  # -4 indicates 3 parts
# Result: "b7c8d9e0f1a2b3c4...-3"

print(f"Etag: {etag}")

# Checksum
file_content = part1_content + part2_content + part3_content + part4_content
crc64_value = awscrt.checksums.crc64nvme(file_content)
crc64_bytes = crc64_value.to_bytes(8, byteorder='big')
checksum_crc64nvme = base64.b64encode(crc64_bytes).decode('ascii')

print(f"Checksum: {checksum_crc64nvme}")


# ETag depends on upload method and part sizes (algorithm difference) 
# Content checksum depends only on final file content (always same)