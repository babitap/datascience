

class BenchmarkReportMetadata:

  larger = 1
  smaller= 2
  unknown = 3


  filterColumnsDict = {"filters": [\
    {"type":"multioption", "fronEndVarSelectedDefault": "stateDefaultOption", "fronEndVarOptions": "stateOptions", "dbCol":"State", "label": "State"},
    {"type":"multioption", "fronEndVarSelectedDefault": "schoolSectorDefaultOption", "fronEndVarOptions": "schoolSectorOptions", "dbCol":"School_Sector", "label": "School Sector"},
    {"type":"multioption", "fronEndVarSelectedDefault": "schoolTypeDefaultOption", "fronEndVarOptions": "schoolTypeOptions", "dbCol":"School_Type", "label": "School Type"},
    {"type":"singleoption", "fronEndVarSelectedDefault": "schoolGenderDefaultOption", "fronEndVarOptions": "schoolGenderOptions", "dbCol":"Gender", "label": "Gender", "defaultOptions":[{"label": "Both Genders", "value": "Both Genders"},{"label": "Only Boys", "value": "Only Boys"} ,{"label": "Only Girls", "value": "Only Girls"} ]},
    {"type":"multioption", "fronEndVarSelectedDefault": "geolocationDefaultOption", "fronEndVarOptions": "geolocationOptions", "dbCol":"Geolocation", "label": "ABS Area"},
    {"type":"int", "fronEndVarSelectedDefault": "enrolmentRangeStartValue", "fronEndVarOptions": "enlNumFromOptions", "dbCol":"Enrolment_Number From", "label": "Enrolment Number From","defaultOptions":[1]},
    {"type":"int", "fronEndVarSelectedDefault": "enrolmentRangeEndValue", "fronEndVarOptions": "enlNumToOptions", "dbCol":"Enrolment_Number To", "label": "Enrolment Number To","defaultOptions":[10000]},
    {"type":"singleoption", "fronEndVarSelectedDefault": "YearValue", "fronEndVarOptions": "calendarYearOptions", "dbCol":"Calendar_Year", "label": "Calendar Year"},
    #{"type":"int", "fronEndVarSelectedDefault": "distanceKmValue", "fronEndVarOptions": "distanceOptions", "dbCol":"Distance_Within", "Distance Within": "Calendar Year", "defaultOptions":[100]},
    ]}

  acara_benchmark_report_metrics = \
  [
      {
          'label': 'Enrolment Analysis',
          'value': 'student_enrol_analysis',
          'metrics': [
                    
                      {
                          'value' : 'student_number',
                          'label' : 'Student Enrolment Number',
                          'field' : 'total_enrolments',
                          'formula': 'Total enrolment',
                          'good_rating': larger,
                        
                      },
                  
                  ],
      },
      {
          'label': 'Staff Analysis',
          'value': 'staffing_analysis',
          'metrics':  [
                    
                      {
                          'value' : 'non_teaching_ratios',
                          'label' : 'Student/Non-Teacher ratios',
                          'field' : 'nonteachingStaffRate',
                          'formula': "Total enrolment / Total Full-time equivalent non-teacher number (if staff number is 0, by default it will be set to 0.9).",
                          'good_rating': larger,
                      },
                      {
                          'value' : 'teaching_ratios',
                          'label' : 'Student/Teacher ratios',
                          'field' : 'teachingStaffRate',
                          'formula': "Total enrolment / Total Full-time equivalent teacher number. (if staff number is 0, by default it will be set to 0.9).",
                          'good_rating': larger,
                      },
                  
                  ],
      },

      {
          'label': 'Finance Analysis',
          'value': 'financial_analysis',
          'metrics':  [
                    
                      {
                          'value' : 'recurrent_income_per_st',
                          'label' : 'Total Recurrent income per student $',
                          'field' : 'Income_Total_Net_Recurrent_Per_Student',
                          'formula': "Total Recurrent Income / number of students.",
                          'good_rating': unknown,
                      },
                      {
                          'value' : 'fee_income_per_st',
                          'label' : 'Total Fee income per student $',
                          'field' : 'Income_Fees_Charges_Parent_Per_Student',
                          'formula': "Total Fee Income / number of students.",
                          'good_rating': unknown,
                      },
                      {
                          'value' : 'national_grant_per_st',
                          'label' : 'Total National Grant per student $',
                          'field' : 'Income_Aus_Recurrent_Per_Student',
                          'formula': "Total National Grant / number of students.",
                          'good_rating': larger,
                      },
                  
                  ],
                    
      },

      {
          'label': 'Academic Performance Analysis',
          'value': 'academicPerformance',
          'metrics':  [
                    
                      {
                          'value' : 'studentAtUniversity',
                          'label' : 'Percentage of students at university',
                          'field' : 'students_at_university',
                          'formula': "Percentage of students at university",
                          'good_rating': larger,
                      },
                    
                  
                  ],
                    
      },
      {
          'label': 'Pricing Analysis',
          'value': 'pricing_analysis',
          'metrics':  [
                    
                      {
                          'value' : 'avgPriceChart',
                          'label' : 'Average fees per student $',
                          'field' : 'Income_Fees_Charges_Parent_Per_Student',
                          'formula': "Total fee Income / number of students.",
                          'good_rating': unknown,
                      },
                    
                  
                  ],
                    
      }
  ]
