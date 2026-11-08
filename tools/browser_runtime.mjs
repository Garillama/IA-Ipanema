import {createRequire} from 'node:module';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export const workspaceRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export const evidenceRoot=path.resolve(process.env.IPANEMA_EVIDENCE_DIR || path.join(workspaceRoot,'reports/runs/legacy',new Date().toISOString().replace(/[:.]/g,'-')+'-'+crypto.randomUUID().slice(0,8)));
export const publicUrl=process.env.IPANEMA_PUBLIC_URL;
export function projectUrl(){if(!publicUrl)throw Error('Configura IPANEMA_PUBLIC_URL o usa tools/ia.py qa con un proyecto.');return publicUrl;}
export function pageUrl(name){const value=process.env['IPANEMA_PAGE_'+name.toUpperCase()];if(!value)throw Error('Página '+name+' sin configurar; no se inventará una ruta.');return new URL(value,projectUrl()).href;}
export function knowledgeFile(relative){return path.join(process.env.IPANEMA_KNOWLEDGE_ROOT||path.join(workspaceRoot,'ipanema-discovery'),relative);}
const requirements=[createRequire(path.join(workspaceRoot,'package.json'))];
let rootsLoaded=false;
function roots(){
 if(rootsLoaded)return;rootsLoaded=true;
 const locations=[];
 if(process.env.IPANEMA_NODE_MODULE_ROOT)locations.push(process.env.IPANEMA_NODE_MODULE_ROOT);
 try{locations.push(execFileSync(process.platform==='win32'?'npm.cmd':'npm',['root','-g'],{encoding:'utf8',timeout:5000,stdio:['ignore','pipe','ignore']}).trim());}catch{}
 for(const location of locations){requirements.push(createRequire(path.join(location,'__ipanema_resolver.cjs')));const cli=path.join(location,'@tiendanube/cli/package.json');if(fs.existsSync(cli))requirements.push(createRequire(cli));}
 try{const cli=requirements[0].resolve('@tiendanube/cli/package.json');requirements.push(createRequire(cli));}catch{}
}
export const cliRequire={resolve(name){roots();for(const req of requirements){try{return req.resolve(name);}catch{}}throw Error('Dependencia opcional ausente: '+name+'. Consulta doctor y package.json; no se instalará automáticamente.');}};
export async function loadDependency(name){return import(pathToFileURL(cliRequire.resolve(name)).href);}
export function chromePath(engine){
 const explicit=process.env.IPANEMA_CHROME_PATH;
 if(explicit){if(!fs.existsSync(explicit))throw Error('IPANEMA_CHROME_PATH no existe.');return explicit;}
 const candidates=[];
 try{candidates.push(engine.executablePath());}catch{}
 const names=process.platform==='win32'?['chrome.exe','chromium.exe']:['google-chrome','google-chrome-stable','chromium','chromium-browser'];
 for(const folder of (process.env.PATH||'').split(path.delimiter))for(const name of names)candidates.push(path.join(folder,name));
 if(process.platform==='darwin')candidates.push('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
 if(process.platform==='win32')for(const name of ['PROGRAMFILES','PROGRAMFILES(X86)','LOCALAPPDATA'])if(process.env[name])candidates.push(path.join(process.env[name],'Google/Chrome/Application/chrome.exe'));
 const found=candidates.find(p=>typeof p==='string'&&p&&fs.existsSync(p));if(!found)throw Error('Chrome/Chromium no disponible. Configura IPANEMA_CHROME_PATH.');return found;
}
export function cleanUrl(value){try{const u=new URL(value);u.username='';u.password='';u.hash='';for(const key of [...u.searchParams.keys()])if(/token|key|secret|auth|session|email|phone|password/i.test(key))u.searchParams.set(key,'[redacted]');return u.href;}catch{return value;}}
export function assertUrl(value){
 const u=new URL(value);const loopback=['127.0.0.1','localhost','[::1]'].includes(u.hostname);
 if(u.username||u.password||!['https:','http:'].includes(u.protocol)||u.protocol==='http:'&&!loopback)throw Error('URL de auditoría inválida.');
 if(!loopback&&process.env.IPANEMA_ALLOW_NETWORK!=='1')throw Error('La auditoría remota requiere --allow-network y un origen registrado.');
 const allowed=(process.env.IPANEMA_ALLOWED_ORIGINS||'').split(',').filter(Boolean);
 if(!loopback&&(!allowed.length||!allowed.includes(u.origin)))throw Error('Origen no autorizado para esta ejecución.');
 return u;
}
const authPages=new WeakSet();
const protectedPages=new WeakMap();
function protectPage(page,browser){
 if(protectedPages.has(page))return protectedPages.get(page);
 const ready=(async()=>{
 await page.setBypassServiceWorker(true);
 await page.setRequestInterception(true);
 page.on('request',request=>{
  let permitted=['GET','HEAD','OPTIONS'].includes(request.method());
  if(!permitted&&authPages.has(page)&&request.method()==='POST'){
   try{const u=new URL(request.url());permitted=u.origin===new URL(projectUrl()).origin&&/^\/password\/?$/.test(u.pathname);}catch{}
  }
  if(request.isNavigationRequest()&&request.frame()===page.mainFrame()){
   try{assertUrl(request.url());}catch{permitted=false;}
  }
  try{if(/\/(?:admin|logout|sair|checkout)(?:\/|$)|\/cart\/(?:add|remove|update)(?:\/|$)/i.test(new URL(request.url()).pathname))permitted=false;}catch{}
  if(browser.__accessLimited)permitted=false;
  if(!request.isInterceptResolutionHandled())(permitted?request.continue():request.abort('blockedbyclient')).catch(()=>{});
 });
 page.on('response',response=>{if([403,429].includes(response.status())&&response.request().isNavigationRequest())browser.__accessLimited=response.status();});
 const goto=page.goto.bind(page);
 page.goto=async(url,...args)=>{assertUrl(url);if(browser.__accessLimited)throw Error('Acceso limitado previamente; ejecución detenida.');const response=await goto(url,...args);if(browser.__accessLimited)throw Error('HTTP '+browser.__accessLimited+': detenido sin reintentos.');return response;};
 await page.evaluateOnNewDocument(()=>{window.WebSocket=function(){throw Error('WebSocket deshabilitado durante QA de lectura.');};});
 return page;
 })();
 protectedPages.set(page,ready);
 return ready;
}
export const puppeteer={async launch(options={}){
 const knowledgeRoot=path.resolve(process.env.IPANEMA_KNOWLEDGE_ROOT||path.join(workspaceRoot,'ipanema-discovery'));
 const inside=(candidate,root)=>candidate===root||candidate.startsWith(root+path.sep);
 if(inside(evidenceRoot,knowledgeRoot))throw Error('El destino de navegador no puede sobrescribir el discovery histórico.');
 if(process.env.IPANEMA_THEME_ROOT&&inside(evidenceRoot,path.resolve(process.env.IPANEMA_THEME_ROOT)))throw Error('La evidencia no puede escribirse dentro del tema.');
 function containsFiles(folder){if(!fs.existsSync(folder))return false;return fs.readdirSync(folder,{withFileTypes:true}).some(e=>e.isFile()||e.isSymbolicLink()||e.isDirectory()&&containsFiles(path.join(folder,e.name)));}
 if(containsFiles(evidenceRoot))throw Error('El destino ya contiene archivos; usa una ejecución nueva.');
 const engine=(await loadDependency('puppeteer')).default;
 const browser=await engine.launch({...options,executablePath:chromePath(engine),headless:true,args:options.args||['--disable-dev-shm-usage']});
 browser.on('targetcreated',target=>{if(target.type()==='page')target.page().then(page=>page&&protectPage(page,browser)).catch(()=>{browser.__protectionError=true;});});
 for(const page of await browser.pages())await protectPage(page,browser);
 const configure=context=>{const newPage=context.newPage.bind(context);context.newPage=async()=>protectPage(await newPage(),browser);return context;};
 configure(browser.defaultBrowserContext());
 const create=browser.createBrowserContext.bind(browser);browser.createBrowserContext=async(...args)=>configure(await create(...args));
 const newPage=browser.newPage.bind(browser);browser.newPage=async()=>protectPage(await newPage(),browser);
 for(const folder of ['screenshots','measurements/browser','measurements/crawl','measurements/responsive-matrix','screenshots/matrix','measurements/lighthouse'])fs.mkdirSync(path.join(evidenceRoot,folder),{recursive:true});
 return browser;
}};
export async function runtimeDoctor(){
 const dependencies={};for(const name of ['puppeteer','axe-core','lighthouse']){try{dependencies[name]={available:true,path:cliRequire.resolve(name)};}catch{dependencies[name]={available:false};}}
 let chrome=null;if(dependencies.puppeteer.available){try{chrome=chromePath((await loadDependency('puppeteer')).default);}catch{}}
 return {node:process.versions.node,os:process.platform,dependencies,chrome,network_performed:false};
}
export async function authenticate(browser,url){
 assertUrl(url);
 const secret=process.env.IPANEMA_AUDIT_PASSWORD;
 if(!secret)return [];
 const context=await browser.createBrowserContext();
 try{
  const page=await context.newPage();const entry=process.env.IPANEMA_AUDIT_ENTRY_URL||url;
  if(new URL(entry).origin!==new URL(url).origin)throw Error('La URL de acceso debe pertenecer al mismo origen.');
  const response=await page.goto(entry,{waitUntil:'networkidle2',timeout:45000});
  if([403,429].includes(response?.status()))throw Error('Acceso limitado. No reintentar automáticamente.');
  if(new URL(page.url()).pathname.startsWith('/password')){
   const input=await page.$('input[name="password"]');if(!input)throw Error('Pantalla de acceso sin el input esperado.');
   await input.type(secret);authPages.add(page);
   try{await Promise.all([page.waitForNavigation({waitUntil:'domcontentloaded',timeout:30000}),page.evaluate(()=>{const form=document.querySelector('input[name="password"]').form;if(!form)throw Error('Formulario ausente');form.requestSubmit();})]);}finally{authPages.delete(page);}
   if(new URL(page.url()).pathname.startsWith('/password'))throw Error('No se concedió acceso al storefront.');
  }
  return await context.cookies();
 }finally{await context.close();}
}
if(process.argv.includes('--doctor'))console.log(JSON.stringify(await runtimeDoctor()));
