<%inherit file="rpac.templates.master"/>

<%
    from repoze.what.predicates import in_any_group,in_group,has_permission
%>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extCSS()">
    <link rel="stylesheet" type="text/css" href="/css/custom/status.css" media="screen,print"/>
    <style type="text/css">
        .gridTable td {
            padding : 5px;
        }
        
        .file_textarea {
            width:200px;
            height:30px;
        }
        
        .template{
            display : none;
        }
    </style>
</%def>

<%def name="extJavaScript()">
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
		$(document).ready(function(){
		    $( ".datePicker" ).datepicker({"dateFormat":"yy/mm/dd"});
		    $("#t").val("${values.get('t','')}");
		})
	        
	    function toSearch(){
	       $("form").submit()
	    }
	    
        function toEdit(id){
            window.location.href="/master/edit?id="+id+"&t=${values.get('t','')}";
        }
	    
	    function toDel(id){
	       if(window.confirm("Are you sure to delete this record?")){
	           window.location.href="/master/delete?id="+id+"&t=${values.get('t','')}";
	       }
	    }
    //]]>
   </script>
</%def>


<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="176" valign="top" align="left"><a href="/m"><img src="/images/images/menu_master_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
    <td width="176" valign="top" align="left"><a href="/master/add?t=${values.get('t','')}"><img src="/images/images/menu_new_g.jpg"/></a></td> 
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Master&nbsp;&nbsp;&gt;&nbsp;&nbsp;${label}</div>


<div>
	${widget(values,action="/master/index")|n}
</div>

<div style="clear:both"></div>

<%
    my_page = tmpl_context.paginators.result
    pager = my_page.pager(symbol_first="<<",show_if_single_page=True,t=values.get('t',''))
%>

<div id="recordsArea" style="margin:5px 0px 10px 10px">
    <table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:1200px">
        <thead>
          %if my_page.item_count > 0 :
              <tr>
                <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="20">
                  ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                </td>
              </tr>
          %endif
            <tr>
                %if values.get('t',None) in ['Division','Category','Brand',]:
                    <th width="700" height="25">${label} Name</th>
                %elif values.get('t',None) in ['Fibers','COO','GarmentPart',]:
                    <th width="150" height="25">English</th>
                    <th width="150" height="25">French Canadian</th>
                    <th width="150" height="25">Spanish (MX)</th>
                    <th width="150" height="25">Spanish (Latin)</th>
                    <th width="150" height="25">Russian</th>
                    <th width="150" height="25">French (Morocco + France)</th>
                    <th width="150" height="25">Arabic</th>
                    <th width="150" height="25">Japanese</th>
                    <th width="150" height="25">Hebrew</th>
                    <th width="150" height="25">Turkish</th>
                    <th width="150" height="25">Polish</th>
                    <th width="150" height="25">Chinese (simplified)</th>
                    <th width="150" height="25">Bahasa</th>
                    <th width="150" height="25">German</th>
                    <th width="150" height="25">Dutch</th>
                    <th width="150" height="25">Hindi</th>
                    
                %elif values.get('t',None) in ['Care',]:
                    <th width="100" height="25">Type</th>
                    <th width="150" height="25">English</th>
                    <th width="150" height="25">French Canadian</th>
                    <th width="150" height="25">Spanish (MX)</th>
                    <th width="150" height="25">Spanish (Latin)</th>
                    <th width="150" height="25">Russian</th>
                    <th width="150" height="25">French (Morocco + France)</th>
                    <th width="150" height="25">Arabic</th>
                    <th width="150" height="25">Japanese</th>
                    <th width="150" height="25">Hebrew</th>
                    <th width="150" height="25">Turkish</th>
                    <th width="150" height="25">Polish</th>
                    <th width="150" height="25">Chinese (simplified)</th>
                    <th width="150" height="25">Bahasa</th>
                    <th width="150" height="25">German</th>
                    <th width="150" height="25">Dutch</th>
                    <th width="150" height="25">Hindi</th>
                %elif values.get('t',None) in ['Product',]:
                    <th width="150" height="25">Division</th>
                    <th width="100" height="25">Brand</th>
                    <th width="150" height="25">Category</th>
                    <th width="150" height="25">Item Code</th>
                    <th width="150" height="25">Product Type</th>
                    <th width="150" height="25">High Price</th>
                    <th width="150" height="25">Low Price</th>
                    <th width="150" height="25">Image</th>
                %elif values.get('t',None) in ['Size',]:
                    <th width="100" height="25">Brand</th>
                    <th width="150" height="25">Category</th>
                    <th width="150" height="25">US Size</th>
                    <th width="150" height="25">Canada Size</th>
                    <th width="150" height="25">Mexico Size</th>
                    <th width="150" height="25">UK Size</th>
                    <th width="150" height="25">Chinese Size</th>
                %endif
                <th width="200">Create Date (HKT)</th>
                <th width="100">Action</th>
            </tr>
        </thead>
        <tbody>
            %if len(result) < 1:
                <tr>
                    <td colspan="20" style="border-left:1px solid #ccc">No match record(s) found!</td>
                </tr>
            %else:
                %for obj in result:
                <tr>
                    %if values.get('t',None) in ['Division','Category','Brand',]:
                        <td style="border-left:1px solid #ccc;">${obj.name or ''}&nbsp;</td>
                    %elif values.get('t',None) in ['COO','Fibers','GarmentPart']:
                        <td style="border-left:1px solid #ccc;">${obj.english or ''}&nbsp;</td>
                        <td>${obj.french_canadian or ''}&nbsp;</td>
                        <td>${obj.spanish_mx or ''}&nbsp;</td>
                        <td>${obj.spanish_latin or ''}&nbsp;</td>
                        <td>${obj.russian or ''}&nbsp;</td>
                        <td>${obj.french or ''}&nbsp;</td>
                        <td>${obj.arabic or ''}&nbsp;</td>
                        <td>${obj.japanese or ''}&nbsp;</td>
                        <td>${obj.hebrew or ''}&nbsp;</td>
                        <td>${obj.turkish or ''}&nbsp;</td>
                        <td>${obj.polish or ''}&nbsp;</td>
                        <td>${obj.chinese_simple or ''}&nbsp;</td>
                        <td>${obj.bahasa or ''}&nbsp;</td>
                        <td>${obj.german or ''}&nbsp;</td>
                        <td>${obj.dutch or ''}&nbsp;</td>
                        <td>${obj.hindi or ''}&nbsp;</td>
                        
                    %elif values.get('t',None) in ['Care',]:
                        <td style="border-left:1px solid #ccc;">${obj.showType() or ''}&nbsp;</td>
                        <td>${obj.english or ''}&nbsp;</td>
                        <td>${obj.french_canadian or ''}&nbsp;</td>
                        <td>${obj.spanish_mx or ''}&nbsp;</td>
                        <td>${obj.spanish_latin or ''}&nbsp;</td>
                        <td>${obj.russian or ''}&nbsp;</td>
                        <td>${obj.french or ''}&nbsp;</td>
                        <td>${obj.arabic or ''}&nbsp;</td>
                        <td>${obj.japanese or ''}&nbsp;</td>
                        <td>${obj.hebrew or ''}&nbsp;</td>
                        <td>${obj.turkish or ''}&nbsp;</td>
                        <td>${obj.polish or ''}&nbsp;</td>
                        <td>${obj.chinese_simple or ''}&nbsp;</td>
                        <td>${obj.bahasa or ''}&nbsp;</td>
                        <td>${obj.german or ''}&nbsp;</td>
                        <td>${obj.dutch or ''}&nbsp;</td>
                        <td>${obj.hindi or ''}&nbsp;</td>
                    %elif values.get('t',None) in ['Product',]:
                        <td style="border-left:1px solid #ccc;">${obj.division or ''}&nbsp;</td>
                        <td>${obj.brand or ''}&nbsp;</td>
                        <td>${obj.category or ''}&nbsp;</td>
                        <td>${obj.itemCode or ''}&nbsp;</td>
                        <td>${obj.productType or ''}&nbsp;</td>
                        <td>${obj.highPrice or ''}&nbsp;</td>
                        <td>${obj.lowPrice or ''}&nbsp;</td>
                        <td><img src="${obj.thumb or ''}"/>&nbsp;</td>
                    %elif values.get('t',None) in ['Size',]:
                        <td style="border-left:1px solid #ccc;">${obj.brand or ''}&nbsp;</td>
                        <td>${obj.category or ''}&nbsp;</td>
                        <td>${obj.us_size or ''}&nbsp;</td>
                        <td>${obj.ca_size or ''}&nbsp;</td>
                        <td>${obj.mx_size or ''}&nbsp;</td>
                        <td>${obj.uk_size or ''}&nbsp;</td>
                        <td>${obj.cn_size or ''}&nbsp;</td>
                    %endif
                    <td>${obj.createTime.strftime("%Y/%m/%d %H:%M") if obj.createTime else ''}</td>
                    <td>            
                        <input type="button" class="btn" onclick="toEdit(${obj.id})" value="Edit"/>&nbsp;
                        <input type="button" class="btn" onclick="toDel(${obj.id})" value="Del">
                    </td>
                </tr>
                %endfor
            %endif
            %if my_page.item_count > 0 :
              <tr>
                <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="20">
                  ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                </td>
              </tr>
            %endif
        </tbody>
    </table>
</div>
