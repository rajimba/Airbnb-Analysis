import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu
from shapely.geometry import Point
import geopandas as gpd
import sklearn

st.set_page_config(layout='wide')

with st.sidebar:
    select= option_menu("Main Page",["HomePage","Analysis"])


filepath = "C:/Users/rajij/Downloads/Airbnb1.csv"
df = pd.read_csv(filepath)


def priceanalysis(column1, column2):
    col1, col2 = st.columns([10,1])
    with col1:
        filepath = "C:/Users/rajij/Downloads/Airbnb1.csv"
        df = pd.read_csv(filepath)
        df_p = df[df['country']==country_s]
        avg_price = df_p.groupby(column1)[column2].mean().reset_index()

        plt.figure(figsize=(15,4)) 
    
        plt.bar(avg_price[column1], avg_price[column2], color='darkred')

        plt.xlabel(column1, fontsize=12)
        plt.ylabel(column2, fontsize=12)
        plt.title(f"Average Price - {column1}")
        for index, value in enumerate(avg_price[column2]):
            plt.text(index, value, f'{value:.1f}', ha='center', va='bottom', fontsize=8)
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        plt.tick_params(axis='both', labelsize=8)    
        return st.pyplot(plt)

def Availability(days):
    df_c = df[df['country'] == country_s]

# Group by '30_days' and count occurrences of 'name'
    count_avail = df_c.groupby(days)['name'].count().reset_index()

    plt.figure(figsize=(20,4))  # Adjust width and height here

    plt.plot(count_avail[days], count_avail['name'], marker='o', color='orange', linestyle='-')

    plt.xlabel(f" {days} Availability", fontsize=20)
    plt.ylabel('No. of Property Available for Rent', fontsize=12)
#plt.title(f" {days} Availability Trend", fontsize=24)

# Add value labels on the points
# for index, value in enumerate(count_avail['name']):
#     plt.text(count_avail[days].iloc[index], value + 0.5, f'{value}', ha='center')

    return st.pyplot(plt), count_avail

def toprated(column1, column2):

    df_p = df[df['country'] == country_s]

    # Calculate the average price
    avg_price = df_p.groupby(column1)[column2].sum().reset_index()

    # Sort the DataFrame by the average price in descending order and get the top 10
    top_avg_price = avg_price.nlargest(10, column2)

    # Create the bar chart
    plt.figure(figsize=(15, 4))
    plt.bar(top_avg_price[column1], top_avg_price[column2], color='darkblue')

    # Set labels and title
    plt.xlabel(column1, fontsize=12)
    plt.ylabel(column2, fontsize=12)
    

    # Annotate the bars
    for index, value in enumerate(top_avg_price[column2]):
        plt.text(index, value, f'{value:.1f}', ha='center', va='bottom', fontsize=8)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    plt.tick_params(axis='both', labelsize=8)

    # Display the plot using Streamlit
    return st.pyplot(plt)

if select =="HomePage":
 st.title("Airbnb Analysis")
 st.subheader("Airbnb, Inc. is an American company operating an online marketplace for short-and-long-term homestays and experiences in various countries and regions. It acts as a broker and charges a commission from each booking. Airbnb was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. It is the most well-known company for short-term housing rentals. ")
 image_path = "C:/Users/rajij/Downloads/airbnb image.png" 
 st.image(image_path, use_column_width=100)

elif select=='Analysis':
    tab1,tab2= st.tabs(["Geospatial Visualization","General Analysis"])
    with tab1:
      
        df_loc = df[['country', 'longitide', 'latitude', 'street', 'property_type', 'room_type', 'beds', 'number_of_reviews', 'minimum_nights', 'maximum_nights','365_days', 'price', 'security_deposit', 'cleaning_fee','amenities']]
        
        country_d = sorted(df_loc['country'].unique())

        country_s= st.selectbox('Please select a Country from the dropdown below:', country_d, index=None, key=1)

        df_location = (df_loc[df_loc['country']==country_s])

        if country_s is None:
            pass
        else:
#############################Geo Map#######################################################3        
            st.markdown("""<h2 style='text-align: center; color: pink;'>Airbnb Listings</h2>""", unsafe_allow_html=True) 

            fig = px.scatter_geo(df_location, lat='latitude', lon='longitide', hover_name='country', hover_data={'street': True, 'property_type': True, 'room_type': True, 'beds': True, '365_days': True, 'price': True, 'security_deposit': True, 'cleaning_fee': True, 'number_of_reviews': True, 'minimum_nights': True, 'maximum_nights': True},
            color='property_type', 
            color_continuous_scale=px.colors.sequential.Plasma  
            )


    # Update layout
    #fig.update_layout(title='Airbnb Listings', title_x=0.4)

            st.plotly_chart(fig,use_container_width=True)
            
#########Availability Trend###############################################
            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Availability in {country_s}</h2>""", unsafe_allow_html=True)
            col1, col2 = st.columns([5,1])
            with col1:
                Availability('30_days')

            col1, col2 = st.columns([7,1])
            with col1:
                Availability('60_days')
            
            col1, col2 = st.columns([50,1])
            with col1:
                Availability('90_days')

            col1, col2 = st.columns([500,1])
            with col1:
                Availability('365_days')    

###################Price Trend####################################3                

            st.markdown(f"""<h2 style='text-align: center; color:pink;'>Airbnb Average Price - Property Type in {country_s}</h2>""", unsafe_allow_html=True)
            priceanalysis('property_type', 'price')

            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Average Price - Room Type in {country_s}</h2>""", unsafe_allow_html=True)
            priceanalysis('room_type', 'price') 

            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Average Price - Suburb in {country_s}</h2>""", unsafe_allow_html=True)
            priceanalysis('suburb', 'price')

            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Top 10 Host Based on Reviews in {country_s}</h2>""", unsafe_allow_html=True)
            
            toprated('host_name', 'number_of_reviews')

            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Top 10 Location Based on Reviews in {country_s}</h2>""", unsafe_allow_html=True)
            
            toprated('street', 'number_of_reviews')            

            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Top 10 High Priced Location in {country_s}</h2>""", unsafe_allow_html=True)
            
            toprated('street', 'price')

            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Cheapest Destination in {country_s}</h2>""", unsafe_allow_html=True)

            df_p = df[df['country'] == country_s]

            # Calculate the average price
            avg_price = df_p.groupby('street')['price'].sum().reset_index()

            # Sort the DataFrame by the average price in descending order and get the top 10
            top_avg_price = avg_price.nsmallest(10, 'price')

            # Create the bar chart
            plt.figure(figsize=(15, 4))
            plt.bar(top_avg_price['street'], top_avg_price['price'], color='darkblue')

            # Set labels and title
            plt.xlabel('street', fontsize=12)
            plt.ylabel('price', fontsize=12)
            

            # Annotate the bars
            for index, value in enumerate(top_avg_price['price']):
                plt.text(index, value, f'{value:.1f}', ha='center', va='bottom', fontsize=8)

            # Rotate x-axis labels
            plt.xticks(rotation=45, ha='right')
            plt.tick_params(axis='both', labelsize=8)

            # Display the plot using Streamlit
            st.pyplot(plt)
################Total LIsting based on property type###################################            
            st.markdown(f"""<h2 style='text-align: center; color: pink;'>Airbnb Total Listing - Property Type in {country_s}</h2>""", unsafe_allow_html=True)          
            df_p = df[df['country'] == country_s]

            # Calculate the average price
            property_counts = df_p.groupby('property_type')['name'].count().reset_index()

            plt.figure(figsize=(10, 5))
            colors = plt.cm.tab10.colors
            patches, texts = plt.pie(
                property_counts['name'],
#                labels=property_counts['property_type'],
                startangle=180,
                colors=colors,

                labeldistance=1.2 # Distance of labels from center
            )

            # Set equal aspect ratio for a circular pie chart
            plt.axis('equal')

             # Adjust font size for the labels
            for text in texts:
                text.set_fontsize(6)

            # Create a legend next to the pie chart
            plt.legend(patches, [f"{ptype}: {count}" for ptype, count in zip(property_counts['property_type'], property_counts['name'])],
                    title="Property Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)

            # Display the plot using Streamlit
            st.pyplot(plt)
##############################Host Information Based on Location, Availability and Property Type##############################################################
            col1, col2, col3 = st.columns([1,1, 1])
            with col1:

                # Filter DataFrame for the selected country
                df_p = df[df['country'] == country_s]
                
                # Get unique street names
                street_d = sorted(df_p['street'].unique())
                
                # Select a destination from the filtered streets
                destination = st.selectbox('Please select a destination from the dropdown below:', street_d, index=None, key=3)

            with col2:
                # Availability options
                Availability = ['30_days', '60_days', '90_days', '365_days']
                Availability_ = st.selectbox('Please select an availability period:', Availability, index=None, key=4)

            with col3:
                # Availability options
                Property_type_d = sorted(df_p['property_type'].unique())
                Property_type_ = st.selectbox('Please select a property type:', Property_type_d,index=None, key=5)                

            # Check if the selection is valid
            if destination and Availability_ and Property_type_:
                # Filter the DataFrame based on destination and availability
                df_list = df[(df['street'] == destination) & (df['property_type'] == Property_type_) & (df[Availability_] > 0)]
                
                # Display the filtered DataFrame
                st.dataframe(df_list)
            else:
                pass



    with tab2:
        st.subheader("Average Cost Per Day Stay & Listing Count Across Countries")
##########PRICE TREND AND LISTING INFO BASED ON PROPERTY TYPE FOR COUNTRY AND CITY#########################################################################################################
        Proptype_d = df_loc['property_type'].unique()

        Proptype_s= st.selectbox('Please select a property_type from the dropdown below:', Proptype_d, index=None, key=2)
        
        if Proptype_s is None:
            pass
        else:
            col1, col2 = st.columns([1,1])
            with col1:
                

                df_prop = (df[df['property_type']==Proptype_s])

                avg_price = df_prop.groupby('country')['price'].mean().reset_index()

                plt.figure(figsize=(8, 4)) 
            
                plt.barh(avg_price['country'], avg_price['price'], color='darkblue')

                plt.xlabel('Price')
                plt.ylabel('Country')
                plt.title('Average Price - Country')
                for index, value in enumerate(avg_price['price']):
                    plt.text(value, index, f'{value:.1f}')
                st.pyplot(plt)

            with col2:
            
                df_prop = (df[df['property_type']==Proptype_s])

                avgp_price = df_prop.groupby('market')['price'].mean().reset_index()

                plt.figure(figsize=(8, 4)) 

                plt.barh(avgp_price['market'], avgp_price['price'], color='Purple')

                plt.xlabel('Price')
                plt.ylabel('City')
                plt.title('Average Price - City')
                for index, value1 in enumerate(avgp_price['price']):
                    plt.text(value1, index, f'{value1:.1f}')
                st.pyplot(plt)

            col1, col2 = st.columns([1,1])
            with col1:
                

                df_prop = (df[df['property_type']==Proptype_s])

                avg_price = df_prop.groupby('country')['name'].count().reset_index()

                plt.figure(figsize=(8, 4)) 
            
                plt.barh(avg_price['country'], avg_price['name'], color='darkred')

                plt.xlabel('No.of Airbnb listings')
                plt.ylabel('Country')
                plt.title('No.of listing - Country')
                for index, value in enumerate(avg_price['name']):
                    plt.text(value, index, f'{value:.1f}')
                st.pyplot(plt)

            with col2:
                

                df_prop = (df[df['property_type']==Proptype_s])

                avg_price = df_prop.groupby('market')['name'].count().reset_index()

                plt.figure(figsize=(8, 4)) 
            
                plt.barh(avg_price['market'], avg_price['name'], color='orange')

                plt.xlabel('No.of Airbnb listings')
                plt.ylabel('City')
                plt.title('No.of listing - City')
                for index, value in enumerate(avg_price['name']):
                    plt.text(value, index, f'{value:.1f}')
                st.pyplot(plt)                
##########PRICE TREND AND LISTING INFO BASED ON ROOM TYPE FOR COUNTRY AND CITY#########################################################################################################

        roomtype_d = df_loc['room_type'].unique()

        roomtype_s= st.selectbox('Please select a room_type from the dropdown below:', roomtype_d, index=None, key=7)
        if roomtype_s is None:
            pass
        else:

            col1, col2 = st.columns([1,1])
            with col1:
                

                df_prop = (df[df['room_type']==roomtype_s])

                avg_price = df_prop.groupby('country')['price'].mean().reset_index()

                plt.figure(figsize=(8, 4)) 
            
                plt.barh(avg_price['country'], avg_price['price'], color='darkblue')

                plt.xlabel('Price')
                plt.ylabel('Country')
                plt.title('Average Price - Country')
                for index, value in enumerate(avg_price['price']):
                    plt.text(value, index, f'{value:.1f}')
                st.pyplot(plt)

            with col2:
            
                df_prop = (df[df['room_type']==roomtype_s])

                avgp_price = df_prop.groupby('market')['price'].mean().reset_index()

                plt.figure(figsize=(8, 4)) 

                plt.barh(avgp_price['market'], avgp_price['price'], color='Purple')

                plt.xlabel('Price')
                plt.ylabel('City')
                plt.title('Average Price - City')
                for index, value1 in enumerate(avgp_price['price']):
                    plt.text(value1, index, f'{value1:.1f}')
                st.pyplot(plt)

            col1, col2 = st.columns([1,1])
            with col1:
                

                df_prop = (df[df['room_type']==roomtype_s])

                avg_price = df_prop.groupby('country')['name'].count().reset_index()

                plt.figure(figsize=(8, 4)) 
            
                plt.barh(avg_price['country'], avg_price['name'], color='darkred')

                plt.xlabel('No.of Airbnb listings')
                plt.ylabel('Country')
                plt.title('No.of listing - Country')
                for index, value in enumerate(avg_price['name']):
                    plt.text(value, index, f'{value:.1f}')
                st.pyplot(plt)

            with col2:
                

                df_prop = (df[df['room_type']==roomtype_s])

                avg_price = df_prop.groupby('market')['name'].count().reset_index()

                plt.figure(figsize=(8, 4)) 
            
                plt.barh(avg_price['market'], avg_price['name'], color='orange')

                plt.xlabel('No.of Airbnb listings')
                plt.ylabel('City')
                plt.title('No.of listing - City')
                for index, value in enumerate(avg_price['name']):
                    plt.text(value, index, f'{value:.1f}')
                st.pyplot(plt)                       

#st.table(df_prop)