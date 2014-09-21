/*
 * table.js
 * Copyright (C) 2014 Sébastien Diemer <sebastien.diemer@mines-paristech.fr>
 *
 * Distributed under terms of the MIT license.
 *
 */

SERVER_URL = 'http://localhost:5000/dataiku'

function ask_column(column) {
    $.ajax({
        cache: false,
        url: SERVER_URL+'/columns/'+column,
        type: "GET",
        contentType: "application/json"
    }).done(function(json) {
        $('#thetable tr').not(':first').not(':last').remove();
        var html = '';
        for(var i = 0; i < json['column'].length; i++)
                    html += '<tr><td>' + json['column'][i]['value'] + 
                            '</td><td>' + json['column'][i]['count'] +
                            '</td><td>' + json['column'][i]['average age'] + '</td></tr>';
        $('#thetable tr').first().after(html);
        if (json['ignored'] == 0) {
            $('#ignored').html('');
        } else {
            $('#ignored').html(json['ignored'] + ' values clipped');
        }
    });
}

$(document).ajaxError(function( event, request, settings ) {
      $( "#content" ).css("color", "red");
      $( "#content" ).html("Error server unavailable");
});

$(document).ready(
    function get_columns() {
        $.ajax({
            cache: false,
            url: SERVER_URL+'/columns',
            type: "GET",
            contentType: "application/json"
        }).done(function(json) {
            var $inputColumns = $("select[name='inputColumns']")
            var columns = json['columns']
            $(columns).each(function(i, v) { 
                    $inputColumns.append($("<option>", { value: v, html: v }));
            });
        });
    });
