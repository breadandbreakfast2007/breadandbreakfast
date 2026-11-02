(function(){
  var root=document.documentElement;
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  // mobile nav
  var t=document.querySelector('.menu-toggle'),n=document.getElementById('site-nav');
  if(t)t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)});
  // cookie notice
  var c=document.getElementById('cookie');
  if(c&&!get('cookieOk')){c.hidden=false;document.getElementById('cookie-ok').onclick=function(){set('cookieOk','1');c.hidden=true}}
  // accessibility toolbar
  var toggles=['contrast','mono','readable','links','headings','cursor','motion'];
  var st={};try{st=JSON.parse(get('a11y')||'{}')}catch(e){}
  function apply(){
    toggles.forEach(function(k){root.classList.toggle('a11y-'+k,!!st[k]);
      var b=document.querySelector('[data-a11y="'+k+'"]');if(b)b.setAttribute('aria-pressed',!!st[k])});
    root.style.fontSize=(st.font||100)+'%';set('a11y',JSON.stringify(st));
  }
  var btn=document.querySelector('.a11y-toggle'),panel=document.getElementById('a11y-panel');
  btn.addEventListener('click',function(){panel.hidden=!panel.hidden;btn.setAttribute('aria-expanded',!panel.hidden)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!panel.hidden){panel.hidden=true;btn.focus()}});
  panel.addEventListener('click',function(e){var a=e.target.getAttribute('data-a11y');if(!a)return;
    if(a==='font-up')st.font=Math.min((st.font||100)+10,160);
    else if(a==='font-down')st.font=Math.max((st.font||100)-10,80);
    else if(a==='reset')st={};else st[a]=!st[a];apply()});
  apply();
  // forms: submit via fetch (Web3Forms), show success text
  document.querySelectorAll('.lead-form').forEach(function(f){f.addEventListener('submit',function(e){
    e.preventDefault();var ok=f.querySelector('.form-ok'),b=f.querySelector('[type=submit]');b.disabled=true;
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}})
      .then(function(r){return r.json()}).then(function(j){if(!j.success)throw 0;f.reset();ok.textContent='ההודעה נשלחה בהצלחה !';ok.hidden=false})
      .catch(function(){ok.textContent='השליחה נכשלה. אפשר להתקשר אלינו: 09-772-8340';ok.hidden=false})
      .finally(function(){b.disabled=false});
  })});
})();
