import pickle


with open('model_pickle', 'rb') as r:
    modelload = pickle.load(r)

luas_lantai = 1
lantai_tanah = 1
dinding_bambu = 1
tidak_punya_mck = 1
tidak_punya_listrik = 1
air_minum_sumur = 1
kayu_bakar = 1
daging_satu_seminggu = 1
satu_baju_setahun = 1
makan_satu_dua_sehari = 1
tidak_sanggup_berobat = 1
penghasilan_dibawah_600 = 1
kk_tidak_sekolah = 1
tidak_punya_tabungan = 1
lansia = 1
disabilitas = 1
usia_dini = 0
ibu_hamil = 0
anak_sd = 0
anak_smp = 0
anak_sma = 0

data = [
    luas_lantai,
    lantai_tanah,
    dinding_bambu,
    tidak_punya_mck,
    tidak_punya_listrik,
    air_minum_sumur,
    kayu_bakar,
    daging_satu_seminggu,
    satu_baju_setahun,
    makan_satu_dua_sehari,
    tidak_sanggup_berobat,
    penghasilan_dibawah_600,
    kk_tidak_sekolah,
    tidak_punya_tabungan,
    lansia,
    disabilitas,
    usia_dini,
    ibu_hamil,
    anak_sd,
    anak_smp,
    anak_sma,
]

predicted = modelload.predict([data])
print(predicted)
