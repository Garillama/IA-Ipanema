// Per-process guard around the native CLI fetch; never reads .nuvem or logs bodies.
import {createHash} from 'node:crypto';
export function guardedFetch(fetchImpl,{mode='read',sourceId='',targetId='',publishedId='',files=[],expectedHashes={},origins=['https://api.nuvemshop.com.br','https://api.tiendanube.com']}={}){
 let stopped=false,cloned=false;const writes=new Set();
 return async(input,options={})=>{
  const url=new URL(typeof input==='string'||input instanceof URL?input:input.url);
  const method=(options.method||input.method||'GET').toUpperCase();
  const match=url.pathname.match(/^\/v1\/\d+\/theme-installations(?:\/(\d+))?(\/.*)?$/);
  if(stopped||!origins.includes(url.origin)||!match||url.username||url.password)throw Error('IA_THEME_API_BLOCKED');
  const write=!['GET','HEAD','OPTIONS'].includes(method);const id=match[1],suffix=match[2]||'';
  if(write){
   let body;try{body=JSON.parse(options.body);}catch{throw Error('IA_THEME_API_INVALID_BODY');}
   if(mode==='clone'&&method==='POST'&&id===sourceId&&suffix==='/clone'&&!cloned&&Object.keys(body).length===1&&typeof body.title==='string')cloned=true;
   else if((mode==='push'&&id!==publishedId||mode==='production-push'&&id===publishedId)&&id===targetId&&publishedId&&/^[0-9]+$/.test(targetId)&&
      (method==='PATCH'&&suffix==='/files'||method==='POST'&&suffix==='/files/validate')&&
      Array.isArray(body.upsert)&&body.upsert.length>0&&body.upsert.every(file=>files.includes(file.path))&&
      (!body.delete||Array.isArray(body.delete)&&body.delete.length===0)){
    if(mode==='production-push'&&!body.upsert.every(file=>typeof file.content==='string'&&expectedHashes[file.path]===createHash('sha256').update(file.content).digest('hex')))throw Error('IA_THEME_API_CONTENT_HASH_MISMATCH');
    const key=method+url.pathname+options.body;
    if(writes.has(key))throw Error('IA_THEME_API_DUPLICATE_WRITE');writes.add(key);
   }else throw Error('IA_THEME_API_WRITE_NOT_AUTHORIZED');
  }
  let response;
  try{response=await fetchImpl(input,options);}catch(error){
   if(write){stopped=true;throw Error('IA_THEME_API_UNCERTAIN_WRITE_NO_RETRY');}
   throw error;
  }
  if([403,429].includes(response.status)){stopped=true;throw Error('IA_THEME_API_STOP_'+response.status);}
  if(write&&response.status>=500){stopped=true;throw Error('IA_THEME_API_UNCERTAIN_WRITE_NO_RETRY');}
  return response;
 };
}

if(process.env.IPANEMA_THEME_GUARD_MODE){
 globalThis.fetch=guardedFetch(globalThis.fetch,{
  mode:process.env.IPANEMA_THEME_GUARD_MODE,sourceId:process.env.IPANEMA_THEME_GUARD_SOURCE,
  targetId:process.env.IPANEMA_THEME_GUARD_TARGET,publishedId:process.env.IPANEMA_THEME_GUARD_PUBLISHED,
  files:(process.env.IPANEMA_THEME_GUARD_FILES||'').split(',').filter(Boolean),
  expectedHashes:JSON.parse(process.env.IPANEMA_THEME_GUARD_HASHES||'{}')
 });
}
