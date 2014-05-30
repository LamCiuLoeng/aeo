<%inherit file="rpac.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
from tg import session
from repoze.what.predicates import in_group
%>

<%def name="extTitle()">r-pac - Service Bureau Ordering</%def>

<%def name="extCSS()">
<link rel="stylesheet" type="text/css" href="/css/nyroModal.css" media="screen,print"/>
<style type="text/css">
	td {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 12px;
        line-height: normal;
    }
	
	.option {
        border: #aaa solid 1px;
        width: 250px;
        background-color: #FFe;
    }

	
	#warning {
		font:italic small-caps bold 16px/1.2em Arial;
	}
	
	.error {
	   background-color: #FFEEEE !important;
	   border: 1px solid #FF6600 !important;
	}
	        
    .num,.float{
        text-align : right;
    }
    
    .label{
       background-color: #4e7596;
        border-bottom: #FFF solid 1px;
        padding-right: 10px;
        font-family: Tahoma, Geneva, sans-serif;
        font-size: 12px;
        font-weight: bold;
        text-decoration: none;
    }
    
    .template,.parttemplate {
        display : none;
    }
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.nyroModal.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/listItems.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/item_common.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
//<![CDATA[
        $(document).ready(function(){
            $(".num").numeric();
            $('.nyroModal').nyroModal();
            
            
            $( "#option-div" ).dialog({
                  modal: true,
                  autoOpen: false,
                  width: 850,
                  height: 600 ,
                  buttons: {
                    "Submit" : function() { 
                        addtocart();
                    },
                    "Cancel" : function() { $( this ).dialog( "close" ); }
                  }
             });
                
        });
        
        function checkout(){
            window.location.href = '/ordering/placeorder';
        }
        
        function PreviewImage(imageUrl, index) {
            $("#nyroModal" + index).html("<img src=\"" + imageUrl + "\" />");
        }
        
		function toSearch(){
			$("form").submit();
		}
//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/index"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Service Bureau Ordering</div>

<div>
	${widget(values,action="/ordering/listItems")|n}
</div>
<div style="clear:both"></div>
<%
    my_page = tmpl_context.paginators.result
    pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
%>    
<div style="width:1300px;padding:10px">
    <p style="text-align:right; padding:0px 0px 0px 0px">
    	<input type="button" class="btn" value="Search" onclick="toSearch()"/>
        <input type="button" onclick="checkout()" class="btn checkoutbtn" value="Shopping Cart [${len(session.get('items',[]))}],Checkout">
    </p> 
    
    <table cellspacing="0" cellpadding="0" border="0" class="gridTable" style="background:white">
    <thead>
    	 %if my_page.item_count > 0 :
              <tr>
                <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="20">
                  ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                </td>
              </tr>
          %endif
        <tr style="text-align: center;">                     
            <th style="width:100px;height:30px;">Action</th>
            <th style="width:200px">Item Code</th>
            <th style="width:100px">Division</th>
            <th style="width:100px">Brand</th>
            <th style="width:100px">Category</th>
            <th style="width:100px">Product Type</th>
            <th style="width:50px">Price</th>
            <th style="width:50px">Logo</th>
            <th style="width:50px">Size</th>
            <th style="width:50px">Content</th>
            <th style="width:50px">Care</th>
            <th style="width:100px">Image</th>
        </tr>
    </thead>
    <tbody>
    	%if len(result) < 1:
            <tr>
                <td colspan="100" style="border-left:1px solid #ccc">No match record(s) found!</td>
            </tr>
        %else:
	        %for index,p in  enumerate(result):
	            %if index % 2 == 0:
	                <tr class="even">
	            %else:
	                <tr class="odd">
	            %endif
	                <td style="border-left:1px solid #ccc;"><input type="button" class="btn" value="Add to Cart" onclick="showoptions(${p.id})"/></td>
	                <td style="text-align:left;padding-left:5px;">${p.itemCode}</td>
	                <td>${p.division}</td>
	                <td>${p.brand}</td>
	                <td>${p.category}</td>
	                <td>${p.productType}</td>
	                <td>${p.highPrice or ''}</td>
	                <td>${p.logo}</td>
	                <td>${p.size}</td>
	                <td>${p.content}</td>
	                <td>${p.care}</td>
	                <td style="padding:5px;">
	                    <a href='${p.image}' class="nyroModal" title="${p.itemCode}">
	                    <img src="${p.thumb}"/>
	                    </a>
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
    
    <p style="text-align:right; padding:0px 0px 0px 0px">
        <input type="button" onclick="checkout()" class="btn checkoutbtn" value="Shopping Cart [${len(session.get('items',[]))}],Checkout">
    </p> 
</div>

<div style="clear:both"></div>


<div id="option-div" title="Select Item's Option">
    <input type="hidden" id="current_item" value=""/>
    <table class="" cellpadding="3" cellspacing="3" border="1" id="option-tb" style="width:800px">
        
    </table>
</div>
