from flask import Flask, render_template
import pandas as pd
df = pd.read_csv("yurakucho.csv", encoding="shift-jis")
dg = pd.read_csv("hinan_tika.csv", encoding="shift-jis")

x = df["marker_lat"].mean()
y = df["marker_lng"].mean()
data1 = df.values
data2 = dg.values
app = Flask(__name__)
print("app")

@app.route("/")
def hello_world():
    print("/")
    dst = ""
    point = "\t\t\tvar mpoint = ["+ str(x) +", "+ str(y) +"];"
    for i in range(len(data1)):
        dst = dst + "\t\t\tL.marker(["+ str(data1[i][4]) +","+ str(data1[i][5]) +"],{title:\""+ data1[i][1].replace("\n", "").replace("\r", "") +"\"}).addTo(map);\n"
    return render_template("sample.html", dst=dst, point=point)

        for i in range(len(data2)):
        dst = dst + "\t\t\tL.marker(["+ str(data2[i][1]) +","+ str(data2[i][2]) +"],{title:\""+ data2[i][0].replace("\n", "").replace("\r", "") +"\"}).addTo(map);\n"
    return render_template("sample.html", dst=dst, point=point)
        

if __name__ == "__main__":
    app.run()
