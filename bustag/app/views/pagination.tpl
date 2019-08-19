% curr_page = page_info[2]
% max_page = page_info[1]
% total_items = page_info[0]
<div class="row">
	<div class="col-12 text-center">
	<h6>
	<span>共 {{total_items}}条</span>
	% if curr_page != 1:
	<a href="?page=1&like={{like}}"> 第一页</a>
	% end
	% if curr_page > 1:
	<a href="?page={{curr_page - 1}}&like={{like}}"> 上一页</a>
	% end
	第{{curr_page}}页
	% if curr_page < max_page:
	 <a href="?page={{curr_page + 1}}&like={{like}}">下一页</a>
	% end
	% if curr_page != max_page:
	<a href="?page={{max_page}}&like={{like}}">最后页</a>
	% end
	</h6>
	</div>
</div>