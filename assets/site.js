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
  // forms: browser checks required fields, then we send to FormSubmit as JSON (their documented AJAX format).
  // If that fails (network, CORS, slow service), fall back to a normal form post that returns to this page.
  var PHONE='<a href="tel:097728340" dir="ltr" class="tel">09-772-8340</a>';
  document.querySelectorAll('.lead-form').forEach(function(f){
    var ok=f.querySelector('.form-ok'),b=f.querySelector('[type=submit]');
    function say(h,bad){ok.innerHTML=h;ok.classList.toggle('bad',!!bad);ok.hidden=false;ok.scrollIntoView({block:'nearest'})}
    if(/[?&]sent=1/.test(location.search))say('ההודעה נשלחה בהצלחה !');
    f.addEventListener('invalid',function(){say('נא למלא את השדות המסומנים ולסמן אישור לתקנון ולמדיניות הפרטיות',true)},true);
    function classic(){
      var next=document.createElement('input');next.type='hidden';next.name='_next';
      next.value=location.origin+location.pathname+'?sent=1';f.appendChild(next);
      f.action=f.action.replace('/ajax/','/');HTMLFormElement.prototype.submit.call(f);
    }
    f.addEventListener('submit',function(e){
      e.preventDefault();b.disabled=true;var label=b.textContent;b.textContent='שולח...';ok.hidden=true;
      var data={};new FormData(f).forEach(function(v,k){data[k]=v});
      var ctl=window.AbortController?new AbortController():null;var timer=setTimeout(function(){ctl&&ctl.abort()},10000);
      fetch(f.action,{method:'POST',body:JSON.stringify(data),headers:{'Content-Type':'application/json',Accept:'application/json'},signal:ctl&&ctl.signal})
        .then(function(r){return r.json()}).then(function(j){
          clearTimeout(timer);b.disabled=false;b.textContent=label;
          if(j.success===true||j.success==='true'){f.reset();say('ההודעה נשלחה בהצלחה !');return}
          if(/activat/i.test(j.message||'')){say('הטופס ממתין להפעלה: נשלח מייל אישור לכתובת של העסק');return}
          say('השליחה נכשלה. אפשר להתקשר אלינו: '+PHONE,true)})
        .catch(function(){clearTimeout(timer);classic()});
    });
  });
})();
