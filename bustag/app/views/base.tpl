<%print(path)%>
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <link rel="shortcut icon" type="image/ico" href="/static/images/favicon.ico"/>

    <!-- Bootstrap CSS -->
	<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">

	<link rel="stylesheet" type="text/css" href="/static/css/bustag.css">

    <title>{{title or ''}}</title>
  </head>
  <body>

<div class="container">
  <div class="row">
    <div class="col-12">
	<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="/"><img src="/static/images/logo.png" width="140"></a>
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
      <li class="nav-item {{ 'active' if path=='/local' else ''}}">
        <a class="nav-link" href="/local">本地</a>
      </li>
      <li class="nav-item {{ 'active' if path=='/model' else ''}}">
        <a class="nav-link" href="/model">模型</a>
      </li>
      <li class="nav-item {{ 'active' if path=='/load_db' else ''}}">
        <a class="nav-link" href="/load_db">数据</a>
      </li>
      <li class="nav-item {{ 'active' if path=='/about' else ''}}">
        <a class="nav-link" href="/about">关于</a>
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
  % if defined('msg') and msg != '':
    <div class="alert alert-success" role="alert">
    {{msg}}
    </div>
  % end

  % if defined('errmsg') and errmsg != '':
    <div class="alert alert-danger" role="alert">
    {{errmsg}}
    </div>
  % end
    </div>
  </div>
</div>

{{!base}}
<% from bustag import __version__ %>
<footer class="my-3">
  <div class="container">
  <div class="col">
    <p class="text-center">
    <span class="badge badge-pill badge-info">version : {{__version__}}</span>
  </p>
  <p class="text-center">
  Developed by 凤凰山@2019 <a href="https://github.com/gxtrobot/bustag" target="_blank">github</a>
  </p>
  </div>
</div>

<!-- The Modal -->
<div class="modal fade" id="imagemodal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-body">
      	<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
        <img id="imglarge" src="" class="imagepreview" style="width: 100%;" >
      </div>
    </div>
  </div>
</div>

</footer>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
   	<script type="text/javascript" src="/static/js/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/popper.min.js"></script>
	<script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="/static/js/bustag.js"></script>
  </body>
</html>

