% rebase('base.tpl', title='本地', path=path, msg=msg)

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

<form action="" method="post">
	<div class="row py-3">
		<div class="col-12 ">
		<div class="form-check">
			<input class="form-check-input" type="checkbox" value="1" id="tag_like" name="tag_like">
			<label class="form-check-label" for="tag_like">
				全部打标为喜欢
			</label>
		</div>
		  <div class="form-group py-3">
			<label for="fanhao">每行格式: 番号(XXX-123),URL(可省略, 本地文件无效, 须为Plex等服务器视频URL)</label>
			<textarea class="form-control" id="fanhao" name="fanhao" rows="20"></textarea>
		  </div>
		<div class="text-center">
		<button type="submit" name="submit" class="btn btn-primary mx-2" value="1">提交</button>
		<button type="submit" name="submit" class="btn btn-danger" value="0">重置</button>
		</div>
		</div>
	</div>
</form>

</div>
