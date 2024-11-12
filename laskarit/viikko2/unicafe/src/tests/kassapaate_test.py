import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)


    def test_kassapaate_saldo_alussa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kassapaate_syo_edullisesti_kateisella(self):
        maksu = 500
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(maksu)
        self.assertEqual(vaihtoraha, maksu - 240)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

        maksu = 200
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(maksu)
        self.assertEqual(vaihtoraha, maksu)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_kassapaate_syo_maukkaasti_kateisella(self):
        maksu = 500
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(maksu)
        self.assertEqual(vaihtoraha, maksu - 400)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

        maksu = 200
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(maksu)
        self.assertEqual(vaihtoraha, maksu)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_kassapaate_syo_edullisesti_kortilla(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.maksukortti.saldo_euroina(), 7.60)

        kortti = Maksukortti(100)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(kortti))
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(kortti.saldo_euroina(), 1.00)

    def test_kassapaate_syo_maukkaasti_kortilla(self):
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.maksukortti.saldo_euroina(), 6.00)

        kortti = Maksukortti(100)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(kortti.saldo_euroina(), 1.00)

    def test_lataaa_rahaa_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 11.00)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 11.00)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_kassassa_rahaa_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)