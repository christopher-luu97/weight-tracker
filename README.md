This repository contains python built scripts to address my personal needs.

First utility (Complete): Converting my excel weight data spreadsheet to a proper format
1. Execute in cmd: 
python convert_excel_weight.py <file_name> <sheet_name: optional> <date_value: optional>
2. The input <file_name> can be found within input_data. This can also be edited to your specific needs, following the format. Dates can be changed as necessary.
3. Output is a formatted version that is more suitable for graphs

Second utility (WIP): Add average column and generate plots 
1. Average column created
2. Plots (WIP)

Third (WIP): Use Python to Read and Write to PostgreSQL instead of reading from updated Excel sheet and creating a newly formatted output file every day.

Fourth (Complete): Create a python application with a gui for the first utility.
    - This was performed to gather an understanding of GUI development and compiling a simple Python application to an executable.

Fifth (WIP): Create a dashboard to display plots
Sixth (WIP): Add functionality to update plots in dashboard via user input

Ideal end state:
Create a dashboard for weight data that can be updated via web-browser interface.
Connects straight to PostgreSQL db
    - Potential options for deployment: Streamlit + heroku


Testing: 
1. Need to get requirements.txt, setup with GitHub actions to automate testing on conversion pipeline.
    - COMPLETED