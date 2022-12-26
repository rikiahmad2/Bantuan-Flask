import json
from flask import Flask, render_template, request, jsonify
import pickle
app = Flask(__name__)

@app.route('/')
def index():
    title= 'Home'
    active1= 'current'
    return render_template('index.html', title=title, active1=active1)


@app.route('/form')
def form():
    title= 'Form'
    active2='current'
    return render_template('form.html', active2=active2, title=title)


@app.route('/about')
def about():
    title= 'About'
    active3='current'
    return render_template('about.html', active3=active3, title=title)

@app.route('/form_post', methods=['POST'])
def form_post():
    with open('model_pickle', 'rb') as r:
        modelload = pickle.load(r)
    form = request.form
    luas_lantai = form['luas_lantai']
    luas_lantai = int(luas_lantai)
    if(luas_lantai >= 60):
        luas_lantai = '0'
    else :
        luas_lantai = '1'      
    dataArray = [
        luas_lantai,
        form['lantai_tanah'],
        form['dinding_bambu'],
        form['tidak_punya_mck'],
        form['tidak_punya_listrik'],
        form['air_minum_sumur'],
        form['kayu_bakar'],
        form['daging_satu_seminggu'],
        form['satu_baju_setahun'],
        form['makan_satu_dua_sehari'],
        form['tidak_sanggup_berobat'],
        form['penghasilan_dibawah_600'],
        form['kk_tidak_sekolah'],
        form['tidak_punya_tabungan'],
        form['lansia'],
        form['disabilitas'],
        form['usia_dini'],
        form['ibu_hamil'],
        form['anak_sd'],
        form['anak_smp'],
        form['anak_sma'],
    ]
    predicted = modelload.predict([dataArray])
    finaldata = json.dumps(predicted.tolist())
    result = finaldata[1]
    reason = arrayCheck(dataArray)
    if(result == '2'):
        data = 'Tidak Berhak Mendapat Bantuan'
        icon = 'cancel.svg'
    if(result == '0'):
        data = 'Bantuan BLT'
        icon = 'love.svg'
    if(result == '1'):
        data = 'Bantuan PKH'
        icon = 'info.svg'
    title= 'Result'
    return render_template('result.html', title=title, data=data, icon=icon, reason=reason, len=len(reason))

def arrayCheck(array):
    data = []
    for idx, val in enumerate(array):
        if(array[idx] == '1'):
            data.append(questionSwitchCaseIndex(idx)+" : Ya")
        if(array[idx] == '0'):
            data.append(questionSwitchCaseIndex(idx)+" : Tidak")

    return data

def questionSwitchCaseIndex(questionIndex):
    match questionIndex:
        case 0:
            return "Berapa Luas Lantai"
        case 1:
            return "Lantai Terbuat Dari tanah/ bambu/ kayu"
        case 2:
            return "Dinding terbuat dari bambu / rumbia / kayu / tembok tanpa plester"
        case 3:
            return "Buang air besar tanpa fasilitas / fasilitas bersama"
        case 4:
            return "Penerangan tanpa listrik"
        case 5:
            return "Air minum dari sumur / mata air tidak terlindungi / sungai / air hujan"
        case 6:
            return "Bahan bakar kayu bakar / arang / minyak tanah"
        case 7:
            return "Konsumsi daging / susu / ayam hanya 1 kali seminggu"
        case 8:
            return "Satu stel pakaian setahun"
        case 9:
            return "Makan 1-2 kali sehari"
        case 10:
            return "Tidak sanggup berobat ke puskesmas / poliklinik"
        case 11:
            return "Besaran penghasilan Kepala Keluarga Rp.600.000/bulan"
        case 12:
            return "Pendidikan Kepala Keluarga tidak sekolah / tidak tamat SD / tamat SD"
        case 13:
            return "Tidak memiliki tabungan / barang mudah dijual minimal Rp.500.000"
        case 14:
            return "Apakah ada anggota keluarga yang lanjut usia"
        case 15:
            return "Apakah ada anggota keluarga dengan kebutuhan khusus (disabilitas)"
        case 16:
            return "Apakah ada anak usia dini 0 s/d 6 tahun"
        case 17:
            return "Apakah ada kondisi ibu hamil/nifas"
        case 18:
            return "Apakah ada anak yang sedang bersekolah SD/sederajat"
        case 19:
            return "Apakah ada anak yang sedang bersekolah SMP/sederajat"
        case 20:
            return "Apakah ada anak yang sedang bersekolah SMA/sederajat"
        case _:
            return "Undefined Index"

def treeCheck(array):
    data = []

    #Right Node Of Tree
    if(array[13] == '0'):
        data.append("Tidak Punya Tabungan : Tidak")
        if(array[16] == '0'):
            data.append("Usia Dini : Tidak")
            return data
        if(array[16] == '1'):
            data.append("Usia Dini : Ya")
            if(array[11] == '1'):
                data.append("Penghasilan Dibawah 600Rb : Ya")
            if(array[11] == '0'):
                data.append("Penghasilan Dibawah 600Rb : Tidak")
                if(array[20] == '1'):
                    data.append("Anak SMA : Ya")
                    if(array[19] == '1'):
                        data.append("Anak SMP : Ya")
                        if(array[17] == '1'):
                            data.append("Ibu Hamil : Ya")
                            if(array[12] == '1'):
                                data.append("KK Tidak Sekolah : Ya")
                                if(data[3] == '0'):
                                    data.append("Tidak Punya MCK : Tidak")
                                    return data
                                if(data[3] == '1'):
                                    data.append("Tidak Punya MCK : Ya")
                                    if(data[0] == 1):
                                        data.append("Luas Lantai Lebih Kecil Dari 60m2 : Ya")
                                        return data
                                    if(data[0] == 0):
                                        data.append("Luas Lantai Lebih Kecil Dari 60m2 : Tidak")
                                        return data

                            if(array[12] == '0'):
                                data.append("KK Tidak Sekolah : Tidak")
                                if(array[18] == '1'):
                                    data.append("Anak SD : Ya")
                                    if(array[0] == 0):
                                        data.append("Luas Lantai Lebih Kecil Dari 60m2 : Tidak")
                                        return data
                                    if(array[0] == 1):
                                        data.append("Luas Lantai Lebih Kecil Dari 60m : Ya")
                                        if(array[2] == '0'):
                                            data.append("Dinding Bambu : Tidak")
                                            return data
                                        if(array[2] == '1'):
                                            data.append("Dinding Bambu : Ya")
                                            if(array[1] == '0'):
                                                data.append("Lantai Tanah : Tidak")
                                                return data
                                            if(array[1] == '1'):
                                                data.append ("Lantai Tanah : Ya")
                                                return data

                                if(array[18] == '0'):
                                    data.append("Anak SD : Tidak")
                                    if(array[15] == '0'):
                                        data.append("Disabilitas : Tidak")
                                        return data
                                    if(array[15] == '1'):
                                        data.append("Disabilitas : Ya")
                                        return data

                        if(array[17] == '0'):
                            data.append("Ibu Hamil : Tidak")
                            return data

                    if(array[19] == '0'):
                        data.append("Anak SMP: Tidak")
                        return data

                if(array[20] == '0'):
                    data.append("Anak SMA : Tidak")
                    if(array[3] == '1'):
                        data.append("Tidak punya mck : Ya")
                        return data
                    if(array[3] == '0'):
                        data.append("Tidak punya mck : Tidak")
                        return data


    #Left Node Of Tree            
    if(array[13] == '1'):
        data.append("Tidak Punya Tabungan : Ya")
        if(array[18] == '0'):
            data.append("Anak SD : Tidak")
            if(array[1] == '0'):
                data.append("Lantai Tanah : Tidak")
                if(array[11] == '1'):
                    data.append("Penghasilan Dibawah 600Rb : Ya")
                    return data
                if(array[11] == '0'):
                    data.append("Penghasilan Dibawah 600Rb : Tidak")
                    return data
            if(array[1] == '1'):
                data.append("Lantai Tanah : Ya")
                return data

        if(array[18] == '1'):
            data.append("Anak SD : Ya")
            if(array[20] == '0'):
                data.append("Anak SMA : Tidak")
                return data
            if(array[20] == '1'):
                data.append("Anak SMA : Ya")
                if(array[16] == '0'):
                    data.append("Usia Dini : Tidak")
                    if(array[1] == '0'):
                        data.append("Lantai Tanah : Tidak")
                        return data
                    if(array[1] == '1'):
                        data.append("Lantai Tanah : Ya")
                        return data
                if(array[16] == '1'):
                    data.append("Usia Dini : Ya")
                    if(array[19] == '0'):
                        data.append("Anak SMP : Tidak")
                        if(array[0] == 0):
                            data.append("Luas Lantai Lebih Kecil Dari 60m2 : Tidak")
                            return data
                        if(array[0] == 1):
                            data.append("Luas Lantai Lebih Kecil Dari 60m2 : Ya")
                            return data
                    if(array[19] == '1'):
                        data.append("Anak SMP : Ya")
                        if(array[17] == '0'):
                            data.append("Ibu Hamil : Tidak")
                            return data
                        if(array[17] == '1'):
                            data.append("Ibu Hamil : Ya")
                            if(array[11] == '1'):
                                data.append("Penghasilan Dibawah 600Rb : Ya")
                                return data
                            if(array[11] == '0'):
                                data.append("Penghasilan Dibawah 600Rb : Tidak")
                                if(array[0] == 0):
                                    data.append("Luas Lantai Lebih Kecil Dari 60m2 : Tidak")
                                    if(array[15] == '0'):
                                        data.append("Disabilitas : Tidak")
                                        return data
                                    if(array[15] == '1'):
                                        data.append("Disabilitas : Ya")
                                        return data
                                if(array[0] == 1):
                                    data.append("Luas Lantai Lebih Kecil Dari 60m2 : Ya")
                                    if(array[14] == '0'):
                                        data.append("Lansia : Tidak")
                                        if(array[1] == '0'):
                                            data.append("Lantai Tanah : Tidak")
                                            return data
                                        if(array[1] == '1'):
                                            data.append("Lantai Tanah : Ya")
                                            return data
                                    if(array[14] == '1'):
                                        data.append("Lansia : Ya")
                                        return data

#Run Main Program
if __name__ == '__main__':
    app.debug = True
    app.run()
                        