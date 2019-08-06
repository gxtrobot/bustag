% rebase('base.tpl', title='打标')
% curr_page = page_info[2]
% max_page = page_info[1]
<div class="container">
 <div class="row py-3">
	<div class="col-12">
		<ul class="nav nav-tabs">
		<li class="nav-item">
			<a class="nav-link {{'active' if like is None else ''}}" href="?">未打标的</a>
		</li>
		<li class="nav-item">
			<a class="nav-link {{'active' if like==1 else ''}}" href="?like=1">喜欢</a>
		</li>
		<li class="nav-item">
			<a class="nav-link {{'active' if like==0 else ''}}" href="?like=0">不喜欢</a>
		</li>
		</ul>
	</div>
</div>
%#generate list of rows of items 
%for item in items:
<form action="/tag/{{item.id}}?page={{curr_page}}" method="post">
	<div class="row py-3">
		<div class="col-12 col-sm-3">
		<img src={{item.cover_img_url}} width="200">
		</div>
			
			<div class="col-6 col-sm-5">
			<p class="small text-muted">{{item.add_date}}</p>
			<h6>{{item.fanhao}} </h6>
			<a href="{{item.url}}" target="_blank"> {{item.title}} </a>
			<div>
			<span class="badge badge-primary">高清</span>
			<span class="badge badge-primary">高画质</span>
			</div>
		
			</div>
		<div class="col-6 col-sm-4  align-self-center">
		<button type="submit" name="submit" class="btn btn-primary btn-sm" value="1">喜欢</button>
		<button type="submit" name="submit" class="btn btn-danger btn-sm" value="0">不喜欢</button>
		</div>
	</div>
	</form>
%end
<div class="row">
	<div class="col-12 text-center">
	<a href="?page=1"> 第一页</a>
	% if curr_page > 1:
	<a href="?page={{curr_page - 1}}"> 上一页</a>
	% end
	% if curr_page < max_page:
	 <a href="?page={{curr_page + 1}}">下一页</a>
	% end
	<a href="?page={{max_page}}">最后页</a>
	</div>
</div>
</div>