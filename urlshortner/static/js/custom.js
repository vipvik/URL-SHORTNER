$(document).ready(function(){
	var resp;
	$('form').on('submit', function(event){
		var long_url = {
		   longurl : $("#longurl").val(),	
		};
		$.ajax({
			data : long_url,
			type : 'POST',
			url : "/short_url",
			
            success : function(response){
                if(response.error){
                	$("#errorAlert").text(response.error).show();
                	$("#successAlert").hide();
                	$("#copy-code").hide();
                }else{
                	$("#successAlert").text(response.short_url).show();
                	$("#copy-code").show();
                	$("#errorAlert").hide();
                	resp = response.short_url;
                }
            },
            error : function(error){
            	    console.log("vipl1");
                	$("#errorAlert").html("Server Error !");
                	$("#successAlert").hide();  
                	$("#copy-code").hide();         	
            }
		});
		event.preventDefault();
	});

    function copy_to_clipbord(element){
    	   var $temp = $("<input>");
           $("body").append($temp);
           $temp.val(element).select();
           document.execCommand("copy");
           $temp.remove();
    }

	$("#copy-code").click(function(){
		copy_to_clipbord(resp);
	});
});
