function toggle_display(){
  el = document.querySelector('.card');
  el2 = document.querySelector('.translation');

  if(el2.style.visibility == 'hidden'){
    el.style.visibility = 'hidden';
    el2.style.visibility = 'visible';
  }
  else{
    el.style.visibility = 'visible';
    el2.style.visibility = 'hidden';
  }
}
