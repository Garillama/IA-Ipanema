# Source and contract checks for the scoped Rhino blog performance patch.
import sys,json,pathlib,re,ast,argparse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'tools'))
from ipanema.core import Project,write_json,digest,now
parser=argparse.ArgumentParser();parser.add_argument('--run',required=True,type=pathlib.Path);parser.add_argument('--baseline-run',required=True,type=pathlib.Path);parser.add_argument('--applied',action='store_true');args=parser.parse_args();p=Project(project_id='rhino-performance');root=p.require_theme();r=args.run.resolve();checks=[]
def check(n,b,details=None):checks.append({'name':n,'status':'passed'if b else'failed','details':details})
patches=json.load(open(r/'patches.json'));b=(r/'before/sections/main-blog.tpl').read_text();a=(r/'candidate/sections/main-blog.tpl').read_text();expr=re.search(r'card_image_priority_high:\s*([^,]+),',a).group(1);expr=expr.replace('loop.first','first').replace('params.view','view').replace('params.tag','tag');parsed=ast.parse(expr,mode='eval')
def evaluate(n,v):
 if isinstance(n,ast.Expression):return evaluate(n.body,v)
 if isinstance(n,ast.Name):assert n.id in v;return v[n.id]
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.BoolOp):assert isinstance(n.op,ast.And);return all(evaluate(x,v)for x in n.values)
 if isinstance(n,ast.UnaryOp):assert isinstance(n.op,ast.Not);return not evaluate(n.operand,v)
 if isinstance(n,ast.Compare):
  assert len(n.ops)==1;left,right=evaluate(n.left,v),evaluate(n.comparators[0],v)
  if isinstance(n.ops[0],ast.Eq):return left==right
  if isinstance(n.ops[0],ast.NotEq):return left!=right
 raise ValueError('Unsupported expression node '+type(n).__name__)
cases=[]
for case,values,expected in [('normal',dict(template='blog',view='',tag='',show_image=True),True),('page2',dict(template='blog',view='',tag='',show_image=True),True),('index_fragment',dict(template='blog',view='cards',tag='',show_image=True),False),('filtered_landing',dict(template='blog',view='',tag='Recovery',show_image=True),False),('images_disabled',dict(template='blog',view='',tag='',show_image=False),False),('other_template',dict(template='product',view='',tag='',show_image=True),False)]:
 flags=[bool(evaluate(parsed,{**values,'first':i==0}))for i in range(3)];check('gate:'+case,flags==[expected,False,False],flags);cases.append({'name':case,'flags':flags,'show_image':values['show_image']})
card=patches['snippets/blog-card.tpl'];check('default_false','{% set card_image_priority_high = card_image_priority_high ?? false %}'in card);check('explicit_both_branches',card.count('image_priority_high: card_image_priority_high,')==2)
for n in('sections/blog-carousel.tpl','sections/blog-post-related.tpl','sections/home-news.tpl'):check('consumer_false:'+n,'card_image_priority_high: false,'in patches[n])
consumers=[]
for d in ('sections','blocks','snippets'):
 for f in(root/d).rglob('*.tpl'):
  if "'snippets/blog-card.tpl'"in f.read_text():consumers.append(str(f.relative_to(root)))
check('all_consumers_accounted',sorted(consumers)==sorted(['sections/main-blog.tpl','sections/blog-carousel.tpl','sections/blog-post-related.tpl','sections/home-news.tpl']),consumers)
helper=(root/'snippets/image.tpl').read_text();check('native_helper_disables_both_lazy','{% set image_lazy = image_lazy and not image_priority_high %}'in helper and'{% set image_lazy_js = image_lazy_js and not image_priority_high %}'in helper);check('native_helper_eager_src','{% else %}\n\t\t\t\tsrc="{{ src }}"'in helper);check('native_helper_high_attribute','fetchpriority="high"'in helper)
css=(root/'static/css/style-critical.css').read_text();m=re.search(r'\.fade-in\s*\{[^}]*\}',css);m2=re.search(r'\.fade-in\.lazyloaded,[\s\S]*?\.fade-in\.image-priority-high\s*\{[^}]*\}',css);assert m and m2;check('native_css_high_priority_visible','opacity: 1' in m2.group())
template=json.load(open(root/'templates/pages/blog.json'));enabled=[template['sections'][k]['type']for k in template['order']if not template['sections'][k].get('disabled',False)];check('current_first_visible_section',enabled[0]=='main-blog',enabled)
# Current published baseline: first card actually above fold in three independent mobile samples.
prior=args.baseline_run.resolve();lh=json.load(open(prior/'blog-mobile-performance.json'))['result'];bounds=[]
for s in lh['samples']:
 items=s['observations']['audits']['lcp-breakdown-insight']['details']['items'];nodes=[x for x in items if x.get('type')=='node'];bounds.append(nodes[0].get('boundingRect'));check('observed_first_card_above_fold:'+s['measured_at'],'blog-card-img'in nodes[0].get('selector','')and 0<=bounds[-1]['top']<s['profile']['screen']['height'],bounds[-1])
for n in patches:
 check('current_source_hash:'+n,digest(root/n)==digest(r/('candidate'if args.applied else'before')/n));old=(r/'before'/n).read_text();new=(r/'candidate'/n).read_text();check('no_new_js_or_important:'+n,new.count('<script')==old.count('<script')and new.count('!important')==old.count('!important'))
 for t in re.findall(r'{%[\s\S]*?%}',new):assert'{#'not in t,'Comment inside Twig statement'
 for sch in re.findall(r'{% schema %}([\s\S]*?){% endschema %}',new):json.loads(sch)
 check('schema_unchanged:'+n,re.findall(r'{% schema %}([\s\S]*?){% endschema %}',new)==re.findall(r'{% schema %}([\s\S]*?){% endschema %}',old))
proof={'at':now(),'project':p.id,'kind':'static_candidate_qa','checks':checks,'outcome':'passed'if all(x['status']=='passed'for x in checks)else'failed','limits':['Expression evaluator is restricted and source-bound; not a full Twig renderer.','Current template composition and prior observed LCP location checked; future reordered layouts require revalidation.']};write_json(r/'static-qa.json',proof,overwrite=True)
write_json(r/'browser-cases.json',{'cases':cases,'native_css':m.group()+'\n'+m2.group(),'helper_sha256':digest(root/'snippets/image.tpl'),'candidate_card_sha256':digest(r/'candidate/snippets/blog-card.tpl'),'projection':'Source-bound boolean and native image attribute branches; no platform renderer.','selector':'.blog-card-img'},overwrite=True);print(json.dumps({'checks':len(checks),'outcome':proof['outcome'],'failed':[x for x in checks if x['status']=='failed']}))
