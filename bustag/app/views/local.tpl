% rebase('base.tpl', title='本地文件', path=path)
% curr_page = page_info[2]

<div class="container">
 <div class="row py-3">
	<div class="col-12">
		<ul class="nav nav-tabs">
        <li class="nav-item">
			<a class="nav-link {{'active' if path=='/local' else ''}}" href="/local">本地文件</a>
		</li>
        <li class="nav-item">
			<a class="nav-link {{'active' if path=='/local_fanhao' else ''}}" href="/local_fanhao">上传番号</a>
		</li>
		<li class="nav-item">
		</li>
		</ul>
	</div>
 </div>
%#generate list of rows of items
%for local_item in items:
	<div class="row py-3">
		<div class="col-12 col-md-4">
		<img class="img-fluid img-thumbnail coverimg" alt="点击放大" src={{local_item.item.cover_img_url}}>
		</div>

			<div class="col-7 col-md-5">
			<div class="small text-muted">发行日期: {{local_item.item.release_date}}</div>
			<div class="small text-muted">上次观看: {{local_item.last_view_date}}</div>
			<div class="small text-muted">观看次数观看: {{local_item.view_times}}</div>
			<h6>{{local_item.item.fanhao}} </h6>
			<a href="{{local_item.item.url}}" target="_blank"> {{local_item.item.title[:30]}} </a>
			<div>
			% for t in local_item.item.tags_dict['genre']:
			<span class="badge badge-primary">{{t}}</span>
			% end
			</div>
			<div>
			% for t in local_item.item.tags_dict['star']:
			<span class="badge badge-warning">{{t}}</span>
			% end
			</div>

			</div>
		<div class="col-5 col-md-3  align-self-center">
<a class="btn btn-primary" target="_blank" href="/local_play/{{local_item.id}}" role="button">播放</a>
		</div>
	</div>
%end
% include('pagination.tpl', page_info=page_info)

</div>