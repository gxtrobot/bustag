% rebase('base.tpl', title='打标')
<div class="container">
 <div class="row py-3">
	<div class="col-12">
		<ul class="nav nav-tabs">
		<li class="nav-item">
			<a class="nav-link active" href="#">喜欢</a>
		</li>
		<li class="nav-item">
			<a class="nav-link" href="#">不喜欢</a>
		</li>
		<li class="nav-item">
			<a class="nav-link" href="#">全部</a>
		</li>
		</ul>
	</div>
</div>
%#generate list of rows of items 
%for item in items:
<form action="/tag/{{item.id}}" method="post">
	<div class="row py-3">
		<div class="col-3">
		<img src={{1}} width="150">
		</div>
			<div class="col-5">
			{{item.title}}
			<div>
			<span class="badge badge-primary">高清</span>
			<span class="badge badge-primary">高画质</span>
			</div>
		
			</div>
		<div class="col-4 align-self-center">
		<button type="submit" name="submit" class="btn btn-primary btn-sm" value="1">喜欢</button>
		<button type="submit" name="submit" class="btn btn-danger btn-sm" value="0">不喜欢</button>
		</div>
	</div>
	</form>
%end
</div>