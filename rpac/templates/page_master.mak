<%inherit file="rpac.templates.master"/>

<%
  from repoze.what.predicates import not_anonymous, in_group, has_permission
%>

<%def name="extTitle()">r-pac - Master</%def>

<div class="main-div">
	<div id="main-content">
    	    <div class="block">
    	    	<a href="/master/index?t=Product"><img src="/images/product.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Product">Item</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=Size"><img src="/images/size.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Size">Size</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=COO"><img src="/images/coo.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=COO">Country</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=GarmentPart"><img src="/images/part.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=GarmentPart">Garment Parts</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=Fibers"><img src="/images/fibers.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Fibers">Fabrics</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=Care"><img src="/images/care.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Care">Care Instructions</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=Division"><img src="/images/div.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Division">Division</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=Category"><img src="/images/category.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Category">Category</a></p>
    	    </div>
    	    <div class="block">
    	    	<a href="/master/index?t=Brand"><img src="/images/brand.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Brand">Brand</a></p>
    	    </div>
	</div>
</div>