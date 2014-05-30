<%inherit file="rpac.templates.master"/>

<%
  from repoze.what.predicates import not_anonymous, in_group, has_permission
%>

<%def name="extTitle()">r-pac - American Eagle Outfitters</%def>

<div class="main-div">
	<div id="main-content">
        %if has_permission("MAIN_ORDERING_PLACEORDER"):
            <div class="block">
                <a href="/ordering/listItems"><img src="/images/aeo.jpg" width="55" height="55" alt="" /></a>
                <p><a href="/ordering/listItems">Service bureau ordering</a></p>
            </div>
        %endif
        %if has_permission("MAIN_ORDERING_CHECKING"):
            <div class="block">
                <a href="/ordering/index"><img src="/images/aeo.jpg" width="55" height="55" alt="" /></a>
                <p><a href="/ordering/index">Check order screen</a></p>
            </div>
        %endif
	</div>
</div>