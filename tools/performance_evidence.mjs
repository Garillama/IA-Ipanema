// Evidence only: retain browser/Lighthouse observations without inventing attribution.
// Standalone function: Puppeteer serializes it into the page, without module closures.
export function installPerformanceObservers(){
 const clean=value=>{
  if(typeof value!=='string'||!value)return null;
  if(value.startsWith('data:'))return '[inline-resource]';
  try{const u=new URL(value,location.href);u.username='';u.password='';u.hash='';for(const k of [...u.searchParams.keys()])if(/token|secret|password|auth|session|email|phone|api.?key/i.test(k))u.searchParams.set(k,'[redacted]');return u.href;}catch{return null;}
 };
 const srcset=value=>!value?null:value.split(',').map(part=>{const [url,...descriptor]=part.trim().split(/\s+/);return [clean(url),...descriptor].join(' ');}).join(', ');
 window.__audit={lcp:[],shifts:[],longTasks:[]};
 for(const [type,key] of [['largest-contentful-paint','lcp'],['layout-shift','shifts'],['longtask','longTasks']]){
  try{new PerformanceObserver(list=>window.__audit[key].push(...list.getEntries().map(e=>{
   const row={startTime:e.startTime,duration:e.duration,value:e.value,hadRecentInput:e.hadRecentInput,size:e.size};
   if(key==='lcp'){
    const element=e.element;
    Object.assign(row,{url:clean(e.url||element?.currentSrc||''),renderTime:e.renderTime,loadTime:e.loadTime,
     tag:element?.tagName||null,id:element?.id&&/^[a-zA-Z0-9_-]{1,200}$/.test(element.id)?element.id:null,
     currentSrc:clean(element?.currentSrc||''),srcset:srcset(element?.getAttribute?.('srcset')),sizes:element?.getAttribute?.('sizes')||null,
     loading:element?.loading||null,fetchPriority:element?.fetchPriority||null,
     // Each picture source is retained independently; no guesses about selected downloads.
     sources:[...(element?.closest?.('picture')?.querySelectorAll('source')||[])].map(s=>({media:s.media,type:s.type,sizes:s.sizes,srcset:srcset(s.srcset)})),
     attribution:'observed-browser-entry; resource timing and navigation must be matched before decomposition'});
   }
   return row;
  }))).observe({type,buffered:true});}catch{}
 }
}

// Do not persist the full LHR: node snippets and URL credentials can contain private data.
export function lighthouseEvidence(lhr){
 const ids=['lcp-breakdown-insight','lcp-discovery-insight','largest-contentful-paint-element',
  'network-requests','server-response-time','render-blocking-insight','render-blocking-resources',
  'font-display-insight','mainthread-work-breakdown','bootup-time'];
 const sanitize=(value,key='')=>{
  if(/token|secret|password|cookie|authorization|session|email|phone|snippet|nodeLabel/i.test(key))return '[redacted]';
  if(Array.isArray(value))return value.map(x=>sanitize(x));
  if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,sanitize(v,k)]));
  if(typeof value==='string'&&/^https?:\/\//i.test(value)){
   try{const u=new URL(value);u.username='';u.password='';u.hash='';for(const k of [...u.searchParams.keys()])if(/token|secret|password|auth|session|email|phone|api.?key/i.test(k))u.searchParams.set(k,'[redacted]');return u.href;}catch{return '[invalid-url]';}
  }
  if(typeof value==='string'&&value.startsWith('data:'))return '[inline-resource]';
  return value;
 };
 const audits={};const missing=[];
 for(const id of ids){
  const audit=lhr?.audits?.[id];
  if(!audit){missing.push(id);continue;}
  audits[id]=sanitize({score:audit.score,scoreDisplayMode:audit.scoreDisplayMode,numericValue:audit.numericValue,
   numericUnit:audit.numericUnit,details:audit.details,errorMessage:audit.errorMessage});
 }
 return {measurement:'lighthouse-laboratory',audits,not_available:missing,
  attribution:'Original Lighthouse audit details only; no inferred percentages. Missing audits may depend on version or page.',
  field_inp:null};
}

// CDP reuses requestId across redirects. Keep one observation per HTTP hop instead
// of replacing the preceding response. Never retain headers, cookies or postData.
export function createNetworkRecorder(cleanUrl=value=>value){
 const active=new Map(),records=[];
 const bytes=value=>Number.isFinite(value)&&value>=0?value:null;
 const response=(row,value)=>Object.assign(row,{status:value.status,mime:value.mimeType,
  from_disk_cache:!!value.fromDiskCache,from_service_worker:!!value.fromServiceWorker});
 return {
  requestWillBeSent(event,phase){
   let previous=active.get(event.requestId);
   if(event.redirectResponse){
    if(!previous){
     previous={request_id:event.requestId,redirect_hop:0,url:cleanUrl(event.redirectResponse.url),type:event.type,
      requested:false,phase,missing_request_event:true};records.push(previous);
    }
    response(previous,event.redirectResponse);
    Object.assign(previous,{completed:true,redirect:true,redirect_to:cleanUrl(event.request.url),
     finish_timestamp:event.timestamp,encoded_bytes:bytes(event.redirectResponse.encodedDataLength),
     encoded_bytes_basis:'redirectResponse.encodedDataLength'});
   }
   const row={request_id:event.requestId,redirect_hop:event.redirectResponse?(previous?.redirect_hop??0)+1:0,
    url:cleanUrl(event.request.url),method:event.request.method,type:event.type,requested:true,phase,
    request_timestamp:event.timestamp};
   records.push(row);active.set(event.requestId,row);
  },
  responseReceived(event){
   const row=active.get(event.requestId);if(!row)return;
   response(row,event.response);row.response_timestamp=event.timestamp;
  },
  loadingFinished(event){
   const row=active.get(event.requestId);if(!row)return;
   Object.assign(row,{completed:true,finish_timestamp:event.timestamp,encoded_bytes:bytes(event.encodedDataLength),
    encoded_bytes_basis:'loadingFinished.encodedDataLength'});active.delete(event.requestId);
  },
  loadingFailed(event){
   const row=active.get(event.requestId);if(!row)return;
   Object.assign(row,{completed:false,error:event.errorText,finish_timestamp:event.timestamp});active.delete(event.requestId);
  },
  snapshot(){return records.map(row=>({...row}));}
 };
}
