"""Datos sintéticos: las cifras sirven para probar contradicciones, no son catálogo."""
import json
from pathlib import Path
import tempfile
import unittest

from tests.support import make_project, put
from ipanema.core import Project, IpanemaError, digest
from ipanema.seo.extractor import extract, parse_json_ld
from ipanema.seo.schema_graph import build_graph
from ipanema.seo.schema_validator import validate
from ipanema.seo.generator import generate, safe_json, repair_trailing_json, checked_facts
from ipanema.seo.page_audit import audit_html, internal_architecture
from ipanema.seo.source_audit import breadcrumb_proposal

URL='https://example.invalid/products/fixture'


def html(node, extra=''):
    return '<title>Fixture</title><link rel="canonical" href="'+URL+'"><h1>Fixture</h1>'+extra+'<script type="application/ld+json">'+json.dumps(node)+'</script>'


def product(**values):
    return {'@context':'https://schema.org','@type':'Product','@id':URL+'#product','name':'Fixture','url':URL,
            'image':'https://example.invalid/image.webp','offers':{'@type':'Offer','price':'12.50','priceCurrency':'MXN','availability':'https://schema.org/InStock'},**values}


def rules(result):
    return {f['rule'] for f in result['findings']}


class Extraction(unittest.TestCase):
    def test_coordinator_distinguishes_editor_and_commerce_schema(self):
        from ipanema.coordinator import route
        self.assertIn('ipanema-seo-expert',route('Corrige el schema de Product con Offer')['skills'])
        self.assertNotIn('ipanema-seo-expert',route('Modifica el schema del hero en el editor')['skills'])

    def test_valid_and_invalid_json(self):
        self.assertIsNone(parse_json_ld('{"x":1}')[1])
        self.assertIsNotNone(parse_json_ld('{"x":1,}')[1])
        self.assertIsNotNone(parse_json_ld('{"x":NaN}')[1])
        self.assertIsNotNone(parse_json_ld('{"x":1,"x":2}')[1])

    def test_syntax_not_google_eligibility(self):
        result=validate(extract(html({'@context':'https://schema.org','@type':'Product'}),URL),'product')
        self.assertTrue(result['states']['syntax_valid'])
        self.assertIn('C110',rules(validate(extract(html(product(offers={'@type':'Offer'})),URL),'product')))
        self.assertEqual(result['states']['confirmed_by_external_tool'],'not_checked')
        self.assertIn('C101',rules(result))

    def test_absence_is_not_a_pass(self):
        result=validate(extract('',URL),'product')
        self.assertIsNone(result['states']['syntax_valid'])
        self.assertIsNone(result['states']['semantic_valid_for_checked_rules'])
        self.assertEqual(result['states']['google_requirements_met_by_feature']['merchant_listing'],'not_present')

    def test_microdata_nested(self):
        snap=extract('<div itemscope itemtype="https://schema.org/Product"><span itemprop="name">Fixture</span><div itemprop="offers" itemscope itemtype="https://schema.org/Offer"><meta itemprop="price" content="12.50"><meta itemprop="priceCurrency" content="MXN"></div></div>',URL)
        self.assertEqual(snap['microdata'][0]['obj']['name'],'Fixture')
        self.assertEqual(snap['microdata'][0]['obj']['offers']['price'],'12.50')
        self.assertIn('Offer',build_graph(snap)['types'])

    def test_rdfa_and_limit(self):
        snap=extract('<div vocab="https://schema.org/" typeof="Product" about="#p"><span property="name">Fixture</span><div property="offers" typeof="Offer"><meta property="price" content="12.50"></div></div>',URL)
        graph=build_graph(snap)
        self.assertIn('Product',graph['types']);self.assertIn('Offer',graph['types'])
        self.assertEqual(sum('Offer' in e['types'] for e in graph['raw_entities']),1)

    def test_graph_complementary_and_external_reference(self):
        nodes={'@context':'https://schema.org','@graph':[{'@type':'Product','@id':'#p','name':'Fixture'},
                  {'@id':'#p','image':'https://example.invalid/image.webp'},
                  {'@type':'WebPage','mainEntity':{'@id':'#p'},'publisher':{'@id':'https://example.invalid/#organization'}}]}
        graph=build_graph(extract(html(nodes),URL))
        self.assertFalse(graph['conflicts']);self.assertFalse(graph['duplicates'])
        result=validate(extract(html(nodes),URL),'product')
        self.assertNotIn('G003',rules(result));self.assertIn('G004',rules(result))
        self.assertNotIn('C101', [f['rule'] for f in result['findings'] if 'image' in f['message']])

    def test_duplicate_conflicting_price_and_app_source(self):
        a=product();b=product();b['offers']['price']='99'
        content=html(a)+'<script type="application/ld+json" data-component="third-party">'+json.dumps(b)+'</script>'
        result=validate(extract(content,URL),'product')
        self.assertTrue(result['graph']['duplicates']);self.assertTrue(result['graph']['conflicts'])

    def test_name_is_not_identity(self):
        nodes={'@context':'https://schema.org','@graph':[{'@type':'Product','name':'Same'},{'@type':'Product','name':'Same'}]}
        self.assertFalse(build_graph(extract(html(nodes),URL))['duplicates'])

    def test_empty_and_correct_breadcrumb(self):
        empty={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[]}
        self.assertIn('C220',rules(validate(extract(html(empty),URL),'category')))
        empty['itemListElement']=[{'@type':'ListItem','position':1,'name':'Home','item':'https://example.invalid/'},
                                 {'@type':'ListItem','position':2,'name':'Category'}]
        self.assertNotIn('C220',rules(validate(extract(html(empty),URL),'category')))

    def test_list_positions_can_span_pages_and_direct_entities(self):
        node={'@context':'https://schema.org','@type':'ItemList','itemListElement':[{'@type':'ListItem','position':21,'url':URL}]}
        self.assertNotIn('B051',rules(validate(extract(html(node),URL),'category')))
        node['itemListElement']=[{'@type':'Product','name':'Fixture'}]
        self.assertNotIn('B051',rules(validate(extract(html(node),URL),'category')))

    def test_price_and_availability_consistency(self):
        result=validate(extract(html(product()),URL),'product',{'price':'13','currency':'USD','availability':'OutOfStock','sku':'known'})
        self.assertTrue({'D020','D030','D040'} <= rules(result))
        self.assertNotIn('D060',rules(result))  # Missing SKU is not a fake contradiction.
        self.assertIn('C121',rules(result))

    def test_price_specification_and_zero(self):
        node=product(offers={'@type':'Offer','priceSpecification':{'@type':'UnitPriceSpecification','price':'12.50','priceCurrency':'MXN'}})
        result=validate(extract(html(node),URL),'product')
        self.assertNotIn('C110',rules(result));self.assertNotIn('C152',rules(result))
        node['offers']['priceSpecification']['price']='0'
        self.assertIn('C111',rules(validate(extract(html(node),URL),'product')))

    def test_variants_not_compared_to_one_price_or_canonical(self):
        first=product(sku='a',url=URL+'?variant=a');second=product(sku='b',url=URL+'?variant=b')
        first.pop('@id');second.pop('@id');second['offers']['price']='15'
        node={'@context':'https://schema.org','@type':'ProductGroup','name':'Fixture','productGroupID':'group-real-fixture',
              'variesBy':['https://schema.org/color'],'hasVariant':[first,second]}
        facts={'variants':[{'sku':'a','url':first['url'],'price':'12.50'},{'sku':'b','url':second['url'],'price':'15'}]}
        result=validate(extract(html(node),URL),'product',facts)
        self.assertNotIn('D020',rules(result));self.assertNotIn('D010',rules(result));self.assertNotIn('C144',rules(result))

    def test_article_dates_and_author_are_not_invented(self):
        node={'@context':'https://schema.org','@type':'BlogPosting','headline':'Fixture'}
        result=validate(extract(html(node),URL),'post')
        self.assertIn('C301',rules(result));self.assertFalse(any(f['severity']=='error' for f in result['findings']))
        node.update({'author':'Unknown raw author','datePublished':'2026-02-31'})
        result=validate(extract(html(node),URL),'post')
        self.assertIn('B030',rules(result));self.assertIn('B100',rules(result))

    def test_unverified_reviews_and_policies(self):
        node=product(aggregateRating={'@type':'AggregateRating','ratingValue':5,'reviewCount':1})
        node['offers']['shippingDetails']={'@type':'OfferShippingDetails'}
        result=validate(extract(html(node),URL),'product')
        self.assertTrue({'D080','D090','C113'} <= rules(result))

    def test_carousel_links_dom_and_unreachable_pagination(self):
        initial='<title>Fixture</title><h1>Fixture</h1><div class="swiper"><a href="/products/fixture">Fixture</a><a onclick="go()">Broken</a></div><a class="load-more">Ver más</a>'
        with tempfile.TemporaryDirectory() as tmp:
            p=Project(make_project(Path(tmp)))
            result=audit_html(p,initial,URL,'category',status=200,rendered_html=initial+'<a href="/products/late">Late</a>',no_js_html=initial)
            self.assertTrue({'SEO010','SEO011','SEO020'} <= rules(result))
            self.assertEqual(result['html_dom_comparison']['links_only_after_js'],['https://example.invalid/products/late'])
            self.assertFalse(result['indexation_verified'])

    def test_canonical_query_mismatch_and_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Project(make_project(Path(tmp)))
            result=audit_html(p,html(product()),URL+'?variant=a','product',status=200,headers={'X-Robots-Tag':'noindex'})
            self.assertEqual(result['indexability_observable'],'noindex_observed')
            self.assertIn('SEO006',rules(result))

    def test_native_controls_are_not_destination_links(self):
        content='<h1>Fixture</h1><main><div class="swiper"><a class="js-variant-button">M</a><a href="#" class="js-product-thumb">Thumbnail</a><a href="/product">Product</a></div><a href="#" class="js-accordion-private-toggle">Ver más</a></main><a href="#" class="js-modal-close-private">Ver más productos</a>'
        with tempfile.TemporaryDirectory() as tmp:
            p=Project(make_project(Path(tmp)))
            result=audit_html(p,content,URL,'category')
            self.assertNotIn('SEO010',rules(result));self.assertNotIn('SEO011',rules(result))
            self.assertEqual(len(result['crawl']['non_navigation_carousel_controls']),2)


class Generation(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.project=Project(make_project(self.root))
        self.doc={'project':'sample','url':URL,'page_type':'product','source':{'kind':'synthetic_fixture','observed_at':'2026-11-08'},
                  'data':{'product':{'name':'Fixture','price':'12.50','currency':'MXN','image':'https://example.invalid/image.webp','sku':'actual-fixture'}}}

    def tearDown(self):self.tmp.cleanup()

    def test_safe_serialization_and_repair(self):
        text='</script>\u2028& "quote"'
        raw=safe_json({'name':text})
        self.assertNotIn('</script>',raw);self.assertEqual(json.loads(raw)['name'],text)
        self.assertEqual(json.loads(repair_trailing_json('{"x":"a,}",}')['json']),{'x':'a,}'})
        with self.assertRaises(IpanemaError):repair_trailing_json('{x:1}')

    def test_generate_minimal_does_not_invent(self):
        result=generate(self.project,self.doc,'Product',fixture=True)
        self.assertEqual(result['data']['offers']['price'],'12.50')
        for absent in ('availability','shippingDetails','hasMerchantReturnPolicy','priceValidUntil'):
            self.assertNotIn(absent,result['data']['offers'])
        self.assertNotIn('gtin',result['data']);self.assertNotIn('aggregateRating',result['data'])

    def test_product_on_category_refused(self):
        self.doc['page_type']='category'
        with self.assertRaises(IpanemaError):generate(self.project,self.doc,'Product',fixture=True)

    def test_data_project_domain_and_evidence_hash(self):
        self.doc['project']='other'
        with self.assertRaises(IpanemaError):checked_facts(self.project,self.doc,fixture=True)
        self.doc['project']='sample';self.doc['url']='https://other.invalid/p'
        with self.assertRaises(IpanemaError):checked_facts(self.project,self.doc,fixture=True)
        self.doc['url']=URL
        path=self.root/'reports/runs/catalog.json';put(path,{'project':'sample','url':URL,'data':self.doc['data']})
        self.doc['source']={'kind':'authorized_catalog_export','observed_at':'2026-11-08','reference':'reports/runs/catalog.json','sha256':digest(path)}
        self.assertEqual(checked_facts(self.project,self.doc)[0],self.doc['data'])
        put(path,{'data':{}})
        with self.assertRaises(IpanemaError):checked_facts(self.project,self.doc)

    def test_duplicates_and_native_invalid_block_new_generation(self):
        snap=extract(html(product()),URL)
        with self.assertRaises(IpanemaError):generate(self.project,self.doc,'Product',snapshot=snap,fixture=True)
        invalid=extract('<script type="application/ld+json">{"x":1,}</script>',URL)
        with self.assertRaises(IpanemaError):generate(self.project,self.doc,'Product',snapshot=invalid,fixture=True)

    def test_update_preserves_identity(self):
        snap=extract(html(product()),URL)
        result=generate(self.project,self.doc,'Product',snapshot=snap,mode='update',fixture=True)
        self.assertEqual(result['data']['@id'],URL+'#product')
        self.assertEqual(result['action'],'replace_existing_at_source')

    def test_no_unverified_reviews_or_free_shipping(self):
        for key,value in [('reviews',{'aggregateRating':{'ratingValue':5}}),('policies',{'shippingDetails':{'shippingRate':0}})]:
            self.doc['data'][key]=value
            with self.assertRaises(IpanemaError):generate(self.project,self.doc,'Product',fixture=True)
            self.doc['data'].pop(key)

    def test_no_variant_urls_invented(self):
        self.doc['data']['product'].update({'productGroupID':'g','variesBy':['color'],'variants':[{},{}]})
        with self.assertRaises(IpanemaError):generate(self.project,self.doc,'ProductGroup',fixture=True)

    def test_article_no_audit_date_as_publication(self):
        self.doc['page_type']='post';self.doc['data']={'article':{'headline':'Fixture'}}
        result=generate(self.project,self.doc,'BlogPosting',fixture=True)
        self.assertNotIn('dateModified',result['data']);self.assertNotIn('author',result['data'])

    def test_fixture_is_never_default(self):
        with self.assertRaises(IpanemaError):generate(self.project,self.doc,'Product')

    def test_native_patch_does_not_touch_theme(self):
        src='''<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","breadcrumb":{"@type":"BreadcrumbList","itemListElement":[{"name":"Home"}{% if template != 'home' %},{% endif %}{% if template == 'page' or template == 'cart' or template == 'search' or template == 'account.order' %}{"name":"Current"}{% else %}{% for crumb in breadcrumbs %}{"name":"Crumb"}{% if not loop.last %},{% endif %}{% endfor %}{% endif %}]}}</script>'''
        path=self.root/'theme/snippets/structured-data/structured-data.tpl';put(path,src)
        before=digest(path);proposal=breadcrumb_proposal(self.project.require_theme())
        self.assertEqual(digest(path),before);self.assertEqual(proposal['status'],'proposal_only')
        self.assertEqual(sum(c['after']['invalid_json_blocks'] for c in proposal['cases']),0)
        self.assertGreater(sum(c['before']['invalid_json_blocks'] for c in proposal['cases']),0)


if __name__=='__main__':unittest.main()
