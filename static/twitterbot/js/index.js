function show(text)
{
	var twitterHandle =  document.getElementById('twitter_handle').value;
	document.getElementById('result').innerHTML = twitterHandle;
}

function ajaxCall()
{
	$.ajax({
        type: 'GET',
        url:  'twitterbot/ajax',


        success: function(data, status){
        	alert(data);  
        },
        error:   function(){alert('ERROR!'); }
       	});
}