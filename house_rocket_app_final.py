import pandas         as pd
import streamlit      as st
import numpy          as np
import folium
import geopandas
import plotly.express as px
from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster
from datetime         import datetime

st.set_page_config( layout = 'wide')

@st.cache( allow_output_mutation=True )
def get_data( path ):
    data = pd.read_csv( path )
    return data

@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    geofile = geopandas.read_file( url )
    return geofile

def set_feature ( data ):
    # add new_feature
    data['price_m2'] = data['price'] / data['sqft_lot']
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    return data

def overview_data ( data ):
    # ============================
    # Data overview
    # ============================

    f_attributes = st.sidebar.multiselect(
        'Enter columns',
        data.columns
    )
    f_zipcode = st.sidebar.multiselect(
        'Enter zipcode',
        data['zipcode'].unique()
    )

    st.title('Data Overview')

    if (f_zipcode != []) & (f_attributes != []):
        d1 = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
    elif (f_zipcode != []) & (f_attributes == []):
        d1 = data.loc[data['zipcode'].isin(f_zipcode), :]
    elif (f_zipcode == []) & (f_attributes != []):
        d1 = data.loc[:, f_attributes]
    else:
        d1 = data.copy()

    st.dataframe(d1)

    c1, c2 = st.beta_columns((1, 1))
    # Average metrics

    if (f_zipcode != []):
        data = data.loc[data['zipcode'].isin(f_zipcode)];
    else:
        data = data.copy()

    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # Merge
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')
    df.columns = ['Zipcode', 'Total houses', 'Price', 'Sqft living', 'Price by M2']
    c1.title('Average Metrics')
    c1.dataframe(df, height=600, width=500)

    # Statistic descriptive
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    mean = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    df1 = pd.concat([max_, min_, mean, mediana, std], axis=1).reset_index()
    df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

    c2.title('Descriptive Analysis')
    c2.dataframe(df1, height=600, width=500)

    return None

def portfolio_density ( data, geofile ):
    # ============================
    # Densidade de Portfólio
    # ============================

    st.title('Region overview')

    c1, c2 = st.beta_columns((1, 1))

    c1.header('Porfolio density')
    df = data.copy()
    # Base map - Folium
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${} on: {}. Features: {} sqft, {} bedrooms, ''{} bathrooms, year built: {}'.format(
                          row['price'], row['date'], row['sqft_living'], row['bedrooms'], row['bathrooms'],
                          row['yr_built'])).add_to(marker_cluster)
    with c1:
        folium_static(density_map)

    # Region price map

    c2.header('Price Density')
    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

    df.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]
    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE'
                                )

    with c2:
        folium_static(region_price_map)

    return None

def commercial_distribution ( data ):
    # ==================================================
    # Distribuição dos imóveis por categorias comerciais
    # ==================================================

    st.sidebar.title('Commercial Options:')

    st.title('Commercial attributes')

    # ----------- Avg price by year

    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # Filters
    min_yr_built = int(data['yr_built'].min())
    max_yr_built = int(data['yr_built'].max())

    st.sidebar.subheader('Select max year built')
    f_year_built = st.sidebar.slider('Year built', min_yr_built, max_yr_built, min_yr_built)

    st.header('Avg price per year built')

    # Data selection
    df = data.loc[data['yr_built'] < f_year_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # Plot
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # ----------- Avg price by day

    st.header('Avg price per day')
    st.sidebar.subheader('Select max date')
    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Date', min_date, max_date, min_date)

    # Data filtering

    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # Plot
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # =============================
    # Histograma
    # =============================

    # Price
    st.header('Price distribution')
    st.sidebar.subheader('Select max price')

    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    mean_price = int(data['price'].mean())

    f_price = st.sidebar.slider('Price', min_price, max_price, mean_price)
    df = data.loc[data['price'] < f_price]

    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return None

def attributes_distribution ( data ):
    # ===========================
    # Distribuição dos imóveis por categorias físicas
    # ===========================

    st.sidebar.title('Atributes options')
    st.title('House Attributes')

    c1, c2 = st.beta_columns(2)
    # Filters
    f_bedrooms = st.sidebar.selectbox('Max number of bedrooms',
                                      data['bedrooms'].sort_values().unique(),
                                      index=3)

    data = data.loc[data['bedrooms'] <= f_bedrooms]
    c1.header('Houses per bedrooms')
    fig = px.histogram(data, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # -----------------

    f_bathrooms = st.sidebar.selectbox('Max number of bathrooms',
                                       data['bathrooms'].sort_values().unique(),
                                       index=1)

    data = data.loc[data['bathrooms'] <= f_bathrooms]
    c2.header('Houses per bathrooms')
    fig = px.histogram(data, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # -----------------
    c1, c2 = st.beta_columns(2)

    f_floors = st.sidebar.selectbox('Max number of floors',
                                    data['floors'].sort_values().unique(),
                                    index=1)

    data = data.loc[data['floors'] <= f_floors]
    c1.header('Houses per floors')
    fig = px.histogram(data, x='floors', nbins=30)
    c1.plotly_chart(fig, use_container_width=True)

    # -----------------

    f_waterview = st.sidebar.checkbox('Only houses with waterfront')

    if f_waterview:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()
    c2.header('Houses with waterfront')

    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)

    return None

if __name__ == '__main__':
    #ETL
    # Data extraction
    #Get data
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    path = 'kc_house_clean.csv'
    data = get_data(path)
    geofile = get_geofile( url )

    # Transformation
    data = set_feature( data )
    overview_data( data )
    portfolio_density ( data, geofile )
    commercial_distribution ( data )
    attributes_distribution ( data )
    # Loading
























