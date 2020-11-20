<template>
<div class="download">
    <div class="row row-equal outer-container">
        
        <div class="flex xs12 dropdown-container">
            <label >{{reportName}}</label>
            <div class="flex xs12 row" >
                <div class="flex xs5 ">
                    
                    <multiselect
                        :value="selectedFile"
                        :options="availableFiles"
                        :multiple="false"
                        :taggable="true"
                        :allow-empty="false"
                        :showLabels="false"
                        @tag="addTag"
                        @input="selectFileName"
                    ></multiselect>

                </div>

                <div class="flex xs4 ">
                    
                    <va-button class="btn" @click="download">Download</va-button>   
                </div>
                
            </div>
        </div>
    </div> 

    <div  class="flex xs12 dropdown-container">
        <DocumentPreview :fileName="selectedFile"  :url="selectedFileUrl" />
    </div>    

</div>    
</template>

<script>

import { mapState, mapActions } from "vuex";
import { loadingService } from '@/app/shared/services/loading-service'
import DocumentPreview from '../../shared/DocumentPreview'
import Multiselect from "vue-multiselect";
import { httpClient } from '@/app/shared/services/http-client'
import axios from "axios"

export default {
    name: "download",
    components:{
        Multiselect,
        DocumentPreview,
    },
    props: { 
        reportName:String  
    }, 
    data () {
        return {
            availableBlobUrls : {},
            availableFiles:[],
            selectedFile: '' , 
            selectedFileUrl: '',
        }
    },
    computed:{
        ...mapState({
            selectedEntity: state => state.user.selectedEntity,
        }), 
    },

    async created(){
        // 1, send the GET request to get all available blob urls

        const url = '/download/'+ '48004' +'/'+this.reportName
        
        await httpClient.get(url)
            .then(res => {
                const data = res.data;
                
                var list_availableFiles = []
                // print the dictionary 
                for( var document_name in data.blob_url ){
                    var document_sas_url = data.blob_url[document_name]
                    console.log(document_name+'  :  ' + document_sas_url)
                    list_availableFiles.push( document_name ) 
                }

                // 1, get all available blob urls
                this.availableBlobUrls = data.blob_url

                // 2, get the list of available files
                this.availableFiles = list_availableFiles

                // 3, default selected file
                this.selectedFile = this.availableFiles[ this.availableFiles.length-1]

                // 4, default selected file url 
                this.selectedFileUrl = this.availableBlobUrls[this.selectedFile]
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })

    },
    methods: {
        ...mapActions(
            {

            }
        ),
        selectFileName( new_file_name ){
            // 3, default selected file
            this.selectedFile = new_file_name

            // 4, default selected file url 
            this.selectedFileUrl = this.availableBlobUrls[this.selectedFile]
        },

        triggerDownload( blob_url, file_name ){
            axios({
                url: blob_url,
                method: 'GET',
                responseType: 'blob',
                headers: {'Access-Control-Allow-Origin': '*'},
            }).then((response) => {
                    var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                    var fileLink = document.createElement('a');

                    fileLink.href = fileURL;
                    fileLink.setAttribute('download', file_name);
                    document.body.appendChild(fileLink);
                    setTimeout(() => {  fileLink.click(); }, 3000);
                    //fileLink.click();
            }); 
        },

        async download(e){

            var selectedFile = this.selectedFile
            var blob_url_link = this.availableBlobUrls[selectedFile]
            this.triggerDownload(blob_url_link, selectedFile)
            
        },
        addTag(e){
            console.log('addTag()')
        }
    }
}
</script>
<style scoped>
.dropdown-container {
  display: flex;
  flex-wrap: wrap;
  border: none;
  border-radius: 0.375rem;
  background: white;
}

.dropdown {
  margin: 5px;
}

.outer-container {
  margin-left: 0 !important;
  margin-right: 0 !important;
}

.row.row-equal.outer-container + .row.row-equal.outer-container {
  margin-top: 15px;
}

.group-title {
  float: left;
  font-weight: 600;
  padding: 0 !important;
}
</style>
