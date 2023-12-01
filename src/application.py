from flask import Flask, render_template, request, redirect
import pandas as pd
import html

df = pd.read_csv("result2.csv", encoding="shift-jis")
x = df["marker_lat"].mean()
y = df["marker_lng"].mean()
data = df.values
application = Flask(__name__)
print("app")
#参考 https://ihoujin.nagoya/gait-speed/
apv = {
       "20e" : {"m" : 87.6, "w" : 74.1},
       "20l" : {"m" : 85.2, "w" : 74.2},
       "30e" : {"m" : 95.5, "w" : 72.2},
       "30l" : {"m" : 85.3, "w" : 67.2},
       "40e" : {"m" : 82.3, "w" : 71.0},
       "40l" : {"m" : 82.5, "w" : 78.6},
       "50e" : {"m" : 77.8, "w" : 67.2},
       "50l" : {"m" : 72.6, "w" : 63.5},
       "60e" : {"m" : 70.1, "w" : 59.2},
       "60l" : {"m" : 63.8, "w" : 59.8},
       "70e" : {"m" : 60.7, "w" : 55.0},
       "70l" : {"m" : 54.5, "w" : 50.7},
       }
#参考 https://nuclearsecrecy.com/nukemap/
bom = {"North Korea weapon tested in 2013(10kt)": {
        "r1" : {"dist" : 153},
        "r2" : {"dist" : 1050},
        "r3" : {"dist" : 1510},
        "r4" : {"dist" : 1530},
        "r5" : {"dist" : 5700}}
       ,
       "Little Boy - Hiroshima bomb(15kt)": {
        "r1" : {"dist" : 153},
        "r2" : {"dist" : 1050},
        "r3" : {"dist" : 1510},
        "r4" : {"dist" : 1530},
        "r5" : {"dist" : 4260}}
       ,
       "Fat man - Nagasaki bomb(20kt)": {
        "r1" : {"dist" : 760},
        "r2" : {"dist" : 1310},
        "r3" : {"dist" : 1720},
        "r4" : {"dist" : 2210},
        "r5" : {"dist" : 4590}}
        ,
        "virtual bomb(50kt)": {
        "r1" : {"dist" : 292},
        "r2" : {"dist" : 1160},
        "r3" : {"dist" : 2590},
        "r4" : {"dist" : 3200},
        "r5" : {"dist" : 7280}}
        ,
        "virtual bomb(100kt)": {
        "r1" : {"dist" : 560},
        "r2" : {"dist" : 1820},
        "r3" : {"dist" : 2120},
        "r4" : {"dist" : 3900},
        "r5" : {"dist" : 5460}}
        ,
        "virtual bomb(150kt)": {
        "r1" : {"dist" : 660},
        "r2" : {"dist" : 1940},
        "r3" : {"dist" : 2430},
        "r4" : {"dist" : 4670},
        "r5" : {"dist" : 6250}}
        ,
        "virtual bomb(200kt)": {
        "r1" : {"dist" : 740},
        "r2" : {"dist" : 2020},
        "r3" : {"dist" : 2680},
        "r4" : {"dist" : 5300},
        "r5" : {"dist" : 6880}}
        ,
        "virtual bomb(250kt)": {
        "r1" : {"dist" : 800},
        "r2" : {"dist" : 2090},
        "r3" : {"dist" : 2880},
        "r4" : {"dist" : 5840},
        "r5" : {"dist" : 7410}}
        ,
        "virtual bomb(300kt)": {
        "r1" : {"dist" : 870},
        "r2" : {"dist" : 2140},
        "r3" : {"dist" : 3060},
        "r4" : {"dist" : 6330},
        "r5" : {"dist" : 7880}}
        ,
        "virtual bomb(350kt)": {
        "r1" : {"dist" : 920},
        "r2" : {"dist" : 2190},
        "r3" : {"dist" : 3230},
        "r4" : {"dist" : 6770},
        "r5" : {"dist" : 8290}}
        ,
        "virtual bomb(400kt)": {
        "r1" : {"dist" : 970},
        "r2" : {"dist" : 2230},
        "r3" : {"dist" : 3370},
        "r4" : {"dist" : 7170},
        "r5" : {"dist" : 8670}}
        ,
        "virtual bomb(450kt)": {
        "r1" : {"dist" : 1020},
        "r2" : {"dist" : 2260},
        "r3" : {"dist" : 3510},
        "r4" : {"dist" : 7550},
        "r5" : {"dist" : 9020}}
        ,
        "virtual bomb(500kt)": {
        "r1" : {"dist" : 1060},
        "r2" : {"dist" : 2290},
        "r3" : {"dist" : 3630},
        "r4" : {"dist" : 7910},
        "r5" : {"dist" : 9340}}
       }
       
@application.route("/")
def hello_world():
    dst = ""
    point = "\t\t\tvar mpoint = ["+ html.escape(str(x)) +", "+ html.escape(str(y)) +"];"
    for i in range(len(data)):
        dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
    if request.args.get("err") is None:
        return render_template("sample.html", dst=dst, point=point)
    else:
        if request.args.get("err") == "null":
            return render_template("sample.html", dst=dst, point=point, err="<h2>緯度経度情報を埋めてください</h2>")
        if request.args.get("err") == "time":
            return render_template("sample.html", dst=dst, point=point, err="<h2>避難時間の中に地下に隠れる時間を含みます</h2>")

@application.route("/bomb")
def bomb():
    x = request.args.get("ido")
    y = request.args.get("kei")
    b = request.args.get("bomb")
    sx = request.args.get("sido")
    sy = request.args.get("skei")
    #dis = float(request.args.get("dis"))
    age = request.args.get("age")
    time = float(request.args.get("time"))
    sex = request.args.get("sex")
    hide = float(request.args.get("hide"))
    num = int(request.args.get("num"))
    if time < hide:
        return redirect("..?err=time")
    dis = (time - hide) * apv[age][sex]
    #term = int(request.args.get("term"))
    #term2 = int(request.args.get("term2"))
    if x == "" or y == "" or sx == "" or sy == "":
        return redirect("..?err=null")
    dst = ""
    point = "\t\t\tvar mpoint = ["+ html.escape(str(x)) +", "+ html.escape(str(y)) +"];"
    esc = []
    dgr = []
    dst = dst + "\t\t\tL.polyline([["+ html.escape(str(sx))+","+ html.escape(str(sy))+"],["+ html.escape(str(x)) +","+ html.escape(str(y)) +"]], { color: \"#FF0000\", weight: 5 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r1"]["dist"])) +", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r2"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r3"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r4"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r5"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.marker(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"],{ icon: redIcon }, {title:\"爆心地\"}).addTo(map);\n"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"], { radius: "+ html.escape(str(dis))+", color: \"#00FF00\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.marker(["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"],{ icon: bkIcon }, {title:\"指定座標\"}).addTo(map);\n"
    for i in range(len(data)):
        px = (float(data[i][4])-float(x))*111111
        py = (float(data[i][5])-float(y))*91000
        px2 = (float(data[i][4])-float(sx))*111111
        py2 = (float(data[i][5])-float(sy))*91000
        dist = (px**2 + py**2)**0.5
        news = ""
        if px2 > 0.0:
            news = news + "北"
        else:
            news = news + "南"
        if py2 > 0.0:
            news = news + "東"
        else:
            news = news + "西"
        if bom[b]["r1"]["dist"] > dist:
            dgr.append([data[i][1], data[i][4], data[i][5], dist])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{ icon: Icon45 },{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
        elif bom[b]["r2"]["dist"] > dist:
            dgr.append([data[i][1], data[i][4], data[i][5], dist])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{ icon: Icon90 },{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
        elif bom[b]["r3"]["dist"] > dist:
            dgr.append([data[i][1], data[i][4], data[i][5], dist])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{ icon: Icon135 },{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
        elif bom[b]["r4"]["dist"] > dist:
            #dgr.append([data[i][1], data[i][4], data[i][5], dist])
            esc.append([data[i][1], data[i][4], data[i][5], (px2**2 + py2**2)**0.5, abs(px2) + abs(py2), news])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{ icon: Icon180 },{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
        elif bom[b]["r5"]["dist"] > dist:
            esc.append([data[i][1], data[i][4], data[i][5], (px2**2 + py2**2)**0.5, abs(px2) + abs(py2), news])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{ icon: Icon225 },{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
        else:
            esc.append([data[i][1], data[i][4], data[i][5], (px2**2 + py2**2)**0.5, abs(px2) + abs(py2), news])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
    px = abs(float(x)-float(sx))*111111
    py = abs(float(y)-float(sy))*91000
    dist = (px**2 + py**2)**0.5
    state = "<br>避難可能距離:%.1f(m)<br>避難者の速度:%.1f(m/分)<br>"%(dis, apv[age][sex])
    if bom[b]["r1"]["dist"] > dist:
        state = state + "<h1>核火球の最大サイズ</h1>\n火の玉の中にあるものはすべて効果的に蒸発します"
    elif bom[b]["r2"]["dist"] > dist:
        state = state + "<h1>500レム電離放射線量</h1>\n約1か月以内に死亡する可能性が高い。 生存者の 15% は、被曝の結果、最終的に癌で死亡します。"
    elif bom[b]["r3"]["dist"] > dist:
        state = state + "<h1>中程度の爆発被害半径</h1>\nほとんどの住宅建物が倒壊し、死亡者が広範囲に発生します。 商業施設や住宅への被害から火災が発生する可能性が高く、被害が大きくなった建物は延焼の危険性が高くなります。"
    elif bom[b]["r4"]["dist"] > dist:
        state = state + "<h1>熱放射半径 (3度の熱傷)</h1>\n3度の熱傷は皮膚の層全体に広がり、痛みの神経を破壊するため、多くの場合痛みがありません。 重度の瘢痕化や障害を引き起こす可能性があり、切断が必要になる場合もあります。"
    elif bom[b]["r5"]["dist"] > dist:
        state = state + "<h1>光爆によるダメージ半径</h1>\nガラス窓が破損することが予想されます。 これにより、核爆発の閃光（圧力波よりも速く伝わる）を見た後に窓際に来た周囲の人々に多くの怪我を引き起こす可能性があります。"
    state = "爆心地から" + str(int(dist)) + "m" + state
    dst2 = ""
    if len(esc) == 0:
        return render_template("sample.html", ido=html.escape(str(x)), kei=html.escape(str(y)), sido=html.escape(str(sx)), skei=html.escape(str(sy)), dst=dst, point=point, state=state, dst2="<h2>避難可能不可能</h2>", bomb=b)
    df_esc = pd.DataFrame(esc)
    df_esc.columns = ["避難場所", "緯度", "経度", "避難所までの距離", "マンハッタン距離", "大まかな方角"]
    #df_esc = df_esc.query("避難所までの距離<%d"%(term))
    df_esc = df_esc.sort_values("避難所までの距離")
    esc = df_esc.head(num).values
    #if len(esc) != 0:
    dst2 = dst2 + "<h2>最適な避難所" + str(len(esc)) + "選</h2>"
    dst2 = dst2 + "<table border=1>\n"
    dst2 = dst2 + "\t<tr><th>避難場所</th><th>緯度</th><th>経度</th><th>避難所までの直線距離</th><th>マンハッタン距離</th><th>大まかな方角</th></tr>\n"
    for i in range(len(esc)):
        if esc[i][3] <= dis:
            dst = dst + "L.polyline([["+ html.escape(str(esc[i][1])) +","+ html.escape(str(esc[i][2]))+"],["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"]], { color: \"#008000\", weight: 5 }).addTo(map);"
            dst2 = dst2 + "\t<tr><td>"+ html.escape(str(esc[i][0])) +"</td><td>"+ html.escape(str(esc[i][1])) +"</td><td>"+ html.escape(str(esc[i][2])) +"</td><td>"+ html.escape(str(int(esc[i][3]))) +"m</td><td>"+ html.escape(str(int(esc[i][4]))) +"m</td><td>"+ html.escape(str(esc[i][5])) +"</td></tr>\n"
        else:
            dst = dst + "L.polyline([["+ html.escape(str(esc[i][1])) +","+ html.escape(str(esc[i][2]))+"],["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"]], { color: \"#000000\", weight: 5 }).addTo(map);"
            dst2 = dst2 + "\t<tr><td><font color=\"#FF0000\">"+ html.escape(str(esc[i][0])) +"</font></td><td>"+ html.escape(str(esc[i][1])) +"</td><td>"+ html.escape(str(esc[i][2])) +"</td><td>"+ html.escape(str(int(esc[i][3]))) +"m</td><td>"+ html.escape(str(int(esc[i][4]))) +"m</td><td>"+ html.escape(str(esc[i][5])) +"</td></tr>\n"
    dst2 = dst2 + "</table>"
    #else:
    #    dst2 = dst2 + "<h2>圏内に避難可能な場所がありません</h2>"
    dst2 = dst2 + "<h2>危険な避難所</h2>\n"
    dst2 = dst2 + "<table border=1>\n"
    dst2 = dst2 + "\t<tr><th>避難所</th><th>爆心地までの距離</th></tr>\n"
    for i in range(len(dgr)):
        dst2 = dst2 + "\t<tr><td>"+ html.escape(str(dgr[i][0])) +"</td><td>"+ html.escape(str(int(dgr[i][3]))) +"m</td></tr>\n"
    dst2 = dst2 + "</table>"
    return render_template("sample.html", ido=html.escape(str(x)), kei=html.escape(str(y)), sido=html.escape(str(sx)), skei=html.escape(str(sy)), dst=dst, point=point, state=state, dst2=dst2, bomb=b)
    
if __name__ == "__main__":
    application.run()
