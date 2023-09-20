import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import datetime
import os



def read_consolidate(path= ''):
    
    df= pd.DataFrame()
    for file in os.listdir(f"{path}\\Raw_data"):
        temp_df = pd.read_csv(f"{path}\\Raw_data\\{file}")
        df = pd.concat([df, temp_df])
        
    df.reset_index(inplace=True, drop=True)
    df['Performance_Name'] = ''
    df['Performance_Value'] = ''
    for index, row in df.iterrows():
#         print(f"row index: {index}")
        for colomn, value in row.iteritems():
            if pd.notna(value) and type(value) != str :
                df.at[index,'Performance_Name'] = colomn
                df.at[index, 'Performance_Value'] = value
#                 print(f"Column: {colomn}, Values: {value} with type of: {type(value)}")

    performance_unique_name = list(df['Performance_Name'].unique())    
    df = df.drop(columns=performance_unique_name)
    df['process_end_date'] = df['process_end_date'].apply(lambda x: pd.to_datetime(x))
    today = str(datetime.date.today())
    df.to_csv(f"{path}\\Final_Results\\Combined_Results_{today}.csv", index=False)
    return df

def Run_chart_Plot(df = ''):
    for unique_performance_metric in list(df['Performance_Name'].unique()):
        plt.figure(figsize=(16,8))
        plt.plot(df[df['Performance_Name']==unique_performance_metric].sort_values(by='process_end_date')['process_end_date'], df[df['Performance_Name']== unique_performance_metric].sort_values(by='process_end_date')['Performance_Value'],marker='o')
        plt.xlabel("Process End Time")
        plt.ylabel(f"{unique_performance_metric} Values")
        plt.title(f"Run chart for {unique_performance_metric}")
        plt.show()
        
def Distribution_charts(df = ''):
    for unique_performance_metric in list(df['Performance_Name'].unique()):
        sns.displot(df[df['Performance_Name'] == unique_performance_metric]['Performance_Value'])
        average = df[df['Performance_Name'] == unique_performance_metric]['Performance_Value'].mean()
        std = np.std(df[df['Performance_Name'] == unique_performance_metric]['Performance_Value'])
        plt.axvline(average, color='red', linestyle='--', label='Average')
        plt.axvline(average + 3 * std, color='green', linestyle='--', label='3 Sigma')
        plt.axvline(average - 3 * std, color='green', linestyle='--')
        plt.title(f"Distibution of {unique_performance_metric}")
        plt.legend()
        plt.show()
def main():
    Project_path ="C:\\Users\\mrzak\\OneDrive - University of Ottawa\\Documents\\Assessment"
    
    df = read_consolidate(Project_path)
    # Run_chart_Plot(df)
    # Distribution_charts(df)

if __name__ =='__main__':
    main()

