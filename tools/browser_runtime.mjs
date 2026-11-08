import {createRequire} from 'node:module';
export const cliRequire=createRequire('/home/alanrichard/.local/lib/node_modules/@tiendanube/cli/package.json');
export const {default:puppeteer}=await import(cliRequire.resolve('puppeteer'));
export async function authenticate(browser,url){
 const secret=process.env.IPANEMA_AUDIT_PASSWORD;
 if(!secret)return [];
 const context=await browser.createBrowserContext();
 try{
  const page=await context.newPage();
  const entry=process.env.IPANEMA_AUDIT_ENTRY_URL||url;
  if(new URL(entry).origin!==new URL(url).origin)throw Error('La URL de acceso debe pertenecer al mismo origen.');
  const response=await page.goto(entry,{waitUntil:'networkidle2',timeout:45000});
  if([403,429].includes(response?.status()))throw Error('Acceso limitado por HTTP '+response.status()+'. No reintentar automáticamente.');
  if(new URL(page.url()).pathname.startsWith('/password')){
   const input=await page.$('input[name="password"]');
   if(!input)throw Error('Pantalla de acceso sin el input esperado; inspeccionar antes de continuar.');
   await input.type(secret);
   await Promise.all([
    page.waitForNavigation({waitUntil:'domcontentloaded',timeout:30000}),
    page.evaluate(()=>{const form=document.querySelector('input[name="password"]').form;if(!form)throw Error('Formulario ausente');form.requestSubmit();})
   ]);
   if(new URL(page.url()).pathname.startsWith('/password'))throw Error('El formulario no concedió acceso al storefront.');
  }
  return await context.cookies();
 }finally{await context.close();}
}
