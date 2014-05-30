$(document).ready(function(){
    $( ".datePicker" ).datepicker({"dateFormat":"yy/mm/dd"});
    $(".num").numeric();
    
    $(".cboxClass").click(function(){
       isCompleteOK();            
    });

    $( "#so-div" ).dialog({
        modal: true,
        autoOpen: false,
        width: 400,
        height: 200 ,
        buttons: {
        "Submit" : function() { 
            var so = $("#so").val();
            if(!so){
                alert("Please input the SO number!");
                return;
            }else{
                var params = {
                    id : $(".cboxClass:checked").val(),
                    status : 1,                            
                    so : so,
                    t : $.now()
                };
                $.getJSON('/ordering/ajaxChangeStatus',params,function(r){
                    if(r.flag != 0){
                        alert(r.msg);
                    }else{
                        alert('Update the record successfully!');
                        window.location.reload(true);
                    }
                });
            }
    
        },
        "Cancel" : function() { $( this ).dialog( "close" ); }
        }
    });
    
    
    $( "#ship-div" ).dialog({
        modal: true,
        autoOpen: false,
        width: 600,
        height: 200 ,
        buttons: {
        "Submit" : function() { 
            var params = {
                id : $(".cboxClass:checked").val(),
                status : 2,
                courier : $("#courier").val(),
                trackingNumber : $("#trackingNumber").val(),
                t : $.now()
            };
            $.getJSON('/ordering/ajaxChangeStatus',params,function(r){
                if(r.flag != 0){
                    alert(r.msg);
                }else{
                    alert('Update the record successfully!');
                    window.location.reload(true);
                }
            });
    
        },
        "Cancel" : function() { $( this ).dialog( "close" ); }
        }
    });
    
});

function isCompleteOK(){
   var one = false;               
   $(".cboxClass").each(function(){
       var t = $(this);
       if(t.attr("status") == "1" && t.is(":checked")){
           one = true;
       }
   });
   if(one){
       $("#completebtn").addClass("btn").removeClass("btndisable");
   }else{
       $("#completebtn").addClass("btndisable").removeClass("btn");
   }
}

function toSearch(){
   $(".ordersearchform").attr("action","/ordering/index");
   $(".ordersearchform").submit();
}

function toExport(){
   $(".ordersearchform").attr("action","/ordering/export");
   $(".ordersearchform").submit();
}


function selectAll(obj){
    if($(obj).is( ":checked" )){
        $(".cboxClass").prop("checked",true);
    }else{
        $(".cboxClass").prop("checked",false);
    }
    isCompleteOK();
}

function toAssign(){
    var cb = $(".cboxClass:checked");
    if(cb.length != 1){
        alert("Please select one and only one record to assign so!");
        return;        
    }else if(cb.attr("status") != 0){
        alert("The record is not in New status!");
        return;
    }else{
        $( "#so-div" ).dialog( "open" );
    }
}

function toComplete(){
    var cb = $(".cboxClass:checked");
    if(cb.length != 1){
        alert("Please select one and only one record to edit status!");
        return;        
    }else if(cb.attr("status") != 1){
        alert("The record is not in process status!");
        return;
    }else{
        var params = {
            id : cb.val(),                       
            t : $.now()
        };
        $.getJSON("/ordering/ajaxOrderInfo",params,function(r){
            if(r.flag != 0 ){
                alert(r.msg);
                return;
            }else{
                $(".num","#ship-div").numeric();
                $( "#ship-div" ).dialog( "open" );
            }
        });
    }     
}
