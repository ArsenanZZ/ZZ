/* Small native-vector landmark illustrations for the historical RunCN maps. */
module.exports=function(kind){
 const green='#194e46',gold='#d3a24a',paper='#f5e8c4',ink='#163e47';
 const roof=(x,y,w)=>`<path d="M${x-w/2} ${y} Q${x-w/3} ${y+6} ${x} ${y-18} Q${x+w/3} ${y+6} ${x+w/2} ${y} L${x+w/2-9} ${y+9} H${x-w/2+9}Z" fill="${green}"/>`;
 let art='';
 if(['pavilion','tower','pagoda'].includes(kind)){
  const levels=kind==='pagoda'?5:3;
  for(let i=0;i<levels;i++){const y=142-i*23,w=144-i*19;art+=`<path d="M${160-w/2+16} ${y-18}H${160+w/2-16}V${y+8}H${160-w/2+16}Z" fill="${paper}"/>`+roof(160,y-19,w);for(let j=-1;j<=1;j++)art+=`<path d="M${160+j*(w/3-6)} ${y-16}V${y+7}"/>`;}
  art+='<path d="M80 163H240M70 170H250"/>';
 }else if(kind==='church'){
  art=`<path d="M102 155V85H218V155ZM121 85V63H199V85" fill="${paper}"/><path d="M160 20C154 42 117 37 123 67H197C203 37 166 42 160 20Z" fill="${green}"/><path d="M160 7V26M153 13H167"/><path d="M139 156V119Q160 88 181 119V156" fill="${green}"/><path d="M88 155V111H102M218 111H232V155" fill="${paper}"/><path d="M76 111L96 86L116 111M204 111L224 86L244 111" fill="${green}"/>`;
 }else if(kind==='gate'||kind==='greatwall'){
  art=`<path d="M57 157V102H263V157H182V133Q160 109 138 133V157Z" fill="${green}"/><path d="M57 102V87H75V102H92V87H110V102H129V87H148V102H167V87H186V102H205V87H224V102H244V87H263V102" fill="${paper}"/><path d="M105 87V59H215V87" fill="${paper}"/>`+roof(160,57,145)+roof(160,37,111);
 }else if(kind==='bridge'){
  art=`<path d="M39 142H282M50 119H271M63 119V142M257 119V142M89 119V142M231 119V142"/><path d="M51 119V70L106 119L160 70L214 119L269 70V119M51 70H269M51 70L106 119L160 70L214 119L269 70" fill="none"/><path d="M66 143V164M254 143V164M156 143V164" stroke-width="10"/>`;
 }else if(kind==='lighthouse'){
  art=`<path d="M137 156L146 54H174L184 156Z" fill="${paper}"/><path d="M143 82H177V98H142M140 116H180V131H139" fill="${green}"/><path d="M138 54V36H182V54ZM132 36L160 17L188 36Z" fill="${gold}"/><path d="M107 61L63 83M213 61L257 83"/>`;
 }else if(kind==='skyline'){
  art=`<path d="M150 163V50L177 19L187 163Z" fill="${green}"/><path d="M107 163V103M107 103V38M107 38V19"/><circle cx="107" cy="56" r="18" fill="${gold}"/><circle cx="107" cy="108" r="26" fill="${paper}"/><path d="M205 163V76H236V163M213 86H229V104H213Z" fill="${green}"/><path d="M53 163V123H78V163M244 163V110H266V163" fill="${paper}"/>`;
 }else if(kind==='tram'){
  art=`<path d="M86 152V40Q86 30 98 30H223Q235 30 235 40V152Z" fill="${green}"/><path d="M96 42H225V85H96ZM96 94H225V128H96Z" fill="${paper}"/><path d="M138 42V85M181 42V85M138 94V128M181 94V128M106 150L97 172M216 150L225 172M130 30L151 11H190"/><circle cx="111" cy="140" r="5" fill="${gold}"/><circle cx="212" cy="140" r="5" fill="${gold}"/>`;
 }else if(kind==='palm'||kind==='island'){
  art=`<path d="M147 164Q163 116 151 65" stroke-width="10"/><path d="M151 66Q113 16 68 59Q120 50 151 66Q180 8 234 41Q192 45 151 66Q208 45 244 93Q197 67 151 66Q115 47 83 107Q113 77 151 66Z" fill="${green}"/><path d="M197 158V116H259V158M192 117L228 98L265 117" fill="${paper}"/>`;
 }else if(kind==='blossom'){
  art=`<path d="M79 163Q126 93 220 43M133 114Q115 66 88 42M172 79Q209 96 256 81" fill="none" stroke-width="9"/>`;
  for(const [x,y] of [[88,42],[130,85],[220,43],[256,81],[173,70]]){for(let k=0;k<5;k++){let a=k*Math.PI*2/5;art+=`<ellipse cx="${x+Math.cos(a)*10}" cy="${y+Math.sin(a)*10}" rx="10" ry="8" fill="#e4b6a5"/>`;}art+=`<circle cx="${x}" cy="${y}" r="4" fill="${gold}"/>`;}
 }else if(kind==='lake'){
  art=`<path d="M25 137Q65 85 107 130Q144 92 187 129Q231 77 294 139" fill="${green}"/><path d="M65 160Q160 82 255 160M65 149Q160 71 255 149M80 140V151M108 121V132M136 111V120M164 108V118M192 114V125M220 129V140M246 144V155" fill="none"/><path d="M206 100V72H257V100" fill="${paper}"/>`+roof(232,69,75);
 }else if(kind==='karst'){
  art=`<path d="M31 153Q62 130 69 86Q78 50 97 96L111 136Q135 115 139 58Q154 12 170 59L181 129Q200 104 206 64Q218 29 237 90L253 126Q271 109 289 155Z" fill="${green}"/><path d="M182 151Q219 93 252 151" fill="${paper}"/>`;
 }
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200"><g stroke="${gold}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"><circle cx="230" cy="60" r="42" fill="#e5c67e" opacity=".7"/><path d="M14 165Q69 127 110 151T211 143T307 165L292 184H25Z" fill="${green}"/>${art}<path d="M35 173Q88 157 133 172T236 171T286 175M53 185Q114 170 174 183T270 182" fill="none" stroke="${paper}" stroke-width="3"/></g></svg>`;
};
