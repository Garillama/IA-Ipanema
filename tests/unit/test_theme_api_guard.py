"""Guardia del CLI nativo con transporte simulado; no cambia instalaciones remotas."""
import json
import subprocess
import unittest
from tests.support import ROOT


class ThemeGuardTests(unittest.TestCase):
    def test_single_clone_stop_limits_and_draft_file_scope(self):
        module=(ROOT/'tools/theme_api_guard.mjs').as_uri()
        script='''import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {guardedFetch} from MODULE;
const root='https://api.tiendanube.com/v1/1/theme-installations/';
let calls=0;
const ok=async()=>{calls++;return new Response('{}',{status:200});};
let clone=guardedFetch(ok,{mode:'clone',sourceId:'123'});
await clone(root+'123/clone',{method:'POST',body:JSON.stringify({title:'QA'})});
await assert.rejects(()=>clone(root+'123/clone',{method:'POST',body:JSON.stringify({title:'QA'})}));
assert.equal(calls,1);
for(const status of [403,429,503]){
 let count=0;const fetch=guardedFetch(async()=>{count++;return new Response('{}',{status});},{mode:'clone',sourceId:'123'});
 await assert.rejects(()=>fetch(root+'123/clone',{method:'POST',body:JSON.stringify({title:'QA'})}));
 await assert.rejects(()=>fetch(root+'123/clone',{method:'POST',body:JSON.stringify({title:'QA'})}));
 assert.equal(count,1);
}
const push=guardedFetch(ok,{mode:'push',targetId:'456',publishedId:'123',files:['static/css/damar.css']});
const body=JSON.stringify({upsert:[{path:'static/css/damar.css',content:'a{}'}],delete:[]});
await assert.rejects(()=>push(root+'123/files',{method:'PATCH',body}));
await assert.rejects(()=>push(root+'456/publish',{method:'POST',body:'{}'}));
await assert.rejects(()=>push(root+'456/files',{method:'PATCH',body:JSON.stringify({upsert:[{path:'layouts/layout.tpl'}]})}));
await push(root+'456/files',{method:'PATCH',body});
await assert.rejects(()=>push(root+'456/files',{method:'PATCH',body}));
const production=guardedFetch(ok,{mode:'production-push',targetId:'123',publishedId:'123',files:['static/css/damar.css'],expectedHashes:{'static/css/damar.css':createHash('sha256').update('a{}').digest('hex')}});
await assert.rejects(()=>production(root+'123/publish',{method:'POST',body:'{}'}));
await assert.rejects(()=>production(root+'456/files',{method:'PATCH',body}));
await production(root+'123/files',{method:'PATCH',body});
console.log('GUARD_VERIFIED');'''.replace('MODULE',json.dumps(module))
        result=subprocess.run(['node','--input-type=module'],input=script,capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('GUARD_VERIFIED',result.stdout)


if __name__=='__main__':unittest.main()
