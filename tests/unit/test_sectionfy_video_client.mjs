// Standalone offline contract tests: source path and fresh result path supplied by caller.
import fs from 'node:fs/promises';
import vm from 'node:vm';
const [source,out]=process.argv.slice(2);if(!source||!out)throw Error('Indicar archivo fuente y salida nueva.');
const script=await fs.readFile(source,'utf8');const checks=[];
const check=(name,pass)=>{checks.push({name,status:pass?'passed':'failed'});if(!pass)throw Error(name);};
let fetches=[];let response={sections:{'video_banner-product-1-a':{estado:{lifecycle:'active',storefrontVisible:true},campos:{videoUrl:'https://cdn.example.com/a.mp4',videoMimeType:'video/mp4'}}}};let status=200;let redirect=false;let hang=false;
const context={URL,Promise,AbortController,setTimeout,clearTimeout,document:{readyState:'loading',addEventListener(){},querySelectorAll(){return[];}},window:{setTimeout,clearTimeout,Promise,AbortController,fetch:(url,opts)=>{fetches.push({url,opts});if(hang)return new Promise((resolve,reject)=>opts.signal.addEventListener('abort',()=>reject(new Error('aborted'))));return Promise.resolve({ok:status===200,status,redirected:redirect,json:()=>Promise.resolve(response)});}}};
vm.createContext(context);vm.runInContext(script,context);const api=context.window.Sectionfy;
const base='https://api.bbeboy.store/api/public/video-banner/{token}?placement=product&target_id=';
let result={at:new Date().toISOString(),scope:'Offline VM, mocked fetch only',checks};
try{
 check('legacy_api_preserved',typeof api.load==='function'&&typeof api.pick==='function'&&typeof api.register==='function');check('sectionfy_video_capability',typeof api.loadVideoBanner==='function'&&typeof api.selectVideoBanner==='function');
 await Promise.all([api.loadVideoBanner(base+'1','TEST'),api.loadVideoBanner(base+'1','TEST')]);check('one_request_per_endpoint',fetches.length===1);check('token_substitution',fetches[0].url.includes('/TEST?'));check('no_credentials',fetches[0].opts.credentials==='omit');check('reject_redirect_policy',fetches[0].opts.redirect==='error');check('fresh_per_page_policy',fetches[0].opts.cache==='no-store');
 await api.loadVideoBanner(base+'2','TEST');check('separate_endpoint_cache',fetches.length===2);
 const content='https://api.bbeboy.store/api/public/content/TEST/product/42';const before=fetches.length;await api.load('42','https://api.bbeboy.store/api/public/content','TEST');await api.loadVideoBanner(content,'TEST');check('shares_legacy_content_request',fetches.length===before+1);
 const content2='https://api.bbeboy.store/api/public/content/TEST/product/43';const second=fetches.length;await api.loadVideoBanner(content2,'TEST');await api.load('43','https://api.bbeboy.store/api/public/content','TEST');check('shares_video_first_content_request',fetches.length===second+1);
 const extra=fetches.length;await api.loadVideoBanner('https://sectionfy.codefy-apps.com/api/public/content/{token}/home-page','TEST');check('verified_home_host_allowed',fetches.length===extra+1&&fetches.at(-1).url==='https://sectionfy.codefy-apps.com/api/public/content/TEST/home-page');
 const selected=api.selectVideoBanner(response,'');check('ready_banner_selected',selected.length===1);check('wrong_instance_not_selected',api.selectVideoBanner(response,'other').length===0);
 const two=JSON.parse(JSON.stringify(response));two.sections['video_banner-product-1-b']=two.sections['video_banner-product-1-a'];let rejected=false;try{api.selectVideoBanner(two,'');}catch{rejected=true;}check('ambiguous_banner_rejected',rejected);check('exact_instance_selected',api.selectVideoBanner(two,'video_banner-product-1-b').length===1);
 for(const state of[{lifecycle:'draft',storefrontVisible:true},{lifecycle:'active',storefrontVisible:false},{lifecycle:'deleted',storefrontVisible:true}]){const x=JSON.parse(JSON.stringify(response));x.sections['video_banner-product-1-a'].estado=state;check('state_gate_'+state.lifecycle+'_'+state.storefrontVisible,api.selectVideoBanner(x,'').length===0);}
 check('unrelated_kind_excluded',api.selectVideoBanner({sections:{'faq-product-1-a':response.sections['video_banner-product-1-a']}},'').length===0);
 for(const [index,url]of['','http://api.bbeboy.store/api/public/video-banner/T','https://api.bbeboy.store.evil.example/api/public/video-banner/T','https://user:pass@api.bbeboy.store/api/public/video-banner/T','https://api.bbeboy.store/admin/T','https://api.bbeboy.store:444/api/public/video-banner/T','javascript:alert(1)'].entries()){
  const n=fetches.length;let fail=false;try{await api.loadVideoBanner(url,'TEST');}catch{fail=true;}check('reject_url_'+index,fail&&fetches.length===n);
 }
 for(const code of[403,429,500]){status=code;const n=fetches.length;const url=base+'error'+code;for(let i=0;i<2;i++){try{await api.loadVideoBanner(url,'TEST');}catch{}}check('no_retry_'+code,fetches.length===n+1);}
 status=200;redirect=true;let fails=false;try{await api.loadVideoBanner(base+'redirect','TEST');}catch{fails=true;}check('redirected_response_rejected',fails);
 await api.load('redirected-legacy','https://api.bbeboy.store/api/public/content','TEST');let sharedFails=false;try{await api.loadVideoBanner('https://api.bbeboy.store/api/public/content/TEST/product/redirected-legacy','TEST');}catch{sharedFails=true;}check('redirected_legacy_cache_not_trusted_for_video',sharedFails);redirect=false;
 for(const [index,body]of[null,{},[],{sections:[]},{sections:null}].entries()) {response=body;let fails=false;try{await api.loadVideoBanner(base+'shape'+index,'TEST');}catch{fails=true;}check('reject_shape_'+index,fails);}
 hang=true;const start=Date.now();let abort=false;try{await api.loadVideoBanner(base+'timeout','TEST');}catch{abort=true;}check('bounded_abort_timeout',abort&&Date.now()-start<5500&&fetches.at(-1).opts.signal.aborted);hang=false;
 const instance=context.window.Sectionfy;vm.runInContext(script,context);check('duplicate_client_init_idempotent',instance===context.window.Sectionfy);
 result.outcome='passed';
}catch(error){result.outcome='failed';result.error=error.message;}
await fs.writeFile(out,JSON.stringify(result,null,2),{flag:'wx'});console.log(JSON.stringify({outcome:result.outcome,checks:checks.length,error:result.error}));
if(result.outcome!=='passed')process.exitCode=1;
