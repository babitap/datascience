
from api.graphqlapi.shema_shared import *


class AcaraDashboardMetricsQuery(graphene.ObjectType):
    studentTeacherRatio    = graphene.Float()
    studentNonTeacherRatio = graphene.Float()
    recurrentIncomePerStudent = graphene.Float()

class AcaraDashboardQuery( graphene.ObjectType ): 
    basicMetrics     = graphene.Field( AcaraDashboardMetricsQuery, id = graphene.Int() ) 

    master = graphene.Field( AcaraSchoolMasterType, id = graphene.Int() ) 
    basicYearlyInfo   = graphene.List( AcaraSchoolBasicYearlyType, id = graphene.Int() )
    enrolmentsByGrade = graphene.List( AcaraSchoolGradeEnrolmentsType, id = graphene.Int() )
    finance           = graphene.List( AcaraSchoolFinanceType, id = graphene.Int() )
    location          = graphene.List( AcaraSchoolLocationType, id = graphene.Int() )
    secondaryOutcome  = graphene.List( AcaraSchoolSecondaryOutcomeType, id = graphene.Int() )
    attendance        = graphene.List( AcaraSchoolStudentAttendanceType, id = graphene.Int() )
    postSchoolDestination = graphene.List( AcaraSchoolPostSchoolDestinationType, id = graphene.Int() )
    
    def resolve_basicMetrics(self, info, id=None, **kwargs ):
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )

        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------

        # 1, get queryset of the basicYearlyInfo
        basicYearlyInfo = AcaraSchoolBasicYearly.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )
        basicYearlyInfo_df = pd.DataFrame(list(basicYearlyInfo.values()))

        # 2, get queryset of the finance
        financeInfo     = AcaraSchoolFinance.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )
        financeInfo_df = pd.DataFrame(list(financeInfo.values()))

        # 3, merge datasets 
        df = basicYearlyInfo_df.merge(financeInfo_df, on=['acara_id', 'calendar_year'], how='left')
        df = df.sort_values(by='calendar_year', ascending=False)

        # 4, calculate studentTeacherRatio and studentNonTeacherRatio
        df['student_teacher_ratio'] = df['full_time_equivalent_enrolments'] / df['full_time_equivalent_teaching_staff']
        df['student_non_teacher_ratio'] = df['full_time_equivalent_enrolments'] / df['full_time_equivalent_non_teaching_staff']
        
        student_teacher_ratio     = df[~df['student_teacher_ratio'].isnull()].iloc[0]['student_teacher_ratio']
        student_non_teacher_ratio = df[~df['student_non_teacher_ratio'].isnull()].iloc[0]['student_non_teacher_ratio']

        # 5, calculate reCurrentIncomePerStudent 
        df['recurrent_income_per_student'] = df['income_total_net_recurrent_per_student']
        recurrent_income_per_student = df[~df['recurrent_income_per_student'].isnull()].iloc[0]['recurrent_income_per_student']

        # 6, return latest results

        return AcaraDashboardMetricsQuery(  studentTeacherRatio = student_teacher_ratio , 
                                            studentNonTeacherRatio = student_non_teacher_ratio , 
                                            recurrentIncomePerStudent = recurrent_income_per_student )

    def resolve_master(self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------

        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolMaster.objects.using(DEFAULT_ACARA_DATABASE).get(  q_filter.get_filter()  )
    
    def resolve_basicYearlyInfo( self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------        
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolBasicYearly.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )

    def resolve_enrolmentsByGrade( self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------        
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolGradeEnrolments.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )

    def resolve_finance( self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------        
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolFinance.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )

    def resolve_location( self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------        
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolLocation.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )

    def resolve_secondaryOutcome( self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------
                
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolSecondaryOutcome.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )

    def resolve_attendance( self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------        
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolStudentAttendance.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )

    def resolve_postSchoolDestination( self, info, id=None, **kwargs): 
        # ------------------------------------------------------------------------------
        # permission Check                                                   -- Fred 
        # need a logic to check whether user (info.context.user) has access to school (id) 
        if not checkUserNameHasPermissionAcaraSchool( user_name=info.context.user, acara_id = id ):
            raise PermissionError("No permission") 
        # ------------------------------------------------------------------------------        
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=id) )
        return AcaraSchoolPostSchoolDestination.objects.using(DEFAULT_ACARA_DATABASE).filter(  q_filter.get_filter()  )