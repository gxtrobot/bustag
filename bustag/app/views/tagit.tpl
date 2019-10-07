% rebase('base.tpl', title='打标', path=path)
% curr_page = page_info[2]
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
% i = 1
%for item in items:
<form id="form-{{i}}" action="/tag/{{item.fanhao}}?page={{curr_page}}&like={{like}}" method="post">
	<div class="row py-3">
		<div class="col-12 col-md-4">
		<img class="img-fluid img-thumbnail coverimg" src={{item.cover_img_url}}>
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
		<input type=hidden name="formid" value="form-{{i}}">
% if like is None or like == 0:
		<button type="submit" name="submit" class="btn btn-primary btn-sm" value="1">喜欢</button>
% end
% if like is None or like == 1:
		<button type="submit" name="submit" class="btn btn-danger btn-sm" value="0">不喜欢</button>
% end
		</div>
	</div>
	</form>
% i = i + 1
%end
% include('pagination.tpl', page_info=page_info)

</div>