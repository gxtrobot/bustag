% rebase('base.tpl', title='推荐', path=path)
% curr_page = page_info[2]
% max_page = page_info[1]

<div class="container">
 <div class="row py-3">
	<div class="col-12">
		<ul class="nav nav-tabs">
		<li class="nav-item">
			<a class="nav-link {{'active' if like==1 else ''}}" href="?like=1">喜欢</a>
		</li>
		<li class="nav-item">
			<a class="nav-link {{'' if like==1 else 'active'}}" href="?like=0">不喜欢</a>
		</li>
		<li class="nav-item">
		</li>
		</ul>
	</div>
</div>
%#generate list of rows of items 
%for item in items:
<form action="/correct/{{item.id}}?page={{curr_page}}&like={{like}}" method="post">
	<div class="row py-3">
		<div class="col-12 col-md-4">
		<img class="img-fluid img-thumbnail" src={{item.cover_img_url}}>
		</div>
			
			<div class="col-7 col-md-5">
			<div class="small text-muted">id: {{item.id}}</div>
			<div class="small text-muted">发行日期: {{item.release_date}}</div>
			<div class="small text-muted">添加日期: {{item.add_date}}</div>
			<h6>{{item.fanhao}} </h6>
			<a href="{{item.url}}" target="_blank"> {{item.title[:30]}} </a>
			<div>
			% for t in item.tags_dict['genre']:
			<span class="badge badge-primary">{{t}}</span>
			% end
			</div>
			<div>
			% for t in item.tags_dict['star']:
			<span class="badge badge-warning">{{t}}</span>
			% end
			</div>
		
			</div>
		<div class="col-5 col-md-3  align-self-center">
		<button type="submit" name="submit" class="btn btn-primary mx-2" value="1">正确</button>
		<button type="submit" name="submit" class="btn btn-danger" value="0">错误</button>
		</div>
	</div>
	</form>
%end
<div class="row">
	<div class="col-12 text-center">
	<a href="?page=1&like={{like}}"> 第一页</a>
	% if curr_page > 1:
	<a href="?page={{curr_page - 1}}&like={{like}}"> 上一页</a>
	% end
	% if curr_page < max_page:
	 <a href="?page={{curr_page + 1}}&like={{like}}">下一页</a>
	% end
	<a href="?page={{max_page}}&like={{like}}">最后页</a>
	</div>
</div>
</div>