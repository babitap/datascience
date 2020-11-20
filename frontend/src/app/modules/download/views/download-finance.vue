<template> 
<Download :reportName="report_name"> </Download>
</template> 

<script>
import Download from './download'

export default {
  name: 'DownloadFinance',
    components: {
        Download
    },
  data: function(){
      return {
          report_name : 'the Catheral School Monthly Finance Report'
      }
  },
}
</script>