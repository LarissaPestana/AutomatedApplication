import mdfreader
import pandas as pd
import re
import ctypes
import os
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()
root.attributes('-topmost', True)
root.wm_attributes('-topmost', 1)  
root.lift()
folder_selected = filedialog.askdirectory(title='Directory')
if folder_selected:
    print(f'Folder Select:{folder_selected}')
    full_path = os.path.abspath(folder_selected)
    print(full_path)
    
    file_list = []
    for root_dir, _, filenames in os.walk(folder_selected):
            for filename in filenames:
                if filename.endswith('.dat'):
                    file_list.append(os.path.join(root_dir, filename))
    os.system(f'explorer "{full_path}"')
    num_len=len(file_list)
    print(num_len)

    for a in range(num_len):
        n=file_list[a]
        
        print(n)
        yop = mdfreader.Mdf(n)
        yop.convert_to_pandas()
        dataframes_list = []
        non_numeric_channels = []

        
        for group_name in yop.masterGroups:
            i = yop[group_name]
            
            
           
            for column in i.columns:
                if 'time' in column.lower():
                    i.rename(columns={column: 'time'}, inplace=True)
            
            
            
               
            i['time'] = i['time'].astype(str)
            i['time'] = i['time'].apply(lambda x: re.sub(r'[^0-9.]', '', x) if re.match(r'^[\d.]+$', x) else pd.NA)
            i['time'] = pd.to_numeric(i['time'], errors='coerce') 
            i = i.dropna(subset=['time'])
            
            dataframes_list.append(i)
            

            for df in dataframes_list:
                df = df.apply(pd.to_numeric, errors='coerce')

            result_df = dataframes_list[0]  
            for df in dataframes_list[1:]:
                result_df = result_df.merge(df, on='time', how='outer')
            
            result_df.sort_values(by='time', inplace=True)
            

            result_df.reset_index(drop=True, inplace=True)
            
            precision = 2  
            result_df['time'] = pd.to_numeric(result_df['time'], errors='coerce').round(precision)
            result_df = result_df.dropna(subset=['time']) 
            result_df = result_df.apply(pd.to_numeric, errors='coerce')
           
            print(result_df)
            
            result_df = result_df.groupby('time').mean()
            result_df.reset_index(inplace=True)
           
            print(result_df)
            result_df.interpolate(method='polynomial', order=1, axis=0, inplace=True)
            print(df)
            
            print(result_df)
            
        print(df)
        
        print(result_df)
        output_file = n + ".xlsx"
        nome_planilha = 'CAN C'
        result_df.to_excel(output_file, sheet_name=nome_planilha, index=False)
    
    ctypes.windll.user32.MessageBoxW(0, "Converted data", "Completed Process", 0x40 | 0x1)
else: full_path=None











