<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
	<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">
	
    <title>{{title or '首页'}}</title>
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
        <a class="nav-link" href="/">推荐 <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/tagit">打标</a>
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

{{!base}}

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
   	<script type="text/javascript" src="/static/js/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/popper.min.js"></script>
	<script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
  </body>
</html>

