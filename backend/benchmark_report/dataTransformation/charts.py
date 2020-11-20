import pandas as pd
import datetime
from benchmark_report.dataTransformation.cards import Card
from benchmark_report.benchmark_report_metadata import BenchmarkReportMetadata

school_num_max = 3

class Chart:

    # get data for ploting recurrent income per st
    @staticmethod
    def get_benchmark_position_chart(similar_school_finance_df, selected_school_finance_df, metric_info):
        # select similar schools
        school_finance_df = pd.concat([selected_school_finance_df, similar_school_finance_df])

        # remove the na columns
        school_finance_df = school_finance_df.dropna()

        if school_finance_df.shape[0] < school_num_max or selected_school_finance_df.shape[0] == 0:
            return {}, {}

        selected_school_finance_df = selected_school_finance_df.to_dict('records')[0]
        # sort by values so that plot to the chart and give position

        if metric_info['good_rating'] != BenchmarkReportMetadata.smaller:
          school_finance_df =school_finance_df.sort_values(metric_info['field'], ascending=False).reset_index(drop=True)
        else:
          school_finance_df =school_finance_df.sort_values(metric_info['field'], ascending=True).reset_index(drop=True)

        school_finance_df["position"] = range(1,school_finance_df.shape[0]+1)
        median_value = round(school_finance_df[metric_info['field']].median(),2)
        selected_school_value = selected_school_finance_df[metric_info['field']]

        # get rating for metric
        #start give input to draw chart
        rating = 'unknown'
        rating_html = '''<span style="color: rgb(50, 100, 168); font-size: 40px;">&#63;</span>'''
        if metric_info['good_rating'] == BenchmarkReportMetadata.smaller:
          if selected_school_value>median_value:
              rating='bad'
              rating_html = '''<span style="color: rgb(237, 19, 19); font-size: 40px;">&#9746;</span>'''
          else:
              rating='good'
              rating_html = '''<span style="color: rgb(38, 237, 19); font-size: 40px;">&#10003;</span>'''
        elif metric_info['good_rating'] == BenchmarkReportMetadata.larger:
          if selected_school_value<median_value:
              rating='bad'
              rating_html = '''<span style="color: rgb(237, 19, 19); font-size: 40px;">&#9746;</span>'''
          else:
              rating='good'
              rating_html = '''<span style="color: rgb(38, 237, 19); font-size: 40px;">&#10003;</span>'''

        # put information for chart
        title = metric_info['label']
        traceBarX = school_finance_df["position"].values.tolist()
        traceBarY = school_finance_df[metric_info['field']].values.tolist()
        traceBarName = metric_info['label']
        # traceBarColor = color
        highlightedBarPosition = school_finance_df[school_finance_df['acara_id'] == selected_school_finance_df['acara_id']].index.values.astype(int)[0]
        traceLineX = school_finance_df["position"].values.tolist()
        traceLineY = [median_value] * school_finance_df.shape[0]
        traceLineName = 'Median ' + metric_info['label']
        chart = Chart.getComboLineBarChartJson(title, traceBarX, traceBarY, traceBarName, highlightedBarPosition, traceLineX, traceLineY, traceLineName)

        # this part for card infor of the chart
        # create infor of the chart
        formular = metric_info['formula']
        position = int(school_finance_df[school_finance_df['acara_id'] == selected_school_finance_df["acara_id"]]["position"].iloc[0])
        infor_card = Card.getCardOfSummaryChart(formular, rating, highlightedBarPosition, school_finance_df[metric_info['field']].values.tolist())

        data = {"chart": chart, "infor": infor_card}

        

        # create summary data
        summary = {'Bechmark Type': metric_info['label'] , 'Your Shool Value': selected_school_value, 'Median value of Other Schools': median_value, 'Rating': rating_html}

        #print("summary ne ", summary)

        return data, summary

    @staticmethod
    def getComboLineBarChartJson(title, traceBarX, traceBarY, traceBarName, highlightedBarPosition, traceLineX, traceLineY, traceLineName):
        trace1 = dict()
        trace1['x'] = traceBarX
        trace1['y'] = traceBarY

        # by default put the color is gray
        color = ['rgba(204,204,204,1)'] * len(traceBarX)
        # the highlighted color is red
        color[highlightedBarPosition] = 'rgba(222,45,38,0.8)'
        trace1["marker"] = {'color': color}
        trace1['type'] = 'bar'
        trace1['name'] = traceBarName
        # trace1['orientation'] = 'h'

        trace2 = dict()
        trace2['x'] = traceLineX

        trace2['y'] = traceLineY

        trace2['type'] = 'scatter'
        trace2['name'] = traceLineName

        layout =  {
                      'title': title,
                      # 'paper_bgcolor':'rgb(246, 243, 243)',
                      # 'plot_bgcolor':'rgb(246, 243, 243)',
                      'yaxis': {
                        # autotick: false,
                        # gridwidth: 2
                      },
                      'xaxis': {
                      'type': 'category'
                      },
                      'legend': {"orientation": "h"}
                    }
        return {"chart_data": [trace1,trace2], 'layout':layout}

    @staticmethod
    def getDoubleHorizontalBarChartJson(title, traceBar1X, traceBar1Y, traceBar1Name, highlightedBar1Position, traceBar2PercentX, traceBar2PercentY, traceBar2Name, highlightedBar2Position):

        trace1ColorList = ['rgba(204,204,204,1)'] * len(traceBar1X)
        for index in highlightedBar1Position:
            trace1ColorList[index] = 'rgba(222,45,38,0.8)'
        trace2ColorList = ['rgba(255,102,0,1)'] * len(traceBar2PercentX)
        for index in highlightedBar2Position:
            trace2ColorList[index] = 'rgba(0,153,0,1)'

        trace1 = {
        'x': traceBar1X,
        'y': traceBar1Y,
        'xaxis': 'x1',
        'yaxis': 'y1',
        'type': 'bar',
        'marker': {
          'color': trace1ColorList
        },
        'name': traceBar1Name,
        'orientation': 'h'
        }
        trace2 = {
        'x': traceBar2PercentX,
        'y': traceBar2PercentY,
        'xaxis': 'x2',
        'yaxis': 'y1',
        'type': 'bar',
        'marker': {
          'color': trace2ColorList
        },
        'name': traceBar2Name,
          'orientation': 'h'
        };

        layout = {

        'title': title, #{'text': title, 'xanchor': 'left', 'yanchor': 'top'},
        'xaxis1': {
          'range': [0, float(max(traceBar1X))],
          'domain': [0, 0.5],
          'zeroline': False,
          'showline': False,
          'showticklabels': True,
          'showgrid': True
        },
        'xaxis2': {
          'tickformat': ',.0%',
          'range': [float(min(traceBar2PercentX)),float(max(traceBar2PercentX))],
          'domain': [0.5, 1],
          'zeroline': False,
          'showline': False,
          'showticklabels': True,
          'showgrid': True,
          'side': 'top'
        },
        'yaxis1': {
          'showticklabels': True,
          'type': 'category'
        },
        'yaxis2': {
          'showticklabels': True,
          'type': 'category'
        },
        'legend': {"orientation": "h"},
        'margin': {
          'l': 200,
          'r': 20
          # 't': 200,
          # 'b': 70
        },
        'height': 800,
        # 'paper_bgcolor':'rgb(246, 243, 243)',
        # 'plot_bgcolor':'rgb(246, 243, 243)'
        }

        return {"chart_data": [trace1,trace2], 'layout':layout}

    @staticmethod
    def getstackedBarchart(data, title, xTitle, yTitle, isDataPercented = False, IsTextShown = False):
        # data: 'xAxis', 'yAxis','category','text'
        # for per centage text, if the data is percentage, do not need to calcuate percentage text
        if isDataPercented == False:
            if(0):
                data["percent"] = 0
                for index, row in data.iterrows():
                    total = data[data["xAxis"] == row["xAxis"]]['yAxis'].sum()
                    data.loc[index,'percent'] = round(row['yAxis']*100/total,2)
                if data['yAxis'].max() > 1000:
                    data['textyAxis'] = data['yAxis'].apply(lambda y: round(y/1000,2)  ).astype(str) + 'K'
                    data['text'] = data["percent"].astype(str) + '% <br />'
                else:
                    data['text'] = data["percent"].astype(str) + '% <br />'
            data['text'] = data['yAxis']
        else:
            # print('fixxxx khoooooooooooooo')
            # data['text'] = round(data["yAxis"],2)
            data['text'] = round(data["yAxis"] *100,2)
            data['text'] = data['text'].astype(str) + '%'

        chart = []
        categoryList = data['category'].unique().tolist()
        for category in categoryList:
            trace = dict()
            trace['x'] = data['xAxis'].unique().tolist()
            trace['y'] = data[data['category'] == category]['yAxis'].values.tolist()
            trace['text'] = data[data['category'] == category]['text'].values.tolist()
            trace['textposition']= 'auto'
            trace['type'] = 'bar'
            trace['name'] = category
            chart.append(trace)

        traceLine = dict()
        total_df = data.groupby('xAxis').agg({'yAxis':'sum'}).reset_index()
        trace3 = {
        'x': total_df['xAxis'],
        'y': total_df['yAxis'],
        'name': 'Total',
        # 'text':['123','22','3'],
        # 'textposition': 'auto',
        'type': 'scatter'
        }

        chart.append(traceLine)


        layout = {'barmode': 'stack',
        # 'paper_bgcolor':'rgb(246, 243, 243)',
        # 'plot_bgcolor':'rgb(246, 243, 243)',
        'legend': {"orientation": "h"},
        'title': title,
        'xaxis': {
          'showticklabels': True,
          'type': 'category',
          'title': xTitle

        },
        'yaxis':{
        # 'range': [10000, max_v+10000],
        'zeroline': False,
        'showline': False,
        'showgrid': True,
        'title':yTitle
        }
        }

        if isDataPercented == True:
            layout['yaxis']['tickformat'] = ',.0%'
            layout['yaxis']['range'] = [0,1]
            #  yaxis: {
            #   tickformat: ',.0%',
            #   range: [0,1]
            # },

        return {"chart_data": chart, 'layout':layout}

    @staticmethod
    def getSimpleBarChart(data, title, xTitle, yTitle):
        # data: x => xaxis, y => yaxis, text
        trace = dict()
        chart = []
        trace['x'] = data['xAxis'].tolist()
        trace['y'] = data['yAxis'].tolist()
        trace['type'] = 'bar'
        trace['text'] = data['text'].tolist()
        trace['textposition']= 'auto'

        chart.append(trace)

        layout = {
        'showlegend': False,
        'title': title,
        'xaxis': {
          'showticklabels': True,
          'type': 'category',
          'title': xTitle
        },
        'yaxis':{
        'zeroline': False,
        'showline': False,
        'showgrid': True,
        'title':yTitle
            }
        }
        return {"chart_data": chart, 'layout':layout}

    @staticmethod
    def getLineChart(data, title, xTitle, yTitle):

        chart = []
        categoryList = data['category'].unique().tolist()
        for category in categoryList:
            trace = dict()
            trace['x'] = data['xAxis'].unique().tolist()
            trace['y'] = data[data['category'] == category]['yAxis'].values.tolist()
            # trace['text'] = data[data['category'] == category]['text'].values.tolist()
            # trace['textposition']= 'auto'
            # trace['type'] = 'bar'
            trace['name'] = category
            trace['mode'] = 'lines+markers'
            chart.append(trace)

        layout = {
            'legend': {"orientation": "h"},
            'title': title,
            'hoverlabel': {"namelength": -1},
            'xaxis': {
              'showticklabels': True,
              'type': 'category',
              'title': xTitle
            },
            'yaxis':{
            'zeroline': False,
            'showline': False,
            'showgrid': True,
            'title':yTitle
            }
        }


        return {"chart_data": chart, 'layout':layout}
