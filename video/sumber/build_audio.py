import json,subprocess,os
SRC="/root/.claude/uploads/8675c1f7-f316-5d3a-9f38-491e66860ad9/788baa07-Suara_baru.mp3"
GAP=0.35; INTRO=4.6   # placeholder silent card for the missing Hakim line
segs=[ # who, src_start, src_end, [(a,b,text)]
("AMIR",0.0,10.40,[(0.00,3.06,"Entah kenapa kebelakangan ni aku asyik gelisah..."),(3.82,6.82,"Susah nak tidur, fikiran pun tak tenang."),(7.84,10.40,"Rasa macam terlalu banyak benda yang aku tanggung.")]),
("PAUSE",None,None,[]),
("AMIR",11.18,13.66,[(11.18,13.66,"Safron? Apa kaitannya dengan aku?")]),
("HAKIM",14.46,21.28,[(14.46,17.72,"Ibn Sina, tokoh perubatan Islam yang terkenal,"),(17.72,21.28,"pernah membincangkan safron dalam kitab perubatan beliau.")]),
("HAKIM",22.16,38.86,[(22.16,26.26,"Kitab ini ialah Al-Qanun fi al-Tibb, karya Ibn Sina."),(27.02,31.78,"Menurut satu kajian ilmiah dalam jurnal Phytotherapy Research pada tahun 2013,"),(32.86,38.86,"safron disenaraikan dalam kitab ini, termasuk penggunaan tradisionalnya sebagai bahan antikemurungan.")]),
("HAKIM",39.72,47.44,[(39.72,42.78,"Bayangkan... beratus-ratus tahun dahulu,"),(43.40,47.44,"safron sudah pun menjadi sebahagian daripada perbincangan ilmu perubatan.")]),
("HAKIM",48.40,56.26,[(48.40,52.50,"Dan hari ini, safron masih terus dikaji oleh para saintis,"),(52.50,56.26,"termasuk potensinya berkaitan mood dan kesejahteraan.")]),
("AMIR",56.84,59.42,[(56.84,59.42,"Rupanya banyak benda aku tak tahu tentang safron.")]),
("HAKIM",60.08,71.44,[(60.08,63.70,"Betul. Tapi ingat, safron bukan ubat ajaib."),(64.40,66.98,"Kalau kau rasa tertekan atau cemas berpanjangan,"),(67.46,69.02,"jangan pendam seorang diri."),(69.62,71.44,"Dapatkan bantuan profesional juga.")]),
("NARATOR",72.24,80.26,[(72.24,76.86,"Safron. Warisan yang telah dikenali sejak berabad-abad lamanya,"),(77.40,80.26,"dan kini terus diterokai oleh sains moden.")]),
]
t=0.0; tl=[]; inputs=[]; filt=[]
for i,(who,a,b,lines) in enumerate(segs):
    if who=="PAUSE":
        t+=0.65; continue
    if who=="INTRO":
        tl.append(dict(who="HAKIM",start=t,end=t+INTRO,subs=[dict(a=t+0.2,b=t+INTRO-0.2,text="Safron bukan sekadar rempah yang mahal. Dah lama ia dikenali dalam sejarah perubatan.")],silent=True))
        t+=INTRO+GAP; continue
    dur=b-a; off=t-a
    tl.append(dict(who=who,start=t,end=t+dur,subs=[dict(a=x+off,b=y+off,text=s) for x,y,s in lines]))
    f=f"seg/s{i}.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(a-0.06),"-to",str(b+0.12),"-i",SRC,"-ar","44100","-ac","2",f],check=True)
    inputs.append((f,t-0.06)); t+=dur+GAP
speech_end=tl[-1]["end"]; TOTAL=round(speech_end+3.8,2)
json.dump(dict(total=TOTAL,segs=tl),open("timeline.json","w"),indent=1)
# voice track
cmd=["ffmpeg","-y","-loglevel","error"]
for f,_ in inputs: cmd+=["-i",f]
fc=";".join(f"[{k}]adelay={int(max(0,s)*1000)}|{int(max(0,s)*1000)}[v{k}]" for k,(f,s) in enumerate(inputs))
fc+=";"+"".join(f"[v{k}]" for k in range(len(inputs)))+f"amix=inputs={len(inputs)}:normalize=0,volume=1.0,apad=whole_dur={TOTAL}[vo]"
cmd+=["-filter_complex",fc,"-map","[vo]","-t",str(TOTAL),"voice.wav"]
subprocess.run(cmd,check=True)
# ambient pad
pad=f"aevalsrc='0.5*sin(2*PI*110*t)+0.4*sin(2*PI*164.81*t)+0.3*sin(2*PI*220*t)+0.25*sin(2*PI*261.63*t+sin(2*PI*0.1*t))+0.15*sin(2*PI*329.63*t)':s=44100:d={TOTAL}"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i",pad,"-af",f"tremolo=f=0.15:d=0.4,lowpass=f=900,aecho=0.8:0.7:600:0.4,afade=t=in:d=3,afade=t=out:st={TOTAL-3}:d=3,volume=0.07","pad.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","voice.wav","-i","pad.wav","-filter_complex","[0][1]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]","-map","[a]","-c:a","aac","-b:a","192k","audio.m4a"],check=True)
print("TOTAL",TOTAL); [print(f"{s['who']:8s} {s['start']:.2f}-{s['end']:.2f}") for s in tl]
