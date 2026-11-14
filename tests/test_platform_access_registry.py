"""Offline catalogue consistency, not connector certification."""
from pathlib import Path
import csv
import importlib.util
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('daat_source_access',ROOT/'tools'/'daat_source_access.py')
mod=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=mod.load_registry()
        cls.rows=cls.doc['platforms']

    def test_schema(self):
        self.assertEqual(self.doc['schema'],'koa.daat.platform-access-registry.v1')

    def test_unique_ids(self):
        self.assertEqual(len({r['id'] for r in self.rows}),len(self.rows))

    def test_all_36_families_covered(self):
        covered={n for r in self.rows for n in r['family_ids']}
        self.assertEqual(covered,{f'{i:02d}' for i in range(1,37)})

    def test_all_access_modes_known(self):
        for r in self.rows:
            modes={a['mode'] for a in r['access_paths']}
            self.assertIn(r['preferred_path'],modes)
            self.assertLessEqual(modes,set(self.doc['method_legend']))

    def test_all_uncertified_and_without_canonical_authority(self):
        for r in self.rows:
            self.assertEqual(r['daat_connector_status'],'not_certified')
            self.assertEqual(r['owner_authorization_status'],'not_established')
            self.assertFalse(r['full_text_access_implied'])
            self.assertFalse(r['canonical_kristal_authority'])

    def test_medium_and_philpapers_different_paths(self):
        medium=mod.search(self.doc,query='Medium')[0]
        phil=mod.search(self.doc,query='PhilPapers')[0]
        self.assertIn('rss_atom',{a['mode'] for a in medium['access_paths']})
        self.assertIn('harvest_oai_pmh',{a['mode'] for a in phil['access_paths']})
        self.assertNotIn('api_read',{a['mode'] for a in medium['access_paths']})

    def test_verified_status_has_official_references(self):
        for r in self.rows:
            if r['platform_doc_status']=='official_docs_checked':
                self.assertTrue(r['source_reference_urls'])
                self.assertTrue(all(u.startswith('https://') for u in r['source_reference_urls']))

    def test_search_by_family(self):
        self.assertTrue(mod.search(self.doc,family='13'))
        self.assertEqual([],mod.search(self.doc,family='99'))

    def test_csv_json_platform_identity_parity(self):
        with (ROOT/'docs/data/platform-access-registry.v1.csv').open(encoding='utf-8-sig',newline='') as f:
            csv_ids={r['id'] for r in csv.DictReader(f)}
        self.assertEqual(csv_ids,{r['id'] for r in self.rows})

    def test_no_credentials_in_catalog(self):
        data=(ROOT/'docs/data/platform-access-registry.v1.json').read_text(encoding='utf-8')
        self.assertNotIn('-----BEGIN PRIVATE KEY-----',data)
        self.assertNotIn('sk_live_',data)

if __name__=='__main__': unittest.main()
