import fs from 'fs';
import {feature} from 'topojson-client';
import {geoMercator, geoPath} from 'd3-geo';
const topo=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const fc=feature(topo,topo.objects.countries);
const mk=(box,w,h)=>{
  const [[x0,y0],[x1,y1]]=box;
  const poly={type:'MultiPoint',coordinates:[[x0,y0],[x1,y0],[x1,y1],[x0,y1]]};
  const proj=geoMercator().fitExtent([[0,0],[w,h]],poly);
  const path=geoPath(proj).digits(1);
  const countries=fc.features.map(f=>{const b=path.bounds(f);const ok=b[1][0]>-50&&b[0][0]<w+50&&b[1][1]>-50&&b[0][1]<h+50;return {n:f.properties.name,d:ok?path(f):null}}).filter(c=>c.d);
  return {w,h,proj,countries};
};
const pts={KL:[101.69,3.14],Mashhad:[59.6,36.3],Torbat:[59.22,35.27],Qaen:[59.18,33.73],Gonabad:[58.68,34.35],Tehran:[51.39,35.69],Hormuz:[56.3,26.55],Gulf:[51.5,27.6],Caspian:[51.2,40.5]};
const out={};
const A=mk([[43,-4],[106,44]],1000,760);
const B=mk([[43.5,24],[64,40.5]],960,1000);
for(const [k,m] of [['route',A],['iran',B]]){
  out[k]={w:m.w,h:m.h,countries:m.countries,pts:Object.fromEntries(Object.entries(pts).map(([n,c])=>[n,m.proj(c).map(v=>+v.toFixed(1))]))};
}
fs.writeFileSync('src/mapdata.json',JSON.stringify(out));
console.log(Object.keys(out), out.route.pts, out.iran.pts, out.iran.countries.filter(c=>c.n=='Iran').length);
