<template> 
<Download :reportName="report_name"> </Download>
</template> 

<script>
import Download from './download'

export default {
  name: 'DownloadEnrolment',
    components: {
        Download
    },
  data: function(){
      return {
          report_name : 'the Catheral School Monthly Enrolment Report'
      }
  },
}
</script>   