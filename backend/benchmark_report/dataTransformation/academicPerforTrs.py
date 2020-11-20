from benchmark_report.dataTransformation.dataConnection import *
import pandas as pd
import datetime
from benchmark_report.dataTransformation.charts import Chart
from benchmark_report.dataTransformation.cards import Card
import numpy as np
school_num_max = 3


def getPostStuDestination(similar_schools_df, selected_school):
    # select similar schools
    selected_school = selected_school.dropna()
    similar_schools_df = similar_schools_df.dropna()

    # sort by values so that plot to the chart and give position
    if similar_schools_df.shape[0] < school_num_max :
        return {}
    # selected_school = selected_school.to_dict('records')[0]
    similar_schools_df = similar_schools_df.mean()
    # get mean value
    # print(similar_schools_df)
    # print(selected_school)
    selected_school['acara_school_id'] = 'Your School'
    similar_schools_df['acara_school_id'] = 'Siminar Schools'
    schools_df = selected_school.append(similar_schools_df, ignore_index=True)
    # print(type(similar_schools_df))
    schools_df = schools_df.rename(columns = {"students_at_university" : 'students at university', 'students_at_tafe': 'students at tafe', 'students_in_employment': 'students in employment' })
    schools_df = pd.melt(schools_df, id_vars=['acara_school_id'], value_vars=['students at university', 'students at tafe', 'students in employment'])
    schools_df = schools_df.rename(columns= {'acara_school_id': 'xAxis', 'variable' : 'category', 'value': 'yAxis'})
    schools_df['yAxis'] = round(schools_df['yAxis']/100,2)
    chart = Chart.getstackedBarchart(schools_df, "Students' Post School Destinations (%)",'','Performance rate', True)

    # create infor of the chart
    # formular = "Percentage."
    # position = int(schools_df[schools_df['acara_school_id'] == selected_school['acara_school_id']]["position"].iloc[0])
    # infor_card = Card.getCardOfSummaryChart(formular, rating, highlightedBarPosition, schools_df["nonteachingStaffRate"].values.tolist())

# , "infor": infor_card
    data = {"chart": chart}

    return data
