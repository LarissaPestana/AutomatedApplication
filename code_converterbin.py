import ctypes
from apread import APReader
import pandas as pd
import re
import os
from tkinter import filedialog
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
                if filename.endswith('.bin'):
                    file_list.append(os.path.join(root_dir, filename))
                elif filename.endswith('.BIN'):
                    file_list.append(os.path.join(root_dir, filename))
    os.system(f'explorer "{full_path}"')
    num_len=len(file_list)
    print(num_len)

    for n in file_list:
        data = APReader(n)

        channel_data = {} 
        dataframes = {}
        dataframes_list=[]

        def count_keys_time(dictionary):
            count = 0
            for key in dictionary.keys():      
                if 'time' in key.lower():
                    dataframe = pd.DataFrame({f'df{count}': ['time']})
                    dataframes[f'df{count}'] = dataframe
                    count += 1
            return dataframes, count
            
        max_length = max(len(channel.data) for channel in data.Channels)

        for channel in data.Channels:
            names_channel = channel.Name
            datas_channel = channel.data
            channel_data[names_channel] = datas_channel
        dataframes, count = count_keys_time(channel_data)

        if count > 1:
            new_dataframes = {}
            current_df = None
            for name, data in channel_data.items():
                print(name)
                if 'time' in name.lower():
                    current_df = pd.DataFrame()
                    new_dataframes[name] = current_df
                if current_df is not None:
                    current_df[name] = data

            list_new_dataframes=list(new_dataframes.values())
            for i in list_new_dataframes:
                
                print(i)
                for column in i.columns:
                    
                    print(column)
                    if 'time' in column.lower():
                        i.rename(columns={column: 'time'}, inplace=True)
            
                i['time'] = i['time'].astype(str)
                i['time'] = i['time'].apply(lambda x: re.sub(r'[^0-9.]', '', x) if re.match(r'^[\d.]+$', x) else pd.NA)
                i['time'] = pd.to_numeric(i['time'], errors='coerce') 
                i = i.dropna(subset=['time'])

                dataframes_list.append(i)

                for df in dataframes_list:
                    df = df.apply(pd.to_numeric, errors='coerce')

                print(dataframes_list)
                result_df = dataframes_list[0]  
                for df in dataframes_list[1:]:
                    result_df = result_df.merge(df, on='time', how='outer')

                print(result_df)
                result_df.sort_values(by='time', inplace=True)
                result_df.reset_index(drop=True, inplace=True)
                precision = 2 
                result_df['time'] = pd.to_numeric(result_df['time'], errors='coerce').round(precision)

                result_df = result_df.dropna(subset=['time'])

                result_df = result_df.apply(pd.to_numeric, errors='coerce')
                result_df = result_df.groupby('time').mean()
                result_df.reset_index(inplace=True)
                result_df.interpolate(method='linear', axis=0, inplace=True)
                
                print(result_df)
                print(df)
            print(df)
            output_file = n + ".xlsx"
            nome_planilha = 'CAN C'
            result_df.to_excel(output_file, sheet_name=nome_planilha, index=False)
    

        else:
            df = pd.DataFrame(channel_data)
            output_file = n + ".xlsx"
            nome_planilha = 'CAN C'

            df.to_excel(output_file, sheet_name=nome_planilha, index=False)
            
    ctypes.windll.user32.MessageBoxW(0, "Converted data", "Completed Process", 0x40 | 0x1)

else: full_path=None