import os
dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'
version = 'v1.0-mini'
table_root = os.path.join(dataroot, version)

print(f"Dataset root exists: {os.path.exists(dataroot)}")  # Should be True
print(f"Expected table root: {table_root}")  # Should show correct path
print(f"Table root exists: {os.path.exists(table_root)}")  # Should be True

