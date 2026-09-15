/* Démo Corrext · Fast translation : données réelles récoltées dans l'application le 14 septembre 2026 (moteurs nommables uniquement).
   Partagé par la page d'accueil et la page Fast translation. Une seule instance de cadre #cx par page. */
(function(){
  var EX={
    co:{label:"Contrat · art. 104 CO",
      src:"Le débiteur en demeure doit des intérêts moratoires au taux de 5% l'an, conformément à l'art. 104 al. 1 CO, sans qu'une mise en demeure formelle soit nécessaire lorsqu'un terme a été convenu.",
      def:"de",
      out:{
        de:{main:"Der säumige Schuldner schuldet gemäss Art. 104 Abs. 1 OR Verzugszinsen von 5 % pro Jahr; eine förmliche Mahnung ist nicht erforderlich, wenn ein Termin vereinbart wurde.",
            alt:[{e:"DeepL Pro",t:"Der in Verzug befindliche Schuldner schuldet gemäss Art. 104 Abs. 1 OR Verzugszinsen in Höhe von 5 % pro Jahr, ohne dass eine förmliche Mahnung erforderlich ist, sofern eine Frist vereinbart wurde."},
                 {e:"Azure OpenAI - GPT",t:"Der Schuldner im Verzug schuldet Verzugszinsen zum Satz von 5% pro Jahr gemäss Art. 104 Abs. 1 OR, ohne dass eine förmliche Mahnung erforderlich ist, wenn eine Frist vereinbart wurde."}]},
        it:{main:"Il debitore in mora deve gli interessi moratori al tasso del 5 per cento annuo secondo l'articolo 104 capoverso 1 CO; non è necessaria una diffida formale se era stato fissato un termine.",
            alt:[{e:"DeepL Pro",t:"Il debitore inadempiente è tenuto a corrispondere interessi di mora al tasso del 5% annuo, ai sensi dell'art. 104, comma 1, CO, senza che sia necessaria una formale messa in mora qualora sia stato concordato un termine."},
                 {e:"Azure OpenAI - GPT",t:"Il debitore in mora deve interessi moratori al tasso del 5% annuo, conformemente all'art. 104 cpv. 1 CO, senza che sia necessaria una costituzione in mora formale quando è stato convenuto un termine."}]}
      },
      lookup:{q:"Verzugszins",l1:"German",l2:"French",count:"324 results",rows:[
        {a:"Kann die Zahlstelle den fehlenden Betrag zuzüglich Verzugszins nicht mehr der betroffenen Person nachbelasten, zum Beispiel weil diese nicht mehr ihre Kundin ist, so ist die Zahlstelle zur Leistung des fehlenden Betrages zuzüglich Verzugszins verpflichtet.",b:"Si l'agent payeur ne peut plus prélever ultérieurement le montant manquant avec l'intérêt moratoire, notamment parce que la personne concernée n'est plus cliente de son établissement, il reste tenu de verser le montant correspondant.",dom:"OTHER",src:"Feuille Fédérale/Bundesblatt - Source: Feuille Fédérale/Bundesblatt - Data Set: Neur.on"},
        {a:"Art. 24 Verzugszins Auf Einmalzahlungen, abgeltenden Steuern und Abgeltungszahlungen, die der ESTV verspätet überwiesen werden, ist ohne Mahnung ein Verzugszins nach Ablauf der in diesem Gesetz festgelegten Fristen bis zum Datum des Eingangs geschuldet.",b:"5373 Art. 24 Intérêt moratoire Un intérêt moratoire est dû sans sommation dès l'échéance des délais fixés dans la présente loi sur les paiements uniques, les impôts libératoires et les paiements libératoires virés en retard à l'AFC et jusqu'à réception des sommes dues.",dom:"TAX LAW & CUSTOMS",src:"SIF FF20125365 Bundesgesetz-über-die-internationale-Quellenbesteuerung-IQG - Source: fedlex.admin.ch - Data Set: Neur.on"}],
        mark:["Verzugszins","intérêt moratoire","Intérêt moratoire"]},
      reph:{def:"Le débiteur en <u>retard</u> doit <u>verser</u> des intérêts moratoires au taux de 5 % <u>par</u> an, conformément à l’art. 104 al. 1 CO, sans qu’une mise en demeure formelle soit nécessaire <u>dès lors qu’</u>un terme a été <u>fixé</u>.",
            simp:"<u>Celui qui ne paie pas à temps</u> doit <u>verser</u> des intérêts <u>de retard de</u> 5% <u>par</u> an, <u>d'après</u> l'art. 104 al. 1 CO. <u>Une demande de paiement officielle n'est pas obligatoire si</u> une <u>date limite</u> a été <u>fixée</u>."}
    },
    lb:{label:"Banque · art. 47 LB",
      src:"L'établissement assujetti veille au respect du secret bancaire au sens de l'art. 47 LB et met en œuvre les exigences de la FINMA en matière de lutte contre le blanchiment d'argent.",
      def:"en",
      out:{
        en:{main:"The subject institution ensures that banking secrecy is observed pursuant to Article 47 BA and implements the requirements of FINMA regarding combating money laundering.",
            alt:[{e:"DeepL Pro",t:"The regulated institution ensures compliance with banking secrecy as defined in Article 47 of the Banking Act and implements FINMA's anti-money laundering requirements."},
                 {e:"Azure OpenAI - GPT",t:"The supervised institution ensures compliance with banking secrecy as defined in Art. 47 of the Banking Act and implements FINMA's requirements regarding anti-money laundering."}]},
        it:{main:"L'istituto soggetto all'obbligo di vigilanza provvede affinché sia rispettato il segreto bancario ai sensi dell'articolo 47 LB e attua i requisiti della FINMA per quanto concerne la lotta contro il riciclaggio di denaro.",
            alt:[{e:"DeepL Pro",t:"L'istituto soggetto a vigilanza garantisce il rispetto del segreto bancario ai sensi dell'art. 47 LB e attua i requisiti della FINMA in materia di lotta contro il riciclaggio di denaro."},
                 {e:"Azure OpenAI - GPT",t:"L'ente soggetto garantisce il rispetto del segreto bancario ai sensi dell'art. 47 LB e attua i requisiti della FINMA in materia di lotta contro il riciclaggio di denaro."}]}
      },
      lookup:{q:"Bankgeheimnis",l1:"German",l2:"French",count:"425 results",rows:[
        {a:"Anlässlich dieses Treffens wurde der Kundenberater misstrauisch, da die Kundin auffällige Fragen über das Schweizer Bankgeheimnis und das Geldwäschereigesetz stellte.",b:"Lors de l'entretien, le conseiller à la clientèle est devenu méfiant parce que la cliente posait des questions suspectes sur le secret bancaire suisse et sur la loi sur le blanchiment d'argent.",dom:"BANKING & FINANCE",src:"MROS - Source: fedpol.admin.ch - Data Set: Neur.on"},
        {a:"Obwohl der Begriff Bankgeheimnis im Initiativtext nicht und im Argumentarium nur sparsam verwendet wird, beabsichtigt die Initiative insbesondere die Verankerung des steuerlichen Bankgeheimnisses im Inland auf Verfassungsstufe.",b:"Bien que le terme ne figure pas dans le texte de l'initiative et que l'argumentaire du comité d'initiative n'en fasse qu'un usage parcimonieux, un des buts principaux de l'initiative est d'inscrire la notion de secret bancaire dans la Constitution.",dom:"TAX LAW & CUSTOMS",src:"ESTV FF20156429 Botschaft-zur-Volksinitiative-Ja-zum-Schutz-der-Privatsphäre- - Source: fedlex.admin.ch - Data Set: Neur.on"}],
        mark:["Bankgeheimnis","secret bancaire"]}
    },
    ldip:{label:"Arbitrage · art. 186 LDIP",
      src:"Le tribunal arbitral statue sur sa propre compétence conformément à l'art. 186 LDIP, et la sentence peut faire l'objet d'un recours au Tribunal fédéral.",
      def:"en",
      out:{
        en:{main:"The Arbitration Panel shall have jurisdiction to decide on its own competence under Art. 186 PILA and the award may be appealed before the Federal Supreme Court.",
            alt:[{e:"DeepL Pro",t:"The arbitral tribunal shall rule on its own jurisdiction in accordance with Article 186 of the LDIP, and the award may be appealed to the Federal Supreme Court."},
                 {e:"Azure OpenAI - GPT",t:"The arbitral tribunal rules on its own jurisdiction in accordance with Art. 186 PILA, and the award may be subject to an appeal before the Federal Supreme Court."}]}
      }
    }
  };
  var LANGS={de:"German",en:"English",it:"Italian"};
  var $=function(id){return document.getElementById(id);};
  var cx=$("cx"); if(!cx) return;
  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var st={ex:"co",tgt:"de",eng:"Neur.on LLM",alts:[],ai:0,timer:null};
  var src=$("cxSrc"),out=$("cxOut"),cnt=$("cxCnt"),tgt=$("cxTgt"),eng=$("cxEng"),srcLang=$("cxSrcLang"),
      alts=$("cxAlts"),altT=$("cxAltT"),pg=$("cxPg"),notice=$("cxNotice"),lookupBtn=$("cxLookupBtn"),modal=$("cxModal");

  function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function setTargets(ex){
    var d=EX[ex]; [].forEach.call(tgt.options,function(o){var ok=!!d.out[o.value]; o.disabled=!ok; o.textContent=LANGS[o.value]+(ok?"":" (démo : bientôt)");});
    if(!d.out[st.tgt]) st.tgt=d.def; tgt.value=st.tgt;
  }
  function loadExample(ex){
    st.ex=ex; var d=EX[ex];
    [].forEach.call(document.querySelectorAll("#cxEx button"),function(b){b.classList.toggle("on",b.getAttribute("data-ex")===ex);});
    src.value=d.src; cnt.textContent=d.src.length+" / 10000"; srcLang.selectedIndex=1;
    setTargets(ex); closeAlts(); translate(); loadReph();
  }
  function currentText(){
    var d=EX[st.ex].out[st.tgt]; if(!d) return null;
    if(st.eng==="Neur.on LLM") return d.main;
    for(var i=0;i<d.alt.length;i++) if(d.alt[i].e===st.eng) return d.alt[i].t;
    return null;
  }
  function translate(){
    if(st.timer){clearTimeout(st.timer);st.timer=null;}
    closeAlts();
    if(!src.value){out.innerHTML='';return;}
    out.innerHTML='<div class="cx-shim" style="width:92%"></div><div class="cx-shim" style="width:78%"></div><div class="cx-shim" style="width:86%"></div>';
    st.timer=setTimeout(function(){var t=currentText(); out.textContent=t||""; st.timer=null;},reduce?0:900);
  }
  function buildAlts(){
    var d=EX[st.ex].out[st.tgt]; if(!d) return [];
    var list=[{e:"Neur.on LLM",t:d.main}].concat(d.alt);
    return list.filter(function(a){return a.e!==st.eng;});
  }
  function showAlt(){
    if(!st.alts.length) return;
    var a=st.alts[st.ai];
    altT.innerHTML=esc(a.t)+' <em>- '+esc(a.e)+'</em>';
    pg.textContent=(st.ai+1)+" / "+st.alts.length;
  }
  function openAlts(){
    if(!src.value||st.timer) return;
    st.alts=buildAlts(); st.ai=0; if(!st.alts.length) return;
    alts.classList.add("on");
    altT.innerHTML='<span class="ph">Generating alternatives…</span>'; pg.textContent="";
    setTimeout(showAlt,reduce?0:700);
  }
  function closeAlts(){alts.classList.remove("on");}

  /* Extraits */
  [].forEach.call(document.querySelectorAll("#cxEx button"),function(b){b.addEventListener("click",function(){loadExample(b.getAttribute("data-ex"));});});
  tgt.addEventListener("change",function(){st.tgt=tgt.value; translate();});
  eng.addEventListener("change",function(){st.eng=eng.value; notice.classList.toggle("show",st.eng!=="Neur.on LLM"); $("cxFEng").value=st.eng; translate();});
  $("cxFEng").addEventListener("change",function(){eng.value=$("cxFEng").value; st.eng=eng.value; notice.classList.toggle("show",st.eng!=="Neur.on LLM"); translate();});
  $("cxClear").addEventListener("click",function(){src.value=""; cnt.textContent="0 / 10000"; srcLang.selectedIndex=0; out.innerHTML=""; closeAlts(); lookupBtn.classList.remove("show"); [].forEach.call(document.querySelectorAll("#cxEx button"),function(b){b.classList.remove("on");});});
  $("cxSpark").addEventListener("click",openAlts);
  $("cxAltX").addEventListener("click",closeAlts);
  $("cxUp").addEventListener("click",function(){if(!st.alts.length)return; st.ai=(st.ai-1+st.alts.length)%st.alts.length; showAlt();});
  $("cxDn").addEventListener("click",function(){if(!st.alts.length)return; st.ai=(st.ai+1)%st.alts.length; showAlt();});
  $("cxCopy").addEventListener("click",function(){var t=out.textContent; if(!t) return; try{navigator.clipboard&&navigator.clipboard.writeText(t);}catch(e){}});

  /* Interrupteur Highly sensitive content */
  var sw=$("cxSwitch");
  sw.addEventListener("click",function(){var on=sw.classList.toggle("off"); sw.setAttribute("aria-pressed",on?"false":"true");});

  /* Onglets */
  var tabs=[].slice.call(document.querySelectorAll(".cx-tab"));
  tabs.forEach(function(t){t.addEventListener("click",function(){
    tabs.forEach(function(x){var on=x===t; x.classList.toggle("on",on); x.setAttribute("aria-selected",on?"true":"false");});
    ["text","file","pdf","reph"].forEach(function(k){$("cxp-"+k).classList.toggle("on",k===t.getAttribute("data-tab"));});
    sw.classList.toggle("dis",t.getAttribute("data-tab")==="pdf");
    lookupBtn.classList.remove("show");
  });});

  /* Fast Lookup : surligner un mot dans la source ouvre CHnell */
  function selectionInSrc(){var s=window.getSelection?String(window.getSelection()):""; return s&&s.trim().length>1;}
  src.addEventListener("mouseup",function(){setTimeout(function(){lookupBtn.classList.toggle("show",selectionInSrc());},10);});
  src.addEventListener("keyup",function(){lookupBtn.classList.toggle("show",selectionInSrc());});
  document.addEventListener("mousedown",function(e){if(!lookupBtn.contains(e.target)&&e.target!==src) lookupBtn.classList.remove("show");});
  function mark(text,terms){var h=esc(text); terms.forEach(function(t){h=h.split(esc(t)).join('<mark>'+esc(t)+'</mark>');}); return h;}
  function openLookup(){
    var d=EX[st.ex]; var cols=$("cxLkCols");
    if(!d.lookup){cols.innerHTML='<div class="cell" style="grid-column:1 / -1">Démo : Fast Lookup est disponible sur les extraits « Contrat » et « Banque ».</div>'; modal.classList.add("on"); return;}
    $("cxLkQ").textContent=d.lookup.q; $("cxLkL1").textContent=d.lookup.l1; $("cxLkL2").textContent=d.lookup.l2;
    var h='<div class="colh"><i>'+esc(d.lookup.q)+'</i> in <b>'+esc(d.lookup.l1)+'</b><small>'+esc(d.lookup.count)+'</small></div><div class="colh r"><i>'+esc(d.lookup.q)+'</i> in <b>'+esc(d.lookup.l2)+'</b></div>';
    d.lookup.rows.forEach(function(r){h+='<div class="cell">'+mark(r.a,d.lookup.mark)+'</div><div class="cell r">'+mark(r.b,d.lookup.mark)+'</div><div class="meta"><span><span class="dom">'+esc(r.dom)+'</span>'+esc(r.src)+'</span><a>Show in context</a></div>';});
    cols.innerHTML=h; modal.classList.add("on"); lookupBtn.classList.remove("show");
  }
  lookupBtn.addEventListener("click",openLookup);
  $("cxLkClose").addEventListener("click",function(){modal.classList.remove("on");});
  modal.addEventListener("click",function(e){if(e.target===modal) modal.classList.remove("on");});

  /* File translation et PDF to Word : dépôt simulé */
  function simulate(drop,row,bar,stEl,done){
    drop.addEventListener("click",function(){
      row.classList.add("show"); bar.style.transform="scaleX(0)"; stEl.textContent=stEl.getAttribute("data-run")||stEl.textContent;
      setTimeout(function(){bar.style.transform="scaleX(1)";},60);
      setTimeout(function(){stEl.textContent=done;},reduce?50:2600);
    });
  }
  $("cxFileSt").setAttribute("data-run","Translating…"); $("cxPdfSt").setAttribute("data-run","Converting…");
  simulate($("cxFileDrop"),$("cxFileRow"),$("cxFileBar"),$("cxFileSt"),"Download");
  simulate($("cxPdfDrop"),$("cxPdfRow"),$("cxPdfBar"),$("cxPdfSt"),"Download .docx");
  $("cxFTgt").addEventListener("change",function(){$("cxFileSub").textContent="248 KB · 14 pages · German → "+$("cxFTgt").value;});

  /* Rephrasing */
  var rsrc=$("cxRSrc"),rout=$("cxROut"),rcnt=$("cxRCnt"),pop=$("cxSetPop"),dot=$("cxSetDot"),rstyle=null,rTimer=null;
  function loadReph(){
    var d=EX[st.ex];
    if(!d.reph){rsrc.value=""; rcnt.textContent="0 / 5000"; rout.innerHTML='<span class="ph">'+esc("Démo : choisissez l'extrait « Contrat · art. 104 CO » pour la réécriture.")+'</span>'; return;}
    rsrc.value=d.src; rcnt.textContent=d.src.length+" / 5000"; rephrase();
  }
  function rephrase(){
    var d=EX[st.ex]; if(!d.reph) return;
    if(rTimer){clearTimeout(rTimer);}
    rout.innerHTML='<div class="cx-shim" style="width:90%"></div><div class="cx-shim" style="width:82%"></div><div class="cx-shim" style="width:70%"></div>';
    rTimer=setTimeout(function(){rout.innerHTML=(rstyle==="Simplified")?d.reph.simp:d.reph.def; rTimer=null;},reduce?0:900);
  }
  $("cxSetBtn").addEventListener("mousedown",function(e){e.preventDefault(); pop.classList.toggle("on");});
  $("cxSetBtn").addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault(); pop.classList.toggle("on");}});
  [].forEach.call(document.querySelectorAll("#cxSetPop .cx-chip"),function(c){c.addEventListener("click",function(){
    var was=c.classList.contains("on"); [].forEach.call(document.querySelectorAll("#cxSetPop .cx-chip"),function(x){x.classList.remove("on");}); if(!was) c.classList.add("on");
  });});
  $("cxSetApply").addEventListener("click",function(){
    var on=document.querySelector("#cxSetPop .cx-chip.on"); rstyle=on?on.getAttribute("data-style"):null;
    dot.classList.toggle("on",!!rstyle); pop.classList.remove("on");
    if(rstyle&&rstyle!=="Simplified"){$("cxRNote").textContent="Démo : le style « "+rstyle+" » n'est pas disponible sur cet extrait ; réglage par défaut appliqué. Styles réels de Corrext : Formal legal, Financial, Simplified, Formal, Informal, Shorten."; rstyle=null; dot.classList.remove("on");}
    else{$("cxRNote").textContent="Démo : réécriture disponible sur l'extrait « Contrat · art. 104 CO », avec le réglage par défaut et le style Simplified.";}
    rephrase();
  });
  $("cxSetReset").addEventListener("click",function(){[].forEach.call(document.querySelectorAll("#cxSetPop .cx-chip"),function(x){x.classList.remove("on");}); rstyle=null; dot.classList.remove("on"); pop.classList.remove("on"); rephrase();});
  document.addEventListener("mousedown",function(e){if(pop.classList.contains("on")&&!pop.contains(e.target)&&e.target!==$("cxSetBtn")) pop.classList.remove("on");});

  /* Démarrage : premier extrait, dès que le cadre approche du viewport (240px avant) */
  var started=false;
  function start(){if(started)return; started=true; loadExample("co");}
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){start(); io.disconnect();}});},{threshold:0,rootMargin:"0px 0px 240px 0px"});
    io.observe(cx);
  } else start();
})();
