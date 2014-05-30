<%inherit file="rpac.templates.master"/>

<%
    from repoze.what.predicates import in_any_group,in_group,has_permission
%>

<%def name="extTitle()">r-pac - Check Order Screen</%def>

<%def name="extCSS()">
    <link rel="stylesheet" type="text/css" href="/css/nyroModal.css" media="screen,print"/>
    <link rel="stylesheet" type="text/css" href="/css/custom/status.css" media="screen,print"/>
    <style type="text/css">
        .gridTable td {
            padding : 5px;
        }
        
        .num {
            text-align : right;
            width : 100px;
        }
        
        .template{
        	display : none;
        }
    </style>
</%def>

<%def name="extJavaScript()">
    <script type="text/javascript" src="/js/jquery.nyroModal.custom.min.js" language="javascript"></script>
    <script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
    <script type="text/javascript" src="/js/custom/ordering_index.js" language="javascript"></script>
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
		
    //]]>
   </script>
</%def>


<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="176" valign="top" align="left"><a href="/ordering/index"><img src="/images/images/menu_title_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Check Order Screen</div>

<div>
	${widget(values,action="/ordering/index")|n}
</div>
<div style="clear:both"></div>

<div style="margin:5px 0px 10px 10px">
    <input type="button" class="btn" value="Search" onclick="toSearch()"/>&nbsp;
    %if has_permission("MAIN_ORDERING_EXPORT"):
        <input type="button" class="btn" value="Export" onclick="toExport()"/>&nbsp;
    %endif
    %if has_permission("MAIN_ORDERING_ASSIGN_SO"):
        <input type="button" class="btn" value="Add SO" onclick="toAssign()"/>&nbsp;
    %endif
    %if has_permission("MAIN_ORDERING_EDIT_STATUS"):
        <input type="button" class="btndisable" value="Complete" onclick="toComplete()" id="completebtn"/>&nbsp;
    %endif
</div>
<%
    my_page = tmpl_context.paginators.result
    pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
%>
<div id="recordsArea" style="margin:5px 0px 10px 10px">
    <table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:1430px">
        <thead>
          %if my_page.item_count > 0 :
              <tr>
                <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="20">
                  ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                </td>
              </tr>
          %endif
            <tr>
                <th width="50"><input type="checkbox" onclick="selectAll(this)"/></th>
                <th width="150" height="25">Job No</th>
                <th width="250">AEO PO#</th>
                <th width="250">Vendor PO</th>
                <th width="250">Item Ordered</th>
                <th width="200">Create Date (HKT)</th>
                <th width="150">Create By</th>
                <th width="150">Total Qty</th>
                <th width="200">r-pac manufacturing location</th>
                <th width="150">Status</th>
                <th width="180">Completed Date</th>
                <th width="150">Courier</th>
                <th width="200">Tracking Number</th>
                %if is_admin:
                	<th>High price</th>
                	<th>Low price</th>
                	<th>Commision</th>
                %endif
            </tr>
        </thead>
        <tbody>
            %if len(result) < 1:
                <tr>
                    <td colspan="100" style="border-left:1px solid #ccc">No match record(s) found!</td>
                </tr>
            %else:
                %for obj in result:
                <tr>
                    <td style="border-left:1px solid #ccc;"><input type="checkbox" value="${obj.id}" class="cboxClass" status="${obj.status}"/></td>
                    <td><a href="/ordering/detail?id=${obj.id}">${obj.no}</a></td>
                    <td>${obj.customerpo}</td>
                    <td>${obj.vendorpo}</td>
                    <td>
                    	%if obj.items:
                    		${' , '.join(obj.items.split("|"))}		
                    	%endif
                    </td>
                    <td>${obj.createTime.strftime("%Y/%m/%d %H:%M")}</td>
                    <td>${obj.createBy}</td>
                    <td>${obj.totalQty}</td>
                    <td>${obj.printShop}</td>
                    <td class="status${obj.status}">${obj.showStatus()}</td>
                    <td>${obj.completeDate.strftime("%Y/%m/%d %H:%M") if obj.completeDate else ''}</td>
                    <td>${obj.courier}</td>
                    <td>${obj.trackingNumber}</td>
                    %if is_admin:
                    	<td></td>
                    	<td></td>
                    	<td></td>
                    %endif
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





<div id="so-div" title="Assign SO">
    <table >
        <tr>
            <td valign="top" width="120">SO#</td>
            <td><input type="text" id="so" value=""/></td>
        </tr>        
    </table>
</div>

<div id="ship-div" title="Complete Order">
    <table >
        <tr>
            <td valign="top" width="150">Courier</td>
            <td><input type="text" id="courier" value=""/></td>
        </tr>
        <tr>
            <td valign="top">Tracking number</td>
            <td><input type="text" id="trackingNumber" value=""/></td>
        </tr>        
    </table>
</div>