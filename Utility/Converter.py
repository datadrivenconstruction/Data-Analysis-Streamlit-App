import os
import subprocess

import pandas as pd

# Folder where the DDC converter is located
path_conv = r''
# Path address of the folder where RVT | IFC | DWG  project are located
file_path = r''

# Conversion of one RVT project
process = subprocess.Popen([os.path.join(path_conv, 'RvtExporter.exe'), file_path], cwd=path_conv)


process.wait()  # Waiting for the process to be completed
print("DDC Conversion process finished")

output_file = file_path[:-4] + "_rvt.xlsx"

# Read the converted Excel file
df = pd.read_excel(output_file)

# Update column names to remove storage type in parameter
df.columns = [col.split(' : ')[0] for col in df.columns]

# Save the filtered data to a new Excel file
df.to_excel("filtered_data_groupby_type.xlsx", index=False)