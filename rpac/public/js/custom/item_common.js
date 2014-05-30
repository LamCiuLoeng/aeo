if(!Array.indexOf) 
{ 
    Array.prototype.indexOf = function(obj) 
    {                
        for(var i=0; i<this.length; i++) 
        { 
            if(this[i]==obj){ return i; } 
        } 
        return -1; 
    };
}

if(!String.trim){
    String.prototype.trim=function(){return this.replace(/(^\s*)|(\s*$)/g,"");};
}
    



function outputOptions(list,val){
    var _html = '';
    for(var i=0;i<list.length;i++){
        var t = list[i];
        if(t.key+'' == val + ''){
            _html += '<option value="'+t.key+'" selected="selected">'+t.value+'</option>';
        }else{
            _html += '<option value="'+t.key+'">'+t.value+'</option>';
        }
    }
    return _html;
}


function adjustqty(obj){
    var t = $(obj);
    var v = t.val().trim();
    var moq = parseInt(t.attr('moq'));
    var roundup = parseInt(t.attr('roundup'));
    
    if(!isNaN(moq)){
        v = v > moq ? v : moq;
    }
    if(!isNaN(roundup)){
        var n = v % roundup == 0 ? 0 : 1; 
        v = roundup * (parseInt(v / roundup ) + n);
    }
    t.val(v);
}

var timestamp = $.now();
var index = 11;


function _add(obj,cls){
	var t = $(obj);
    var cell = $(t.parents(cls)[0]);
    var template = $(".template:eq(0)",cell);
    var clone = template.clone().removeClass("template").addClass("copied");
    index ++;
    $("input[type='text'],select",clone).each(function(){
        var k = $(this);
        var n = k.attr("name");
        k.attr("name",n.replace("_x","_"+timestamp+index));
    });
    template.before(clone);
}



function addrow(obj){
	/*
    var t = $(obj);
    var cell = $(t.parents(".cell")[0]);
    var template = $(".template",cell);
    var clone = template.clone().removeClass("template").addClass("copied");
    index ++;
    $("input[type='text'],select",clone).each(function(){
        var k = $(this);
        var n = k.attr("name");
        k.attr("name",n.replace("_x","_"+timestamp+index));
    });
    template.before(clone);
    */
   _add(obj,".cell");
}

function addpart(obj){
	var t = $(obj);
    var cell = $(t.parents("td.part")[0]);
    var template = $(".parttemplate",cell);
    var clone = template.clone().removeClass("parttemplate").addClass("copied");
    index ++;
    $("input[type='text'],select",clone).each(function(){
        var k = $(this);
        var n = k.attr("name");
        k.attr("name",n.replace("_y","_"+timestamp+index));
    });
    template.before(clone);
}

function addContent(obj){
	_add(obj,".content");
}

function delrow(obj){
    var t = $(obj);
    $(t.parents(".copied")[0]).remove();
}


function checkInput(){
    var msg = [];
    var numreg = /^\d+$/;
    var floatreg = /^\d+(.\d+)?$/;
    
    $(".error").removeClass("error");
    
    var qs = $("input[name^='option_qty_']");
    if(qs.length > 0){
        var qtyok = false;
        qs.each(function(){
            var t = $(this);
            if(t.val()){ qtyok = true; }
        });
        if(!qtyok){ msg.push("Please input at lease one qty! "); }
    }else{
        if(!$("input[name='option_qty']").val()){
            msg.push("Please input the qty !");
        }
    }
    
    
    var allrequired = true;
    $(".required").not("form").not("[name$='_x']").each(function(){
        var t = $(this);
        if(!t.val()){ 
            allrequired = false;
            t.addClass("error"); 
        }
    });
    if(!allrequired){ msg.push("Please input the required field(s)"); }
        
    var allnum = true;
    $(".num").not("[name$='_x']").each(function(){
        var t = $(this);
        if(t.val() && !numreg.test(t.val()) ){ 
            allnum = false; 
            t.addClass("error");
        }
    });
    if(!allnum){ msg.push("Please correct the number field(s)"); }
    
    var allfloat = true;
    $(".float").not("[name$='_x']").each(function(){
        var t = $(this);
        if(t.val() && !floatreg.test(t.val()) ){ 
            allfloat = false; 
            t.addClass("error");
        }
    });
    if(!allfloat){ msg.push("Please correct the float field(s)"); }
    
    
    var allsum = {};
    var atleastsum = false;
    var sumok = true;
    $(".percent").not("[name$='_x']").each(function(){
        var t = $(this);    
        var _id = t.attr("name").split("_")[2];
        var v = parseFloat(t.val());
        if(!isNaN(v)){ 
            if(isNaN(allsum[_id])){ allsum[_id] = 0; }
            allsum[_id] += v; 
            atleastsum = true;
        }        
    });
    
    for(k in allsum){
        if(allsum[k] != 100){ sumok = false; }
    }
    if(!atleastsum){ msg.push("Please input at lease one percentage !"); }
    if(!sumok){ msg.push("Please input the correct fiber percentage, total should be 100% !"); }
    return msg;
}




function _o(v){
   var options = '';
   var fs = ['MEXICO ONLY','CHINA ONLY'];
   for(var m=0;m<fs.length;m++){
   options += '<option value="'+fs[m]+'"';
       if(v == fs[m]){
           options += ' selected="selected"';
       }
       options += '>' + fs[m] + '</option>';
   }
   return options;
       
}
   
//draw every part table
function _p(partname,partvalue,onlyname,onlyvalue,contentlist,contentvalues,perlist,pervalues,first,r){
   var _pid = partname.split("_")[2];
   
   var tb = '<table class="content">';
   tb += '<tr><td style="width:100px;">Garment Part</td><td><select name="'+partname+'" style="width:250px;">'+outputOptions(r.options.content.parts,partvalue);
   tb += '</select>&nbsp;<select name="'+onlyname+'" style="width:100px;">'+_o(onlyvalue)+'</select></td>';
   if(first){
       tb += '<td><input type="button" class="btn" value="Add Garment Part" onclick="addpart(this)"/></td></tr>';
   }else{
       tb += '<td><input type="button" class="btn" value="Del Garment Part" onclick="delrow(this)"/></td></tr>';
   }
   if(contentlist.length > 0){
       for(var k=0;k<contentlist.length;k++){
           if(k==0){
               var prefix = '<tr>';
               var subfix = '<td><input type="button" class="btn" value="Add Content" onclick="addContent(this)"/></td>';
           }else{
               var prefix = '<tr class="copied">';
               var subfix = '<td><input type="button" class="btn" value="Del Content" onclick="delrow(this)"/></td>';
           }
           tb += prefix;
           console.log(contentvalues[k]);
           tb += '<td style="width:100px;">Content</td><td><select name="'+contentlist[k]+'" style="width:250px;">'+outputOptions(r.options.content.fabrics,contentvalues[k])+'</select>&nbsp;';
           tb += '<input type="text" name="'+perlist[k]+'" value="'+pervalues[k]+'" style="width:100px;" class="percent float"/></td>';
           tb += subfix + '</tr>';                         
       }
   }else{
       
       tb += '<tr><td style="width:100px;">Content</td><td><select name="option_content_'+_pid+'_10" style="width:250px;">'+outputOptions(r.options.content.fabrics,null)+'</select>&nbsp;';
       tb += '<input type="text" name="option_percentage_'+_pid+'_10" value="" style="width:100px;" class="percent float"/></td>';
       tb += '<td><input type="button" class="btn" value="Add Content" onclick="addContent(this)"/></td></tr>';
       
   } 
   
   tb += '<tr class="template"><td style="width:100px;">Content</td><td><select name="option_content_'+_pid+'_x" style="width:250px;">'+outputOptions(r.options.content.fabrics,null)+'</select>';
   tb += '&nbsp;<input type="text" name="option_percentage_'+_pid+'_x" value="" style="width:100px;" class="percent float"/></td>';
   tb += '<td><input type="button" class="btn" value="Del Content" onclick="delrow(this)"/></td></tr>';
   tb += '</table>';
   return tb;
}