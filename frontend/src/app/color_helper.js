

const findex_colors = [     '#d43d27', // 0 findex orange
                            '#516cb3', // 1 findex purple
                            '#0eacbd', // 2 findex blue
                            '#8dc63f', // 3 findex green 
                            '#757679', // 4
                            '#bfbfbf', // 5
                            '#68c9d0', // 6
                            '#489db1', // 7
                            '#99c4c7', // 8
                            '#6ac288', // 9
                            '#5dabdf', //10
                            '#0091d0', //11
                            '#6196a6', //12
                        ]

function getFindexColors (number) {
    var existing_color_len = findex_colors.length
    var return_color_list = []
    for( var i=0; i<number; i++ ){
        return_color_list.push( findex_colors[ i % existing_color_len ] )
    }
    return return_color_list
}

function getBinaryColors(){
    return {'FOCUSED': findex_colors[0], 'NOT_FOCUSED': findex_colors[5] }
}

export {getFindexColors, getBinaryColors}