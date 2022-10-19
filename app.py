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
        luas_lantai = 0
    else :
        luas_lantai = 1       
    data = [
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
    predicted = modelload.predict([data])
    finaldata = json.dumps(predicted.tolist())
    result = finaldata[1]
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
    return render_template('result.html', title=title, data=data, icon=icon)



if __name__ == '__main__':
    app.debug = True
    app.run()
