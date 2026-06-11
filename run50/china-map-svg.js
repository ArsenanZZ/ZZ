// China Province Map SVG — simplified polygons
// Projection: x=(lon-70)*11.8, y=(55-lat)*13.5  viewBox "0 0 800 600"
const CHINA_MAP_SVG = `<svg xmlns="http://www.w3.org/2000/svg" id="cn-map-master" viewBox="0 0 800 560">
  <!-- Xinjiang 新疆 -->
  <polygon id="cn_xinjiang" points="35,81 248,81 307,149 260,189 307,243 248,297 166,297 107,270 71,243 35,189"/>
  <!-- Tibet 西藏 -->
  <polygon id="cn_tibet" points="95,243 248,243 307,243 354,270 354,338 320,378 248,378 177,364 107,311 95,270"/>
  <!-- Qinghai 青海 -->
  <polygon id="cn_qinghai" points="236,162 390,162 437,216 402,270 354,270 307,243 248,243 236,216"/>
  <!-- Inner Mongolia 内蒙古 -->
  <polygon id="cn_innermongolia" points="307,54 626,27 709,81 661,162 579,162 519,189 437,216 390,189 307,162"/>
  <!-- Heilongjiang 黑龙江 -->
  <polygon id="cn_heilongjiang" points="614,27 779,27 779,135 709,149 709,81 626,27"/>
  <!-- Jilin 吉林 -->
  <polygon id="cn_jilin" points="614,135 709,135 709,175 661,162 614,162"/>
  <!-- Liaoning 辽宁 -->
  <polygon id="cn_liaoning" points="567,162 661,162 709,175 700,216 614,229 555,229 555,202"/>
  <!-- Gansu 甘肃 -->
  <polygon id="cn_gansu" points="236,162 307,162 390,189 437,216 390,270 354,270 307,243 248,243 236,216"/>
  <!-- Ningxia 宁夏 -->
  <polygon id="cn_ningxia" points="390,216 437,216 437,270 402,270 390,243"/>
  <!-- Shaanxi 陕西 -->
  <polygon id="cn_shaanxi" points="437,216 484,202 519,202 519,256 496,283 484,324 460,338 449,311 437,270"/>
  <!-- Shanxi 山西 -->
  <polygon id="cn_shanxi" points="484,189 519,189 519,256 496,283 484,270 472,256 484,216"/>
  <!-- Hebei 河北 -->
  <polygon id="cn_hebei" points="519,162 567,162 555,202 614,229 590,256 555,270 519,256 519,189"/>
  <!-- Beijing 北京 -->
  <polygon id="cn_beijing" points="531,175 555,175 555,202 531,202"/>
  <!-- Tianjin 天津 -->
  <polygon id="cn_tianjin" points="555,202 579,202 579,229 555,229"/>
  <!-- Shandong 山东 -->
  <polygon id="cn_shandong" points="519,256 590,256 638,243 638,283 590,297 543,297 519,270"/>
  <!-- Henan 河南 -->
  <polygon id="cn_henan" points="484,270 519,256 543,270 543,311 519,338 484,324 472,311"/>
  <!-- Hubei 湖北 (contains Xiangyang) -->
  <polygon id="cn_hubei" points="449,311 484,297 543,311 555,338 519,351 484,351 460,338"/>
  <!-- Anhui 安徽 -->
  <polygon id="cn_anhui" points="543,283 590,270 602,297 590,338 567,351 543,338 519,338 543,311"/>
  <!-- Jiangsu 江苏 -->
  <polygon id="cn_jiangsu" points="555,256 614,256 626,283 614,311 590,324 567,311 567,283 543,270"/>
  <!-- Shanghai 上海 -->
  <polygon id="cn_shanghai" points="614,297 638,297 638,324 614,311"/>
  <!-- Zhejiang 浙江 -->
  <polygon id="cn_zhejiang" points="567,311 614,311 638,311 638,378 602,391 567,364 555,338"/>
  <!-- Jiangxi 江西 -->
  <polygon id="cn_jiangxi" points="519,338 567,338 567,364 555,405 531,418 507,405 507,378 507,351"/>
  <!-- Fujian 福建 -->
  <polygon id="cn_fujian" points="567,351 614,338 638,364 626,432 590,432 555,418 567,391"/>
  <!-- Hunan 湖南 (contains Guilin via proximity) -->
  <polygon id="cn_hunan" points="460,338 519,338 507,378 531,432 507,432 484,418 460,405 449,378 449,351"/>
  <!-- Chongqing 重庆 -->
  <polygon id="cn_chongqing" points="413,311 460,311 460,338 449,351 425,364 413,351"/>
  <!-- Sichuan 四川 -->
  <polygon id="cn_sichuan" points="307,297 413,297 413,311 425,364 390,378 354,378 320,378 307,338"/>
  <!-- Guizhou 贵州 -->
  <polygon id="cn_guizhou" points="413,351 460,351 460,405 449,418 413,418 390,405 390,378 425,364"/>
  <!-- Yunnan 云南 -->
  <polygon id="cn_yunnan" points="307,338 390,338 390,405 390,459 354,472 307,459 284,432 295,378"/>
  <!-- Guangxi 广西 (contains Guilin ~475,401) -->
  <polygon id="cn_guangxi" points="390,392 484,392 520,432 507,459 472,486 425,486 390,459"/>
  <!-- Guangdong 广东 -->
  <polygon id="cn_guangdong" points="460,378 555,378 567,405 555,459 519,486 472,486 507,459 507,432 460,405"/>
  <!-- Hong Kong 香港 -->
  <polygon id="cn_hongkong" points="519,432 531,432 531,459 507,459"/>
  <!-- Hainan 海南 -->
  <polygon id="cn_hainan" points="449,486 484,486 484,513 449,513"/>
  <!-- Taiwan 台湾 -->
  <polygon id="cn_taiwan" points="590,405 614,405 614,459 590,459"/>
</svg>`;
