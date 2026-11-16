import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
const times=process.argv.slice(3).map(Number); const out=process.argv[2];
const serveUrl=await bundle({entryPoint:'src/index.ts'});
const comp=await selectComposition({serveUrl,id:'SaffronIran'});
for(const t of times){await renderStill({composition:comp,serveUrl,frame:Math.round(t*30),output:`${out}/s_${t}.png`,browserExecutable:'/opt/pw-browsers/chromium',scale:0.5,chromiumOptions:{gl:'angle'}});console.log('ok',t)}
