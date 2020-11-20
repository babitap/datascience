
global_acara_benchmark_fields_structure = \
[
    {
        'label': 'Enrolment',
        'value': 'enrolment',
        'metrics': [
                    
                    {
                        'value' : 'totalEnrolments_allYearLevels',
                        'label' : 'Total Enrolments - All Year Levels',
                        'model' : 'AcaraSchoolGradeEnrolments',
                        'field' : 'enrolmentsAllYearLevels',
                        'sub_metrics': [
                            {
                                'field': 'twoYearsBeforeYear1Enrolments',
                                'value': 'twoYearsBeforeYear1Enrolments',
                                'label': 'Two Years Before Year 1 Enrolments',
                            },
                            {
                                'field': 'oneYearBeforeYear1Enrolments',
                                'value': 'oneYearBeforeYear1Enrolments',
                                'label': 'One Year Before Year 1 Enrolments',
                            },
                            {
                                'field': 'year1Enrolments',
                                'value': 'year1Enrolments',
                                'label': 'Year 1 Enrolments',
                            },      
                            {
                                'field': 'year2Enrolments',
                                'value': 'year2Enrolments',
                                'label': 'Year 2 Enrolments',
                            },  
                            {
                                'field': 'year3Enrolments',
                                'value': 'year3Enrolments',
                                'label': 'Year 3 Enrolments',
                            },    
                            {
                                'field': 'year4Enrolments',
                                'value': 'year4Enrolments',
                                'label': 'Year 4 Enrolments',
                            },    
                            {
                                'field': 'year5Enrolments',
                                'value': 'year5Enrolments',
                                'label': 'Year 5 Enrolments',
                            },    
                            {
                                'field': 'year6Enrolments',
                                'value': 'year6Enrolments',
                                'label': 'Year 6 Enrolments',
                            },    
                            {
                                'field': 'year7Enrolments',
                                'value': 'year7Enrolments',
                                'label': 'Year 7 Enrolments',
                            },    
                            {
                                'field': 'year8Enrolments',
                                'value': 'year8Enrolments',
                                'label': 'Year 8 Enrolments',
                            },    
                            {
                                'field': 'year9Enrolments',
                                'value': 'year9Enrolments',
                                'label': 'Year 9 Enrolments',
                            },    
                            {
                                'field': 'year10Enrolments',
                                'value': 'year10Enrolments',
                                'label': 'Year 10 Enrolments',
                            },    
                            {
                                'field': 'year11Enrolments',
                                'value': 'year11Enrolments',
                                'label': 'Year 11 Enrolments',
                            },    
                            {
                                'field': 'year12Enrolments',
                                'value': 'year12Enrolments',
                                'label': 'Year 12 Enrolments',
                            },    
                            {
                                'field': 'primaryUngradedEnrolments',
                                'value': 'primaryUngradedEnrolments',
                                'label': 'Primary Ungraded Enrolments',
                            },    
                            {
                                'field': 'secondaryUngradedEnrolments',
                                'value': 'secondaryUngradedEnrolments',
                                'label': 'Secondary Ungraded Enrolments',
                            } 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                        ], 
                    },
                    {
                        'value' : 'totalEnrolments_bothGenders',
                        'label' : 'Total Enrolments - Both Genders',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'enrolmentsAllGenders',
                        'sub_metrics': [
                            {
                                'field': 'boysEnrolments',
                                'value': 'boysEnrolments',
                                'label': 'Boys Enrolments',
                            },
                            {
                                'field': 'girlsEnrolments',
                                'value': 'girlsEnrolments',
                                'label': 'Girls Enrolments',
                            }                                                                                                                                                                                                                                                                                                                                                                                                                                                             
                        ], 
                    }, 
                    {
                        'label': 'Total Enrolment (FTE) ',
                        'field': 'fullTimeEquivalentEnrolments',
                        'model': 'AcaraSchoolBasicYearly',
                        'value': 'fullTimeEquivalentEnrolments',
                    },

                    {
                        'label': 'Indigenous Enrolments Percentage',
                        'field': 'indigenousEnrolmentsPercent',
                        'model': 'AcaraSchoolBasicYearly',
                        'value': 'indigenousEnrolmentsPercent',
                    },

                    {
                        'label': 'Non-English Background Percentage',
                        'field': 'languageBackgroundOtherThanEnglishPercent',
                        'model': 'AcaraSchoolBasicYearly',
                        'value': 'languageBackgroundOtherThanEnglishPercent',
                    },
                ],
    },
    {
        'label': 'Staff',
        'value': 'staff',
        'metrics': [
                    {
                        'label' : 'Total Staff (People)',
                        'value' : 'total_staff_people',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'totalStaffPeople',
                        'sub_metrics': [
                                        {
                                            'field': 'teachingStaff',
                                            'value': 'teachingStaff',
                                            'label': 'Teaching Staff (People)',
                                        },
                                        {
                                            'field': 'nonTeachingStaff',
                                            'value': 'nonTeachingStaff',
                                            'label': 'Non-Teaching Staff (People)',
                                        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                        ]
                    },
                    {
                        'label' : 'Total Staff (FTE)',
                        'value' : 'total_staff_fte',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'totalStaffFTE',
                        'sub_metrics': [
                                        {
                                            'field': 'fullTimeEquivalentTeachingStaff',
                                            'value': 'fullTimeEquivalentTeachingStaff',
                                            'label': 'Teaching Staff (FTE)',
                                        },
                                        {
                                            'field': 'fullTimeEquivalentNonTeachingStaff',
                                            'value': 'fullTimeEquivalentNonTeachingStaff',
                                            'label': 'Non-Teaching Staff (FTE)',
                                        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                        ]
                    },
                    {
                        'label' : 'Enrolments per Staff',
                        'value' : 'enrolmentsPerStaff',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'enrolmentsPerStaff'
                    },
                    {
                        'label' : 'Enrolments per Teacher',
                        'value' : 'enrolmentsPerTeacher',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'enrolmentsPerTeacher'
                    },
                    {
                        'label' : 'Enrolments per Non-Teacher',
                        'value' : 'enrolmentsPerNonTeacher',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'enrolmentsPerNonTeacher'
                    },
                    {
                        'label' : 'Enrolments per Staff(FTE)',
                        'value' : 'enrolmentsPerStaffFullTimeEquivalent',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'enrolmentsPerStaffFullTimeEquivalent'
                    },
                    {
                        'label' : 'Enrolments per Teacher(FTE)',
                        'value' : 'enrolmentsPerTeacherFullTimeEquivalent',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'enrolmentsPerTeacherFullTimeEquivalent'
                    },
                    {
                        'label' : 'Enrolments per Non-Teacher(FTE)',
                        'value' : 'enrolmentsPerNonTeacherFullTimeEquivalent',
                        'model' : 'AcaraSchoolBasicYearly',
                        'field' : 'enrolmentsPerNonTeacherFullTimeEquivalent'
                    },
        ],
    },

    {
        'label': 'Finance',
        'value': 'finance',
        'metrics': [
                    {
                        'label' : 'Total Gross Income',
                        'value' : 'incomeTotalGross',
                        'model' : 'AcaraSchoolFinance',
                        'field' : 'incomeTotalGross',
                        'sub_metrics': [
                                        {
                                            'field': 'incomeAusRecurrent',
                                            'value': 'incomeAusRecurrent',
                                            'label': 'Recurrent Income (Commonwealth)',
                                        },
                                        {
                                            'field': 'incomeStateRecurrent',
                                            'value': 'incomeStateRecurrent',
                                            'label': 'Recurrent Income (State)',
                                        } ,           
                                        {
                                            'field': 'incomeFeesChargesParent',
                                            'value': 'incomeFeesChargesParent',
                                            'label': 'Recurrent Income (Fee Charges)',
                                        },              
                                        {
                                            'field': 'incomeOtherPrivate',
                                            'value': 'incomeOtherPrivate',
                                            'label': 'Other Private Income',
                                        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                        ]
                    },
                    {
                        'label' : 'Total Gross Income per Student',
                        'value' : 'incomeTotalGrossPerStudent',
                        'model' : 'AcaraSchoolFinance',
                        'field' : 'incomeTotalGrossPerStudent',
                        'sub_metrics': [
                                        {
                                            'field': 'incomeAusRecurrentPerStudent',
                                            'value': 'incomeAusRecurrentPerStudent',
                                            'label': 'Recurrent Income (Commonwealth) per Enrolment',
                                        },
                                        {
                                            'field': 'incomeStateRecurrentPerStudent',
                                            'value': 'incomeStateRecurrentPerStudent',
                                            'label': 'Recurrent Income (State) per Enrolment',
                                        } ,           
                                        {
                                            'field': 'incomeFeesChargesParentPerStudent',
                                            'value': 'incomeFeesChargesParentPerStudent',
                                            'label': 'Recurrent Income (Fee Charges) per Enrolment',
                                        },              
                                        {
                                            'field': 'incomeOtherPrivatePerStudent',
                                            'value': 'incomeOtherPrivatePerStudent',
                                            'label': 'Other Private Income per Enrolment',
                                        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                        ]
                    },
                    {
                        'label' : 'Total Net Recurrent Income',
                        'value' : 'incomeTotalNetRecurrent',
                        'model' : 'AcaraSchoolFinance',
                        'field' : 'incomeTotalNetRecurrent',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                    },
                    {
                        'label' : 'Total Net Recurrent Income per Student',
                        'value' : 'incomeTotalNetRecurrentPerStudent',
                        'model' : 'AcaraSchoolFinance',
                        'field' : 'incomeTotalNetRecurrentPerStudent',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                    },
                    {
                        'label' : 'Total Gross Deduction',
                        'value' : 'deductionsTotal',
                        'model' : 'AcaraSchoolFinance',
                        'field' : 'deductionsTotal',
                        'sub_metrics': [
                                        {
                                            'field': 'deductionsCurrCapitalProj',
                                            'value': 'deductionsCurrCapitalProj',
                                            'label': 'Deduction Current Capital',
                                        },
                                        {
                                            'field': 'deductionsFutCapitalProj',
                                            'value': 'deductionsFutCapitalProj',
                                            'label': 'Deduction Future Capital',
                                        } ,           
                                        {
                                            'field': 'deductionsDebtService',
                                            'value': 'deductionsDebtService',
                                            'label': 'Deduction Debt Service',
                                        },                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                        ]
                    },
                    {
                        'label' : 'Total Capital Expense',
                        'value' : 'capitalExpendTotal',
                        'model' : 'AcaraSchoolFinance',
                        'field' : 'capitalExpendTotal',
                        'sub_metrics': [
                                        {
                                            'field': 'capitalExpendAus',
                                            'value': 'capitalExpendAus',
                                            'label': 'Capital Expense (Commonwealth)',
                                        },
                                        {
                                            'field': 'capitalExpendState',
                                            'value': 'capitalExpendState',
                                            'label': 'Capital Expense (State)',
                                        } ,           
                                        {
                                            'field': 'capitalExpendNewSchoolLoans',
                                            'value': 'capitalExpendNewSchoolLoans',
                                            'label': 'Capital Expense (New School Loans)',
                                        },      
                                        {
                                            'field': 'capitalExpendCurrCapitalProj',
                                            'value': 'capitalExpendCurrCapitalProj',
                                            'label': 'Capital Expense Current Capital Proj.',
                                        },       
                                        {
                                            'field': 'capitalExpendOtherPrivate',
                                            'value': 'capitalExpendOtherPrivate',
                                            'label': 'Capital Expense Other Private',
                                        },       
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                        ]
                    },
        ]
    }
]
