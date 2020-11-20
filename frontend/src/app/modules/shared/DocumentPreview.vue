<template> 
<div>
  <label style="font-size: 12px;"> previewing {{fileName}}</label> 
  <iframe :src="encoded_url"
            width="100%" height="1000"
            frameborder="0" scrolling="yes" id="google_iframe"
         >
  </iframe>
</div>
</template> 

<script>
export default {
  name: 'DocumentPreview',
  props: { fileName: String, url:String  }, 
  data: function(){
      return {
          encoded_url : this.encode_google_url(this.url)  
      }
  },
  computed: {
      /*
      encoded_url: function(){

            return this.encode_google_url(this.url)  
      }
      */
  },
  watch:{
      url: function(val){
            var iframe = document.getElementById('google_iframe');
            this.encoded_url = this.encode_google_url(val)
            iframe.src = this.encoded_url//this.encode_google_url(val)
      }
  },
  methods: {
      encode_google_url( value ){
            var encodedUrl = encodeURIComponent( value ); 
            var google_doc_url = 'https://docs.google.com/viewer?url=' + encodedUrl + '&embedded=true';
            return google_doc_url
      }
  },
}
</script>
