const {chromium}=require('/opt/node-tools/node_modules/playwright');
const {spawn}=require('child_process');
const [,, start, end, out]=process.argv;
(async()=>{
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 p.on('pageerror',e=>console.error('PAGEERR',e.message));p.on('console',m=>{if(m.type()==='error')console.error('CONSOLE',m.text())});
 await p.goto('http://localhost:8765/index.html');await p.waitForFunction('window.READY===true');
 const f=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',out]);
 for(let i=+start;i<+end;i++){
  const d=await p.evaluate(i=>{frame(i);return document.getElementById('c').toDataURL('image/jpeg',0.93)},i);
  const buf=Buffer.from(d.split(',')[1],'base64');if(!f.stdin.write(buf))await new Promise(r=>f.stdin.once('drain',r));
 }
 f.stdin.end();await new Promise(r=>f.on('close',r));await b.close();
})();
