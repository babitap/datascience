import pandas as pd
import datetime
import statistics

class Card:
    @staticmethod
    def getCardOfSummaryChart(formular, rating, selected_school_position, sorted_schools_values):

        # create infor of the chart
        print("position", selected_school_position)

        total_samples = len(sorted_schools_values)
        left_side_schools = round((selected_school_position)*100/(len(sorted_schools_values)-1),2)
        right_side_schools = round((len(sorted_schools_values) - selected_school_position-1)*100/(len(sorted_schools_values)-1),2)
        median_value = round(statistics.median(sorted_schools_values),2)
        infor_card = {
        "formular":formular, "position":int(selected_school_position+1),
        "total_samples":total_samples,
        "left_side_schools":left_side_schools,
        "right_side_schools":right_side_schools,
        "median" : median_value,
        "school_value": (sorted_schools_values[selected_school_position]),
        "rating": rating
        }

        return infor_card
