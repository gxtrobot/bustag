% rebase('base.tpl', title='数据', path=path, msg=msg)

<div class="container">
 <div class="row py-3">
 <div class="col-10 offset-1 ">
		<ul class="nav nav-tabs">
        <li class="nav-item">
			<a class="nav-link {{'active' if path=='/load_db' else ''}}" href="/load_db">导入打标数据</a>
		</li>
		<li class="nav-item">
		</li>
		</ul>
	</div>
 </div>

<form action="" method="post" enctype="multipart/form-data">
	<div class="row py-3">
 <div class="col-10 offset-1 ">
    <div class="form-group">
        <label for="dbfile">选择要导入的数据库文件(*.db)</label>
        <input type="file" class="form-control-file" id="dbfile" name="dbfile">
    </div>

		<div class="text-center">
		<button type="submit" name="submit" class="btn btn-primary mx-2 my-3" value="1">提交</button>
		</div>
		</div>
	</div>
</form>

</div>
