<%inherit file="rpac.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/custom/access.css" type="text/css" />
</%def>

<%def name="extJavaScript()">
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
        function toSave(){
            %if t in ['Division','Category','Brand',]:
                if(!$("#form1_name").val()){
                   alert("Please input the ${label} name!");
                   return false;
                }else{
                   $("form").submit();
                }
            %elif t in ['COO','Fibers','GarmentPart']:
                if(!$("#form2_english").val()){
                   alert("Please input the English!");
                   return false;
                }else{
                    $("form").submit();
                }            
            %elif t in ['Care',]:
                if(!$("#form3_english").val()){
                   alert("Please input the English!");
                   return false;
                }else{
                    $("form").submit();
                }      
            %elif t in ['Product', 'Size', ]:
                $("form").submit();
            %endif
        }

    //]]>
   </script>
</%def>


<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="176" valign="top" align="left"><a href="/access/index"><img src="/images/images/menu_master_g.jpg"/></a></td>
    <td width="176" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Master&nbsp;&nbsp;&gt;&nbsp;&nbsp;${label}&nbsp;&nbsp;&gt;&nbsp;&nbsp;New</div>

<div style="margin: 10px 0px; overflow: hidden;">
  <div style="float: left;">
    %if t in ['Division','Category','Brand',]:
        <div>
          <form name="userForm" class="tableform" method="post" action="/master/save_new">
          	<input type="hidden" name="t" value="${t}"/>
            <div class="case-list-one">
              <div class="case-list">
                <ul>
                  <li class="label">
                    <label for="form1_value" class="fieldlabel">${label} Name</label>
                  </li>
                  <li>
                    <input type="text" id="form1_name" name="name" class="textfield" style="width: 250px;"/>
                  </li>
                </ul>            
              </div>
            </div>
            <div style="clear: both;"><br/>
            </div>
          </form>
        </div>

    %elif t in ['COO','Fibers','GarmentPart']:
        <div>
          <form name="groupForm" class="tableform" method="post" action="/master/save_new">
          	<input type="hidden" name="t" value="${t}"/>
            <div class="case-list-one">
              <div class="case-list">
	              %for l,n in [("English","english"),("Spanish (MX)","spanish_mx"),("Russian","russian"),("Arabic","arabic"),("Hebrew","hebrew"),("Polish","polish"),("Bahasa","bahasa"),("Dutch","dutch")]:
		                <ul>
		                  <li class="label">
		                    <label for="form2_english" class="fieldlabel">${l}</label>
		                  </li>
		                  <li>
		                    <input type="text" id="form2_${n}" name="${n}" class="textfield" style="width: 250px;" value=""/>
		                  </li>
		                </ul>
	            	%endfor
              </div>
            </div>
            <div class="case-list-one">
              <div class="case-list">
	              %for l,n in [("French Canadian","french_canadian"),("Spanish (Latin)","spanish_latin"),("French (Morocco + France)","french"),("Japanese","japanese"),("Turkish","turkish"),("Chinese (simplified)","chinese_simple"),("German","german"),("Hindi","hindi")]:
		                <ul>
		                  <li class="label">
		                    <label for="form2_${n}" class="fieldlabel">${l}</label>
		                  </li>
		                  <li>
		                    <input type="text" id="form2_${n}" name="${n}" class="textfield" style="width: 250px;" value="${getattr(obj,n,'')}"/>
		                  </li>
		                </ul>
	              %endfor
              </div>
            </div>
            <div style="clear: both;"><br/></div>
          </form> 
        </div>
    
    %elif t in ['Care',]:
        <div>
          <form name="groupForm" class="tableform" method="post" action="/master/save_new">
            <input type="hidden" name="t" value="${t}"/>
            <div class="case-list-one">
              <div class="case-list">
                %for l,n in [("English","english"),("Spanish (MX)","spanish_mx"),("Russian","russian"),("Arabic","arabic"),("Hebrew","hebrew"),("Polish","polish"),("Bahasa","bahasa"),("Dutch","dutch")]:
	                <ul>
	                  <li class="label">
	                    <label for="form2_english" class="fieldlabel">${l}</label>
	                  </li>
	                  <li>
	                    <input type="text" id="form2_${n}" name="${n}" class="textfield" style="width: 250px;" value="${getattr(obj,n,'')}"/>
	                  </li>
	                </ul>
            	%endfor
                <ul>
                  <li class="label">
                    <label for="form3_type" class="fieldlabel">Type</label>
                  </li>
                  <li>
                    <select id="form3_type" name="type" style="width: 250px;">
                        %for k,v in [( 'WASH', "Wash" ), ( 'BLEACH', "Bleach" ),( 'DRY', "Dry" ), ( 'IRON', "Iron" ),( 'DRYCLEAN', "Dry Clean" ), ( 'SPECIALCARE', "Special Care" )]:
                            <option value="${k}">${v}</option>
                        %endfor
                    </select>
                  </li>
                </ul>
              </div>
            </div>
            <div class="case-list-one">
              <div class="case-list">
	              %for l,n in [("French Canadian","french_canadian"),("Spanish (Latin)","spanish_latin"),("French (Morocco + France)","french"),("Japanese","japanese"),("Turkish","turkish"),("Chinese (simplified)","chinese_simple"),("German","german"),("Hindi","hindi")]:
		                <ul>
		                  <li class="label">
		                    <label for="form2_${n}" class="fieldlabel">${l}</label>
		                  </li>
		                  <li>
		                    <input type="text" id="form2_${n}" name="${n}" class="textfield" style="width: 250px;" value="${getattr(obj,n,'')}"/>
		                  </li>
		                </ul>
	              %endfor
              </div>
            </div>
            <div style="clear: both;"><br/></div>
          </form> 
        </div>
    
    %elif t in ['Product',]:
        <div>
          <form name="groupForm" class="tableform" method="post" action="/master/save_new" enctype="multipart/form-data">
            <input type="hidden" name="t" value="${t}"/>
            <div class="case-list-one">
              <div class="case-list">

                <ul>
                  <%
                    l, n = "Division", "divisionId"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in divisions:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

                <ul>
                  <%
                    l, n = "Brand", "brandId"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in brands:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

                <ul>
                  <%
                    l, n = "Category", "categoryId"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in cats:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

                <ul>
                  <%
                    l, n = "Logo", "logo"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in [( 'Y', "Y" ), ( 'N', "N" )]:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

                <ul>
                  <%
                    l, n = "Size", "size"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in [( 'Y', "Y" ), ( 'N', "N" )]:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

                <ul>
                  <%
                    l, n = "Content", "content"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in [( 'Y', "Y" ), ( 'N', "N" )]:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

                <ul>
                  <%
                    l, n = "Care", "care"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in [( 'Y', "Y" ), ( 'N', "N" )]:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

              </div>
            </div>

            <div class="case-list-one">
              <div class="case-list">
                %for l,n in [("ItemCode","itemCode"),("Width","width"),("Substrate","substrate")]:
                    <ul>
                      <li class="label">
                        <label for="form2_${n}" class="fieldlabel">${l}</label>
                      </li>
                      <li>
                        <input type="text" id="form2_${n}" name="${n}" class="textfield" style="width: 250px;" value="${getattr(obj,n,'')}"/>
                      </li>
                    </ul>
                %endfor

                <ul>
                  <%
                    l, n = "Image", "image"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <input type="file" id="id_${n}" name="${n}" accept="image/gif, image/jpeg, image/png, image/jpg">
                    <script>
                      var file = document.getElementById('id_image');
                      file.onchange = function(e){
                          var ext = this.value.match(/\.([^\.]+)$/)[1];
                          switch(ext)
                          {
                              case 'jpg':
                              case 'bmp':
                              case 'png':
                              case 'jpeg':
                              case 'gif':
                                  break;
                              default:
                                  alert('jpg, bmp, png, jpeg, gif only!');
                                  this.value='';
                          }
                      };
                    </script>
                  </li>
                </ul>

              </div>
            </div>
            <div style="clear: both;"><br/></div>
          </form> 
        </div>

    %elif t in ['Size',]:
        <div>
          <form name="groupForm" class="tableform" method="post" action="/master/save_new" enctype="multipart/form-data">
            <input type="hidden" name="t" value="${t}"/>
            <div class="case-list-one">
              <div class="case-list">

                <ul>
                  <%
                    l, n = "Brand", "brandId"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in brands:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

                <ul>
                  <%
                    l, n = "Category", "categoryId"
                  %>
                  <li class="label">
                    <label for="${n}" class="fieldlabel">${l}</label>
                  </li>
                  <li>
                    <select id="${n}" name="${n}" style="width: 250px;">
                      %for k,v in cats:
                        <option value="${k}">${v}</option>
                      %endfor
                    </select>
                  </li>
                </ul>

              </div>
            </div>

            <div class="case-list-one">
              <div class="case-list">
                %for l,n in [("US Size","us_size"),("Canada Size","ca_size"),("Mexico Size","mx_size"),('UK Size','uk_size'),('Chinese Size','cn_size')]:
                    <ul>
                      <li class="label">
                        <label for="form2_${n}" class="fieldlabel">${l}</label>
                      </li>
                      <li>
                        <input type="text" id="form2_${n}" name="${n}" class="textfield" style="width: 250px;" value="${getattr(obj,n,'')}"/>
                      </li>
                    </ul>
                %endfor

              </div>
            </div>
            <div style="clear: both;"><br/></div>
          </form> 
        </div>
    %endif
  </div>
</div>
