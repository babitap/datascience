from django.db import connections
import pandas as pd
import math
import itertools
import numpy as np

def stringifyRange(rng):
    string=['%s' for _ in range(len(rng))]
    string=",".join(string)
    return string

def calcOutliers(df,alpha=1.5):
    
    #Find bounds
    Q1,Q3=df['Value'].quantile(0.25),df['Value'].quantile(0.75)

    #print("quant", Q1, Q3)
    IQR=Q3-Q1

    #Double check
    low=max(Q1-alpha*IQR, df['Value'].min())
    high=min(Q3+alpha*IQR,df['Value'].max())

    #Check filter vals to min/max
    #low = low if low<-500 else -500
    #high = high if high>500 else 500
    
    #Filter
    if low!=high:
        df=df[(df['Value']>=low)&(df['Value']<=high)]
        
    return df

def roundCols(df):

    #Check value size
    cols=[col for col in df if col not in ['Code','Name','Year','Label','Latitude','Longitude']]
    for col in cols:
        #Change round size based on decimals on max value
        df[col]=df[col].round(2)

    return df

def checkThematic(params):

    #Split thematic if exists
    them_type='abs'
    thematic=params['thematic'][0]
    if thematic.endswith('/sqkm'):
        thematic=thematic.split('/sqkm')[0]
        them_type='dty'
    elif thematic.endswith(' Change'):
        thematic=thematic.split(' Change')[0]
        them_type='chg'
    elif thematic.endswith(' Change %'):
        thematic=thematic.split(' Change %')[0]
        them_type='per'

    #Reset params
    params['thematic'][0]=thematic

    return params,them_type

def convertRegionToTbl(region):

    #Get index and db
    if region == 'SA1': return 'SA1_MAINCODE_2016','SA1_NAME_2016','dbo.abs_Area_SA'
    elif region == 'SA2': return 'SA2_MAINCODE_2016','SA2_NAME_2016','dbo.abs_Area_SA'
    elif region == 'SA3': return 'SA3_CODE_2016','SA3_NAME_2016','dbo.abs_Area_SA'
    elif region == 'SA4': return 'SA4_CODE_2016','SA4_NAME_2016','dbo.abs_Area_SA'
    elif region == 'GCC': return 'GCCSA_CODE_2016','GCCSA_NAME_2016','dbo.abs_Area_SA'
    elif region == 'STE': return 'STATE_CODE_2016','STATE_NAME_2016','dbo.abs_Area_SA'
    elif region == 'POA': return 'POA_CODE_2016','POA_CODE_2016','dbo.abs_Area_POA'
    elif region == 'LGA': return 'LGA_CODE_2016','LGA_NAME_2016','dbo.abs_Area_LGA'
    elif region == 'SSC': return 'SSC_CODE_2016','SSC_NAME_2016','dbo.abs_Area_SSC'

def getArea(region):

    index,tbl = convertRegionToTbl(region)

    #SQL query
    sql=[
        "select",
        index,
        "as Code, sum(AREASQKM) as Area from",
        tbl,
        "group by",
        index
    ]
    sql=' '.join(sql)
    #print(sql)

    #Run query
    df=pd.read_sql(
        sql=sql,
        con=connections['public_data']
        )

    return df

def calcDensity(df, region):

    #Add area to df
    df=df.merge(getArea(region),on='Code')

    #Calc density
    df['Value']=df.apply(lambda x: x['Value']/x['Area'] if x['Area']!=0 else np.nan, axis=1)
    df=df.drop(['Area'], axis=1)

    return df

def calcDifferences(df_in, them_type, included_cols):
    """
    Calculate the differences to the value column
    >>Input should always be dataframe with columns as keys, Year,  Value
    """

    keysAndYear = included_cols + ['Year']

    #Get all combinations of code and year
    #df=pd.DataFrame(list(itertools.product(df_in[included_cols].drop_duplicates(), df_in['Year'].unique())), columns=keysAndYear)

    df1 = df_in[included_cols].drop_duplicates()
    df1['tempKey'] = 1
    
    df2 = df_in[["Year"]].drop_duplicates()
    df2['tempKey'] = 1
    
    df = df1.merge(df2, on='tempKey')[keysAndYear]
    
    #Merge Data

    
    df=df.merge(df_in,on=keysAndYear,how='outer').fillna(0)

    

    #Ensure order
    df=df.sort_values(keysAndYear)

    #Calc change
    df['last']=df.groupby(included_cols)['Value'].transform('first')

    

    df['Change']=df['Value'] - df['last']
    if them_type=='per':
      df['Change %']=df['Change']/df['Value']*100
      df.loc[df['Change %']==np.inf,['Change %']] = 100
      df.loc[df['Change %']==-np.inf,['Change %']] = -100
      #print("df cal diff marker 4", df[df["Code"] == '302031036' ])
      #print("df cal diff marker 5", df[df['Change %'].isin([-np.inf, np.inf]) ])
   
    

    #Remove first transformed column
    col='Change' if them_type=='chg' else 'Change %' if them_type=='per' else 'Value'
    all_needed_cols = keysAndYear + [col]
    #print("merge ",all_needed_cols)
    df=df[all_needed_cols].rename({col:'Value'}, axis=1)

    
    #print("df cal diff marker", df)
    #Drop nans
    df=df.dropna()

    #print("df cal diff marker 2", df[df["Value"].isin([-np.inf, np.inf]) ])
    

    return df

def setCirclePolygon(name, latitude, longitude, edges):

        def getCoordByAng(lat, lon, phi, d):

            #Convert inputs to radians
            R = 6378.1 #Earth radius
            phi = math.pi * phi/180;
            lat = math.pi * lat/180;
            lon = math.pi * lon/180;

            #Calc new point
            new_lat = math.asin( math.sin(lat)*math.cos(d/R) + math.cos(lat)*math.sin(d/R)*math.cos(phi));
            new_lon = lon + math.atan2(math.sin(phi)*math.sin(d/R)*math.cos(lat), math.cos(d/R)-math.sin(lat)*math.sin(lat));

            #Convert new point to degrees
            new_lat = new_lat * 180/math.pi;
            new_lon = new_lon * 180/math.pi;

            return [new_lon,new_lat]
        
        #-------------------------------------------
        #Define polygon geojson
        #Start with main school entered as a point
        polygon={
            "type":"FeatureCollection", 
            "features": [{
                "type":"Feature",
                "geometry":{
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "properties":{
                    "description": name
                }
            }]}

        #Go thru all radii
        for radius in [2,5,10]:
            #Reset coords
            coords=[];
            for i in range(edges):
                coords.append(getCoordByAng(latitude, longitude, i*(360/edges), radius))
            
            #Add to polygon
            polygon['features'].append({
                "type":"Feature",
                "geometry":{
                    "type": "LineString",
                    "coordinates": coords
                },
                "properties":{
                    "description": str(radius)+" km",
                    "stroke": "#53a0db",
                    "stroke-width": 3
                }
            })

        return polygon

def modify_params(layer_type, params):
    #Need to modify keys based on region type

    if layer_type == 'region':

        if 'dropdown1' in params:
            params['state'] = params.pop('dropdown1')

        if 'dropdown2' in params:
            params['region'] = params.pop('dropdown2')

        if 'dropdown3' in params:
            params['gender'] = params.pop('dropdown3')

        if 'dropdown4' in params:
            params['thematic'] = params.pop('dropdown4')

        if 'dropdown5' in params:
            params['year'] = params.pop('dropdown5')

    elif layer_type == 'marker':

        if 'dropdown1' in params:
            params['state'] = params.pop('dropdown1')

        if 'dropdown2' in params:
            params['sector'] = params.pop('dropdown2')

        if 'dropdown3' in params:
            params['type'] = params.pop('dropdown3')

        if 'dropdown4' in params:
            params['thematic'] = params.pop('dropdown4')

        if 'dropdown5' in params:
            params['year'] = params.pop('dropdown5')

    return params
