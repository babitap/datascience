
from benchmark_report.dataTransformation.dataConnection import *
import pandas as pd
import datetime
from benchmark_report.dataTransformation.charts import Chart
from benchmark_report.dataTransformation.cards import Card
import numpy as np


school_num_max = 3

# for the change in student number chart
def get_data_for_change_in_student_enrolment(similar_schools_df, selected_school):

    # select similar schools
    schools_df = pd.concat([similar_schools_df, selected_school])
    schools_df = schools_df.dropna()
    # sort by values so that plot to the chart and give position
    if schools_df.shape[0] < school_num_max :
        return {}
    selected_school = selected_school.to_dict('records')[0]
    data = dict()
    schools_df['changePercent']  = round((schools_df['enroChanged']) /schools_df['prevEnroNum'],2)
    # schools_df = schools_df.dropna()
    schools_df =schools_df.sort_values('total_enrolments', ascending=True).reset_index(drop=True)

    schools_df["position"] = range(schools_df.shape[0],0,-1)
    highlightedBar1Position = []
    highlightedBar2Position = []
    for index, row in schools_df.iterrows():

        if row['acara_id'] == selected_school['acara_id']:
            highlightedBar1Position.append(index)

        if row['changePercent'] > 0:
            highlightedBar2Position.append(index)
    title = 'Number of Enrolment Change'
    traceBar1X = schools_df['total_enrolments'].values.tolist()
    traceBar1Y = ('School ' + schools_df['position'].astype(str)).values.tolist()# (schools_df['school_name'].astype(str)).values.tolist() #('Position ' + schools_df['position'].astype(str)).values.tolist() # (schools_df['school_name'].astype(str)).values.tolist()#('Position ' + schools_df['position'].astype(str)).values.tolist() #(schools_df['acara_id'].astype(str) +'_'+ schools_df['position'].astype(str)).values.tolist()
    traceBar1Name = 'Student Number'
    traceBar2PercentX = schools_df['changePercent'].values.tolist()
    traceBar2PercentY = ('School ' + schools_df['position'].astype(str)).values.tolist() #(schools_df['school_name'].astype(str)).values.tolist() #   #(schools_df['acara_id'].astype(str) +'_'+ schools_df['position'].astype(str)).values.tolist()
    traceBar2Name = 'Change In enrolment compared with previous year'
    chart = Chart.getDoubleHorizontalBarChartJson(title, traceBar1X, traceBar1Y, traceBar1Name, highlightedBar1Position, traceBar2PercentX, traceBar2PercentY, traceBar2Name, highlightedBar2Position)

    data = {"chart": chart}

    return data
