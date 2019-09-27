% rebase('base.tpl', title='其他', path=path)

<div class="container">
 <div class="row py-3">
 <div class="col-10 offset-1 ">
    <div class="accordion" id="accordionExample">
  <div class="card">
    <div class="card-header" id="headingOne">
      <h2 class="mb-0">
        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
          训练模型
        </button>
      </h2>
    </div>

    <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordionExample">
        <div class="card-body">
        <h5 class="card-title">重新训练模型</h5>
        <p class="card-text">重新使用系统所有用户打标数据训练模型, 当打标数据增多后, 可以重新训练模型, 提高模型预测效果</p>
        <a href="/do-training" class="btn btn-primary">开始训练</a>
        </div>
        <div class="card-header">
           <h6> 当前模型数据 </h6>
        </div>
        % if defined('error_msg') and error_msg is not None:
        <p class="card-text text-danger">{{error_msg}} </a>
        % end
        % if model_scores is not None:
        <ul class="list-group list-group-flush">
            <li class="list-group-item">准确率: {{model_scores['precision']}}</li>
            <li class="list-group-item">覆盖率: {{model_scores['recall']}}</li>
            <li class="list-group-item">综合评分(越高越好): {{model_scores['f1']}}</li>
        </ul>
        % else:
        <div class="card-body">
           还没有训练过模型.
        </div>
        % end
        </div>
    </div>
  </div>
  <div class="card">
    <div class="card-header" id="headingTwo">
      <h2 class="mb-0">
        <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">

        </button>
      </h2>
    </div>
    <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionExample">
      <div class="card-body">
        Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.
      </div>
    </div>
  </div>
 </div>
 </div>
</div>
</div>