# import module
import streamlit as st
import pandas as pd
import numpy as np
subprocess.check_call([sys.executable, "-m", "pip", "install", 'panel'])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'matplotlib'])


import panel as pn
import matplotlib.pyplot as plt
pn.extension('tabulator')


# Title
st.title("Pioneer Dashboard")

# reading the data from url and looking for site from it
df=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQi5lnVESmIFGng5PeZj2QYEM1hEcrGxmpTCidXkbHZmR-7eswXAsSqI0ZC02tdsJ5aTKzs56F_G0n7/pub?output=csv")

# taking site values
site_values= df['Site '].unique()

# making a dropdown with all the sites

# selection box using all the unique values in site

site = st.selectbox(" Our Sites: ", site_values)
 
# print the selected hobby
st.write("Your selected site is : ", site)

# I am creating a table where the site is selected site and having workorder/ priorty /name/ status and Date started as a column for each

def filter_by_site(df, selected_site):
    filtered_df = df[df['Site '] == selected_site]  
    return filtered_df[['WorkOrder', 'Name', 'Status', 'Date Started']] 


#selected_site = 'Break' 

filtered_table = filter_by_site(df, site)

# Displaying the table
st.table(filtered_table)  

# Creating  the pie chart
status_counts = df['Status'].value_counts()
plt.figure(figsize=(10,6))
status_pie = plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
plt.title('Status Distribution')

# Save the pie chart as an image
plt.savefig("piechart.png", format='png')
plt.close()  # Close the plot to free up resources

# Display the saved image using Streamlit
st.image("piechart.png")

#creatin a column with high priority work
df['Work_with_high_priority'] = df['WorkOrder'].dropna().apply(lambda x: x.startswith(('AH', 'SH')))

# print(df['Work_with_high_priority'])    
def priority_table(df, selected_value):
    filtered_df = df[df['Work_with_high_priority'] == selected_value]  
    return filtered_df[['WorkOrder', 'Name', 'Status']]     


priority_table=priority_table(df, True)

# Displaying the priority table
st.title('Higest Priority Running work')
st.table(priority_table) 






# Create a list of options for the dropdown
options = df['Name'].unique().tolist()

# Create the dropdown widget
dropdown = pn.widgets.Select(name='Employee', options=options)



st.sidebar.title(":black[Select an Employee]")

emp_dropdown = st.sidebar.selectbox("Choose Employee: ", df['Name'].unique())

# Create the dropdown widget
#selected_name = st.selectbox("Select Name", df['Name'])



# Filter the dataframe based on the selected name
filtered_df = df[df['Name'] == emp_dropdown]

# Display the information
if not filtered_df.empty:
    st.sidebar.write(f"Work Orders assigned to {emp_dropdown}:")
    workorder_status = st.sidebar.selectbox("Choose Status of WorkOrder you want to view : ", filtered_df['Status'].unique())
    
    for index, work_order in filtered_df['WorkOrder'].iteritems():
        
        #st.sidebar.write(filtered_df[['WorkOrder']])
        if st.sidebar.button(work_order):
        # Handle button click event
            #st.sidebar.write(f"You clicked on {work_order}")
            st.sidebar.write(f":red [WorkOrder ID:] :red[{work_order}]")


            st.sidebar.write(filtered_df['Description']) 
            #st.write()
    # if st.button("WorkOrder"):
    #     # Handle button click event
    #     st.write(f"The button for {selected_name}'s WOrkOrder was clicked!")
else:
    st.sidebar.write(f"No information found for {emp_dropdown}.")

