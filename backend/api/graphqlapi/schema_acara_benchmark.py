from api.graphqlapi.shema_shared import *
from api.graphqlapi.config.benchmark_structure import global_acara_benchmark_fields_structure

from graphene import Int , String
import geopy.distance

class BenchmarkSubMetricType(graphene.ObjectType):
    label = graphene.String()
    value = graphene.String()
    field = graphene.String()

class BenchmarkMetricType(graphene.ObjectType):
    label = graphene.String()
    value = graphene.String()
    model = graphene.String()
    field = graphene.String()
    subMetrics = graphene.List( BenchmarkSubMetricType )


class BenchmarkDatasetType(graphene.ObjectType):
    label = graphene.String()
    value = graphene.String()
    metrics = graphene.List( BenchmarkMetricType )
    
#--------------------------------------------------------------------#
class BenchmarkBasicLineDataType(graphene.ObjectType):
    calendarYear = graphene.Int()
    value       = graphene.Float()    

class BenchmarkPositionChart(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.Float()
    focused = graphene.Boolean()

class BenchmarkTrendChart(graphene.ObjectType):
    id     = graphene.Int()
    focused = graphene.Boolean()
    lineData = graphene.List(BenchmarkBasicLineDataType  )

class BenchmarkYearlyChangeChart(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.Float()
    focused = graphene.Boolean()

class BenchmarkMultiYearsChangeChart(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.Float()
    focused = graphene.Boolean()

class BenchmarkMarketShareChart(graphene.ObjectType):
    calendarYear = graphene.Int()
    value = graphene.Float()
    
class BenchmarkDistributionPositionChart(graphene.ObjectType):
    id = graphene.Int()
    submetric = graphene.String()
    value = graphene.Float()
    focused = graphene.Boolean()

class BenchmarkDistributionTrendChart(graphene.ObjectType):
    calendarYear = graphene.Int()
    submetric = graphene.String()
    value = graphene.Float()

class BenchmarkChartsDataType(graphene.ObjectType):
    position = graphene.List(BenchmarkPositionChart)
    trend    = graphene.List(BenchmarkTrendChart)
    yearlyChange = graphene.List(BenchmarkYearlyChangeChart)
    multiYearsChange = graphene.List(BenchmarkMultiYearsChangeChart)
    marketShare = graphene.List(BenchmarkMarketShareChart)
    distributionPosition = graphene.List(BenchmarkDistributionPositionChart)
    distributionTrend   = graphene.List(BenchmarkDistributionTrendChart)

class AcaraBenchmarkFilterOptionType(graphene.ObjectType):
    value = graphene.String()
    label = graphene.String()

class AcaraSchoolId(graphene.ObjectType):
    id = graphene.Int()


class AcaraBenchmarkFilterDefaultValuesType(graphene.ObjectType):
    schoolSectorDefaultOption = graphene.List( AcaraBenchmarkFilterOptionType )
    schoolTypeDefaultOption   = graphene.List( AcaraBenchmarkFilterOptionType )
    schoolGenderDefaultOption = graphene.List( AcaraBenchmarkFilterOptionType )
    stateDefaultOption        = graphene.List( AcaraBenchmarkFilterOptionType )
    geolocationDefaultOption  = graphene.List( AcaraBenchmarkFilterOptionType )
    enrolmentRangeStartValue  = graphene.Int()
    enrolmentRangeEndValue    = graphene.Int()
    distanceKmValue           = graphene.Int() 
    
class AcaraBenchmarkSchoolFilterOptionsType(graphene.ObjectType):
    schoolSectorOptions = graphene.List( AcaraBenchmarkFilterOptionType )
    schoolTypeOptions   = graphene.List( AcaraBenchmarkFilterOptionType )
    schoolGenderOptions = graphene.List( AcaraBenchmarkFilterOptionType )
    stateOptions        = graphene.List( AcaraBenchmarkFilterOptionType )
    geolocationOptions  = graphene.List( AcaraBenchmarkFilterOptionType )
    genderOptions       = graphene.List( AcaraBenchmarkFilterOptionType )

    

    def get_unique_values( self, model, field ):
        data_model = get_data_model_from_name_string( model )
        available_values = data_model.objects.using(DEFAULT_ACARA_DATABASE).values(field).distinct()
        available_values = list(available_values) if available_values else []

        return_list = []
        for value in available_values:
            #if value[field] == None: 
            #    value[field] = "Not Sure"
            return_list.append( AcaraBenchmarkFilterOptionType( value=value[field], label=value[field] ) )
        return return_list

    def resolve_schoolSectorOptions(self, info, **kwargs):
        return self.get_unique_values( 'AcaraSchoolMaster', 'school_sector' )

    def resolve_schoolTypeOptions(self, info, **kwargs):
        return self.get_unique_values( 'AcaraSchoolMaster', 'school_type' )

    def resolve_geolocationOptions(self, info, **kwargs):
        return self.get_unique_values( 'AcaraSchoolMaster', 'geolocation' )

    def resolve_stateOptions(self, info, **kwargs):
        return self.get_unique_values( 'AcaraSchoolMaster', 'state' )       

    def resolve_schoolGenderOptions(self, info, **kwargs):
        return_list = []
        for gender in ['Only Boys', 'Only Girls', 'Both Genders']:
            return_list.append( AcaraBenchmarkFilterOptionType( value=gender, label=gender )  )
        return return_list



class AcaraBenchmarkQuery(graphene.ObjectType):
    filterOptions  = graphene.Field( AcaraBenchmarkSchoolFilterOptionsType )
    filterDefaultValues = graphene.Field( AcaraBenchmarkFilterDefaultValuesType , id = graphene.Int() )
    comparableSchools = graphene.List( AcaraSchoolId, id = graphene.Int(), 
                                            schoolSector=graphene.List(String), 
                                            schoolType=graphene.List(String), 
                                            schoolGender=graphene.List(String), 
                                            schoolState=graphene.List(String), 
                                            schoolGeolocation=graphene.List(String), 
                                            enrolmentStartValue=graphene.Int(), 
                                            enrolmentEndValue = graphene.Int(), 
                                            distanceKm = graphene.Int(),
                                             )

    datasets = graphene.List( BenchmarkDatasetType )

    charts   = graphene.Field( BenchmarkChartsDataType, 
                                id = graphene.Int(),                                                    # focusing school 
                                comparable_ids = graphene.List(graphene.Int, description="ID List"),    # comparable schools
                                model  = graphene.String(),                                             # data model 
                                metric_field = graphene.String(),                                       # metric field 
                                submetrics_fields = graphene.List(graphene.String, description="Submetric List"  ),    # submetric field 
                                 ) 

    def resolve_comparableSchools( self, info, id, schoolSector=[], schoolType=[],schoolGender=[], schoolState=[], schoolGeolocation=[],
                                        enrolmentStartValue=0,enrolmentEndValue=0,distanceKm=0,**kwargs):
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------

        # firstly, search in school master
        q_filter = Q_list()
        q_filter.add_Q( ~Q( acara_id=id ) )
        if schoolSector !=None and len(schoolSector)>0:
            q_filter.add_Q(  Q( school_sector__in=schoolSector ) )
        if schoolType!=None and len(schoolType)>0:
            q_filter.add_Q(  Q( school_type__in=schoolType ) )
        if schoolState!=None and len(schoolState)>0:
            q_filter.add_Q(  Q( state__in=schoolState ) )
        if schoolGeolocation!=None and len(schoolGeolocation)>0:
            q_filter.add_Q(  Q( geolocation__in=schoolGeolocation ) )

        school_masters = AcaraSchoolMaster.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )
        school_masters_df = pd.DataFrame( list(school_masters.values()) )

        print('After check school master, Potential comparable schools: ')
        print(school_masters_df)

        potential_comparable_schools_list = []
        if len(school_masters_df) == 0 :
            return [] 
        else: 
            potential_comparable_schools_list = school_masters_df['acara_id'].tolist()

            # secondly, match in geolocation if distanceKm is given (>0)
            if distanceKm > 0 or distanceKm==None :
                q_filter = Q_list()
                q_filter.add_Q(  Q( acara_id__in=potential_comparable_schools_list ) ) 
                q_filter.add_Q(  Q( acara_id=id ) ) 

                school_locations = AcaraSchoolLocation.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter_with_or_logic()  )

                school_locations_df = pd.DataFrame( list(school_locations.values()) )

                our_school_location = school_locations_df[school_locations_df['acara_id']==id]
                potential_comparable_schools_location = school_locations_df[~(school_locations_df['acara_id']==id)]

                
                if len(our_school_location)==0 or len(potential_comparable_schools_location)==0:
                    return []
                else:  
                    potential_comparable_schools_list = []

                    centralPoint = ( float(our_school_location.iloc[0]['latitude']), float(our_school_location.iloc[0]['longitude']) )
                    for index, row in potential_comparable_schools_location.iterrows(): 
                        coords_1 = (float(row['latitude']), float(row['longitude']))
                        if geopy.distance.vincenty(coords_1, centralPoint).km <= distanceKm:
                            potential_comparable_schools_list.append( row['acara_id'] )
                print('After check geolocation, Potential comparable schools: ')
                print(len(potential_comparable_schools_list))

            # thirdly, match in yearlybasic
            q_filter = Q_list()
            q_filter.add_Q(  Q( acara_id__in=potential_comparable_schools_list ) )

            q_filter.add_Q(  Q( calendar_year__gte=2016 ) ) 
            if schoolGender != None: 
                if schoolGender == 'Only Boys':
                    q_filter.add_Q(  Q( boys_enrolments__gte=0 ) )
                    q_filter.add_Q(  ~Q( girls_enrolments__gte=0 ) )
                elif schoolGender == 'Only Girls':
                    q_filter.add_Q(  ~Q( boys_enrolments__gte=0 ) ) 
                    q_filter.add_Q(  Q( girls_enrolments__gte=0 ) ) 
                elif schoolGender == 'Both Genders':
                    q_filter.add_Q(  Q( boys_enrolments__gte=0 ) ) 
                    q_filter.add_Q(  Q( girls_enrolments__gte=0 ) ) 
            
            if (enrolmentStartValue != None ) and enrolmentStartValue > 0: 
                q_filter.add_Q(  Q( total_enrolments__gte= enrolmentStartValue ) )

            if (enrolmentEndValue != None ) and enrolmentEndValue > 0:     
                q_filter.add_Q(  Q( total_enrolments__lte= enrolmentEndValue ) )
                
            final_list = AcaraSchoolBasicYearly.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  ).values('acara_id').distinct()
            final_list = list(final_list) if final_list else []

            school_basic_yearly = AcaraSchoolBasicYearly.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )
            school_basic_yearly = pd.DataFrame( list(school_basic_yearly.values()) )
            
            #print('After check yearly basic, school_basic_yearly')
            #print((school_basic_yearly))
            final_list = school_basic_yearly['acara_id'].unique()

            final_return = []
            for school_id in final_list:
                final_return.append( AcaraSchoolId(id=school_id) )

            return final_return 


    def resolve_filterDefaultValues(self, info,  id=None, **kwargs):
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------

        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )

        school_masters = AcaraSchoolMaster.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  ).values()
        school_masters = list(school_masters) if school_masters else []

        query_set = AcaraSchoolBasicYearly.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )
        data_df = pd.DataFrame( list( query_set.values('acara_id', 'calendar_year', 'boys_enrolments', 'girls_enrolments', 'total_enrolments') ) )
        latest_year = data_df['calendar_year'].max()
        latest_df = data_df[data_df['calendar_year']==latest_year]

        if len(school_masters) == 0 or len(latest_df) == 0: 
            return null 
        else :
            school_master = school_masters[0]
            school_sector = school_master['school_sector']
            school_type   = school_master['school_type']
            school_state  = school_master['state']
            school_geolocation = school_master['geolocation']

            boys_num  = latest_df.iloc[0]['boys_enrolments']
            girls_num = latest_df.iloc[0]['girls_enrolments']
            gender_defaut_value = ''
            if( boys_num>0 and not ( girls_num > 0 ) ):
                gender_defaut_value = 'Only Boys'
            elif( girls_num>0 and not ( boys_num > 0 ) ):
                gender_defaut_value = 'Only Girls'
            elif( boys_num > 0 and girls_num>0 ):
                gender_defaut_value = 'Both Genders'
            else: 
                gender_defaut_value = 'Not Sure'

            total_enrolments = latest_df.iloc[0]['total_enrolments']
            range_start_value = (total_enrolments - 300) if (total_enrolments - 500)>0 else 1
            range_end_value   = total_enrolments + 300 

            return AcaraBenchmarkFilterDefaultValuesType(
                schoolSectorDefaultOption =[ AcaraBenchmarkFilterOptionType( value=school_sector , label=school_sector)], 
                schoolTypeDefaultOption   =[ AcaraBenchmarkFilterOptionType( value=school_type , label=school_type)],  
                stateDefaultOption        =[ AcaraBenchmarkFilterOptionType( value=school_state , label=school_state)],   
                geolocationDefaultOption  =[ AcaraBenchmarkFilterOptionType( value=school_geolocation , label=school_geolocation)] , 
                schoolGenderDefaultOption =[ AcaraBenchmarkFilterOptionType( value=gender_defaut_value , label=gender_defaut_value)] , 
                enrolmentRangeStartValue  = range_start_value,
                enrolmentRangeEndValue    = range_end_value,
                distanceKmValue           = 0,
            )

    def _change_dataframe_column_name_to_graphql_format( self, df ):
        rename_dict = {}
        for column_name in df.columns:
            new_column_name = ''
            splited_terms = column_name.split('_')
            for splited_term in splited_terms:
                if new_column_name == '':
                    new_column_name = splited_term.lower()
                else: 
                    splited_term = splited_term[0:1].upper() + splited_term[1:].lower()
                    new_column_name = new_column_name + splited_term
            rename_dict[column_name] = new_column_name
        #print(rename_dict)
        return df.rename(columns = rename_dict)

    def _enable_BenchmarkPositionChart(self, df, id_field, year_field, sum_field, focused_school_label):
        return_list = []
        # get the latest position
        latest_year = df[year_field].max()
        latest_df = df[df[year_field]==latest_year]
        for ind, row in latest_df.iterrows():
            acara_id = row[id_field]
            total_value = row[sum_field]
            focused = row[focused_school_label]
            return_list.append( BenchmarkPositionChart( id=acara_id, value=total_value, focused = focused ) )
            
        return return_list 

    def _enable_BenchmarkTrendChart(self, df, id_field, year_field, sum_field, focused_school_label):
        return_list = []
        # get unique ids and focused column 
        ids_df = df[[id_field, focused_school_label]].drop_duplicates()

        # loop through ids and generate their list 
        for ind1, schoo_row in ids_df.iterrows():
            school_id = schoo_row[id_field]
            focused = schoo_row[focused_school_label]
            school_df = df[ df[id_field] == school_id ].sort_values(by=year_field, ascending=True)
            line_data_list = []
            for ind2, row in school_df.iterrows():
                calendar_year = row[year_field]
                total_value = row['sum']
                line_data_list.append(BenchmarkBasicLineDataType( calendarYear=calendar_year,value=total_value  )  )
                
            return_list.append( BenchmarkTrendChart( id=school_id, focused = focused, lineData= line_data_list) )
                
        return return_list 

    def resolve_filterOptions(self, info, **kwargs):
        return AcaraBenchmarkSchoolFilterOptionsType()

    def resolve_charts( self, info, id=48004, comparable_ids=[46483,46621,46746,47485,47577,47913], 
                        model='AcaraSchoolBasicYearly', metric_field='totalEnrolments_all_gender', 
                        submetrics_fields=[ 'boysEnrolments','girlsEnrolments'] ,**kwargs ):

        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------

        # get filters on acara_id 
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        for comparable_id in comparable_ids:
            q_filter.add_Q( Q(acara_id=comparable_id) )

        # get the data from data model following the aboeve filters 
        data_model = get_data_model_from_name_string( model )
        query_set = data_model.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter_with_or_logic()  )
        data_df = pd.DataFrame( list( query_set.values() ) )
        data_df = self._change_dataframe_column_name_to_graphql_format(data_df)

        # add sum column 
        if ( len(submetrics_fields) == 0 ) & ( len(metric_field)>0 ) : 
            print("use metric field instead of submetrics")
            data_df['sum'] = data_df[metric_field].fillna(0)
        else: 
            data_df['sum'] = 0
            for field in submetrics_fields:
                data_df['sum'] = data_df[field].fillna(0) + data_df['sum']

        # add random id (rid) column in order to hide acaraId
        latest_year = data_df['calendarYear'].max()
        latest_df = data_df[data_df['calendarYear']==latest_year]
        ordered_acara_id_df = latest_df.sort_values(by='sum', ascending=False)
        ordered_acara_id_df['rid'] = np.arange(len(ordered_acara_id_df)) + 1
        ordered_acara_id_df['focused_school_label'] = ordered_acara_id_df['acaraId'].apply(lambda x: True if x==id else False )
        ordered_acara_id_df = ordered_acara_id_df[['acaraId', 'rid', 'focused_school_label']]
        data_with_rid_df = data_df.merge( ordered_acara_id_df, on="acaraId", how="left" ) 

        position = self._enable_BenchmarkPositionChart( data_with_rid_df, 'rid', 'calendarYear', 'sum', 'focused_school_label' )
        trend    = self._enable_BenchmarkTrendChart( data_with_rid_df, 'rid', 'calendarYear', 'sum' , 'focused_school_label')

        return BenchmarkChartsDataType( position = position , trend=trend )


    def resolve_datasets(self, info, **kwargs): 
        dataset_list = []
        #dataset_is_selected = True 
        for dataset in global_acara_benchmark_fields_structure: 
            
            metric_list = []
            if 'metrics' in dataset: 
                #metric_is_selected = True 
                for metric in dataset['metrics']: 
                    
                    sub_metric_list = []
                    #submetric_is_selected = True 
                    if 'sub_metrics' in metric: 
                        
                        for sub_metric in metric['sub_metrics']: 
                            sub_metric_dict = BenchmarkSubMetricType(   #selected = submetric_is_selected,
                                                                        label = sub_metric['label'], 
                                                                        value = sub_metric['value'],
                                                                        field = sub_metric['field'] )
                            sub_metric_list.append( sub_metric_dict )
                    
                    metric_dict = BenchmarkMetricType(  #selected = metric_is_selected, 
                                                        label = metric['label'],
                                                        value = metric['value'], 
                                                        model = metric['model'],
                                                        field = metric['field'],
                                                        subMetrics = sub_metric_list )
                    metric_list.append( metric_dict )
                    #metric_is_selected = False
            
            dataset_dict = BenchmarkDatasetType(    #selected = dataset_is_selected,
                                                    label = dataset['label'], 
                                                    value = dataset['value'],
                                                    metrics =  metric_list , 
                                                    )
            dataset_list.append( dataset_dict )
            #dataset_is_selected = False
        return dataset_list

