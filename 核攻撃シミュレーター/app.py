from flask import Flask, render_template, request, redirect
import pandas as pd
import html
#----------------------------------------------------------------
# データの読み込み
df = pd.read_csv("result2.csv", encoding="shift-jis")
x = df["marker_lat"].mean()
y = df["marker_lng"].mean()
#----------------------------------------------------------------

# データの配列化
data = df.values

app = Flask(__name__)
print("app")

#----------------------------------------------------------------
# 核爆弾の連想配列
bom = {"North Korea weapon tested in 2013(10kt)": {
        "r1" : {"dist" : 153},#核火球の最大サイズ
        "r2" : {"dist" : 1050},#500レム電離放射線
        "r3" : {"dist" : 1510},#中程度の爆発被害半径
        "r4" : {"dist" : 1530},#熱放射半径 (3度の熱傷)
        "r5" : {"dist" : 4260}}#光爆によるダメージ半径
       ,
       "Little Boy - Hiroshima bomb(15kt)": {
        "r1" : {"dist" : 339},
        "r2" : {"dist" : 1200},
        "r3" : {"dist" : 1670},
        "r4" : {"dist" : 1910},
        "r5" : {"dist" : 4520}}
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
       }
       
#----------------------------------------------------------------
@app.route("/")
def hello_world():
    dst = "" #出力結果
    point = "\t\t\tvar mpoint = ["+ html.escape(str(x)) +", "+ html.escape(str(y)) +"];" #中心座標(全座標の重心(平均値))
    for i in range(len(data)):
        #避難所のマーカー
        dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
    #-------------------------------------------------------------
    #エラー対応
    #正常の場合
    if request.args.get("err") is None:
        return render_template("sample.html", dst=dst, point=point)
    #エラーが送られた場合
    else:
        #エラー内容が入力不足
        if request.args.get("err") == "null":
            return render_template("sample.html", dst=dst, point=point, err="<h2>緯度経度情報を埋めてください</h2>")
    #-------------------------------------------------------------

@app.route("/bomb")
def bomb():
    #-------------------------------------------------------------
    #URLパラメータ
    x = request.args.get("ido")#爆心地の緯度
    y = request.args.get("kei")#爆心地の経度
    b = request.args.get("bomb")#爆弾の種類
    sx = request.args.get("sido")#観測者の緯度
    sy = request.args.get("skei")#観測者の経度
    #-------------------------------------------------------------
    if x == "" or y == "" or sx == "" or sy == "":#情報が不足している場合
        return redirect("..?err=null")#ホーム画面にリダイレクト
    dst = ""#JavaScritの出力内容
    point = "\t\t\tvar mpoint = ["+ html.escape(str(x)) +", "+ html.escape(str(y)) +"];"#中心座標(爆心地)
    esc = []#安全な避難所情報
    dgr = []#危険な避難所情報
    #爆心地から観測者を直線で結ぶ
    dst = dst + "\t\t\tL.polyline([["+ html.escape(str(sx))+","+ html.escape(str(sy))+"],["+ html.escape(str(x)) +","+ html.escape(str(y)) +"]], { color: \"#FF0000\", weight: 5 }).addTo(map);"
    #爆心地から被害の程度を円で表示
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r1"]["dist"])) +", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r2"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r3"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r4"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r5"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);"
    #爆心地をマーカーで表示
    dst = dst + "\t\t\tL.marker(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"],{ icon: redIcon }, {title:\"爆心地\"}).addTo(map);\n"
    #観測値をマーカーで表示
    dst = dst + "\t\t\tL.marker(["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"],{ icon: bkIcon }, {title:\"指定座標\"}).addTo(map);\n"
    for i in range(len(data)):
        px = (float(data[i][4])-float(x))*111111#避難所から爆心地の緯度による距離
        py = (float(data[i][5])-float(y))*91000#避難所から爆心地の経度による距離
        px2 = (float(data[i][4])-float(sx))*111111#避難所から観測地の緯度による距離
        py2 = (float(data[i][5])-float(sy))*91000#避難所から観測地の経度による距離
        dist = (px**2 + py**2)**0.5#爆心地から避難所の距離を計算
        #大まかな東西南北判定
        news = ""
        if px2 > 0.0:
            news = news + "北"
        else:
            news = news + "南"
        if py2 > 0.0:
            news = news + "東"
        else:
            news = news + "西"
        #避難所の内外判定　避難所までの距離がr5より大きければ安全圏で、それ以外は危険
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
            dgr.append([data[i][1], data[i][4], data[i][5], dist])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{ icon: Icon180 },{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
        elif bom[b]["r5"]["dist"] > dist:
            esc.append([data[i][1], data[i][4], data[i][5], (px2**2 + py2**2)**0.5, news])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{ icon: Icon225 },{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
        else:
            esc.append([data[i][1], data[i][4], data[i][5], (px2**2 + py2**2)**0.5, news])
            dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
    #爆心地から観測地の距離を計測
    px = abs(float(x)-float(sx))*111111
    py = abs(float(y)-float(sy))*91000
    dist = (px**2 + py**2)**0.5
    #観測地の被害状況を考察
    state = ""
    if bom[b]["r1"]["dist"] > dist:
        state = "<h1>重爆破半径</h1>\n20 psi の過圧では、頑丈に建てられたコンクリートの建物が深刻な損傷を受けるか取り壊されます。死亡率は100%に近づきます。都市における大きな被害のベンチマークとしてよく使用されます。この効果を最大化する最適な爆発の高さは494  mです。"
    elif bom[b]["r2"]["dist"] > dist:
        state = "<h1>500レム電離放射線量</h1>\n約1か月以内に死亡する可能性が高い。 生存者の 15% は、被曝の結果、最終的に癌で死亡します。"
    elif bom[b]["r3"]["dist"] > dist:
        state = "<h1>中程度の爆発被害半径</h1>\nほとんどの住宅建物が倒壊し、死亡者が広範囲に発生します。 商業施設や住宅への被害から火災が発生する可能性が高く、被害が大きくなった建物は延焼の危険性が高くなります。"
    elif bom[b]["r4"]["dist"] > dist:
        state = "<h1>熱放射半径 (3度の熱傷)</h1>\n3度の熱傷は皮膚の層全体に広がり、痛みの神経を破壊するため、多くの場合痛みがありません。 重度の瘢痕化や障害を引き起こす可能性があり、切断が必要になる場合もあります。"
    elif bom[b]["r5"]["dist"] > dist:
        state = "<h1>光爆によるダメージ半径</h1>\nガラス窓が破損することが予想されます。 これにより、核爆発の閃光（圧力波よりも速く伝わる）を見た後に窓際に来た周囲の人々に多くの怪我を引き起こす可能性があります。"
    state = "爆心地から" + str(int(dist)) + "m" + state
    #最適な避難所を表で表示
    dst2 = ""
    dst2 = dst2 + "<h2>最適な避難所5選</h2>"
    dst2 = dst2 + "<table border=1>\n"
    dst2 = dst2 + "\t<tr><th>避難場所</th><th>緯度</th><th>経度</th><th>避難所までの距離</th><th>大まかな方角</th></tr>\n"
    df_esc = pd.DataFrame(esc)#ソートと最初5つを簡単に取り出すためにデータフレーム化
    df_esc.columns = ["避難場所", "緯度", "経度", "避難所までの距離", "大まかな方角"]
    df_esc = df_esc.sort_values("避難所までの距離")
    esc = df_esc.head().values
    for i in range(len(esc)):
        #避難所と観測地の直線
        dst = dst + "L.polyline([["+ html.escape(str(esc[i][1])) +","+ html.escape(str(esc[i][2]))+"],["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"]], { color: \"#000000\", weight: 5 }).addTo(map);"
        #安全な避難所の情報を表示
        dst2 = dst2 + "\t<tr><td>"+ html.escape(str(esc[i][0])) +"</td><td>"+ html.escape(str(esc[i][1])) +"</td><td>"+ html.escape(str(esc[i][2])) +"</td><td>"+ html.escape(str(int(esc[i][3]))) +"m</td><td>"+ html.escape(str(esc[i][4])) +"</td></tr>\n"
    dst2 = dst2 + "</table>"
    #危険な避難所情報を表で表示
    dst2 = dst2 + "<h2>危険な避難所</h2>\n"
    dst2 = dst2 + "<table border=1>\n"
    dst2 = dst2 + "\t<tr><th>避難所</th><th>爆心地までの距離</th></tr>\n"
    for i in range(len(dgr)):
        dst2 = dst2 + "\t<tr><td>"+ html.escape(str(dgr[i][0])) +"</td><td>"+ html.escape(str(int(dgr[i][3]))) +"m</td></tr>\n"
    dst2 = dst2 + "</table>"
    return render_template("sample.html", dst=dst, point=point, state=state, dst2=dst2, bomb=b)
    
if __name__ == "__main__":
    app.run()
