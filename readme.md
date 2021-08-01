This project is to clean option data avialble at https://github.com/oyeluckydps/option_analysis. In future we might add feature to visulize, analyze and even backtest option chains.

An user needs to create a folder structure as shown below:  

root  
|-> main.py  
|-> option_data  
&nbsp;&nbsp;&nbsp;&nbsp;|-> 2019  
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|-> Expiry 01st August.zip  
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|-> Expiry 03rd October.zip  
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|-> ... etc  
&nbsp;&nbsp;&nbsp;&nbsp;|-> 2020  
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|-> ... etc  
&nbsp;&nbsp;&nbsp;&nbsp;|-> 2021  
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|-> ... etc  
&nbsp;&nbsp;&nbsp;&nbsp;|-> concat  

Keep all the expiry data downloaded from the above link year wise in folders shown above. After excution of main.py, the final output is present in concat folder. It contains cleaned data for each expiry and a all_in_1.csv folder that has all the data.
