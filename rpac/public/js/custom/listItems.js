/*
function showoptions(id){
    $("#current_item").val(id);
    var params = {
        id : id,
        t : $.now()
    };
    $.getJSON('/ordering/ajaxProductInfo',params,function(r){
       if(r.flag!=0){
           alert(r.msg);
           return ;
       }else{
           //parese the product option begin
           var required = '<sup class="star">*</sup>';
           var html = '<tr><td style="width:200px">'+required+'Qty</td><td><input type="text" class="option num required"  id="item_qty" name="qty" moq="'+r.product.moq+'" roundup="'+r.product.roundup+'" onchange="adjustqty(this)"/></td></tr>';
           for(var i=0;i<r.options.length;i++){
               var option = r.options[i];
               html += '<tr><td valign="top">';              
               if(option.css.SELECT.indexOf('required') > -1 || option.css.TEXT.indexOf('required') > -1){
                   html += required + option.name+'</td><td>';
               }else{ html += option.name+'</td><td>'; }
               if(option.type == 'TEXT'){ // ONLY TEXT
                   var css = option.css.TEXT.join(" ");        
                   if(option.multiple == 'Y'){  //multiple 
                       html += '<div><input type="text" class="option '+css+'" name="option_a_'+option.id+'_10" value=""/>';
                       html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                       html += '<div class="template"><input type="text" class="option '+css+'" name="option_a_'+option.id+'_x" value=""/>';
                       html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                   }else{
                       html += '<input type="text" class="option '+css+'" name="option_a_'+option.id+'" value=""/>';
                   }
                   
               }else if(option.type == 'SELECT'){ // ONLY SELECT
                   var optionhtml = outputOptions(option.values,null);
                   var css = option.css.SELECT.join(" ");
                   if(option.multiple == 'Y'){  //multiple
                       html += '<div><select name="option_a_'+option.id+'" class="option '+css+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                       html += '<div class="template"><select name="option_a_' + option.id + '_x" class="option '+css+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                   }else{
                       html += '<select name="option_a_'+option.id+'" class="option '+css+'">'+optionhtml+'</select>';
                   }
               }else if(option.type == 'SELECT+TEXT'){ // SELECT + TEXT
                   var optionhtml = outputOptions(option.values,null);
                   var selectcss = option.css.SELECT.join(" ");
                   var textcss = option.css.TEXT.join(" ");
                   if(option.multiple == 'Y'){  //multiple
                       html += '<div><select name="option_as_'+option.id+'" class="option '+selectcss+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'" style="width:80px"/>';
                       html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                       html += '<div class="template"><select name="option_as_' + option.id + '_x" class="option '+selectcss+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'_x" style="width:80px"/>';
                       html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                   }else{
                       html += '<select name="option_as_'+option.id+'" class="option '+selectcss+'">'+optionhtml+'</select>';
                       html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'" style="width:80px"/>';
                   }
               }
               html += '</td></tr>' ;
           }//FOR
                                                    
           $("#option-tb").html(html);
           $(".num,.float","#option-tb").numeric();
           //parese the product option end
           var height = 400; 
           if(r.options.length < 3){
               height = 300;
           }else if(r.options.length < 5){
               height = 400;
           }else if(r.options.length < 9){
               height = 500;
           }else{
               height = 600;
           }
           $( "#option-div" ).dialog({height : height});
           $( "#option-div" ).dialog( "open" );           
       }
    });
}
    
*/


function showoptions(id){
    $("#current_item").val(id);
    var params = {
        id : id,
        t : $.now()
    };
	$.getJSON('/ordering/ajaxProductInfo',params,function(result){
		if(result.flag!=0){
           alert(result.msg);
           return ;
       }else{
           console.log(result.product.type);
           if(result.product.type == 'GUARANTEECARD'){
               var html = showGuaranteeCardOptions(result);
           }else{
               var html = showNormalOptions(result);
           }
           
           $("#option-tb").html(html);
           $(".num,.float","#option-tb").numeric();
           $( "#option-div" ).dialog( "open" );      
       }
	});

}


function showNormalOptions(r){
   var options = r.options;
   var required = '<sup class="star">*</sup>';
   var html = '';
   if(options.size != undefined){
       var os = '';
       for(var i=0; i< options.size.values.length;i++){
           var o = options.size.values[i];
           os += '<option value="'+o.key+'">'+o.value+'</option>';
       }
       
       html += '<tr><td style="width:100px">Size</td><td class="cell">';
       html += '<div><select name="option_size_10">' + os + '</select>&nbsp;Qty&nbsp;<input type="text" name="option_qty_10" class="num"/>&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
       html += '<div class="template"><select name="option_size_x">'+ os +'</select>&nbsp;Qty&nbsp;<input type="text" name="option_qty_x" class="num"/>&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
       html += '</td></tr>';
   }else{
       html += '<tr><td style="width:100px">'+required+'Qty</td><td><input type="text" class="option num required" name="option_qty"/></td></tr>';
   }
   
   if(options.coo != undefined){
       html += '<tr><td>COO</td><td><select name="option_coo">';
       for(var i=0; i< options.coo.values.length;i++){
           var o = options.coo.values[i];
           html += '<option value="'+o.key+'">'+o.value+'</option>';
       }
       html += '</select></tr>';
   }
   
   if(options.care != undefined){
       html += '<tr><td>Care Instruction</td><td>';
       var cs = [['WASH','Wash'],['BLEACH','Bleach'], ['DRY','Dry'], ['IRON','Iron'], ['DRYCLEAN','Dry Clean'], ['SPECIALCARE','Special Care']];
       for(var i=0;i<cs.length;i++){
           var c = cs[i];
           var os = '';
           for(var j=0;j<options.care.values[c[0]].length;j++){
               var t = options.care.values[c[0]][j];
               os += '<option value="'+t.key+'">'+t.value+'</option>';
           }
           
           html += '<table class="cell"><tr><td style="width:100px;">'+c[1]+'</td><td><select name="option_'+c[0]+'_10" style="width:350px;">'+os+'</select></td><td><input type="button" class="btn" value="Add" onclick="addrow(this)"/></td></tr>';
           html += '<tr class="template"><td>&nbsp;</td><td><select name="option_'+c[0]+'_x" style="width:350px;">'+os+'</select></td><td><input type="button" class="btn" value="Del" onclick="delrow(this)"/></td></tr>';               
           html += '</table>';
       }
       html += '</td></tr>';
   }
   
   if(options.content != undefined){
       var partselect = '';
       var contentselect = '';
       
       for(var i=0;i<options.content.parts.length;i++){
           var t = options.content.parts[i];
           partselect += '<option value="'+t.key+'">'+t.value+'</option>';
       }
       
       for(var i=0;i<options.content.fabrics.length;i++){
           var t = options.content.fabrics[i];
           contentselect += '<option value="'+t.key+'">'+t.value+'</option>';
       }
       
       function _tb(flag){
           var f =  flag != '_y' ? true : false;
           var tb = '<table class="content"><tr><td style="width:100px;">Garment Part</td><td><select name="option_part'+flag+'" style="width:250px;">'+partselect+'</select>';
           tb += '&nbsp;<select style="width:100px;" name="option_only'+flag+'"><option value="MEXICO ONLY">MEXICO ONLY</option><option value="CHINA ONLY">CHINA ONLY</option></select></td><td>';
           if(f){
               tb += '<input type="button" class="btn" value="Add Garment Part" onclick="addpart(this)"/></td></tr>';
           }else{
               tb += '<input type="button" class="btn" value="Del Garment Part" onclick="delrow(this)"/></td></tr>';
           }
           tb += '<tr><td style="width:100px;">Content</td><td><select name="option_content'+flag+'_10" style="width:250px;">'+contentselect+'</select>';
           tb += '&nbsp;<input type="text" name="option_percentage'+flag+'_10" value="" class="percent float" style="width:100px;"/></td><td><input type="button" class="btn" value="Add Content" onclick="addContent(this)"/></td></tr>';
           
           if(f){
               tb += '<tr class="template"><td style="width:100px;">Content</td><td><select name="option_content_10_x" style="width:250px;">'+contentselect+'</select>';
               tb += '&nbsp;<input type="text" name="option_percentage_10_x" value="" class="percent float" style="width:100px;"/></td><td><input type="button" class="btn" value="Del Content" onclick="delrow(this)"/></td></tr>';
           }else{
               tb += '<tr class="template"><td style="width:100px;">Content</td><td><select name="option_content_y_x" style="width:250px;">'+contentselect+'</select>';
               tb += '&nbsp;<input type="text" name="option_percentage_y_x" value="" class="percent float" style="width:100px;"/></td><td><input type="button" class="btn" value="Del Content" onclick="delrow(this)"/></td></tr>';
           }
           tb += '</table>';
           return tb;
       }
       html += '<tr><td>Fabric Content</td><td class="part"><div>' +_tb('_10') + '</div>';
       html += '<div class="parttemplate">'+_tb('_y')+'</div></td></tr>';              
   }
   return html;
}


function showGuaranteeCardOptions(r){
    var html = '';
    var ns = [['Qty','option_qty'],['Product Standard Name','option_ProductStandardName'],['China Size','option_ChinaSize'],
             ['Product Standard','option_ProductStandard'],['Quality Grade','option_QualityGrade'],
             ['Safety Standard','option_SafetyStandard'],['Qualified Certificate','option_QualifiedCertificate'],
             ['China Address','option_ChinaAddress']];
    var html = '';
    for(var i=0;i<ns.length;i++){
        html += '<tr><td>' + ns[i][0] + '</td><td><input type="text" name="'+ns[i][1];
        if(ns[i][1] == 'option_qty'){
            html += '" class="num"';
        }else{
            html += '" class="required"';
        }
        html += ' style="width:300px;"/></td></tr>';
    }

    //Fiber composition (drop down like other items)
    html += '<tr><td>Fiber Composition</td><td class="part">';
    html += '<div>' + _p('option_part_10',null,'option_only_10',null,[],[],[],[],true,r) + '</div>';
    html += '<div class="parttemplate">' + _p('option_part_y',null,'option_only_y',null,[],[],[],[],false,r) + '</div>';
    html += '</td></tr>';
    //Card with additional care terms (drop down like other items)
    html += '<tr><td>Card with additional care terms</td><td>';
    var cs = [['WASH','Wash'],['BLEACH','Bleach'], ['DRY','Dry'], ['IRON','Iron'], ['DRYCLEAN','Dry Clean'], ['SPECIALCARE','Special Care']];
    for(var i=0;i<cs.length;i++){
       var c = cs[i];
       var os = '';
       for(var j=0;j<r.options.care.values[c[0]].length;j++){
           var t = r.options.care.values[c[0]][j];
           os += '<option value="'+t.key+'">'+t.value+'</option>';
       }
       
       html += '<table class="cell"><tr><td style="width:100px;">'+c[1]+'</td><td><select name="option_'+c[0]+'_10" style="width:350px;">'+os+'</select></td><td><input type="button" class="btn" value="Add" onclick="addrow(this)"/></td></tr>';
       html += '<tr class="template"><td>&nbsp;</td><td><select name="option_'+c[0]+'_x" style="width:350px;">'+os+'</select></td><td><input type="button" class="btn" value="Del" onclick="delrow(this)"/></td></tr>';               
       html += '</table>';
    }
    html += '</td></tr>';
        
    //Country of Origin (drop down like other items)
    html += '<tr><td>Country of Origin</td><td><select name="option_coo" style="width:300px;">' + outputOptions(r.options.coo.values,null) + '</select></td></tr>';
    return html;
}


function addtocart(){
    var msg = checkInput();
    if(msg.length > 0){
        alert(msg.join('\n'));
        return;
    }
    var params = {
        id : $("#current_item").val(),
        t : $.now()
    };
    
    $(".template").remove();
    $(".parttemplate").remove();
    $("[name^='option_']").each(function(){
        var t = $(this);
        
        if(t.prop('tagName') == 'INPUT'){
            params[t.attr('name')] = [t.val(),t.val()].join("|");
        }else if(t.prop('tagName') == 'SELECT'){
            params[t.attr('name')] = [t.val(),$(":selected",t).text()].join("|");
        }        
    });
    
    $.getJSON('/ordering/ajaxAddtoCart',params,function(r){
        if(r.flag !=0){
            alert(r.msg);
        }else{
            //window.location.reload(true);
            alert('Add the item to shopping cart successfully!');
            $(".checkoutbtn").val("Shopping Cart [" + r.total + "],Checkout");
            $( "#option-div" ).dialog( "close" );  
        }
    });
}




