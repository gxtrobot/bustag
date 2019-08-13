<%print(path)%>
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
	<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">
	
    <title>{{title or ''}}</title>
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
      <li class="nav-item {{ 'active' if path=='/' else ''}}">
        <a class="nav-link" href="/">推荐 <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item {{ 'active' if path=='/tagit' else ''}}">
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

<footer class="my-3">
  <div class="container">
  <div class="col">
  <p class="text-center">
  Developed by 凤凰山@2019 <a href="https://github.com/gxtrobot/bustag" target="_blank">github</a>
  </p>
  </div>
</div>
</footer>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
   	<script type="text/javascript" src="/static/js/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/popper.min.js"></script>
	<script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
  </body>
</html>

