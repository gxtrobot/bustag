<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
	<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">
	
    <title>Hello, world!</title>
  </head>
  <body>

<div class="container">
  <div class="row">
    <div class="col-12">
	<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#"></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="#">推荐 <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">打标</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">其他</a>
      </li>
    </ul>
  </div>
</nav>
    </div>
  </div>
</div>
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
	<div class="row py-3">
		<div class="col-3">
		<img src={{item.cover_img_url}} width="150">
		</div>
			<div class="col-5">
			{{item.title}}
			<div>
			<span class="badge badge-primary">高清</span>
			<span class="badge badge-primary">高画质</span>
			</div>
		
			</div>
		<div class="col-4 align-self-center">
		<button type="button" class="btn btn-primary btn-sm">喜欢</button>
		<button type="button" class="btn btn-danger btn-sm">不喜欢</button>
		</div>
	</div>
%end
</div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
   	<script type="text/javascript" src="/static/js/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/popper.min.js"></script>
	<script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
  </body>
</html>

