// Skyline noturno gerado por código (substitua por uma imagem sua se preferir)
(function(){
  var svg=document.getElementById('skyline'),s=7,out='';
  function r(){s=(s*9301+49297)%233280;return s/233280}
  var x=0;
  while(x<1000){
    var w=30+r()*60,h=120+r()*(r()>.85?420:240),y=600-h;
    out+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" fill="#0a0a0c"/>';
    for(var wy=y+10;wy<598;wy+=11){
      for(var wx=x+5;wx<x+w-6;wx+=8){
        if(r()>.72) out+='<rect x="'+wx+'" y="'+wy+'" width="3" height="4" fill="#e8d9a8" opacity="'+(.35+r()*.6).toFixed(2)+'"/>';
      }
    }
    x+=w+r()*6;
  }
  svg.innerHTML=out;
})();