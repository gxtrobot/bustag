% rebase('base.tpl', title='本地', path=path, msg=msg)

<div class="container">
 <div class="row py-3">
	<div class="col-12">
		<ul class="nav nav-tabs">
        <li class="nav-item">
			<a class="nav-link" href="/local">本地文件</a>
		</li>
        <li class="nav-item">
			<a class="nav-link" href="/local_fanhao">上传番号</a>
		</li>
		<li class="nav-item">
		</li>
		</ul>
	</div>
 </div>

<form action="" method="post">
	<div class="row py-3">
		<div class="col-12 ">
		<form>
		  <div class="form-group">
			<label for="fanhao">每行格式: 番号,URL(本地文件无效, 须为Plex等服务器视频URL)</label>
			<textarea class="form-control" id="fanhao" name="fanhao" rows="20"></textarea>
		  </div>
		<div class="text-center">
		<button type="submit" name="submit" class="btn btn-primary mx-2" value="1">提交</button>
		<button type="submit" name="submit" class="btn btn-danger" value="0">重置</button>
		</div>
		</form>
		</div>
	</div>
</form>

</div>