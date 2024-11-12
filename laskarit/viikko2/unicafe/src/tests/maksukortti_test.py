import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_lataa_rahaa(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 11.00 euroa")

        self.maksukortti.lataa_rahaa(-100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_ota_rahaa(self):
        self.maksukortti.ota_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 9.00 euroa")

        self.maksukortti.ota_rahaa(-100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

        kortti = Maksukortti(1000)
        self.assertTrue(kortti.ota_rahaa(500))

        kortti = Maksukortti(1000)
        self.assertFalse(kortti.ota_rahaa(1500))

    def test_saldo_euroina(self):
        kortti = Maksukortti(1200)
        self.assertEqual(kortti.saldo_euroina(), 12)

        kortti = Maksukortti(999)
        self.assertEqual(kortti.saldo_euroina(), 9.99)