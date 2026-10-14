(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nav = document.getElementById('nav'), burger = document.getElementById('burger');

  // mobile menu
  if (burger) burger.addEventListener('click', function(){
    var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o);
  });
  document.querySelectorAll('#menu a').forEach(function(a){
    a.addEventListener('click', function(){ nav.classList.remove('open'); if (burger) burger.setAttribute('aria-expanded', false); });
  });

  // services dropdown: hover on desktop (CSS), click/keyboard everywhere
  document.querySelectorAll('.has-dd').forEach(function(li){
    var btn = li.querySelector('.dd-toggle');
    btn.addEventListener('click', function(e){
      e.preventDefault();
      var o = li.classList.toggle('open'); btn.setAttribute('aria-expanded', o);
    });
    li.addEventListener('keydown', function(e){
      if (e.key === 'Escape'){ li.classList.remove('open'); btn.setAttribute('aria-expanded', false); btn.focus(); }
    });
    document.addEventListener('click', function(e){
      if (!li.contains(e.target)){ li.classList.remove('open'); btn.setAttribute('aria-expanded', false); }
    });
  });

  // scroll reveal: only items currently below the fold start hidden, so the first frame is complete
  var items = [].slice.call(document.querySelectorAll('.reveal'));
  if (!reduce && 'IntersectionObserver' in window){
    var vh = window.innerHeight;
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.remove('pre'); io.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -8% 0px'});
    items.forEach(function(el){
      if (el.getBoundingClientRect().top > vh){
        el.classList.add('pre');
        var sib = el.parentElement ? [].indexOf.call(el.parentElement.children, el) : 0;
        el.style.transitionDelay = (Math.min(sib, 6) * 70) + 'ms';
        io.observe(el);
      }
    });
  }

  // process timeline, reading progress, table-of-contents highlight
  var steps = document.getElementById('steps'), fill = document.getElementById('fill');
  var stepEls = steps ? steps.querySelectorAll('.step') : [];
  var bar = document.getElementById('progress');
  var article = document.querySelector('.article');
  var tocLinks = [].slice.call(document.querySelectorAll('.toc a'));
  var tocTargets = tocLinks.map(function(a){ return document.getElementById(a.getAttribute('href').slice(1)); });
  function onScroll(){
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 10);
    var mid = window.innerHeight * 0.6;
    if (steps){
      var r = steps.getBoundingClientRect();
      fill.style.height = Math.max(0, Math.min(r.height - 20, mid - r.top)) + 'px';
      stepEls.forEach(function(s){ s.classList.toggle('on', s.getBoundingClientRect().top + 28 < mid); });
    }
    if (bar && article){
      var a = article.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (window.innerHeight * 0.3 - a.top) / Math.max(1, a.height - window.innerHeight * 0.4)));
      bar.style.transform = 'scaleX(' + p + ')';
    }
    if (tocLinks.length){
      var cur = 0;
      tocTargets.forEach(function(t, i){ if (t && t.getBoundingClientRect().top < window.innerHeight * 0.35) cur = i; });
      tocLinks.forEach(function(l, i){ l.classList.toggle('active', i === cur); });
    }
  }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

  // forms (not wired to a backend yet)
  document.querySelectorAll('form.lead-form').forEach(function(f){
    var ok = f.querySelector('.form-ok'), msg = f.getAttribute('data-ok') || 'We received your request and will be in touch soon.';
    f.addEventListener('submit', function(e){
      e.preventDefault();
      var name = f.querySelector('[name=name]'), email = f.querySelector('[name=email]');
      if (!name.value.trim()){ ok.hidden = false; ok.textContent = 'Please add your name so we know who to contact.'; name.focus(); return; }
      if (!/^\S+@\S+\.\S+$/.test(email.value)){ ok.hidden = false; ok.textContent = 'Please enter a valid email address, like name@email.com.'; email.focus(); return; }
      ok.hidden = false; ok.textContent = 'Thanks, ' + name.value.trim().split(' ')[0] + '. ' + msg; f.reset();
    });
  });

  // hero flake-floor canvas
  var c = document.getElementById('flakes');
  if (c){
    var ctx = c.getContext('2d'), flakes = [], W, H, dpr;
    var cols = ['#ff6a13','#ff9a52','#ffd2b0','#3b2c22','#c9b9a6','#ffffff'];
    var size = function(){
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = c.clientWidth; H = c.clientHeight; c.width = W*dpr; c.height = H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
      var n = Math.round(W*H/2600); flakes = [];
      for (var i=0;i<n;i++) flakes.push({x:Math.random()*W,y:Math.random()*H,s:2+Math.random()*6,a:Math.random()*6.28,v:(Math.random()-.5)*.004,dy:.05+Math.random()*.18,col:cols[(Math.random()*cols.length)|0],k:3+((Math.random()*3)|0)});
    };
    var draw = function(){
      ctx.clearRect(0,0,W,H);
      for (var i=0;i<flakes.length;i++){
        var f = flakes[i];
        if (!reduce){ f.a += f.v; f.y += f.dy; if (f.y > H+10){ f.y = -10; f.x = Math.random()*W; } }
        ctx.save(); ctx.translate(f.x,f.y); ctx.rotate(f.a); ctx.fillStyle = f.col; ctx.beginPath();
        for (var j=0;j<f.k;j++){ var ang = j/f.k*6.28, rr = f.s*(.6+.4*((j*7)%3)/2); ctx.lineTo(Math.cos(ang)*rr, Math.sin(ang)*rr); }
        ctx.closePath(); ctx.fill(); ctx.restore();
      }
      if (!reduce) requestAnimationFrame(draw);
    };
    size(); draw();
    var rt; window.addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(function(){ size(); if (reduce) draw(); }, 150); });
  }
})();
