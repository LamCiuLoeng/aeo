function toCancel(){
    if(confirm("Are you sure to leave this page without saving ?")){
        window.location.href = "/index";
    }else{
        return;
    }
    
}

function toSave(){
    var msg = [];
    
    $(".error").removeClass("error");

    var fields = ['shipCompany','billCompany','shipAddress','billAddress',
                  'shipCity','billCity','shipState','billState',
                  'shipCountry','billCountry','shipTel','billTel','shipEmail','billEmail',
                  'customerpo','vendorpo','printShopId'];

    var allOK = true;         
    for(var i=0;i<fields.length;i++){
        var n = fields[i];
        if(!$("#"+n).val()){
            $("#"+n).addClass('error');
            allOK = false;
        }
    }
    if(!allOK){ msg.push('Please fill in the required field(s)!'); }
        
    if(msg.length > 0 ){
        var m = '<ul>';
        for(var i=0;i<msg.length;i++){ m += '<li>' + msg[i] + '</li>'; }
        m += '</ul>';        
        var html = '<div id="alert-message" title="Alert">'+ m +'</div>';
        $(html).dialog({
              modal: true,
              width: 500,
              buttons: {
                Ok: function() { $( this ).dialog( "close" ); }
              }
        });
        return;
    }else{ 
        $("form").submit();
    }
    
}


function removeItem(flag,obj){
    if(!window.confirm("Are you sure to remove this item ?")){
        return;
    }
    var params = {
        _k : flag,
        t : $.now()
    };
    $.getJSON('/ordering/ajaxRemoveItem',params,function(r){
        if(r.flag != 0 ){
            alert(r.msg);
            return;
        }else{
            alert('Remove the item successfully!');
            var t = $(obj);
            $(t.parents("tr")[0]).remove();
        }
    });
}

/*
function searchItems(values,id,f){
    if(f === undefined ){
        f = 'a';
    }
    var r = new RegExp("^option_"+f+"_"+id,"g");
    var result = [];
    for(var i=0;i<values.length;i++){
        var t = values[i];
        if(t.key.search(r) > -1){
            result.push(t);
        }
    }
    return result;
}
*/

function searchItems(values,prefix){
	var r = new RegExp("^"+prefix,"g");
	var result = [];
    for(var i=0;i<values.length;i++){
        var t = values[i];
        if(t.key.search(r) > -1){
            result.push(t);
        }
    }
    return result;
}




function findMatch(key,values){
    var tmp = key.replace("_as_","_at_");
    for(var i=0;i<values.length;i++){
        if( tmp == values[i].key){ return values[i]; }
    }
    return null;
}

/*
function editItem(flag){
    var params = {
        _k : flag,
        t : $.now()
    };
    $.getJSON('/ordering/ajaxEditItem',params,function(r){
        if(r.flag != 0){
            alert(r.msg);
            return;
        }else{
            //parese the product option begin
            var html = '<tr><td style="width:200px">Qty</td><td><input type="text" class="option num required" id="item_qty" name="qty" moq="'+r.product.moq+'" roundup="'+r.product.roundup+'" onchange="adjustqty(this)" value="'+r.product.qty+'"/></td></tr>';
            for(var i=0;i<r.options.length;i++){
                var option = r.options[i];
                html += '<tr><td valign="top">' + option.name + '</td><td>';
                if(option.type == 'TEXT'){ // ONLY TEXT
                    var existing =  searchItems(r.values, option.id);
                    var css = option.css.TEXT.join(" ");      
                    if(option.multiple == 'Y'){  //multiple 
                        for(var j=0;j<existing.length;j++){  //add the previous input value
                            var e = existing[j];
                            html += '<div><input type="text" class="option '+css+'" name="'+e.key+'" value="' + e.value + '"/>';
                            if(j==0){
                                html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                            }else{
                                html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                            }
                        }
                        html += '<div class="template"><input type="text" class="option '+css+'" name="option_a_'+option.id+'_x" value=""/>';
                        html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                    }else{
                        if(existing.length > 0){
                            html += '<input type="text" class="option '+css+'" name="'+existing[0].key+'" value="'+existing[0].value+'"/>';
                        }else{
                            html += '<input type="text" class="option '+css+'" name="option_a_'+option.id+'" value=""/>';
                        }
                    }
                }else if(option.type == 'SELECT'){ // ONLY SELECT
                    var existing =  searchItems(r.values, option.id);
                    var css = option.css.SELECT.join(" ");
                    if(option.multiple == 'Y'){  //multiple
                        for(var j=0;j<existing.length;j++){  //add the previous input value
                            var e = existing[j];
                            html += '<div><select name="'+e.key+'" class="option '+css+'">';
                            html += outputOptions(option.values,e.value);
                            html += '</select>';
                            if(j==0){
                                html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                            }else{
                                html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                            }
                        }                        
                        html += '<div class="template"><select name="option_a_'+option.id+'_x" class="option '+css+'">'+outputOptions(option.values,null)+'</select>';
                        html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                    }else{
                        if(existing.length > 0){
                            html += '<select name="'+existing[0].key+'" class="option '+css+'">'+outputOptions(option.values,existing[0].value)+'</select>';
                        }else{
                            html += '<select name="option_a_'+option.id+'" class="option '+css+'">'+outputOptions(option.values,null)+'</select>';
                        }          
                    }                                   
                }else if(option.type == 'SELECT+TEXT'){ // SELECT + TEXT
                    var selectvalues =  searchItems(r.values, option.id,'as');
                    var inputvalues =  searchItems(r.values, option.id,'at');
                    var selectcss = option.css.SELECT.join(" ");
                    var textcss = option.css.TEXT.join(" ");
                    if(option.multiple == 'Y'){
                        if(selectvalues.length == inputvalues.length){
                            for(var j=0;j<selectvalues.length;j++){
                                var s = selectvalues[j];
                                var t = findMatch(s.key,inputvalues);
                                html += '<div><select name="'+s.key+'" class="option '+selectcss+'">' + outputOptions(option.values,s.value) + '</select>';
                                html += '&nbsp;<input type="text" class="option '+textcss+'" name="'+t.key+'" style="width:80px" value="'+t.value+'"/>';
                                if(j==0){
                                    html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                                }else{
                                    html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                                }
                            }
                        }else{
                            html += '<div><select name="option_as_'+option.id+'" class="option '+selectcss+'">' + outputOptions(option.values,null) + '</select>';
                            html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'" style="width:80px"/>';
                            html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                        }
                        html += '<div class="template"><select name="option_as_' + option.id + '_x" class="option '+selectcss+'">' + outputOptions(option.values,null) + '</select>';
                        html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'_x" style="width:80px"/>';
                        html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                    }else{
                        if( selectvalues.length ==1 && inputvalues.length == 1){
                            html += '<select name="option_as_'+option.id+'" class="option '+selectcss+'">'+outputOptions(option.values,selectvalues[0].value)+'</select>';
                            html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'" style="width:80px" value="'+inputvalues[0].value+'"/>';
                        }else{
                            html += '<select name="option_as_'+option.id+'" class="option '+selectcss+'">'+optionhtml+'</select>';
                            html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'" style="width:80px"/>';
                        }
                    } 
                }
                html += '</td></tr>';
            }// FOR
                
            $("#option-tb").html(html);
            $(".num,.float","#option-tb").numeric();
            //parese the product option end
            $("#current_item").val(flag);
            $( "#option-div" ).dialog( "open" );
        }
    });
}
*/


function editItem(flag) {
    var params = {
        _k : flag,
        t : $.now()
    };
    $.getJSON('/ordering/ajaxEditItem',params,function(result){
       if(result.flag != 0){
            alert(result.msg);
            return;
       }else{
           if(result.product.type == 'GUARANTEECARD'){
               var html =showGuaranteeCardOptions(result);
           }else{
               var html = showNormalOptions(result);
           }
       }
       
       $("#option-tb").html(html);
       $(".num,.float","#option-tb").numeric();
       $("#current_item").val(flag);
       $( "#option-div" ).dialog( "open" );
    });
    
}


function showNormalOptions(r){
   var options = r.options;
   var required = '<sup class="star">*</sup>';
   var htmlsize = '';
   var htmlcoo = '';
   var htmlcare = '';
   var htmlcontent = '';
   // size begin
   if(options.size != undefined){  //if there's size option
       var ssexisting =  searchItems(r.values, "option_size_");
       var qtyexisting =  searchItems(r.values, "option_qty_");
       htmlsize += '<tr><td style="width:100px">Size</td><td class="cell">';
       if(ssexisting.length > 0){
           for(var i=0;i<ssexisting.length;i++){
               var s = ssexisting[i];
               var q = qtyexisting[i];
               if(i==0){
                   htmlsize += '<div><select name="'+s.key+'">' + outputOptions(r.options.size.values,s.value) + '</select>&nbsp;Qty&nbsp;<input type="text" name="'+q.key+'" value="'+q.value+'" class="num"/>';
                   htmlsize += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
               }else{
                   htmlsize += '<div class="copied"><select name="'+s.key+'">' + outputOptions(r.options.size.values,s.value) + '</select>&nbsp;Qty&nbsp;<input type="text" name="'+q.key+'" value="'+q.value+'" class="num"/>';
                   htmlsize += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
               }
           }
       }else{
           htmlsize += '<div><select name="option_size_10">' + outputOptions(r.options.size.values,null) + '</select>&nbsp;Qty&nbsp;<input type="text" name="option_qty_10" class="num"/>&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
       }
       htmlsize += '<div class="template"><select name="option_size_x">'+ outputOptions(r.options.size.values,null) +'</select>&nbsp;Qty&nbsp;<input type="text" name="option_qty_x" class="num"/>&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';  
       htmlsize += '</td></tr>';                   
   }else{ //if no size option
       var qtyexisting =  searchItems(r.values, "option_qty");
       if(qtyexisting.length > 0){
           var q = qtyexisting[0];
           htmlsize += '<tr><td style="width:100px">'+required+'Qty</td><td><input type="text" class="option num required" name="option_qty" value="'+q.value+'"/></td></tr>';
       }else{
           htmlsize += '<tr><td style="width:100px">'+required+'Qty</td><td><input type="text" class="option num required" name="option_qty"/></td></tr>';
       }
   } // size end
   
   // coo start
   if(options.coo != undefined){
       var existing =  searchItems(r.values, "option_coo");
       htmlcoo += '<tr><td>COO</td><td><select name="option_coo">';
       if(existing.length > 0){
           var e= existing[0];
           htmlcoo += outputOptions(r.options.coo.values,e.value);
       }else{
           htmlcoo += outputOptions(r.options.coo,null);
       }
       htmlcoo += '</select></td></tr>';
   } // coo end
   
   // care start
   if(options.care != undefined){
       htmlcare += '<tr><td>Care Instruction</td><td>';
       var cs = [['WASH','Wash'],['BLEACH','Bleach'], ['DRY','Dry'], ['IRON','Iron'], ['DRYCLEAN','Dry Clean'], ['SPECIALCARE','Special Care']];
       for(var i=0;i<cs.length;i++){
           var c = cs[i];
           var cexisting = searchItems(r.values, "option_"+c[0]+"_");
           htmlcare += '<table class="cell">';
           if(cexisting.length > 0){
               for(var j=0;j<cexisting.length;j++){
                   var e = cexisting[j];
                   if(j==0){
                       htmlcare += '<tr><td style="width:100px;">'+c[1]+'</td><td><select name="'+e.key+'" style="width:350px;">'+outputOptions(r.options.care.values[c[0]],e.value)+'</select></td>';
                       htmlcare += '<td><input type="button" class="btn" value="Add" onclick="addrow(this)"/></td></tr>';
                   }else{
                       htmlcare += '<tr class="copied"><td style="width:100px;">&nbsp;</td><td><select name="'+e.key+'" style="width:350px;">'+outputOptions(r.options.care.values[c[0]],e.value)+'</select></td>';
                       htmlcare += '<td><input type="button" class="btn" value="Del" onclick="delrow(this)"/></td></tr>';
                   }
               }
           }else{
               htmlcare += '<tr><td style="width:100px;">'+c[1]+'</td><td><select name="option_'+c[0]+'_10" style="width:350px;">'+outputOptions(r.options.care.values[c[0]],null)+'</select></td><td><input type="button" class="btn" value="Add" onclick="addrow(this)"/></td></tr>';
           }
           htmlcare += '<tr class="template"><td>&nbsp;</td><td><select name="option_'+c[0]+'_x" style="width:350px;">'+outputOptions(r.options.care.values[c[0]],null)+'</select></td><td><input type="button" class="btn" value="Del" onclick="delrow(this)"/></td></tr>';               
           htmlcare += '</table>';
       }
       htmlcare += '</td></tr>';
   }// care end
   
   // content start
   if(options.content != undefined){
       htmlcontent += '<tr><td>Fabric Content</td><td class="part">';
       var psexisting = searchItems(r.values,"option_part_");
       var osexisting = searchItems(r.values,"option_only_");                     
       if(psexisting.length > 0){
           for(var i=0;i<psexisting.length;i++){
               var p = psexisting[i];
               var o = osexisting[i];
               _id = p.key.split("_")[2];
               var csexisting = searchItems(r.values,"option_content_" + _id + "_");
               var persexisting = searchItems(r.values,"option_percentage_" + _id + "_");
               var csnames = [];
               var csvalues = [];
               var pernames = [];
               var pervalues = [];
               for(var n=0;n<csexisting.length;n++){
                  csnames.push(csexisting[n].key);
                  csvalues.push(csexisting[n].value);
                  pernames.push(persexisting[n].key);
                  pervalues.push(persexisting[n].value); 
               }
               if(i==0){
                   htmlcontent += '<div>' + _p(p.key,p.value,o.key,o.value,csnames,csvalues,pernames,pervalues,true,r) + '</div>';
               }else{
                   htmlcontent += '<div class="copied">';
                   htmlcontent += _p(p.key,p.value,o.key,o.value,csnames,csvalues,pernames,pervalues,false,r);
                   htmlcontent += '</div>';
               }
               
           }
       }else{
           htmlcontent += '<div>' + _p('option_part_10',null,'option_only_10',null,[],[],[],[],true,r) + '</div>';
       }
       htmlcontent += '<div class="parttemplate">' + _p('option_part_y',null,'option_only_y',null,[],[],[],[],false,r) + '</div>';               
       htmlcontent += '</td></tr>';
       //alert(htmlcontent);
   }// content end
   return htmlsize+htmlcoo+htmlcare+htmlcontent;
}


function showGuaranteeCardOptions(r){
    var html = '';
    //html += '<tr><td>Qty</td><td><input type="text" name="option_qty" value="'+r.product.qty+'" class="num" style="width:300px;"/></td></tr>';
    
    function _c(label,name){
        var _html = '<tr><td>' + label + '</td><td>';
        var _existing = searchItems(r.values,name);
        if(_existing.length > 0){
            _html += '<input type="text" name="" value="'+_existing[0].value+'"';
        }else{
            _html += '<input type="text" name="" value=""';
        }
        if(name == 'option_qty'){
            _html += ' class="num"';
        }else{
            _html += ' class="required"';
        }
        _html += ' style="width:300px;"/></td></tr>';
        return _html;
    }
    var ns = [['Qty','option_qty'],['Product Standard Name','option_ProductStandardName'],['China Size','option_ChinaSize'],
             ['Product Standard','option_ProductStandard'],['Quality Grade','option_QualityGrade'],
             ['Safety Standard','option_SafetyStandard'],['Qualified Certificate','option_QualifiedCertificate'],
             ['China Address','option_ChinaAddress']];
    for(var i=0;i<ns.length;i++){
        html += _c(ns[i][0],ns[i][1]);
    }
    
    //Card with additional care terms (drop down like other items)
    html += '<tr><td>Fiber Composition</td><td class="part">';
    var psexisting = searchItems(r.values,"option_part_");
    var osexisting = searchItems(r.values,"option_only_");
    if(psexisting.length > 0){
       for(var i=0;i<psexisting.length;i++){
           var p = psexisting[i];
           var o = osexisting[i];
           _id = p.key.split("_")[2];
           var csexisting = searchItems(r.values,"option_content_" + _id + "_");
           var persexisting = searchItems(r.values,"option_percentage_" + _id + "_");
           var csnames = [];
           var csvalues = [];
           var pernames = [];
           var pervalues = [];
           for(var n=0;n<csexisting.length;n++){
              csnames.push(csexisting[n].key);
              csvalues.push(csexisting[n].value);
              pernames.push(persexisting[n].key);
              pervalues.push(persexisting[n].value); 
           }
           if(i==0){
               html += '<div>' + _p(p.key,p.value,o.key,o.value,csnames,csvalues,pernames,pervalues,true,r) + '</div>';
           }else{
               html += '<div class="copied">';
               html += _p(p.key,p.value,o.key,o.value,csnames,csvalues,pernames,pervalues,false,r);
               html += '</div>';
           }
           
       }
    }else{
       html += '<div>' + _p('option_part_10',null,'option_only_10',null,[],[],[],[],true,r) + '</div>';
    }
    html += '<div class="parttemplate">' + _p('option_part_y',null,'option_only_y',null,[],[],[],[],false,r) + '</div>';               
    html += '</td></tr>';
       
       
    //Country of Origin (drop down like other items)
    html += '<tr><td>Country of Origin</td><td>';
    var cooexisting = searchItems(r.values,"option_coo");
    if(cooexisting.length > 0){
        html += '<select style="width:300px;" name="'+cooexisting[0].name+'">' + outputOptions(r.options.coo.values,cooexisting[0].value);
    }else{
        html += '<select style="width:300px;" name="option_coo">' + outputOptions(r.options.coo,null);
    }
    html += '</select></td></tr>';
    return html;
}



function savetocart(){
    var msg = checkInput();
    if(msg.length > 0){
        alert(msg.join('\n'));
        return;
    }
    var _k = $("#current_item").val();
    var qty = $("#item_qty").val();
    var params = {
        _k : _k,
        qty : qty,
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
    
    $.getJSON('/ordering/ajaxSavetoCart',params,function(r){
        if(r.flag !=0){
            alert(r.msg);
        }else{
            //window.location.reload(true);
            var html = '<ul>';
            for(var i=0;i<r.optionstext.length;i++){
                html += '<li>' + r.optionstext[i] + '</li>';
            }
            html += '</ul>';
            $("#ot_" + _k).html(html);
            $("#qty_" + _k).text(qty);
            $( "#option-div" ).dialog( "close" );
        }
    });
}
