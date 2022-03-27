// var code_ide = `%matplotlib inline\nfrom aian.main import AIan; from IPython.display import Javascript, display; aian = AIan(\'aian2.cfg\');aian.start(); display(Javascript("hide_aian()"))`;
var code_ide = 'import os; os.chdir("/opt/code/aiduez"); from app import Aian; aian = Aian(); aian.start()'

var code_exam = "from aian.exam.aibasic import AIBasicExam; exam = AIBasicExam(aian); exam(); display(Javascript(\"hide_exam()\"))"

// Hide toolbar. 2021-11-25
// $('#maintoolbar').hide()

function check_refresh(keyword) {
  var inputs = $('div.cell.code_cell').find('div.output');
  count = 0
  inputs.each(function(index, item) {
    if(item.innerText.search(keyword) >= 0) {
      count += 1;
    } 
  });

  if(count == 0) {
    Jupyter.notebook.kernel.restart();
  }
}

function hide_code(code) {
  var inputs = $('div.cell.code_cell').find('div.input');
  inputs.each(function(index, item) {
    if(item.innerText.search(code) >= 0) {
      item.style.display = 'none';
    }
  });
}

function delete_code(code) {
  var cells = IPython.notebook.get_cells();
  cells.forEach(function(cell) {
    if(cell.get_text().includes(code)) {
      var index = IPython.notebook.find_cell_index(cell);
      IPython.notebook.delete_cell(index);
    }
  });
}

function execute_python(code) {
  cellTop = IPython.notebook.insert_cell_above('code', 0).set_text(code);
  var cells = IPython.notebook.get_cells();
  cells.forEach(function(cell) {
    if(cell.get_text().includes(code)) {
      var index = IPython.notebook.find_cell_index(cell);
      IPython.notebook.get_cells()[index].execute();
    }
  });
}

// var hide_aian = () => {return hide_code('aian.main');}
var hide_aian = () => {return hide_code('Aian');}

var hide_exam = () => {return hide_code('AIBasicExam');}

if ($(IPython.toolbar.selector.concat(' > #AIDU ez')).length == 0) {
  IPython.toolbar.add_buttons_group([{
    'label'   : 'AIDU ez',
    'icon'    : 'fa fa-angle-double-down',
    'callback': function() {
      Jupyter.notebook.kernel.restart();
    }}], 'AIDU ez');
}


function load_ide_module() {
  delete_code(code_ide);
  delete_code(code_exam);

  execute_python(code_ide);
}

function on_load_execute(event) {
  console.log('on_load_execute | start')
  if(IPython.notebook.kernel &&
     IPython.notebook.kernel.is_connected()) {

    load_ide_module()
  }

  IPython.notebook.save_checkpoint();
  IPython.notebook.save_notebook();

  console.log('on_load_execute | end')
  return on_load_execute;
}

$([IPython.events]).on('kernel_ready.Kernel kernel_created.Session', on_load_execute);

window.onbeforeunload = function(e) {
  Jupyter.notebook.kernel.kill();
};

window.unload = function(e) {
  Jupyter.notebook.kernel.kill();
}

// var body = document.querySelector('body');
// body.setAttribute('oncopy', 'return false');
// body.setAttribute('oncut', 'return false');
// body.setAttribute('onpaste', 'return false');
// body.setAttribute('onselectstart', 'return false');



IPython.OutputArea.prototype._should_scroll = function(lines) {
  return false;
}