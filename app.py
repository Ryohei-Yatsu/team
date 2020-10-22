# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect

from datetime import datetime

# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')





@app.route("/post",methods=["GET"])
def post_get():
    return render_template("post.html")



@app.route("/post",methods=["POST"])
def post_post():
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    # htmlの入力フォームからデータを取ってきてサーバー側に送ってあげる
    comment = request.form.get("comment")
    discription = request.form.get("discription")
    genre_id = request.form.get("genre_id")
    # ④データベースに接続してtaskをカラムのtaskに入れてあげる。接続終了して最後に入力完了と表示させてあげる
    # dbtest.dbに接続
    conn = sqlite3.connect("tanka.db")
    # データベースの中身がみれるようにする
    c = conn.cursor()
    # SQL文を実行、(task)はタプル型なので「,」を入れる必要あり
    c.execute("insert into tanka values(null,?,?,?,?)",(comment,discription,genre_id,time))
    # 変更を加える
    conn.commit()
    # 取ってきたレコードを格納する
    user_info = c.fetchall()
    # 接続終了
    c.close()

    return "入力完了"




@app.route("/list")
def comment_list():
    # クッキーからuser_idを取得
    conn = sqlite3.connect('tanka.db')
    c = conn.cursor()
    # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
    # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
    c.execute("select * from tanka left outer join genre on tanka.genre_id= genre.id;  where id = ?" ,(genre_id,) )
    # fetchoneはタプル型
    genre_id = []
    for row in c.fetchall():
        comment_list.append({"id": row[0], "comment": row[1],"description":row[2],"genre_id":row[3]})

        c.close()
        return render_template('list.html' , user_info = user_info , comment_list = comment_list)
    else:
        return redirect("/list")



if __name__ == "__main__":
    # Flaskの開発者サーバーを使ってアプリを実行
    app.run(debug=True)