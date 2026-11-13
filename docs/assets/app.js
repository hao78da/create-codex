
(function(){
  var bar=document.querySelector('.searchbar input');
  var cards=[].slice.call(document.querySelectorAll('#list .card'));
  var btns=[].slice.call(document.querySelectorAll('.filters button'));
  var empty=document.querySelector('.empty-msg');
  var cat='all', q='';
  var mod=(new URLSearchParams(location.search)).get('mod')||'';
  var MODS={create:'\u673a\u68b0\u52a8\u529b'};
  function apply(){
    var n=0;
    cards.forEach(function(c){
      var okc=(cat==='all'||c.dataset.cat===cat);
      var okm=!mod||c.dataset.mod===mod;
      var okq=!q||c.dataset.k.indexOf(q)>-1;
      var show=okc&&okq&&okm;
      c.style.display=show?'':'none';
      if(show)n++;
    });
    if(empty)empty.style.display=n?'none':'block';
  }
  (function(){
    if(!mod) return;
    var mb=document.getElementById('modbar'), mn=document.getElementById('modname');
    if(mn) mn.textContent=MODS[mod]||mod;
    if(mb) mb.hidden=false;
  })();
  btns.forEach(function(b){b.addEventListener('click',function(){
    btns.forEach(function(x){x.classList.remove('on')});
    b.classList.add('on'); cat=b.dataset.cat; apply();
  })});
  if(bar){bar.addEventListener('input',function(){q=bar.value.trim().toLowerCase();apply();});}
  (function(){
    var h=location.hash;
    if(h.indexOf('#cat-')===0){
      var c=h.slice(5);
      btns.forEach(function(b){ if(b.dataset.cat===c){ b.click(); } });
    }
  })();
  document.querySelectorAll('.copyid').forEach(function(el){
    el.addEventListener('click',function(){
      var t=el.textContent.trim();
      var done=function(){el.classList.add('ok');el.textContent='已复制';
        setTimeout(function(){el.textContent=t;el.classList.remove('ok')},1200);};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,done)}
      else{var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();
        try{document.execCommand('copy')}catch(e){}document.body.removeChild(ta);done();}
    });
  });
})();
