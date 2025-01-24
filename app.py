import pandas as pd
import numpy as np
import streamlit as st 
import plotly.express as px 

df_orig = pd.read_csv(r"C:\PythonCode\Sprint4FinalProject\Sprint4ProjectCars\vehicles_us.csv")
#Making copy of original dataframe and will use this dataframe copy for the analysis going forward
df_Cars = df_orig.copy()
#We will now clean up dataframe
#Make sure datatypes are correct or make sense for each column and if they don't, fix it
#lets change the year data type from float to int as there are no decimal values in a year 
df_Cars["model_year"] = pd.to_numeric(df_Cars["model_year"], errors='coerce').astype('Int64')
#lets change the cylinder data type from float to int as there are no decimal in the number of cylinders a car has
df_Cars["cylinders"] = pd.to_numeric(df_Cars["cylinders"], errors='coerce').astype('Int64')
#lets change the odometer data type from float to int as well
df_Cars["odometer"] = pd.to_numeric(df_Cars["odometer"], errors='coerce').astype('Int64')
#lets change the date_posted type from string to date/time  
df_Cars['date_posted']=pd.to_datetime(df_Cars['date_posted'], format='%Y-%m-%d', errors='coerce')
#let's convert the price column to type float as prices tend to have decimals
df_Cars["price"]=df_Cars.price.astype(float)
#Let's convert the is 4 wheel drive column to a yes or no, as it makes more sense compared to the current values of 1.0 and NaN.
df_Cars["is_4wd"] = df_Cars["is_4wd"].apply(lambda x: "Yes" if x == 1.0 else "No")

#Cleanup null values and Create New Columns, or break apart existing columns into separate columns if neccessary to enhance the dataset
# we will replace all null values for the paint_color column to unknown
df_Cars["paint_color"]=df_Cars["paint_color"].fillna("unknown")
#the "make" column has both the make and model combined.  We need to split the values out into separate columns, make and model.
#first lets replace all null values for the model column with "unknown unknown" as the first unknown is the make and the 2nd unknown is the model
df_Cars["model"]=df_Cars["model"].fillna("unknown unknown")
#next we split the model value and create another column called "Make"
df_Cars[["make","model"]]=df_Cars["model"].str.split(" ", n=1, expand=True)
#Now lets create a new column called age.  we will take the max of the date posted
#and extract the year to get the most recent year based on this dataset, and subtract
#the model_year column from it to get the relative age of the car based on this dataset
df_Cars["age"] = df_Cars["date_posted"].max().year - df_Cars["model_year"]

# As we can see, except for the model_year, cylinders, and odometer columns the data looks clean without null values.  
# It might be prudent to keep the null values for the 3 columns mentioned above because we may want to see how no values in the model year,
# number of cylinders, and odometer affect whether or not a car gets sold or how long it sits based on the days_listed column.  
#lets change the make and model values to proper case just to make the data values look nicer
df_Cars["model"]=df_Cars["model"].str.title()
df_Cars["make"]=df_Cars["make"].str.title()
#Let's reorder the columns so that make and model are next to each other and are also before the model_year cdataframe_columns
# Get the current column order
columns = list(df_Cars.columns)
# Define the desired column order
new_order = ['make', 'model'] + [col for col in columns if col not in ['make', 'model']]
# Reorder the DataFrame columns
df_Cars = df_Cars[new_order]


#STEP 1, create lists that will feed our dropdownlist values for end users to select from in our Web Application

Make_List = df_Cars["make"].unique()
Make_List.sort()
#want to add an "All" value as a choice incase end users want to select all. I will do this for some lists where applicable going forward.
#Make_List.insert(0,"All") 
Make_List=np.insert(Make_List, 0, "All")


CarType_List = df_Cars["type"].unique()
#We are allowing for an option for the end user to select all car types
CarType_List=np.insert(CarType_List, 0, "All")
# so now we have the following lists to use for dropdown selections for end users to pick from.  We will use the following lists for our program
# for dropdown list selection Make_List, CarType_List for the first portion of our webapp


# First portion of the Design of our Web App Begins now:
# first we will encapsulate this portion of the code in a try except to capture any errors that may arise from the first portion of our code.
try:
    st.header("""Market of used Cars""")
    st.write("""##### Filter the data below by make, type, price and mileage.""")
    Maker_Selection=st.selectbox("Select an Automaker:",Make_List)
    Type_Selection=st.selectbox("Select an Car type:",CarType_List)
    # Since we added an "All" in the dropdown list, we have to right an if statement for all senarios where end user selects "All" from
    # either Make selection, car type selection or both
    if (Maker_Selection == "All") & (Type_Selection == "All") :
        df_filtered = df_Cars
    elif (Maker_Selection == "All") & (Type_Selection != "All"):
        df_filtered = df_Cars[(df_Cars.type==Type_Selection)]
    elif (Maker_Selection != "All") & (Type_Selection != "All"):
        df_filtered = df_Cars[(df_Cars.make==Maker_Selection)&(df_Cars.type==Type_Selection)]
    elif (Maker_Selection != "All") & (Type_Selection == "All"):
        df_filtered = df_Cars[(df_Cars.make==Maker_Selection)]
    #Let's get the min, max and avg price for the current selection

    MinPrice = int(df_filtered["price"].min())
    MaxPrice = int(df_filtered["price"].max())
    AvgPrice = int(df_filtered["price"].mean())

    # Format the values with dollar signs and commas
    formatted_max_price = f"\\${MaxPrice:,.2f}"  # Dollar sign does not need escaping in Streamlit
    formatted_min_price = f"\\${MinPrice:,.2f}"
    formatted_avg_price = f"\\${AvgPrice:,.2f}"

    # Display the formatted message in the Streamlit app
    st.write(f"For the current selections, the min price is: {formatted_min_price}, the max price is: {formatted_max_price}, and the avg price is: {formatted_avg_price}")

    # now let's set the min and max values for a price slider for end users to further narrow down their car search based on price
    PriceRange = st.slider("Based on your selections above, you can filter down further based on price if you like. Please select your price range", value=(MinPrice,MaxPrice),min_value=MinPrice,max_value=MaxPrice)
    
    df_filteredPrice=df_filtered[(df_filtered["price"]>=PriceRange[0]) & (df_filtered["price"]<=PriceRange[1])]
    
    # now let's set the min and max values for a odometer slider for end users to further narrow down their car search based on mileage
    #let's get the max and min values for the odometer from the df_filteredPrice dataframe and apply these values to set our mileage slider
    MinM = int(df_filteredPrice["odometer"].min())
    MaxM = int(df_filteredPrice["odometer"].max())
    AvgM = int(df_filteredPrice["odometer"].mean())
    MileageRange = st.slider("Based on your price selection above, you can filter further based on mileage if you like. Please select your mileage range", value=(MinM,MaxM),min_value=MinM,max_value=MaxM)
   
   # we create a new dataframe below called df_filteredMiles to reflect the records filted based on odometer mileage selected by the end user
    df_filteredMiles=df_filteredPrice[(df_filteredPrice["odometer"]>=MileageRange[0]) & (df_filteredPrice["odometer"]<=MileageRange[1])]
    df_filteredMiles
    
    
    
except Exception as e:
    st.error(f"Sorry, no cars matched your selection choices. Please try a different selection of the automaker or car type.")




#2nd Portion of our code starts here. We will be plotting a histogram and scatter plot chart:
st.header("""Viewing Car Data by Histogram and Scatter plot Charts""")
st.write("""##### Choose below the car characteristic and how it affects price for the Histogram Chart""")
#HISTOGRAM CHART: We will plot a historgram chart to see how the following factors affect a car's price: fuel, type, paint_color, make
Hist_DropdownChoice = ["make","type", "fuel","paint_color"]
choice = st.selectbox("Select a car characteristic to compare against price:",Hist_DropdownChoice)
Fig_Hist = px.histogram(df_Cars, x="price", color = choice, width=2000, height=500)
Fig_Hist.update_layout(title="<b> {} vs Price</b>".format(choice))
# we will limit the x axis range to 100,000 just to make the graph look bigger and better proportioned
Fig_Hist.update_xaxes(range=[0, 100000])
st.plotly_chart(Fig_Hist)

#SCATTER PLOT CHART:
# we will plot a scatter plot to see how the following factors affect a car's price: "age","odometer", "cyclinders","days_listed","model_year"
st.write("""#####  Choose below the car characteristic and how it affects price for the Scatter Plot Chart""")
Scatter_DropdownChoice = ["age","odometer", "cylinders","days_listed","model_year"]
# since the following columns contain null values,(age, odometer, cyclinders, and model_year) we will clean our main df_Cars dataframe of null values
# and use the resultant dataframe,(df_cleaned), for our scatter plot.
df_cleaned =df_Cars.dropna()

Scatter_choice = st.selectbox("Select one of the choices to compare against price:",Scatter_DropdownChoice)
#the colors will be based on the make of the car.
Fig_Scatter = px.scatter(df_cleaned, x="price", y=Scatter_choice, color = "make",hover_data="model", width=2000, height=500)
Fig_Scatter.update_layout(title="<b> {} vs Price</b>".format(Scatter_choice))
# we will limit the x axis range to 100,000 just to make the graph look bigger and better proportioned
Fig_Scatter.update_xaxes(range=[0, 100000])
st.plotly_chart(Fig_Scatter)

# THE WEB APP IS NOW COMPLETE.  First portion of the web app filters a dataframe.  Second portion displays an interactive Histogram
# and Scatter-plot graph